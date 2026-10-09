"""Static-only versioned operation metadata; never a callable purity registry."""

STANDARD_VERSION = "pyalamode.standard-v1"
STANDARD_NATIVE = {
    "builtins": frozenset({"type", "int", "str", "bytes", "len", "ord", "chr", "enumerate", "range", "tuple", "list", "object", "TypeError", "ValueError", "UnicodeEncodeError", "UnicodeDecodeError"}),
    "types": frozenset({"FunctionType"}),
}
SCALAR_SIGNATURES = {
    "text_split": (("str", "str"), "Vector[str]", ("ValueError",)),
    "text_join": (("Vector[str]", "str"), "str", ("RecursionError",)),
    "text_replace": (("str", "str", "str"), "str", ()),
    "text_startswith": (("str", "str"), "bool", ()),
    "text_slice": (("str", "int", "int"), "str", ()),
    "integer_clamp": (("int", "int", "int"), "int", ("ValueError",)),
    "integer_parse_decimal": (("str",), "int", ("ValueError",)),
    "integer_format_decimal": (("int",), "str", ("ValueError",)),
    "utf8_encode": (("str",), "bytes", ("UnicodeError",)),
    "utf8_decode": (("bytes",), "str", ("UnicodeError",)),
    "hex_encode": (("bytes",), "str", ()),
    "hex_decode": (("str",), "bytes", ("ValueError",)),
}
TOOLKIT_SIGNATURES = {
    "vector_scan": "(Vector[T], (A,T)->A, A, /)->Vector[A]; initial first, n+1 outputs, left-to-right",
    "vector_group_by": "(Vector[T], T->K, /)->OrderedMap[K,Vector[T]]; exact homogeneous scalar K, first-key-encounter order",
    "compose": "(B->R, A->B, /)->A->R; unary inner then outer; B/R data; construction invokes neither",
    "partial_first": "((A,B)->R, A, /)->B->R; A/R data; binds first argument, construction invokes no callback",
    "result_traverse": "(Vector[T], T->Result[U,E], /)->Result[Vector[U],E]; left-to-right fail-fast, empty Ok(empty)",
}
STANDARD_NAMES = frozenset(SCALAR_SIGNATURES) | frozenset(TOOLKIT_SIGNATURES)
_BEHAVIORS = {
    "text_split": "explicit nonempty separator; empty pieces retained in input order",
    "text_join": "exact Vector strings in input order; empty input produces empty text",
    "text_replace": "all nonoverlapping exact string replacements; empty old inserts at every boundary",
    "text_startswith": "exact prefix test; empty prefix is true",
    "text_slice": "unit-step half-open code-point slice; negative/clamped exact-int bounds",
    "integer_clamp": "inclusive exact integer bounds; ValueError if lower exceeds upper",
    "integer_parse_decimal": "manual ASCII [+-]?[0-9]{1,4096}; leading zeros allowed; no ambient decimal conversion limit",
    "integer_format_decimal": "manual canonical ASCII decimal; absolute value below 10**4096; no ambient formatter or decimal limit",
    "utf8_encode": "manual RFC3629, no BOM insertion/normalization; first consecutive surrogate span raises exact UnicodeEncodeError",
    "utf8_decode": "manual shortest-form RFC3629, no BOM removal; first malformed/truncated sequence raises exact UnicodeDecodeError",
    "hex_encode": "exactly two lowercase ASCII hex digits per byte in input order",
    "hex_decode": "even ASCII hex pairs only, either case; no whitespace, restoration or codec dispatch",
}
_INITIALIZATION = {
    "effects": [], "failures": [],
    "evidence": "trusted product definitions, fixed alphabets/integer bound and characterized product imports; no application callback or ambient observation",
    "application_import": "separate ordinary initialization is unchecked; a pure export never certifies its module import",
}
_FOUNDATIONS = ["builtins." + name for name in sorted(STANDARD_NATIVE["builtins"])] + [
    "types.FunctionType", "exact str.split/join/replace/startswith/subscription",
    "exact bytes.hex/fromhex/subscription", "exact int arithmetic/comparison/shifts/bit operations", "exact tuple/list private construction/iteration/append/reverse",
    "pyalamode.collections.Vector/OrderedMap/_invalid/_validate/_storage/_validate_key/_function/_new",
    "pyalamode.sums.Ok/Err exact construction and fixed payload slots",
    "complete inherited collections/records/oneofs native and product foundations",
]


def _initialization():
    return {key: list(value) if type(value) is list else value for key, value in _INITIALIZATION.items()}


