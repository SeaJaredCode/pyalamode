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
        print(f"Strict gate passed: {selected} selected functions and {modules} functional modules; ordinary shells and ordinary initialization are unchecked.")
        if not selected:
            print("No participating functions were selected; module initialization coverage is reported separately.")
    if result.output:
        print(f"Built ordinary Python source: {result.output}")
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
            "tuple": "Exact recursive tuple[T1, T2], homogeneous tuple[T, ...], or empty tuple[()]; immutable data only, no subclasses or callable payloads. Fixed tuples use literal indexes/slices; homogeneous tuples admit exact int indexes/slices. Equality and len are characterized; iteration remains unsupported.",
            "Callable": "typing/collections.abc Callable[[T1, T2], R]: fixed positional pure invocation, exact inputs/result and stable captures; failure upper bound IndexError, KeyError, ValueError, ZeroDivisionError and RecursionError. Analyzed callers supply resolved checked callable evidence; annotations do not prove actual callbacks pure.",
            "Vector": "Vector[T]: eager exact deep data. of(*explicit items), Vector[T].of() empty, int index/slice, appended(T), updated_at(int,T), concat(Vector[T]), map(checked Callable[[T],R]), filter(checked Callable[[T],bool]), fold(checked Callable[[A,T],A],A). Retains prior versions; tuple-copy updates O(n); len/equality. IndexError and zero-step ValueError; callback failures propagate. GenericAlias types are runtime erased.",
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
