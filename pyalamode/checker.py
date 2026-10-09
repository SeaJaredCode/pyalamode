"""Closed scalar checker. Application code is parsed, never imported or evaluated."""

from __future__ import annotations

import ast
import hashlib
import io
import json
import tokenize
from dataclasses import dataclass
from pathlib import Path

from .model import (CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, CheckResult,
                    FunctionContract, SCALARS, diagnostic, foundation_identities)

BUILTINS = frozenset({"abs", "min", "max", "len"})
_UNKNOWN = object()


def fingerprint(source: bytes, policy: dict | None = None) -> str:
    """Include source, edition, rules, target, policy, and operation identities."""
    metadata = json.dumps({"rules": CHECKER_VERSION, "edition": EDITION, "target": TARGET,
                           "operations": OPERATION_VERSION, "policy": policy or {},
                           "dependencies": ["pyalamode.fun@0.1.0", "CPython3.13.1 scalar builtins"],
                           "product_artifacts": foundation_identities()},
                          sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(metadata + b"\0" + source).hexdigest()


@dataclass(frozen=True)
class Value:
    types: frozenset[str]
    literal: object = _UNKNOWN

    @classmethod
    def exact(cls, kind: str, literal: object = _UNKNOWN) -> Value:
        return cls(frozenset({kind}), literal)

    @property
    def kind(self) -> str | None:
        return next(iter(self.types)) if len(self.types) == 1 else None


UNKNOWN = Value(frozenset())


@dataclass(frozen=True)
class Binding:
    value: Value
    first: tuple[int, ...]
    definite: bool = True


def _target_names(node: ast.AST) -> list[str]:
    return [n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)]


