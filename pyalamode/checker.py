"""Closed immutable source checker. Application source is never imported or evaluated."""

from __future__ import annotations

import ast
import hashlib
import io
import json
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

from .model import (CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, CheckResult,
                    FunctionContract, SCALARS, diagnostic, foundation_identities, runtime_environment)
from .standard_contracts import (STANDARD_NAMES, STANDARD_NATIVE, STANDARD_VERSION,
                                 SCALAR_SIGNATURES, operation_contract, setup_contract)
from .integration_contracts import (INTEGRATION_NAMES, INTEGRATION_FOUNDATIONS,
                                    INTEGRATION_VERSION, integration_snapshot)

BUILTINS = frozenset({"abs", "min", "max", "len"})
COLLECTIONS = frozenset({"Vector", "OrderedMap", "Map", "Set"})
DOMAIN_TYPES = frozenset({"Option", "Result"})
DOMAIN_CASES = frozenset({"Some", "Nothing", "Ok", "Err"})
DOMAIN_DECORATORS = frozenset({"oneof", "variant"})
DOMAIN_PRIMITIVES = frozenset({"oneof", "variant", "case", "accumulate", "failure_value", "Failure", *DOMAIN_TYPES, *DOMAIN_CASES})
HANDLER_CATEGORIES = frozenset({"ZeroDivisionError", "IndexError", "KeyError", "ValueError", "RecursionError", "RuntimeError", "OSError", "UnicodeError"})
HANDLER_COVERAGE = {category: frozenset({category}) for category in HANDLER_CATEGORIES}
HANDLER_COVERAGE["ValueError"] |= {"UnicodeError"}
HANDLER_COVERAGE["RuntimeError"] |= {"RecursionError"}
RECORD_PRIMITIVES = frozenset({"record", "replace"})
BOUNDARY_PRIMITIVES = frozenset({"freeze", "thaw", "dataclass_adapter", "namedtuple_adapter"})
EFFECT_FAMILIES = frozenset({"IO", "State", "Clock", "Random", "Environment"})
CAPABILITIES = {"IOCapability": "IO", "StateCapability": "State", "ClockCapability": "Clock", "RandomCapability": "Random", "EnvironmentCapability": "Environment"}
CAPABILITY_OPERATIONS = {
    "IOCapability": {"read_text": (("str",), "str", ("OSError", "UnicodeError", "ValueError", "RuntimeError", "KeyError")), "write_text": (("str", "str"), "None", ("OSError", "UnicodeError", "ValueError", "RuntimeError", "KeyError"))},
    "StateCapability": {"get": ((), "int", ("RuntimeError",)), "set": (("int",), "None", ("RuntimeError",))},
    "ClockCapability": {"now_ns": ((), "int", ("RuntimeError", "OSError", "IndexError"))},
    "RandomCapability": {"below": (("int",), "int", ("RuntimeError", "ValueError", "OSError", "IndexError"))},
    "EnvironmentCapability": {"get": (("str", "str"), "str", ("RuntimeError", "ValueError", "OSError", "UnicodeError"))},
}
PROVIDER_FACTORIES = {"live_io": "IOCapability", "recorded_io": "IOCapability", "state": "StateCapability", "live_clock": "ClockCapability", "recorded_clock": "ClockCapability", "live_random": "RandomCapability", "recorded_random": "RandomCapability", "live_environment": "EnvironmentCapability", "recorded_environment": "EnvironmentCapability"}
EFFECT_PRIMITIVES = frozenset({"effects", "borrow", "Effectful", *EFFECT_FAMILIES, *CAPABILITIES, *PROVIDER_FACTORIES})
CALLABLE_FAILURES = frozenset({"ZeroDivisionError", "RecursionError", "IndexError", "KeyError", "ValueError", "UnicodeError"})
# Trusted foundation inventory only; these names are not application call admission.
EFFECT_FOUNDATIONS = {
    "builtins": frozenset({"type", "object", "tuple", "list", "dict", "set", "len", "any", "all", "enumerate", "next", "str", "int", "bool", "bytes", "open", "range", "min", "getattr", "repr", "isinstance", "classmethod", "staticmethod", "ValueError", "TypeError", "RuntimeError", "AttributeError", "OSError", "UnicodeError", "PermissionError", "IndexError", "KeyError", "FileNotFoundError", "NotADirectoryError", "BytesWarning", "__build_class__", "__import__"}),
    "types": frozenset({"GenericAlias"}),
    "time": frozenset({"time_ns"}),
    "sys": frozenset({"getfilesystemencoding", "getfilesystemencodeerrors", "flags"}),
    "os": frozenset({"environ", "_Environ", "urandom", "fspath", "fsencode", "fsdecode", "getcwd", "getcwdb", "stat", "lstat", "readlink", "path"}),
    "posixpath": frozenset({"_get_sep", "join", "isabs", "normpath", "realpath", "abspath", "commonpath", "split", "splitdrive", "islink", "isdir", "_joinrealpath", "normcase", "exists", "lexists", "sep", "curdir", "pardir", "os", "stat", "genericpath"}),
    "genericpath": frozenset({"isdir", "_check_arg_types", "os", "stat"}),
    "io": frozenset({"open", "TextIOWrapper", "FileIO", "BufferedReader", "BufferedWriter"}),
    "_io": frozenset({"open", "TextIOWrapper", "FileIO", "BufferedReader", "BufferedWriter"}),
    "stat": frozenset({"S_ISLNK", "S_IFMT", "S_IFLNK", "S_ISDIR", "S_IFDIR"}),
    "typing": frozenset({"_CallableGenericAlias"}),
    "collections.abc": frozenset({"_CallableGenericAlias", "Callable"}),
    "_collections_abc": frozenset({"Mapping", "MutableMapping"}),
}

RETURN_ONLY_UPDATES = frozenset({"appended", "updated_at", "concat", "updated", "without", "merge", "added", "union", "intersection", "difference"})
# Actual explicit/implicit foundation reads of the shipped collections-v1
# backend, including its declaration/import initialization. This is a closed
# dependency inventory, not admission for application calls to these names.
COLLECTION_FOUNDATIONS = {
    "builtins": frozenset({"type", "any", "all", "id", "set", "enumerate", "tuple", "len", "sorted", "repr", "hex", "zip", "iter", "next", "object", "getattr", "bool", "int", "str", "bytes", "classmethod", "TypeError", "AttributeError", "IndexError", "KeyError", "ValueError", "__build_class__", "__import__"}),
    "types": frozenset({"FunctionType", "GenericAlias"}),
}
RECORD_FOUNDATIONS = {
    "builtins": COLLECTION_FOUNDATIONS["builtins"] | frozenset({"list", "dict", "frozenset", "range", "staticmethod", "RuntimeError", "SyntaxError", "compile", "callable", "isinstance", "issubclass", "hasattr", "setattr", "delattr", "vars", "reversed", "map", "eval", "exec", "NotImplemented", "hash", "super"}),
    "sys": frozenset({"modules", "intern"}),
    "ast": frozenset({"parse", "Name", "Constant", "Subscript", "Tuple", "Attribute", "PyCF_ONLY_AST"}),
    "types": COLLECTION_FOUNDATIONS["types"] | frozenset({"ModuleType", "CodeType", "GetSetDescriptorType", "new_class", "resolve_bases", "prepare_class", "_calculate_meta", "MemberDescriptorType", "MappingProxyType"}),
    "dataclasses": frozenset({"make_dataclass", "dataclass", "field", "Field", "FrozenInstanceError", "_DataclassParams", "MISSING", "KW_ONLY", "InitVar", "_FIELD", "_FIELD_CLASSVAR", "_FIELD_INITVAR", "_FIELDS", "_PARAMS", "_POST_INIT_NAME", "_EMPTY_METADATA", "_HAS_DEFAULT_FACTORY", "_FuncBuilder", "_process_class", "_get_field", "_is_classvar", "_is_initvar", "_is_kw_only", "_fields_in_init_order", "_init_fn", "_init_param", "_field_init", "_field_assign", "_frozen_get_del_attr", "_hash_action", "_hash_add", "_hash_fn", "_tuple_str", "_set_new_attribute", "_replace", "recursive_repr", "sys", "types", "inspect", "keyword", "abc"}),
    "collections": frozenset({"namedtuple", "_sys", "_iskeyword", "_tuplegetter"}),
    "inspect": frozenset({"get_annotations"}),
    "keyword": frozenset({"iskeyword"}),
    "abc": frozenset({"update_abstractmethods"}),
    "reprlib": frozenset({"recursive_repr", "get_ident"}),
    "_thread": frozenset({"get_ident"}),
    "typing": frozenset({"ClassVar", "_GenericAlias"}),
}
_UNKNOWN = object()


def fingerprint(source: bytes, policy: dict | None = None) -> str:
    """Include source, edition, rules, target, policy, and operation identities."""
    metadata = json.dumps({"rules": CHECKER_VERSION, "edition": EDITION, "target": TARGET,
                           "operations": OPERATION_VERSION, "policy": policy or {},
                           "dependencies": ["pyalamode.fun@0.1.0", "CPython3.13.1 scalar builtins"],
                           "product_artifacts": foundation_identities(), "runtime_environment": runtime_environment()},
                          sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(metadata + b"\0" + source).hexdigest()


@dataclass(frozen=True)
class CapabilityValue:
    """Static interface/permission/lifetime evidence; never a runtime registry."""
    interface: str
    operations: tuple[str, ...]
    lifetime: str
    provider: str


@dataclass(frozen=True)
class Value:
    types: frozenset[str]
    literal: object = _UNKNOWN
    items: tuple[Value, ...] | None = None
    callable: CallableValue | None = None
    capability: CapabilityValue | None = None

    @classmethod
    def exact(cls, kind: str, literal: object = _UNKNOWN) -> Value:
        return cls(frozenset({kind}), literal)

    @property
    def kind(self) -> str | None:
        return next(iter(self.types)) if len(self.types) == 1 else None

    def with_callable(self, callback: CallableValue) -> Value:
        return Value(self.types, self.literal, self.items, callback, self.capability)


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
            first_binding=f"{self.path}:{first}" if first is not None else None,
            end_line=getattr(node, "end_lineno", None),
            end_column=getattr(node, "end_col_offset", -1) + 1 if getattr(node, "end_col_offset", None) is not None else None))

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
                                          line=getattr(error, "lineno", 1) or 1, column_encoding="unicode-codepoints"))
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

    def _add_failures(self, categories):
        self.failures.update(set(categories) - getattr(self, "handled_failures", set()))

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
            if node.id in getattr(self, "exception_tokens", set()):
                return reject("PAL340", "actual handler exceptions are opaque; only direct failure_value conversion is admitted")
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
                self._add_failures(("ZeroDivisionError",))
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
                        if isinstance(resolved_info, Value):
                            self._wrapper_inputs(call, resolved_info.callable, env, False)
                        elif resolved_info:
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
                    if hasattr(self, "symbols") and module:
                        symbol = self.symbols.get(statement.name)
                        if symbol and symbol.kind in {"record", "variant"} and self._symbol_stable(statement.name, symbol):
                            env[statement.name] = Binding(self._resolve_symbol(symbol, statement, True), (statement.lineno,))
                    continue
                calls(statement)
                if hasattr(self, "_ordinary_capability_writes"):
                    self._ordinary_capability_writes(statement, env)
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
                elif isinstance(statement, ast.With) and len(statement.items) == 1 and hasattr(self, "_ordinary_borrow_env"):
                    borrowed = self._ordinary_borrow_env(statement, env)
                    block(statement.body, borrowed or {}, lexical_writes, boundary, dict(aliases), external, module)
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
    effect_bound: tuple[str, ...] = ()

    def __str__(self) -> str:
        if self.name == "union":
            return " | ".join(map(str, self.arguments))
        if self.name.startswith("variant:"):
            return "Variant[" + repr(self.name[len("variant:"):]) + "]"
        if self.name.startswith("case:"):
            return "Case[" + repr(self.name[len("case:"):]) + "]"
        if self.name.startswith("record:"):
            return "Record[" + repr(self.name[len("record:"):]) + "]"
        if self.name == "tuple":
            if not self.arguments:
                return "tuple[()]"
            return "tuple[" + ", ".join(map(str, self.arguments)) + (", ..." if self.variadic else "") + "]"
        if self.name == "Callable":
            if self.effect_bound:
                return "Effectful[[" + ", ".join(map(str, self.arguments)) + "], " + str(self.result) + ", " + ", ".join(self.effect_bound) + "]"
            return "Callable[[" + ", ".join(map(str, self.arguments)) + "], " + str(self.result) + "]"
        if self.name in COLLECTIONS | DOMAIN_TYPES | (DOMAIN_CASES - {"Nothing"}):
            return self.name + "[" + ", ".join(map(str, self.arguments)) + "]"
        return self.name


def _contract_type(text: str) -> TypeSpec:
    """Decode our canonical cache schema, never a user annotation or Python value."""
    def parse(node):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            members = []
            for side in (node.left, node.right):
                member = parse(side)
                members.extend(member.arguments if member.name == "union" else (member,))
            return TypeSpec("union", tuple(members))
        if isinstance(node, ast.Name) and node.id in SCALARS | CAPABILITIES.keys() | {"Nothing"}:
            return TypeSpec(node.id)
        if isinstance(node, ast.Constant) and node.value is None:
            return TypeSpec("None")
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
            if node.value.id in {"Variant", "Case"} and isinstance(node.slice, ast.Constant) and type(node.slice.value) is str:
                return TypeSpec(node.value.id.lower() + ":" + node.slice.value)
            if node.value.id == "Record" and isinstance(node.slice, ast.Constant) and type(node.slice.value) is str:
                return TypeSpec("record:" + node.slice.value)
            parts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
            if node.value.id == "tuple":
                variadic = len(parts) == 2 and isinstance(parts[-1], ast.Constant) and parts[-1].value is Ellipsis
                return TypeSpec("tuple", tuple(parse(p) for p in (parts[:-1] if variadic else parts)), variadic=variadic)
            if node.value.id in {"Callable", "Effectful"} and len(parts) >= 2 and isinstance(parts[0], ast.List):
                return TypeSpec("Callable", tuple(parse(p) for p in parts[0].elts), parse(parts[1]), effect_bound=tuple(p.id for p in parts[2:]))
            if node.value.id in COLLECTIONS | DOMAIN_TYPES | (DOMAIN_CASES - {"Nothing"}):
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
    effect_bound: tuple[str, ...] = ()
    wrapper: str | None = None
    components: tuple[CallableValue, ...] = ()
    bound_arguments: tuple[tuple[str, str], ...] = ()
    obligation: str | None = None
    captured_callbacks: tuple[tuple[str, CallableValue], ...] = ()


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
    data_assertions: list[dict] = field(default_factory=list)
    declared_effects: set[str] = field(default_factory=set)
    required_effects: set[str] = field(default_factory=set)
    effect_origins: dict[str, set[str]] = field(default_factory=dict)
    borrow_scopes: list[dict] = field(default_factory=list)
    callable_dependencies: set[str] = field(default_factory=set)
    callable_arguments: dict[str, set[str]] = field(default_factory=dict)
    failure_edges: list[dict] = field(default_factory=list)
    patterns: list[dict] = field(default_factory=list)
    handlers: list[dict] = field(default_factory=list)
    direct_failures: set[str] = field(default_factory=set)
    external_operation_sites: dict[str, set[int]] = field(default_factory=dict)

    @property
    def identity(self) -> str:
        return self.analyzer.path + "::" + self.qualified

    def value(self) -> Value:
        positional = tuple(self.parameters[n] for n in self.parameters if self.kinds[n] != "keyword_only")
        schema = TypeSpec("Callable", tuple(self.analyzer.graph.types.get(t, TypeSpec("<unknown>")) for t in positional),
                          self.analyzer.graph.types.get(self.returns), effect_bound=tuple(sorted(self.declared_effects)))
        kind = str(schema)
        self.analyzer.graph.types[kind] = schema
        return Value.exact(kind).with_callable(CallableValue(
            positional, self.returns, (self.identity,), tuple((n, self.captures[n].kind or "unknown") for n in sorted(self.capture_uses)), effect_bound=tuple(sorted(self.declared_effects)),
            captured_callbacks=tuple((n, self.captures[n].callable) for n in sorted(self.capture_uses) if self.captures[n].callable)))


@dataclass(frozen=True)
class Symbol:
    kind: str
    name: str
    node: ast.AST | None = None


@dataclass
class RecordInfo:
    node: ast.ClassDef
    analyzer: FunctionalAnalyzer
    module: str
    fields: dict[str, str] = field(default_factory=dict)
    defaults: dict[str, Value] = field(default_factory=dict)
    failures: set[str] = field(default_factory=set)
    valid: bool = True
    ready: bool = False
    preparing: bool = False

    @property
    def schema(self):
        return TypeSpec("record:" + self.module + ":" + self.node.name)

    @property
    def identity(self):
        return str(self.schema)


@dataclass
class CaseInfo(RecordInfo):
    domain: str = ""

    @property
    def schema(self):
        return TypeSpec("case:" + self.module + ":" + self.domain + ":" + self.node.name)


@dataclass
class VariantInfo:
    node: ast.ClassDef
    analyzer: FunctionalAnalyzer
    module: str
    cases: dict[str, RecordInfo] = field(default_factory=dict)
    valid: bool = True
    ready: bool = False
    preparing: bool = False

    @property
    def identity(self):
        return str(TypeSpec("variant:" + self.module + ":" + self.node.name))

    @property
    def fingerprint(self):
        data = [(name, list(info.fields.items())) for name, info in self.cases.items()]
        return hashlib.sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()

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
    files = {"pyalamode": "__init__.py", "pyalamode.collections": "collections.py", "pyalamode.effects": "effects.py", "pyalamode.variants": "variants.py", "pyalamode.failures": "failures.py", "pyalamode.standard": "standard.py", "pyalamode.standard_contracts": "standard_contracts.py", "pyalamode.integrations": "integrations.py", "pyalamode.integration_contracts": "integration_contracts.py"}
    return name in files and path == Path(__file__).resolve().parent / files[name]


