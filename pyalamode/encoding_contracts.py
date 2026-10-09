"""Detached static contracts for exactly two explicit stable value codecs."""

ENCODING_VERSION = "pyalamode.encoding-v1"
ENCODING_NAMES = frozenset({"value_encode", "value_decode"})
ENCODING_FOUNDATIONS = {
    "builtins": frozenset({"type", "object", "tuple", "list", "set", "dict", "frozenset", "len", "range", "enumerate", "zip", "any", "all", "sorted", "id", "ord", "chr", "str", "bytes", "int", "bool", "next", "Ellipsis", "TypeError", "ValueError", "AttributeError", "RecursionError", "__build_class__", "__import__"}),
    "types": frozenset({"GenericAlias", "MemberDescriptorType", "GetSetDescriptorType", "MappingProxyType"}),
}
_BOUNDS = {
    "wire_bytes": 1048576, "schema_bytes": 65536, "schema_nodes": 1024,
    "value_nodes": 16384, "root_depth": 0, "maximum_depth": 32,
    "container_items": 4096, "record_case_fields": 128, "domain_cases": 128,
    "bytes_atom": 262144, "string_code_points": 65536,
    "nominal_identity_code_points": 1024, "field_case_name_code_points": 128,
    "integer_minimum": -(2 ** 63), "integer_maximum": 2 ** 63 - 1,
}
_VOCABULARY = ["None", "bool", "int", "str", "bytes", "fixed/homogeneous exact tuple",
               "Vector[T]", "OrderedMap[K,V]", "Map[K,V]", "Set[T]", "exact product record",
               "closed product domain/case", "Option[T]", "Result[T,E]", "Some[T]", "Nothing", "Ok[T]", "Err[E]"]
_FOUNDATIONS = ["builtins." + name for name in sorted(ENCODING_FOUNDATIONS["builtins"])] + [
    "types.GenericAlias exact native origin/args", "types.MemberDescriptorType exact name/objclass/get/set",
    "types.GetSetDescriptorType direct builtin type dictionary/qualname/name metadata reads",
    "types.MappingProxyType exact class metadata lookup", "type.__getattribute__", "object.__new__",
    "exact int arithmetic/comparison/shifts/bit operations", "exact str ordinal iteration/index/comparison/join/split/isidentifier/startswith",
    "exact bytes index/slice/construction/comparison", "exact tuple/list/set private traversal/construction/append/extend/add/remove",
    "pyalamode.collections exact classes/descriptor owners", "pyalamode.records._RECORDS fixed identity/field rows",
    "pyalamode.variants._VARIANTS/_CASES fixed closed-domain/case rows and Option/Result identities",
    "complete inherited collection/record/domain native and product foundations",
]


def operation_contract(name):
    if type(name) is not str:
        return None
    if name.startswith("encoding."):
        name = name[len("encoding."):]
    if name not in ENCODING_NAMES:
        return None
    encode = name == "value_encode"
    return {
        "identity": "pyalamode.encoding." + name, "version": ENCODING_VERSION,
        "runtime": "CPython 3.13.1 standard GIL macOS arm64/Linux aarch64 UTF8/surrogateescape",
        "signature": "(value:T, schema:T, /)->bytes" if encode else "(data:bytes, schema:T, /)->T",
        "inputs": ["exact recursively selected T" if encode else "exact bytes", "explicit resolved existing exact data schema T"],
        "output": "exact bytes" if encode else "exact recursively selected T",
        "schema_vocabulary": list(_VOCABULARY), "bounds": dict(_BOUNDS), "effects": [],
        "failures": ["ValueError", "RecursionError"], "ordinary_invalid_inputs": ["TypeError"],
        "behavior": "PALV1 bounded tagged binary with complete nominal/structural schema; signed64 exact integers; bool distinct; all string code points including surrogates; raw bytes; canonical homogeneous scalar Map/Set order; tuple/Vector/OrderedMap order preserved; exact end-of-input; no default filling",
        "implicit_dispatch": "identity admission before metadata; exact native slots only; object.__new__ bypasses user new/init/setters; custom product/MRO finalizers refuse before allocation; no imports, constructors, eval, restoration, arbitrary protocols or codec/error registry",
        "aliases": "no mutable alias or live view; decoding allocates fresh product storage; repeated references expand by value; immutable native scalars may be reused",
        "initialization": {"effects": [], "failures": [], "evidence": "trusted finite product imports/definitions; no application lookup, callback, environmental observation or external backend", "application_import": "separate ordinary initialization remains unchecked"},
        "nominal_compatibility": "exact module:qualified and complete recursive structural descriptor; nonempty dotted identifiers; local classes unsupported; duplicate admitted labels refuse; no incoming symbolic identity resolves/imports an object",
        "preconditions": ["unchanged registered classes/catalogs/module/qualname/native descriptors and dependencies", "selected exact schema and admitted data", "no unchecked product or interpreter modification"],
        "metadata_limit": "record catalog has no captured original module:qualname; unchecked relabel to unused valid label violates dependencies and is not universally detected",
        "roundtrip": "decode(encode(v,T),T) is exact contract-equivalent; encode(decode(b,T),T)==b for accepted canonical b; no identity preservation",
        "phase": "checked function body only; functional initialization/defaults and first-class schemas excluded",
        "evidence": "trusted product implementation, complete exact installed source identities in product_artifacts; no runtime certificate service",
        "foundations": list(_FOUNDATIONS), "approval": "product-shipped closed foundation; inherited/external assumptions remain visible",
        "owner": "Pyalamode product", "rationale": "finite invoice and immutable domain data interchange; byte transport retains separate effects",
    }


def operation_catalog():
    return [operation_contract(name) for name in sorted(ENCODING_NAMES)]