def _written_names(body: list[ast.stmt]) -> dict[str, list[ast.AST]]:
    """All writes in this lexical scope, including writes in compound statements."""
    output: dict[str, list[ast.AST]] = {}

    def add(name: str, node: ast.AST) -> None:
        output.setdefault(name, []).append(node)

    def walk(node: ast.AST) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            add(node.name, node)
            outside = list(node.decorator_list)
            if isinstance(node, ast.ClassDef):
                outside += node.bases + [keyword.value for keyword in node.keywords]
            else:
                outside += node.args.defaults + [value for value in node.args.kw_defaults if value]
                outside += [a.annotation for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs if a.annotation]
                if node.returns:
                    outside.append(node.returns)
            for expression in outside:
                walk(expression)
            return
        if isinstance(node, ast.Lambda):
            for expression in node.args.defaults + [value for value in node.args.kw_defaults if value]:
                walk(expression)
            return
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            values = [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
            values += [value for generator in node.generators for value in [generator.iter, *generator.ifs]]
            for value in values:
                walk(value)
            return
        if isinstance(node, ast.Import):
            for alias in node.names:
                add(alias.asname or alias.name.split(".")[0], node)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                add(alias.asname or alias.name, node)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            add(node.id, node)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            add(node.name, node)
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
            add(node.name, node)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            add(node.rest, node)
        for child in ast.iter_child_nodes(node):
            walk(child)

    for statement in body:
        walk(statement)
    return output


class ScalarAnalyzer:
    """One file's discovery, participating functions, and inspected ordinary calls."""

    def __init__(self, source: str, path: str, mode: str = "strict", policy: dict | None = None):
        self.source = source
        self.path = path
        self.result = CheckResult(path, fingerprint(source.encode(), policy), mode=mode)
        self.boundary = "<module>"
        self.failures: set[str] = set()
        self.locals: set[str] = set()
        self.in_dead = False
        self.global_writes: dict[str, list[ast.AST]] = {}
        self.marker_names: set[str] = set()
        self.marker_modules: set[str] = set()
        self.marker_imports: dict[str, ast.AST] = {}
        self.module_imports: dict[str, ast.AST] = {}
        self.none_imports: dict[str, ast.AST] = {}
        self.changed_attributes: set[tuple[str, str]] = set()
        self.module_aliases: dict[str, str] = {}
        self.namespace_aliases: set[str] = set()
        self.contracts: dict[str, FunctionContract] = {}
        self.selected_nodes: set[int] = set()

    def emit(self, rule: str, node: ast.AST, reason: str, *, first: int | None = None,
             origin: str = "static source") -> None:
        self.result.diagnostics.append(diagnostic(
            rule, self.path, reason, line=getattr(node, "lineno", 1),
            column=getattr(node, "col_offset", 0) + 1, boundary=self.boundary, origin=origin,
            first_binding=f"{self.path}:{first}" if first is not None else None))

    def _stable(self, name: str, imported: ast.AST) -> bool:
        return self.global_writes.get(name) == [imported]

    def _marker_like(self, node: ast.expr) -> bool:
        if isinstance(node, ast.Call):
            return self._marker_like(node.func)
        return ((isinstance(node, ast.Name) and node.id in self.marker_names) or
                (isinstance(node, ast.Attribute) and node.attr == "fun" and isinstance(node.value, ast.Name)
                 and node.value.id in self.marker_modules))

    def _marker_valid(self, node: ast.expr) -> bool:
        if isinstance(node, ast.Name):
            imported = self.marker_imports.get(node.id)
            return (imported is not None and self._stable(node.id, imported)
                    and not self._attribute_changed("pyalamode", "fun"))
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.attr == "fun":
            imported = self.module_imports.get(node.value.id)
            return (imported is not None and self._stable(node.value.id, imported)
                    and not self._attribute_changed("pyalamode", "fun"))
        return False

    def _annotation(self, node: ast.expr | None) -> str | None:
        original = node
        if isinstance(node, ast.Constant) and type(node.value) is str:
            try:
                node = ast.parse(node.value, mode="eval").body
            except (SyntaxError, ValueError):
                node = None
        kind = None
        if isinstance(node, ast.Constant) and node.value is None:
            kind = "None"
        elif isinstance(node, ast.Name):
            if (node.id in {"bool", "int", "str", "bytes"} and node.id not in self.global_writes
                    and not self._attribute_changed("builtins", node.id)):
                kind = node.id
            elif (node.id in self.none_imports and self._stable(node.id, self.none_imports[node.id])
                  and not self._attribute_changed("types", "NoneType")):
                kind = "None"
        if kind is None:
            self.emit("PAL130", original or ast.Constant(value=None),
                      "annotation must identify an unshadowed exact scalar type")
        return kind

    def analyze(self) -> CheckResult:
        try:
            tree = ast.parse(self.source, filename=self.path, feature_version=(3, 13))
        except (SyntaxError, ValueError) as error:
            self.result.diagnostics.append(diagnostic("PAL001", self.path, str(error),
                                          line=getattr(error, "lineno", 1) or 1))
            return self.result
        self.global_writes = _written_names(tree.body)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # An explicit global write in ordinary source cannot silently replace a dependency.
                global_names = {name for sub in ast.walk(node) if isinstance(sub, ast.Global) for name in sub.names}
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Name) and isinstance(sub.ctx, (ast.Store, ast.Del)) and sub.id in global_names:
                        self.global_writes.setdefault(sub.id, []).append(sub)
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)):
                targets = (node.targets if isinstance(node, (ast.Assign, ast.Delete)) else [node.target])
                for target in targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        self.changed_attributes.add((target.value.id, target.attr))
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "pyalamode" and node.level == 0:
                for alias in node.names:
                    if alias.name == "fun":
                        name = alias.asname or "fun"
                        self.marker_names.add(name)
                        self.marker_imports[name] = node
            if isinstance(node, ast.ImportFrom) and node.module == "types" and node.level == 0:
                for alias in node.names:
                    if alias.name == "NoneType":
                        self.none_imports[alias.asname or "NoneType"] = node
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "pyalamode":
                        name = alias.asname or "pyalamode"
                        self.marker_modules.add(name)
                        self.module_imports[name] = node
                    if alias.name in {"pyalamode", "builtins", "types"}:
                        self.module_aliases[alias.asname or alias.name] = alias.name
        changed = True
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in {"pyalamode", "builtins", "types"}:
                        self.module_aliases[alias.asname or alias.name] = alias.name
        while changed:
            changed = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name) and node.value.id in self.module_aliases:
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id not in self.module_aliases:
                            self.module_aliases[target.id] = self.module_aliases[node.value.id]
                            changed = True
        self.marker_modules.update(name for name, module in self.module_aliases.items() if module == "pyalamode")
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id in {"globals", "vars"} and not node.value.args:
                self.namespace_aliases.update(name for target in node.targets for name in _target_names(target))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Delete)):
                targets = node.targets if isinstance(node, (ast.Assign, ast.Delete)) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Subscript):
                        namespace = target.value
                        direct = isinstance(namespace, ast.Call) and isinstance(namespace.func, ast.Name) and namespace.func.id in {"globals", "vars"} and not namespace.args
                        alias = isinstance(namespace, ast.Name) and namespace.id in self.namespace_aliases
                        if direct or alias:
                            name = target.slice.value if isinstance(target.slice, ast.Constant) and type(target.slice.value) is str else "*"
                            self.global_writes.setdefault(name, []).append(target)
                        if isinstance(namespace, ast.Attribute) and namespace.attr == "__dict__" and isinstance(namespace.value, ast.Name):
                            name = target.slice.value if isinstance(target.slice, ast.Constant) and type(target.slice.value) is str else "*"
                            self.changed_attributes.add((namespace.value.id, name))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"setattr", "delattr"} and len(node.args) >= 2 and isinstance(node.args[0], ast.Name):
                attr = node.args[1].value if isinstance(node.args[1], ast.Constant) and type(node.args[1].value) is str else "*"
                self.changed_attributes.add((node.args[0].id, attr))
        if "*" in self.global_writes:
            self.emit("PAL240", self.global_writes["*"][0], "star imports or dynamic namespace writes leave approved bindings unresolved")
        # M1 intentionally does not implement module mode or policy-selected modules.
        for token in tokenize.generate_tokens(io.StringIO(self.source).readline):
            if token.type == tokenize.COMMENT and token.string.strip() == "# mode: fun":
                self.result.diagnostics.append(diagnostic("PAL120", self.path,
                    "module mode requires the functional-modules milestone", line=token.start[0]))
        parents = {id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        selected = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.result.eligible_functions += 1
                if any(self._marker_like(d) for d in node.decorator_list):
                    self.result.selected_functions += 1
                    self.selected_nodes.add(id(node))
                    selected.append(node)
                    if parents.get(id(node)) is not tree:
                        self.boundary = node.name
                        self.emit("PAL120", node, "only top-level functions participate in the scalar milestone")
        for node in selected:
            self._function(node)
        self._ordinary_calls(tree)
        if self.result.mode == "audit" or self.result.diagnostics:
            for contract in self.result.contracts:
                contract.enforcement = self.result.mode
                contract.source_evidence = "unverified: audit or failed selected gate"
                contract.freshness = "no successful checked claim"
        self.result.diagnostics.sort(key=lambda d: (d.line, d.column, d.rule))
        return self.result

    def _function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.boundary = node.name
        self.failures = set()
        if isinstance(node, ast.AsyncFunctionDef):
            self.emit("PAL120", node, "async functions are outside the scalar subset")
        if self.global_writes.get(node.name) != [node]:
            self.emit("PAL240", node, f"participating export `{node.name}` has another analyzed binding")
        if len(node.decorator_list) != 1 or not self._marker_valid(node.decorator_list[0]):
            self.emit("PAL120", node, "participation requires one unchanged, statically resolved pyalamode.fun identity marker")
        if node.args.defaults or any(d is not None for d in node.args.kw_defaults):
            self.emit("PAL120", node, "defaults are unsupported and have not been evaluated")
        if node.args.vararg or node.args.kwarg or getattr(node, "type_params", []):
            self.emit("PAL120", node, "variadic parameters and type parameters are unsupported")
        arguments = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
        self.locals = set(_written_names(node.body)) | {arg.arg for arg in arguments}
        env: dict[str, Binding] = {}
        parameters = {}
        kinds = {}
        for arg in arguments:
            kind = self._annotation(arg.annotation)
            if kind:
                parameters[arg.arg] = kind
            env[arg.arg] = Binding(Value.exact(kind) if kind else UNKNOWN, (arg.lineno,))
            kinds[arg.arg] = ("positional_only" if arg in node.args.posonlyargs else
                              "keyword_only" if arg in node.args.kwonlyargs else "positional_or_keyword")
        returns = self._annotation(node.returns)
        self.return_type = returns
        continuing = self._block(node.body, env)
        if continuing is not None and returns != "None":
            self.emit("PAL211", node, "a completing path falls through with None instead of the declared result")
        contract = FunctionContract(node.name, self.path, node.lineno, parameters, returns, kinds,
                                    failures=sorted(self.failures))
        contract.caller_obligations = [f"{name}: exact {kind}, with no subclasses" for name, kind in parameters.items()]
        contract.caller_obligations.extend([
            "Approved builtin, marker, annotation, and function bindings remain unchanged during execution.",
            "Ordinary callers receive no runtime input guards or purity claim.",
            "Resource exhaustion and interruption are outside the characterized failures.",
        ])
        self.result.contracts.append(contract)
        self.contracts[node.name] = contract

    def _merge(self, left: dict[str, Binding] | None, right: dict[str, Binding] | None) -> dict[str, Binding] | None:
        if left is None:
            return right
        if right is None:
            return left
        merged = {}
        for name in left.keys() | right.keys():
            a, b = left.get(name), right.get(name)
            if a and b:
                literal = a.value.literal if a.value.literal is not _UNKNOWN and type(a.value.literal) is type(b.value.literal) and a.value.literal == b.value.literal else _UNKNOWN
                merged[name] = Binding(Value(a.value.types | b.value.types, literal), tuple(sorted(set(a.first + b.first))), a.definite and b.definite)
            else:
                binding = a or b
                merged[name] = Binding(binding.value, binding.first, False)
        return merged

    def _block(self, body: list[ast.stmt], env: dict[str, Binding]) -> dict[str, Binding] | None:
        current: dict[str, Binding] | None = dict(env)
        dead_env = dict(env)
        for statement in body:
            if current is None:
                dead_env = self._dead_surface(statement, dead_env)
                continue
            dead_env = dict(current)
            current = self._statement(statement, current)
        return current

    def _dead_surface(self, node: ast.AST, env: dict[str, Binding]) -> dict[str, Binding]:
        # Type/declaration/operation rules still apply to the closed source vocabulary.
        # Only reachable single-assignment obligations are disabled in this traversal.
        previous = self.in_dead
        self.in_dead = True
        try:
            body = node.body if isinstance(node, ast.Module) else [node]
            result = self._block(body, env)
            return result if result is not None else env
        finally:
            self.in_dead = previous

    def _statement(self, node: ast.stmt, env: dict[str, Binding]) -> dict[str, Binding] | None:
        if isinstance(node, ast.Pass):
            return env
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = self._expr(node.value, env) if node.value is not None else UNKNOWN
            if len(targets) != 1 or not isinstance(targets[0], ast.Name) or node.value is None:
                self.emit("PAL110", node, "a binding requires one local name and one initialization expression")
                return env
            name = targets[0].id
            if name in env and not self.in_dead:
                self.emit("PAL101", node, f"`{name}` is already initialized on a reachable path", first=env[name].first[0])
            else:
                env[name] = Binding(value, (node.lineno,))
            if isinstance(node, ast.AnnAssign):
                expected = self._annotation(node.annotation)
                if expected and value.kind != expected:
                    self.emit("PAL210", node, f"binding `{name}` requires exact {expected}; found {self._describe(value)}")
            return env
        if isinstance(node, ast.AugAssign):
            name = node.target.id if isinstance(node.target, ast.Name) else "target"
            binding = env.get(name)
            self.emit("PAL101", node, f"augmented assignment reinitializes `{name}`", first=binding.first[0] if binding else None)
            return env
        if isinstance(node, ast.If):
            condition = self._expr(node.test, env)
            if condition.kind != "bool":
                self.emit("PAL210", node.test, f"branch condition requires exact bool; found {self._describe(condition)}")
            if condition.literal is True:
                self._dead_surface(ast.Module(body=node.orelse, type_ignores=[]), env)
                return self._block(node.body, env)
            if condition.literal is False:
                self._dead_surface(ast.Module(body=node.body, type_ignores=[]), env)
                return self._block(node.orelse, env)
            return self._merge(self._block(node.body, env), self._block(node.orelse, env))
        if isinstance(node, ast.Return):
            value = self._expr(node.value, env) if node.value else Value.exact("None", None)
            if value.kind != self.return_type:
                self.emit("PAL211", node, f"return requires exact {self.return_type}; found {self._describe(value)}")
            return None
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
            # A docstring has ordinary Python semantics and no dispatch.
            return env
        self.emit("PAL110", node, f"{type(node).__name__} is outside the scalar statement vocabulary")
        return env

    @staticmethod
    def _describe(value: Value) -> str:
        return " or ".join(sorted(value.types)) if value.types else "unknown/unsupported value"

    def _expr(self, node: ast.expr, env: dict[str, Binding], *, quiet: bool = False) -> Value:
        def reject(rule: str, reason: str) -> Value:
            if not quiet:
                self.emit(rule, node, reason)
            return UNKNOWN

        if isinstance(node, ast.Constant):
            kind = "None" if node.value is None else type(node.value).__name__
            return Value.exact(kind, node.value) if kind in SCALARS else reject("PAL201", f"{kind} literals are unsupported")
        if isinstance(node, ast.Name):
            binding = env.get(node.id)
            if binding:
                if not binding.definite:
                    return reject("PAL102", f"`{node.id}` is not initialized on every continuing path")
                return binding.value
            if node.id in self.locals:
                return reject("PAL102", f"local `{node.id}` is used before initialization")
            return reject("PAL240", f"ambient binding `{node.id}` is not an admitted scalar dependency")
        if isinstance(node, ast.UnaryOp):
            operand = self._expr(node.operand, env, quiet=quiet)
            expected = "bool" if isinstance(node.op, ast.Not) else "int"
            allowed = isinstance(node.op, (ast.Not, ast.UAdd, ast.USub))
            if not allowed or operand.kind != expected:
                return reject("PAL210", f"{type(node.op).__name__} requires its characterized exact {expected} operand")
            literal = (not operand.literal) if isinstance(node.op, ast.Not) and type(operand.literal) is bool else _UNKNOWN
            return Value.exact(expected, literal)
        if isinstance(node, ast.BinOp):
            left, right = self._expr(node.left, env, quiet=quiet), self._expr(node.right, env, quiet=quiet)
            kind = left.kind
            allowed = (kind == "int" and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod)) or
                       kind in {"str", "bytes"} and isinstance(node.op, ast.Add))
            if not allowed or kind != right.kind:
                return reject("PAL210", f"{type(node.op).__name__} is uncharacterized for {self._describe(left)} and {self._describe(right)}")
            if isinstance(node.op, (ast.FloorDiv, ast.Mod)) and not quiet:
                self.failures.add("ZeroDivisionError")
            return Value.exact(kind)
        if isinstance(node, ast.BoolOp):
            values = [self._expr(value, env, quiet=quiet) for value in node.values]
            if any(value.kind != "bool" for value in values):
                return reject("PAL210", "and/or require exact boolean operands")
            return Value.exact("bool")
        if isinstance(node, ast.Compare):
            previous = self._expr(node.left, env, quiet=quiet)
            for operator, comparator in zip(node.ops, node.comparators):
                value = self._expr(comparator, env, quiet=quiet)
                if isinstance(operator, (ast.Is, ast.IsNot)):
                    valid = isinstance(comparator, ast.Constant) and comparator.value is None and bool(previous.types)
                else:
                    valid = previous.kind == value.kind and (
                        previous.kind in {"int", "str", "bytes"} and isinstance(operator, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)) or
                        previous.kind == "bool" and isinstance(operator, (ast.Eq, ast.NotEq)))
                if not valid:
                    return reject("PAL210", f"comparison {type(operator).__name__} is uncharacterized for these exact operands")
                previous = value
            return Value.exact("bool")
        if isinstance(node, ast.IfExp):
            condition = self._expr(node.test, env, quiet=quiet)
            yes, no = self._expr(node.body, env, quiet=quiet), self._expr(node.orelse, env, quiet=quiet)
            if condition.kind != "bool":
                return reject("PAL210", "conditional expression requires an exact boolean condition")
            return Value(yes.types | no.types)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in BUILTINS:
                return reject("PAL230", "call target is not an approved scalar builtin (checked call graphs are not yet admitted)")
            name = node.func.id
            if name in self.locals or name in self.global_writes:
                return reject("PAL240", f"approved builtin `{name}` is shadowed by an analyzed binding")
            if self._attribute_changed("builtins", name):
                return reject("PAL240", f"approved builtin `{name}` has an analyzed attribute replacement")
            if node.keywords or any(isinstance(a, ast.Starred) for a in node.args):
                return reject("PAL230", f"{name} admits only its published direct positional signature")
            values = [self._expr(arg, env, quiet=quiet) for arg in node.args]
            kinds = [value.kind for value in values]
            if name == "abs" and kinds == ["int"]:
                return Value.exact("int")
            if name == "len" and len(kinds) == 1 and kinds[0] in {"str", "bytes"}:
                return Value.exact("int")
            if name in {"min", "max"} and len(kinds) >= 2 and len(set(kinds)) == 1 and kinds[0] in {"int", "str", "bytes"}:
                return Value.exact(kinds[0])
            return reject("PAL210", f"{name} arguments do not establish its exact supported scalar signature")
        return reject("PAL201", f"{type(node).__name__} is outside the scalar expression vocabulary")

    def _attribute_changed(self, module: str, attribute: str) -> bool:
        return any((name, attribute) in self.changed_attributes or (name, "*") in self.changed_attributes
                   for name, resolved in self.module_aliases.items() if resolved == module)

    def _ordinary_calls(self, tree: ast.Module) -> None:
        """Inspect direct same-file export calls/aliases, without certifying shell behavior.

        Only closed scalar expressions and single stable prior ordinary bindings can
        establish an input. Ordinary parameter annotations never prove exact inputs.
        """
        exports = {name: name for name in self.contracts}

        def block(body: list[ast.stmt], env: dict[str, Binding], lexical_writes: dict[str, list[ast.AST]],
                  boundary: str, aliases: dict[str, str], external: dict[str, str], module: bool = False) -> dict[str, str]:
            previous_locals = self.locals
            self.locals = set(lexical_writes)

            def resolve(name: str) -> str | None:
                if name in aliases:
                    return aliases[name]
                if name not in lexical_writes:
                    return external.get(name)
                return None

            def calls(expression: ast.AST) -> None:
                def expressions(node: ast.AST, shadowed: set[str]):
                    yield node, shadowed
                    if isinstance(node, ast.Lambda):
                        for value in node.args.defaults + [value for value in node.args.kw_defaults if value]:
                            yield from expressions(value, shadowed)
                        nested = shadowed | {a.arg for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs}
                        if node.args.vararg:
                            nested.add(node.args.vararg.arg)
                        if node.args.kwarg:
                            nested.add(node.args.kwarg.arg)
                        yield from expressions(node.body, nested)
                        return
                    if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                        shadowed = shadowed | {name for generator in node.generators for name in _target_names(generator.target)}
                    for child in ast.iter_child_nodes(node):
                        if not isinstance(child, ast.stmt):
                            yield from expressions(child, shadowed)
                for call, shadowed in expressions(expression, set()):
                    target = resolve(call.func.id) if isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id not in shadowed else None
                    if target is not None:
                        self.boundary = boundary
                        self.result.analyzed_call_sites += 1
                        self._call_inputs(call, self.contracts[target], env)

            for statement in body:
                if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if id(statement) not in self.selected_nodes:
                        local_writes = _written_names(statement.body)
                        for arg in statement.args.posonlyargs + statement.args.args + statement.args.kwonlyargs:
                            local_writes.setdefault(arg.arg, []).append(arg)
                        for arg in [statement.args.vararg, statement.args.kwarg]:
                            if arg:
                                local_writes.setdefault(arg.arg, []).append(arg)
                        visible = {name: target for name, target in external.items() if name not in lexical_writes}
                        visible.update(aliases)
                        block(statement.body, {}, local_writes, statement.name, {}, visible)
                    # Defaults/decorators execute in the enclosing shell, not in its body.
                    annotations = [a.annotation for a in statement.args.posonlyargs + statement.args.args + statement.args.kwonlyargs if a.annotation]
                    annotations += [a.annotation for a in [statement.args.vararg, statement.args.kwarg] if a and a.annotation]
                    if statement.returns:
                        annotations.append(statement.returns)
                    for expression in statement.decorator_list + statement.args.defaults + [d for d in statement.args.kw_defaults if d] + annotations:
                        calls(expression)
                    continue
                if isinstance(statement, ast.ClassDef):
                    for expression in statement.bases + [k.value for k in statement.keywords] + statement.decorator_list:
                        calls(expression)
                    block(statement.body, {}, _written_names(statement.body), statement.name, {}, exports)
                    continue
                calls(statement)
                if isinstance(statement, (ast.Assign, ast.AnnAssign)):
                    targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
                    if targets and all(isinstance(target, ast.Name) for target in targets) and statement.value is not None:
                        target = resolve(statement.value.id) if isinstance(statement.value, ast.Name) else None
                        value = self._expr(statement.value, env, quiet=True)
                        for assigned in targets:
                            name = assigned.id
                            if len(lexical_writes.get(name, [])) != 1:
                                continue
                            env[name] = Binding(value, (statement.lineno,))
                            if target:
                                aliases[name] = target
                elif isinstance(statement, ast.If):
                    # Do not infer stable values from ordinary branches; their input obligations still count.
                    block(statement.body, dict(env), lexical_writes, boundary, dict(aliases), external, module)
                    block(statement.orelse, dict(env), lexical_writes, boundary, dict(aliases), external, module)
                elif isinstance(statement, ast.Match):
                    for case in statement.cases:
                        block(case.body, {}, lexical_writes, boundary, dict(aliases), external, module)
                elif hasattr(statement, "body"):
                    block(statement.body, {}, lexical_writes, boundary, dict(aliases), external, module)
                    if hasattr(statement, "orelse"):
                        block(statement.orelse, {}, lexical_writes, boundary, dict(aliases), external, module)
                    if hasattr(statement, "finalbody"):
                        block(statement.finalbody, {}, lexical_writes, boundary, dict(aliases), external, module)
                    for handler in getattr(statement, "handlers", []):
                        block(handler.body, {}, lexical_writes, boundary, dict(aliases), external, module)
            self.locals = previous_locals
            return aliases

        block(tree.body, {}, self.global_writes, "<ordinary module>", dict(exports), {}, True)

    def _call_inputs(self, node: ast.Call, contract: FunctionContract, env: dict[str, Binding]) -> None:
        if self.global_writes.get(node.func.id) and node.func.id == contract.name and len(self.global_writes[node.func.id]) != 1:
            self.emit("PAL240", node, f"checked function binding `{node.func.id}` is replaced in analyzed source", origin="ordinary call obligation")
        positional = [name for name, kind in contract.parameter_kinds.items() if kind != "keyword_only"]
        supplied: dict[str, ast.expr] = {}
        malformed = len(node.args) > len(positional) or any(isinstance(a, ast.Starred) for a in node.args)
        for name, argument in zip(positional, node.args):
            supplied[name] = argument
        for keyword in node.keywords:
            if keyword.arg is None or keyword.arg not in contract.parameters or keyword.arg in supplied or contract.parameter_kinds.get(keyword.arg) == "positional_only":
                malformed = True
            else:
                supplied[keyword.arg] = keyword.value
        if malformed or supplied.keys() != contract.parameters.keys():
            self.emit("PAL221", node, f"call to `{contract.name}` does not establish its required argument signature", origin="ordinary call obligation")
        for name, argument in supplied.items():
            expected = contract.parameters.get(name)
            value = self._expr(argument, env, quiet=True)
            if expected and value.kind != expected:
                self.emit("PAL221", argument, f"argument `{name}` of `{contract.name}` requires exact {expected}; found {self._describe(value)}", origin="ordinary call obligation")


def analyze_source(source: str, path: str = "<source>", *, audit: bool = False,
                   policy: dict | None = None) -> CheckResult:
    """Analyze text only; this API does not certify the caller's runtime environment."""
    return ScalarAnalyzer(source, path, "audit" if audit else "strict", policy).analyze()


def analyze_file(path: str | Path, *, audit: bool = False, policy: dict | None = None) -> CheckResult:
    resolved = Path(path).resolve()
    try:
        with tokenize.open(resolved) as stream:
            source = stream.read()
    except (OSError, UnicodeError, SyntaxError) as error:
        result = CheckResult(str(resolved), "", mode="audit" if audit else "strict")
        result.diagnostics.append(diagnostic("PAL001", str(resolved), f"cannot read source: {error}"))
        return result
    return analyze_source(source, str(resolved), audit=audit, policy=policy)
