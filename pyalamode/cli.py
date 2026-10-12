"""Local static check/build and finite contract explanations."""

import argparse
import json
from .model import RULES, TARGET
from .project import build_paths, check_paths
from .encoding_contracts import ENCODING_VERSION, operation_catalog as codec_catalog, operation_contract as codec_contract
from .builder_contracts import BUILDER_VERSION, operation_catalog as builder_catalog, operation_contract as builder_contract
from .task_contracts import TASK_VERSION, operation_catalog as task_catalog, operation_contract as task_contract, setup_contract as task_setup
from .standard_contracts import STANDARD_VERSION, operation_contract, operation_catalog
from .integration_contracts import INTEGRATION_VERSION, operation_contract as external_contract, integration_snapshot


def _show(result, structured: bool) -> None:
    if structured:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return
    for item in result.tooling:
        print(item.format())
    for item in result.policy_diagnostics:
        if not any(item in file.diagnostics for file in result.results):print(item.format())
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
        print(f"Strict gate passed: {selected} selected functions, {records} record declarations, {coverage['selected_variants']} closed variants and {modules} functional modules; ordinary shells and ordinary initialization are unchecked.")
        if not selected:
            print("No participating functions were selected; module initialization coverage is reported separately.")
    if result.output:
        print(f"Built ordinary Python source: {result.output}")
    for file in result.results:
        for contract in file.contracts:
            for assumption in contract.external_assumptions:
                approval = assumption["approval"] or {}
                print(f"External assumption {assumption['identity']} in {contract.name}: {assumption['admission']}; owner {approval.get('owner', 'unapproved')}; dependency {assumption['dependency_sha256']}; expiry {approval.get('expires_at', 'nonexpiring or unapproved')}.")
        for adapter in file.unsafe_adapters:
            print(f"Unsafe ordinary adapter {adapter['name']} at {file.path}:{adapter['line']}: scope {adapter['scope']}; {adapter['rationale']}; unchecked behavior.")
        for setup in file.setup_observations:
            print(f"Ordinary setup {setup['identity']} at {file.path}:{setup['line']}: effects {setup['effects']}; {setup['phase']}; surrounding initialization/body unchecked.")
    for boundary in result.guarded_exports:
        state = "generated" if boundary["generated"] else "selected for build"
        print(f"Guarded public boundary {boundary['public_boundary']} ({state}); original {boundary['original_boundary']}: {boundary['original_protection']}.")
    if result.boundary_guards == "debug":
        print(f"Debug data assertions: {len(result.debug_coverage)} selected functions; exact supported parameters, local data bindings and returns; callable evidence remains a caller obligation.")
    print(f"{coverage['analyzed_call_sites']} checked or resolved ordinary caller sites inspected; elapsed {result.elapsed_seconds:.6f}s.")


