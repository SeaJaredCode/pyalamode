"""Small usable command interface for the scalar milestone."""

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
        print(f"Strict gate passed: {selected} selected scalar functions; ordinary shell and module initialization are unchecked.")
        if not selected:
            print("No participating exports were selected; this check establishes no export claim.")
    if result.output:
        print(f"Built ordinary Python source: {result.output}")
    print(f"{coverage['analyzed_call_sites']} ordinary same-file call sites inspected; elapsed {result.elapsed_seconds:.6f}s.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pyalamode", description="Statically check the closed scalar subset of ordinary Python.")
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
            "len": "len(exact str or bytes) -> exact int; one positional argument.",
            "min": "min(two or more exact int, str, or bytes of one type) -> same type; no iterable/key/default forms.",
            "max": "max(two or more exact int, str, or bytes of one type) -> same type; no iterable/key/default forms.",
            "fun": "Runtime identity marker. Execution adds no checked evidence and performs no input validation.",
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