def operation_contract(name):
    """Return detached serializable metadata, never runtime application objects."""
    if name.startswith("standard."):
        name = name[len("standard."):]
    invoking = name.endswith(".invoke")
    if invoking:
        name = name[:-len(".invoke")]
    if name in SCALAR_SIGNATURES:
        parameters, result, failures = SCALAR_SIGNATURES[name]
        return {"identity": "pyalamode.standard." + name, "version": STANDARD_VERSION,
                "runtime": "CPython 3.13.1 standard GIL macOS/Linux", "signature": "(" + ", ".join(parameters) + ", /)->" + result,
                "inputs": list(parameters), "output": result, "behavior": _BEHAVIORS[name], "effects": [], "failures": list(failures),
                "implicit_dispatch": "exact native/product scalar operations only; no foreign hooks, codec/error registries or restoration",
                "aliases": "immutable data may be reused; no retained mutable alias or live view", "initialization": _initialization(),
                "evidence": "trusted product implementation; exact source identities are in product_artifacts", "foundations": list(_FOUNDATIONS),
                "approval": "product-shipped closed foundation; external integration approvals remain deferred",
                "ordinary_invalid_inputs": ["TypeError"], "owner": "Pyalamode product", "rationale": "bounded exact standard data workflows"}
    if name in TOOLKIT_SIGNATURES or name == "Vector.fold":
        signature = TOOLKIT_SIGNATURES.get(name, "Vector[T].fold((A,T)->A, A, /)->A; left-to-right, empty initial")
        constructing = name in {"compose", "partial_first"} and not invoking
        return {"identity": "pyalamode.standard." + name if name != "Vector.fold" else "pyalamode.Vector.fold", "version": STANDARD_VERSION,
                "runtime": "CPython 3.13.1 standard GIL macOS/Linux", "signature": signature,
                "inputs": "exact data and resolved fixed callable contracts with stable captures", "output": "exact data or characterized returned wrapper",
                "behavior": signature, "phase": "invocation" if invoking else "construction" if constructing else "eager invocation", "effects": [] if constructing else ["callback effect-bound union"],
                "failures": ["RecursionError"] if name == "partial_first" else [] if constructing else ["RecursionError", "callback raised-failure bounds"],
                "invocation_effects": ["callback declared/required effects; never discharged by provider substitution or failure handling"],
                "invocation_failures": ["RecursionError", "callback raised-failure bounds"],
                "implicit_dispatch": "exact FunctionType callback with actual checked evidence; no arbitrary callable/iterator/key protocol",
                "aliases": "stable callback captures and bound data retained; no capability retention; eager immutable result storage",
                "initialization": _initialization(), "evidence": "trusted product helper plus actual callback target/capture evidence",
                "foundations": list(_FOUNDATIONS), "ordinary_invalid_inputs": ["TypeError"], "owner": "Pyalamode product",
                "approval": "product-shipped foundation, callback assumptions remain visible", "rationale": "bounded eager ordered algorithms"}
    capability = {
        "IOCapability.read_text": (["str"], "str", "IO", ["OSError", "UnicodeError", "ValueError", "RuntimeError", "KeyError"]),
        "IOCapability.write_text": (["str", "str"], "None", "IO", ["OSError", "UnicodeError", "ValueError", "RuntimeError", "KeyError"]),
        "ClockCapability.now_ns": ([], "int", "Clock", ["RuntimeError", "OSError", "IndexError"]),
        "EnvironmentCapability.get": (["str", "str"], "str", "Environment", ["RuntimeError", "ValueError", "OSError", "UnicodeError"]),
    }.get(name)
    if capability:
        inputs, output, effect, failures = capability
        return {"identity": "pyalamode." + name, "version": STANDARD_VERSION, "runtime": "CPython 3.13.1 standard GIL macOS/Linux",
                "signature": "(" + ", ".join(inputs) + ", /)->" + output, "inputs": inputs, "output": output, "effects": [effect], "failures": failures,
                "behavior": "effects-v1 exact opaque interface and lease; UTF8 filesystem encoding/surrogateescape errors required; roots/paths/environment names reject every surrogate code point; controlled providers retain effects; rooted binary whole-file IO uses manual UTF8; write truncates before encoding and can fail non-atomically",
                "implicit_dispatch": "finite exact capability/provider operations, characterized native read/write/close/path/clock/environment",
                "aliases": "capability borrowed for invocation only; stable return data; no live views or transfer",
                "initialization": {"evidence": "provider setup is ordinary unchecked source and separately reported", "effects": ["IO"] if effect == "IO" else []},
                "foundations": ["complete effects-v1 OS/provider/lease/native inventory", "standard.utf8_encode/decode and complete standard foundations", "builtins.open", "_io.BufferedReader/BufferedWriter/FileIO read/write/context/close", "time.time_ns", "os.environ exact UTF8/surrogateescape native branch", "sys.getfilesystemencoding/getfilesystemencodeerrors/flags"],
                "evidence": "trusted product effects/standard implementations; actual identities in product_artifacts", "owner": "Pyalamode product", "rationale": "finite effectful shell",
                "approval": "product-shipped foundation; required family and project effect policy remain mandatory", "ordinary_invalid_inputs": ["TypeError"]}
    return None


def operation_catalog():
    names = sorted(STANDARD_NAMES) + ["Vector.fold", "IOCapability.read_text", "IOCapability.write_text", "ClockCapability.now_ns", "EnvironmentCapability.get"]
    return [operation_contract(name) for name in names]


def setup_contract(name):
    effects = ["IO"] if name == "live_io" else []
    failures = ["ValueError", "OSError", "RuntimeError"] if name == "live_io" else ["RuntimeError"] if name == "live_environment" else ["ValueError"] if name.startswith("recorded_") else []
    return {"identity": "pyalamode." + name, "version": STANDARD_VERSION, "effects": effects, "failures": failures,
            "evidence": "statically recognized ordinary provider setup; surrounding ordinary initialization/body is unchecked",
            "behavior": "live_io observes realpath/existing-directory filesystem state; live IO/environment setup requires UTF8 filesystem encoding/surrogateescape errors; caller roots/paths/names reject every surrogate code point; other live factories allocate without sampling; recorded factories validate explicit tuples; later interface invocation retains its family",
            "aliases": "fresh opaque provider with private mutable state; no stable data claim", "policy": "refused in functional initialization/defaults; ordinary shell only"}
