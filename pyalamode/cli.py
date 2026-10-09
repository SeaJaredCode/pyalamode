"""Local static check/build and finite contract explanations."""

import argparse
import json
from .model import RULES, TARGET
from .project import build_paths, check_paths


def _show(result, structured: bool) -> None:
    if structured:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return
    for item in result.tooling:
        print(item.format())
    for file in result.results:
        for item in file.diagnostics:
            print(item.format())
    data = result.to_dict()
    coverage = data["coverage"]
    selected = coverage["selected_functions"]
    if result.audit:
        print(f"Audit: {selected} selected / {coverage['eligible_functions']} eligible functions; no strict certificate.")
    elif result.status:
        print("Verification failed; no successful checked claim.")
    else:
        modules = sum(file.module_mode for file in result.results)
        records = coverage['selected_records']
        print(f"Strict gate passed: {selected} selected functions, {records} record declarations and {modules} functional modules; ordinary shells and ordinary initialization are unchecked.")
        if not selected:
            print("No participating functions were selected; module initialization coverage is reported separately.")
    if result.output:
        print(f"Built ordinary Python source: {result.output}")
    for boundary in result.guarded_exports:
        state = "generated" if boundary["generated"] else "selected for build"
        print(f"Guarded public boundary {boundary['public_boundary']} ({state}); original {boundary['original_boundary']}: {boundary['original_protection']}.")
    if result.boundary_guards == "debug":
        print(f"Debug data assertions: {len(result.debug_coverage)} selected functions; exact supported parameters, local data bindings and returns; callable evidence remains a caller obligation.")
    print(f"{coverage['analyzed_call_sites']} checked or resolved ordinary caller sites inspected; elapsed {result.elapsed_seconds:.6f}s.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pyalamode", description="Statically check functional modules and the closed immutable subset of ordinary Python.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "build"):
        command = commands.add_parser(name)
        command.add_argument("paths", nargs="*", help="Python files/directories; default is current project")
        command.add_argument("--target", default=TARGET)
        command.add_argument("--json", action="store_true", help="structured report")
        command.add_argument("--root", help="project root for policy and cache")
        if name == "check":
            command.add_argument("--audit", action="store_true", help="report findings without strict evidence")
            command.add_argument("--no-cache", action="store_true")
        else:
            command.add_argument("--output", help="fresh output directory; default build/pyalamode")
    explanation = commands.add_parser("explain", help="describe a stable rule or scalar operation")
    explanation.add_argument("symbol")
    args = parser.parse_args(argv)
    if args.command == "explain":
        symbol = args.symbol.upper()
        if symbol in RULES:
            title, remediation = RULES[symbol]
            print(f"{symbol}: {title}\n{remediation}")
            if symbol == "PAL101":
                print("Example rejected: x = 1; x = 2. Exclusive if/else bindings are permitted.")
            return 0
        operations = {
            "abs": "abs(exact int) -> exact int; one positional argument.",
            "len": "len(exact str, bytes, recursively admitted tuple, Vector, OrderedMap, Map or Set) -> exact int; one positional argument.",
            "min": "min(two or more exact int, str, or bytes of one type) -> same type; no iterable/key/default forms.",
            "max": "max(two or more exact int, str, or bytes of one type) -> same type; no iterable/key/default forms.",
            "fun": "Runtime identity marker. Execution adds no checked evidence and performs no input validation.",
            "record": "@record declares an exact fixed record with public typed data fields and stable defaults; required fields precede defaults. Constructor positional/keyword inputs and defaults undergo deep exact schema validation; fields cannot be reassigned/deleted. No bases, metaclasses, descriptors, methods, custom validators/constructors, callable fields, forward/recursive record declarations or static record patterns in M4. Runtime __match_args__ supports ordinary Python matching; static patterns arrive in M6. Equality includes exact record identity and recursively equivalent field values; records are unhashable.",
            "replace": "replace(exact_record, **explicit_known_field_changes) returns a new validated exact record, preserving prior versions. Strict calls use only known field keywords and admitted nested data; an ignored replacement is PAL250. Recursive validation may raise RecursionError under valid contracts; invalid ordinary inputs raise TypeError with a path.",
            "freeze": "Ordinary shell freeze(value, *, exclusive=False, adapter=None, schema=None): closed exact list -> Vector, tuple -> tuple, dict -> OrderedMap, scalar set/frozenset -> Set, admitted stable data -> validated reuse. Explicit exclusive=True asserts caller-held exclusive access for recursively mutable or unknown source data; the library does not detect ownership or lock concurrent writers. Missing preconditions, subclasses, cycles, hooks and views fail. Explicit schema=Vector[int]/closed schema establishes supported output shape for analyzed simple ordinary assignments and subsequent checked calls. Conversions certify the output data, not preceding shell/provider behavior; no strict pure-body/default/initializer conversion contract.",
            "thaw": "Ordinary shell thaw(admitted_data) creates independent fresh mutable integration containers: Vector/tuple -> list, Map/OrderedMap -> dict, Set -> set, records -> dict of fields, scalars reuse. Nested exports never retain a mutable alias into the source; no arbitrary restoration/constructor hooks. Not admitted in strict pure functions.",
            "dataclass_adapter": "dataclass_adapter(ExactOrdinaryDataclass, ExactTargetRecord): named finite compatibility qualifier for direct ordinary generated storage/behavior, stable defaults, no factories/custom hooks/subclasses. freeze(source, adapter=adapter, exclusive=True, schema=TargetRecord) recursively snapshots fields into the exact target schema. frozen=True alone never qualifies source behavior/data; the foreign object is not strict data.",
            "namedtuple_adapter": "namedtuple_adapter(ExactGeneratedNamedTuple, ExactTargetRecord): named ordinary-shell qualifier, generated fixed storage/behavior only; no custom getters/constructors/subclasses. Snapshot produces validated concrete product record fields; foreign named tuples do not become admitted strict objects.",
            "guards": "Policy boundary_guards=off (default), exports, or debug; guarded_exports=['module:function'] selects exact top-level public boundaries. Build generates normally importable pyalamode_exports.module:function aliases; original functions stay unwrapped in exports mode and internal direct calls have no repeated guards. Selected guards validate exact deep arguments before body and returns after; Callable, Effectful and capability boundaries are refused. Debug adds finite supported parameter/local/return data assertions to copied source, with documented overhead; it does not prove effects, callback purity, ownership or dependency identity.",
            "tuple": "Exact recursive tuple[T1, T2], homogeneous tuple[T, ...], or empty tuple[()]; immutable data only, no subclasses or callable payloads. Fixed tuples use literal indexes/slices; homogeneous tuples admit exact int indexes/slices. Equality and len are characterized; iteration remains unsupported.",
            "effects": "@effects(IO,State,Clock,Random,Environment) is an identity declaration factory selecting checked effectful source; unique finite tokens only, optionally with @fun. Declared upper bounds and required operation/callback effect unions remain distinct; Task is reserved. Unknown operations remain refused. Initialization/provider construction remains ordinary-shell setup; no runtime registry or purity validation.",
            "Effectful": "Effectful[[T1,...],R,Clock,...]: fixed positional callable upper bound; concrete target bounds must be subsets, conditional alternatives union their bounds and finite failures. Exact capability slots require the corresponding effect family; captures/defaults/results cannot retain capabilities. Pure Callable retains an empty effect bound.",
            "borrow": "with borrow(exact_local_capability) as fresh_name: one characterized logical lease; supports finite nested borrowing and invocation lending to exact checked capability slots. View invalidates on every exit, including return/body failure; it does not expose a persistent OS reader. Capabilities cannot be data, aliases, global constants, defaults, callable captures or stable returned values. Factory setup and resource ownership remain ordinary caller obligations.",
            "capabilities": "Finite exact interfaces: IOCapability.read_text(str)->str/write_text(str,str)->None; StateCapability.get()->int/set(int)->None; ClockCapability.now_ns()->int; RandomCapability.below(int)->int; EnvironmentCapability.get(str,str)->str. Each retains its family for live/recorded providers. IO whole-path operations use internal open/read-or-write/close; persistent readers, sessions, arbitrary dispatch and resource transfer remain unsupported. Provider/runtime/path/lifetime assumptions are published in the M5 runtime contract.",
            "Callable": "typing/collections.abc Callable[[T1, T2], R]: fixed positional pure invocation, exact inputs/result and stable captures; failure upper bound IndexError, KeyError, ValueError, ZeroDivisionError and RecursionError. Analyzed callers supply resolved checked callable evidence; annotations do not prove actual callbacks pure.",
            "Vector": "Vector[T]: eager exact deep data. of(*explicit items), Vector[T].of() empty, int index/slice, appended(T), updated_at(int,T), concat(Vector[T]), map(checked bounded callback T->R), filter(checked bounded callback T->bool), fold(checked bounded callback (A,T)->A,A); invocation effects union into caller bounds. Retains prior versions; tuple-copy updates O(n); len/equality. IndexError and zero-step ValueError; callback failures propagate. GenericAlias types are runtime erased.",
            "OrderedMap": "OrderedMap[K,V]: exact homogeneous scalar keys and recursively admitted values; of(*exact pair tuples), typed empty, key lookup/get(key,V default)/contains, updated/without/merge, entries()/keys()/values() -> Vector. Replace preserves key position, new keys append; right merge wins; order participates in equivalence. Missing lookup KeyError; tuple-copy updates O(n).",
            "Map": "Map[K,V]: unordered exact homogeneous scalar keys; of(*exact pair tuples), typed empty, lookup/get/contains/updated/without/merge and extensional equality. ordered_entries()/ordered_keys()/ordered_values() -> Vector use scalar total order. No arbitrary traversal or callbacks; canonical representation; missing lookup KeyError; tuple-copy updates O(n).",
            "Set": "Set[T]: unordered homogeneous exact scalar elements; of(*items), typed empty, contains/added/without/union/intersection/difference, ordered_values() -> Vector in scalar total order. No arbitrary traversal or callbacks; typed extensional equality and canonical representation; tuple-copy updates O(n).",
            "module": "# mode: fun after the optional shebang/encoding/docstring and before executable source, or project require_modules globs; initialization is checked without application imports or evaluation.",
        }
        if args.symbol in operations:
            print(operations[args.symbol])
            return 0
        print(f"Unknown rule or operation: {args.symbol}")
        return 2
    if args.command == "check":
        result = check_paths(args.paths, root=args.root, audit=args.audit, target=args.target, cache=not args.no_cache)
    else:
        result = build_paths(args.paths, root=args.root, output=args.output, target=args.target)
    _show(result, args.json)
    return result.status
