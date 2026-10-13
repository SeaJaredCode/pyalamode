"""Current engine capture, local adoption queues and finite read-only previews."""
from __future__ import annotations

import ast
import copy
from dataclasses import asdict, fields
from datetime import datetime, timezone
import difflib
import fnmatch
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import tokenize

from .model import CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, diagnostic, runtime_environment, SYNTAX_VERSION, SOURCE_MAP_SCHEMA, FunctionContract
from . import source_maps as sm
from .migration import (MigrationError, IDENTITY_VERSION, SOURCE_RULES, GATES,
                        finding_context, normalize_state, compare_states,
                        evaluate_gates, load_reference)


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()


def _hash(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _relative(path, root):
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError:
        raise MigrationError("migration source resolves outside project; refused before reading") from None


def _location(path, node=None):
    return {"path": path, "line": node.lineno if node else 1,
            "column": node.col_offset + 1 if node else 1,
            "end_line": node.end_lineno if node else None,
            "end_column": node.end_col_offset + 1 if node else None,
            "column_encoding": "utf-8-bytes"}


def _authored_location(snapshot, path, relative, node=None):
    value = _location(relative, node)
    unit = snapshot.source_units.get(path)
    if node is None or unit is None or unit.source_map is None: return value
    span = sm.ByteSpan(sm.offset_at(unit.normalized_bytes,node.lineno,node.col_offset+1),
        sm.offset_at(unit.normalized_bytes,node.end_lineno,node.end_col_offset+1))
    mapped = sm.map_range(unit.source_map,span,source=unit.authored_bytes,generated=unit.normalized_bytes)
    first,last=sm.position_at(unit.authored_bytes,mapped.source_span.start),sm.position_at(unit.authored_bytes,mapped.source_span.end)
    value.update(line=first.line,column=first.column,end_line=last.line,end_column=last.column)
    return value


def _authored_line(snapshot, path, line):
    unit = snapshot.source_units.get(path) or (snapshot.graph.source_units.get(path) if snapshot.graph else None)
    if unit is None or unit.source_map is None: return line
    offset=sm.offset_at(unit.normalized_bytes,line,1)
    mapped=sm.map_range(unit.source_map,sm.ByteSpan(offset,offset),source=unit.authored_bytes,generated=unit.normalized_bytes)
    return sm.position_at(unit.authored_bytes,mapped.source_span.start).line


def _logical(row):
    return {key: row[key] for key in ("kind", "selector", "qualified_name")}


def _policy(policy):
    migration = {"schema": 1, "baseline": ".pyalamode/baseline.json", **{key: False for key in GATES}}
    migration.update(policy.get("migration", {}))
    return {"require_modules": list(policy.get("require_modules", [])),
            "effect_bounds": copy.deepcopy(policy.get("effect_bounds", {})),
            "explicit_cases": list(policy.get("explicit_cases", [])),
            "external_trust": policy.get("external_trust", "deny"),
            "integration_manifests": list(policy.get("integration_manifests", [])),
            "integration_approvals": copy.deepcopy(policy.get("integration_approvals", [])),
            "required_exports": list(policy.get("required_exports", [])),
            "boundary_guards": policy.get("boundary_guards", "off"),
            "guarded_exports": list(policy.get("guarded_exports", [])), "distribution":copy.deepcopy(policy.get("distribution")), "checked_dependencies":copy.deepcopy(policy.get("checked_dependencies",[])), "builders":policy.get("builders",False), "tasks":policy.get("tasks",False), "edition": policy.get("edition", EDITION), "migration": migration}


def inventory(root, paths=None):
    """Inventory exclusions without reading them; paths only select display."""
    from .project import _EXCLUDED
    root = Path(root).resolve()
    exclusions = []
    for directory, children, _ in os.walk(root):
        excluded = [name for name in children if name in _EXCLUDED or name.endswith(".egg-info") or name.startswith(".pyalamode-build-")]
        for name in excluded:
            exclusions.append({"path": (Path(directory) / name).relative_to(root).as_posix(), "reason": "reserved product build staging" if name.startswith(".pyalamode-build-") else "excluded project directory"})
        children[:] = sorted(name for name in children if name not in excluded)
    requested = []
    for value in paths or [root]:
        path = Path(value).resolve()
        relative = _relative(path, root)
        if any(part in _EXCLUDED or part.endswith(".egg-info") or part.startswith(".pyalamode-build-") for part in Path(relative).parts):
            raise MigrationError("display selection is excluded source: " + relative)
        if not path.exists() or (path.is_file() and path.suffix not in {".py", ".pya"}):
            raise MigrationError("display selection must be existing project-local Python source or directory")
        requested.append(path)
    return {"requested": requested, "exclusions": sorted(exclusions, key=lambda row: (row["path"], row["reason"]))}


def _displayed(snapshot, inv):
    root = Path(snapshot.inputs["root"])
    return sorted(_relative(path, root) for path in snapshot.sources
                  if any(Path(path) == selected or Path(path).is_relative_to(selected) for selected in inv["requested"]))


def _module_marker(analyzer):
    tree = analyzer.tree
    if tree is None:
        return False
    doc = tree.body[0] if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and type(tree.body[0].value.value) is str else None
    first = tree.body[1] if doc and len(tree.body) > 1 else (tree.body[0] if not doc and tree.body else None)
    valid = False
    for token in tokenize.generate_tokens(io.StringIO(analyzer.source, newline=None).readline):
        if token.type == tokenize.COMMENT and token.string.strip() == "# mode: fun":
            if not token.start[1] and (not doc or token.start[0] > doc.end_lineno) and (not first or token.start[0] < first.lineno) and not valid:
                valid = True
    return valid


def _required_module(path, policy):
    return any(fnmatch.fnmatchcase(path, pattern) or PurePosixPath(path).match(pattern)
               or ("**/" in pattern and fnmatch.fnmatchcase(path, pattern.replace("**/", "")))
               for pattern in policy.get("require_modules", []))


def _signature(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return json.dumps({"arguments": ast.dump(node.args, include_attributes=False, show_empty=False),
                           "returns": ast.dump(node.returns, include_attributes=False, show_empty=False) if node.returns else None,
                           "type_parameters": [ast.dump(n, include_attributes=False, show_empty=False) for n in node.type_params]}, sort_keys=True, separators=(",", ":"))
    if isinstance(node, ast.ClassDef):
        return json.dumps([ast.dump(n, include_attributes=False, show_empty=False) for n in node.body], separators=(",", ":"))
    return None


def _constructor_aliases(analyzer):
    """Exact generated Name occurrences with their actual stable import owner."""
    unit = analyzer.graph.source_units.get(analyzer.path)
    if unit is None or unit.translation is None: return {}
    admitted = {}
    for family in unit.translation.used_collections:
        alias = "_pyalamode_syntax_"+family
        symbol = analyzer.symbols.get(alias)
        if (symbol and symbol.kind == "import" and symbol.name == "pyalamode:"+family
                and analyzer._symbol_stable(alias,symbol) and not analyzer._module_changed("pyalamode",family)):
            admitted[alias] = family
    return {str(node.lineno)+":"+str(node.col_offset+1)+":"+node.id: admitted[node.id]
        for node in ast.walk(analyzer.tree) if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load) and node.id in admitted}


def _canonical_node(analyzer, node):
    """Normalize only actual compiler-owned constructor binding occurrences."""
    aliases = _constructor_aliases(analyzer)
    cloned = copy.deepcopy(node)
    class ConstructorNames(ast.NodeTransformer):
        def visit_Name(self, value):
            key = str(value.lineno)+":"+str(value.col_offset+1)+":"+value.id
            if isinstance(value.ctx,ast.Load) and key in aliases: value.id=aliases[key]
            return value
    return ConstructorNames().visit(cloned) if aliases else cloned


def _project_policy_diagnostic(result, item):
    if item not in result.policy_diagnostics:
        result.policy_diagnostics.append(item)
    # The existing editor consumes these rows. They are projected after body
    # caching and raw source proof, with an independent project-policy status.
    target = next((file for file in result.results if file.path == item.path), result.results[0] if result.results else None)
    if target is not None and item not in target.diagnostics:
        target.diagnostics.append(item)


def apply_current_policy(result, graph, policy, root):
    """Current requirements, before any historical comparison."""
    root = Path(root).resolve()
    policy_location = _location("pyproject.toml")
    for selector in policy.get("required_exports", []):
        module, name = selector.split(":")
        analyzer = graph.modules.get(module)
        nodes = [node for node in analyzer.tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name] if analyzer and analyzer.tree else []
        if len(nodes) > 1:
            result.current_policy_status = 2
            _project_policy_diagnostic(result, diagnostic("PAL001", str(root / "pyproject.toml"), "required export is an ambiguous canonical declaration: " + selector, origin="current export policy"))
            continue
        info = analyzer.infos.get(id(nodes[0])) if nodes else None
        contract = info.contract if info else None
        reason = "absent" if not nodes else "unselected" if info is None else "unverified" if contract is None or not contract.source_evidence.startswith("checked") else None
        if reason:
            evidence = contract.source_evidence if contract else "unchecked ordinary source" if nodes else "absent canonical export"
            event = {"boundary": {"kind": "function", "selector": selector, "qualified_name": name}, "before": None,
                     "after": {"selector": selector, "engine_status": 1, "engine_rule": "PAL361", "source_evidence": evidence},
                     "reason": "current-required-export-" + reason, "location": policy_location}
            result.current_policy_events["required_exports"].append(event)
            result.current_policy_status = max(result.current_policy_status, 1)
            _project_policy_diagnostic(result, diagnostic("PAL361", str(root / "pyproject.toml"), event["reason"] + ": " + selector, boundary=name, origin="current export policy"))
    now = datetime.now(timezone.utc)
    for approval in result.integration_approvals:
        expires = approval.get("expires_at")
        if expires and now >= datetime.strptime(expires, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc):
            expired = {**copy.deepcopy(approval), "status": "expired"}
            event = {"boundary": None, "before": None, "after": expired, "reason": "configured-approval-expired", "location": policy_location}
            result.current_policy_events["expired_approvals"].append(event)
            if policy.get("migration", {}).get("reject_expired_approvals", False):
                result.current_policy_status = max(result.current_policy_status, 1)
                _project_policy_diagnostic(result, diagnostic("PAL364", str(root / "pyproject.toml"), "configured approval expired: " + approval["operation"], origin="current approval expiry"))


def _operation_rows(snapshot):
    from .checker import _module_name
    graph = snapshot.graph
    if graph is None:
        return []
    root = Path(snapshot.inputs["root"])
    sites = {}
    for owner in graph.functions.values():
        if owner.analyzer.path not in snapshot.sources: continue
        pending = [(owner.identity, "direct")]
        seen = set()
        while pending:
            target, via = pending.pop()
            if (target, via) in seen or target not in graph.functions:
                continue
            seen.add((target, via))
            info = graph.functions[target]
            for operation, lines in info.external_operation_sites.items():
                canonical = "pyalamode." + operation
                for line in lines:
                    row = {"boundary": graph.module_name(owner.analyzer.path) + ":" + owner.qualified,
                           "path": _relative(info.analyzer.path, root) if info.analyzer.path in snapshot.sources else next(m["authored_path"] for r in graph.distributions["receipts"].values() if r.get("_payload") for m in r["_payload"]["modules"] if m["module"]==graph.module_name(info.analyzer.path)), "line": _authored_line(snapshot, info.analyzer.path, line), "via": via,
                           "source_owner": "project" if info.analyzer.path in snapshot.sources else next({"name":r["declaration"]["name"],"version":r["declaration"]["version"],"package":graph.module_name(info.analyzer.path).split(".")[0]} for r in graph.distributions["receipts"].values() if r["declaration"]["name"]==graph.source_owners[info.analyzer.path])}
                    sites.setdefault(canonical, {})[_canonical(row)] = row
            pending.extend((target_, "retained" if via == "retained" else "invoked") for target_ in info.calls)
            pending.extend((target_, "retained") for target_ in info.callable_dependencies)
    catalog = {row["identity"]: row for row in snapshot.result.integration_catalog}
    rows = []
    for operation, required in sorted(sites.items()):
        source = catalog[operation]
        evidence = graph.external_assumption(source)
        admission = source["admission"]
        if admission == "invalid policy":
            raise MigrationError("invalid engine integration policy cannot become migration evidence")
        rows.append({"operation": operation, "required_by": sorted(required.values(), key=lambda row: (row["boundary"], row["path"], row["line"], row["via"])),
                     "contract_sha256": source["contract_sha256"], "dependency_sha256": source["dependency_sha256"],
                     "admission": admission, "engine_status": 0 if admission == "approved" else 1,
                     "engine_rule": None if admission == "approved" else "PAL350",
                     "evidence": {"kind": "external-assumption", "value": evidence}})
    return rows


def capture_state(snapshot, policy, inventory):
    from .checker import _module_name
    if snapshot.result.audit:
        raise MigrationError("migration state requires an actual strict capture")
    root = Path(snapshot.inputs["root"])
    graph = snapshot.graph
    boundaries = []
    boundary_nodes = {}
    files = {file.path: file for file in snapshot.result.results}
    if graph:
        for path, analyzer in graph.analyzers.items():
            if path not in files: continue
            file = files[path]
            relative, module = _relative(path, root), _module_name(path, root)
            marker, required = _module_marker(analyzer), _required_module(relative, policy)
            module_reasons = (["module_marker"] if marker else []) + (["required_module"] if required else [])
            def append(kind, node, qualified, selected, evidence=None, info=None):
                selector = "module:" + module if kind == "module" else module + ":" + qualified
                contract = next((c for c in file.contracts if c.name == qualified), None) if kind == "function" else None
                data = asdict(contract) if contract else evidence or {}
                reasons = list(module_reasons) if selected else []
                if kind == "function" and info:
                    if info.parent:
                        reasons.append("enclosing_selection")
                    if any(analyzer._marker_like(d) for d in node.decorator_list):
                        reasons.append("source_fun")
                    if any(analyzer._effects_like(d) for d in node.decorator_list):
                        reasons.append("source_effects")
                if kind in {"record", "oneof"}:
                    reasons = []
                source_evidence = file.initialization_evidence if kind == "module" else data.get("source_evidence", "unchecked ordinary source")
                checked = bool(selected and source_evidence.startswith("checked"))
                public = bool(kind != "module" and module and "." not in qualified and not qualified.startswith("_") and graph.modules.get(module) is analyzer)
                guard = next((copy.deepcopy(row) for row in snapshot.result.guarded_exports if row["selection"] == selector), None) if public else None
                debug = next((copy.deepcopy(row) for row in snapshot.result.debug_coverage if row["path"] == path and row["name"] == qualified), None)
                if debug:
                    debug["path"] = relative
                row = {"id": None, "kind": kind, "selector": selector, "path": relative, "qualified_name": module if kind == "module" else qualified,
                       "signature": _signature(_canonical_node(analyzer,node)) if node is not None else None,
                       "definition_sha256": _hash(ast.dump(_canonical_node(analyzer,node or analyzer.tree), include_attributes=False, show_empty=False)),
                       "selected": bool(selected), "selection_reasons": sorted(set(reasons)), "strict_checked": checked,
                       "public_export": public, "required_export": kind == "function" and public and selector in policy.get("required_exports", []),
                       "mode": "strict" if selected else "off", "source_evidence": source_evidence,
                       "effect_bound": data.get("effect_bound", []), "required_effects": data.get("required_effects", []), "effect_origins": data.get("effect_origins", {}),
                       "external_assumptions": copy.deepcopy(data.get("external_assumptions", [])),
                       "failures": {"invocation": data.get("failures", []), "definition": data.get("definition_failures", []), "initialization": file.initialization_failures if kind == "module" else []},
                       "guard_coverage": {"mode": snapshot.result.boundary_guards, "selected_export": guard, "debug": debug, "data_assertions": data.get("data_assertions", [])},
                       "location": _authored_location(snapshot, path, relative, node)}
                boundaries.append(row)
                boundary_nodes.setdefault((relative, "<module>" if kind == "module" else qualified), []).append(row)
            if analyzer.tree is None:
                continue
            append("module", None, module, file.module_mode)
            def visit(body, prefix=""):
                for node in body:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        qualified = prefix + node.name
                        info = analyzer.infos.get(id(node))
                        append("function", node, qualified, info is not None, info=info)
                        visit(node.body, qualified + ".")
                    elif isinstance(node, ast.ClassDef):
                        for kind, declarations, evidence_rows in (("record", graph.record_declarations, file.records), ("oneof", graph.oneof_declarations, file.oneofs)):
                            declaration = next((info for info in declarations if info.analyzer is analyzer and info.node is node), None)
                            if declaration:
                                data = next((data for data in evidence_rows if data["name"] == node.name), {})
                                append(kind, node, prefix + node.name, True, data)
                        visit(node.body, prefix + node.name + ".")
                    else:
                        for field in ("body", "orelse", "finalbody"):
                            body_ = getattr(node, field, None)
                            if isinstance(body_, list):
                                visit(body_, prefix)
                        for handler in getattr(node, "handlers", []):
                            visit(handler.body, prefix)
                        for case in getattr(node, "cases", []):
                            visit(case.body, prefix)
            visit(analyzer.tree.body)
    grouped = {}
    for file in snapshot.result.results:
        relative = _relative(file.path, root)
        for item in file.diagnostics:
            if item.rule not in SOURCE_RULES:
                continue
            possible = boundary_nodes.get((relative, item.boundary), [])
            if len(possible) != 1:
                possible = boundary_nodes.get((relative, "<module>"), [])
                boundary = possible[0] if possible else None
                context = {"kind": "unavailable", "reason": "diagnostic boundary ownership is unavailable or ambiguous"}
            else:
                boundary = possible[0]
                from .checker import public_result
                analyzer = graph.analyzers[file.path]
                unit = graph.source_units[file.path]
                private_rows = []
                for d in analyzer.result.diagnostics:
                    if (d.rule,d.boundary,d.reason) != (item.rule,item.boundary,item.reason): continue
                    probe = copy.deepcopy(analyzer.result)
                    probe.diagnostics = [d]
                    mapped = public_result(probe,unit).diagnostics[0]
                    if asdict(mapped) == asdict(item): private_rows.append(d)
                private_boundary = copy.deepcopy(boundary)
                private_node = next((i.node for i in analyzer.infos.values() if i.qualified == item.boundary), None)
                private_boundary["location"] = _location(relative, private_node)
                if len(private_rows) != 1 or private_rows[0].origin == "experimental source frontend":
                    context = {"kind":"unavailable","reason":"diagnostic has no unique normalized authored occurrence"}
                else:
                    context = finding_context(analyzer.source, asdict(private_rows[0]), private_boundary, constructor_aliases=_constructor_aliases(analyzer))
            if boundary is None:
                raise MigrationError("diagnostic has no captured module boundary")
            location = {key: asdict(item)[key] for key in ("line", "column", "end_line", "end_column", "column_encoding", "first_binding", "reason", "remediation")}
            location["path"] = _relative(item.path, root)
            if location["first_binding"]:
                parts = location["first_binding"].rsplit(":", 2)
                first_path, tail = (parts[0], ":".join(parts[1:])) if len(parts) == 3 and parts[1].isdecimal() else (parts[-2], parts[-1])
                location["first_binding"] = _relative(first_path, root) + ":" + tail
            key = _hash({"rule": item.rule, "boundary": _logical(boundary), "signature": boundary["signature"], "context": context, "origin": item.origin})
            if key not in grouped:
                grouped[key] = {"id": None, "identity_key": None, "birth_identity": None, "rule": item.rule,
                                "boundary_id": None, "logical_boundary": _logical(boundary), "signature": boundary["signature"],
                                "context_sha256": None, "context": context, "origin": item.origin, "count": 0, "locations": [],
                                "review_required": context["kind"] == "unavailable"}
            grouped[key]["count"] += 1
            grouped[key]["locations"].append(location)
    required_operations = _operation_rows(snapshot)
    current_events = copy.deepcopy(snapshot.result.current_policy_events)
    for row in required_operations:
        if row["admission"] != "approved":
            site = row["required_by"][0]
            current_events["approval_failures"].append({"boundary": None, "before": None, "after": copy.deepcopy(row),
                 "reason": "required-operation-approval-not-current", "location": {**_location(site["path"]), "line": site["line"]}})
    unsafe = []
    for file in snapshot.result.results:
        for adapter in file.unsafe_adapters:
            row = copy.deepcopy(adapter)
            row["boundary"] = _module_name(file.path, root) + ":" + row.pop("name")
            row["path"] = _relative(row["path"], root)
            unsafe.append(row)
    modules = [row for row in boundaries if row["kind"] == "module"]
    functions = [row for row in boundaries if row["kind"] == "function"]
    state = {"schema": 5, "kind": "pyalamode-migration-state", "identity_version": IDENTITY_VERSION,
             "syntax_version": SYNTAX_VERSION, "source_map_schema": SOURCE_MAP_SCHEMA,
             "target": TARGET, "runtime_environment": runtime_environment(), "edition": policy.get("edition", EDITION), "checker": CHECKER_VERSION,
             "operation_contract": OPERATION_VERSION, "snapshot": snapshot.snapshot, "freshness": snapshot.freshness,
             "strict_status": max(snapshot.result.dependency_status,snapshot.result.source_status if snapshot.result.source_status is not None else snapshot.result.status),
             "current_policy_status": snapshot.result.current_policy_status, "current_policy_events": current_events,
             "current_dependency_status":snapshot.result.dependency_status,"current_dependency_events":copy.deepcopy(snapshot.result.dependency_events),
             "required_operations": required_operations,
             "inputs": {"sources": {_relative(path, root): copy.deepcopy(row) for path, row in snapshot.inputs["sources"].items()},
                        "policy_sha256": snapshot.inputs["policy_sha256"], "product_artifacts": snapshot.inputs["product_artifacts"],
                        "integration_inputs": snapshot.inputs["integration_inputs"], "checked_dependencies":copy.deepcopy(snapshot.result.distribution_inputs)},
             "scope": {"project_root": str(root), "selected_paths": sorted(_relative(path, root) for path in snapshot.sources),
                       "displayed_paths": _displayed(snapshot, inventory), "exclusions": inventory["exclusions"]},
             "coverage": {"eligible_modules": len(modules), "selected_modules": sum(row["selected"] for row in modules),
                          "checked_modules": sum(row["strict_checked"] for row in modules), "eligible_functions": len(functions),
                          "selected_functions": sum(row["selected"] for row in functions), "checked_functions": sum(row["strict_checked"] for row in functions),
                          "checked_exports": sum(row["public_export"] and row["strict_checked"] for row in boundaries),
                          "selected_records": sum(row["selected"] for row in boundaries if row["kind"] == "record"),
                          "selected_oneofs": sum(row["selected"] for row in boundaries if row["kind"] == "oneof")},
             "boundaries": boundaries, "findings": list(grouped.values()), "policy": _policy(policy),
             "approvals": copy.deepcopy(snapshot.result.integration_approvals), "unsafe_adapters": unsafe}
    return normalize_state(state)


def _reference(root, state, explicit=None, *, required=None, automatic=True):
    policy = state["policy"]["migration"]
    relative = explicit or policy["baseline"]
    if required is None:
        required = explicit is not None or any(policy[key] for key in GATES if key != "reject_expired_approvals")
    if not automatic:
        return None
    if (root / relative).exists() or required:
        return load_reference(root, relative)
    return None


def make_report(snapshot, state, reference=None, *, bootstrap=False):
    comparison = compare_states(reference["state"] if reference else None, state)
    selected_policy = state["policy"]["migration"]
    gates_policy = copy.deepcopy(selected_policy)
    if bootstrap:
        for key in GATES:
            if key != "reject_expired_approvals":
                gates_policy[key] = False
    gates = evaluate_gates(comparison, gates_policy)
    if bootstrap:
        for decision in gates["decisions"]:
            decision["enabled"] = selected_policy[decision["gate"]]
    status = max(state["strict_status"], state["current_policy_status"], gates["status"])
    return {"schema": 1, "kind": "pyalamode-migration-report", "state": state,
            "reference_id": reference["receipt"]["id"] if reference else None,
            "comparison": comparison, "gates": gates, "status": status,
            "verified": status == 0 and not bootstrap and snapshot.freshness == "current disk snapshot",
            "claim_scope": "Current selected source and exact current policy; historical comparison is review evidence, ordinary source is unchecked.",
            "human_measurement": {"status": "UNMEASURED", "participants": 0, "attempts": 0}}


def observe(root, paths=None, *, target=TARGET, compare=None, bootstrap=False):
    from .project import check_snapshot, load_policy
    root = Path(root).resolve()
    inv = inventory(root, paths)
    snapshot = check_snapshot([root], root=root, target=target, cache=False, _migration_history=False)
    if snapshot.result.status == 2 or snapshot.freshness.startswith("stale"):
        reasons = [d.reason for d in snapshot.result.tooling] + [d.reason for file in snapshot.result.results for d in file.diagnostics if d.rule in {"PAL001", "PAL002"}]
        raise MigrationError("; ".join(reasons) or "migration capture failed its tooling/freshness gate")
    policy, error = load_policy(root, root)
    if error:
        raise MigrationError(error)
    state = capture_state(snapshot, policy, inv)
    explicitly_configured = "baseline" in policy.get("migration", {})
    reference = None if bootstrap else _reference(root, state, compare, required=True if explicitly_configured or compare else None)
    report = make_report(snapshot, state, reference, bootstrap=bootstrap)
    return snapshot, state, report, reference


def make_prepublish(snapshot, state, reference_receipts):
    if snapshot.freshness != "current disk snapshot":
        raise MigrationError("durable publication requires current disk evidence")
    root = Path(snapshot.inputs["root"])
    expected_inputs = copy.deepcopy(state["inputs"])
    expected_events = copy.deepcopy(state["current_policy_events"])
    expected_status = (state["strict_status"], state["current_policy_status"])
    def validate():
        from .project import check_snapshot, load_policy
        for receipt in reference_receipts:
            if load_reference(root, receipt["path"])["receipt"] != receipt:
                raise MigrationError("migration reference changed before publication")
        live = check_snapshot([root], root=root, cache=False, _migration_history=False)
        policy, error = load_policy(root, root)
        if error or live.freshness != "current disk snapshot" or live.result.status == 2:
            raise MigrationError("current source/policy/target evidence failed before publication")
        current = capture_state(live, policy, inventory(root))
        if (current["inputs"] != expected_inputs or current["scope"]["selected_paths"] != state["scope"]["selected_paths"]
                or current["current_policy_events"] != expected_events
                or (current["strict_status"], current["current_policy_status"]) != expected_status):
            raise MigrationError("source inventory/resolution/writer, policy, product, integration or UTC expiry changed before publication")
        return None
    return validate


def integrate_team_policy(result, root, policy, target, overlays=None, versions=None):
    """Attach fresh full-project policy to an inherited strict/audit result."""
    from .project import check_snapshot
    metadata = {path: {"text": text, "version": (versions or {}).get(path, 0)} for path, text in (overlays or {}).items()}
    try:
        captured = check_snapshot([root], root=root, target=target, cache=False, overlays=metadata, _migration_history=False)
        if captured.result.status == 2 or captured.freshness.startswith("stale"):
            raise MigrationError("full-project current team-policy capture failed tooling/freshness")
        state = capture_state(captured, policy, inventory(root))
        reference = _reference(root, state, required=True if "baseline" in policy.get("migration", {}) else None,
                               automatic="migration" in policy)
        report = make_report(captured, state, reference)
        result.migration = report
        result.current_policy_status = captured.result.current_policy_status
        result.current_policy_events = copy.deepcopy(state["current_policy_events"])
        result.historical_policy_status = report["gates"]["status"]
        for item in captured.result.policy_diagnostics:
            _project_policy_diagnostic(result, item)
        for event in report["gates"]["diagnostics"]:
            location = event["location"] or _location("pyproject.toml")
            row = event["boundary"]
            _project_policy_diagnostic(result, diagnostic(event["rule"], str(root / location["path"]), event["reason"],
                        line=location["line"], column=location["column"], end_line=location["end_line"], end_column=location["end_column"],
                        column_encoding=location["column_encoding"], boundary=row["qualified_name"] if row else "<module>", origin="migration team policy"))
        result._migration_snapshot = captured
        result._migration_state = state
        result._migration_reference_receipts = [reference["receipt"]] if reference else []
        # Project gates may inspect hidden boundaries, including ordinary writers.
        # Source failures remain source failures for strict commands, while audit
        # keeps inherited non-tooling source status and visible debt.
        if not result.audit and state["strict_status"]:
            result.source_status = max(result.source_status or 0, state["strict_status"])
            for file in captured.result.results:
                for item in file.diagnostics:
                    if item.rule in SOURCE_RULES:
                        target_file = next((out for out in result.results if out.path == file.path), None)
                        if target_file is None:
                            target_file = copy.deepcopy(file)
                            result.results.append(target_file)
                        elif item not in target_file.diagnostics:
                            target_file.diagnostics.append(item)
    except (MigrationError, OSError, ValueError, TypeError, RecursionError) as error:
        result.historical_policy_status = 2
        item = diagnostic("PAL001", str(root / "pyproject.toml"), "migration policy: " + str(error)[:1024], origin="migration team policy")
        _project_policy_diagnostic(result, item)
        if not result.results:
            result.tooling.append(item)


def regions_view(snapshot, state):
    displayed = set(state["scope"]["displayed_paths"])
    rows = [copy.deepcopy(row) for row in state["boundaries"] if row["path"] in displayed]
    return {"schema": 1, "kind": "pyalamode-regions", "status": max(state["strict_status"], state["current_policy_status"]),
            "verified": False, "state": state, "regions": rows,
            "displayed_coverage": {"modules": sum(row["kind"] == "module" for row in rows), "functions": sum(row["kind"] == "function" for row in rows)},
            "unsafe_adapters": [row for row in state["unsafe_adapters"] if row["path"] in displayed]}


def _components(vertices, edges):
    index, stack, on_stack, indices, low, groups = 0, [], set(), {}, {}, []
    def visit(vertex):
        nonlocal index
        indices[vertex] = low[vertex] = index
        index += 1
        stack.append(vertex)
        on_stack.add(vertex)
        for target in sorted(edges.get(vertex, set())):
            if target not in vertices:
                continue
            if target not in indices:
                visit(target)
                low[vertex] = min(low[vertex], low[target])
            elif target in on_stack:
                low[vertex] = min(low[vertex], indices[target])
        if low[vertex] == indices[vertex]:
            group = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                group.append(member)
                if member == vertex:
                    break
            groups.append(sorted(group))
    for vertex in sorted(vertices):
        if vertex not in indices:
            visit(vertex)
    return groups


def _candidate_inventory(snapshot):
    from .checker import _module_name
    root = Path(snapshot.inputs["root"])
    supported, excluded = {}, []
    if snapshot.graph:
        for path, analyzer in snapshot.graph.analyzers.items():
            if path not in snapshot.sources: continue
            if analyzer.tree is None:
                continue
            names = {}
            for node in analyzer.tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.setdefault(node.name, []).append(node)
            for name, nodes in names.items():
                identity = path + "::" + name
                selector = _module_name(path, root) + ":" + name
                node = nodes[0]
                info = analyzer.infos.get(id(node))
                if info:
                    continue
                reason = "duplicate declaration" if len(nodes) != 1 else "async or generic declaration" if not isinstance(node, ast.FunctionDef) or node.type_params else None
                if any(adapter["name"] == name for adapter in analyzer.result.unsafe_adapters):
                    reason = "unsafe ordinary adapter"
                if reason:
                    excluded.append({"selector": selector, "path": _relative(path, root), "reason": reason})
                else:
                    supported[identity] = {"selector": selector, "path": path, "node": node}
    return supported, excluded


def _available_marker(analyzer, node):
    # Validate the existing alias at the actual declaration, with normal source
    # availability and writer rules. No import/decorator is synthesized here.
    from .checker import FunctionInfo
    prior = analyzer.active
    analyzer.active = FunctionInfo(node, analyzer, node.name)
    try:
        options = [(name, ast.Name(id=name, ctx=ast.Load())) for name in sorted(analyzer.marker_names)]
        options += [(name + ".fun", ast.Attribute(value=ast.Name(id=name, ctx=ast.Load()), attr="fun", ctx=ast.Load())) for name in sorted(analyzer.marker_modules)]
        return next((text for text, expression in options if analyzer._marker_valid(expression)), None)
    finally:
        analyzer.active = prior


def ready_view(snapshot, state):
    from .project import check_snapshot
    root = Path(snapshot.inputs["root"])
    candidates, excluded = _candidate_inventory(snapshot)
    overlays = {path: {"text": text, "version": snapshot.inputs["sources"][path]["version"] or 0} for path, text in snapshot.sources.items() if snapshot.inputs["sources"][path]["origin"] == "overlay"}
    hypothetical = check_snapshot([root], root=root, cache=False, overlays=overlays, _candidate_selection={"functions": sorted(candidates), "modules": []}, _migration_history=False)
    graph = hypothetical.graph
    edges = {identity: set() for identity in candidates}
    edge_rows = []
    if graph:
        for identity in candidates:
            info = graph.functions.get(identity)
            if not info:
                continue
            for kind, targets in (("direct", info.calls), ("retained", info.callable_dependencies)):
                for target in sorted(targets):
                    edge_rows.append({"caller": identity, "callee": target, "kind": kind})
                    if target in candidates:
                        edges[identity].add(target)
    components = _components(set(candidates), edges)
    component_of = {member: index for index, group in enumerate(components) for member in group}
    displayed = set(state["scope"]["displayed_paths"])
    disk_checked = {str(root / row["path"]) + "::" + row["qualified_name"]
                    for row in state["boundaries"] if row["kind"] == "function" and row["strict_checked"]}
    groups = []
    for index, group in enumerate(components):
        members = [candidates[identity]["selector"] for identity in group]
        if not any(_relative(candidates[identity]["path"], root) in displayed for identity in group):
            continue
        blockers, prerequisites, external_prerequisites, available = [], [], [], True
        for identity in group:
            item = candidates[identity]
            current_analyzer = snapshot.graph.analyzers[item["path"]]
            marker = _available_marker(current_analyzer, item["node"])
            if marker is None:
                blockers.append({"selector": item["selector"], "reason": "no stable available identity-marker import"})
                available = False
            if item["node"].decorator_list:
                blockers.append({"selector": item["selector"], "reason": "ordinary additional decorators require manual review"})
                available = False
            info = graph.functions.get(identity) if graph else None
            if info:
                for target in sorted(info.calls | info.callable_dependencies):
                    if target in candidates and component_of[target] != index:
                        blockers.append({"selector": item["selector"], "reason": "predecessor component is not adopted on disk", "predecessor": candidates[target]["selector"]})
                    elif target not in candidates:
                        callee = graph.functions.get(target)
                        enclosing = callee.parent if callee else None
                        follows_component = False
                        while enclosing:
                            if enclosing.identity in group:
                                follows_component = True
                                break
                            enclosing = enclosing.parent
                        if not follows_component:
                            if callee and callee.analyzer.path not in snapshot.sources and callee.analyzer.result.verified and not snapshot.result.dependency_status:
                                external_prerequisites.append({"selector":graph.module_name(callee.analyzer.path)+":"+callee.qualified,"dependency":graph.source_owners[callee.analyzer.path],"source_evidence":callee.contract.source_evidence,"failures":list(callee.contract.failures),"trust":list(callee.contract.trust),"effect_bound":list(callee.contract.effect_bound),"required_effects":list(callee.contract.required_effects),"initialization":[{"module":module,"source_evidence":a.result.initialization_evidence,"effects":[] if a.module_mode and a.result.verified else None,"failures":list(a.result.initialization_failures) if a.module_mode and a.result.verified else None,"setup_observations":copy.deepcopy(a.result.setup_observations)} for count in range(1,len(graph.module_name(callee.analyzer.path).split("."))+1) if (module:=".".join(graph.module_name(callee.analyzer.path).split(".")[:count])) in graph.modules and (a:=graph.modules[module])] })
                            elif target in disk_checked:
                                prerequisites.append(target)
                            else:
                                blockers.append({"selector": item["selector"], "reason": "prerequisite lacks current disk strict source proof", "prerequisite": target})
                for diagnostic_ in info.analyzer.result.diagnostics:
                    if diagnostic_.boundary == info.qualified and diagnostic_.rule in SOURCE_RULES:
                        blockers.append({"selector": item["selector"], "reason": diagnostic_.reason, "diagnostic": asdict(diagnostic_)})
            else:
                blockers.append({"selector": item["selector"], "reason": "candidate engine evidence unavailable"})
        hypothetical_contracts = []
        for member in group:
            if graph and graph.functions.get(member) and graph.functions[member].contract:
                contract = asdict(graph.functions[member].contract)
                contract["source_evidence"] = "hypothetical candidate analysis: " + contract["source_evidence"]
                contract["freshness"] = "analysis-only candidate snapshot; current source selection is unchanged"
                hypothetical_contracts.append(contract)
        groups.append({"id": index, "members": members, "physical_members": group, "recursive": len(group) > 1 or any(member in edges[member] for member in group),
                       "current_selected": False, "hypothetical": True, "blockers": blockers, "checked_prerequisites": sorted(set(prerequisites)),"external_prerequisites":external_prerequisites,
                       "predecessor_groups": sorted({component_of[target] for member in group for target in edges[member] if component_of[target] != index}),
                       "preview_available": available, "ready": not blockers,
                       "contracts": hypothetical_contracts})
    modules = []
    for boundary in state["boundaries"]:
        if boundary["kind"] != "module" or boundary["selected"] or boundary["path"] not in displayed:
            continue
        if not boundary["qualified_name"]:
            modules.append({"selector": boundary["selector"], "ready": False, "blockers": ["empty root module has no named conversion target"], "preview_available": False})
            continue
        path = str(root / boundary["path"])
        candidate = check_snapshot([root], root=root, cache=False, overlays=overlays, _candidate_selection={"functions": [], "modules": [path]}, _migration_history=False)
        file = next((file for file in candidate.result.results if file.path == path), None)
        modules.append({"selector": boundary["selector"], "ready": bool(file and file.verified and not candidate.result.current_policy_status),
                        "blockers": [asdict(item) for item in file.diagnostics] if file else ["module evidence unavailable"], "preview_available": True,
                        "candidate_snapshot": candidate.snapshot, "candidate_analysis": candidate.inputs["analysis"]})
    # All eligible ordinary shapes remain visible alongside adoption candidates.
    candidate_selectors = {row["selector"] for row in candidates.values()}
    excluded_selectors = {row["selector"] for row in excluded}
    for row in state["boundaries"]:
        if row["kind"] == "function" and not row["selected"] and row["selector"] not in candidate_selectors | excluded_selectors:
            excluded.append({"selector": row["selector"], "path": row["path"], "reason": "nested or method adoption follows its supported enclosing boundary"})
    return {"schema": 1, "kind": "pyalamode-readiness", "status": max(state["strict_status"], state["current_policy_status"]),
            "verified": False, "state": state, "groups": groups, "modules": modules, "edges": edge_rows,
            "excluded_candidates": excluded, "candidate_status": hypothetical.result.status,
            "candidate_snapshot": hypothetical.snapshot, "candidate_analysis": hypothetical.inputs["analysis"],
            "limits": "Hypothetical engine selection discovers dependencies; actual source marker availability and complete current policy must pass the conversion overlay recheck."}


def _physical_lines(text):
    import re
    return [match.group() for match in re.finditer(r"[^\r\n]*(?:\r\n|\r|\n|$)", text) if match.group()]


def _newline(text):
    return "\r\n" if "\r\n" in text else "\r" if "\r" in text and "\n" not in text else "\n"


def _insert_module_comment(text, tree):
    lines = _physical_lines(text)
    index = 1 if lines and lines[0].startswith("#!") else 0
    for position_, line in enumerate(lines[:2]):
        if "coding" in line and line.lstrip().startswith("#"):
            index = max(index, position_ + 1)
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and type(tree.body[0].value.value) is str:
        index = max(index, tree.body[0].end_lineno)
    if index and not lines[index - 1].endswith(("\r", "\n")):
        lines[index - 1] += _newline(text)
    lines.insert(index, "# mode: fun" + _newline(text))
    return "".join(lines)


def _preview_result(snapshot, state, target, *, status, blockers, edits=None, candidate=None, component=None, limits=""):
    return {"schema": 1, "kind": "pyalamode-conversion-preview", "target": target,
            "component": component or [target], "status": status, "verified": bool(status == 0 and candidate and candidate.result.verified and not candidate.freshness.startswith("stale")),
            "snapshot": snapshot.snapshot, "inputs": copy.deepcopy(state["inputs"]), "edits": edits or [],
            "blockers": blockers, "candidate": candidate.result.to_dict() if candidate else None,
            "candidate_snapshot": candidate.snapshot if candidate else None,
            "candidate_inputs": copy.deepcopy(candidate.inputs) if candidate else None,
            "candidate_freshness": candidate.freshness if candidate else None,
            "retained_dimensions": [field.name for field in fields(FunctionContract)] + ["records", "oneofs", "initialization", "setup_observations", "untargeted input identities"],
            "limits": limits, "applied": False}


def convert_preview(snapshot, state, target):
    from .project import check_snapshot
    from .checker import _module_name
    if type(target) is not str:
        raise MigrationError("conversion requires one exact kind-prefixed target")
    parts = target.split(":")
    if parts[0] == "function" and len(parts) == 3:
        kind, module, name = parts
        if not module or not name or any(not part.isidentifier() for part in (module + "." + name).split(".")):
            raise MigrationError("malformed exact function conversion selector")
        selector = module + ":" + name
    elif parts[0] == "module" and len(parts) == 2:
        kind, module = parts
        if not module or any(not part.isidentifier() for part in module.split(".")):
            raise MigrationError("conversion requires a named exact module")
        name, selector = module, target
    else:
        raise MigrationError("use function:module:qualified.function or module:module.name")
    matches = [row for row in state["boundaries"] if row["kind"] == kind and row["selector"] == selector]
    if len(matches) != 1:
        raise MigrationError("unknown or ambiguous authored conversion target: " + target)
    boundary = matches[0]
    root = Path(snapshot.inputs["root"])
    path = str(root / boundary["path"])
    analyzer = snapshot.graph.analyzers[path]
    repair_relation = None
    if boundary["selected"] and kind == "function":
        findings = [row for row in state["findings"] if row["logical_boundary"] == _logical(boundary)]
        repair = next((row for row in findings if row["rule"] in {"PAL101", "PAL250"}), None)
        if repair:
            from .editor import EditorSession, ProtocolError
            session = EditorSession(root)
            session.documents = {source: {"text": text, "version": snapshot.inputs["sources"][source]["version"] or 0} for source, text in snapshot.sources.items()}
            session.refresh()
            item = next((row for row in session.diagnostics if row["uri"] == Path(path).as_uri() and row["data"]["boundary"] == name and row["code"] == repair["rule"]), None)
            if item:
                try:
                    proposal = session.preview({"uri": Path(path).as_uri(), "version": session.documents[path]["version"],
                                               "snapshot": session.current.snapshot, "diagnosticIndex": item["data"]["diagnosticIndex"]})
                    after = proposal["after"]
                    repair_relation = session._last_repair_relation
                except ProtocolError as error:
                    return _preview_result(snapshot, state, target, status=max(1, state["current_policy_status"]), blockers=[str(error)], limits="Inherited conservative M9 repair refusal.")
            else:
                return _preview_result(snapshot, state, target, status=1, blockers=["supported repair diagnostic unavailable"])
        elif boundary["strict_checked"]:
            return _preview_result(snapshot, state, target, status=max(state["strict_status"], state["current_policy_status"]), blockers=[], limits="Already participating; no source edit proposed.")
        else:
            return _preview_result(snapshot, state, target, status=1, blockers=["current source has no finite safe repair"])
        changed = {path: after}
        component = [selector]
    elif kind == "module":
        if boundary["selected"]:
            return _preview_result(snapshot, state, target, status=max(state["strict_status"], state["current_policy_status"]), blockers=[], limits="Module already participating; no source edit proposed.")
        changed = {path: _insert_module_comment(snapshot.sources[path], analyzer.tree)}
        component = [selector]
    else:
        candidates, _ = _candidate_inventory(snapshot)
        physical = path + "::" + name
        if physical not in candidates:
            return _preview_result(snapshot, state, target, status=1, blockers=["adoption requires a unique supported ordinary top-level function"])
        ready = ready_view(snapshot, state)
        group = next((group for group in ready["groups"] if physical in group["physical_members"]), None)
        if group is None:
            return _preview_result(snapshot, state, target, status=1, blockers=["candidate component unavailable"])
        blockers = [row for row in group["blockers"] if "predecessor" in row or row["reason"] in {"no stable available identity-marker import", "ordinary additional decorators require manual review"}]
        if blockers:
            return _preview_result(snapshot, state, target, status=1, blockers=blockers, component=group["members"])
        insertions = {}
        for member in group["physical_members"]:
            item = candidates[member]
            node = item["node"]
            if node.args.vararg or node.args.kwarg or node.type_params:
                return _preview_result(snapshot, state, target, status=1, blockers=["variadic or generic adoption requires manual review"])
            marker = _available_marker(snapshot.graph.analyzers[item["path"]], node)
            if marker is None:
                return _preview_result(snapshot, state, target, status=1, blockers=["actual marker availability is not established"])
            authored_line = _authored_location(snapshot,item["path"],item["path"],node)["line"]
            insertions.setdefault(item["path"], []).append((authored_line - 1, "@" + marker + _newline(snapshot.sources[item["path"]])))
        changed = {}
        for source, rows in insertions.items():
            lines = _physical_lines(snapshot.sources[source])
            for line, text in sorted(rows, reverse=True):
                lines.insert(line, text)
            changed[source] = "".join(lines)
        component = group["members"]
    edits = []
    for source, after in sorted(changed.items()):
        from .project import _owned_source_bytes
        raw = _owned_source_bytes(source, root)
        encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
        if encoding.lower().replace("_", "-") not in {"utf-8", "utf-8-sig"}:
            return _preview_result(snapshot, state, target, status=1, blockers=["source encoding has no supported finite preview"], component=component)
        before = snapshot.sources[source]
        edits.append({"path": _relative(source, root), "before": before, "after": after,
                      "diff": "".join(difflib.unified_diff(_physical_lines(before), _physical_lines(after), fromfile=source, tofile=source + " (preview)"))})
    overlays = {source: {"text": text, "version": snapshot.inputs["sources"][source]["version"] or 0} for source, text in snapshot.sources.items() if snapshot.inputs["sources"][source]["origin"] == "overlay"}
    overlays.update({source: {"text": text, "version": snapshot.inputs["sources"][source]["version"] or 0} for source, text in changed.items()})
    candidate = check_snapshot([root], root=root, cache=False, overlays=overlays)
    blockers = []
    if candidate.freshness.startswith("stale"):
        blockers.append("candidate input snapshot is stale")
    for key in ("policy_sha256", "product_artifacts", "integration_inputs", "checked_dependencies"):
        if candidate.inputs[key] != snapshot.inputs[key]:
            blockers.append("untargeted input changed: " + key)
    if set(candidate.inputs["sources"]) != set(snapshot.inputs["sources"]):
        blockers.append("source/import/writer inventory changed during preview")
    for source, row in snapshot.inputs["sources"].items():
        after = candidate.inputs["sources"].get(source)
        if after is None or (source not in changed and row != after) or (source in changed and row["disk_sha256"] != after["disk_sha256"]):
            blockers.append("untargeted source/disk identity changed: " + source)
    from .project import _contract_comparison, _occurrence_relation, _file_dimensions_equal
    for file in snapshot.result.results:
        other = next((file_ for file_ in candidate.result.results if file_.path == file.path), None)
        relation = _occurrence_relation(snapshot,candidate,file.path) if file.path in changed else None
        # Adoption changes the reviewed target's participation. Repair and all
        # untargeted files retain their complete declaration/init/setup facts.
        if (repair_relation is not None or file.path not in changed) and (other is None or not _file_dimensions_equal(file,other,relation=relation,repair=repair_relation if file.path == path else None)):
            blockers.append("existing declaration/initialization/setup dimensions changed: " + file.path)
        for old in file.contracts:
            new = next((contract for contract in other.contracts if contract.name == old.name), None) if other else None
            repair_ = repair_relation if file.path == path and old.name == name else None
            comparison = _contract_comparison(old,new,relation=relation,repair=repair_) if new is not None else None
            demotion = {"source_evidence": "unverified: audit or failed selected gate",
                "freshness": "no successful checked claim", "behavior": "unverified behavior; no certified effect bound"}
            if (comparison is not None and not comparison["matched"] and kind == "function" and repair_relation is None
                    and file.path in changed and candidate.result.status == 1 and candidate.result.source_status == 1
                    and not snapshot.result.audit and not candidate.result.audit and other.diagnostics
                    and old.source_evidence == "checked participating source" and old.freshness == "current for recorded inputs"
                    and old.behavior == ("pure" if not old.effect_bound else "effects <= {" + ", ".join(old.effect_bound) + "}")
                    and all(getattr(new,key) == value for key,value in demotion.items())):
                expected = asdict(old)
                expected.update(demotion)
                if _contract_comparison(expected,new,relation=relation)["matched"]:
                    blockers.append({"reason": "candidate source refusal demotes existing local evidence",
                        "boundary": _module_name(file.path, root) + ":" + old.name,
                        "demotion_fields": sorted(demotion), "contract_comparison": comparison})
                    continue
            if comparison is None or not comparison["matched"]:
                blockers.append("existing participating dimensions changed: " + _module_name(file.path, root) + ":" + old.name)
    dimension_blockers = [row for row in blockers if not (type(row) is dict
        and set(row) == {"reason", "boundary", "demotion_fields", "contract_comparison"}
        and row["reason"] == "candidate source refusal demotes existing local evidence")]
    status = max(candidate.result.status, 2 if any("changed" in str(row) or "stale" in str(row) for row in dimension_blockers) else 0)
    if candidate.result.status:
        blockers += [asdict(item) for item in candidate.result.tooling] + [asdict(item) for file in candidate.result.results for item in file.diagnostics]
    return _preview_result(snapshot, state, target, status=status, blockers=blockers, edits=edits, candidate=candidate,
                           component=component, limits="Read-only full-project overlay rechecked by the actual engine without hypothetical selection; no permission, trust, source or baseline edit was applied.")