def load_sources(paths: list[Path], root: Path, raw_sources: dict[str, bytes] | None = None,
                 overlays: dict[str, str] | None = None, read_root: Path | None = None) -> tuple[dict[str, str], list]:
    """Read selected files and resolvable local imports, including package initialization."""
    sources: dict[str, str] = {}
    errors = []
    queue = list(paths)
    while queue:
        path = queue.pop(0).resolve()
        if read_root is not None and not path.is_relative_to(read_root):
            errors.append(diagnostic("PAL001", str(read_root), "editor source resolves outside workspace; refused before reading", origin="editor source ownership"))
            continue
        if str(path) in sources:
            continue
        try:
            if overlays and str(path) in overlays:
                text = overlays[str(path)]
                encoding, _ = tokenize.detect_encoding(io.BytesIO(text.encode("utf-8")).readline)
                raw = text.encode(encoding)
            else:
                raw = path.read_bytes()
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            source = raw.decode(encoding)
            if raw_sources is not None:
                raw_sources[str(path)] = raw
            sources[str(path)] = source
            tree = ast.parse(source, filename=str(path), feature_version=(3, 13))
        except (OSError, UnicodeError, SyntaxError, ValueError) as error:
            errors.append(diagnostic("PAL001", str(path), f"cannot read/parse source: {error}",
                                     line=getattr(error, "lineno", 1) or 1, column_encoding="unicode-codepoints"))
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

    def __init__(self, sources: dict[str, str], root: Path, audit: bool, policy: dict | None,
                 candidate_selection: dict | None = None):
        self.root, self.policy = root, policy or {}
        self.candidate_functions = set((candidate_selection or {}).get("functions", []))
        self.candidate_modules = set((candidate_selection or {}).get("modules", []))
        self.integration_snapshot = self.policy.get("_integration_snapshot") or integration_snapshot(self.policy, root)
        self.integrations = {row["identity"].rsplit(".", 1)[-1]: row for row in self.integration_snapshot["catalog"]}
        self.types = {kind: TypeSpec(kind) for kind in SCALARS}
        self.analyzers: dict[str, FunctionalAnalyzer] = {}
        self.modules: dict[str, FunctionalAnalyzer] = {}
        self.functions: dict[str, FunctionInfo] = {}
        self.records: dict[str, RecordInfo] = {}
        self.variants: dict[str, VariantInfo] = {}
        self.cases: dict[str, RecordInfo] = {}
        self.record_declarations: list[RecordInfo] = []
        self.variant_declarations: list[VariantInfo] = []
        for path, source in sources.items():
            analyzer = FunctionalAnalyzer(source, path, "audit" if audit else "strict", policy, self)
            self.analyzers[path] = analyzer
            module = _module_name(path, root)
            # Full-project discovery can select both name.py and name/__init__.py.
            # Match ordinary CPython package-before-module resolution rather than
            # allowing input ordering to choose an imported namespace.
            resolved = _local_path(root, module)
            if module not in self.modules or resolved == Path(path).resolve():
                self.modules[module] = analyzer
        for analyzer in self.analyzers.values():
            analyzer.prepare()
            for error in self.integration_snapshot["errors"]:
                analyzer.result.diagnostics.append(diagnostic("PAL001", analyzer.path, error, origin="integration policy/manifest"))
        for analyzer in self.analyzers.values():
            analyzer.discover()
            analyzer.discover_records()
        for analyzer in self.analyzers.values():
            analyzer.discover_variants()
        # Case lookup follows the chosen domain, including disjoint tag names;
        # shadow declarations remain reportable but cannot extend that catalog.
        self.cases = {case.identity: case for domain in self.variants.values() for case in domain.cases.values()}
        self.replaced_functions: set[str] = set()
        self.replaced_records: set[str] = set()
        self.replaced_variants: set[str] = set()
        self.domain_dependency_replacements: set[str] = set()
        self.replaced_foundations: set[tuple[str, str]] = set()
        self.collection_dependency_replacements: set[str] = set()
        self.record_dependency_replacements: set[str] = set()
        self.effect_dependency_replacements: set[str] = set()
        self.standard_dependency_replacements: set[str] = set()
        self.integration_dependency_replacements: set[str] = set()
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
                    if isinstance(target, ast.Subscript):
                        owner = target.value
                    reference = self.reference(analyzer, owner, aliases) if owner else None
                    if reference in self.functions:
                        self.replaced_functions.add(reference)
                    elif reference in self.records:
                        self.replaced_records.add(reference)
                    elif reference in self.variants or reference in self.cases:
                        self.replaced_variants.add(reference)
                    elif reference == "module:pyalamode.effects":
                        # Private imports can alias record/collection helpers as
                        # well as capability machinery. Conservatively gate the
                        # whole product after any such behavioral replacement.
                        self.replaced_foundations.add(("pyalamode", "*"))
                        self.record_dependency_replacements.add("pyalamode.effects.*")
                        self.effect_dependency_replacements.add("pyalamode.effects.*")
                    elif reference in {"module:pyalamode.records", "module:pyalamode.boundaries", "module:pyalamode.variants", "module:pyalamode.failures", "module:pyalamode.standard", "module:pyalamode.standard_contracts", "module:pyalamode.integrations", "module:pyalamode.integration_contracts"}:
                        self.replaced_foundations.update(("pyalamode", name) for name in RECORD_PRIMITIVES | BOUNDARY_PRIMITIVES | COLLECTIONS | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES | STANDARD_NAMES)
                        self.effect_dependency_replacements.add(reference[len("module:"):] + ".*")
                        self.record_dependency_replacements.add(reference[len("module:"):] + ".*")
                    elif reference in {"module:pyalamode", "module:pyalamode.collections"}:
                        self.replaced_foundations.add(("pyalamode", "*"))
                    elif reference and reference.startswith("module:") and reference[len("module:"):] in self.modules:
                        defined = self.modules[reference[len("module:"):]]
                        self.replaced_functions.update(info.identity for info in self.functions.values() if info.analyzer is defined)
                        self.replaced_records.update(info.identity for info in self.records.values() if info.analyzer is defined)
                        self.replaced_variants.update(info.identity for info in [*self.variants.values(), *self.cases.values()] if info.analyzer is defined)
                        self.replaced_foundations.add((reference[len("module:"):], "*"))
                    elif reference and reference.startswith("foundation:"):
                        _, module, attribute = reference.split(":", 2)
                        self.replaced_foundations.add((module, attribute))
                setter = self.reference(analyzer, node.func, aliases) if isinstance(node, ast.Call) else None
                # A resolved checked source function may have a collection
                # mutator's spelling (e.g. calculations.add). Its body is
                # inspected independently; the attribute call does not mutate
                # the defining module merely because of that spelling.
                dictionary_writer = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and setter not in self.functions and node.func.attr in {"__setitem__", "__delitem__", "update", "clear", "pop", "popitem", "setdefault", "append", "extend", "insert", "remove", "reverse", "sort", "add", "discard"}
                if isinstance(node, ast.Call) and (dictionary_writer or node.args and setter in {"foundation:builtins:setattr", "foundation:builtins:delattr"}):
                    reference = self.reference(analyzer, node.func.value if dictionary_writer else node.args[0], aliases)
                    if reference in self.functions:
                        self.replaced_functions.add(reference)
                    elif reference in self.records:
                        self.replaced_records.add(reference)
                    elif reference in self.variants or reference in self.cases:
                        self.replaced_variants.add(reference)
                    elif reference == "module:pyalamode.effects":
                        # Private imports can alias record/collection helpers as
                        # well as capability machinery. Conservatively gate the
                        # whole product after any such behavioral replacement.
                        self.replaced_foundations.add(("pyalamode", "*"))
                        self.record_dependency_replacements.add("pyalamode.effects.*")
                        self.effect_dependency_replacements.add("pyalamode.effects.*")
                    elif reference in {"module:pyalamode.records", "module:pyalamode.boundaries", "module:pyalamode.variants", "module:pyalamode.failures", "module:pyalamode.standard", "module:pyalamode.standard_contracts", "module:pyalamode.integrations", "module:pyalamode.integration_contracts"}:
                        self.replaced_foundations.update(("pyalamode", name) for name in RECORD_PRIMITIVES | BOUNDARY_PRIMITIVES | COLLECTIONS | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES | STANDARD_NAMES)
                        self.effect_dependency_replacements.add(reference[len("module:"):] + ".*")
                        self.record_dependency_replacements.add(reference[len("module:"):] + ".*")
                    elif reference in {"module:pyalamode", "module:pyalamode.collections"}:
                        self.replaced_foundations.add(("pyalamode", "*"))
                    elif reference and reference.startswith("module:") and reference[len("module:"):] in self.modules:
                        defined = self.modules[reference[len("module:"):]]
                        self.replaced_functions.update(info.identity for info in self.functions.values() if info.analyzer is defined)
                        self.replaced_records.update(info.identity for info in self.records.values() if info.analyzer is defined)
                        self.replaced_variants.update(info.identity for info in [*self.variants.values(), *self.cases.values()] if info.analyzer is defined)
                        self.replaced_foundations.add((reference[len("module:"):], "*"))
                    elif reference and reference.startswith("foundation:"):
                        _, module, attribute = reference.split(":", 2)
                        self.replaced_foundations.add((module, attribute))
                if isinstance(node, ast.Call):
                    # Lending native namespaces/classes/functions to an unknown
                    # ordinary call can expose their mutable behavior. Refuse the
                    # affected integration assumption without executing the call.
                    for argument in [*node.args, *(keyword.value for keyword in node.keywords)]:
                        reference = self.reference(analyzer, argument, aliases)
                        if reference and (reference.startswith("foundation:integrations:") or reference.startswith(("foundation:binascii:", "foundation:_sha2:", "foundation:_imp:", "foundation:sys:", "foundation:importlib:")) or reference in {"module:binascii", "module:_sha2", "module:pyalamode.integrations"}):
                            if reference.startswith("foundation:"):
                                _, module, attribute = reference.split(":", 2)
                                self.replaced_foundations.add((module, attribute))
                            else:
                                self.integration_dependency_replacements.add(reference[len("module:"):] + ".<unknown call escape>")
        for module, attributes in COLLECTION_FOUNDATIONS.items():
            for attribute in attributes:
                replaced = ((module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations
                            or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values()))
                if replaced:
                    self.collection_dependency_replacements.add(module + "." + attribute)
                    # Refuse all collection contracts conservatively. The fun
                    # marker and unrelated scalar bodies retain their own gates.
                    self.replaced_foundations.update(("pyalamode", name) for name in COLLECTIONS)
        for module, attributes in RECORD_FOUNDATIONS.items():
            for attribute in attributes:
                if ((module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations
                        or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values())):
                    self.record_dependency_replacements.add(module + "." + attribute)
                    self.replaced_foundations.update(("pyalamode", name) for name in RECORD_PRIMITIVES | BOUNDARY_PRIMITIVES)
        for module, attributes in EFFECT_FOUNDATIONS.items():
            for attribute in attributes:
                if ((module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations
                        or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values())):
                    self.effect_dependency_replacements.add(module + "." + attribute)
                    self.replaced_foundations.update(("pyalamode", name) for name in EFFECT_PRIMITIVES)
        for module, attributes in STANDARD_NATIVE.items():
            for attribute in attributes:
                if ((module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations
                        or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values())):
                    self.standard_dependency_replacements.add(module + "." + attribute)
        # Standard helpers recursively read the inherited exact-data machinery.
        self.standard_dependency_replacements.update(self.collection_dependency_replacements | self.record_dependency_replacements | self.domain_dependency_replacements)
        if self.standard_dependency_replacements:
            self.replaced_foundations.update(("pyalamode", name) for name in STANDARD_NAMES)
        # Binary IO now depends on both manual Unicode converters and their exact
        # scalar/helper foundations; a writer cannot reopen an implicit callback.
        if self.standard_dependency_replacements or any(("pyalamode", name) in self.replaced_foundations for name in {"utf8_encode", "utf8_decode"}):
            self.effect_dependency_replacements.add("pyalamode.standard.manual_utf8")
            self.replaced_foundations.update(("pyalamode", name) for name in EFFECT_PRIMITIVES)
        for identity in self.record_dependency_replacements | self.collection_dependency_replacements | self.effect_dependency_replacements:
            self.domain_dependency_replacements.add(identity)
        for module, attributes in {"builtins": HANDLER_CATEGORIES | {"UnicodeDecodeError", "UnicodeEncodeError", "UnicodeTranslateError", "BlockingIOError", "ChildProcessError", "ConnectionError", "BrokenPipeError", "ConnectionAbortedError", "ConnectionRefusedError", "ConnectionResetError", "FileExistsError", "FileNotFoundError", "InterruptedError", "IsADirectoryError", "NotADirectoryError", "PermissionError", "ProcessLookupError", "TimeoutError"}}.items():
            for attribute in attributes:
                if (module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values()):
                    self.domain_dependency_replacements.add(module + "." + attribute)
        if self.domain_dependency_replacements:
            self.replaced_foundations.update(("pyalamode", name) for name in DOMAIN_PRIMITIVES)
            self.standard_dependency_replacements.update(self.domain_dependency_replacements)
            self.replaced_foundations.update(("pyalamode", name) for name in STANDARD_NAMES)
        inherited_data = COLLECTIONS | RECORD_PRIMITIVES | DOMAIN_PRIMITIVES
        changed_data = {name for name in inherited_data if ("pyalamode", name) in self.replaced_foundations or
                        any(analyzer._attribute_changed(module, name) for module in ("pyalamode", "pyalamode.collections", "pyalamode.records", "pyalamode.variants", "pyalamode.failures") for analyzer in self.analyzers.values())}
        if changed_data:
            self.standard_dependency_replacements.update("pyalamode." + name for name in changed_data)
            self.replaced_foundations.update(("pyalamode", name) for name in STANDARD_NAMES)
            self.effect_dependency_replacements.add("pyalamode.standard.data_foundations")
            self.replaced_foundations.update(("pyalamode", name) for name in EFFECT_PRIMITIVES)
        for module, attributes in INTEGRATION_FOUNDATIONS.items():
            for attribute in attributes:
                if ((module, attribute) in self.replaced_foundations or (module, "*") in self.replaced_foundations
                        or any(analyzer._attribute_changed(module, attribute) for analyzer in self.analyzers.values())):
                    self.integration_dependency_replacements.add(module + "." + attribute)
        for module in ("pyalamode.integrations", "pyalamode.integration_contracts"):
            if any(identity.startswith(module + ".") for identity in self.record_dependency_replacements) or any(m == module for m, _ in self.replaced_foundations):
                self.integration_dependency_replacements.add(module + ".*")
        if any(module == "integrations" for module, _ in self.replaced_foundations):
            self.integration_dependency_replacements.add("pyalamode.integrations.<adapter behavior>")
        # Schema families depend on every contained exact case, even when a
        # receiving function only returns its input without matching it.
        for family, cases in {"Option": ("Some", "Nothing"), "Result": ("Ok", "Err")}.items():
            if any(("pyalamode", name) in self.replaced_foundations or
                   any(analyzer._attribute_changed(module, name) for module in ("pyalamode", "pyalamode.variants") for analyzer in self.analyzers.values())
                   for name in cases):
                self.replaced_foundations.add(("pyalamode", family))
        # Replacement identities must be established before annotation admission;
        # all signatures still precede bodies, including recursive components.
        for variant_info in self.variant_declarations:
            variant_info.analyzer.prepare_variant(variant_info)
        for record_info in self.record_declarations:
            record_info.analyzer.prepare_record(record_info)
        for info in self.functions.values():
            info.analyzer.declare_effects(info)
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
                if node.id in {"setattr", "delattr"} and node.id not in analyzer.global_writes:
                    return "foundation:builtins:" + node.id
                infos = [i for i in analyzer.infos.values() if i.node.name == node.id]
                return infos[0].identity if len(infos) == 1 else None
            if symbol.kind == "function":
                return symbol.name
            if symbol.kind in {"record", "variant"}:
                return symbol.name
            if symbol.kind == "module":
                # __init__ exports an effects function under the submodule name:
                # Python's import pyalamode.effects as alias binds that function.
                if symbol.name == "pyalamode.effects":
                    return "foundation:pyalamode:effects"
                return "module:" + symbol.name
            if symbol.kind == "constant":
                return self.reference(analyzer, symbol.node.value, aliases, seen)
            if symbol.kind == "import":
                module, name = symbol.name.split(":", 1)
                if module == "pyalamode.integrations" and analyzer._foundation_available(module):
                    return "foundation:integrations:" + name if name in INTEGRATION_NAMES else "module:" + module
                if module == "pyalamode.effects" and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + name if name in EFFECT_PRIMITIVES else "module:pyalamode.effects"
                if module in {"pyalamode.standard", "pyalamode.standard_contracts"} and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + name if name in STANDARD_NAMES else "module:" + module
                if module in {"pyalamode.variants", "pyalamode.failures"} and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + name if name in DOMAIN_PRIMITIVES else "module:" + module
                if module in {"pyalamode.records", "pyalamode.boundaries", "pyalamode.effects"} and analyzer._foundation_available(module):
                    return "module:" + module
                if module == "pyalamode.collections" and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + (name if name in COLLECTIONS else "*")
                target = self.modules.get(module)
                return self.reference(target, ast.Name(id=name), None, seen) if target else "foundation:" + module + ":" + name if module in {"pyalamode", "typing", "collections.abc", "types", "builtins", *RECORD_FOUNDATIONS, *EFFECT_FOUNDATIONS, *STANDARD_NATIVE, *INTEGRATION_FOUNDATIONS} else None
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr in {"get", "__getitem__"}:
                namespace = self.reference(analyzer, node.func.value, aliases, seen)
                if namespace and namespace.startswith("module:"):
                    return namespace
            producer = self.reference(analyzer, node.func, aliases, seen)
            if producer in {"foundation:pyalamode:compose", "foundation:pyalamode:partial_first"}:
                return "module:pyalamode.standard"
        if isinstance(node, ast.Subscript):
            reference = self.reference(analyzer, node.value, aliases, seen)
            if reference and reference.startswith("module:"):
                return reference
            if reference and reference.startswith("foundation:") and (reference.split(":", 2)[1] in {"integrations", "binascii", "_sha2", "_imp", "sys", "importlib", "importlib.util", "importlib.machinery"} or reference.split(":", 2)[1] == "builtins" and reference.rsplit(":", 1)[-1] in INTEGRATION_FOUNDATIONS["builtins"]):
                return reference
            if reference and reference.startswith("foundation:pyalamode:") and reference.rsplit(":", 1)[-1] in COLLECTIONS:
                return reference
        if isinstance(node, ast.Attribute):
            owner = self.reference(analyzer, node.value, aliases, seen)
            if owner and owner.startswith("foundation:integrations:"):
                return "module:pyalamode.integrations" if node.attr == "__globals__" else owner
            if owner and owner.startswith("foundation:") and (owner.split(":", 2)[1] in {"binascii", "_sha2", "_imp", "sys", "importlib", "importlib.util", "importlib.machinery"} or owner.split(":", 2)[1] == "builtins" and owner.rsplit(":", 1)[-1] in INTEGRATION_FOUNDATIONS["builtins"]):
                return owner
            if node.attr == "__dict__" and owner in self.functions:
                return owner
            if node.attr == "__globals__":
                # A function's globals belong to its defining module and are
                # shared by other helpers. Alias/dict writes taint that complete
                # module, rather than only the spelling used to obtain the dict.
                if owner in self.functions:
                    return "module:" + _module_name(self.functions[owner].analyzer.path, self.root)
                if owner and owner.startswith("foundation:pyalamode:"):
                    name = owner.rsplit(":", 1)[-1]
                    module = ("standard" if name in STANDARD_NAMES else "collections" if name in COLLECTIONS else
                              "records" if name in RECORD_PRIMITIVES else "boundaries" if name in BOUNDARY_PRIMITIVES else
                              "effects" if name in EFFECT_PRIMITIVES else "failures" if name in {"failure_value", "Failure"} else
                              "variants" if name in DOMAIN_PRIMITIVES else None)
                    return "module:pyalamode" + ("." + module if module else "")
                if owner and owner.startswith("module:pyalamode"):
                    return owner
                if isinstance(node.value, ast.Call):
                    producer = self.reference(analyzer, node.value.func, aliases, seen)
                    if producer and (producer.startswith("foundation:pyalamode:") or producer in self.functions):
                        # Ordinary reflected factory output can expose a product
                        # wrapper's defining globals; uncertain output fails closed.
                        return "module:pyalamode"
            if owner in self.variants:
                case_info = self.variants[owner].cases.get(node.attr)
                return str(case_info.schema) if case_info else owner
            if owner in self.records or owner in self.cases:
                return owner
            if owner and owner.startswith("foundation:pyalamode:") and owner.rsplit(":", 1)[-1] in COLLECTIONS | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES | STANDARD_NAMES | {"*"}:
                return owner
            if owner and owner.startswith("module:"):
                module = owner.split(":", 1)[1]
                if module in {"pyalamode.integrations", "pyalamode.integration_contracts"}:
                    return "foundation:integrations:" + node.attr if module == "pyalamode.integrations" and node.attr in INTEGRATION_NAMES else "module:" + module
                if module == "pyalamode" and node.attr == "integrations" and analyzer._foundation_available("pyalamode.integrations"):
                    return "module:pyalamode.integrations"
                if module in {"pyalamode.standard", "pyalamode.standard_contracts"}:
                    return "foundation:pyalamode:" + node.attr if node.attr in STANDARD_NAMES else "module:" + module
                if module == "pyalamode" and node.attr in {"collections", "records", "boundaries", "variants", "failures", "standard", "standard_contracts"} and analyzer._foundation_available("pyalamode." + node.attr):
                    return "module:pyalamode." + node.attr
                if module in {"pyalamode.variants", "pyalamode.failures"} and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + node.attr if node.attr in DOMAIN_PRIMITIVES else "module:" + module
                if module in {"pyalamode.records", "pyalamode.boundaries", "pyalamode.effects"} and analyzer._foundation_available(module):
                    return "module:" + module
                if module == "pyalamode.collections" and analyzer._foundation_available(module):
                    return "foundation:pyalamode:" + (node.attr if node.attr in COLLECTIONS else "*")
                target = self.modules.get(module)
                if target and node.attr in target.symbols:
                    return self.reference(target, ast.Name(id=node.attr), None, seen)
                if module + "." + node.attr in self.modules:
                    return "module:" + module + "." + node.attr
                if module in {"pyalamode", "typing", "collections.abc", "types", "builtins", *RECORD_FOUNDATIONS, *EFFECT_FOUNDATIONS, *STANDARD_NATIVE, *INTEGRATION_FOUNDATIONS}:
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
                if module in {"pyalamode.variants", "pyalamode.failures", "pyalamode.effects", "pyalamode.standard"} and attribute in DOMAIN_PRIMITIVES | EFFECT_PRIMITIVES | STANDARD_NAMES:
                    relevant.add(("pyalamode", attribute))
            elif symbol.kind == "module":
                relevant.add((symbol.name, "*"))
                if symbol.name in {"pyalamode.variants", "pyalamode.failures", "pyalamode.standard", "pyalamode.standard_contracts"}:
                    relevant.add(("pyalamode", "*"))
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
        for identity in self.replaced_records:
            record_info = self.records[identity]
            if record_info.analyzer.path in {path} | set(dependencies):
                replacements.add(identity + ".<record behavior>")
        for module, attribute in self.replaced_foundations:
            if (module, attribute) in relevant or (module, "*") in relevant or attribute == "*" and any(m == module for m, _ in relevant):
                replacements.add(module + "." + attribute + ".<behavior>")
        if any(("pyalamode", name) in relevant for name in COLLECTIONS) or ("pyalamode", "*") in relevant:
            replacements.update(identity + ".<collection dependency>" for identity in self.collection_dependency_replacements)
        if any(("pyalamode", name) in relevant for name in RECORD_PRIMITIVES | BOUNDARY_PRIMITIVES) or ("pyalamode", "*") in relevant or self.policy.get("boundary_guards", "off") != "off" or any(symbol.kind == "record" for symbol in analyzer.symbols.values()):
            replacements.update(identity + ".<record/boundary dependency>" for identity in self.record_dependency_replacements)
        if any(("pyalamode", name) in relevant for name in EFFECT_PRIMITIVES) or ("pyalamode", "*") in relevant or ("pyalamode.effects", "*") in relevant:
            replacements.update(identity + ".<effect dependency>" for identity in self.effect_dependency_replacements)
        if any(("pyalamode", name) in relevant for name in STANDARD_NAMES) or ("pyalamode", "*") in relevant or any(module in {"pyalamode.standard", "pyalamode.standard_contracts"} for module, _ in relevant):
            replacements.update(identity + ".<standard dependency>" for identity in self.standard_dependency_replacements)
        if any(module == "pyalamode.integrations" for module, _ in relevant):
            replacements.update(identity + ".<integration dependency>" for identity in self.integration_dependency_replacements)
        for identity in self.replaced_variants:
            info = self.variants.get(identity) or self.cases.get(identity)
            if info.analyzer.path in {path} | set(dependencies):
                replacements.add(identity + ".<domain behavior>")
        if any(("pyalamode", name) in relevant for name in DOMAIN_PRIMITIVES) or ("pyalamode", "*") in relevant or any(symbol.kind == "variant" for symbol in analyzer.symbols.values()):
            replacements.update(identity + ".<domain dependency>" for identity in self.domain_dependency_replacements)
        return sorted(replacements)

    def integration_context(self, path, dependencies):
        """Conservative import closure; unrelated scalar files retain warm hits."""
        selected = set()
        for source in {path} | set(dependencies):
            analyzer = self.analyzers[source]
            for symbol in analyzer.symbols.values():
                if symbol.kind == "import" and symbol.name.startswith("pyalamode.integrations:"):
                    name = symbol.name.split(":", 1)[1]
                    if name in INTEGRATION_NAMES:
                        selected.add("pyalamode.integrations." + name)
                elif symbol.kind == "module" and symbol.name == "pyalamode.integrations":
                    selected.update(self.integration_snapshot["inputs"])
            if analyzer._integration_imported():
                selected.update(self.integration_snapshot["inputs"])
        return {name: self.integration_snapshot["inputs"][name] for name in sorted(selected)}

    def analyze(self, cached: dict[str, CheckResult] | None = None) -> dict[str, CheckResult]:
        for path, result in (cached or {}).items():
            analyzer = self.analyzers[path]
            analyzer.result = result
            analyzer.dependencies.update(result.dependencies)
            for info in analyzer.infos.values():
                info.contract = next((c for c in result.contracts if c.name == info.qualified), None)
                if info.contract:
                    info.calls = set(info.contract.invoked_targets)
                    info.callable_dependencies = set(info.contract.callable_dependencies)
                    info.callable_arguments = {n: set(targets) for n, targets in info.contract.callable_arguments.items()}
                    info.dependencies = {d for d in info.contract.dependencies if d in self.analyzers}
                    info.failures = set(info.contract.direct_failures)
                    info.direct_failures = set(info.contract.direct_failures)
                    info.failure_edges = list(info.contract.failure_edges)
                    info.patterns = list(info.contract.patterns)
                    info.handlers = list(info.contract.handlers)
                    info.required_effects = set(info.contract.required_effects)
                    info.effect_origins = {e: set(paths) for e, paths in info.contract.effect_origins.items()}
                    info.borrow_scopes = list(info.contract.borrow_scopes)
                    info.operations = set(info.contract.operations)
                    info.definition_failures = set(info.contract.definition_failures)
                    info.capture_uses = set(info.contract.captures)
                    for name, kind in info.contract.captures.items():
                        if kind in {"unknown", "<unknown>"}:
                            info.captures[name] = UNKNOWN
                            continue
                        if kind not in self.types:
                            self.types[kind] = _contract_type(kind)
                        value = analyzer.annotation_value(kind)
                        evidence = info.contract.callable_capture_evidence.get(name)
                        if evidence and value.callable:
                            value = value.with_callable(analyzer._restore_callable(evidence))
                        info.captures[name] = value
                    evidence = info.contract.return_callable_evidence
                    if evidence:
                        value = analyzer.annotation_value(info.returns)
                        if value.callable:
                            info.return_value = value.with_callable(analyzer._restore_callable(evidence))
                    for name, kind in info.contract.defaults.items():
                        if kind in {"unknown", "<unknown>"}:
                            info.defaults[name] = UNKNOWN
                            continue
                        if kind not in self.types:
                            self.types[kind] = _contract_type(kind)
                        value = analyzer.annotation_value(kind)
                        evidence = info.contract.callable_default_evidence.get(name)
                        info.defaults[name] = value.with_callable(analyzer._restore_callable(evidence)) if evidence else value
                    info.analyzed = True
        self._initialization_cycles()
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
                # Recursive application operations can raise at an invocation;
                # each call edge retains its own enclosing handler masks.
                for edge in info.failure_edges:
                    if recursive(info.identity, edge["target"], set()) and "RecursionError" not in edge["handled"]:
                        info.failures.add("RecursionError")
        changed = True
        while changed:
            changed = False
            for info in self.functions.values():
                for target in info.calls:
                    callee = self.functions[target]
                    before = (len(info.failures), len(info.dependencies), len(info.operations), len(info.required_effects), len(info.callable_dependencies))
                    masks = [set(edge["handled"]) for edge in info.failure_edges if edge["target"] == target]
                    for mask in masks or [set()]:
                        info.failures.update(callee.failures - mask)
                    info.dependencies.update(callee.dependencies)
                    info.operations.update(callee.operations)
                    info.callable_dependencies.update(callee.callable_dependencies)
                    info.required_effects.update(callee.declared_effects | callee.required_effects)
                    for effect in callee.declared_effects | callee.required_effects:
                        info.effect_origins.setdefault(effect, set()).add(info.qualified + " -> " + callee.qualified)
                    if before != (len(info.failures), len(info.dependencies), len(info.operations), len(info.required_effects), len(info.callable_dependencies)):
                        changed = True
        for info in self.functions.values():
            if info.contract:
                info.contract.failures = sorted(info.failures)
                info.contract.direct_failures = sorted(info.direct_failures)
                info.contract.failure_edges = list(info.failure_edges)
                info.contract.patterns = list(info.patterns)
                info.contract.handlers = list(info.handlers)
                info.contract.dependencies = sorted(info.dependencies | info.calls | info.callable_dependencies)
                info.contract.invoked_targets = sorted(info.calls)
                info.contract.callable_dependencies = sorted(info.callable_dependencies)
                info.contract.callable_arguments = {n: sorted(targets) for n, targets in info.callable_arguments.items()}
                info.contract.callable_operations = sorted({op for target in info.callable_dependencies for op in self.functions[target].operations})
                info.contract.operations = sorted(info.operations)
                info.contract.operation_contracts = [entry for op in sorted(info.operations) if (entry := self.operation_contract(op)) is not None]
                info.contract.external_assumptions = [self.external_assumption(self.integrations[op.split(".", 1)[1]]) for op in sorted(info.operations) if op.startswith("integrations.")]
                info.contract.required_effects = sorted(info.required_effects)
                info.contract.effect_origins = {effect: sorted(paths) for effect, paths in info.effect_origins.items()}
                missing = info.required_effects - info.declared_effects
                if missing and not any(d.rule == "PAL310" and d.boundary == info.qualified for d in info.analyzer.result.diagnostics):
                    info.analyzer.boundary = info.qualified
                    info.analyzer.emit("PAL310", info.node, "transitive invocation requires undeclared " + ", ".join(sorted(missing)), origin="finite effect graph")
                if info.declared_effects or any(kind in CAPABILITIES or "Effectful[" in kind for kind in [*info.parameters.values(), info.returns or ""]):
                    assumption = "pyalamode effects-v1: opaque exact interfaces, finite operations, logical lease lifetime, stock CPython/OS trusted providers; controlled providers retain interface effects"
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                schemas = [*info.parameters.values(), info.returns or "", *info.contract.captures.values()]
                if any(operation.split(".", 1)[0] in COLLECTIONS for operation in info.operations) or any(name + "[" in kind for name in COLLECTIONS for kind in schemas):
                    assumption = "pyalamode collections-v1: exact deep-data façade, CPython tuple-copy storage and canonical scalar ordering"
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                if info.patterns or info.handlers or any(operation.startswith(("Variant.", "Pattern.", "Failure.", "Result.", "Some.", "Nothing.", "Ok.", "Err.")) for operation in info.operations) or any("Variant[" in kind or "Case[" in kind or "Option[" in kind or "Result[" in kind or "pyalamode:Failure" in kind for kind in schemas):
                    assumption = "pyalamode domains-v1: exact closed cases, deep data validation, finite match dispatch and opaque characterized builtin failure conversion"
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                if any(operation.startswith("Record.") for operation in info.operations) or any("Record[" in kind for kind in schemas):
                    assumption = "pyalamode records-v1: exact fixed fields, deep schema validation and type-sensitive value equivalence"
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                if any(operation.startswith("standard.") for operation in info.operations):
                    assumption = STANDARD_VERSION + ": finite exact data, manual decimal/UTF8, explicit eager callback/wrapper evidence and separately characterized ordinary setup"
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                for external in info.contract.external_assumptions:
                    assumption = "external " + external["identity"] + " contract=" + external["contract_sha256"] + " dependency=" + str(external["dependency_sha256"]) + " approval=" + external["admission"]
                    if assumption not in info.contract.trust:
                        info.contract.trust.append(assumption)
                info.analyzer.dependencies.update(info.dependencies)
        # Callable values retain their target assumptions even when the receiving
        # function does not invoke them. This does not add invocation effects.
        changed = True
        while changed:
            changed = False
            for info in self.functions.values():
                if not info.contract:
                    continue
                trust = set(info.contract.trust)
                external = {entry["identity"]: entry for entry in info.contract.external_assumptions}
                for target in info.calls | info.callable_dependencies:
                    if self.functions[target].contract:
                        trust.update(self.functions[target].contract.trust)
                        external.update({entry["identity"]: entry for entry in self.functions[target].contract.external_assumptions})
                updated = sorted(trust)
                assumptions = [external[key] for key in sorted(external)]
                changed |= updated != info.contract.trust or assumptions != info.contract.external_assumptions
                info.contract.trust = updated
                info.contract.external_assumptions = json.loads(json.dumps(assumptions))
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
                    contract.behavior = "unverified behavior; no certified effect bound"
                for record in [*analyzer.result.records, *analyzer.result.variants]:
                    record["source_evidence"] = "unverified: dependency gate failed"
                    record["freshness"] = "no successful checked claim"
                    record["behavior"] = "unverified declaration; product construction behavior is conditional on a qualifying declaration"
                if analyzer.module_mode:
                    analyzer.result.initialization_evidence = "unverified: dependency gate failed"
        return {path: analyzer.result for path, analyzer in self.analyzers.items()}

    def operation_contract(self, operation):
        if operation.startswith("integrations."):
            return json.loads(json.dumps(self.integrations[operation.split(".", 1)[1]]))
        return operation_contract(operation)

    @staticmethod
    def external_assumption(row):
        fields = ("identity", "version", "effects", "failures", "initialization", "provenance", "approval", "contract_sha256", "dependency_sha256", "installed_identity", "admission")
        return {**json.loads(json.dumps({key: row[key] for key in fields})), "source_evidence": "opaque external implementation; explicitly trusted operation contract"}

    def _initialization_cycles(self):
        """Finite conservative availability gate for checked import cycles.

        Importing a module namespace can be safe for deferred function bodies.
        Reading a member while that cycle initializes is not established by a
        complete static signature graph. M4 refuses those eager cycle reads.
        """
        edges = {name: set() for name in self.modules}
        imports = {}
        for module, analyzer in self.modules.items():
            if analyzer.tree is None:
                continue
            for node in analyzer.tree.body:
                names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [_import_name(node, module, Path(analyzer.path).name == "__init__.py")] if isinstance(node, ast.ImportFrom) else []
                targets = {name for imported in names for count in range(1, len(imported.split(".")) + 1) if (name := ".".join(imported.split(".")[:count])) in self.modules}
                edges[module].update(targets)
                imports[id(node)] = targets
        def reaches(start, target, seen):
            if start == target:
                return True
            if start in seen:
                return False
            seen.add(start)
            return any(reaches(child, target, seen) for child in edges[start])
        for module, analyzer in self.modules.items():
            if not analyzer.module_mode or analyzer.tree is None:
                continue
            cycle = {target for target in edges[module] if reaches(target, module, set())}
            if not cycle:
                continue
            def reject(node, reason):
                if not any(d.rule == "PAL241" and d.line == node.lineno and d.reason == reason for d in analyzer.result.diagnostics):
                    analyzer.emit("PAL241", node, reason, origin="checked initialization cycle")
            postponed = any(isinstance(node, ast.ImportFrom) and node.module == "__future__" and any(alias.name == "annotations" for alias in node.names) for node in analyzer.tree.body)
            for node in analyzer.tree.body:
                if isinstance(node, ast.ImportFrom) and imports.get(id(node), set()) & cycle:
                    reject(node, "cyclic from-import initialization cannot establish member availability; use module imports and deferred function references")
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    continue
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    expressions = [*node.decorator_list, *node.args.defaults, *[default for default in node.args.kw_defaults if default is not None]]
                    if not postponed:
                        expressions += [arg.annotation for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs if arg.annotation and not isinstance(arg.annotation, ast.Constant)]
                        if node.returns is not None and not isinstance(node.returns, ast.Constant):
                            expressions.append(node.returns)
                else:
                    expressions = [node]
                for expression in expressions:
                    for access in ast.walk(expression):
                        if not isinstance(access, ast.Attribute):
                            continue
                        owner = self.reference(analyzer, access.value)
                        if owner and owner.startswith("module:") and owner[len("module:"):] in cycle:
                            reject(access, "eager namespace access in an initialization cycle has no established member availability")


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
        self.handled_failures: set[str] = set()
        self.exception_tokens: set[str] = set()
        self.cleanup_names: set[str] = set()

    def prepare(self):
        tree = self._prepare()
        if isinstance(tree, CheckResult):
            return
        self.tree = tree
        self.parents = {id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        doc = tree.body[0] if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and type(tree.body[0].value.value) is str else None
        first = tree.body[1] if doc and len(tree.body) > 1 else (tree.body[0] if not doc and tree.body else None)
        directives = [t for t in tokenize.generate_tokens(io.StringIO(self.source, newline=None).readline)
                      if t.type == tokenize.COMMENT and t.string.strip() == "# mode: fun"]
        for token in tokenize.generate_tokens(io.StringIO(self.source, newline=None).readline):
            if token.type == tokenize.COMMENT and token.string.strip().startswith("# mode:") and token.string.strip() != "# mode: fun":
                self.result.diagnostics.append(diagnostic("PAL121", self.path, "the only supported directive is the module header # mode: fun; region toggles are unsupported", line=token.start[0]))
        valid = False
        for token in directives:
            if token.start[1] != 0 or (doc and token.start[0] <= doc.end_lineno) or (first and token.start[0] >= first.lineno) or valid:
                self.result.diagnostics.append(diagnostic("PAL121", self.path, "module directive must occur once in the module header after any docstring", line=token.start[0], column=token.start[1] + 1, column_encoding="unicode-codepoints"))
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
        self.module_mode = valid or required or self.path in self.graph.candidate_modules
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
        for node in tree.body:
            importing = (isinstance(node, ast.Import) and any(alias.name == "pyalamode.integrations" for alias in node.names)
                or isinstance(node, ast.ImportFrom) and (node.module == "pyalamode.integrations" or node.module == "pyalamode" and any(alias.name == "integrations" for alias in node.names)))
            if importing:
                self.result.setup_observations.append({"identity": "pyalamode.integrations import", "version": INTEGRATION_VERSION,
                    "line": node.lineno, "phase": "ordinary external import setup", "effects": ["IO"], "failures": ["ImportError", "OSError"],
                    "backends": ["binascii", "_sha2"], "evidence": "native-loader setup is separate from approved adapter invocation; surrounding ordinary initialization/body unchecked",
                    "policy": "not admitted in functional module initialization"})

    def discover(self):
        if self.tree is None:
            return
        def visit(body, parent=None, prefix="", strict=False):
            for node in body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.result.eligible_functions += 1
                    qualified = prefix + node.name
                    selected = (strict or self.path + "::" + qualified in self.graph.candidate_functions
                                or any(self._marker_like(d) or self._effects_like(d) for d in node.decorator_list))
                    for declaration in node.decorator_list:
                        if isinstance(declaration, ast.Call) and self.graph.reference(self, declaration.func) == "foundation:pyalamode:unsafe":
                            values = {keyword.arg: keyword.value.value for keyword in declaration.keywords if isinstance(keyword.value, ast.Constant) and type(keyword.value.value) is str}
                            valid = (not declaration.args and len(declaration.keywords) == 2 and values.keys() == {"scope", "rationale"} and all(value.strip() for value in values.values()))
                            if not valid or selected:
                                self.boundary = qualified
                                self.emit("PAL351", declaration, "unsafe is an ordinary adapter declaration requiring exact nonempty scope/rationale; it cannot select or decorate participating source")
                                self.boundary = "<module>"
                            self.result.unsafe_adapters.append({"name": qualified, "path": self.path, "line": node.lineno,
                                "scope": values.get("scope"), "rationale": values.get("rationale"), "valid_declaration": valid and not selected,
                                "source_evidence": "unchecked ordinary unsafe adapter", "behavior": "unknown; no certified effect bound",
                                "output_boundary": "explicit exclusive snapshot/schema validation may start a new checked computation; preceding execution remains unchecked"})
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
                    for case in getattr(node, "cases", []):
                        visit(case.body, parent, prefix, strict)
        visit(self.tree.body, strict=self.module_mode)

    def _integration_imported(self):
        return self.tree is not None and any(isinstance(node, ast.Import) and any(alias.name == "pyalamode.integrations" for alias in node.names)
            or isinstance(node, ast.ImportFrom) and node.module == "pyalamode" and any(alias.name == "integrations" for alias in node.names) for node in self.tree.body)

    def _effects_like(self, node):
        if not isinstance(node, ast.Call):
            return self.graph.reference(self, node) == "foundation:pyalamode:effects"
        if isinstance(node.func, ast.Attribute):
            return node.func.attr == "effects"
        if isinstance(node.func, ast.Name):
            return node.func.id == "effects" or self.graph.reference(self, node.func) == "foundation:pyalamode:effects"
        return False

    def _effect_identity(self, node, names=()):
        identity = self._type_identity(node, set(names))
        return identity if identity in EFFECT_FAMILIES else None

    def declare_effects(self, info):
        previous = self.active, self.boundary, self.definition_mode, self.constant_limit, self.locals
        self.active, self.boundary = info, info.qualified
        self.definition_mode = True
        self.constant_limit = info.node.lineno if info.parent is None else None
        names = set()
        parent = info.parent
        while parent:
            names.update(parent.parameters)
            names.update(a.arg for a in parent.node.args.posonlyargs + parent.node.args.args + parent.node.args.kwonlyargs)
            names.update(_written_names(parent.node.body))
            parent = parent.parent
        self.locals = names
        declarations = [d for d in info.node.decorator_list if self._effects_like(d)]
        if len(declarations) > 1:
            self.emit("PAL120", info.node, "only one finite @effects declaration is supported")
        for declaration in declarations:
            if not isinstance(declaration, ast.Call):
                self.emit("PAL120", declaration, "effects is a finite declaration factory; use @effects(Clock,...) with supported tokens")
                continue
            bound = [self._effect_identity(arg, names) for arg in declaration.args]
            if not self._primitive_identity(declaration.func, {"effects"}) or declaration.keywords or not bound or any(e is None for e in bound) or len(set(bound)) != len(bound):
                self.emit("PAL120", declaration, "@effects requires one or more unique unchanged product IO/State/Clock/Random/Environment tokens; Task and dynamic declarations are unsupported")
            else:
                info.declared_effects.update(bound)
        selection = _module_name(self.path, self.graph.root) + ":" + info.qualified
        policy_bound = self.policy.get("effect_bounds", {}).get(selection)
        if policy_bound is not None and not info.declared_effects.issubset(policy_bound):
            self.emit("PAL310", info.node, "source effect declaration exceeds project entry bound: " + ", ".join(sorted(info.declared_effects - set(policy_bound))), origin="project effect policy")
        self.active, self.boundary, self.definition_mode, self.constant_limit, self.locals = previous

    @staticmethod
    def _callable_failures(effects):
        failures = set(CALLABLE_FAILURES)
        for kind, family in CAPABILITIES.items():
            if family in effects:
                for _, _, bound in CAPABILITY_OPERATIONS[kind].values():
                    failures.update(bound)
        return failures

    def _require_effects(self, effects, node, origin):
        if not self.active:
            return
        for effect in effects:
            self.active.required_effects.add(effect)
            self.active.effect_origins.setdefault(effect, set()).add(self.active.qualified + " -> " + origin)
        missing = set(effects) - self.active.declared_effects
        if missing:
            self.emit("PAL310", node, "boundary requires undeclared " + ", ".join(sorted(missing)), origin=self.active.qualified + " -> " + origin)

    def _capability_call(self, node, env, quiet):
        if not isinstance(node.func, ast.Attribute):
            return None
        owner = self._expr(node.func.value, env, quiet=True)
        if owner.kind not in CAPABILITIES:
            return None
        operation = CAPABILITY_OPERATIONS[owner.kind].get(node.func.attr)
        def reject(rule, reason):
            if not quiet:
                self.emit(rule, node, reason)
            return UNKNOWN
        if self.definition_mode or self.initializing or not self.active:
            return reject("PAL230", "capability invocation belongs to a checked effectful function body")
        if self._module_changed("pyalamode", owner.kind) or not self._foundation_available("pyalamode.effects"):
            return reject("PAL240", "capability interface or trusted implementation dependencies have an analyzed replacement")
        if operation is None:
            return reject("PAL230", "capability operation is outside its finite allowed operation set")
        parameters, returned, failures = operation
        values = [self._expr(arg, env, quiet=quiet) for arg in node.args]
        if node.keywords or len(values) != len(parameters) or any(isinstance(a, ast.Starred) for a in node.args) or any(not self.matches(v, t) for v, t in zip(values, parameters)):
            return reject("PAL221", owner.kind + "." + node.func.attr + " requires its exact fixed positional signature")
        if not quiet:
            identity = owner.kind + "." + node.func.attr
            self._collection_operation(identity, node, failures=failures)
            self._require_effects((CAPABILITIES[owner.kind],), node, identity)
        return self.annotation_value(returned)

    def _ordinary_capability_writes(self, statement, env):
        expressions = [statement.value] if isinstance(statement, (ast.Expr, ast.Assign, ast.AnnAssign)) and statement.value is not None else []
        if isinstance(statement, (ast.If, ast.With, ast.For, ast.While, ast.Try, ast.Match)):
            expressions = [statement]
        for expression in expressions:
            for call in ast.walk(expression):
                if not isinstance(call, ast.Call):
                    continue
                names = [call.func.value.id] if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) else []
                target = self._expr(call.func, env, quiet=True)
                checked = target.callable and all(identity in self.graph.functions for identity in target.callable.targets) and bool(target.callable.targets)
                primitive = target.kind and target.kind.startswith(("primitive:", "builtin:"))
                if not checked and not primitive:
                    names += list(env)
                    names += [arg.id for arg in call.args if isinstance(arg, ast.Name)]
                    names += [keyword.value.id for keyword in call.keywords if isinstance(keyword.value, ast.Name)]
                for name in names:
                    binding = env.get(name)
                    if binding and binding.value.capability:
                        cap = binding.value.capability
                        # Even known shell methods may affect lifetime through
                        # unchecked surrounding behavior; subsequent lending needs
                        # a new provider or supported borrow. No dynamic evaluation.
                        value = Value(binding.value.types, capability=CapabilityValue(cap.interface, cap.operations, "unestablished after shell operation", cap.provider))
                        for alias, candidate in list(env.items()):
                            if candidate.value.capability and candidate.value.capability.provider == cap.provider:
                                env[alias] = Binding(Value(candidate.value.types, capability=CapabilityValue(cap.interface, cap.operations, "unestablished after shell operation", cap.provider)), candidate.first, candidate.definite)

    def _ordinary_borrow_env(self, node, env):
        item = node.items[0]
        call = item.context_expr
        if not isinstance(call, ast.Call) or len(call.args) != 1 or call.keywords or not isinstance(call.args[0], ast.Name) or not isinstance(item.optional_vars, ast.Name):
            return None
        target = self._expr(call.func, env, quiet=True)
        binding = env.get(call.args[0].id)
        if target.kind != "primitive:borrow" or not binding or not self.matches(binding.value, binding.value.kind):
            return None
        cap = binding.value.capability
        if cap is None:
            return None
        borrowed = dict(env)
        borrowed[item.optional_vars.id] = Binding(Value(binding.value.types, capability=CapabilityValue(cap.interface, cap.operations, "borrowed", cap.provider)), (node.lineno,))
        return borrowed

    def _provider_call(self, node, env, quiet):
        target = self._expr(node.func, env, quiet=True)
        name = target.kind[len("primitive:"):] if target.kind and target.kind.startswith("primitive:") else None
        if name not in PROVIDER_FACTORIES:
            return None
        if self.active or self.definition_mode or self.initializing:
            if not quiet:
                self.emit("PAL230", node, "provider construction is ordinary unchecked setup, distinct from checked capability invocation")
            return UNKNOWN
        if any(isinstance(a, ast.Starred) for a in node.args):
            return UNKNOWN
        operations = tuple(sorted(CAPABILITY_OPERATIONS[PROVIDER_FACTORIES[name]]))
        if name in {"live_io", "recorded_io"}:
            if len(node.keywords) != 1 or node.keywords[0].arg != "allowed_ops":
                return UNKNOWN
            permitted = self._expr(node.keywords[0].value, env, quiet=True)
            if permitted.items is None or not permitted.items or any(v.kind != "str" or v.literal not in operations for v in permitted.items):
                return UNKNOWN
            operations = tuple(v.literal for v in permitted.items)
            if len(set(operations)) != len(operations):
                return UNKNOWN
        elif node.keywords:
            return UNKNOWN
        values = [self._expr(arg, env, quiet=True) for arg in node.args]
        parameters = {"live_io": ("str",), "recorded_io": ("tuple[tuple[str, str], ...]",), "state": ("int",), "live_clock": (), "recorded_clock": ("tuple[int, ...]",), "live_random": (), "recorded_random": ("tuple[int, ...]",), "live_environment": (), "recorded_environment": ("tuple[tuple[str, str], ...]",)}[name]
        for expected in parameters:
            if expected not in self.graph.types:
                self.graph.types[expected] = _contract_type(expected)
        if len(values) != len(parameters) or any(not self.matches(v, t) for v, t in zip(values, parameters)):
            return UNKNOWN
        # Only the finite full-interface factory signature establishes live,
        # full-operation evidence. Setup behavior and external state are unchecked.
        kind = PROVIDER_FACTORIES[name]
        self.graph.types[kind] = TypeSpec(kind)
        parent = self.parents.get(id(node))
        phase = "ordinary module initialization"
        while parent is not None and not isinstance(parent, ast.Module):
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                phase = "ordinary function setup; not performed by import alone"
                break
            parent = self.parents.get(id(parent))
        observation = {**setup_contract(name), "path": self.path, "line": node.lineno, "column": node.col_offset + 1,
                       "phase": phase, "inputs": [value.kind for value in values], "input_evidence": "exact established source expressions; surrounding shell remains unchecked",
                       "output": kind, "allowed_operations": list(operations)}
        if observation not in self.result.setup_observations:
            self.result.setup_observations.append(observation)
        return Value(frozenset({kind}), capability=CapabilityValue(kind, tuple(sorted(operations)), "live", name + "@" + self.path + ":" + str(node.lineno) + ":" + str(node.col_offset)))

    def _primitive_identity(self, node, admitted):
        reference = self.graph.reference(self, node)
        if not reference or not reference.startswith("foundation:pyalamode:"):
            return None
        name = reference.rsplit(":", 1)[-1]
        if self.definition_mode and self.constant_limit is not None:
            value = self._expr(node, {}, quiet=True)
            if value.kind != "primitive:" + name:
                return None
        return name if name in admitted and self._foundation_available("pyalamode") and not self._module_changed("pyalamode", name) else None

    def discover_records(self):
        if self.tree is None:
            return
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef) and any(self._primitive_identity(d, {"record"}) for d in node.decorator_list):
                info = RecordInfo(node, self, _module_name(self.path, self.graph.root))
                self.graph.record_declarations.append(info)
                if info.identity not in self.graph.records or self.graph.modules.get(info.module) is self:
                    self.graph.records[info.identity] = info
                self.graph.types[info.identity] = info.schema
                self.symbols[node.name] = Symbol("record", info.identity, node)

    def discover_variants(self):
        if self.tree is None:
            return
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef) and any(self._primitive_identity(d.func if isinstance(d, ast.Call) else d, {"case"}) for d in node.decorator_list):
                self.emit("PAL120", node, "@case declarations are supported only inside a closed @oneof domain")
            if isinstance(node, ast.ClassDef) and any(self._primitive_identity(d.func if isinstance(d, ast.Call) else d, DOMAIN_DECORATORS) for d in node.decorator_list):
                info = VariantInfo(node, self, _module_name(self.path, self.graph.root))
                self.graph.variant_declarations.append(info)
                if info.identity not in self.graph.variants or self.graph.modules.get(info.module) is self:
                    self.graph.variants[info.identity] = info
                self.graph.types[info.identity] = TypeSpec("variant:" + info.module + ":" + node.name)
                self.symbols[node.name] = Symbol("variant", info.identity, node)
                for member in node.body:
                    if isinstance(member, ast.ClassDef):
                        case_info = CaseInfo(member, self, info.module, domain=node.name)
                        info.cases[member.name] = case_info
                        self.graph.cases[case_info.identity] = case_info
                        self.graph.types[case_info.identity] = case_info.schema

    def prepare_variant(self, info):
        if info.ready:
            return
        if info.preparing:
            info.valid = False
            self.emit("PAL120", info.node, "recursive domain declarations have no finite construction contract")
            return
        info.preparing = True
        previous = self.active, self.boundary, self.locals, self.definition_mode, self.constant_limit, self.failures
        self.active, self.boundary, self.locals = None, info.node.name, set()
        self.definition_mode, self.constant_limit, self.failures = True, info.node.lineno, set()
        before = len(self.result.diagnostics)
        node = info.node
        if self.graph.variants.get(info.identity) is not info:
            self.emit("PAL241", node, "closed domain declaration conflicts with the canonical package/module schema; shadowed nominal declarations are unverified", origin="nominal import resolution")
        if node.bases or node.keywords or getattr(node, "type_params", []) or len(node.decorator_list) != 1 or not self._primitive_identity(node.decorator_list[0], DOMAIN_DECORATORS):
            self.emit("PAL120", node, "domains require only @oneof, nested fixed @case declarations and no bases/metaclass/generic behavior")
        if not self._symbol_stable(node.name, self.symbols[node.name]) or info.identity in self.graph.replaced_variants:
            self.emit("PAL240", node, "domain namespace or case behavior has an analyzed replacement")
        names = set()
        for member in node.body:
            if isinstance(member, ast.Expr) and isinstance(member.value, ast.Constant) and type(member.value.value) is str:
                continue
            if not isinstance(member, ast.ClassDef) or member.name.startswith("_"):
                self.emit("PAL120", member, "a closed domain contains only public nested @case declarations")
                continue
            if member.name in names:
                self.emit("PAL101", member, "domain case name has another declaration")
            for decorator in member.decorator_list:
                root = decorator.func if isinstance(decorator, ast.Call) else decorator
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in names:
                    self.emit("PAL120", decorator, "nested case decorator is shadowed by an earlier outer class binding")
            names.add(member.name)
            case_info = info.cases[member.name]
            self.failures = case_info.failures
            if member.bases or member.keywords or getattr(member, "type_params", []) or len(member.decorator_list) != 1 or not self._primitive_identity(member.decorator_list[0], {"case"}):
                self.emit("PAL120", member, "cases require only @case, fixed typed data fields, no class behavior")
            if case_info.identity in self.graph.replaced_variants:
                self.emit("PAL240", member, "case behavior has an analyzed replacement")
            default_seen = False
            class_defaults = {}
            postponed = any(isinstance(item, ast.ImportFrom) and item.module == "__future__" and any(alias.name == "annotations" for alias in item.names) for item in self.tree.body)
            self.locals = set()
            for field_node in member.body:
                if isinstance(field_node, ast.Pass) or isinstance(field_node, ast.Expr) and isinstance(field_node.value, ast.Constant) and type(field_node.value.value) is str:
                    continue
                if not isinstance(field_node, ast.AnnAssign) or not isinstance(field_node.target, ast.Name) or field_node.target.id.startswith("_"):
                    self.emit("PAL120", field_node, "case payloads require public typed data fields and stable trailing defaults")
                    continue
                name = field_node.target.id
                if name in case_info.fields:
                    self.emit("PAL101", field_node, "case field has another declaration")
                    continue
                value = None
                if field_node.value is not None:
                    self.locals = set(class_defaults)
                    value = self._expr(field_node.value, class_defaults)
                    class_defaults[name] = Binding(value, (field_node.lineno,))
                annotation_names = () if postponed or isinstance(field_node.annotation, ast.Constant) and type(field_node.annotation.value) is str else class_defaults
                expected = self._annotation(field_node.annotation, extra_names=annotation_names)
                if not self._data_schema(self.graph.types.get(expected)):
                    self.emit("PAL130", field_node, "case fields require previously available recursively admitted data")
                    expected = None
                case_info.fields[name] = expected or "<unknown>"
                if field_node.value is not None:
                    default_seen = True
                    if not expected or not self.matches(value, expected):
                        self.emit("PAL221", field_node, "case default does not establish its exact field schema")
                    case_info.defaults[name] = value
                elif default_seen:
                    self.emit("PAL120", field_node, "required case fields precede defaults")
            case_info.ready = True
        if not names:
            self.emit("PAL120", node, "a closed domain must declare at least one case")
        info.valid = len(self.result.diagnostics) == before
        for case_info in info.cases.values():
            case_info.valid = info.valid
        info.ready, info.preparing = True, False
        self.active, self.boundary, self.locals, self.definition_mode, self.constant_limit, self.failures = previous

    def prepare_record(self, info):
        if info.ready:
            return
        if info.preparing:
            info.valid = False
            self.emit("PAL120", info.node, "recursive record declarations have no finite M4 construction contract")
            return
        info.preparing = True
        node = info.node
        previous = self.active, self.boundary, self.locals, self.definition_mode, self.constant_limit, self.failures
        self.active, self.boundary, self.locals = None, node.name, set()
        self.definition_mode, self.constant_limit, self.failures = True, node.lineno, info.failures
        before = len(self.result.diagnostics)
        if self.graph.records.get(info.identity) is not info:
            self.emit("PAL241", node, "record declaration conflicts with the canonical package/module schema; shadowed nominal declarations are unverified", origin="nominal import resolution")
        if node.bases or node.keywords or getattr(node, "type_params", []) or len(node.decorator_list) != 1 or not self._primitive_identity(node.decorator_list[0], {"record"}):
            self.emit("PAL120", node, "record declarations require only @record, fixed fields, no bases, metaclass or generic parameters")
        if not self._symbol_stable(node.name, self.symbols[node.name]) or info.identity in self.graph.replaced_records:
            self.emit("PAL240", node, "record class or behavioral attributes have an analyzed replacement")
        default_seen = False
        class_defaults = {}
        postponed = any(isinstance(item, ast.ImportFrom) and item.module == "__future__" and any(alias.name == "annotations" for alias in item.names) for item in self.tree.body)
        for member in node.body:
            if isinstance(member, ast.Pass) or isinstance(member, ast.Expr) and isinstance(member.value, ast.Constant) and type(member.value.value) is str:
                continue
            if not isinstance(member, ast.AnnAssign) or not isinstance(member.target, ast.Name) or member.target.id.startswith("_"):
                self.emit("PAL120", member, "records admit only public typed fields with stable data defaults; methods, descriptors and class behavior are unsupported")
                continue
            name = member.target.id
            if name in info.fields:
                self.emit("PAL101", member, f"record field `{name}` is already declared")
                continue
            value = None
            if member.value is not None:
                self.locals = set(class_defaults)
                value = self._expr(member.value, class_defaults)
                class_defaults[name] = Binding(value, (member.lineno,))
            annotation_names = () if postponed or isinstance(member.annotation, ast.Constant) and type(member.annotation.value) is str else class_defaults
            expected = self._annotation(member.annotation, extra_names=annotation_names)
            if expected and not self._data_schema(self.graph.types.get(expected)):
                self.emit("PAL130", member, "record fields require recursively admitted data, excluding callables and capabilities")
                expected = None
            info.fields[name] = expected or "<unknown>"
            def prepare_nested(schema):
                if schema is None:
                    return
                if schema.name.startswith("record:"):
                    nested = self.graph.records.get(str(schema))
                    if nested:
                        nested.analyzer.prepare_record(nested)
                        if not nested.valid:
                            self.emit("PAL130", member, "record field depends on an invalid or recursive record declaration")
                for argument in schema.arguments:
                    prepare_nested(argument)
            prepare_nested(self.graph.types.get(expected))
            if member.value is not None:
                default_seen = True
                if not expected or not self.matches(value, expected):
                    self.emit("PAL221", member.value, f"record default `{name}` does not establish {expected}", origin="record definition-time default")
                info.defaults[name] = value
            elif default_seen:
                self.emit("PAL120", member, "required record fields must precede fields with defaults")
        info.valid = info.valid and len(self.result.diagnostics) == before
        info.ready, info.preparing = True, False
        self.active, self.boundary, self.locals, self.definition_mode, self.constant_limit, self.failures = previous

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
        if self.definition_mode and self.constant_limit is not None and symbol.node is not None and symbol.node.lineno >= self.constant_limit:
            return UNKNOWN
        if symbol.kind == "variant":
            info = self.graph.variants[symbol.name]
            if not info.valid or info.identity in self.graph.replaced_variants:
                return UNKNOWN
            self._depend(info.analyzer.path)
            return Value.exact("variant_class:" + info.identity)
        if symbol.kind == "record":
            info = self.graph.records[symbol.name]
            if not info.valid or info.identity in self.graph.replaced_records or self.constant_limit is not None and symbol.node.lineno >= self.constant_limit:
                return UNKNOWN
            self._depend(info.analyzer.path)
            return Value.exact("record_class:" + info.identity)
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
            if module == "pyalamode.integrations" and name in INTEGRATION_NAMES and self._foundation_available(module) and not self._module_changed(module, name):
                return Value.exact("integration:" + name)
            if module == "pyalamode" and name == "integrations" and self._foundation_available("pyalamode.integrations") and not self._module_changed(module, name):
                return Value.exact("module:pyalamode.integrations")
            if module == "pyalamode" and name in COLLECTIONS and self._foundation_available(module) and not self._module_changed(module, name):
                return Value.exact("collection_class:" + name)
            if module in {"pyalamode", "pyalamode.effects", "pyalamode.variants", "pyalamode.failures", "pyalamode.standard"} and name in RECORD_PRIMITIVES | BOUNDARY_PRIMITIVES | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES | STANDARD_NAMES and self._foundation_available(module) and not self._module_changed(module, name) and not self._module_changed("pyalamode", name):
                return Value.exact("primitive:" + name)
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
            if symbol.name == "pyalamode.effects":
                return Value.exact("primitive:effects") if self._foundation_available(symbol.name) and not self._module_changed("pyalamode", "effects") else UNKNOWN
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
                elif expected and self.graph.types.get(expected, TypeSpec("")).name in DOMAIN_TYPES:
                    value = self.annotation_value(expected)
            if value.kind in CAPABILITIES:
                if not quiet:
                    self.emit("PAL320", symbol.node, "capabilities cannot be stable global constants")
                value = UNKNOWN
            if value.types:
                self.constants[name] = value
            return value
        finally:
            self.constant_limit, self.locals, self.boundary, self.definition_mode, self.failures = previous
            self.constant_busy.remove(name)

    def _type_identity(self, node: ast.expr, env_names: set[str]) -> str | None:
        root = node
        while isinstance(root, ast.Attribute):
            root = root.value
        if isinstance(root, ast.Name) and root.id not in env_names:
            symbol = self.symbols.get(root.id)
            if symbol and self._symbol_stable(root.id, symbol) and self._annotation_available(symbol):
                reference = self.graph.reference(self, node)
                variant_info = self.graph.variants.get(reference)
                case_info = self.graph.cases.get(reference)
                if variant_info and variant_info.valid and reference not in self.graph.replaced_variants:
                    return "variant:" + variant_info.module + ":" + variant_info.node.name
                if case_info and case_info.valid and reference not in self.graph.replaced_variants:
                    return case_info.schema.name
                record_info = self.graph.records.get(reference)
                if record_info and record_info.valid and reference not in self.graph.replaced_records and not self._module_changed(record_info.module, record_info.node.name):
                    return record_info.schema.name
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
                if module in {"pyalamode", "pyalamode.effects", "pyalamode.variants", "pyalamode.failures"} and name in COLLECTIONS | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES:
                    return name if not self._module_changed("pyalamode", name) else None
        if isinstance(node, ast.Attribute):
            symbol = self.symbols.get(node.value.id) if isinstance(node.value, ast.Name) and node.value.id not in env_names else None
            if symbol and not self._annotation_available(symbol):
                return None
            if symbol and self._symbol_stable(node.value.id, symbol) and symbol.kind == "module" and not self._module_changed(symbol.name, node.attr):
                if not self._foundation_available(symbol.name):
                    return None
                if symbol.name in {"typing", "collections.abc"} and node.attr == "Callable":
                    return "Callable"
                if symbol.name in {"pyalamode", "pyalamode.variants", "pyalamode.failures"} and node.attr in COLLECTIONS | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES:
                    return node.attr if not self._module_changed("pyalamode", node.attr) else None
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
        if self.definition_mode and self.constant_limit is not None:
            # Record schemas and defaults resolve only already available names.
            # M4 deliberately rejects forward/recursive record schemas, including
            # postponed text, instead of requiring runtime deferred resolution.
            return symbol.node is not None and symbol.node.lineno < self.constant_limit
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
        union_reason = []

        def parse(expression):
            if isinstance(expression, ast.Constant) and expression.value is None:
                return TypeSpec("None")
            if isinstance(expression, ast.BinOp) and isinstance(expression.op, ast.BitOr):
                members, pending = [], [expression]
                while pending:
                    item = pending.pop()
                    if isinstance(item, ast.BinOp) and isinstance(item.op, ast.BitOr):
                        pending += [item.right, item.left]
                    else:
                        members.append(parse(item))
                if any(member is None for member in members):
                    return None
                union, reason = self.union_schema(members)
                if reason:
                    union_reason.append(reason)
                return union
            identity = self._type_identity(expression, names) if expression is not None else None
            if identity in SCALARS | CAPABILITIES.keys():
                return TypeSpec(identity)
            if identity == "Failure":
                return TypeSpec("record:pyalamode:Failure")
            if identity and identity.startswith(("record:", "variant:", "case:")):
                return TypeSpec(identity)
            if isinstance(expression, ast.Subscript):
                identity = self._type_identity(expression.value, names)
                parts = expression.slice.elts if isinstance(expression.slice, ast.Tuple) else [expression.slice]
                if identity == "tuple":
                    if isinstance(expression.slice, ast.Tuple) and not expression.slice.elts:
                        return TypeSpec("tuple")
                    variadic = len(parts) == 2 and isinstance(parts[-1], ast.Constant) and parts[-1].value is Ellipsis
                    args = [parse(p) for p in (parts[:-1] if variadic else parts)]
                    if args and all(self._data_schema(a) for a in args):
                        return TypeSpec("tuple", tuple(args), variadic=variadic)
                if identity in {"Callable", "Effectful"} and len(parts) >= 2 and isinstance(parts[0], ast.List):
                    bound = tuple(self._effect_identity(p, names) for p in parts[2:])
                    if identity == "Callable" and len(parts) != 2 or identity == "Effectful" and (not bound or any(e not in EFFECT_FAMILIES for e in bound) or len(set(bound)) != len(bound)):
                        return None
                    args = [parse(p) for p in parts[0].elts]
                    result = parse(parts[1])
                    if all(a is not None and (a.name not in CAPABILITIES or CAPABILITIES[a.name] in bound) for a in args) and result is not None and result.name not in CAPABILITIES:
                        return TypeSpec("Callable", tuple(args), result, effect_bound=tuple(sorted(bound)))
                if identity in DOMAIN_TYPES:
                    args = [parse(p) for p in parts]
                    if len(args) == (1 if identity == "Option" else 2) and all(self._data_schema(a) for a in args):
                        return TypeSpec(identity, tuple(args))
                if identity in COLLECTIONS:
                    args = [parse(p) for p in parts]
                    arity = 2 if identity in {"Map", "OrderedMap"} else 1
                    if len(args) == arity and all(self._data_schema(a) for a in args):
                        if identity in {"Map", "OrderedMap", "Set"} and args[0].name not in SCALARS:
                            return None
                        return TypeSpec(identity, tuple(args))
            return None
        schema = parse(node)
        if schema is None and union_reason:
            self.emit("PAL130", original, union_reason[0])
            return None
        if schema is None:
            self.emit("PAL130", original or ast.Constant(value=None), "annotation must identify a closed exact scalar, recursive tuple/collection/record/domain/Option/Result, or fixed positional Callable contract; Map keys and Set elements use homogeneous exact scalars")
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
        if info.returns in CAPABILITIES:
            self.emit("PAL320", node.returns, "live capabilities cannot be returned as stable results")
        for name, kind in info.parameters.items():
            if kind in CAPABILITIES and CAPABILITIES[kind] not in info.declared_effects:
                self.emit("PAL310", node, f"capability parameter `{name}` requires declared {CAPABILITIES[kind]}", origin="capability invocation borrow")
        self.active, self.boundary = previous

    def annotation_value(self, kind):
        schema = self.graph.types.get(kind)
        if schema and schema.name == "Callable":
            return Value.exact(kind).with_callable(CallableValue(tuple(map(str, schema.arguments)), str(schema.result), conditional=True, effect_bound=schema.effect_bound))
        if kind in CAPABILITIES:
            return Value(frozenset({kind}), capability=CapabilityValue(kind, tuple(sorted(CAPABILITY_OPERATIONS[kind])), "invocation obligation", "exact interface supplied by caller"))
        return Value.exact(kind) if schema else UNKNOWN

    def union_classes(self, schema):
        """Exact runtime classes a closed-union member occupies, or None if ineligible."""
        if schema.name in SCALARS:
            return {schema.name}
        if schema.name.startswith(("record:", "case:")) and self._data_schema(schema):
            return {str(schema)}
        if schema.name.startswith("variant:") and self._data_schema(schema):
            return {case.identity for case in self.graph.variants[str(schema)].cases.values()}
        return None

    def union_schema(self, members):
        """Normalize closed-union members: flatten, deduplicate, refuse overlap, order canonically."""
        flat = {}
        for member in members:
            for child in (member.arguments if member.name == "union" else (member,)):
                flat[str(child)] = child
        occupied = set()
        for text, member in flat.items():
            classes = self.union_classes(member)
            if classes is None:
                return None, "closed union members are exact None, bool, int, str, bytes, records, domains or cases; `" + text + "` is not admitted"
            if classes & occupied:
                return None, "closed union members must not overlap by exact runtime class; `" + text + "` overlaps another member"
            occupied |= classes
        if {"bool", "int"} <= occupied:
            return None, "bool | int is refused because class patterns cannot separate bool from int"
        if len(flat) == 1:
            return next(iter(flat.values())), None
        return TypeSpec("union", tuple(flat[text] for text in sorted(flat))), None

    def union_tags(self, schema):
        """Exact coverage tags: scalar classes (bool as True/False), records and cases."""
        tags = set()
        for member in schema.arguments:
            classes = self.union_classes(member) or set()
            tags |= {"True", "False"} if classes == {"bool"} else classes
        return tags

    def union_fingerprint(self, schema):
        data = [(str(member), self.graph.variants[str(member)].fingerprint if member.name.startswith("variant:") else None)
                for member in schema.arguments]
        return hashlib.sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()

    def _data_schema(self, schema):
        if schema is not None and schema.name == "union":
            return len(schema.arguments) > 1 and all(self._data_schema(member) for member in schema.arguments)
        return schema is not None and (schema.name in SCALARS or (schema.name == "record:pyalamode:Failure" or schema.name.startswith("record:") and str(schema) in self.graph.records and self.graph.records[str(schema)].valid or schema.name.startswith("variant:") and str(schema) in self.graph.variants and self.graph.variants[str(schema)].valid or schema.name.startswith("case:") and str(schema) in self.graph.cases and self.graph.cases[str(schema)].valid) or schema.name == "Nothing" or schema.name in {"tuple", *COLLECTIONS, *DOMAIN_TYPES, *DOMAIN_CASES} and all(self._data_schema(a) for a in schema.arguments))

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
        if expected in CAPABILITIES:
            evidence = value.capability
            return value.types == frozenset({expected}) and evidence is not None and evidence.lifetime in {"live", "invocation obligation", "borrowed"} and set(CAPABILITY_OPERATIONS[expected]).issubset(evidence.operations)
        if schema.name == "union" or any(self.graph.types.get(kind) and self.graph.types[kind].name == "union" for kind in value.types):
            if value.callable or value.capability:
                return False
            return all(self._schema_matches(self.graph.types.get(kind), schema) for kind in value.types)
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
            if not set(callback.effect_bound).issubset(schema.effect_bound):
                return False
            for target in callback.targets:
                info = self.graph.functions[target]
                if any(k == "keyword_only" for k in info.kinds.values()):
                    return False
            return True
        if schema.name in DOMAIN_TYPES or schema.name.startswith("variant:"):
            return all(self._domain_matches(self.graph.types.get(kind), schema) for kind in value.types)
        if schema.name in COLLECTIONS:
            return all(self._schema_matches(self.graph.types.get(kind), schema) for kind in value.types)
        return value.types == frozenset({expected})

    def _domain_matches(self, actual, expected):
        if actual is None:
            return False
        if actual == expected:
            return True
        if expected.name.startswith("variant:"):
            info = self.graph.variants.get(str(expected))
            return bool(info and str(actual) in {case.identity for case in info.cases.values()})
        if expected.name == "Option":
            return actual.name == "Nothing" or actual.name == "Some" and self._schema_matches(actual.arguments[0], expected.arguments[0])
        if expected.name == "Result":
            index = 0 if actual.name == "Ok" else 1 if actual.name == "Err" else None
            return index is not None and self._schema_matches(actual.arguments[0], expected.arguments[index])
        return False

    def _schema_matches(self, actual, expected):
        if actual is not None and actual.name == "union":
            return all(self._schema_matches(member, expected) for member in actual.arguments)
        if expected.name == "union":
            if any(self._schema_matches(actual, member) for member in expected.arguments):
                return True
            # A domain value fits when each of its exact cases is itself a member.
            domain = self.graph.variants.get(str(actual)) if actual is not None and actual.name.startswith("variant:") else None
            return bool(domain) and all(any(self._schema_matches(case.schema, member) for member in expected.arguments) for case in domain.cases.values())
        if expected.name in DOMAIN_TYPES or expected.name.startswith("variant:"):
            return self._domain_matches(actual, expected)
        if actual is None or actual.name != expected.name:
            return False
        if expected.name in COLLECTIONS | DOMAIN_TYPES | DOMAIN_CASES:
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
                        self._add_failures(info.definition_failures)
                elif isinstance(node, ast.ClassDef) and self.symbols.get(node.name, Symbol("", "")).kind == "variant":
                    info = self.graph.variants[self.symbols[node.name].name]
                    if info.valid:
                        env[node.name] = Binding(Value.exact("variant_class:" + info.identity), (node.lineno,))
                        self._add_failures(category for case_info in info.cases.values() for category in case_info.failures)
                elif isinstance(node, ast.ClassDef) and self.symbols.get(node.name, Symbol("", "")).kind == "record":
                    info = self.graph.records[self.symbols[node.name].name]
                    if info.valid:
                        env[node.name] = Binding(Value.exact("record_class:" + info.identity), (node.lineno,))
                        self._add_failures(info.failures)
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
            if module == "pyalamode.integrations" or module == "pyalamode" and symbol.name == "pyalamode:integrations":
                self.emit("PAL241", node, "external adapter import has ordinary native-loader IO setup; pure exports do not establish pure import initialization")
                continue
            if module in {"pyalamode", "pyalamode.effects", "pyalamode.variants", "pyalamode.failures", "types", "builtins", "typing", "collections", "collections.abc", "__future__", "pyalamode.standard"} and self._foundation_available(module):
                if symbol.kind == "import":
                    allowed = {"pyalamode.effects": EFFECT_PRIMITIVES, "pyalamode.standard": STANDARD_NAMES, "pyalamode": {"fun", *COLLECTIONS, *RECORD_PRIMITIVES, *BOUNDARY_PRIMITIVES, *EFFECT_PRIMITIVES, *DOMAIN_PRIMITIVES, *STANDARD_NAMES}, "types": {"NoneType"}, "pyalamode.variants": DOMAIN_PRIMITIVES - {"failure_value", "Failure"}, "pyalamode.failures": {"failure_value", "Failure"}, "builtins": BUILTINS | HANDLER_CATEGORIES | {"int", "bool", "str", "bytes", "tuple"}, "typing": {"Callable"}, "collections.abc": {"Callable"}, "__future__": {"annotations"}}
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
        handler_context = self.handled_failures, self.exception_tokens, self.cleanup_names
        self.handled_failures, self.exception_tokens, self.cleanup_names = set(), set(), set()
        node = info.node
        if isinstance(node, ast.AsyncFunctionDef) or node.args.vararg or node.args.kwarg or getattr(node, "type_params", []):
            self.emit("PAL120", node, "async, variadic and generic functions have no supported contract")
        if info.parent is None and self.parents.get(id(node)) is self.tree:
            if self.global_writes.get(node.name) != [node]:
                self.emit("PAL240", node, f"participating binding `{node.name}` has another analyzed initialization")
        if info.identity in self.graph.replaced_functions:
            self.emit("PAL240", node, f"checked callable `{info.qualified}` has an analyzed attribute/behavior replacement")
        decorators = node.decorator_list
        ordinary = [d for d in decorators if not self._effects_like(d)]
        if ordinary and (len(ordinary) != 1 or not self._marker_valid(ordinary[0])):
            self.emit("PAL120", node, "only one unchanged @fun and one finite @effects declaration are supported")
        if not decorators and not (self.module_mode or info.parent or info.identity in self.graph.candidate_functions):
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
        env = {}
        for name, kind in info.parameters.items():
            value = self.annotation_value(kind)
            if value.callable:
                callback = value.callable
                value = value.with_callable(CallableValue(callback.parameters, callback.returns, conditional=True, effect_bound=callback.effect_bound, obligation=info.identity + ":" + name))
            env[name] = Binding(value, (node.lineno,))
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
            if info.parameters[name] in CAPABILITIES:
                self.emit("PAL320", value_node, "capabilities cannot have definition-time defaults")
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
        info.direct_failures = set(info.failures)
        contract = FunctionContract(info.qualified, self.path, node.lineno, dict(info.parameters), info.returns, dict(info.kinds),
                                    defaults={n: v.kind or "unknown" for n, v in info.defaults.items()},
                                    captures={n: info.captures[n].kind or "unknown" for n in info.capture_uses},
                                    callable_targets={n: list(info.captures[n].callable.targets) for n in info.capture_uses if info.captures[n].callable},
                                    callable_defaults={n: list(v.callable.targets) for n, v in info.defaults.items() if v.callable},
                                    callable_default_evidence={n: self._callable_evidence(v.callable) for n, v in info.defaults.items() if v.callable},
                                    return_callable_targets=list(info.return_value.callable.targets) if info.return_value and info.return_value.callable else [],
                                    callable_capture_evidence={n: self._callable_evidence(info.captures[n].callable) for n in info.capture_uses if info.captures[n].callable},
                                    return_callable_evidence=self._callable_evidence(info.return_value.callable) if info.return_value and info.return_value.callable else None,
                                    definition_failures=sorted(info.definition_failures), operations=sorted(info.operations),
                                    data_assertions=list(info.data_assertions),
                                    effect_bound=sorted(info.declared_effects), required_effects=sorted(info.required_effects),
                                    effect_origins={e: sorted(paths) for e, paths in info.effect_origins.items()},
                                    capability_parameters={n: {"interface": k, "effect": CAPABILITIES[k], "operations": sorted(CAPABILITY_OPERATIONS[k]), "lifetime": "invocation borrow; no retention or transfer", "permissions": "full interface operation set required; minimal callee permissions are not inferred"} for n, k in info.parameters.items() if k in CAPABILITIES},
                                    borrow_scopes=list(info.borrow_scopes), failure_edges=list(info.failure_edges),
                                    direct_failures=sorted(info.direct_failures), patterns=list(info.patterns), handlers=list(info.handlers))
        contract.behavior = "effects <= {" + ", ".join(sorted(info.declared_effects)) + "}" if info.declared_effects else "pure"
        contract.caller_obligations = [f"{name}: exact {kind}; recursively admitted contents and checked callable/capture evidence where applicable" for name, kind in info.parameters.items()]
        contract.caller_obligations.extend(["Resolved constant, callable, capture, marker, annotation and builtin bindings remain unchanged during execution.",
                                            "Callable inputs satisfy their finite invocation effect bound with stable captures; annotations alone do not establish actual evidence. Capability inputs have the exact supported interface, allowed operations and live invocation lifetime; no retention or transfer.",
                                            "Pure Callable invocation failure upper bound: IndexError, KeyError, ValueError, UnicodeError, ZeroDivisionError and RecursionError. Effectful conditional callbacks additionally propagate the finite operation failure bounds of their declared families; concrete target failures propagate separately.",
                                            "Ordinary callers receive no runtime guards; unchecked import initialization has no purity claim.",
                                            "Handler tokens are actual mutable Python exceptions: only direct finite failure_value conversion is admitted; exact approved builtin failure universe and unchanged operation dependencies are preconditions.",
                                            "Matching assumes exact characterized case tags and payload schemas; capture-free guards do not establish full case coverage unless literal True.",
                                            "Recursion may diverge or raise RecursionError; resource exhaustion and interruption are outside the failure contract."])
        info.contract = contract
        self.result.contracts.append(contract)
        if info.parent is None and self.parents.get(id(node)) is self.tree:
            self.contracts[node.name] = contract
        info.analyzed, info.analyzing = True, False
        self.active, self.boundary, self.locals, self.failures, self.return_type, self.in_dead = previous
        self.handled_failures, self.exception_tokens, self.cleanup_names = handler_context

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
                                     a.callable.conditional or b.callable.conditional,
                                     tuple(sorted(set(a.callable.effect_bound + b.callable.effect_bound))),
                                     wrapper="choice" if a.callable != b.callable else a.callable.wrapper,
                                     components=(a.callable, b.callable) if a.callable != b.callable else a.callable.components,
                                     obligation=a.callable.obligation if a.callable.obligation == b.callable.obligation else None,
                                     captured_callbacks=a.callable.captured_callbacks + b.callable.captured_callbacks)
        capability = a.capability if a.capability == b.capability else None
        types = a.types | b.types
        if callback:
            schema = TypeSpec("Callable", tuple(self.graph.types[k] for k in callback.parameters), self.graph.types[callback.returns], effect_bound=callback.effect_bound)
            self.graph.types[str(schema)] = schema
            types = frozenset({str(schema)})
        return Value(types, literal, a.items if a.items == b.items else None, callback, capability)

    def _collection_operation(self, identity, node, quiet=False, failures=()):
        if not quiet:
            self._record_call(node)
            self._add_failures(failures)
            if self.active:
                self.active.operations.add(identity)

    @staticmethod
    def _nested_validation_failures(schema):
        # Traversal depth follows the exact recursive data schema. This bound is
        # separate from recursive application call-graph failures.
        return ("RecursionError",) if schema is not None and schema.name not in SCALARS else ()

    def _collection_callback(self, callback, parameters, returns, node, env, quiet):
        if not quiet and callback.callable:
            self._require_effects(callback.callable.effect_bound, node, "ordered callback invocation")
        schema = TypeSpec("Callable", tuple(parameters), returns, effect_bound=tuple(sorted(self.active.declared_effects)) if self.active else ())
        self.graph.types[str(schema)] = schema
        if not self.matches(callback, str(schema)):
            if not quiet:
                self.emit("PAL221", node, f"collection callback requires resolved bounded {schema} with stable captures")
            return False
        if not quiet:
            self._ready_callable(callback, env, node)
            evidence = callback.callable
            self._add_failures(self._wrapper_validation_failures(evidence))
            for operation in self._wrapper_operations(evidence):
                self._collection_operation(operation, node)
            if evidence.conditional:
                self._add_failures(self._callable_failures(evidence.effect_bound))
            for identity in evidence.targets:
                info = self.graph.functions[identity]
                if self.active:
                    self._failure_edge(identity, node)
                    self.active.dependencies.update(info.dependencies)
                self._depend(info.analyzer.path)
        return True

    def _wrapper_value(self, name, parameters, returned, components, bound=()):
        effects = tuple(sorted({effect for part in components for effect in part.effect_bound}))
        callback = CallableValue(tuple(parameters), returned,
                                 tuple(sorted({target for part in components for target in part.targets})),
                                 tuple(sorted({capture for part in components for capture in part.captures})),
                                 any(part.conditional for part in components), effects, name, tuple(components), tuple(bound))
        schema = TypeSpec("Callable", tuple(self.graph.types[k] for k in parameters), self.graph.types[returned], effect_bound=effects)
        self.graph.types[str(schema)] = schema
        return Value.exact(str(schema)).with_callable(callback)

    def _standard_call(self, node, env, quiet):
        target = self._expr(node.func, env, quiet=True)
        name = target.kind[len("primitive:"):] if target.kind and target.kind.startswith("primitive:") else None
        if name not in STANDARD_NAMES:
            return None
        def reject(reason):
            if not quiet:
                self.emit("PAL221", node, reason)
            return UNKNOWN
        if node.keywords or any(isinstance(arg, ast.Starred) for arg in node.args):
            return reject("standard operations require exactly their published positional-only signature")
        values = [self._expr(arg, env, quiet=quiet) for arg in node.args]
        if name in SCALAR_SIGNATURES:
            parameters, returned, failures = SCALAR_SIGNATURES[name]
            if returned not in self.graph.types:
                self.graph.types[returned] = _contract_type(returned)
            for parameter in parameters:
                if parameter not in self.graph.types:
                    self.graph.types[parameter] = _contract_type(parameter)
            if len(values) != len(parameters) or any(not self.matches(value, expected) for value, expected in zip(values, parameters)):
                return reject(name + " requires exact " + str(parameters))
            self._collection_operation("standard." + name, node, quiet, failures)
            return self.annotation_value(returned)

        if self.definition_mode or self.initializing or not self.active:
            return reject("higher-order standard operations and wrapper construction are confined to checked function bodies")
        if name in {"compose", "partial_first"}:
            if len(values) != 2:
                return reject(name + " requires exactly two arguments")
            callbacks = [value.callable for value in values] if name == "compose" else [values[0].callable]
            if any(callback is None or not callback.targets and not callback.conditional for callback in callbacks):
                return reject(name + " requires actual resolved callable/capture evidence")
            for value in values if name == "compose" else values[:1]:
                callback = value.callable
                schema = TypeSpec("Callable", tuple(self.graph.types[k] for k in callback.parameters), self.graph.types[callback.returns], effect_bound=callback.effect_bound)
                self.graph.types[str(schema)] = schema
                if not self.matches(value, str(schema)):
                    return reject("wrapper callback must have its exact fixed positional signature")
                if not quiet:
                    self._ready_callable(value, env, node)
            if name == "compose":
                outer, inner = callbacks
                if len(outer.parameters) != 1 or len(inner.parameters) != 1 or inner.returns != outer.parameters[0] or not self._data_schema(self.graph.types.get(inner.returns)) or not self._data_schema(self.graph.types.get(outer.returns)) or not (inner.parameters[0] in CAPABILITIES or self._data_schema(self.graph.types.get(inner.parameters[0]))):
                    return reject("compose requires unary outer B->R and inner A->B, admitted data B/R, and data or exact capability input A")
                result = self._wrapper_value(name, inner.parameters, outer.returns, callbacks)
                failures = ()
            else:
                callback = callbacks[0]
                bound_schema = self.graph.types.get(callback.parameters[0]) if callback.parameters else None
                if len(callback.parameters) != 2 or not self._data_schema(bound_schema) or not self.matches(values[1], str(bound_schema)) or not self._data_schema(self.graph.types.get(callback.returns)) or not (callback.parameters[1] in CAPABILITIES or self._data_schema(self.graph.types.get(callback.parameters[1]))):
                    return reject("partial_first requires (A,B)->R with admitted data A/R and exact stable bound A; capabilities/callables cannot be bound")
                result = self._wrapper_value(name, callback.parameters[1:], callback.returns, callbacks,
                                             ((str(bound_schema), ast.dump(node.args[1], include_attributes=False)),))
                failures = self._nested_validation_failures(bound_schema)
            self._collection_operation("standard." + name, node, quiet, failures)
            return result
        if len(values) != (3 if name == "vector_scan" else 2):
            return reject(name + " has the published fixed eager Vector signature")
        schema = self.graph.types.get(values[0].kind)
        callback = values[1].callable
        if schema is None or schema.name != "Vector" or callback is None:
            return reject(name + " requires exact ordered Vector and resolved checked callback")
        element = schema.arguments[0]
        returned = self.graph.types.get(callback.returns)
        if name == "vector_scan":
            accumulator = self.graph.types.get(callback.parameters[0]) if len(callback.parameters) == 2 else None
            if not self._data_schema(accumulator) or not self.matches(values[2], str(accumulator)) or not self._collection_callback(values[1], (accumulator, element), accumulator, node.args[1], env, quiet):
                return reject("vector_scan requires (Vector[T], (A,T)->A, exact admitted A initial)")
            result = self._value_schema("Vector", (accumulator,))
        elif name == "vector_group_by":
            if returned is None or returned.name not in SCALARS or not self._collection_callback(values[1], (element,), returned, node.args[1], env, quiet):
                return reject("vector_group_by requires T->K with one exact scalar key schema")
            group = self._value_schema("Vector", (element,))
            result = self._value_schema("OrderedMap", (returned, self.graph.types[group.kind]))
        else:
            if returned is None or returned.name != "Result" or not self._collection_callback(values[1], (element,), returned, node.args[1], env, quiet):
                return reject("result_traverse requires T->Result[U,E] with admitted U/E schemas")
            successes = self._value_schema("Vector", (returned.arguments[0],))
            result = self._value_schema("Result", (self.graph.types[successes.kind], returned.arguments[1]))
        self._collection_operation("standard." + name, node, quiet, ("RecursionError",))
        return result

    def _integration_call(self, node, env, quiet):
        target = self._expr(node.func, env, quiet=True)
        name = target.kind[len("integration:"):] if target.kind and target.kind.startswith("integration:") else None
        if name not in INTEGRATION_NAMES:
            return None
        row = self.graph.integrations[name]
        if self.definition_mode or self.initializing or not self.active:
            if not quiet:
                self.emit("PAL241", node, "external integration invocation is confined to checked function bodies after ordinary setup")
            return UNKNOWN
        if not quiet:
            self.active.operations.add("integrations." + name)
        if self.graph.integration_dependency_replacements:
            if not quiet:
                self.emit("PAL240", node, "external adapter/native/importer dependencies have analyzed replacements: " + ", ".join(sorted(self.graph.integration_dependency_replacements)))
            return UNKNOWN
        if not quiet:
            self.active.external_operation_sites.setdefault("integrations." + name, set()).add(node.lineno)
        if row["admission"] != "approved":
            if not quiet:
                self.emit("PAL350", node, row["identity"] + " approval is " + row["admission"] + (": " + row["identity_error"] if row["identity_error"] else ""), origin="external operation policy")
            return UNKNOWN
        if node.keywords or len(node.args) != 1 or isinstance(node.args[0], ast.Starred):
            if not quiet:
                self.emit("PAL221", node, name + " requires exactly one positional-only exact bytes argument")
            return UNKNOWN
        value = self._expr(node.args[0], env, quiet=quiet)
        if value.kind != "bytes":
            if not quiet:
                self.emit("PAL221", node.args[0], name + " requires established exact bytes, not a mutable buffer or foreign protocol")
            return UNKNOWN
        if not quiet:
            self._require_effects(row["effects"], node, row["identity"])
            self._collection_operation("integrations." + name, node, failures=row["failures"])
        return Value.exact("bytes")

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
                    return reject(f"Vector.{method} requires a checked bounded fixed callback with admitted result")
                result = owner if method == "filter" else self._value_schema("Vector", (returned,))
                if method == "map":
                    failures = self._nested_validation_failures(returned)
            elif method == "fold" and len(values) == 2:
                callback = values[0].callable
                accumulator = self.graph.types.get(callback.parameters[0]) if callback and len(callback.parameters) == 2 else None
                if not self._data_schema(accumulator) or not self.matches(values[1], str(accumulator)) or not self._collection_callback(values[0], (accumulator, element), accumulator, node.args[0], env, quiet):
                    return reject("Vector.fold requires (checked bounded Callable[[A,T],A], admitted A initial)")
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

    def _record_call_value(self, node, env, quiet):
        target = self._expr(node.func, env, quiet=True)
        primitive = target.kind == "primitive:replace"
        if primitive:
            if len(node.args) != 1 or any(isinstance(a, ast.Starred) for a in node.args):
                if not quiet:
                    self.emit("PAL221", node, "replace requires one exact record and explicit field keywords")
                return UNKNOWN
            owner = self._expr(node.args[0], env, quiet=quiet)
            info = self.graph.records.get(owner.kind)
            positional = []
        elif target.kind and target.kind.startswith("record_class:"):
            info = self.graph.records.get(target.kind[len("record_class:"):])
            owner = self.annotation_value(info.identity) if info else UNKNOWN
            positional = list(info.fields) if info else []
        else:
            return None
        if not info or not info.valid:
            if not quiet:
                self.emit("PAL221", node, "operation requires a valid exact record declaration")
            return UNKNOWN
        supplied = dict(zip(positional, node.args)) if not primitive else {}
        malformed = not primitive and (len(node.args) > len(positional) or any(isinstance(a, ast.Starred) for a in node.args))
        for keyword in node.keywords:
            if keyword.arg is None or keyword.arg not in info.fields or keyword.arg in supplied:
                malformed = True
            else:
                supplied[keyword.arg] = keyword.value
        if malformed or not primitive and set(info.fields) - set(supplied) - set(info.defaults):
            if not quiet:
                self.emit("PAL221", node, "record construction/replacement requires its fixed field signature")
            return UNKNOWN
        for name, expression in supplied.items():
            value = self._expr(expression, env, quiet=quiet)
            if not self.matches(value, info.fields[name]):
                if not quiet:
                    self.emit("PAL221", expression, f"record field `{name}` requires {info.fields[name]}; found {self._describe(value)}")
                return UNKNOWN
        self._depend(info.analyzer.path)
        self._collection_operation("Record.replace" if primitive else "Record.construct", node, quiet, ("RecursionError",))
        return owner

    def _boundary_call(self, node, env, quiet):
        target = self._expr(node.func, env, quiet=True)
        if target.kind not in {"primitive:" + name for name in BOUNDARY_PRIMITIVES}:
            return None
        if self.active or self.definition_mode or self.initializing:
            if not quiet:
                self.emit("PAL230", node, "snapshot/export/adapters belong to an ordinary integration shell; ownership and mutable allocation have no pure strict M4 contract")
            return UNKNOWN
        if target.kind != "primitive:freeze" or len(node.args) != 1 or isinstance(node.args[0], ast.Starred):
            return UNKNOWN
        keywords = {k.arg: k.value for k in node.keywords}
        if len(keywords) != len(node.keywords) or any(k is None or k not in {"exclusive", "schema", "adapter"} for k in keywords):
            return UNKNOWN
        exclusive = keywords.get("exclusive")
        value = self._expr(node.args[0], env, quiet=True)
        if not self._data_value(value) and not (isinstance(exclusive, ast.Constant) and exclusive.value is True):
            return UNKNOWN
        if "schema" in keywords:
            shadowed = {name for name in self.locals if name not in env or not env[name].value.kind or not env[name].value.kind.startswith(("collection_class:", "record_class:", "variant_class:", "case_class:", "primitive:", "module:"))}
            expected = self._annotation(keywords["schema"], extra_names=shadowed)
            schema = self.graph.types.get(expected)
            return self.annotation_value(expected) if self._data_schema(schema) else UNKNOWN
        return value if self._data_value(value) else UNKNOWN

    def _failure_edge(self, target, node):
        if self.active:
            self.active.calls.add(target)
            edge = {"target": target, "line": node.lineno, "column": node.col_offset + 1,
                    "handled": sorted(self.handled_failures)}
            if edge not in self.active.failure_edges:
                self.active.failure_edges.append(edge)

    def _domain_call(self, node, env, quiet):
        target = self._expr(node.func, env, quiet=True)
        name = target.kind[len("primitive:"):] if target.kind and target.kind.startswith("primitive:") else None
        case_info = self.graph.cases.get(target.kind[len("case_class:"):]) if target.kind and target.kind.startswith("case_class:") else None
        if name not in DOMAIN_CASES | {"Failure", "failure_value", "accumulate"} and case_info is None:
            return None
        def reject(reason):
            if not quiet:
                self.emit("PAL221", node, reason)
            return UNKNOWN
        if name == "failure_value":
            if len(node.args) != 1 or node.keywords or not isinstance(node.args[0], ast.Name) or node.args[0].id not in self.exception_tokens:
                return reject("failure_value requires one direct live opaque handler exception token")
            schema = TypeSpec("record:pyalamode:Failure")
            self.graph.types[str(schema)] = schema
            self._collection_operation("Failure.convert", node, quiet, ("RecursionError",))
            return self.annotation_value(str(schema))
        if name == "accumulate":
            if len(node.args) != 2 or node.keywords:
                return reject("accumulate requires exactly two Result values with the same exact error schema")
            values = [self._expr(arg, env, quiet=quiet) for arg in node.args]
            schemas = [self.graph.types.get(value.kind) for value in values]
            if any(schema is None or schema.name != "Result" for schema in schemas) or schemas[0].arguments[1] != schemas[1].arguments[1]:
                return reject("accumulate requires two established Result[T,E] schemas with identical E; annotate checked inputs or bindings")
            pair = TypeSpec("tuple", (schemas[0].arguments[0], schemas[1].arguments[0]))
            errors = TypeSpec("Vector", (schemas[0].arguments[1],))
            self.graph.types[str(pair)] = pair
            self.graph.types[str(errors)] = errors
            result = self._value_schema("Result", (pair, errors))
            self._collection_operation("Result.accumulate", node, quiet, ("RecursionError",))
            return result
        fields = case_info.fields if case_info else {"category": "str", "message": "str"} if name == "Failure" else {} if name == "Nothing" else {"error" if name == "Err" else "value": None}
        defaults = case_info.defaults if case_info else {}
        if any(isinstance(arg, ast.Starred) for arg in node.args) or any(keyword.arg is None for keyword in node.keywords) or len(node.args) > len(fields):
            return reject("case construction requires its exact fixed field signature")
        values = {key: self._expr(arg, env, quiet=quiet) for key, arg in zip(fields, node.args)}
        for keyword in node.keywords:
            if keyword.arg not in fields or keyword.arg in values:
                return reject("case constructor has an unknown or duplicate field")
            values[keyword.arg] = self._expr(keyword.value, env, quiet=quiet)
        for field_name, expected in fields.items():
            value = values.get(field_name, defaults.get(field_name))
            if value is None or expected is not None and not self.matches(value, expected) or expected is None and (not self._data_value(value) or value.kind is None):
                return reject("case field `" + field_name + "` requires its exact recursively admitted immutable data schema")
            values[field_name] = value
        if case_info:
            result = self.annotation_value(case_info.identity)
            operation = "Variant.construct"
        elif name == "Failure":
            schema = TypeSpec("record:pyalamode:Failure")
            self.graph.types[str(schema)] = schema
            result = self.annotation_value(str(schema))
            operation = "Failure.construct"
        else:
            result = self._value_schema(name, () if name == "Nothing" else (self.graph.types[next(iter(values.values())).kind],))
            operation = name + ".construct"
        self._collection_operation(operation, node, quiet, ("RecursionError",) if fields else ())
        return result

    def _handler_identity(self, node):
        if isinstance(node, ast.Name) and node.id in HANDLER_CATEGORIES and node.id not in self.locals and node.id not in self.global_writes:
            return node.id if not self._module_changed("builtins", node.id) else None
        reference = self.graph.reference(self, node)
        if reference and reference.startswith("foundation:builtins:"):
            name = reference.rsplit(":", 1)[-1]
            root = node
            while isinstance(root, ast.Attribute):
                root = root.value
            symbol = self.symbols.get(root.id) if isinstance(root, ast.Name) and root.id not in self.locals else None
            if name in HANDLER_CATEGORIES and symbol and self._symbol_stable(root.id, symbol) and self._foundation_available("builtins") and not self._module_changed("builtins", name):
                return name
        return None

    def _try_statement(self, node, env):
        if not self.active or node.orelse or node.finalbody or not node.handlers:
            self.emit("PAL340", node, "checked try supports known category handlers, without else/finally or arbitrary cleanup")
            return env
        covered = set()
        handlers = []
        targets = set()
        for handler in node.handlers:
            expressions = handler.type.elts if isinstance(handler.type, ast.Tuple) else [handler.type]
            categories = [self._handler_identity(expression) for expression in expressions if expression is not None]
            if not categories or any(category is None for category in categories):
                self.emit("PAL340", handler, "handler categories must be unchanged exact characterized builtins; broad/user/bare handlers are unsupported")
                continue
            mask = set()
            for category in categories:
                scope = set(HANDLER_COVERAGE[category])
                if scope & (mask | covered):
                    self.emit("PAL340", handler, "handler categories overlap in the characterized builtin hierarchy")
                mask.update(scope)
            covered.update(mask)
            if handler.name:
                targets.add(handler.name)
                if handler.name in env or handler.name in self.cleanup_names:
                    self.emit("PAL101", handler, "exception cleanup target must be fresh and cannot overwrite a stable binding")
            handlers.append((handler, categories, mask))
        try_writes = set(_written_names(node.body))
        for handler, _, _ in handlers:
            if handler.name in try_writes:
                self.emit("PAL101", handler, "exception target can overwrite a partially initialized try binding")
        previous_mask = self.handled_failures
        self.handled_failures = previous_mask | covered
        try:
            successful = self._block(node.body, dict(env))
        finally:
            self.handled_failures = previous_mask
        continuing = successful
        for handler, categories, mask in handlers:
            conflicting = try_writes & set(_written_names(handler.body))
            if conflicting:
                self.emit("PAL101", handler, "handler can reinitialize partially completed try bindings: " + ", ".join(sorted(conflicting)))
            nested = dict(env)
            if handler.name:
                nested[handler.name] = Binding(UNKNOWN, (handler.lineno,))
                self.exception_tokens.add(handler.name)
            self.active.handlers.append({"line": handler.lineno, "categories": categories, "discharged": sorted(mask),
                                         "target": handler.name, "target_semantics": "opaque actual Python exception, deleted on every handler exit"})
            try:
                branch = self._block(handler.body, nested)
            finally:
                if handler.name:
                    self.exception_tokens.discard(handler.name)
            if branch is not None and handler.name:
                branch[handler.name] = Binding(UNKNOWN, (handler.lineno,), False)
            continuing = self._merge(continuing, branch)
        self.cleanup_names.update(targets)
        if continuing is not None:
            for name in targets:
                continuing[name] = Binding(UNKNOWN, (node.lineno,), False)
        return continuing

    def _pattern_shape(self, schema, reference):
        if schema is None:
            return None
        case_info = self.graph.cases.get(reference)
        if case_info and self._domain_matches(case_info.schema, schema) or case_info and schema == case_info.schema:
            return case_info.identity, case_info.fields
        record_info = self.graph.records.get(reference)
        if record_info and record_info.schema == schema:
            return record_info.identity, record_info.fields
        if schema.name == "record:pyalamode:Failure" and reference == "foundation:pyalamode:Failure":
            return str(schema), {"category": "str", "message": "str"}
        name = reference.rsplit(":", 1)[-1] if reference and reference.startswith("foundation:pyalamode:") else None
        if schema.name == "Option" and name in {"Some", "Nothing"}:
            return name, {} if name == "Nothing" else {"value": str(schema.arguments[0])}
        if schema.name == "Result" and name in {"Ok", "Err"}:
            return name, {"value" if name == "Ok" else "error": str(schema.arguments[0 if name == "Ok" else 1])}
        if schema.name in DOMAIN_CASES and name == schema.name:
            return name, {} if name == "Nothing" else {"error" if name == "Err" else "value": str(schema.arguments[0])}
        return None

    def _pattern(self, pattern, schema, captures):
        if isinstance(pattern, ast.MatchAs) and pattern.pattern is None:
            if pattern.name:
                if pattern.name in captures:
                    self.emit("PAL330", pattern, "a pattern capture name appears twice")
                captures[pattern.name] = self.annotation_value(str(schema))
            return None, True
        if schema.name == "union":
            return self._union_pattern(pattern, schema, captures)
        if isinstance(pattern, ast.MatchSingleton):
            kind = "None" if pattern.value is None else "bool"
            if schema.name != kind:
                self.emit("PAL330", pattern, "singleton pattern requires its exact scalar payload schema")
            return repr(pattern.value), schema.name == "None"
        if isinstance(pattern, ast.MatchValue) and isinstance(pattern.value, (ast.Constant, ast.UnaryOp)):
            value = self._expr(pattern.value, {}, quiet=True)
            if value.kind != str(schema) or value.kind not in {"int", "str", "bytes"}:
                self.emit("PAL330", pattern, "literal pattern requires an exact same-type scalar payload")
            return None, False
        if isinstance(pattern, ast.MatchClass):
            reference = self.graph.reference(self, pattern.cls)
            shape = self._pattern_shape(schema, reference)
            value = self._expr(pattern.cls, {}, quiet=True)
            if shape is None or not value.kind or not value.kind.startswith(("case_class:", "record_class:", "primitive:")):
                self.emit("PAL330", pattern, "class pattern requires a resolved unchanged exact product case/record compatible with the subject")
                return None, False
            tag, fields = shape
            if len(pattern.patterns) > len(fields) or len(set(pattern.kwd_attrs)) != len(pattern.kwd_attrs):
                self.emit("PAL330", pattern, "class pattern exceeds its fixed payload signature")
                return tag, False
            names = list(fields)[:len(pattern.patterns)]
            children = list(pattern.patterns)
            for name, child in zip(pattern.kwd_attrs, pattern.kwd_patterns):
                if name not in fields or name in names:
                    self.emit("PAL330", pattern, "class pattern contains an unknown or duplicate payload field")
                    return tag, False
                names.append(name)
                children.append(child)
            complete = True
            for name, child in zip(names, children):
                child_schema = self.graph.types[fields[name]]
                child_tag, irrefutable = self._pattern(child, child_schema, captures)
                # A narrowing pattern never exhausts a union-typed payload.
                if child_schema.name == "union" and not (isinstance(child, ast.MatchAs) and child.pattern is None):
                    irrefutable = False
                # A full payload case does not exhaust its containing union.
                if isinstance(child, ast.MatchClass):
                    if child_schema.name in DOMAIN_TYPES:
                        irrefutable = False
                    elif child_schema.name.startswith("variant:"):
                        irrefutable &= len(self.graph.variants[str(child_schema)].cases) == 1
                complete &= irrefutable
            return tag, complete
        self.emit("PAL330", pattern, "pattern has no characterized finite dispatch/binding contract")
        return None, False

    def _union_pattern(self, pattern, schema, captures):
        """Narrow one pattern to the closed-union member its exact runtime class selects."""
        members = {str(member): member for member in schema.arguments}

        def member_for(classes):
            for member in schema.arguments:
                if classes & (self.union_classes(member) or set()):
                    return member
            return None

        if isinstance(pattern, ast.MatchSingleton):
            kind = "None" if pattern.value is None else "bool"
            if kind not in members:
                self.emit("PAL330", pattern, "singleton pattern requires a matching None or bool union member")
                return None, False
            return repr(pattern.value), True
        if isinstance(pattern, ast.MatchValue) and isinstance(pattern.value, (ast.Constant, ast.UnaryOp)):
            value = self._expr(pattern.value, {}, quiet=True)
            if value.kind not in {"int", "str", "bytes"} or value.kind not in members:
                self.emit("PAL330", pattern, "literal pattern requires an exact same-type scalar union member")
            return None, False
        if isinstance(pattern, ast.MatchClass):
            names, scope = set(), self.active.node if self.active else None
            while scope is not None:
                if isinstance(scope, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.update(_written_names(scope.body))
                    names.update(a.arg for a in scope.args.posonlyargs + scope.args.args + scope.args.kwonlyargs)
                scope = self.parents.get(id(scope))
            kind = self._type_identity(pattern.cls, names) if isinstance(pattern.cls, ast.Name) else None
            if kind in {"bool", "int", "str", "bytes"}:
                if kind not in members or pattern.kwd_patterns or len(pattern.patterns) > 1:
                    self.emit("PAL330", pattern, "scalar class pattern requires a matching union member and at most one positional pattern for the subject itself")
                    return None, False
                complete = True
                if pattern.patterns:
                    _, complete = self._pattern(pattern.patterns[0], members[kind], captures)
                return ("bool" if kind == "bool" else kind), complete
            reference = self.graph.reference(self, pattern.cls)
            case_info = self.graph.cases.get(reference)
            record_info = self.graph.records.get(reference)
            classes = {case_info.identity} if case_info else {record_info.identity} if record_info else {"Record['pyalamode:Failure']"} if reference == "foundation:pyalamode:Failure" else set()
            member = member_for(classes)
            if member is None:
                self.emit("PAL330", pattern, "class pattern requires a resolved unchanged exact record or case that is a member of the closed union")
                return None, False
            return self._pattern(pattern, member, captures)
        self.emit("PAL330", pattern, "pattern has no characterized finite dispatch/binding contract")
        return None, False

    def _match_statement(self, node, env):
        subject = self._expr(node.subject, env)
        schema = self.graph.types.get(subject.kind)
        if schema is None and len(subject.types) > 1 and not subject.callable and not subject.capability:
            # Merged branch values already carry a finite exact type set.
            specs = [self.graph.types.get(kind) for kind in subject.types]
            schema, _ = self.union_schema(specs) if all(specs) else (None, None)
            if schema is not None:
                self.graph.types[str(schema)] = schema
        if schema is None or schema.name not in DOMAIN_TYPES | DOMAIN_CASES | {"bool", "None", "union"} and not schema.name.startswith(("variant:", "case:", "record:")):
            self.emit("PAL330", node, "match requires one established closed domain/case/union, exact record, bool or None schema")
            return env
        if schema.name == "union":
            domain = None
            expected = self.union_tags(schema)
            identity, version = str(schema), self.union_fingerprint(schema)
            member_domains = [self.graph.variants[str(member)] for member in schema.arguments if member.name.startswith("variant:")]
            policy_domains = {info.module + ":" + info.node.name for info in member_domains}
        elif schema.name.startswith("variant:"):
            domain = self.graph.variants[str(schema)]
            expected = {case.identity for case in domain.cases.values()}
            identity = domain.module + ":" + domain.node.name
            version = domain.fingerprint
        else:
            domain = None
            expected = {"Some", "Nothing"} if schema.name == "Option" else {"Ok", "Err"} if schema.name == "Result" else {"True", "False"} if schema.name == "bool" else {"None"} if schema.name == "None" else {str(schema)} if schema.name.startswith(("case:", "record:")) else {schema.name}
            identity, version = str(schema), "builtin-domains-v1"
        coverage, wildcard, continuing = set(), False, None
        for index, case in enumerate(node.cases):
            captures = {}
            tag, complete = self._pattern(case.pattern, schema, captures)
            is_wildcard = isinstance(case.pattern, ast.MatchAs) and case.pattern.pattern is None and case.pattern.name is None
            if captures and (not complete or case.guard is not None):
                self.emit("PAL330", case.pattern, "failed partial/guarded patterns cannot establish fresh capture initialization")
            if isinstance(case.pattern, ast.MatchAs) and case.pattern.name:
                self.emit("PAL330", case.pattern, "root named capture is outside explicit finite dispatch; use class patterns or explicit _")
            branch = dict(env)
            for name, value in captures.items():
                if name in env and not self.in_dead:
                    self.emit("PAL101", case.pattern, "pattern capture `" + name + "` overwrites an initialized binding", first=env[name].first[0])
                branch[name] = Binding(value, (case.pattern.lineno,))
            guarded = case.guard is not None
            guard_true = False
            if guarded:
                guard = self._expr(case.guard, branch)
                if guard.kind != "bool":
                    self.emit("PAL210", case.guard, "pattern guard requires exact bool")
                guard_true = guard.literal is True
            if (complete or schema.name == "bool" and isinstance(case.pattern, ast.MatchSingleton)) and (not guarded or guard_true) and tag:
                coverage.update({"True", "False"} if tag == "bool" else {tag})
            if is_wildcard and (not guarded or guard_true):
                wildcard = True
                if index != len(node.cases) - 1:
                    self.emit("PAL330", case.pattern, "deliberate wildcard must be final")
            continuing = self._merge(continuing, self._block(case.body, branch))
        if schema.name != "union":
            policy_domains = {identity} if domain else set()
        policy_explicit = bool(policy_domains & set(self.policy.get("explicit_cases", [])))
        if policy_explicit and wildcard:
            self.emit("PAL330", node, "project explicit_cases policy requires full explicit case coverage and forbids wildcard consumers")
        if not wildcard and expected - coverage:
            self.emit("PAL330", node, "match is not exhaustive; missing full case coverage: " + ", ".join(sorted(expected - coverage)))
        if self.active:
            self.active.patterns.append({"line": node.lineno, "schema": str(schema), "case_set": sorted(expected), "covered": sorted(coverage),
                                         "wildcard": wildcard, "case_fingerprint": version, "policy_explicit": policy_explicit})
        self._collection_operation("Pattern.dispatch", node, failures=("RecursionError",) if schema.name not in {"bool", "None"} else ())
        return continuing

    def _statement(self, node, env):
        if isinstance(node, ast.Match):
            return self._match_statement(node, env)
        if isinstance(node, ast.Try):
            return self._try_statement(node, env)
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            names = _target_names(node)
            if any(name in self.cleanup_names or name in self.exception_tokens for name in names):
                self.emit("PAL340", node, "opaque exception cleanup targets cannot be initialized or aliased as stable bindings")
                return env
        if isinstance(node, ast.With):
            if len(node.items) != 1:
                self.emit("PAL320", node, "borrow admits exactly one context item")
                return env
            item = node.items[0]
            call = item.context_expr
            target = self._expr(call.func, env, quiet=True) if isinstance(call, ast.Call) else UNKNOWN
            capability = self._expr(call.args[0], env) if isinstance(call, ast.Call) and len(call.args) == 1 else UNKNOWN
            if not self.active or self.definition_mode or self.initializing or target.kind != "primitive:borrow" or not isinstance(call, ast.Call) or call.keywords or len(call.args) != 1 or not isinstance(call.args[0], ast.Name) or capability.kind not in CAPABILITIES or not isinstance(item.optional_vars, ast.Name):
                self.emit("PAL320", node, "only with borrow(exact local capability) as fresh_name has a characterized context lifetime")
                return env
            name = item.optional_vars.id
            if name in env and not self.in_dead:
                self.emit("PAL101", node, f"borrow binding `{name}` is already initialized", first=env[name].first[0])
                return env
            if not self._foundation_available("pyalamode.effects") or self._module_changed("pyalamode", "borrow"):
                self.emit("PAL240", node, "borrow implementation or dependency identity was replaced")
            self._require_effects((CAPABILITIES[capability.kind],), node, "borrow entry/exit")
            self._collection_operation("borrow.enter_exit", node, failures=("RuntimeError",))
            self.active.borrow_scopes.append({"name": name, "interface": capability.kind, "line": node.lineno, "end_line": node.end_lineno, "lifetime": "logical view invalidated on every exit; resource transfer unsupported"})
            nested = dict(env)
            nested[name] = Binding(capability, (node.lineno,))
            result = self._block(node.body, nested)
            if result is not None:
                result[name] = Binding(UNKNOWN, (node.lineno,), False)
            return result
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            # Characterized effects may intentionally return None. Unknown calls
            # still go through finite call resolution and fail, regardless of bounds.
            value = self._expr(node.value, env)
            owner = self._expr(node.value.func.value, env, quiet=True) if isinstance(node.value.func, ast.Attribute) else UNKNOWN
            if owner.kind in CAPABILITIES or value.kind == "None":
                return env
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
            value = self._expr(node.value, env, quiet=True)
            if value.kind in CAPABILITIES:
                self.emit("PAL320", node, "capability alias bindings are unsupported; use a parameter or finite borrow scope")
                return env
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and self._primitive_identity(node.value.func, {"replace"}):
            self._expr(node.value, env)
            self.emit("PAL250", node, "replace returns a new record value; its result is ignored", origin="persistent return-only operation")
            return env
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
            self._add_failures(info.definition_failures)
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
            if expected and self.graph.types.get(expected, TypeSpec("")).name in DOMAIN_TYPES and self.matches(value, expected):
                value = self.annotation_value(expected)
            if node.target.id in env and not self.in_dead:
                self.emit("PAL101", node, f"`{node.target.id}` is already initialized", first=env[node.target.id].first[0])
            else:
                env[node.target.id] = Binding(value, (node.lineno,))
                self._data_assertion(node, node.target.id, value)
            return env
        result = super()._statement(node, env)
        if isinstance(node, ast.Assign) and result is not None:
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in result:
                    self._data_assertion(node, target.id, result[target.id].value)
        return result

    def _data_assertion(self, node, name, value):
        if self.active and self._data_value(value) and value.kind:
            assertion = {"line": node.lineno, "name": name, "schema": value.kind}
            if assertion not in self.active.data_assertions:
                self.active.data_assertions.append(assertion)

    def _expr(self, node, env, *, quiet=False):
        def reject(rule, reason):
            if not quiet:
                self.emit(rule, node, reason)
            return UNKNOWN
        if isinstance(node, ast.Name):
            if node.id in getattr(self, "exception_tokens", set()):
                return reject("PAL340", "actual handler exceptions are opaque; only direct failure_value conversion is admitted")
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
                if value.kind in CAPABILITIES:
                    return reject("PAL320", f"capability `{node.id}` cannot be captured by a callable")
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
            if owner.kind and owner.kind.startswith("variant_class:"):
                domain = self.graph.variants.get(owner.kind[len("variant_class:"):])
                case_info = domain.cases.get(node.attr) if domain else None
                if case_info and case_info.valid and case_info.identity not in self.graph.replaced_variants:
                    return Value.exact("case_class:" + case_info.identity)
                return reject("PAL240", "domain member is absent or its behavior is replaced")
            case_info = self.graph.cases.get(owner.kind)
            if case_info and node.attr in case_info.fields:
                self._collection_operation("Variant.field", node, quiet)
                return self.annotation_value(case_info.fields[node.attr])
            schema = self.graph.types.get(owner.kind)
            if schema and schema.name in {"Some", "Ok", "Err"} and node.attr == ("error" if schema.name == "Err" else "value"):
                self._collection_operation(schema.name + ".field", node, quiet)
                return self.annotation_value(str(schema.arguments[0]))
            if owner.kind == "Record['pyalamode:Failure']" and node.attr in {"category", "message"}:
                self._collection_operation("Failure.field", node, quiet)
                return Value.exact("str")
            record_info = self.graph.records.get(owner.kind)
            if record_info and node.attr in record_info.fields:
                self._collection_operation("Record.field", node, quiet)
                return self.annotation_value(record_info.fields[node.attr])
            if owner.kind and owner.kind.startswith("module:"):
                module = owner.kind.split(":", 1)[1]
                if self._module_changed(module, node.attr):
                    return reject("PAL240", f"resolved dependency `{module}.{node.attr}` has an analyzed replacement")
                if module == "builtins" and node.attr in BUILTINS:
                    return Value.exact("builtin:" + node.attr)
                if module == "pyalamode.integrations" and node.attr in INTEGRATION_NAMES and self._foundation_available(module):
                    return Value.exact("integration:" + node.attr)
                if module == "pyalamode" and node.attr == "integrations" and self._integration_imported() and self._foundation_available("pyalamode.integrations"):
                    return Value.exact("module:pyalamode.integrations")
                if module == "pyalamode" and node.attr == "standard" and self._foundation_available("pyalamode.standard"):
                    return Value.exact("module:pyalamode.standard")
                if module == "pyalamode" and node.attr in COLLECTIONS and self._foundation_available(module):
                    return Value.exact("collection_class:" + node.attr)
                if module in {"pyalamode", "pyalamode.effects", "pyalamode.variants", "pyalamode.failures", "pyalamode.standard"} and node.attr in RECORD_PRIMITIVES | BOUNDARY_PRIMITIVES | EFFECT_PRIMITIVES | DOMAIN_PRIMITIVES | STANDARD_NAMES and self._foundation_available(module) and not self._module_changed("pyalamode", node.attr):
                    return Value.exact("primitive:" + node.attr)
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
                    self._add_failures(("ValueError",))
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
            if schema and (schema.name in COLLECTIONS | {"tuple"} or schema.name.startswith(("record:", "variant:", "case:")) or schema.name in DOMAIN_TYPES | DOMAIN_CASES) and not any(isinstance(op, (ast.Is, ast.IsNot)) for op in node.ops):
                previous = left
                for operation, comparator in zip(node.ops, node.comparators):
                    value = self._expr(comparator, env, quiet=quiet)
                    if not isinstance(operation, (ast.Eq, ast.NotEq)) or not self.matches(value, previous.kind):
                        return reject("PAL210", "collection/tuple equality requires the same recursively exact data schema; arbitrary ordering is excluded")
                    previous = value
                recursive = any(arg.name not in SCALARS for arg in schema.arguments)
                self._collection_operation(("Record" if schema.name.startswith("record:") else "Variant" if schema.name.startswith(("variant:", "case:")) else schema.name) + ".equivalent", node, quiet, ("RecursionError",) if recursive or schema.name.startswith(("record:", "variant:", "case:")) or schema.name in DOMAIN_TYPES | DOMAIN_CASES else ())
                return Value.exact("bool")
        if isinstance(node, ast.Tuple):
            if any(isinstance(item, ast.Starred) for item in node.elts):
                return reject("PAL201", "tuple unpacking has no supported construction contract")
            items = tuple(self._expr(item, env, quiet=quiet) for item in node.elts)
            if any(not self._data_value(value) for value in items):
                return reject("PAL221", "tuple contents must be recursively admitted immutable data; capabilities/callables/modules are not tuple data")
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
            integration = self._integration_call(node, env, quiet)
            if integration is not None:
                return integration
            standard = self._standard_call(node, env, quiet)
            if standard is not None:
                return standard
            domain_value = self._domain_call(node, env, quiet)
            if domain_value is not None:
                return domain_value
            capability = self._capability_call(node, env, quiet)
            if capability is not None:
                return capability
            provider = self._provider_call(node, env, quiet)
            if provider is not None:
                return provider
            record_value = self._record_call_value(node, env, quiet)
            if record_value is not None:
                return record_value
            boundary_value = self._boundary_call(node, env, quiet)
            if boundary_value is not None:
                return boundary_value
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
                self._require_effects(callback.effect_bound, node, "callable invocation")
            if callback.wrapper:
                self._wrapper_inputs(node, callback, env, quiet)
                parameters = tuple(self.graph.types[k] for k in callback.parameters)
                returned = self.graph.types[callback.returns]
                if not self._collection_callback(target, parameters, returned, node, env, quiet):
                    return reject("PAL221", "wrapper invocation requires its exact characterized callable contract")
                if not quiet:
                    self._add_failures(self._nested_validation_failures(returned))
                    for identity in self._wrapper_operations(callback):
                        self._collection_operation(identity, node)
                return self.annotation_value(callback.returns)
            if callback.targets:
                if callback.conditional:
                    if node.keywords or len(node.args) != len(callback.parameters) or any(isinstance(a, ast.Starred) for a in node.args):
                        return reject("PAL221", "a conditional callback alternative requires its exact fixed positional signature")
                    for arg, expected in zip(node.args, callback.parameters):
                        if not self.matches(self._expr(arg, env, quiet=quiet), expected) and not quiet:
                            self.emit("PAL221", arg, f"conditional callback argument requires {expected}")
                    if not quiet:
                        self._add_failures(self._callable_failures(callback.effect_bound))
                infos = [self.graph.functions[identity] for identity in callback.targets]
                for info in infos:
                    self._checked_inputs(node, info, env, quiet)
                    if self.active and not quiet:
                        self._failure_edge(info.identity, node)
                        self.active.dependencies.update(info.dependencies)
                    self._depend(info.analyzer.path)
                returns = {info.returns for info in infos}
                if len(infos) == 1 and not callback.conditional and self.graph.types.get(infos[0].returns, TypeSpec("")).name == "Callable":
                    info = infos[0]
                    if info.parent is None and not info.analyzed and not info.analyzing:
                        info.analyzer.function(info)
                    if info.return_value and info.return_value.callable:
                        bindings = self._callable_bindings(node, info, env)
                        specialized = self._specialize_callable(info.return_value.callable, bindings)
                        schema = TypeSpec("Callable", tuple(self.graph.types[k] for k in specialized.parameters), self.graph.types[specialized.returns], effect_bound=specialized.effect_bound)
                        self.graph.types[str(schema)] = schema
                        return Value.exact(str(schema)).with_callable(specialized)
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
                    self._add_failures(self._callable_failures(callback.effect_bound))
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
            if value.callable and self.active and not quiet:
                self._ready_callable(value, env, arg)
                key = info.identity + ":" + name
                self.active.callable_arguments.setdefault(key, set()).update(value.callable.targets)
            if expected and not self.matches(value, expected) and not quiet:
                self.emit("PAL221", arg, f"argument `{name}` of `{info.qualified}` requires {expected}; found {self._describe(value)}")

    def _call_inputs(self, node, contract, env):
        info = self.graph.functions.get(contract.path + "::" + contract.name)
        if info:
            self._checked_inputs(node, info, env)

    def _ordinary_resolved_info(self, expression, env):
        value = self._expr(expression, env, quiet=True)
        if value.callable and value.callable.wrapper:
            return value
        if value.callable and len(value.callable.targets) == 1:
            return self.graph.functions[value.callable.targets[0]]
        return None

    @staticmethod
    def _callable_evidence(callback):
        return {"parameters": list(callback.parameters), "returns": callback.returns,
                "targets": list(callback.targets), "captures": [list(c) for c in callback.captures], "conditional": callback.conditional, "effect_bound": list(callback.effect_bound),
                "wrapper": callback.wrapper, "components": [FunctionalAnalyzer._callable_evidence(part) for part in callback.components],
                "bound_arguments": [list(bound) for bound in callback.bound_arguments], "obligation": callback.obligation,
                "captured_callbacks": [[name, FunctionalAnalyzer._callable_evidence(part)] for name, part in callback.captured_callbacks]}

    @staticmethod
    def _restore_callable(evidence):
        return CallableValue(tuple(evidence["parameters"]), evidence["returns"], tuple(evidence["targets"]), tuple(tuple(c) for c in evidence["captures"]), evidence["conditional"], tuple(evidence["effect_bound"]),
                             evidence.get("wrapper"), tuple(FunctionalAnalyzer._restore_callable(part) for part in evidence.get("components", [])),
                             tuple(tuple(bound) for bound in evidence.get("bound_arguments", [])), evidence.get("obligation"),
                             tuple((name, FunctionalAnalyzer._restore_callable(part)) for name, part in evidence.get("captured_callbacks", [])))

    def _wrapper_inputs(self, node, callback, env, quiet):
        if node.keywords or len(node.args) != len(callback.parameters) or any(isinstance(arg, ast.Starred) for arg in node.args):
            if not quiet:
                self.emit("PAL221", node, "wrapper invocation requires exactly its fixed positional signature")
            return
        for arg, expected in zip(node.args, callback.parameters):
            if not self.matches(self._expr(arg, env, quiet=quiet), expected) and not quiet:
                self.emit("PAL221", arg, "wrapper argument requires exact " + expected)

    def _callable_bindings(self, node, info, env):
        positional = [name for name, kind in info.kinds.items() if kind != "keyword_only"]
        supplied = dict(zip(positional, node.args))
        supplied.update((kw.arg, kw.value) for kw in node.keywords if kw.arg in info.parameters)
        bindings = {}
        for name in info.parameters:
            value = self._expr(supplied[name], env, quiet=True) if name in supplied else info.defaults.get(name, UNKNOWN)
            if value.callable:
                bindings[info.identity + ":" + name] = value.callable
        return bindings

    def _specialize_callable(self, callback, bindings):
        if callback.obligation in bindings:
            return bindings[callback.obligation]
        parts = tuple(self._specialize_callable(part, bindings) for part in callback.components)
        captured = tuple((name, self._specialize_callable(part, bindings)) for name, part in callback.captured_callbacks)
        if parts:
            return CallableValue(callback.parameters, callback.returns,
                                 tuple(sorted({target for part in parts for target in part.targets})),
                                 tuple(sorted({capture for part in parts for capture in part.captures})),
                                 any(part.conditional for part in parts), tuple(sorted({effect for part in parts for effect in part.effect_bound})),
                                 callback.wrapper, parts, callback.bound_arguments, captured_callbacks=captured)
        return CallableValue(callback.parameters, callback.returns, callback.targets, callback.captures, callback.conditional, callback.effect_bound,
                             callback.wrapper, parts, callback.bound_arguments, callback.obligation, captured)

    @staticmethod
    def _wrapper_operations(callback):
        own = {"standard." + callback.wrapper + ".invoke"} if callback.wrapper in {"compose", "partial_first"} else set()
        return own | {operation for part in callback.components for operation in FunctionalAnalyzer._wrapper_operations(part)}

    def _wrapper_validation_failures(self, callback):
        failures = set()
        if callback.wrapper == "compose":
            for kind in (callback.components[1].returns, callback.returns):
                failures.update(self._nested_validation_failures(self.graph.types.get(kind)))
        elif callback.wrapper == "partial_first":
            failures.update(self._nested_validation_failures(self.graph.types.get(callback.returns)))
        for part in callback.components:
            failures.update(self._wrapper_validation_failures(part))
        return failures

    def _ready_callable(self, value, env, node, seen=None):
        if not value.callable or not self.active:
            return
        seen = set() if seen is None else seen
        for part in value.callable.components:
            schema = TypeSpec("Callable", tuple(self.graph.types[k] for k in part.parameters), self.graph.types[part.returns], effect_bound=part.effect_bound)
            self.graph.types[str(schema)] = schema
            self._ready_callable(Value.exact(str(schema)).with_callable(part), env, node, seen)
        for _, part in value.callable.captured_callbacks:
            schema = TypeSpec("Callable", tuple(self.graph.types[k] for k in part.parameters), self.graph.types[part.returns], effect_bound=part.effect_bound)
            self.graph.types[str(schema)] = schema
            self._ready_callable(Value.exact(str(schema)).with_callable(part), env, node, seen)
        for target in value.callable.targets:
            if target in seen:
                continue
            seen.add(target)
            info = self.graph.functions[target]
            self.active.callable_dependencies.add(target)
            self._depend(info.analyzer.path)
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
        self.result.records = []
        for info in self.graph.record_declarations:
            if info.analyzer is not self:
                continue
            admitted = info.valid and self.result.mode == "strict" and not self.result.diagnostics
            self.result.records.append({
                "name": info.node.name, "schema": info.identity, "path": self.path, "line": info.node.lineno,
                "fields": dict(info.fields), "defaults": {name: value.kind for name, value in info.defaults.items()},
                "enforcement": self.result.mode,
                "behavior": "pure admitted construction, replacement and field/value operations" if admitted else "unverified declaration; product construction behavior is conditional on a qualifying declaration",
                "source_evidence": "checked record declaration" if admitted else "unverified record declaration",
                "implementation_evidence": "trusted product records-v1 implementation; generated library methods are not application source-checked methods",
                "trust": ["CPython 3.13.1 standard class, slot, tuple and closed annotation operations",
                          "pyalamode records-v1 exact field schemas, deep data validation and identity-only record metadata",
                          "pyalamode collections-v1 recursive data validation and typed value equivalence"],
                "failures": ["RecursionError"],
                "definition_failures": sorted(info.failures),
                "ordinary_validation_failures": {"TypeError": "invalid or unsupported field data, names or constructor/replacement signature; outside admitted input contracts",
                                                 "AttributeError": "ordinary field mutation or reinitialization is rejected"},
                "ordinary_representation_failures": {"ValueError": "CPython exact-int decimal formatting limit; repr is outside strict expression admission"},
                "freshness": "current for recorded inputs" if admitted else "no successful checked claim",
                "boundary_protection": "no generated record export guard; ordinary library constructors and replacement validate exact field invariants",
                "caller_obligations": [*[name + ": exact " + kind + "; recursively admitted field data" for name, kind in info.fields.items()],
                                       "Record class, behavioral definitions, product runtime and finite foundational dependencies remain unchanged during execution.",
                                       "Compatible foreign classes require a named shell snapshot adapter; frozen=True alone is not record admission.",
                                       "Allocation identity, arbitrary formatting/hashing and unsupported hooks are outside strict record operations."],
                "equivalence": "exact record type and recursively equivalent fields in declaration order"})
        self.result.variants = []
        for info in self.graph.variant_declarations:
            if info.analyzer is not self:
                continue
            admitted = info.valid and self.result.mode == "strict" and not self.result.diagnostics
            self.result.variants.append({"name": info.node.name, "schema": info.identity, "path": self.path, "line": info.node.lineno,
                "cases": {name: {"schema": case_info.identity, "fields": dict(case_info.fields), "defaults": {n: v.kind for n, v in case_info.defaults.items()}} for name, case_info in info.cases.items()},
                "case_fingerprint": info.fingerprint, "enforcement": self.result.mode,
                "behavior": "pure exact closed-case construction, field/pattern dispatch and type-sensitive value equivalence" if admitted else "unverified declaration",
                "source_evidence": "checked closed variant declaration" if admitted else "unverified variant declaration",
                "trust": ["pyalamode variants-v1 immutable exact case catalog, approved records/collections validators and ordinary CPython class operations"],
                "failures": ["RecursionError"], "definition_failures": sorted({failure for case_info in info.cases.values() for failure in case_info.failures}),
                "freshness": "current for recorded case set and ordered schemas" if admitted else "no successful checked claim",
                "boundary_protection": "ordinary constructors validate payloads; optional selected data guards reported separately",
                "caller_obligations": ["Exact declared cases and recursively admitted payloads; unchanged domain/case behavior, builtin bindings and product runtime.",
                    "Unchecked behavioral replacement violates dependency assumptions; no universal sealing or surveillance claim.",
                    "Unknown objects, subclasses, reflective matching/formatting and allocation identity are excluded."],
                "equivalence": "exact domain case tag and recursively type-sensitive payloads in declaration field order"})
        self.result.dependencies = {path: hashlib.sha256(self.graph.analyzers[path].source.encode()).hexdigest()
                                    for path in sorted(self.dependencies) if path in self.graph.analyzers and path != self.path}
        if self.result.mode == "audit" or self.result.diagnostics:
            self.result.initialization_evidence = "unverified initialization" if self.module_mode else self.result.initialization_evidence
            for contract in self.result.contracts:
                contract.enforcement = self.result.mode
                contract.source_evidence = "unverified: audit or failed selected gate"
                contract.freshness = "no successful checked claim"
                contract.behavior = "unverified behavior; no certified effect bound"
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
