"""Serializable checker results shared by CLI and future editor integrations."""

from dataclasses import asdict, dataclass, field
from typing import Any
import hashlib
from pathlib import Path

CHECKER_VERSION = "collections-3.0"
EDITION = "python-v1"
TARGET = "cpython-3.13.1"
OPERATION_VERSION = "scalar-tuple-call-collection-ops-3"
SCALARS = frozenset({"None", "bool", "int", "str", "bytes"})


def foundation_identities() -> dict[str, str]:
    """Actual installed product bytes, so labels alone cannot keep old evidence fresh."""
    directory = Path(__file__).resolve().parent
    return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in ("__init__.py", "collections.py", "model.py", "checker.py", "project.py", "cli.py")}

RULES = {
    "PAL001": ("tooling failure", "Repair the source path, encoding, syntax, policy, or output destination and retry."),
    "PAL002": ("unsupported target", "Use the published CPython 3.13.1 standard-build macOS/Linux target."),
    "PAL101": ("binding already initialized", "Derive a new local name; exclusive branches can initialize one name once."),
    "PAL102": ("binding not initialized on every path", "Initialize the name in every continuing branch before using it."),
    "PAL110": ("unsupported statement or binding", "Extract scalar decision logic using simple assignments, if, return, and pass."),
    "PAL120": ("unsupported declaration", "Use module mode or a resolved @fun, checked nested functions, and stable supported defaults."),
    "PAL121": ("misplaced module directive", "Place # mode: fun after the optional shebang, encoding declaration and docstring, before executable statements."),
    "PAL130": ("annotation contract unknown", "Use explicit exact scalars, recursive tuple/product collection types, or fixed Callable contracts; Map keys and Set elements require exact scalar domains. Annotation expressions are never evaluated."),
    "PAL201": ("unsupported expression", "Use the published exact scalar, tuple, collection and checked callable expression contracts; move uncharacterized integration to ordinary Python."),
    "PAL210": ("operation operand contract not established", "Supply the exact operand types in the published operation contract; no coercion is implicit."),
    "PAL211": ("return contract not established", "Return the declared recursively exact admitted data or checked callable contract on every completing path."),
    "PAL221": ("input contract not established", "Supply values with established recursively exact data schemas and actual checked callable/capture evidence; ordinary unknown inputs remain caller obligations."),
    "PAL230": ("call target unknown or unsupported", "Use a resolved checked callable or an unchanged approved builtin with its supported signature."),
    "PAL240": ("dependency binding is not approved", "Use statically established stable values/callables and leave dependency bindings unchanged."),
    "PAL241": ("module initialization is not characterized", "Use supported stable initialization and import only characterized foundations or checked functional modules."),
    "PAL250": ("persistent update result ignored", "Bind or return the new collection value; persistent updates preserve the receiver."),
}


@dataclass(frozen=True)
class Diagnostic:
    rule: str
    path: str
    line: int
    column: int
    boundary: str
    origin: str
    reason: str
    remediation: str
    first_binding: str | None = None

    def format(self) -> str:
        first = f"\n  first binding: {self.first_binding}" if self.first_binding else ""
        return (f"{self.path}:{self.line}:{self.column}: {self.rule}: {self.reason} "
                f"[{self.boundary}; {self.origin}]{first}\n  {self.remediation}")


@dataclass
class FunctionContract:
    name: str
    path: str
    line: int
    parameters: dict[str, str]
    returns: str | None
    parameter_kinds: dict[str, str] = field(default_factory=dict)
    enforcement: str = "strict"
    behavior: str = "pure"
    source_evidence: str = "checked participating source"
    trust: list[str] = field(default_factory=lambda: ["CPython 3.13.1 standard scalar, tuple, function and annotation operations", "pyalamode.fun identity marker"])
    failures: list[str] = field(default_factory=list)
    freshness: str = "current for recorded inputs"
    boundary_protection: str = "unguarded"
    caller_obligations: list[str] = field(default_factory=list)
    defaults: dict[str, str] = field(default_factory=dict)
    captures: dict[str, str] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)
    callable_targets: dict[str, list[str]] = field(default_factory=dict)
    callable_defaults: dict[str, list[str]] = field(default_factory=dict)
    return_callable_targets: list[str] = field(default_factory=list)
    definition_failures: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)


@dataclass
class CheckResult:
    path: str
    fingerprint: str
    diagnostics: list[Diagnostic] = field(default_factory=list)
    contracts: list[FunctionContract] = field(default_factory=list)
    eligible_functions: int = 0
    selected_functions: int = 0
    analyzed_call_sites: int = 0
    cache_hit: bool = False
    mode: str = "strict"
    module_mode: bool = False
    initialization_evidence: str = "unchecked ordinary module initialization"
    dependencies: dict[str, str] = field(default_factory=dict)
    initialization_failures: list[str] = field(default_factory=list)
    binding_context: list[str] = field(default_factory=list)

    @property
    def verified(self) -> bool:
        return self.mode == "strict" and not self.diagnostics

    @property
    def status(self) -> int:
        if any(d.rule in {"PAL001", "PAL002"} for d in self.diagnostics):
            return 2
        return int(bool(self.diagnostics) and self.mode == "strict")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["verified"] = self.verified
        value["status"] = self.status
        return value


def diagnostic(rule: str, path: str, reason: str, *, line: int = 1,
               column: int = 1, boundary: str = "<module>", origin: str = "static source",
               first_binding: str | None = None) -> Diagnostic:
    return Diagnostic(rule, path, line, column, boundary, origin, reason, RULES[rule][1], first_binding)
