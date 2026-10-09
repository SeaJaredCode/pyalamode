"""Closed scalar/module checker. Application source is never imported or evaluated."""

from __future__ import annotations

import ast
import hashlib
import io
import json
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

from .model import (CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, CheckResult,
                    FunctionContract, SCALARS, diagnostic, foundation_identities)

BUILTINS = frozenset({"abs", "min", "max", "len"})
COLLECTIONS = frozenset({"Vector", "OrderedMap", "Map", "Set"})
CALLABLE_FAILURES = frozenset({"ZeroDivisionError", "RecursionError", "IndexError", "KeyError", "ValueError"})
RETURN_ONLY_UPDATES = frozenset({"appended", "updated_at", "concat", "updated", "without", "merge", "added", "union", "intersection", "difference"})
# Actual explicit/implicit foundation reads of the shipped collections-v1
# backend, including its declaration/import initialization. This is a closed
# dependency inventory, not admission for application calls to these names.
COLLECTION_FOUNDATIONS = {
    "builtins": frozenset({"type", "any", "all", "id", "set", "enumerate", "tuple", "len", "sorted", "repr", "hex", "zip", "iter", "next", "object", "getattr", "bool", "int", "str", "bytes", "classmethod", "TypeError", "AttributeError", "IndexError", "KeyError", "ValueError", "__build_class__", "__import__"}),
    "types": frozenset({"FunctionType", "GenericAlias"}),
}
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
    items: tuple[Value, ...] | None = None
    callable: CallableValue | None = None

    @classmethod
    def exact(cls, kind: str, literal: object = _UNKNOWN) -> Value:
        return cls(frozenset({kind}), literal)

    @property
    def kind(self) -> str | None:
        return next(iter(self.types)) if len(self.types) == 1 else None

    def with_callable(self, callback: CallableValue) -> Value:
        return Value(self.types, self.literal, self.items, callback)


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
    """Shared scalar operations, lexical write discovery and ordinary caller inspection."""

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

    def _prepare(self) -> ast.Module | CheckResult:
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
        return tree

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
                    resolved_info = None
                    if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and hasattr(self, "_ordinary_resolved_info"):
                        owner = call.func
                        while isinstance(owner, ast.Attribute):
                            owner = owner.value
                        if not isinstance(owner, ast.Name) or owner.id not in shadowed:
                            resolved_info = self._ordinary_resolved_info(call.func, env)
                    elif isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and target is None and call.func.id not in shadowed and hasattr(self, "_ordinary_resolved_info"):
                        resolved_info = self._ordinary_resolved_info(call.func, env)
                    if target is not None or resolved_info is not None:
                        self.boundary = boundary
                        if hasattr(self, "_record_call"):
                            self._record_call(call)
                        else:
                            self.result.analyzed_call_sites += 1
                        if resolved_info:
                            self._checked_inputs(call, resolved_info, env)
                        else:
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
                    elif hasattr(self, "infos"):
                        info = self.infos.get(id(statement))
                        if info:
                            env[statement.name] = Binding(info.value(), (statement.lineno,))
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
                if isinstance(statement, (ast.Import, ast.ImportFrom)) and hasattr(self, "symbols") and module:
                    for name, symbol in self.symbols.items():
                        if symbol.node is statement and self._symbol_stable(name, symbol):
                            env[name] = Binding(self._resolve_symbol(symbol, statement, True), (statement.lineno,))
                elif isinstance(statement, (ast.Assign, ast.AnnAssign)):
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



@dataclass(frozen=True)
class TypeSpec:
    """Closed exact-value schema; no runtime annotation evaluation or protocols."""
    name: str
    arguments: tuple[TypeSpec, ...] = ()
    result: TypeSpec | None = None
    variadic: bool = False

    def __str__(self) -> str:
        if self.name == "tuple":
            if not self.arguments:
                return "tuple[()]"
            return "tuple[" + ", ".join(map(str, self.arguments)) + (", ..." if self.variadic else "") + "]"
        if self.name == "Callable":
            return "Callable[[" + ", ".join(map(str, self.arguments)) + "], " + str(self.result) + "]"
        if self.name in COLLECTIONS:
            return self.name + "[" + ", ".join(map(str, self.arguments)) + "]"
        return self.name


def _contract_type(text: str) -> TypeSpec:
    """Decode our canonical cache schema, never a user annotation or Python value."""
    def parse(node):
        if isinstance(node, ast.Name) and node.id in SCALARS:
            return TypeSpec(node.id)
        if isinstance(node, ast.Constant) and node.value is None:
            return TypeSpec("None")
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
            parts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
            if node.value.id == "tuple":
                variadic = len(parts) == 2 and isinstance(parts[-1], ast.Constant) and parts[-1].value is Ellipsis
                return TypeSpec("tuple", tuple(parse(p) for p in (parts[:-1] if variadic else parts)), variadic=variadic)
            if node.value.id == "Callable" and len(parts) == 2 and isinstance(parts[0], ast.List):
                return TypeSpec("Callable", tuple(parse(p) for p in parts[0].elts), parse(parts[1]))
            if node.value.id in COLLECTIONS:
                return TypeSpec(node.value.id, tuple(parse(p) for p in parts))
        raise ValueError("invalid serialized exact type contract")
    return parse(ast.parse(text, mode="eval").body)


@dataclass(frozen=True)
class CallableValue:
    """Resolved invocation evidence, separate from an annotation's input obligation."""
    parameters: tuple[str, ...]
    returns: str | None
    targets: tuple[str, ...] = ()
    captures: tuple[tuple[str, str], ...] = ()
    conditional: bool = False


@dataclass
class FunctionInfo:
    node: ast.FunctionDef | ast.AsyncFunctionDef
    analyzer: FunctionalAnalyzer
    qualified: str
    parent: FunctionInfo | None = None
    parameters: dict[str, str] = field(default_factory=dict)
    kinds: dict[str, str] = field(default_factory=dict)
    returns: str | None = None
    defaults: dict[str, Value] = field(default_factory=dict)
    captures: dict[str, Value] = field(default_factory=dict)
    calls: set[str] = field(default_factory=set)
    failures: set[str] = field(default_factory=set)
    dependencies: set[str] = field(default_factory=set)
    analyzed: bool = False
    analyzing: bool = False
    contract: FunctionContract | None = None
    enclosing: dict[str, Binding] = field(default_factory=dict)
    enclosing_names: set[str] = field(default_factory=set)
    capture_uses: set[str] = field(default_factory=set)
    definition_failures: set[str] = field(default_factory=set)
    return_value: Value | None = None
    operations: set[str] = field(default_factory=set)

    @property
    def identity(self) -> str:
        return self.analyzer.path + "::" + self.qualified

    def value(self) -> Value:
        positional = tuple(self.parameters[n] for n in self.parameters if self.kinds[n] != "keyword_only")
        schema = TypeSpec("Callable", tuple(self.analyzer.graph.types.get(t, TypeSpec("<unknown>")) for t in positional),
                          self.analyzer.graph.types.get(self.returns))
        kind = str(schema)
        self.analyzer.graph.types[kind] = schema
        return Value.exact(kind).with_callable(CallableValue(
            positional, self.returns, (self.identity,), tuple((n, self.captures[n].kind or "unknown") for n in sorted(self.capture_uses))))


@dataclass(frozen=True)
class Symbol:
    kind: str
    name: str
    node: ast.AST | None = None


