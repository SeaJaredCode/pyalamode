"""Serializable checker results shared by CLI and future editor integrations."""

from dataclasses import asdict, dataclass, field
from typing import Any
import hashlib
from pathlib import Path
import sys

CHECKER_VERSION = "experimental-syntax-14.0"
EDITION = "python-v1"
EXPERIMENTAL_EDITION = "pyalamode-v1-experimental"
SYNTAX_VERSION = "pyalamode.syntax-v1"
SOURCE_MAP_SCHEMA = 1
TARGET = "cpython-3.13.1"
OPERATION_VERSION = "scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-encoding-distribution-builder-task-syntax-ops-14"
SCALARS = frozenset({"None", "bool", "int", "str", "bytes"})


def runtime_environment() -> dict:
    return {"filesystem_encoding": sys.getfilesystemencoding(), "filesystem_errors": sys.getfilesystemencodeerrors(),
            "utf8_mode": sys.flags.utf8_mode}


def foundation_identities() -> dict[str, str]:
    """Actual installed product bytes, so labels alone cannot keep old evidence fresh."""
    directory = Path(__file__).resolve().parent
    return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in ("__init__.py", "integrations.py", "integration_contracts.py", "standard.py", "standard_contracts.py", "variants.py", "failures.py", "effects.py", "collections.py", "records.py", "boundaries.py", "guardgen.py", "model.py", "checker.py", "project.py", "cli.py", "editor.py", "migration.py", "migration_views.py", "distribution.py", "encoding.py", "encoding_contracts.py", "builders.py", "builder_contracts.py", "tasks.py", "task_contracts.py", "syntax.py", "source_maps.py")}

