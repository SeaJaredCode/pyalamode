"""Detached static rows for exactly three confined Vector operations.

Names and rows carry no permission or callable-purity certificate. The checker
must establish lexical ownership and callback evidence under current policy.
"""

BUILDER_VERSION = "pyalamode.builders-v1"
BUILDERS_NAMES = frozenset({"vector_build", "VectorBuilder"})
BUILDERS_FOUNDATIONS = {
    "builtins": frozenset({"type", "object", "tuple", "list", "bool", "int", "str", "classmethod", "sorted", "frozenset",
                           "TypeError", "RuntimeError", "AttributeError", "__build_class__", "__import__"}),
    "types": frozenset({"GenericAlias", "FunctionType"}),
    "_thread": frozenset({"get_ident"}),
}
_ALIASES = {
    "vector_build": "vector_build", "builders.vector_build": "vector_build",
    "pyalamode.builders.vector_build": "vector_build",
    "VectorBuilder.append": "VectorBuilder.append", "builders.VectorBuilder.append": "VectorBuilder.append",
    "pyalamode.builders.VectorBuilder.append": "VectorBuilder.append",
    "VectorBuilder.extend": "VectorBuilder.extend", "builders.VectorBuilder.extend": "VectorBuilder.extend",
    "pyalamode.builders.VectorBuilder.extend": "VectorBuilder.extend",
}
_OPERATIONS = ("vector_build", "VectorBuilder.append", "VectorBuilder.extend")
_FOUNDATIONS = tuple("builtins." + name for name in sorted(BUILDERS_FOUNDATIONS["builtins"])) + (
    "types.GenericAlias exact native construction", "types.FunctionType exact callback admission",
    "_thread.get_ident private owner token bookkeeping", "object.__new__/__getattribute__/__setattr__ exact fixed slots",
    "exact bool/int token shape/comparison", "exact list append/extend/clear and tuple reference copy",
    "pyalamode.collections.Vector/_function/_invalid/_validate/_storage/_new",
    "complete inherited collection/record/domain native and product foundations",
)


def operation_contract(name):
    if type(name) is not str:
        return None
    operation = _ALIASES.get(name)
    if operation is None:
        return None
    construction = operation == "vector_build"
    append = operation == "VectorBuilder.append"
    return {
        "identity": "pyalamode.builders." + operation, "version": BUILDER_VERSION,
        "runtime": "CPython 3.13.1 standard GIL macOS arm64/Linux aarch64 UTF8/surrogateescape",
        "signature": "(VectorBuilder[T]->None, /)->Vector[T]" if construction else "(T, /)->None" if append else "(Vector[T], /)->None",
        "inputs": ["one exact FunctionType with checked pure lexical construction evidence"] if construction else ["exact recursively stable T"] if append else ["exact Vector of recursively stable T"],
        "output": "exact Vector[T] after invalidation and cleanup" if construction else "exact None",
        "effects": [], "failures": ["RecursionError", "callback raised-failure bounds"] if construction else ["RecursionError"],
        "ordinary_invalid_inputs": ["TypeError", "RuntimeError"],
        "behavior": "one fresh builder; callback once; exact None completion; final result validation; all exits revoke before clear; failure publishes no result" if construction else "validate append.value before staging one reference; exact None return" if append else "validate complete extend.values before staging its ordered tuple references; exact None return",
        "ordering": "Python call/argument and statement order; Vector/tuple/OrderedMap input order; inherited canonical homogeneous scalar Map/Set nested validation/error selection",
        "callback": {"count": 1 if construction else 0, "effects": [], "source_contract": "one undecorated direct nested def, one fresh VectorBuilder[T] parameter, explicit None return, consumed once; no aliases/captures/storage/transfer/concurrent use; stable ordinary captures allowed"},
        "lifetime": "fresh callback invocation; invalidated on every exit; no alias, retention or transfer",
        "finalization": "automatic exact Vector result after None; construction failure publishes no result",
        "implicit_dispatch": "exact FunctionType only; no annotation/default/capture inspection or runtime purity inference; exact data admission before storage reads; no arbitrary iterator/getter/hash/equality/representation/conversion hooks under unchanged inherited dependencies",
        "aliases": "one private staging list, copied to one new immutable outer tuple; stable nested values may be reused; retained builders/methods expire; ordinary independent calls receive distinct fresh tokens",
        "initialization": {"effects": [], "failures": [], "evidence": "trusted finite product/native imports, definitions and constants; no application lookup/callback, thread sample, environment observation or external backend", "application_import": "separate ordinary application initialization remains unchecked"},
        "generic_arguments": "T is statically established and runtime-erased; ordinary runtime enforces deep data invariants, not annotation-selected T",
        "phase": "checked function body only with builders=true; designated construction callback only; no functional initialization/defaults or first-class builder schemas",
        "bounds": {"active_builder_parameters": 1, "callback_invocations": 1, "value_quotas": "inherited collections; no new cardinality/integer/string/depth quota or termination/resource guarantee"},
        "complexity": "amortized O(1) append staging / O(m) extend staging plus nested ingress validation; O(n) final tuple copy/clear plus final nested validation and callback work; O(n) staging/final references, inherited recursive/canonical/catalog costs",
        "preconditions": ["exact admitted data and actual callback signature/purity/stable-capture/lexical ownership evidence", "unchanged product classes, fixed catalogs, helpers, module/class/native dependencies", "no unchecked private storage/token or interpreter modification; supported standard GIL runtime"],
        "evidence": "trusted product implementation and actual callback/source evidence; exact installed source identities in product_artifacts; no runtime certificate service or callback registry",
        "foundations": list(_FOUNDATIONS), "approval": "product-shipped closed foundation; builders policy and inherited/external assumptions remain separately visible",
        "owner": "Pyalamode product", "rationale": "finite bulk assembly from ordered stable vectors without public intermediate mutable values",
    }


def operation_catalog():
    return [operation_contract(name) for name in _OPERATIONS]