def _module_name(path: str, root: Path) -> str:
    try:
        relative = Path(path).resolve().relative_to(root)
    except ValueError:
        return Path(path).stem
    parts = list(relative.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _import_name(node: ast.ImportFrom, module_name: str, package: bool) -> str:
    if not node.level:
        return node.module or ""
    parts = module_name.split(".") if package else module_name.split(".")[:-1]
    if node.level > len(parts) + 1:
        return "<invalid-relative-import>"
    prefix = parts[:len(parts) - node.level + 1]
    return ".".join(prefix + ([node.module] if node.module else []))


def _local_path(root: Path, name: str) -> Path | None:
    parts = name.split(".")
    if not name or any(not part.isidentifier() for part in parts):
        return None
    for count in range(1, len(parts)):
        parent = root.joinpath(*parts[:count])
        if parent.with_suffix(".py").is_file() and not (parent / "__init__.py").is_file():
            return None
    base = root.joinpath(*parts)
    # CPython's filesystem finder tries an initialized package before a module file.
    for candidate in (base / "__init__.py", base.with_suffix(".py")):
        if candidate.is_file():
            return candidate.resolve()
    return None


def _product_source(name: str, path: Path) -> bool:
    files = {"pyalamode": "__init__.py", "pyalamode.collections": "collections.py"}
    return name in files and path == Path(__file__).resolve().parent / files[name]


def load_sources(paths: list[Path], root: Path, raw_sources: dict[str, bytes] | None = None) -> tuple[dict[str, str], list]:
    """Read selected files and resolvable local imports, including package initialization."""
    sources: dict[str, str] = {}
    errors = []
    queue = list(paths)
    while queue:
        path = queue.pop(0).resolve()
        if str(path) in sources:
            continue
        try:
            raw = path.read_bytes()
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            source = raw.decode(encoding)
            if raw_sources is not None:
                raw_sources[str(path)] = raw
            sources[str(path)] = source
            tree = ast.parse(source, filename=str(path), feature_version=(3, 13))
        except (OSError, UnicodeError, SyntaxError, ValueError) as error:
            errors.append(diagnostic("PAL001", str(path), f"cannot read/parse source: {error}",
                                     line=getattr(error, "lineno", 1) or 1))
            continue
        module = _module_name(str(path), root)
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = _import_name(node, module, path.name == "__init__.py")
                names = [base] + [base + "." + alias.name for alias in node.names if alias.name != "*"]
            for name in names:
                parts = name.split(".")
                for count in range(1, len(parts) + 1):
                    dependency = _local_path(root, ".".join(parts[:count]))
                    if dependency and not _product_source(".".join(parts[:count]), dependency) and str(dependency) not in sources:
                        queue.append(dependency)
    return sources, errors


class SourceGraph:
    """One closed source snapshot. Local imports never fall back to executing Python."""

    def __init__(self, sources: dict[str, str], root: Path, audit: bool, policy: dict | None):
        self.root, self.policy = root, policy or {}
        self.types = {kind: TypeSpec(kind) for kind in SCALARS}
        self.analyzers: dict[str, FunctionalAnalyzer] = {}
        self.modules: dict[str, FunctionalAnalyzer] = {}
        self.functions: dict[str, FunctionInfo] = {}
        for path, source in sources.items():
            analyzer = FunctionalAnalyzer(source, path, "audit" if audit else "strict", policy, self)
            self.analyzers[path] = analyzer
            self.modules[_module_name(path, root)] = analyzer
        for analyzer in self.analyzers.values():
            analyzer.prepare()
        for analyzer in self.analyzers.values():
            analyzer.discover()
        self.replaced_functions: set[str] = set()
        self.replaced_foundations: set[tuple[str, str]] = set()
        self.collection_dependency_replacements: set[str] = set()
        for analyzer in self.analyzers.values():
            if analyzer.tree is None:
                continue
            aliases = {}
            changed = True
            while changed:
                changed = False
                for node in ast.walk(analyzer.tree):
                    if isinstance(node, ast.Assign):
                        reference = self.reference(analyzer, node.value, aliases)
                        if reference:
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id not in aliases:
                                    aliases[target.id] = reference
                                    changed = True
            for node in ast.walk(analyzer.tree):
                targets = node.targets if isinstance(node, (ast.Assign, ast.Delete)) else [node.target] if isinstance(node, (ast.AnnAssign, ast.AugAssign)) else []
                for target in targets:
                    owner = target.value if isinstance(target, ast.Attribute) else None
                    if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Attribute) and target.value.attr == "__dict__":
                        owner = target.value.value
                    reference = self.reference(analyzer, owner, aliases) if owner else None
                    if reference in self.functions:
                        self.replaced_functions.add(reference)
                    elif reference == "module:pyalamode.collections":
                        self.replaced_foundations.add(("pyalamode", "*"))
                    elif reference and reference.startswith("foundation:"):
                        _, module, attribute = reference.split(":", 2)
                        self.replaced_foundations.add((module, attribute))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"setattr", "delattr"} and node.args:
                    reference = self.reference(analyzer, node.args[0], aliases)
                    if reference in self.functions:
                        self.replaced_functions.add(reference)
                    elif reference == "module:pyalamode.collections":
                        self.replaced_foundations.add(("pyalamode", "*"))
                    elif reference and reference.startswith("foundation:"):
                        _, module, attribute = reference.split(":", 2)
                        self.replaced_foundations.add((module, attribute))
        for module, attributes in COLLECTION_FOUNDATIONS.items():
            for attribute in attributes:
                replaced = ((module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations
                            or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values()))
                if replaced:
                    self.collection_dependency_replacements.add(module + "." + attribute)
                    # Refuse all collection contracts conservatively. The fun
                    # marker and unrelated scalar bodies retain their own gates.
                    self.replaced_foundations.update(("pyalamode", name) for name in COLLECTIONS)
        # Replacement identities must be established before annotation admission;
        # all signatures still precede bodies, including recursive components.
        for info in self.functions.values():
            info.analyzer.signature(info)

    def reference(self, analyzer, node, aliases=None, seen=None):
        """Resolve source alias identity without executing or admitting its behavior."""
        if isinstance(node, ast.Name) and aliases and node.id in aliases:
            return aliases[node.id]
        seen = set() if seen is None else seen
        if isinstance(node, ast.Name):
            key = (analyzer.path, node.id)
            if key in seen:
                return None
            seen.add(key)
            symbol = analyzer.symbols.get(node.id)
            if not symbol:
                infos = [i for i in analyzer.infos.values() if i.node.name == node.id]
                return infos[0].identity if len(infos) == 1 else None
            if symbol.kind == "function":
                return symbol.name
            if symbol.kind == "module":
                return "module:" + symbol.name
            if symbol.kind == "constant":
                return self.reference(analyzer, symbol.node.value, aliases, seen)
            if symbol.kind == "import":
                module, name = symbol.name.split(":", 1)
                if module == "pyalamode.collections" and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + (name if name in COLLECTIONS else "*")
                target = self.modules.get(module)
                return self.reference(target, ast.Name(id=name), None, seen) if target else "foundation:" + module + ":" + name if module in {"pyalamode", "typing", "collections.abc", "types", "builtins"} else None
        if isinstance(node, ast.Subscript):
            reference = self.reference(analyzer, node.value, aliases, seen)
            if reference and reference.startswith("foundation:pyalamode:") and reference.rsplit(":", 1)[-1] in COLLECTIONS:
                return reference
        if isinstance(node, ast.Attribute):
            owner = self.reference(analyzer, node.value, aliases, seen)
            if owner and owner.startswith("foundation:pyalamode:") and owner.rsplit(":", 1)[-1] in COLLECTIONS | {"*"}:
                return owner
            if owner and owner.startswith("module:"):
                module = owner.split(":", 1)[1]
                if module == "pyalamode" and node.attr == "collections" and analyzer._foundation_available("pyalamode.collections"):
                    return "module:pyalamode.collections"
                if module == "pyalamode.collections" and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + (node.attr if node.attr in COLLECTIONS else "*")
                target = self.modules.get(module)
                if target and node.attr in target.symbols:
                    return self.reference(target, ast.Name(id=node.attr), None, seen)
                if module + "." + node.attr in self.modules:
                    return "module:" + module + "." + node.attr
                if module in {"pyalamode", "typing", "collections.abc", "types", "builtins"}:
                    return "foundation:" + module + ":" + node.attr
        return None

    def binding_context(self, path, dependencies):
        """Relevant analyzed replacements are cache inputs, even in ordinary writers."""
        analyzer = self.analyzers[path]
        relevant = {(_module_name(p, self.root), "*") for p in {path} | set(dependencies)}
        for name, symbol in analyzer.symbols.items():
            if symbol.kind == "import":
                module, attribute = symbol.name.split(":", 1)
                relevant.add((module, attribute))
            elif symbol.kind == "module":
                relevant.add((symbol.name, "*"))
        if analyzer.tree:
            for node in ast.walk(analyzer.tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in BUILTINS | {"int", "str", "bool", "bytes", "tuple"}:
                    relevant.add(("builtins", node.id))
        replacements = set()
        for writer in self.analyzers.values():
            for alias, attribute in writer.changed_attributes:
                module = writer.module_aliases.get(alias)
                if module and ((module, attribute) in relevant or (module, "*") in relevant or attribute == "*" and any(m == module for m, _ in relevant)):
                    replacements.add(module + "." + attribute)
        for identity in self.replaced_functions:
            if identity.split("::", 1)[0] in {path} | set(dependencies):
                replacements.add(identity + ".<behavior>")
        for module, attribute in self.replaced_foundations:
            if (module, attribute) in relevant or (module, "*") in relevant or attribute == "*" and any(m == module for m, _ in relevant):
                replacements.add(module + "." + attribute + ".<behavior>")
        if any(("pyalamode", name) in relevant for name in COLLECTIONS) or ("pyalamode", "*") in relevant:
            replacements.update(identity + ".<collection dependency>" for identity in self.collection_dependency_replacements)
        return sorted(replacements)

    def analyze(self, cached: dict[str, CheckResult] | None = None) -> dict[str, CheckResult]:
        for path, result in (cached or {}).items():
            analyzer = self.analyzers[path]
            analyzer.result = result
            analyzer.dependencies.update(result.dependencies)
            for info in analyzer.infos.values():
                info.contract = next((c for c in result.contracts if c.name == info.qualified), None)
                if info.contract:
                    info.calls = {d for d in info.contract.dependencies if d in self.functions}
                    info.dependencies = {d for d in info.contract.dependencies if d in self.analyzers}
                    info.failures = set(info.contract.failures)
                    info.operations = set(info.contract.operations)
                    info.definition_failures = set(info.contract.definition_failures)
                    info.capture_uses = set(info.contract.captures)
                    for name, kind in info.contract.captures.items():
                        if kind not in self.types:
                            self.types[kind] = _contract_type(kind)
                        value = analyzer.annotation_value(kind)
                        targets = info.contract.callable_targets.get(name)
                        if targets and value.callable:
                            value = value.with_callable(CallableValue(value.callable.parameters, value.callable.returns, tuple(targets)))
                        info.captures[name] = value
                    if info.contract.return_callable_targets:
                        value = analyzer.annotation_value(info.returns)
                        if value.callable:
                            info.return_value = value.with_callable(CallableValue(value.callable.parameters, value.callable.returns, tuple(info.contract.return_callable_targets)))
                    info.analyzed = True
        for analyzer in self.analyzers.values():
            if analyzer.path not in (cached or {}):
                analyzer.run()
        def recursive(start, current, seen):
            if current in seen:
                return False
            seen.add(current)
            return any(target == start or recursive(start, target, seen) for target in self.functions[current].calls)
        for info in self.functions.values():
            if recursive(info.identity, info.identity, set()):
                info.failures.add("RecursionError")
        changed = True
        while changed:
            changed = False
            for info in self.functions.values():
                for target in info.calls:
                    callee = self.functions[target]
                    before = (len(info.failures), len(info.dependencies), len(info.operations))
                    info.failures.update(callee.failures)
                    info.dependencies.update(callee.dependencies)
                    info.operations.update(callee.operations)
                    if before != (len(info.failures), len(info.dependencies), len(info.operations)):
                        changed = True
        for info in self.functions.values():
            if info.contract:
                info.contract.failures = sorted(info.failures)
                info.contract.dependencies = sorted(info.dependencies | info.calls)
                info.contract.operations = sorted(info.operations)
                schemas = [*info.parameters.values(), info.returns or "", *info.contract.captures.values()]
                if any(operation.split(".", 1)[0] in COLLECTIONS for operation in info.operations) or any(name + "[" in kind for name in COLLECTIONS for kind in schemas):
                    assumption = "pyalamode collections-v1: exact deep-data façade, CPython tuple-copy storage and canonical scalar ordering"
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                info.analyzer.dependencies.update(info.dependencies)
        # A source dependency carries its own dependencies and initializer assumptions.
        changed = True
        while changed:
            changed = False
            for analyzer in self.analyzers.values():
                before = len(analyzer.dependencies)
                for path in tuple(analyzer.dependencies):
                    if path in self.analyzers:
                        analyzer.dependencies.update(self.analyzers[path].dependencies)
                changed |= before != len(analyzer.dependencies)
        for analyzer in self.analyzers.values():
            analyzer.finish()
        changed = True
        while changed:
            changed = False
            for analyzer in self.analyzers.values():
                if analyzer.module_mode:
                    failures = set(analyzer.result.initialization_failures)
                    for path in analyzer.dependencies:
                        if path in self.analyzers and self.analyzers[path].module_mode:
                            failures.update(self.analyzers[path].result.initialization_failures)
                    new = sorted(failures)
                    changed |= new != analyzer.result.initialization_failures
                    analyzer.result.initialization_failures = new
        for analyzer in self.analyzers.values():
            if any(self.analyzers[path].result.diagnostics for path in analyzer.dependencies if path in self.analyzers):
                if not any(d.origin == "dependency gate" for d in analyzer.result.diagnostics):
                    analyzer.result.diagnostics.append(diagnostic("PAL240", analyzer.path, "a resolved source dependency failed its participating gate", origin="dependency gate"))
                for contract in analyzer.result.contracts:
                    contract.source_evidence = "unverified: dependency gate failed"
                    contract.freshness = "no successful checked claim"
                if analyzer.module_mode:
                    analyzer.result.initialization_evidence = "unverified: dependency gate failed"
        return {path: analyzer.result for path, analyzer in self.analyzers.items()}


class FunctionalAnalyzer(ScalarAnalyzer):
    def __init__(self, source, path, mode, policy, graph):
        super().__init__(source, path, mode, policy)
        self.graph = graph
        self.policy = policy or {}
        self.tree: ast.Module | None = None
        self.symbols: dict[str, Symbol] = {}
        self.constants: dict[str, Value] = {}
        self.constant_busy: set[str] = set()
        self.constant_limit: int | None = None
        self.infos: dict[int, FunctionInfo] = {}
        self.active: FunctionInfo | None = None
        self.dependencies: set[str] = set()
        self.module_mode = False
        self.initializing = False
        self.parents: dict[int, ast.AST] = {}
        self.definition_mode = False
        self.call_sites: set[int] = set()

    def prepare(self):
        tree = self._prepare()
        if isinstance(tree, CheckResult):
            return
        self.tree = tree
        self.parents = {id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        doc = tree.body[0] if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and type(tree.body[0].value.value) is str else None
        first = tree.body[1] if doc and len(tree.body) > 1 else (tree.body[0] if not doc and tree.body else None)
        directives = [t for t in tokenize.generate_tokens(io.StringIO(self.source).readline)
                      if t.type == tokenize.COMMENT and t.string.strip() == "# mode: fun"]
        for token in tokenize.generate_tokens(io.StringIO(self.source).readline):
            if token.type == tokenize.COMMENT and token.string.strip().startswith("# mode:") and token.string.strip() != "# mode: fun":
                self.result.diagnostics.append(diagnostic("PAL121", self.path, "the only supported directive is the module header # mode: fun; region toggles are unsupported", line=token.start[0]))
        valid = False
        for token in directives:
            if token.start[1] != 0 or (doc and token.start[0] <= doc.end_lineno) or (first and token.start[0] >= first.lineno) or valid:
                self.result.diagnostics.append(diagnostic("PAL121", self.path, "module directive must occur once in the module header after any docstring", line=token.start[0], column=token.start[1] + 1))
            else:
                valid = True
        relative = _module_name(self.path, self.graph.root)
        try:
            source_relative = Path(self.path).resolve().relative_to(self.graph.root).as_posix()
        except ValueError:
            source_relative = self.path
        from pathlib import PurePosixPath
        import fnmatch
        required = any(fnmatch.fnmatchcase(source_relative, pattern) or PurePosixPath(source_relative).match(pattern)
                       or ("**/" in pattern and fnmatch.fnmatchcase(source_relative, pattern.replace("**/", "")))
                       for pattern in self.policy.get("require_modules", []))
        self.module_mode = valid or required
        self.result.module_mode = self.module_mode
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name.split(".")[0]
                    target = alias.name if alias.asname else alias.name.split(".")[0]
                    self.symbols[name] = Symbol("module", target, node)
                    self.module_aliases[name] = target
            elif isinstance(node, ast.ImportFrom):
                target = _import_name(node, relative, Path(self.path).name == "__init__.py")
                for alias in node.names:
                    self.symbols[alias.asname or alias.name] = Symbol("import", target + ":" + alias.name, node)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if len(targets) == 1 and isinstance(targets[0], ast.Name) and node.value is not None:
                    self.symbols[targets[0].id] = Symbol("constant", targets[0].id, node)
        # Track aliases to local modules as well as the foundation aliases handled by M1.
        changed = True
        while changed:
            changed = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name) and node.value.id in self.module_aliases:
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id not in self.module_aliases:
                            self.module_aliases[target.id] = self.module_aliases[node.value.id]
                            changed = True

    def discover(self):
        if self.tree is None:
            return
        def visit(body, parent=None, prefix="", strict=False):
            for node in body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.result.eligible_functions += 1
                    selected = strict or any(self._marker_like(d) for d in node.decorator_list)
                    qualified = prefix + node.name
                    info = None
                    if selected:
                        info = FunctionInfo(node, self, qualified, parent)
                        self.infos[id(node)] = info
                        self.graph.functions[info.identity] = info
                        self.selected_nodes.add(id(node))
                        self.result.selected_functions += 1
                        if self.parents.get(id(node)) is self.tree:
                            self.symbols[node.name] = Symbol("function", info.identity, node)
                    visit(node.body, info, qualified + ".", selected)
                elif isinstance(node, ast.ClassDef):
                    visit(node.body, parent, prefix + node.name + ".", strict)
                else:
                    for field in ("body", "orelse", "finalbody"):
                        nested = getattr(node, field, None)
                        if isinstance(nested, list):
                            visit(nested, parent, prefix, strict)
                    for handler in getattr(node, "handlers", []):
                        visit(handler.body, parent, prefix, strict)
        visit(self.tree.body, strict=self.module_mode)

    def _symbol_stable(self, name: str, symbol: Symbol) -> bool:
        writes = self.global_writes.get(name, [])
        targets = [symbol.node]
        if isinstance(symbol.node, ast.Assign):
            targets = symbol.node.targets
        elif isinstance(symbol.node, ast.AnnAssign):
            targets = [symbol.node.target]
        return len(writes) == 1 and writes[0] in targets and "*" not in self.global_writes

    def _module_changed(self, module: str, attribute: str) -> bool:
        replacements = getattr(self.graph, "replaced_foundations", set())
        if (module, attribute) in replacements or (module, "*") in replacements:
            return True
        for analyzer in self.graph.analyzers.values():
            if analyzer._attribute_changed(module, attribute):
                return True
        return False

    def _foundation_available(self, module):
        parts = module.split(".")
        for count in range(1, len(parts) + 1):
            name = ".".join(parts[:count])
            target = self.graph.modules.get(name)
            if target and not _product_source(name, Path(target.path).resolve()):
                return False
        return True

    def _resolve_symbol(self, symbol: Symbol, node: ast.AST, quiet: bool, seen: set[tuple[str, str]] | None = None) -> Value:
        if symbol.kind == "function":
            info = self.graph.functions[symbol.name]
            if info.identity in self.graph.replaced_functions:
                return UNKNOWN
            if self.constant_limit is not None and symbol.node.lineno >= self.constant_limit:
                return UNKNOWN
            self._depend(info.analyzer.path)
            return info.value()
        if symbol.kind == "constant":
            return self._constant(symbol.name, quiet)
        if symbol.kind == "import":
            module, name = symbol.name.split(":", 1)
            if module == "pyalamode" and name in COLLECTIONS and self._foundation_available(module) and not self._module_changed(module, name):
                return Value.exact("collection_class:" + name)
            if module == "builtins" and name in BUILTINS and self._foundation_available(module) and not self._module_changed(module, name):
                return Value.exact("builtin:" + name)
            target = self.graph.modules.get(module)
            if target:
                self._depend(target.path)
                seen = set() if seen is None else seen
                key = (module, name)
                if key in seen:
                    return UNKNOWN
                seen.add(key)
                resolved = target.symbols.get(name)
                if resolved and target._symbol_stable(name, resolved) and not self._module_changed(module, name):
                    return target._resolve_symbol(resolved, node, quiet, seen)
                child = self.graph.modules.get(module + "." + name)
                if child:
                    return Value.exact("module:" + module + "." + name)
            return UNKNOWN
        if symbol.kind == "module":
            return Value.exact("module:" + symbol.name)
        return UNKNOWN

    def _depend(self, path: str):
        if path != self.path:
            self.dependencies.add(path)
            if self.active:
                self.active.dependencies.add(path)

    def _record_call(self, node):
        if id(node) not in self.call_sites:
            self.call_sites.add(id(node))
            self.result.analyzed_call_sites += 1

    def _constant(self, name: str, quiet: bool) -> Value:
        symbol = self.symbols.get(name)
        if not symbol or not self._symbol_stable(name, symbol) or name in self.constant_busy:
            return UNKNOWN
        if self.constant_limit is not None and symbol.node.lineno >= self.constant_limit:
            return UNKNOWN
        if name in self.constants:
            return self.constants[name]
        self.constant_busy.add(name)
        previous = self.constant_limit, self.locals, self.boundary, self.definition_mode, self.failures
        self.constant_limit, self.locals, self.boundary, self.definition_mode = symbol.node.lineno, set(), "<constant " + name + ">", True
        self.failures = set()
        try:
            value = self._expr(symbol.node.value, {}, quiet=quiet)
            if isinstance(symbol.node, ast.AnnAssign):
                expected = self._annotation(symbol.node.annotation)
                if expected and not self.matches(value, expected):
                    if not quiet:
                        self.emit("PAL210", symbol.node, f"constant `{name}` requires {expected}; found {self._describe(value)}")
                    value = UNKNOWN
            if value.types:
                self.constants[name] = value
            return value
        finally:
            self.constant_limit, self.locals, self.boundary, self.definition_mode, self.failures = previous
            self.constant_busy.remove(name)

    def _type_identity(self, node: ast.expr, env_names: set[str]) -> str | None:
        if isinstance(node, ast.Name):
            if node.id in env_names:
                return None
            if node.id in {"bool", "int", "str", "bytes", "tuple"} and node.id not in self.global_writes and not self._module_changed("builtins", node.id):
                return node.id
            symbol = self.symbols.get(node.id)
            if symbol and not self._annotation_available(symbol):
                return None
            if symbol and self._symbol_stable(node.id, symbol) and symbol.kind == "import":
                module, name = symbol.name.split(":", 1)
                if not self._foundation_available(module) or self._module_changed(module, name):
                    return None
                if module == "types" and name == "NoneType":
                    return "None"
                if module in {"typing", "collections.abc"} and name == "Callable":
                    return "Callable"
                if module == "pyalamode" and name in COLLECTIONS:
                    return name
        if isinstance(node, ast.Attribute):
            symbol = self.symbols.get(node.value.id) if isinstance(node.value, ast.Name) and node.value.id not in env_names else None
            if symbol and not self._annotation_available(symbol):
                return None
            if symbol and self._symbol_stable(node.value.id, symbol) and symbol.kind == "module" and not self._module_changed(symbol.name, node.attr):
                if not self._foundation_available(symbol.name):
                    return None
                if symbol.name in {"typing", "collections.abc"} and node.attr == "Callable":
                    return "Callable"
                if symbol.name == "pyalamode" and node.attr in COLLECTIONS:
                    return node.attr
                if symbol.name == "types" and node.attr == "NoneType":
                    return "None"
                if symbol.name == "builtins" and node.attr in {"bool", "int", "str", "bytes", "tuple"}:
                    return node.attr
            if (node.attr == "Callable" and isinstance(node.value, ast.Attribute) and node.value.attr == "abc"
                    and isinstance(node.value.value, ast.Name)):
                symbol = self.symbols.get(node.value.value.id)
                if symbol and symbol.name == "collections" and self._foundation_available("collections.abc") and self._symbol_stable(node.value.value.id, symbol) and not self._module_changed("collections.abc", "Callable"):
                    return "Callable"
        return None

    def _annotation_available(self, symbol):
        postponed = self.tree and any(isinstance(n, ast.ImportFrom) and n.module == "__future__" and any(a.name == "annotations" for a in n.names) for n in self.tree.body)
        return not self.active or self.active.parent is not None or postponed or symbol.node.lineno < self.active.node.lineno

    def _marker_valid(self, node):
        if not self._foundation_available("pyalamode") or not super()._marker_valid(node):
            return False
        name = node.id if isinstance(node, ast.Name) else node.value.id
        imported = self.marker_imports.get(name) or self.module_imports.get(name)
        if self.active:
            if self.active.parent and name in (set(self.active.parent.parameters) | set(_written_names(self.active.parent.node.body))):
                return False
            if self.active.parent is None and self.parents.get(id(self.active.node)) is self.tree and imported.lineno >= self.active.node.lineno:
                return False
        return not self._module_changed("pyalamode", "fun")

    def _annotation(self, node, *, extra_names=()):
        original = node
        if isinstance(node, ast.Constant) and type(node.value) is str:
            try:
                node = ast.parse(node.value, mode="eval").body
            except (SyntaxError, ValueError):
                node = None
        names = set()
        names.update(extra_names)
        if self.active:
            parent = self.parents.get(id(self.active.node))
            while parent:
                if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.update(_written_names(parent.body))
                    names.update(a.arg for a in parent.args.posonlyargs + parent.args.args + parent.args.kwonlyargs)
                parent = self.parents.get(id(parent))
        def parse(expression):
            if isinstance(expression, ast.Constant) and expression.value is None:
                return TypeSpec("None")
            identity = self._type_identity(expression, names) if expression is not None else None
            if identity in SCALARS:
                return TypeSpec(identity)
            if isinstance(expression, ast.Subscript):
                identity = self._type_identity(expression.value, names)
                parts = expression.slice.elts if isinstance(expression.slice, ast.Tuple) else [expression.slice]
                if identity == "tuple":
                    if isinstance(expression.slice, ast.Tuple) and not expression.slice.elts:
                        return TypeSpec("tuple")
                    variadic = len(parts) == 2 and isinstance(parts[-1], ast.Constant) and parts[-1].value is Ellipsis
                    args = [parse(p) for p in (parts[:-1] if variadic else parts)]
                    if args and all(a is not None and a.name != "Callable" for a in args):
                        return TypeSpec("tuple", tuple(args), variadic=variadic)
                if identity == "Callable" and len(parts) == 2 and isinstance(parts[0], ast.List):
                    args = [parse(p) for p in parts[0].elts]
                    result = parse(parts[1])
                    if all(a is not None for a in args) and result is not None:
                        return TypeSpec("Callable", tuple(args), result)
                if identity in COLLECTIONS:
                    args = [parse(p) for p in parts]
                    arity = 2 if identity in {"Map", "OrderedMap"} else 1
                    if len(args) == arity and all(self._data_schema(a) for a in args):
                        if identity in {"Map", "OrderedMap", "Set"} and args[0].name not in SCALARS:
                            return None
                        return TypeSpec(identity, tuple(args))
            return None
        schema = parse(node)
        if schema is None:
            self.emit("PAL130", original or ast.Constant(value=None), "annotation must identify a closed exact scalar, recursive tuple/collection, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars")
            return None
        def register(spec):
            self.graph.types[str(spec)] = spec
            for arg in spec.arguments:
                register(arg)
            if spec.result:
                register(spec.result)
        register(schema)
        return str(schema)

    def signature(self, info):
        previous = self.active, self.boundary
        self.active, self.boundary = info, info.qualified
        node = info.node
        for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            annotation = self._annotation(arg.annotation)
            info.parameters[arg.arg] = annotation or "<unknown>"
            info.kinds[arg.arg] = ("positional_only" if arg in node.args.posonlyargs else "keyword_only" if arg in node.args.kwonlyargs else "positional_or_keyword")
        info.returns = self._annotation(node.returns)
        self.active, self.boundary = previous

    def annotation_value(self, kind):
        schema = self.graph.types.get(kind)
        if schema and schema.name == "Callable":
            return Value.exact(kind).with_callable(CallableValue(tuple(map(str, schema.arguments)), str(schema.result), conditional=True))
        return Value.exact(kind) if schema else UNKNOWN

    @staticmethod
    def _data_schema(schema):
        return schema is not None and (schema.name in SCALARS or schema.name in {"tuple", *COLLECTIONS} and all(FunctionalAnalyzer._data_schema(a) for a in schema.arguments))

    def _data_value(self, value):
        return bool(value.types) and not value.callable and all(self._data_schema(self.graph.types.get(kind)) for kind in value.types)

    def _value_schema(self, name, arguments):
        schema = TypeSpec(name, tuple(arguments))
        self.graph.types[str(schema)] = schema
        return Value.exact(str(schema))

    def matches(self, value: Value, expected: str) -> bool:
        schema = self.graph.types.get(expected)
        if schema is None or not value.types:
            return False
        if schema.name == "tuple":
            if value.items is not None:
                if schema.variadic:
                    return all(self.matches(v, str(schema.arguments[0])) for v in value.items)
                return len(value.items) == len(schema.arguments) and all(self.matches(v, str(t)) for v, t in zip(value.items, schema.arguments))
            return all(self._schema_matches(self.graph.types.get(kind), schema) for kind in value.types)
        if schema.name == "Callable":
            callback = value.callable
            if callback is None or (not callback.targets and not callback.conditional):
                return False
            if callback.parameters != tuple(map(str, schema.arguments)) or callback.returns != str(schema.result):
                return False
            for target in callback.targets:
                info = self.graph.functions[target]
                if any(k == "keyword_only" for k in info.kinds.values()):
                    return False
            return True
        if schema.name in COLLECTIONS:
            return all(self._schema_matches(self.graph.types.get(kind), schema) for kind in value.types)
        return value.types == frozenset({expected})

    def _schema_matches(self, actual, expected):
        if actual is None or actual.name != expected.name:
            return False
        if expected.name in COLLECTIONS:
            return len(actual.arguments) == len(expected.arguments) and all(self._schema_matches(a, b) for a, b in zip(actual.arguments, expected.arguments))
        if expected.name != "tuple":
            return actual == expected
        if expected.variadic:
            return all(self._schema_matches(t, expected.arguments[0]) for t in actual.arguments)
        return not actual.variadic and len(actual.arguments) == len(expected.arguments) and all(self._schema_matches(a, b) for a, b in zip(actual.arguments, expected.arguments))

    def run(self):
        if self.tree is None:
            return
        # Analyze top-level selected functions; nested definitions are checked at their enclosing definition site.
        for info in self.infos.values():
            if info.parent is None:
                if self.parents.get(id(info.node)) is not self.tree:
                    # An ordinary enclosing scope can supply only statically known, single initialized captures.
                    parent = self.parents.get(id(info.node))
                    while parent and not isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        parent = self.parents.get(id(parent))
                    if isinstance(parent, ast.ClassDef):
                        self.boundary = info.qualified
                        self.emit("PAL120", info.node, "class-bound declarations are outside the functional subset")
                    elif parent:
                        info.enclosing = self._ordinary_capture_env(parent, info.node)
                        ancestor = parent
                        while ancestor:
                            if isinstance(ancestor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                info.enclosing_names.update(_written_names(ancestor.body))
                                info.enclosing_names.update(a.arg for a in ancestor.args.posonlyargs + ancestor.args.args + ancestor.args.kwonlyargs)
                            ancestor = self.parents.get(id(ancestor))
                self.function(info)
        if self.module_mode:
            self.initializing = True
            self.active = None
            self.boundary, self.locals = "<module initialization>", set(self.global_writes)
            self.failures = set()
            env = {}
            for node in self.tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    self._check_import(node)
                    for name, symbol in self.symbols.items():
                        if symbol.node is node:
                            env[name] = Binding(self._resolve_symbol(symbol, node, False), (node.lineno,))
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    info = self.infos.get(id(node))
                    if info:
                        env[node.name] = Binding(info.value(), (node.lineno,))
                        self.failures.update(info.definition_failures)
                elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.If, ast.Pass)) or (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str):
                    env = self._statement(node, env) or env
                else:
                    self.emit("PAL241", node, f"{type(node).__name__} is outside checked module initialization")
            self.initializing = False
            self.result.initialization_failures = sorted(self.failures)
            self.result.initialization_evidence = "checked pure source initialization"
        else:
            for name, symbol in self.symbols.items():
                if symbol.kind == "import" and self._symbol_stable(name, symbol):
                    value = self._resolve_symbol(symbol, symbol.node, True)
                    if value.callable and len(value.callable.targets) == 1:
                        info = self.graph.functions[value.callable.targets[0]]
                        self.contracts[name] = info.contract or FunctionContract(info.qualified, info.analyzer.path, info.node.lineno, dict(info.parameters), info.returns, dict(info.kinds))
            self._ordinary_calls(self.tree)

    def _ordinary_capture_env(self, parent, selected):
        writes = _written_names(parent.body)
        changing_cells = {name for sub in ast.walk(parent) if isinstance(sub, ast.Nonlocal) for name in sub.names}
        env = {}
        previous = self.locals, self.active, self.definition_mode
        self.locals, self.active, self.definition_mode = set(writes) | {a.arg for a in parent.args.posonlyargs + parent.args.args + parent.args.kwonlyargs}, None, True
        for statement in parent.body:
            if statement.lineno >= selected.lineno:
                break
            if isinstance(statement, (ast.Assign, ast.AnnAssign)):
                targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
                if len(targets) == 1 and isinstance(targets[0], ast.Name) and targets[0].id not in changing_cells and writes.get(targets[0].id) == [statement.target if isinstance(statement, ast.AnnAssign) else targets[0]]:
                    value = self._expr(statement.value, env, quiet=True)
                    env[targets[0].id] = Binding(value, (statement.lineno,))
        self.locals, self.active, self.definition_mode = previous
        return env

    def _check_import(self, node):
        declared = [(alias.asname or (alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name)) for alias in node.names]
        for name in declared:
            writes = self.global_writes.get(name, [])
            if writes != [node]:
                self.emit("PAL101", node, f"import binding `{name}` has another analyzed initialization", first=writes[0].lineno if writes else None)
        for name, symbol in self.symbols.items():
            if symbol.node is not node:
                continue
            if not self._symbol_stable(name, symbol):
                self.emit("PAL101", node, f"import binding `{name}` has another initialization", first=self.global_writes[name][0].lineno)
            module = symbol.name.split(":", 1)[0]
            if module in {"pyalamode", "types", "builtins", "typing", "collections", "collections.abc", "__future__"} and self._foundation_available(module):
                if symbol.kind == "import":
                    allowed = {"pyalamode": {"fun", *COLLECTIONS}, "types": {"NoneType"}, "builtins": BUILTINS | {"int", "bool", "str", "bytes", "tuple"}, "typing": {"Callable"}, "collections.abc": {"Callable"}, "__future__": {"annotations"}}
                    if symbol.name.split(":", 1)[1] not in allowed.get(module, set()):
                        self.emit("PAL241", node, f"foundation import `{symbol.name}` has no supported contract")
                continue
            target = self.graph.modules.get(module)
            if target is None:
                self.emit("PAL241", node, f"import `{module}` cannot be resolved to checked local source")
            else:
                self._depend(target.path)
                if symbol.kind == "import":
                    exported = symbol.name.split(":", 1)[1]
                    if exported not in target.symbols and module + "." + exported not in self.graph.modules:
                        self.emit("PAL241", node, f"imported binding `{module}.{exported}` is absent from resolved source")
                if not target.module_mode:
                    self.emit("PAL241", node, f"import `{module}` has unchecked initialization; strict modules require a functional module")
                # Python imports each package initializer before its submodule.
                parts = module.split(".")
                for count in range(1, len(parts)):
                    package = self.graph.modules.get(".".join(parts[:count]))
                    if package:
                        self._depend(package.path)
                        if not package.module_mode:
                            self.emit("PAL241", node, f"package `{'.'.join(parts[:count])}` has unchecked initialization")

    def function(self, info):
        if info.analyzed or info.analyzing:
            return
        info.analyzing = True
        previous = self.active, self.boundary, self.locals, self.failures, getattr(self, "return_type", None), self.in_dead
        self.active, self.boundary, self.failures, self.in_dead = info, info.qualified, info.failures, False
        node = info.node
        if isinstance(node, ast.AsyncFunctionDef) or node.args.vararg or node.args.kwarg or getattr(node, "type_params", []):
            self.emit("PAL120", node, "async, variadic and generic functions have no supported contract")
        if info.parent is None and self.parents.get(id(node)) is self.tree:
            if self.global_writes.get(node.name) != [node]:
                self.emit("PAL240", node, f"participating binding `{node.name}` has another analyzed initialization")
        if info.identity in self.graph.replaced_functions:
            self.emit("PAL240", node, f"checked callable `{info.qualified}` has an analyzed attribute/behavior replacement")
        decorators = node.decorator_list
        if decorators and (len(decorators) != 1 or not self._marker_valid(decorators[0])):
            self.emit("PAL120", node, "only one unchanged pyalamode.fun identity declaration is supported")
        if not decorators and not (self.module_mode or info.parent):
            self.emit("PAL120", node, "function is not selected by module mode or a resolved marker")
        if info.parent:
            enclosing_writes = _written_names(info.parent.node.body)
            enclosing_parameters = set(info.parent.parameters)
            info.enclosing_names = set(enclosing_writes) | enclosing_parameters
            info.enclosing_names.update(info.parent.enclosing_names)
            changing_cells = {name for sub in ast.walk(info.parent.node) if isinstance(sub, ast.Nonlocal) for name in sub.names}
            for name, binding in info.enclosing.items():
                occurrences = enclosing_writes.get(name, [])
                if name in changing_cells or (name not in enclosing_parameters and name not in info.parent.captures and len(occurrences) != 1):
                    continue
                if binding.definite and binding.value.types:
                    info.captures[name] = binding.value
            # A stable sibling definition may be referenced through a closure cell for mutual recursion.
            for sibling in self.infos.values():
                if sibling.parent is info.parent and enclosing_writes.get(sibling.node.name) == [sibling.node]:
                    info.captures[sibling.node.name] = sibling.value()
        else:
            info.captures = {name: b.value for name, b in info.enclosing.items() if b.definite and b.value.types}
        local_writes = _written_names(node.body)
        self.locals = set(local_writes) | set(info.parameters)
        env = {name: Binding(self.annotation_value(kind), (node.lineno,)) for name, kind in info.parameters.items()}
        positional = node.args.posonlyargs + node.args.args
        default_nodes = {arg.arg: value for arg, value in zip(positional[-len(node.args.defaults):] if node.args.defaults else [], node.args.defaults)}
        default_nodes.update({arg.arg: value for arg, value in zip(node.args.kwonlyargs, node.args.kw_defaults) if value is not None})
        self.definition_mode = True
        body_failures = self.failures
        self.failures = info.definition_failures
        default_env = info.enclosing
        body_locals = self.locals
        self.locals = set(info.parent.parameters) | set(_written_names(info.parent.node.body)) if info.parent else set()
        prior_limit = self.constant_limit
        if info.parent is None and self.parents.get(id(node)) is self.tree:
            self.constant_limit = node.lineno
        for name, value_node in default_nodes.items():
            value = self._expr(value_node, default_env)
            if not self.matches(value, info.parameters[name]):
                self.emit("PAL221", value_node, f"default `{name}` does not establish {info.parameters[name]}", origin="definition-time default")
            info.defaults[name] = value
        self.definition_mode = False
        self.failures = body_failures
        self.constant_limit = prior_limit
        self.locals = body_locals
        self.return_type = info.returns
        continuing = self._block(node.body, env)
        if continuing is not None and info.returns != "None":
            self.emit("PAL211", node, "a completing path falls through with None instead of the declared result")
        contract = FunctionContract(info.qualified, self.path, node.lineno, dict(info.parameters), info.returns, dict(info.kinds),
                                    defaults={n: v.kind or "unknown" for n, v in info.defaults.items()},
                                    captures={n: info.captures[n].kind or "unknown" for n in info.capture_uses},
                                    callable_targets={n: list(info.captures[n].callable.targets) for n in info.capture_uses if info.captures[n].callable},
                                    callable_defaults={n: list(v.callable.targets) for n, v in info.defaults.items() if v.callable},
                                    return_callable_targets=list(info.return_value.callable.targets) if info.return_value and info.return_value.callable else [],
                                    definition_failures=sorted(info.definition_failures), operations=sorted(info.operations))
        contract.caller_obligations = [f"{name}: exact {kind}; recursively admitted contents and checked callable/capture evidence where applicable" for name, kind in info.parameters.items()]
        contract.caller_obligations.extend(["Resolved constant, callable, capture, marker, annotation and builtin bindings remain unchanged during execution.",
                                            "Callable inputs satisfy their declared pure invocation contract with stable captures; annotations alone do not establish that evidence.",
                                            "Callable invocation failure upper bound: IndexError, KeyError, ValueError, ZeroDivisionError and RecursionError, the closed supported callable failure universe.",
                                            "Ordinary callers receive no runtime guards; unchecked import initialization has no purity claim.",
                                            "Recursion may diverge or raise RecursionError; resource exhaustion and interruption are outside the failure contract."])
        info.contract = contract
        self.result.contracts.append(contract)
        if info.parent is None and self.parents.get(id(node)) is self.tree:
            self.contracts[node.name] = contract
        info.analyzed, info.analyzing = True, False
        self.active, self.boundary, self.locals, self.failures, self.return_type, self.in_dead = previous

    def _merge(self, left, right):
        if left is None:
            return right
        if right is None:
            return left
        merged = {}
        for name in left.keys() | right.keys():
            a, b = left.get(name), right.get(name)
            if a and b:
                value = self.merge_values(a.value, b.value)
                merged[name] = Binding(value, tuple(sorted(set(a.first + b.first))), a.definite and b.definite)
            else:
                binding = a or b
                merged[name] = Binding(binding.value, binding.first, False)
        return merged

    def merge_values(self, a, b):
        literal = a.literal if a.literal is not _UNKNOWN and type(a.literal) is type(b.literal) and a.literal == b.literal else _UNKNOWN
        callback = None
        if a.callable and b.callable and a.callable.parameters == b.callable.parameters and a.callable.returns == b.callable.returns:
            callback = CallableValue(a.callable.parameters, a.callable.returns,
                                     tuple(sorted(set(a.callable.targets + b.callable.targets))),
                                     tuple(sorted(set(a.callable.captures + b.callable.captures))),
                                     a.callable.conditional or b.callable.conditional)
        return Value(a.types | b.types, literal, a.items if a.items == b.items else None, callback)

    def _collection_operation(self, identity, node, quiet=False, failures=()):
        if not quiet:
            self._record_call(node)
            self.failures.update(failures)
            if self.active:
                self.active.operations.add(identity)

    @staticmethod
    def _nested_validation_failures(schema):
        # Traversal depth follows the exact recursive data schema. This bound is
        # separate from recursive application call-graph failures.
        return ("RecursionError",) if schema is not None and schema.name not in SCALARS else ()

    def _collection_callback(self, callback, parameters, returns, node, env, quiet):
        schema = TypeSpec("Callable", tuple(parameters), returns)
        self.graph.types[str(schema)] = schema
        if not self.matches(callback, str(schema)):
            if not quiet:
                self.emit("PAL221", node, f"collection callback requires resolved pure {schema} with stable captures")
            return False
        if not quiet:
            self._ready_callable(callback, env, node)
            evidence = callback.callable
            if evidence.conditional:
                self.failures.update(CALLABLE_FAILURES)
            for identity in evidence.targets:
                info = self.graph.functions[identity]
                if self.active:
                    self.active.calls.add(identity)
                    self.active.dependencies.update(info.dependencies)
                self._depend(info.analyzer.path)
        return True

    def _collection_call(self, node, env, quiet):
        """Finite resolved direct methods; no arbitrary attribute dispatch or protocols."""
        if not isinstance(node.func, ast.Attribute):
            return None
        method, expression = node.func.attr, node.func.value
        typed = None
        if isinstance(expression, ast.Subscript) and self._type_identity(expression.value, self.locals) in COLLECTIONS:
            kind = self._annotation(expression, extra_names=self.locals)
            typed = self.graph.types.get(kind)
            owner = Value.exact("collection_class:" + typed.name) if typed else UNKNOWN
        else:
            owner = self._expr(expression, env, quiet=quiet)
        schema = self.graph.types.get(owner.kind)
        constructor = owner.kind and owner.kind.startswith("collection_class:")
        if not constructor and (schema is None or schema.name not in COLLECTIONS):
            return None
        def reject(reason):
            if not quiet:
                self.emit("PAL221", node, reason)
            return UNKNOWN
        if node.keywords or any(isinstance(a, ast.Starred) for a in node.args):
            return reject("collection operations require their published fixed positional signature; of accepts explicit positional items")
        values = [self._expr(arg, env, quiet=quiet) for arg in node.args]
        if constructor:
            name = owner.kind.split(":", 1)[1]
            if method != "of":
                return reject(f"{name} constructor contract is {name}.of(*explicit admitted items)")
            if name in {"Vector", "Set"}:
                inferred = self.graph.types.get(values[0].kind) if values else None
                element = typed.arguments[0] if typed else inferred
                if not self._data_schema(element) or any(not self.matches(v, str(element)) for v in values):
                    return reject("collection elements must establish one recursively admitted exact data schema; empty of requires explicit type arguments")
                if name == "Set" and element.name not in SCALARS:
                    return reject("Set elements require one homogeneous exact scalar domain")
                result = self._value_schema(name, (element,))
            else:
                pairs = [self.graph.types.get(v.kind) for v in values]
                if any(p is None or p.name != "tuple" or p.variadic or len(p.arguments) != 2 for p in pairs):
                    return reject("map of inputs must be exact fixed two-element key/value tuples")
                arguments = typed.arguments if typed else pairs[0].arguments if pairs else ()
                if len(arguments) != 2 or arguments[0].name not in SCALARS or not self._data_schema(arguments[1]):
                    return reject("map requires homogeneous exact scalar keys and admitted exact values; empty of requires explicit type arguments")
                pair = TypeSpec("tuple", tuple(arguments))
                self.graph.types[str(pair)] = pair
                if any(not self.matches(v, str(pair)) for v in values):
                    return reject(f"map entries require {pair}")
                result = self._value_schema(name, arguments)
            nested = element if name == "Vector" else arguments[1] if name in {"Map", "OrderedMap"} else None
            self._collection_operation(name + ".of", node, quiet, self._nested_validation_failures(nested))
            return result
        name, arguments = schema.name, schema.arguments
        identity = name + "." + method
        if name == "Vector" and method in {"map", "filter", "fold"} and (self.definition_mode or self.initializing):
            return reject("higher-order collection callback invocation is confined to checked function bodies; module/default initialization remains closed data construction")
        result = None
        failures = ()
        if name == "Vector":
            element = arguments[0]
            if method == "appended" and len(values) == 1 and self.matches(values[0], str(element)):
                result = owner
                failures = self._nested_validation_failures(element)
            elif method == "updated_at" and len(values) == 2 and values[0].kind == "int" and self.matches(values[1], str(element)):
                result, failures = owner, ("IndexError", *self._nested_validation_failures(element))
            elif method == "concat" and len(values) == 1 and self.matches(values[0], str(schema)):
                result = owner
                failures = self._nested_validation_failures(element)
            elif method in {"map", "filter"} and len(values) == 1:
                callback = values[0]
                returned = self.graph.types.get(callback.callable.returns) if callback.callable else None
                if method == "filter":
                    returned = self.graph.types["bool"]
                if not self._data_schema(returned) or not self._collection_callback(callback, (element,), returned, node.args[0], env, quiet):
                    return reject(f"Vector.{method} requires a checked pure fixed callback with admitted result")
                result = owner if method == "filter" else self._value_schema("Vector", (returned,))
                if method == "map":
                    failures = self._nested_validation_failures(returned)
            elif method == "fold" and len(values) == 2:
                callback = values[0].callable
                accumulator = self.graph.types.get(callback.parameters[0]) if callback and len(callback.parameters) == 2 else None
                if not self._data_schema(accumulator) or not self.matches(values[1], str(accumulator)) or not self._collection_callback(values[0], (accumulator, element), accumulator, node.args[0], env, quiet):
                    return reject("Vector.fold requires (checked pure Callable[[A,T],A], admitted A initial)")
                result = self.annotation_value(str(accumulator))
                failures = self._nested_validation_failures(accumulator)
        elif name in {"Map", "OrderedMap"}:
            key, value = arguments
            if method == "updated" and len(values) == 2 and self.matches(values[0], str(key)) and self.matches(values[1], str(value)):
                result = owner
                failures = self._nested_validation_failures(value)
            elif method == "without" and len(values) == 1 and self.matches(values[0], str(key)):
                result = owner
            elif method == "contains" and len(values) == 1 and self.matches(values[0], str(key)):
                result = Value.exact("bool")
            elif method == "get" and len(values) == 2 and self.matches(values[0], str(key)) and self.matches(values[1], str(value)):
                result = self.annotation_value(str(value))
                failures = self._nested_validation_failures(value)
            elif method == "merge" and len(values) == 1 and self.matches(values[0], str(schema)):
                result = owner
                failures = self._nested_validation_failures(value)
            elif not values and method in ({"entries", "keys", "values"} if name == "OrderedMap" else {"ordered_entries", "ordered_keys", "ordered_values"}):
                item = TypeSpec("tuple", (key, value)) if method.endswith("entries") else key if method.endswith("keys") else value
                self.graph.types[str(item)] = item
                result = self._value_schema("Vector", (item,))
        elif name == "Set":
            element = arguments[0]
            if method in {"added", "without", "contains"} and len(values) == 1 and self.matches(values[0], str(element)):
                result = Value.exact("bool") if method == "contains" else owner
            elif method in {"union", "intersection", "difference"} and len(values) == 1 and self.matches(values[0], str(schema)):
                result = owner
            elif method == "ordered_values" and not values:
                result = self._value_schema("Vector", (element,))
        if result is None:
            return reject(f"{identity} has no supported signature for these operands; unordered general traversal/callbacks are excluded")
        self._collection_operation(identity, node, quiet, failures)
        return result

    def _statement(self, node, env):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            call = node.value
            owner = self._expr(call.func.value, env, quiet=True)
            schema = self.graph.types.get(owner.kind)
            if schema and schema.name in COLLECTIONS and call.func.attr in RETURN_ONLY_UPDATES:
                self._expr(call, env)
                self.emit("PAL250", node, f"{schema.name}.{call.func.attr} returns a new value; its result is ignored", origin="persistent return-only operation")
                return env
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info = self.infos.get(id(node))
            if info is None:
                self.emit("PAL120", node, "nested function lacks a checked declaration")
                return env
            if node.name in env and not self.in_dead:
                self.emit("PAL101", node, f"`{node.name}` is already initialized", first=env[node.name].first[0])
            info.enclosing = dict(env)
            if self.active:
                info.enclosing.update({n: Binding(v, (self.active.node.lineno,)) for n, v in self.active.captures.items() if n not in self.locals})
            self.function(info)
            if self.active:
                self.active.capture_uses.update(info.capture_uses & self.active.captures.keys())
            self.failures.update(info.definition_failures)
            env[node.name] = Binding(info.value(), (node.lineno,))
            return env
        if isinstance(node, ast.Return):
            value = self._expr(node.value, env) if node.value else Value.exact("None", None)
            self._ready_callable(value, env, node)
            if self.active:
                self.active.return_value = self.merge_values(self.active.return_value, value) if self.active.return_value else value
            if not self.matches(value, self.return_type):
                self.emit("PAL211", node, f"return requires {self.return_type}; found {self._describe(value)}")
            return None
        if isinstance(node, ast.AnnAssign):
            value = self._expr(node.value, env) if node.value is not None else UNKNOWN
            if not isinstance(node.target, ast.Name) or node.value is None:
                self.emit("PAL110", node, "annotated initialization requires one name and a value")
                return env
            expected = self._annotation(node.annotation)
            if expected and not self.matches(value, expected):
                self.emit("PAL210", node, f"binding `{node.target.id}` requires {expected}; found {self._describe(value)}")
            if node.target.id in env and not self.in_dead:
                self.emit("PAL101", node, f"`{node.target.id}` is already initialized", first=env[node.target.id].first[0])
            else:
                env[node.target.id] = Binding(value, (node.lineno,))
            return env
        return super()._statement(node, env)

    def _expr(self, node, env, *, quiet=False):
        def reject(rule, reason):
            if not quiet:
                self.emit(rule, node, reason)
            return UNKNOWN
        if isinstance(node, ast.Name):
            binding = env.get(node.id)
            if binding:
                if not binding.definite:
                    return reject("PAL102", f"`{node.id}` is not initialized on every continuing path")
                return binding.value
            if node.id in self.locals:
                return reject("PAL240" if node.id in BUILTINS else "PAL102", f"local `{node.id}` is not initialized or shadows an approved operation")
            if self.active and node.id in self.active.captures:
                value = self.active.captures[node.id]
                self.active.capture_uses.add(node.id)
                return value
            if self.active and node.id in self.active.enclosing_names:
                return reject("PAL240", f"captured binding `{node.id}` is not established as stable and initialized")
            symbol = self.symbols.get(node.id)
            if symbol and self._symbol_stable(node.id, symbol):
                value = self._resolve_symbol(symbol, node, quiet)
                if value.types:
                    return value
            if node.id in BUILTINS and node.id not in self.global_writes and not self._module_changed("builtins", node.id):
                return Value.exact("builtin:" + node.id)
            return reject("PAL240", f"binding `{node.id}` is not a statically established stable dependency")
        if isinstance(node, ast.Attribute):
            owner = self._expr(node.value, env, quiet=quiet)
            if owner.kind and owner.kind.startswith("module:"):
                module = owner.kind.split(":", 1)[1]
                if self._module_changed(module, node.attr):
                    return reject("PAL240", f"resolved dependency `{module}.{node.attr}` has an analyzed replacement")
                if module == "builtins" and node.attr in BUILTINS:
                    return Value.exact("builtin:" + node.attr)
                if module == "pyalamode" and node.attr in COLLECTIONS and self._foundation_available(module):
                    return Value.exact("collection_class:" + node.attr)
                target = self.graph.modules.get(module)
                if target:
                    symbol = target.symbols.get(node.attr)
                    if symbol and target._symbol_stable(node.attr, symbol):
                        self._depend(target.path)
                        return target._resolve_symbol(symbol, node, quiet)
                if module + "." + node.attr in self.graph.modules:
                    return Value.exact("module:" + module + "." + node.attr)
            return reject("PAL201", "attribute access is admitted only for statically resolved module dependencies")
        if isinstance(node, ast.Subscript):
            owner = self._expr(node.value, env, quiet=quiet)
            schema = self.graph.types.get(owner.kind)
            if schema is None or schema.name not in {"Vector", "Map", "OrderedMap", "tuple"}:
                return reject("PAL201", "indexing requires an admitted exact Vector/map/tuple contract")
            if isinstance(node.slice, ast.Slice):
                if schema.name not in {"Vector", "tuple"}:
                    return reject("PAL210", "maps have key lookup, not slicing")
                bounds = [self._expr(bound, env, quiet=quiet) if bound is not None else Value.exact("None", None)
                          for bound in (node.slice.lower, node.slice.upper, node.slice.step)]
                if any(value.kind not in {"int", "None"} for value in bounds):
                    return reject("PAL210", "slice bounds require exact int or None; bool and custom index dispatch are excluded")
                if not quiet:
                    self.failures.add("ValueError")
                if schema.name == "Vector" or schema.variadic:
                    self._collection_operation(schema.name + ".slice", node, quiet)
                    return owner
                if any(v.literal is _UNKNOWN for v in bounds):
                    return reject("PAL210", "fixed tuple slicing requires literal bounds to establish its exact result schema")
                start, stop, step = (v.literal for v in bounds)
                if step == 0:
                    return reject("PAL210", "a fixed tuple zero-step slice has no completing result schema")
                result = self._value_schema("tuple", schema.arguments[slice(start, stop, step)])
                self._collection_operation("tuple.slice", node, quiet)
                return result
            index = self._expr(node.slice, env, quiet=quiet)
            if schema.name in {"Map", "OrderedMap"}:
                if not self.matches(index, str(schema.arguments[0])):
                    return reject("PAL221", "map lookup key does not establish its exact scalar key domain")
                self._collection_operation(schema.name + ".lookup", node, quiet, ("KeyError",))
                return self.annotation_value(str(schema.arguments[1]))
            if index.kind != "int":
                return reject("PAL210", "sequence index requires exact int; bool and custom index dispatch are excluded")
            if schema.name == "Vector" or schema.variadic:
                element = schema.arguments[0]
            elif type(index.literal) is int and -len(schema.arguments) <= index.literal < len(schema.arguments):
                element = schema.arguments[index.literal]
            else:
                return reject("PAL210", "fixed tuple index requires an in-range literal to establish its exact result schema")
            self._collection_operation(schema.name + ".index", node, quiet, ("IndexError",))
            return self.annotation_value(str(element))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = self._expr(node.operand, env, quiet=quiet)
            if operand.kind != "int":
                return reject("PAL210", "integer unary operation requires exact int")
            literal = (-operand.literal if isinstance(node.op, ast.USub) else operand.literal) if type(operand.literal) is int else _UNKNOWN
            return Value.exact("int", literal)
        if isinstance(node, ast.Compare):
            left = self._expr(node.left, env, quiet=quiet)
            # Membership is a characterized homogeneous scalar lookup, never generic iteration.
            if len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.NotIn)):
                right = self._expr(node.comparators[0], env, quiet=quiet)
                schema = self.graph.types.get(right.kind)
                if schema and schema.name in {"Map", "OrderedMap", "Set"} and self.matches(left, str(schema.arguments[0])):
                    self._collection_operation(schema.name + ".contains", node, quiet)
                    return Value.exact("bool")
                return reject("PAL210", "membership requires a homogeneous exact map key or Set element; arbitrary iteration is excluded")
            schema = self.graph.types.get(left.kind)
            if schema and schema.name in COLLECTIONS | {"tuple"} and not any(isinstance(op, (ast.Is, ast.IsNot)) for op in node.ops):
                previous = left
                for operation, comparator in zip(node.ops, node.comparators):
                    value = self._expr(comparator, env, quiet=quiet)
                    if not isinstance(operation, (ast.Eq, ast.NotEq)) or not self.matches(value, previous.kind):
                        return reject("PAL210", "collection/tuple equality requires the same recursively exact data schema; arbitrary ordering is excluded")
                    previous = value
                recursive = any(arg.name not in SCALARS for arg in schema.arguments)
                self._collection_operation(schema.name + ".equivalent", node, quiet, ("RecursionError",) if recursive else ())
                return Value.exact("bool")
        if isinstance(node, ast.Tuple):
            if any(isinstance(item, ast.Starred) for item in node.elts):
                return reject("PAL201", "tuple unpacking has no supported construction contract")
            items = tuple(self._expr(item, env, quiet=quiet) for item in node.elts)
            if any(not value.types or value.callable or (value.kind and value.kind.startswith(("module:", "builtin:"))) for value in items):
                return reject("PAL221", "tuple contents must be recursively admitted immutable data; callable/module objects are not tuple data")
            args = tuple(self.graph.types[value.kind] for value in items if value.kind in self.graph.types)
            if len(args) != len(items):
                return reject("PAL221", "tuple element exact contract is ambiguous")
            schema = TypeSpec("tuple", args)
            self.graph.types[str(schema)] = schema
            return Value(frozenset({str(schema)}), items=items)
        if isinstance(node, ast.IfExp):
            condition = self._expr(node.test, env, quiet=quiet)
            yes, no = self._expr(node.body, env, quiet=quiet), self._expr(node.orelse, env, quiet=quiet)
            if condition.kind != "bool":
                return reject("PAL210", "conditional expression requires exact bool")
            return self.merge_values(yes, no)
        if isinstance(node, ast.Call):
            collection = self._collection_call(node, env, quiet)
            if collection is not None:
                return collection
            target = self._expr(node.func, env, quiet=quiet)
            if target.kind and target.kind.startswith("builtin:"):
                name = target.kind.split(":", 1)[1]
                if node.keywords or any(isinstance(arg, ast.Starred) for arg in node.args):
                    return reject("PAL230", f"{name} admits only its published positional signature")
                values = [self._expr(arg, env, quiet=quiet) for arg in node.args]
                kinds = [v.kind for v in values]
                if name == "abs" and kinds == ["int"]:
                    return Value.exact("int")
                if name == "len" and len(kinds) == 1 and (kinds[0] in {"str", "bytes"} or self.graph.types.get(kinds[0], TypeSpec("")).name in {"tuple", *COLLECTIONS}):
                    schema = self.graph.types.get(kinds[0])
                    if schema and schema.name in COLLECTIONS:
                        self._collection_operation(schema.name + ".len", node, quiet)
                    return Value.exact("int")
                if name in {"min", "max"} and len(kinds) >= 2 and len(set(kinds)) == 1 and kinds[0] in {"int", "str", "bytes"}:
                    return Value.exact(kinds[0])
                return reject("PAL210", f"{name} inputs do not establish its exact supported signature")
            if not target.callable:
                return reject("PAL230", "call target is not a resolved checked callable or characterized builtin")
            if self.definition_mode or self.initializing:
                return reject("PAL230", "definition-time values use closed stable data expressions and approved builtins; checked application invocation is confined to function bodies")
            callback = target.callable
            if not quiet:
                self._record_call(node)
                self._ready_callable(target, env, node)
            if callback.targets:
                if callback.conditional:
                    if node.keywords or len(node.args) != len(callback.parameters) or any(isinstance(a, ast.Starred) for a in node.args):
                        return reject("PAL221", "a conditional callback alternative requires its exact fixed positional signature")
                    for arg, expected in zip(node.args, callback.parameters):
                        if not self.matches(self._expr(arg, env, quiet=quiet), expected) and not quiet:
                            self.emit("PAL221", arg, f"conditional callback argument requires {expected}")
                    if not quiet:
                        self.failures.update(CALLABLE_FAILURES)
                infos = [self.graph.functions[identity] for identity in callback.targets]
                for info in infos:
                    self._checked_inputs(node, info, env, quiet)
                    if self.active:
                        self.active.calls.add(info.identity)
                        self.active.dependencies.update(info.dependencies)
                    self._depend(info.analyzer.path)
                returns = {info.returns for info in infos}
                if len(infos) == 1 and not callback.conditional and self.graph.types.get(infos[0].returns, TypeSpec("")).name == "Callable":
                    info = infos[0]
                    if info.parent is None and not info.analyzed and not info.analyzing:
                        info.analyzer.function(info)
                    if info.return_value and info.return_value.callable:
                        return info.return_value
                return self.annotation_value(next(iter(returns))) if len(returns) == 1 else UNKNOWN
            if callback.conditional:
                if node.keywords or len(node.args) != len(callback.parameters) or any(isinstance(a, ast.Starred) for a in node.args):
                    return reject("PAL221", "callback invocation requires its exact fixed positional signature")
                for arg, expected in zip(node.args, callback.parameters):
                    value = self._expr(arg, env, quiet=quiet)
                    if not self.matches(value, expected):
                        if not quiet:
                            self.emit("PAL221", arg, f"callback argument requires {expected}; found {self._describe(value)}")
                if not quiet:
                    self.failures.update(CALLABLE_FAILURES)
                return self.annotation_value(callback.returns)
            return reject("PAL230", "callable annotation alone does not establish invocation evidence")
        return super()._expr(node, env, quiet=quiet)

    def _checked_inputs(self, node, info, env, quiet=False):
        positional = [n for n, kind in info.kinds.items() if kind != "keyword_only"]
        supplied = dict(zip(positional, node.args))
        malformed = len(node.args) > len(positional) or any(isinstance(arg, ast.Starred) for arg in node.args)
        for keyword in node.keywords:
            if keyword.arg is None or keyword.arg not in info.parameters or keyword.arg in supplied or info.kinds.get(keyword.arg) == "positional_only":
                malformed = True
            else:
                supplied[keyword.arg] = keyword.value
        # Default existence is syntactic so forward/recursive calls do not depend on analysis order.
        args = info.node.args
        pos = args.posonlyargs + args.args
        default_names = {arg.arg for arg in pos[-len(args.defaults):]} if args.defaults else set()
        default_names |= {arg.arg for arg, value in zip(args.kwonlyargs, args.kw_defaults) if value is not None}
        if malformed or set(info.parameters) - set(supplied) - default_names:
            if not quiet:
                self.emit("PAL221", node, f"call to `{info.qualified}` does not establish its required signature")
        for name, arg in supplied.items():
            value = self._expr(arg, env, quiet=quiet)
            expected = info.parameters.get(name)
            if expected and not self.matches(value, expected) and not quiet:
                self.emit("PAL221", arg, f"argument `{name}` of `{info.qualified}` requires {expected}; found {self._describe(value)}")

    def _call_inputs(self, node, contract, env):
        info = self.graph.functions.get(contract.path + "::" + contract.name)
        if info:
            self._checked_inputs(node, info, env)

    def _ordinary_resolved_info(self, expression, env):
        value = self._expr(expression, env, quiet=True)
        if value.callable and len(value.callable.targets) == 1:
            return self.graph.functions[value.callable.targets[0]]
        return None

    def _ready_callable(self, value, env, node, seen=None):
        if not value.callable or not self.active:
            return
        seen = set() if seen is None else seen
        for target in value.callable.targets:
            if target in seen:
                continue
            seen.add(target)
            info = self.graph.functions[target]
            if info.parent is self.active:
                for name in info.capture_uses:
                    capture = info.captures[name]
                    binding = env.get(name)
                    if binding is None and self.active and name in self.active.captures:
                        binding = Binding(self.active.captures[name], (self.active.node.lineno,))
                    if not binding or not binding.definite:
                        self.emit("PAL240", node, f"callable `{info.qualified}` requires captured cell `{name}` initialized before invocation or escape")
                    elif capture.callable:
                        self._ready_callable(binding.value, env, node, seen)

    def finish(self):
        self.result.dependencies = {path: hashlib.sha256(self.graph.analyzers[path].source.encode()).hexdigest()
                                    for path in sorted(self.dependencies) if path in self.graph.analyzers and path != self.path}
        if self.result.mode == "audit" or self.result.diagnostics:
            self.result.initialization_evidence = "unverified initialization" if self.module_mode else self.result.initialization_evidence
            for contract in self.result.contracts:
                contract.enforcement = self.result.mode
                contract.source_evidence = "unverified: audit or failed selected gate"
                contract.freshness = "no successful checked claim"
        self.result.diagnostics.sort(key=lambda d: (d.line, d.column, d.rule))


def analyze_sources(sources: dict[str, str], *, root: str | Path, audit: bool = False,
                    policy: dict | None = None) -> dict[str, CheckResult]:
    """Analyze a captured source graph without application imports or user evaluation."""
    return SourceGraph(sources, Path(root).resolve(), audit, policy).analyze()


def analyze_source(source: str, path: str = "<source>", *, audit: bool = False,
                   policy: dict | None = None) -> CheckResult:
    """Analyze text only. Cross-module callers use analyze_sources or analyze_file."""
    return analyze_sources({path: source}, root=Path(path).resolve().parent, audit=audit, policy=policy)[path]


def analyze_file(path: str | Path, *, audit: bool = False, policy: dict | None = None) -> CheckResult:
    resolved = Path(path).resolve()
    sources, errors = load_sources([resolved], resolved.parent)
    if errors:
        result = CheckResult(str(resolved), "", diagnostics=errors, mode="audit" if audit else "strict")
        return result
    results = analyze_sources(sources, root=resolved.parent, audit=audit, policy=policy)
    result = results[str(resolved)]
    # Dependency failures cannot be hidden by requesting only one entry file.
    for other in results.values():
        if other is not result:
            result.diagnostics.extend(other.diagnostics)
    return result