RULES = {
    "PAL390": ("experimental source selection required", "Select pyalamode-v1-experimental and an actual whole-module # mode: fun directive for authored .pya source."),
    "PAL391": ("experimental display unsupported", "Use an admitted immutable display or an actual direct annotated Vector/Map empty initializer; comprehensions and mutation remain unsupported."),
    "PAL392": ("experimental compiler name collision", "Keep val and compiler-private constructor bindings reserved; use a fresh ordinary authored binding."),
    "PAL382": ("characterized tasks disabled", "Explicitly opt into tasks=true after reviewing the finite synchronous task, callback, capture and scheduling contract."),
    "PAL380": ("confined construction disabled", "Use immutable construction or explicitly opt into builders=true after reviewing the finite confinement contract."),
    "PAL381": ("confined construction lifetime or escape unsupported", "Keep one fresh lexical callback parameter, direct append/extend statements and automatic finalization; builders and construction callbacks cannot be aliased, retained or transferred."),
    "PAL001": ("tooling failure", "Repair the source path, encoding, syntax, policy, or output destination and retry."),
    "PAL002": ("unsupported target", "Use the published CPython 3.13.1 standard-build macOS/Linux target."),
    "PAL101": ("binding already initialized", "Derive a new local name; exclusive branches can initialize one name once."),
    "PAL102": ("binding not initialized on every path", "Initialize the name in every continuing branch before using it."),
    "PAL110": ("unsupported statement or binding", "Use the published finite initialization, if/return, exact match, characterized try/except and borrow statements."),
    "PAL120": ("unsupported declaration", "Use module mode or a resolved @fun, checked nested functions, and stable supported defaults."),
    "PAL121": ("misplaced module directive", "Place # mode: fun after the optional shebang, encoding declaration and docstring, before executable statements."),
    "PAL130": ("annotation contract unknown", "Use explicit exact scalars, recursive tuple/product collection/record/variant/Option/Result types, or fixed Callable contracts; Map keys and Set elements require exact scalar domains. Annotation expressions are never evaluated."),
    "PAL201": ("unsupported expression", "Use the published exact scalar, tuple, collection, record, closed-domain and checked callable expression contracts; move uncharacterized integration to ordinary Python."),
    "PAL210": ("operation operand contract not established", "Supply the exact operand types in the published operation contract; no coercion is implicit."),
    "PAL211": ("return contract not established", "Return the declared recursively exact admitted data or checked callable contract on every completing path."),
    "PAL221": ("input contract not established", "Supply values with established recursively exact data schemas and actual checked callable/capture evidence; ordinary unknown inputs remain caller obligations."),
    "PAL230": ("call target unknown or unsupported", "Use a resolved checked callable or an unchanged approved builtin with its supported signature."),
    "PAL240": ("dependency binding is not approved", "Use statically established stable values/callables and leave dependency bindings unchanged."),
    "PAL241": ("module initialization is not characterized", "Use supported stable initialization and import only characterized foundations or checked functional modules."),
    "PAL310": ("effect bound exceeded", "Declare the characterized effect at the receiving boundary within project policy, or pass stable data to a pure calculation. Effect names never authorize unknown operations."),
    "PAL320": ("capability lifetime or escape unsupported", "Use an exact capability parameter or the finite borrow scope; lend it only to checked capability slots. Capabilities cannot be data, aliases, defaults, captures or returned values."),
    "PAL330": ("pattern coverage or binding unsupported", "Use unchanged exact product cases/records with fresh irrefutable captures and explicit complete case coverage or a policy-permitted wildcard."),
    "PAL340": ("failure handler contract unsupported", "Use unchanged characterized builtin categories and opaque handler-local exception targets only through failure_value; exception state and arbitrary cleanup remain unsupported."),
    "PAL350": ("external operation approval is not current", "Review the exact operation contract and installed dependency identity, then record explicit owner/rationale/provenance approval within its expiry; drafts and stale approvals cannot admit."),
    "PAL351": ("unsafe ordinary adapter declaration unsupported", "Use an ordinary @unsafe(scope=nonempty_text,rationale=nonempty_text) adapter outside participating code; explicitly snapshot and validate output before a new checked computation."),
    "PAL250": ("persistent update result ignored", "Bind or return the new collection or record value; persistent updates preserve the receiver."),
    "PAL370": ("checked dependency evidence not current", "Rebuild and reinstall the exact checked distribution, then check under current consumer policy."),
    "PAL371": ("checked export unavailable", "Use an explicitly published current strict export of the declared checked dependency."),
    "PAL372": ("installed dependency changed during gate", "Restore stable installed inputs and recheck before building."),
    "PAL360": ("new reviewed audit debt", "Review each new normalized finding; fixing other debt does not offset it."),
    "PAL361": ("strict coverage requirement failed", "Restore the selected boundary or satisfy the exact current required export."),
    "PAL362": ("new external trust assumption", "Review the actual operation, contract and installed dependency identities."),
    "PAL363": ("effect coverage expanded", "Review declared and required effects separately at the affected boundary."),
    "PAL364": ("configured approval expired", "Review and renew the exact configured approval; a baseline cannot waive current expiry."),
    "PAL365": ("unsafe adapter changed", "Review the ordinary adapter scope and behavior outside checked source."),
    "PAL366": ("migration identity requires review", "Resolve duplicate or unavailable current identities; explicitly review ambiguous historical relocation."),
    "PAL367": ("team policy protection weakened", "Review the explicit policy change independently of finding totals."),
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
    end_line: int | None = None
    end_column: int | None = None
    column_encoding: str = "utf-8-bytes"
    dependency_context: dict | None = None

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
    data_assertions: list[dict] = field(default_factory=list)
    callable_capture_evidence: dict[str, dict] = field(default_factory=dict)
    return_callable_evidence: dict | None = None
    invoked_targets: list[str] = field(default_factory=list)
    callable_dependencies: list[str] = field(default_factory=list)
    callable_arguments: dict[str, list[str]] = field(default_factory=dict)
    callable_operations: list[str] = field(default_factory=list)
    effect_bound: list[str] = field(default_factory=list)
    required_effects: list[str] = field(default_factory=list)
    effect_origins: dict[str, list[str]] = field(default_factory=dict)
    capability_parameters: dict[str, dict] = field(default_factory=dict)
    borrow_scopes: list[dict] = field(default_factory=list)
    failure_edges: list[dict] = field(default_factory=list)
    direct_failures: list[str] = field(default_factory=list)
    patterns: list[dict] = field(default_factory=list)
    handlers: list[dict] = field(default_factory=list)
    operation_contracts: list[dict] = field(default_factory=list)
    callable_default_evidence: dict[str, dict] = field(default_factory=dict)
    external_assumptions: list[dict] = field(default_factory=list)
    builder_scopes: list[dict] = field(default_factory=list)
    task_scopes: list[dict] = field(default_factory=list)


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
    records: list[dict] = field(default_factory=list)
    variants: list[dict] = field(default_factory=list)
    setup_observations: list[dict] = field(default_factory=list)
    unsafe_adapters: list[dict] = field(default_factory=list)
    integration_inputs: dict[str, dict] = field(default_factory=dict)
    source_provenance: dict | None = None

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
               first_binding: str | None = None, end_line: int | None = None,
               end_column: int | None = None, column_encoding: str = "utf-8-bytes", dependency_context: dict | None = None) -> Diagnostic:
    return Diagnostic(rule, path, line, column, boundary, origin, reason, RULES[rule][1], first_binding,
                      end_line, end_column, column_encoding, dependency_context)