def explain_symbol(symbol: str, *, root=None, snapshot=None) -> dict:
    """Detached explanations shared by commands and the local editor."""
    from pathlib import Path
    from .project import load_policy
    if ":" in symbol:
        from .project import check_snapshot
        from .checker import _module_name
        from dataclasses import asdict
        project_root = Path(root or Path.cwd()).resolve()
        captured = snapshot or check_snapshot([project_root], root=project_root)
        matches = [contract for file in captured.result.results for contract in file.contracts
                   if _module_name(file.path, project_root) + ":" + contract.name == symbol]
        if len(matches) != 1:
            return {"symbol": symbol, "status": 2, "title": symbol, "text": "Unknown or ambiguous authored boundary: " + symbol, "contract": None}
        contract = asdict(matches[0])
        return {"symbol": symbol, "status": captured.result.status, "title": symbol,
                "text": symbol + " (" + captured.freshness + ")\n" + json.dumps(contract, indent=2, sort_keys=True), "contract": contract}
    external = external_contract(symbol)
    if external is not None or symbol == "integrations":
        project_root = Path(root or Path.cwd()).resolve()
        if snapshot is not None:
            external_snapshot = {"catalog": snapshot.result.integration_catalog, "approvals": snapshot.result.integration_approvals,
                                 "errors": [item.reason for item in snapshot.result.tooling]}
            source_status = snapshot.result.status
        else:
            policy, error = load_policy(project_root)
            if error:
                return {"symbol": symbol, "status": 2, "title": symbol, "text": error, "contract": None}
            external_snapshot = integration_snapshot(policy, project_root)
            source_status = 0
        rows = [row for row in external_snapshot["catalog"] if external is None or row["identity"] == external["identity"]]
        lines = []
        for row in rows:
            lines.append(f"{row['identity']} ({INTEGRATION_VERSION}): {row['signature']}\n{row['behavior']}\nEffects: {row['effects']}; failures: {row['failures']}.\nApproval: {row['admission']}; contract {row['contract_sha256']}; installed dependency {row['dependency_sha256']}.\nInitialization: {row['initialization']['evidence']}\n{row['aliases']}")
            if row["identity_error"]:
                lines.append(row["identity_error"])
        lines.extend(external_snapshot["errors"])
        return {"symbol": symbol, "status": max(source_status, 2 if external_snapshot["errors"] or any(row["identity_error"] for row in rows) else 0),
                "title": symbol, "text": "\n".join(lines), "contract": {"version": INTEGRATION_VERSION, "catalog": rows, "approvals": external_snapshot["approvals"], "errors": external_snapshot["errors"]}}
    task = task_contract(symbol)
    setup = task_setup(symbol)
    if symbol == "tasks" or task is not None or setup is not None:
        rows = task_catalog() if symbol == "tasks" else [task or setup]
        return {"symbol": symbol, "status": 0, "title": symbol, "text": "\n".join(r["identity"] + ": " + r["behavior"] for r in rows), "contract": {"version": TASK_VERSION, "catalog": rows}}
    builder = builder_contract(symbol)
    if symbol == "builders" or builder is not None:
        rows = builder_catalog() if builder is None else [builder]
        return {"symbol": symbol, "status": 0, "title": symbol, "text": "\n".join(r["identity"] + ": " + r["signature"] + "\n" + r["behavior"] for r in rows), "contract": {"version": BUILDER_VERSION, "catalog": rows}}
    codec=codec_contract(symbol)
    if symbol=="encoding" or codec is not None:
        rows=codec_catalog() if codec is None else [codec]
        return {"symbol":symbol,"status":0,"title":symbol,"text":"\n".join(r["identity"]+": "+r["signature"]+"\n"+r["behavior"] for r in rows),"contract":{"version":ENCODING_VERSION,"catalog":rows}}
    if symbol == "standard":
        text = STANDARD_VERSION + ": exact versioned standard operations; ordinary setup and invocation evidence are separate.\n"
        text += "\n".join(row["identity"] + ": " + row["signature"] for row in operation_catalog())
        return {"symbol": symbol, "status": 0, "title": symbol, "text": text, "contract": {"version": STANDARD_VERSION, "catalog": operation_catalog()}}
    standard = operation_contract(symbol)
    if standard is not None:
        text = f"{standard['identity']} ({STANDARD_VERSION}): {standard['signature']}\n{standard['behavior']}\nEffects: {standard['effects']}; failures: {standard['failures']}.\nInitialization: {standard['initialization']['evidence']}\n{standard['aliases']}"
        return {"symbol": symbol, "status": 0, "title": standard["identity"], "text": text, "contract": standard}
    rule = symbol.upper()
    if rule in RULES:
        title, remediation = RULES[rule]
        text = f"{rule}: {title}\n{remediation}"
        if rule == "PAL101":
            text += "\nExample rejected: x = 1; x = 2. Exclusive if/else bindings are permitted."
        return {"symbol": symbol, "status": 0, "title": title, "text": text, "contract": {"rule": rule, "remediation": remediation}}
    operations = {
        "abs": "abs(exact int) -> exact int; one positional argument.",
        "len": "len(exact str, bytes, recursively admitted tuple, Vector, OrderedMap, Map or Set) -> exact int; one positional argument.",
        "min": "min(two or more exact int, str, or bytes of one type) -> same type; no iterable/key/default forms.",
        "max": "max(two or more exact int, str, or bytes of one type) -> same type; no iterable/key/default forms.",
        "fun": "Runtime identity marker. Execution adds no checked evidence and performs no input validation.",
        "unsafe": "@unsafe(scope=nonempty_text,rationale=nonempty_text) returns an ordinary function unchanged. Its adapter remains outside certification; neither pure nor all-effects checked code can call unknown behavior. Explicit exclusive snapshot/schema validation may start a new checked computation without certifying the preceding adapter.",
        "record": "@record declares an exact fixed record with public typed data fields and stable defaults; required fields precede defaults. Constructor positional/keyword inputs and defaults undergo deep exact schema validation; fields cannot be reassigned/deleted. No bases, metaclasses, descriptors, methods, custom validators/constructors, callable fields, forward/recursive record declarations or forward/recursive record declarations. Finite exact record class patterns are supported with irrefutable fresh captures; guarded/partial captures are refused. Equality includes exact record identity and recursively equivalent field values; records are unhashable.",
        "variant": "@variant declares a closed top-level namespace of public nested @case classes with fixed admitted fields and stable defaults; case constructors are Domain.Case(...). Exact tags and payloads are immutable; no bases, methods, dynamic metadata, recursion or arbitrary matcher hooks. Adding a case invalidates incomplete explicit consumers.",
        "case": "Nested @case payload declarations follow fixed record field/signature rules. Match Domain.Case(fresh_capture) or known field keywords; nested exact record/case dispatch is characterized. Constrained partial or guarded patterns cannot have named captures. A deliberate final _ covers future cases unless explicit_cases=['module:Domain'] policy requires explicit coverage.",
        "Option": "Option[T] is Some(value:T) or Nothing(); exact recursively admitted payloads. Construct Some(value) / Nothing(), inspect by exhaustive match. Generic schemas validate payload obligations; unknown/subclass values and arbitrary methods are unsupported.",
        "Result": "Result[T,E] is Ok(value:T) or Err(error:E), with exact immutable payloads. Construct Ok(value)/Err(error), inspect by exhaustive match; expected errors are data alternatives, distinct from raised builtin failure categories.",
        "accumulate": "accumulate(left,right), exactly two positional established Result[T,E]/Result[U,E] schemas, returns Result[tuple[T,U],Vector[E]]. Both ordinary arguments evaluate before accumulation; errors are retained in left-to-right argument order. Sparse Ok/Err constructors require explicit Result bindings to supply missing branch schemas.",
        "Failure": "Exact immutable record category:str,message:str; failure_value(opaque_handler_token) maps finite exact builtin failure identities to fixed category messages without reading args/dictionaries/traceback/frames/formatters. Invalid ordinary exceptions fail TypeError; valid recursive validation may raise RecursionError.",
        "handlers": "Finite try/except unchanged ZeroDivisionError,IndexError,KeyError,ValueError,RecursionError,RuntimeError,OSError,UnicodeError, optional fresh as target. ValueError covers UnicodeError; RuntimeError covers RecursionError. Overlaps, broad/bare/user handlers, else/finally and raise are refused. Actual exception target is opaque and deleted after handler exit; only failure_value conversion is admitted. Per-site handled masks discharge failures while retaining every performed effect, operation and assumption.",
        "replace": "replace(exact_record, **explicit_known_field_changes) returns a new validated exact record, preserving prior versions. Strict calls use only known field keywords and admitted nested data; an ignored replacement is PAL250. Recursive validation may raise RecursionError under valid contracts; invalid ordinary inputs raise TypeError with a path.",
        "freeze": "Ordinary shell freeze(value, *, exclusive=False, adapter=None, schema=None): closed exact list -> Vector, tuple -> tuple, dict -> OrderedMap, scalar set/frozenset -> Set, admitted stable data -> validated reuse. Explicit exclusive=True asserts caller-held exclusive access for recursively mutable or unknown source data; the library does not detect ownership or lock concurrent writers. Missing preconditions, subclasses, cycles, hooks and views fail. Explicit schema=Vector[int]/closed schema establishes supported output shape for analyzed simple ordinary assignments and subsequent checked calls. Conversions certify the output data, not preceding shell/provider behavior; no strict pure-body/default/initializer conversion contract.",
        "thaw": "Ordinary shell thaw(admitted_data) creates independent fresh mutable integration containers: Vector/tuple -> list, Map/OrderedMap -> dict, Set -> set, records -> dict of fields, scalars reuse. Nested exports never retain a mutable alias into the source; no arbitrary restoration/constructor hooks. Not admitted in strict pure functions.",
        "dataclass_adapter": "dataclass_adapter(ExactOrdinaryDataclass, ExactTargetRecord): named finite compatibility qualifier for direct ordinary generated storage/behavior, stable defaults, no factories/custom hooks/subclasses. freeze(source, adapter=adapter, exclusive=True, schema=TargetRecord) recursively snapshots fields into the exact target schema. frozen=True alone never qualifies source behavior/data; the foreign object is not strict data.",
        "namedtuple_adapter": "namedtuple_adapter(ExactGeneratedNamedTuple, ExactTargetRecord): named ordinary-shell qualifier, generated fixed storage/behavior only; no custom getters/constructors/subclasses. Snapshot produces validated concrete product record fields; foreign named tuples do not become admitted strict objects.",
        "guards": "Policy boundary_guards=off (default), exports, or debug; guarded_exports=['module:function'] selects exact top-level public boundaries. Build generates normally importable pyalamode_exports.module:function aliases; original functions stay unwrapped in exports mode and internal direct calls have no repeated guards. Selected guards validate exact deep arguments before body and returns after; Callable, Effectful and capability boundaries are refused. Debug adds finite supported parameter/local/return data assertions to copied source, with documented overhead; it does not prove effects, callback purity, ownership or dependency identity.",
        "tuple": "Exact recursive tuple[T1, T2], homogeneous tuple[T, ...], or empty tuple[()]; immutable data only, no subclasses or callable payloads. Fixed tuples use literal indexes/slices; homogeneous tuples admit exact int indexes/slices. Equality and len are characterized; iteration remains unsupported.",
        "effects": "@effects(IO,State,Clock,Random,Environment,Task) is an identity declaration factory selecting checked effectful source; unique finite tokens only, optionally with @fun. Declared upper bounds and required operation/callback effect unions remain distinct. Task invocations require explicit tasks=true policy, which defaults off. Initialization/provider construction remains ordinary-shell setup; no runtime registry or purity inference.",
        "Effectful": "Effectful[[T1,...],R,Clock,...]: fixed positional callable upper bound; concrete target bounds must be subsets, conditional alternatives union their bounds and finite failures. Exact capability slots require the corresponding effect family; captures/defaults/results cannot retain capabilities. Pure Callable retains an empty effect bound.",
        "borrow": "with borrow(exact_local_capability) as fresh_name: one characterized logical lease; supports finite nested borrowing and invocation lending to exact checked capability slots. View invalidates on every exit, including return/body failure; it does not expose a persistent OS reader. Capabilities cannot be data, aliases, global constants, defaults, callable captures or stable returned values. Factory setup and resource ownership remain ordinary caller obligations.",
        "capabilities": "Finite exact interfaces: IOCapability.read_text(str)->str/write_text(str,str)->None; StateCapability.get()->int/set(int)->None; ClockCapability.now_ns()->int; RandomCapability.below(int)->int; EnvironmentCapability.get(str,str)->str; TaskCapability is consumed by top-level task_map/task_map_with operations and has no admitted methods. Providers retain their family, including controlled Task and recorded external effects. Task invocations default off and require tasks=true; runtime callable admission does not infer purity. IO whole-path operations use internal open/read-or-write/close. Provider/runtime/path/lifetime assumptions are published in the M5 and M13 contracts.",
        "Callable": "typing/collections.abc Callable[[T1, T2], R]: fixed positional pure invocation, exact inputs/result and stable captures; failure upper bound IndexError, KeyError, ValueError, UnicodeError, ZeroDivisionError and RecursionError. Analyzed callers supply resolved checked callable evidence; annotations do not prove actual callbacks pure.",
        "Vector": "Vector[T]: eager exact deep data. of(*explicit items), Vector[T].of() empty, int index/slice, appended(T), updated_at(int,T), concat(Vector[T]), map(checked bounded callback T->R), filter(checked bounded callback T->bool), fold(checked bounded callback (A,T)->A,A); invocation effects union into caller bounds. Retains prior versions; tuple-copy updates O(n); len/equality. IndexError and zero-step ValueError; callback failures propagate. GenericAlias types are runtime erased.",
        "OrderedMap": "OrderedMap[K,V]: exact homogeneous scalar keys and recursively admitted values; of(*exact pair tuples), typed empty, key lookup/get(key,V default)/contains, updated/without/merge, entries()/keys()/values() -> Vector. Replace preserves key position, new keys append; right merge wins; order participates in equivalence. Missing lookup KeyError; tuple-copy updates O(n).",
        "Map": "Map[K,V]: unordered exact homogeneous scalar keys; of(*exact pair tuples), typed empty, lookup/get/contains/updated/without/merge and extensional equality. ordered_entries()/ordered_keys()/ordered_values() -> Vector use scalar total order. No arbitrary traversal or callbacks; canonical representation; missing lookup KeyError; tuple-copy updates O(n).",
        "Set": "Set[T]: unordered homogeneous exact scalar elements; of(*items), typed empty, contains/added/without/union/intersection/difference, ordered_values() -> Vector in scalar total order. No arbitrary traversal or callbacks; typed extensional equality and canonical representation; tuple-copy updates O(n).",
        "module": "# mode: fun after the optional shebang/encoding/docstring and before executable source, or project require_modules globs; initialization is checked without application imports or evaluation.",
    }
    operations["failure_value"] = operations["Failure"]
    operations["match"] = operations["case"]
    if symbol in operations:
        return {"symbol": symbol, "status": 0, "title": symbol, "text": operations[symbol], "contract": None}
    return {"symbol": symbol, "status": 2, "title": symbol, "text": "Unknown rule or operation: " + symbol, "contract": None}


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
            command.add_argument("--output", help="fresh output directory or canonical wheel path")
            command.add_argument("--wheel", action="store_true", help="build the finite ordinary checked source wheel")
    explanation = commands.add_parser("explain", help="describe a stable rule or scalar operation")
    explanation.add_argument("symbol")
    explanation.add_argument("--root", help="project root for current integration policy and identities")
    explanation.add_argument("--json", action="store_true", help="detached operation explanation")
    editor = commands.add_parser("editor", help="local read-only editor protocol over stdio")
    editor.add_argument("--stdio", action="store_true", required=True)
    editor.add_argument("--root", required=True, help="existing project root")
    formatter = commands.add_parser("format", help="read-only experimental source formatting proposal")
    formatter.add_argument("paths", nargs="*")
    formatter.add_argument("--root")
    formatter.add_argument("--json", action="store_true")
    modes = formatter.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--preview", action="store_true")
    locator = commands.add_parser("locate", help="resolve an owned generated source coordinate")
    locator.add_argument("--artifact", required=True)
    locator.add_argument("--path", required=True)
    locator.add_argument("--line", type=int, required=True)
    locator.add_argument("--column", type=int, required=True)
    locator.add_argument("--root")
    locator.add_argument("--json", action="store_true")
    for name in ("regions", "ready", "report", "baseline", "convert"):
        command = commands.add_parser(name, help="local migration evidence and read-only adoption proposals")
        command.add_argument("--root", help="project root")
        command.add_argument("--target", default=TARGET)
        command.add_argument("--json", action="store_true")
        if name in {"regions", "ready", "report"}:
            command.add_argument("paths", nargs="*")
        if name == "report":
            command.add_argument("--compare", help="project-local .pyalamode JSON reference")
            command.add_argument("--save", action="store_true", help="save this exact report without changing the baseline")
        elif name == "baseline":
            command.add_argument("--owner", required=True)
            command.add_argument("--rationale", required=True)
            command.add_argument("--replace", action="store_true")
        elif name == "convert":
            command.add_argument("target_selection")
            command.add_argument("--preview", action="store_true", required=True)
    args = parser.parse_args(argv)
    if args.command in {"format", "locate"}:
        from .project import format_paths, locate_source
        output = (format_paths(args.paths, root=args.root, mode="check" if args.check else "preview") if args.command == "format" else
            locate_source(artifact=args.artifact, path=args.path, line=args.line, column=args.column, root=args.root))
        if args.json: print(json.dumps(output, indent=2, sort_keys=True))
        elif args.command == "format":
            for row in output["files"]:
                if row["diff"]: print(row["diff"], end="")
            print("format: status " + str(output["status"]) + "; read-only proposal")
        else: print(json.dumps(output["authored"] or output["diagnostics"], sort_keys=True))
        return output["status"]
    if args.command == "explain":
        explanation = explain_symbol(args.symbol, root=args.root)
        if args.json:
            print(json.dumps(explanation["contract"] or explanation, indent=2, sort_keys=True))
        else:
            print(explanation["text"])
        return explanation["status"]
    if args.command == "editor":
        from .editor import serve
        return serve(root=args.root)
    if args.command in {"regions", "ready", "report", "baseline", "convert"}:
        from pathlib import Path
        from .migration import MigrationError, write_baseline, save_report
        from .migration_views import observe, regions_view, ready_view, convert_preview, make_prepublish
        from .project import load_policy
        root = Path(args.root or Path.cwd()).resolve()
        try:
            bootstrap = False
            if args.command == "baseline" and not args.replace:
                policy, error = load_policy(root, root)
                if error:
                    raise MigrationError(error)
                active = policy.get("migration", {}).get("baseline", ".pyalamode/baseline.json")
                bootstrap = not (root / active).exists()
            snapshot, state, report, reference = observe(root, getattr(args, "paths", None), target=args.target,
                        compare=getattr(args, "compare", None), bootstrap=bootstrap)
            status, output = report["status"], report
            if args.command == "regions":
                output = regions_view(snapshot, state)
                output["status"] = status
                output["report"] = report
            elif args.command == "ready":
                output = ready_view(snapshot, state)
                output["status"] = status
                output["report"] = report
            elif args.command == "convert":
                output = convert_preview(snapshot, state, args.target_selection)
                output["report"] = report
                if output["candidate"] is None:
                    output["status"] = max(output["status"], report["status"])
                status = output["status"]
            elif args.command == "baseline" or args.command == "report" and args.save:
                callback = make_prepublish(snapshot, state, [reference["receipt"]] if reference else [])
                written = (write_baseline(root, state, owner=args.owner, rationale=args.rationale, replace=args.replace, prepublish=callback)
                           if args.command == "baseline" else save_report(root, report, prepublish=callback))
                output = {"report": report, "written": written}
                if args.command == "baseline":
                    status = written["status"]
            if args.json:
                print(json.dumps(output, indent=2, sort_keys=True))
            else:
                print(f"{args.command}: status {status}; current strict source {state['strict_status']}; current policy {state['current_policy_status']}; no automatic source edits.")
                print(f"Project: {state['coverage']['selected_functions']} selected / {state['coverage']['eligible_functions']} eligible functions; {state['coverage']['checked_exports']} checked exports.")
                if "written" in output:
                    print(f"Recorded {output['written']['id']}: {output['written']['path']}; verified=false.")
                    if output["written"]["history_path"]:
                        print("History: " + output["written"]["history_path"])
                if args.command == "ready":
                    for group in output["groups"]:
                        print(", ".join(group["members"]) + (": ready" if group["ready"] else ": review blockers") + "; " + json.dumps(group["blockers"]))
                if args.command == "convert":
                    for edit in output["edits"]:
                        print(edit["diff"])
                    for blocker in output["blockers"]:
                        print(str(blocker))
                for category, rows in report["comparison"].items():
                    if type(rows) is list and rows:
                        print(f"{category}: {len(rows)} event(s)")
            return status
        except (MigrationError, OSError, ValueError, TypeError, RecursionError, KeyError) as error:
            output = {"schema": 1, "kind": "pyalamode-migration-tooling-error", "status": 2, "verified": False, "error": str(error)[:1024]}
            print(json.dumps(output, indent=2, sort_keys=True) if args.json else "Migration tooling failure: " + output["error"])
            return 2
    if args.command == "check":
        result = check_paths(args.paths, root=args.root, audit=args.audit, target=args.target, cache=not args.no_cache)
    else:
        result = build_paths(args.paths, root=args.root, output=args.output, target=args.target, artifact="wheel" if args.wheel else "tree")
    _show(result, args.json)
    return result.status
