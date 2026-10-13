"""Local check/build gate and disposable content-addressed analysis cache."""

from __future__ import annotations

import hashlib
import copy
import io
import json
import os
import platform
import shutil
import sys
import tempfile
import time
import tomllib
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

from .checker import (SourceGraph, analyze_file, analyze_source, fingerprint, load_sources, _import_name,
                      _local_path, _module_name, source_owner, source_provenance, public_result,
                      translator_identity, map_bytes)
from . import source_maps as sm
from . import syntax
import ast
import difflib
from .model import (CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, CheckResult,
                    Diagnostic, FunctionContract, diagnostic, foundation_identities, runtime_environment,
                    EXPERIMENTAL_EDITION, SYNTAX_VERSION, SOURCE_MAP_SCHEMA)
from .encoding_contracts import ENCODING_VERSION, operation_catalog as encoding_catalog
from .builder_contracts import BUILDER_VERSION, operation_catalog as builder_catalog
from .task_contracts import TASK_VERSION, operation_catalog as task_catalog
from .standard_contracts import STANDARD_VERSION, operation_catalog
from .integration_contracts import INTEGRATION_VERSION, integration_snapshot, validate_policy

_EXCLUDED = frozenset({".git", ".venv", "__pycache__", "build", "dist", ".pyalamode-cache", ".pyalamode"})

# Only fresh source derivations can authorize reuse of disposable payloads.
_SOURCE_CACHE_IDENTITIES: dict[tuple[int, str, str, str], str] = {}


@dataclass
class ProjectResult:
    results: list[CheckResult] = field(default_factory=list)
    tooling: list[Diagnostic] = field(default_factory=list)
    audit: bool = False
    elapsed_seconds: float = 0.0
    output: str | None = None
    boundary_guards: str = "off"
    guarded_exports: list[dict] = field(default_factory=list)
    debug_coverage: list[dict] = field(default_factory=list)
    integration_catalog: list[dict] = field(default_factory=list)
    integration_approvals: list[dict] = field(default_factory=list)
    source_status: int | None = None
    current_policy_status: int = 0
    historical_policy_status: int = 0
    policy_diagnostics: list[Diagnostic] = field(default_factory=list)
    migration: dict | None = None
    current_policy_events: dict = field(default_factory=lambda: {"required_exports": [], "expired_approvals": [], "approval_failures": []})

    distribution_inputs: dict = field(default_factory=dict)
    checked_dependencies: list = field(default_factory=list)
    dependency_status: int = 0
    dependency_events: list = field(default_factory=list)
    distribution: dict | None = None
    analysis_counts: dict = field(default_factory=dict)
    selected_edition: str = EDITION

    @property
    def status(self) -> int:
        # Source refusals can arrive during build publication after the initial
        # source axis was saved. Policy projections are not source diagnostics.
        source = self.source_status or 0
        for file in self.results:
            rows = [d for d in file.diagnostics if d.rule not in {"PAL360", "PAL361", "PAL362", "PAL363", "PAL364", "PAL365", "PAL366", "PAL367"}]
            source = max(source, 2 if any(d.rule in {"PAL001", "PAL002"} for d in rows) else int(bool(rows) and file.mode == "strict"))
        return max(source, 0 if self.audit else self.dependency_status, self.current_policy_status, self.historical_policy_status, 2 if self.tooling else 0)

    @property
    def verified(self) -> bool:
        return not self.audit and self.status == 0

    def to_dict(self) -> dict:
        from dataclasses import asdict
        return {"schema": 1, "edition": self.selected_edition, "checker": CHECKER_VERSION, "target": TARGET,
                "syntax_version": SYNTAX_VERSION, "source_map_schema": SOURCE_MAP_SCHEMA,
                "operation_contract": OPERATION_VERSION, "product_artifacts": foundation_identities(),
                "runtime_environment": runtime_environment(),
                "encoding_operation_version": ENCODING_VERSION, "encoding_catalog": encoding_catalog(),
                "builder_operation_version": BUILDER_VERSION, "builder_catalog": builder_catalog(),
                "task_operation_version": TASK_VERSION, "task_catalog": task_catalog(),
                "standard_operation_version": STANDARD_VERSION, "standard_catalog": operation_catalog(),
                "integration_version": INTEGRATION_VERSION, "integration_catalog": copy.deepcopy(self.integration_catalog),
                "integration_approvals": copy.deepcopy(self.integration_approvals),
                "distribution_inputs": copy.deepcopy(self.distribution_inputs), "checked_dependencies": copy.deepcopy(self.checked_dependencies),
                "dependency_status": self.dependency_status, "dependency_events": copy.deepcopy(self.dependency_events), "distribution": copy.deepcopy(self.distribution),
                "analysis_counts": copy.deepcopy(self.analysis_counts),
                "mode": "audit" if self.audit else "strict",
                "verified": self.verified, "status": self.status,
                "source_status": self.source_status if self.source_status is not None else self.status,
                "current_policy_status": self.current_policy_status,
                "historical_policy_status": self.historical_policy_status,
                "policy_diagnostics": [asdict(d) for d in self.policy_diagnostics],
                "migration": copy.deepcopy(self.migration),
                "elapsed_seconds": self.elapsed_seconds, "output": self.output,
                "boundary_guards": self.boundary_guards, "guarded_exports": self.guarded_exports,
                "debug_coverage": self.debug_coverage,
                "tooling": [asdict(d) for d in self.tooling],
                "files": [r.to_dict() for r in self.results],
                "coverage": {"eligible_functions": sum(r.eligible_functions for r in self.results),
                             "eligible_modules": sum(not any(d.rule == "PAL001" for d in r.diagnostics) for r in self.results),
                             "selected_functions": sum(r.selected_functions for r in self.results),
                             "selected_records": sum(len(r.records) for r in self.results),
                             "selected_oneofs": sum(len(r.oneofs) for r in self.results),
                             "analyzed_call_sites": sum(r.analyzed_call_sites for r in self.results)},
                "claim_scope": "Selected functions, record/oneof declarations, stable dependencies and functional-module initialization; ordinary shells and unrelated ordinary initialization are unchecked."}


@dataclass
class ProjectSnapshot:
    """Read-only captured full-project evidence, including explicit unsaved provenance."""
    result: ProjectResult
    sources: dict[str, str]
    inputs: dict
    freshness: str
    snapshot: str
    graph: SourceGraph | None = field(default=None, repr=False)
    source_units: dict = field(default_factory=dict, repr=False)


def _contract_comparison(before, after, *, relation=None, repair=None):
    """Closed, detached comparison of all actual FunctionContract fields.

    Relations are supplied by the caller from captured owners and paired AST
    occurrences. Foreign provenance and catalog/approval records remain exact.
    """
    from dataclasses import fields, asdict, is_dataclass
    before = asdict(before) if is_dataclass(before) else copy.deepcopy(before)
    after = asdict(after) if is_dataclass(after) else copy.deepcopy(after)
    names = tuple(item.name for item in fields(FunctionContract))
    if type(before) is not dict or type(after) is not dict or set(before) != set(names) or set(after) != set(names):
        raise ValueError("contract comparison requires both complete closed contracts")
    relation = relation or {}
    if type(relation) is not dict or set(relation) - {"owners", "occurrences", "aliases"}:
        raise ValueError("unknown contract occurrence relation")
    owners = relation.get("owners", {})
    occurrences = relation.get("occurrences", {})
    aliases = relation.get("aliases", {})
    if any(type(value) is not dict for value in (owners, occurrences, aliases)):
        raise ValueError("contract relation requires explicit identity maps")
    targets = {"dependencies", "callable_targets", "callable_defaults", "return_callable_targets",
        "invoked_targets", "callable_dependencies", "callable_arguments", "targets", "target", "callback_targets", "callback"}
    located = {"line", "end_line", "callback_line", "callback_end_line"}
    exact = {"parameters", "parameter_kinds", "defaults", "captures", "trust", "caller_obligations",
        "capability_parameters", "operation_contracts", "external_assumptions", "effect_bound", "required_effects",
        "failures", "definition_failures", "direct_failures", "boundary_protection", "enforcement", "name"}
    def normalize(value, key=None, target=False):
        target = target or key in targets
        if type(value) is dict:
            out = {k: normalize(v, k, target) for k, v in value.items()}
            for lk, ck in (("line", "column"), ("end_line", "end_column")):
                if type(value.get(lk)) is int and type(value.get(ck)) is int:
                    pair = occurrences.get(str(value[lk])+":"+str(value[ck]))
                    if pair is not None: out[lk], out[ck] = pair
            return out
        if type(value) is list:
            return [normalize(v, key, target) for v in value]
        if type(value) is int and key in located:
            return occurrences.get(str(value), value)
        if type(value) is str:
            if key == "path" or target:
                if value in owners: return owners[value]
                if "::" in value:
                    owner, tail = value.split("::", 1)
                    if owner in owners: return owners[owner] + "::" + tail
            if key in {"returns", "schema", "operation"} or target:
                return aliases.get(value, value)
        return value
    expected = copy.deepcopy(before)
    if repair is not None:
        keys = {"rule", "line", "old_name", "new_name", "schema", "missing_assertion", "sole_gate", "candidate_verified"}
        if type(repair) is not dict or set(repair) != keys or repair["rule"] not in {"PAL101", "PAL250"} or repair["sole_gate"] is not True or repair["candidate_verified"] is not True:
            raise ValueError("unproven contract repair relation")
        if type(repair["line"]) is not int or type(repair["schema"]) is not str or type(repair["new_name"]) is not str:
            raise ValueError("invalid repair occurrence/schema")
        row = {"line": repair["line"], "name": repair["new_name"], "schema": repair["schema"]}
        if repair["rule"] == "PAL101" and not repair["missing_assertion"]:
            matches = [r for r in expected["data_assertions"] if r == {**row, "name": repair["old_name"]}]
            if len(matches) != 1: raise ValueError("old second assertion is not the proven exact occurrence/schema")
            expected["data_assertions"][expected["data_assertions"].index(matches[0])] = row
        else:
            if any(r["line"] == row["line"] and r["name"] in {repair["old_name"], repair["new_name"]} for r in expected["data_assertions"]):
                raise ValueError("repair cannot duplicate an existing assertion occurrence")
            expected["data_assertions"].append(row)
            expected["data_assertions"].sort(key=lambda r: (r["line"], r["name"]))
        transitions = {"source_evidence": ("unverified: audit or failed selected gate", "checked participating source"),
            "freshness": ("no successful checked claim", "current for recorded inputs"),
            "behavior": ("unverified behavior; no certified effect bound", "pure" if not before["effect_bound"] else "effects <= {" + ", ".join(before["effect_bound"]) + "}")}
        for key, (old, new) in transitions.items():
            if before[key] != old: raise ValueError("repair cannot promote an unrelated evidence refusal")
            expected[key] = new
    rows = []
    for name in names:
        left = expected[name] if name in exact else normalize(expected[name], name)
        right = after[name]
        rows.append({"field": name, "before": copy.deepcopy(before[name]), "after": copy.deepcopy(right),
            "matched": left == right, "rule": "closed-repair" if repair and name in {"data_assertions", "source_evidence", "freshness", "behavior"} else "exact" if name in exact else "owned-occurrence"})
    return {"matched": all(row["matched"] for row in rows), "fields": rows}


def _file_dimensions_equal(before, after, *, relation=None, diagnostics=False, repair=None):
    """Compare complete non-contract source facts through owned typed sites."""
    from dataclasses import asdict
    relation = relation or {}
    owners, points = relation.get("owners", {}), relation.get("occurrences", {})
    def remap(value, key=None):
        if type(value) is list: return [remap(v, key) for v in value]
        if type(value) is dict:
            row = {k: remap(v, k) for k,v in value.items()}
            for lk, ck in (("line", "column"), ("end_line", "end_column")):
                if type(value.get(lk)) is int and type(value.get(ck)) is int:
                    pair = points.get(str(value[lk])+":"+str(value[ck]))
                    if pair is not None: row[lk], row[ck] = pair
            return row
        if type(value) is int and key in {"line", "end_line", "callback_line", "callback_end_line"}: return points.get(str(value),value)
        if type(value) is str and key == "path": return owners.get(value,value)
        if type(value) is str and key == "first_binding" and value:
            for path in (before.path, *owners):
                if value.startswith(path+":"):
                    tail = value[len(path)+1:].split(":")
                    if len(tail) in {1,2} and all(v.isdecimal() for v in tail):
                        if len(tail) == 2 and ":".join(tail) in points:
                            tail = [str(v) for v in points[":".join(tail)]]
                        else: tail[0] = str(points.get(tail[0],int(tail[0])))
                        return owners.get(path,path)+":"+":".join(tail)
        return value
    fields = ("eligible_functions", "selected_functions", "analyzed_call_sites", "mode", "module_mode",
        "initialization_evidence", "initialization_failures", "binding_context", "records", "oneofs",
        "setup_observations", "unsafe_adapters", "integration_inputs")
    for key in fields:
        expected = remap(copy.deepcopy(getattr(before,key)))
        if (key == "initialization_evidence" and repair is not None and repair["sole_gate"] is True
                and repair["candidate_verified"] is True and before.module_mode and after.verified
                and len(before.diagnostics) == 1 and before.diagnostics[0].rule == repair["rule"]
                and before.diagnostics[0].line == repair["line"] and expected == "unverified initialization"):
            expected = "checked pure source initialization"
        if expected != getattr(after,key): return False
    return not diagnostics or remap([asdict(d) for d in before.diagnostics]) == [asdict(d) for d in after.diagnostics]


def _repair_schema(snapshot, path, name, statement_index):
    """Resolve the original pre-refusal RHS in its actual finite lexical env."""
    from .checker import Binding, _written_names
    analyzer = snapshot.graph.analyzers[path]
    info = next((i for i in analyzer.infos.values() if i.qualified == name), None)
    if info is None or type(statement_index) is not int or not 0 <= statement_index < len(info.node.body): return None
    env = {arg: Binding(analyzer.annotation_value(kind), (info.node.lineno,)) for arg, kind in info.parameters.items()}
    previous = analyzer.active, analyzer.locals, analyzer.definition_mode, analyzer.boundary
    analyzer.active, analyzer.locals, analyzer.definition_mode, analyzer.boundary = info, set(_written_names(info.node.body)) | set(info.parameters), False, name
    try:
        for index, node in enumerate(info.node.body[:statement_index + 1]):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if len(targets) != 1 or not isinstance(targets[0], ast.Name) or node.value is None: return None
                value = analyzer._expr(node.value, env, quiet=True)
                if value.kind is None or not analyzer._data_value(value): return None
                if isinstance(node, ast.AnnAssign):
                    expected = analyzer._annotation(node.annotation, extra_names=set(analyzer.locals)-set(env))
                    if expected != value.kind: return None
                if index == statement_index: return value.kind
                env[targets[0].id] = Binding(value, (node.lineno, node.col_offset + 1))
            elif index == statement_index and isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                value = analyzer._expr(node.value, env, quiet=True)
                return value.kind if value.kind and analyzer._data_value(value) else None
            elif not isinstance(node, (ast.Pass, ast.Expr)): return None
        return None
    finally:
        analyzer.active, analyzer.locals, analyzer.definition_mode, analyzer.boundary = previous


def _occurrence_relation(before, after, path):
    """Pair actual structural AST sites; never match by neighboring line text."""
    from .migration_views import _authored_location
    left, right = before.graph.analyzers[path].tree, after.graph.analyzers[path].tree
    points, lines, conflicts = {}, {}, set()
    def visit(a, b):
        if type(a) is not type(b): return
        if isinstance(a, ast.AST):
            if getattr(a, "end_lineno", None) is not None:
                old = _authored_location(before, path, path, a)
                new = _authored_location(after, path, path, b)
                for lk, ck in (("line", "column"), ("end_line", "end_column")):
                    if old[lk] is None or new[lk] is None: continue
                    points[str(old[lk])+":"+str(old[ck])] = [new[lk], new[ck]]
                    key = str(old[lk])
                    if key in lines and lines[key] != new[lk]: conflicts.add(key)
                    lines[key] = new[lk]
            for field in a._fields: visit(getattr(a, field), getattr(b, field))
        elif type(a) is list and len(a) == len(b):
            for x, y in zip(a, b): visit(x, y)
    visit(left, right)
    return {"owners": {}, "occurrences": {**{k:v for k,v in lines.items() if k not in conflicts}, **points}, "aliases": {}}


def format_paths(paths=None, *, root=None, mode="preview", overlays=None):
    """Read-only formatter proposal with an actual full-project parity gate."""
    from dataclasses import asdict
    if mode not in {"preview", "check"}: raise ValueError("unknown format mode")
    project_root = Path(root or Path.cwd()).resolve()
    snapshot = check_snapshot([project_root], root=project_root, cache=False, overlays=overlays)
    chosen, errors = discover_paths(list(paths or [project_root]), project_root)
    rows, proposals, diagnostics = [], {}, [asdict(d) for d in errors]
    source_status, refused = 0, bool(errors or snapshot.result.tooling)
    diagnostics += [asdict(d) for d in snapshot.result.tooling]
    for path in chosen:
        if path.suffix != ".pya":
            diagnostics.append(asdict(diagnostic("PAL001", str(path), "format requires an actual .pya owner", origin="format selection"))); refused = True; continue
        unit = snapshot.source_units.get(str(path))
        if unit is None:
            refused = True; continue
        empty = unit.translation.empty_types if unit.translation else ()
        formatted = syntax.format_source(unit.authored_bytes, unit.owner, edition=unit.selected_edition,
            translator=translator_identity(), empty_types=empty)
        source_status = max(source_status, formatted.source_status)
        diagnostics += [asdict(d) for file in snapshot.result.results if file.path == str(path) for d in file.diagnostics]
        valid = formatted.status != 2 and formatted.after is not None
        refused |= not valid
        before = unit.authored_bytes.decode("utf-8") if unit.encoding != "utf-8-invalid" else None
        after = formatted.after.decode("utf-8") if valid else None
        changed = bool(valid and formatted.after != unit.authored_bytes)
        if valid: proposals[str(path)] = {"text": after, "version": snapshot.inputs["sources"][str(path)]["version"] or 0}
        rows.append({"path": path.relative_to(project_root).as_posix(), "version": snapshot.inputs["sources"][str(path)]["version"],
            "before_sha256": hashlib.sha256(unit.authored_bytes).hexdigest(), "after_sha256": hashlib.sha256(formatted.after).hexdigest() if valid else None,
            "before": before if mode == "preview" else None, "after": after if mode == "preview" and valid else None,
            "edits": [{"start": e.span.start, "end": e.span.end, "replacement": e.replacement.decode("utf-8")} for e in formatted.edits] if mode == "preview" and valid else [],
            "diff": "".join(difflib.unified_diff(io.StringIO(before, newline="").readlines(), io.StringIO(after, newline="").readlines(), fromfile=str(path), tofile=str(path)+" (preview)")) if mode == "preview" and valid else None,
            "changed": changed, "source_provenance": source_provenance(unit)})
    candidate = None
    if not refused:
        candidate = check_snapshot([project_root], root=project_root, cache=False, overlays={**(overlays or {}), **proposals})
        for file in snapshot.result.results:
            other = next((f for f in candidate.result.results if f.path == file.path), None)
            if other is None or len(file.contracts) != len(other.contracts): refused = True; break
            relation = _occurrence_relation(snapshot,candidate,file.path)
            if not _file_dimensions_equal(file,other,relation=relation,diagnostics=True): refused = True; break
            for old in file.contracts:
                new = next((c for c in other.contracts if c.name == old.name), None)
                if new is None or not _contract_comparison(old, new, relation=relation)["matched"]: refused = True; break
        if snapshot.inputs["product_artifacts"] != candidate.inputs["product_artifacts"] or snapshot.inputs["policy_sha256"] != candidate.inputs["policy_sha256"] or snapshot.inputs["integration_inputs"] != candidate.inputs["integration_inputs"] or snapshot.inputs["checked_dependencies"] != candidate.inputs["checked_dependencies"]:
            refused = True
        if set(snapshot.inputs["sources"]) != set(candidate.inputs["sources"]): refused = True
        for path, old in snapshot.inputs["sources"].items():
            new = candidate.inputs["sources"].get(path)
            if new is None or (path not in proposals and old != new) or (path in proposals and old["disk_sha256"] != new["disk_sha256"]): refused = True
        for path, unit in snapshot.source_units.items():
            if unit.dependency_owner is None and hashlib.sha256(_owned_source_bytes(path, project_root)).hexdigest() != snapshot.inputs["sources"][path]["disk_sha256"]:
                refused = True
        refused |= snapshot.freshness.startswith("stale") or candidate.freshness.startswith("stale")
    if refused:
        for row in rows: row.update(after=None, after_sha256=None, edits=[], diff=None, changed=False)
    return {"schema": 1, "kind": "pyalamode-format", "mode": mode, "status": 2 if refused else int(any(r["changed"] for r in rows)),
        "source_status": source_status, "strict_status": candidate.result.status if candidate else snapshot.result.status,
        "applied": False, "snapshot": snapshot.snapshot, "freshness": snapshot.freshness, "inputs": copy.deepcopy(snapshot.inputs), "files": rows, "diagnostics": diagnostics}


def locate_source(*, artifact, path, line, column, root=None):
    """Read exact owned artifacts; malformed and valid stale inputs are distinct."""
    from .distribution import read, bounded, relative, shape, sha, DistributionError, _pairs
    from .checker import prepare_units
    base = Path(artifact).absolute()
    result = {"schema": 1, "kind": "pyalamode-source-location", "status": 2, "verified": False,
        "artifact": str(base), "generated": {"path": path, "line": line, "column": column, "column_encoding": "utf-8-bytes", "sha256": None},
        "authored": None, "exact": None, "segments": [], "snapshot": hashlib.sha256(b"").hexdigest(),
        "inputs": {"evidence_sha256": None, "product_artifacts": foundation_identities(), "artifacts": {}}, "diagnostics": []}
    try:
        relative(path)
        if not path.endswith(".py") or type(line) is not int or type(column) is not int or min(line, column) < 1:
            raise ValueError("query requires ordinary owned .py and positive exact byte coordinates")
        if base.is_symlink() or not base.is_dir() or any(p.is_symlink() for p in base.parents): raise ValueError("artifact must be a regular owned directory")
        evidence_raw = read(base/"pyalamode-evidence.json", 16*1024*1024)
        evidence = json.loads(evidence_raw, object_pairs_hook=_pairs, parse_constant=lambda _: (_ for _ in ()).throw(DistributionError("nonfinite directory evidence JSON")))
        if type(evidence) is not dict:
            raise DistributionError("directory evidence requires an exact object")
        elapsed = evidence.get("elapsed_seconds")
        if type(elapsed) is not float or not 0 <= elapsed < 2**63:
            raise DistributionError("directory elapsed_seconds requires a bounded finite nonnegative float")
        # Directory timing is the sole float; all evidence bounds remain intact.
        bounded({**evidence, "elapsed_seconds": 0})
        result["inputs"]["evidence_sha256"] = hashlib.sha256(evidence_raw).hexdigest()
        inventory = evidence["artifact_files"]
        if type(inventory) is not dict or not inventory: raise ValueError("artifact requires complete byte inventory")
        actual = {}
        for name, digest in inventory.items():
            relative(name); sha(digest)
            maximum = 32*1024*1024 if name.endswith(".map.json") else 8*1024*1024 if name.endswith(".py") else 1024*1024
            raw = read(base/name, maximum)
            actual[name] = hashlib.sha256(raw).hexdigest()
        result["inputs"]["artifacts"] = actual
        result["snapshot"] = hashlib.sha256(json.dumps({"evidence": result["inputs"]["evidence_sha256"], "artifacts": actual}, sort_keys=True).encode()).hexdigest()
        if actual != inventory or evidence.get("product_artifacts") != foundation_identities() or evidence.get("verified") is not True or evidence.get("status") != 0:
            result["status"] = 1; return result
        syntax_rows = evidence["syntax_artifacts"]; shape(syntax_rows, {"schema", "translator", "modules"})
        if syntax_rows["schema"] != 1 or syntax_rows["translator"] != {"version": SYNTAX_VERSION, "files": dict(translator_identity().files)}:
            raise ValueError("unsupported syntax artifact translator")
        rows = syntax_rows["modules"]
        selected = None
        for name, row in rows.items():
            shape(row, {"owner", "edition", "authored", "normalized", "runtime", "authored_copy_path", "lowered_copy_path", "map_path", "map_sha256", "runtime_map_path", "runtime_map_sha256", "facades"})
            owner = sm.SourceOwner(**row["owner"])
            if name != owner.module or row["edition"] != EXPERIMENTAL_EDITION: raise ValueError("unowned syntax module")
            if owner.runtime_path == path: selected = (row, row["runtime_map_path"], row["runtime_map_sha256"], row["runtime"])
            for facade in row["facades"]:
                shape(facade, {"path", "map_path", "map_sha256"})
                if facade["path"] == path:
                    raw_ = read(base/path, 8*1024*1024)
                    selected = (row, facade["map_path"], facade["map_sha256"], as_owner(sm.source_identity(raw_, path=path, edition=EDITION, role="facade")))
        if selected is None: raise ValueError("queried artifact has no owned source relation")
        row, map_path, map_sha, generated_identity = selected
        source = read(base/row["authored_copy_path"])
        generated = read(base/path, 8*1024*1024)
        map_raw = read(base/map_path, 32*1024*1024)
        if hashlib.sha256(map_raw).hexdigest() != map_sha: result["status"] = 1; return result
        descriptor = json.loads(map_raw, object_pairs_hook=_pairs)
        mapping = sm.validate_map(descriptor, source=source, generated=generated, owner=sm.SourceOwner(**row["owner"]),
            translator=translator_identity(), source_identity=sm.SourceIdentity(**row["authored"]), generated_identity=sm.SourceIdentity(**generated_identity))
        # Regenerate from the actual copied authored closure, never execute it.
        copy_root = base/".pyalamode/sources"
        captured = {str(copy_root/r["owner"]["authored_path"]): read(base/r["authored_copy_path"]) for r in rows.values()}
        for old in evidence["files"]:
            provenance = old.get("source_provenance")
            if provenance is None: continue
            name = provenance["owner"]["authored_path"]
            copy_path = ".pyalamode/sources/" + name
            if copy_path in inventory:
                copied = read(base/copy_path)
                if hashlib.sha256(copied).hexdigest() != provenance["authored"]["sha256"]: result["status"] = 1; return result
                captured[str(copy_root/name)] = copied
        texts = {p: raw.decode("utf-8-sig" if Path(p).suffix == ".pya" else tokenize.detect_encoding(io.BytesIO(raw).readline)[0])
            for p, raw in captured.items()}
        policy, error = load_policy(Path(root or Path.cwd()).resolve())
        if error: raise ValueError(error)
        graph = SourceGraph(texts, copy_root, False, {**policy, "edition": EXPERIMENTAL_EDITION, "_raw_sources": captured})
        graph.analyze({})
        unit = graph.source_units[str(copy_root/row["owner"]["authored_path"])]
        file = graph.analyzers[unit.path].result
        old_file = next(f for f in evidence["files"] if f["source_provenance"] and f["source_provenance"]["owner"] == row["owner"])
        # Guard messages use the actual original path retained by the artifact.
        file.path = old_file["path"]
        for c in file.contracts: c.path = old_file["path"]
        from .guardgen import debug_derivation, facade_derivation, record_schemas
        records = record_schemas([a.result for a in graph.analyzers.values()])
        if generated_identity["role"] == "facade":
            names = {r["selection"].split(":")[1] for r in evidence["guarded_exports"] if r["selection"].split(":")[0] == unit.owner.module}
            derivation = facade_derivation(unit, unit.owner.module, [c for c in file.contracts if c.name in names], records, path)
        elif evidence["boundary_guards"] == "debug": derivation = debug_derivation(unit, file, records, path)
        else: derivation = None
        expected_bytes = derivation.generated_bytes if derivation else unit.normalized_bytes
        expected_map = sm.compose_maps(unit.source_map, derivation.source_map, source=source, intermediate=unit.normalized_bytes, generated=expected_bytes) if derivation else unit.source_map
        if expected_bytes != generated or map_bytes(expected_map) != map_raw: result["status"] = 1; return result
        offset = sm.offset_at(generated, line, column)
        mapped = sm.map_range(mapping, sm.ByteSpan(offset, offset), source=source, generated=generated)
        first, last = sm.position_at(source, mapped.source_span.start), sm.position_at(source, mapped.source_span.end)
        result.update(status=0, verified=True, exact=mapped.exact, segments=list(mapped.segments),
            authored={"path": row["owner"]["authored_path"], "source_copy": row["authored_copy_path"], "line": first.line, "column": first.column,
                "end_line": last.line, "end_column": last.column, "column_encoding": "utf-8-bytes", "sha256": hashlib.sha256(source).hexdigest()})
        result["generated"]["sha256"] = hashlib.sha256(generated).hexdigest()
    except (OSError, ValueError, TypeError, KeyError, StopIteration, SyntaxError, RecursionError) as error:
        result["diagnostics"].append(as_owner(diagnostic("PAL001", str(base), str(error), origin="source location")))
    return result


def _policy_identity(root):
    path = root / "pyproject.toml"
    if path.exists() and not path.resolve().is_relative_to(root):
        raise ValueError("editor project policy resolves outside workspace; refused before reading")
    return hashlib.sha256(path.resolve().read_bytes()).hexdigest() if path.exists() else None


def _owned_source_bytes(path, root):
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("source resolves outside project; refused before reading")
    return resolved.read_bytes()


def check_snapshot(paths=None, *, root=None, audit=False, target=TARGET, cache=True,
                   overlays=None, _candidate_selection=None, _migration_history=True) -> ProjectSnapshot:
    """Use the same policy/resolution/writer/approval/guard engine as check/build.

    Overlays are existing project-local .py files with decoded text and versions.
    This captures evidence about those buffers, never a disk build certificate.
    """
    project_root = Path(root or Path.cwd()).resolve()
    selected = list(paths or [project_root])
    normalized = {}
    errors = []
    if any(not Path(path).resolve().is_relative_to(project_root) for path in selected):
        errors.append(diagnostic("PAL001", str(project_root), "editor source selection resolves outside workspace; refused before reading", origin="editor source ownership"))
    for path, entry in (overlays or {}).items():
        candidate = Path(path).resolve()
        if (not candidate.is_relative_to(project_root) or not candidate.is_file() or candidate.suffix not in {".py", ".pya"}
                or type(entry) is not dict or set(entry) != {"text", "version"}
                or type(entry.get("text")) is not str or type(entry.get("version")) is not int
                or entry["version"] < 0):
            errors.append(diagnostic("PAL001", str(candidate), "editor overlay requires existing project-local Python source, decoded text and nonnegative integer version", origin="editor snapshot"))
        else:
            normalized[str(candidate)] = entry
    captured = {"overlay_versions": {path: entry["version"] for path, entry in normalized.items()}}
    products = foundation_identities()
    captured["products"] = products
    try:
        policy_hash = _policy_identity(project_root)
        overlay_disk = {path: hashlib.sha256(_owned_source_bytes(path, project_root)).hexdigest() for path in normalized}
        if (project_root / "pyproject.toml").exists() and not (project_root / "pyproject.toml").resolve().is_relative_to(project_root):
            errors.append(diagnostic("PAL001", str(project_root / "pyproject.toml"), "editor project policy resolves outside workspace", origin="editor snapshot"))
        if errors:
            result = ProjectResult(tooling=errors, audit=audit)
        else:
            result = check_paths(selected, root=project_root, audit=audit, target=target, cache=cache,
                                 _overlays={path: entry["text"] for path, entry in normalized.items()}, _capture=captured, _read_root=project_root,
                                 _candidate_selection=_candidate_selection, _migration_history=_migration_history)
        raw_sources = captured.get("raw_sources", {})
        source_inputs = {path: {"sha256": hashlib.sha256(raw).hexdigest(),
                               "origin": "overlay" if path in normalized else "disk",
                               "version": normalized[path]["version"] if path in normalized else None,
                               "disk_sha256": overlay_disk[path] if path in normalized else hashlib.sha256(raw).hexdigest(),
                               "source_provenance": source_provenance(captured["source_units"][path]) if path in captured.get("source_units", {}) else None}
                         for path, raw in raw_sources.items()}
        inputs = {"root": str(project_root), "paths": [str(Path(p).resolve()) for p in selected],
                  "audit": audit, "target": target, "sources": source_inputs, "policy_sha256": policy_hash,
                  "analysis": {"candidate_selection": copy.deepcopy(_candidate_selection), "migration_history": _migration_history},
                  "product_artifacts": products,
                  "integration_inputs": captured.get("integration_snapshot", {}).get("inputs", {}), "checked_dependencies": result.distribution_inputs}
        stale = []
        for path, entry in source_inputs.items():
            if not Path(path).is_relative_to(project_root):
                stale.append("source resolves outside workspace: " + path)
            elif hashlib.sha256(_owned_source_bytes(path, project_root)).hexdigest() != entry["disk_sha256"]:
                stale.append("source changed during snapshot: " + path)
        if policy_hash != _policy_identity(project_root):
            stale.append("policy changed during snapshot")
        if products != foundation_identities():
            stale.append("product bytes changed during snapshot")
        if "selected_paths" in captured:
            final_paths, final_errors = discover_paths(selected, project_root)
            if final_errors or [str(path) for path in final_paths] != captured["selected_paths"]:
                stale.append("source selection/import resolution changed during snapshot")
        if "integration_snapshot" in captured:
            policy, policy_error = load_policy(project_root)
            current = integration_snapshot(policy, project_root)
            if policy_error or current["errors"] or current["inputs"] != inputs["integration_inputs"]:
                stale.append("integration identity/approval changed during snapshot")
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        result = ProjectResult(tooling=[diagnostic("PAL001", str(project_root), "cannot capture editor project snapshot: " + str(error), origin="editor snapshot")], audit=audit)
        inputs = {"root": str(project_root), "paths": [str(p) for p in selected], "audit": audit, "target": target,
                  "analysis": {"candidate_selection": copy.deepcopy(_candidate_selection), "migration_history": _migration_history},
                  "sources": {}, "policy_sha256": None, "product_artifacts": products, "integration_inputs": {}, "checked_dependencies": {}}
        stale = ["snapshot input capture failed"]
    freshness = "current overlay snapshot; unsaved" if normalized else "current disk snapshot"
    if stale:
        freshness = "stale; recheck required"
        result.tooling.extend(diagnostic("PAL001", str(project_root), reason, origin="editor freshness") for reason in stale)
        for file in result.results:
            file.diagnostics.append(diagnostic("PAL001", file.path, "editor snapshot is stale; recheck required", origin="editor freshness"))
            for declaration in [*file.records, *file.oneofs]:
                declaration["source_evidence"] = "unverified: stale editor snapshot"
            for contract in file.contracts:
                contract.source_evidence = "unverified: stale editor snapshot"
                contract.freshness = "stale; recheck required"
                contract.behavior = "unverified behavior; no certified effect bound"
    key = hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ProjectSnapshot(result, captured.get("sources", {}), inputs, freshness, key, captured.get("graph"), captured.get("source_units", {}))


def runtime_error(target: str = TARGET) -> str | None:
    if target != TARGET:
        return f"unsupported requested target {target}; published target is {TARGET}"
    if platform.python_implementation() != "CPython" or tuple(sys.version_info[:3]) != (3, 13, 1):
        return f"unsupported running interpreter {platform.python_implementation()} {platform.python_version()}; use CPython 3.13.1"
    if (sys.platform,platform.machine()) not in {("darwin","arm64"),("linux","aarch64")}:
        return f"unsupported platform {sys.platform}; supported platforms are macOS arm64 and Linux aarch64"
    if sysconfig_free_threaded():
        return "free-threaded CPython builds are outside the supported target"
    environment = runtime_environment()
    if environment["filesystem_encoding"] != "utf-8" or environment["filesystem_errors"] != "surrogateescape":
        return "unsupported native filesystem configuration; use UTF-8 encoding with surrogateescape errors"
    return None


def sysconfig_free_threaded() -> bool:
    # CPython3.13's free-threaded build ABI has `t`. A sysconfig getter can
    # import environment-selected or shadowed config-data Python source.
    return "t" in sys.abiflags


def load_policy(root: Path, read_root: Path | None = None) -> tuple[dict, str | None]:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}, None
    if not path.resolve().is_relative_to(read_root or root):
        return {}, "editor project policy resolves outside workspace; refused before reading"
    try:
        data = tomllib.loads(path.resolve().read_text(encoding="utf-8"))
        tool = data.get("tool", {})
        if not isinstance(tool, dict):
            return {}, "pyproject tool must be a table"
        policy = tool.get("pyalamode", {})
        if not isinstance(policy, dict):
            return {}, "tool.pyalamode must be a table"
        expected = {"schema": 1, "edition": EDITION, "runtime": "cpython-3.13",
                    "boundary_guards": "off", "external_trust": "deny", "builders": False, "tasks": False,
                    "require_modules": [], "guarded_exports": [], "effect_bounds": {}, "explicit_cases": [],
                    "integration_manifests": [], "integration_approvals": [], "required_exports": [], "migration": {}, "distribution": {}, "checked_dependencies": []}
        for key, value in policy.items():
            if key == "edition":
                if type(value) is not str or value not in {EDITION, EXPERIMENTAL_EDITION}:
                    return policy, "edition must be python-v1 or pyalamode-v1-experimental"
            elif key in {"builders", "tasks"}:
                if type(value) is not bool:
                    return policy, key + " requires an exact boolean"
            elif key in {"distribution", "checked_dependencies"}:
                from .distribution import validate_distribution_policy
                error = validate_distribution_policy(policy)
                if error: return policy, error
            elif key in {"external_trust", "integration_manifests", "integration_approvals"}:
                error = validate_policy(policy)
                if error:
                    return policy, error
            elif key == "require_modules":
                if type(value) is not list or any(type(pattern) is not str or not pattern or pattern.startswith("/") or ".." in Path(pattern).parts or "\\" in pattern for pattern in value):
                    return policy, "require_modules must be a list of nonempty project-relative glob patterns"
            elif key == "explicit_cases":
                if type(value) is not list or any(type(selection) is not str or selection.count(":") != 1 or any(not part.isidentifier() for part in selection.split(":", 1)[0].split(".")) or not selection.split(":", 1)[1].isidentifier() for selection in value) or len(set(value)) != len(value):
                    return policy, "explicit_cases must list unique exact module:Domain selections"
            elif key == "effect_bounds":
                from .checker import EFFECT_FAMILIES
                if type(value) is not dict:
                    return policy, "effect_bounds must be a table of exact module:function selections to finite family lists"
                for selection, bound in value.items():
                    if type(selection) is not str or selection.count(":") != 1 or any(not part.isidentifier() for part in selection.split(":", 1)[0].split(".")) or any(not part.isidentifier() for part in selection.split(":", 1)[1].split(".")):
                        return policy, "effect_bounds selectors must be exact module:function identities"
                    if type(bound) is not list or any(type(effect) is not str or effect not in EFFECT_FAMILIES for effect in bound) or len(set(bound)) != len(bound):
                        return policy, "effect_bounds requires unique IO/State/Clock/Random/Environment/Task family lists"
            elif key == "boundary_guards":
                if type(value) is not str or value not in {"off", "exports", "debug"}:
                    return policy, "boundary_guards must be off, exports or debug"
            elif key == "guarded_exports":
                if type(value) is not list or any(type(selection) is not str or selection.count(":") != 1 or any(not part.isidentifier() for part in selection.split(":", 1)[0].split(".")) or not selection.split(":", 1)[1].isidentifier() or selection.split(":", 1)[1].startswith("_") for selection in value):
                    return policy, "guarded_exports must list exact public module:function selections"
                if len(set(value)) != len(value):
                    return policy, "guarded_exports contains duplicate selections"
            elif key == "required_exports":
                if (type(value) is not list or any(type(selection) is not str or selection.count(":") != 1
                        or any(not part.isidentifier() for part in selection.split(":", 1)[0].split("."))
                        or not selection.split(":", 1)[1].isidentifier() or selection.split(":", 1)[1].startswith("_") for selection in value)
                        or len(set(value)) != len(value)):
                    return policy, "required_exports must list unique exact public top-level module:function selections"
            elif key == "migration":
                allowed = {"schema", "baseline", "reject_new_findings", "reject_lost_strict_coverage", "reject_new_trust", "reject_expanded_effects", "reject_expired_approvals", "reject_unsafe_weakening", "reject_policy_weakening"}
                if type(value) is not dict or set(value) - allowed or type(value.get("schema")) is not int or value["schema"] != 1:
                    return policy, "migration requires closed schema 1"
                relative = value.get("baseline", ".pyalamode/baseline.json")
                if (type(relative) is not str or "\\" in relative or not relative.startswith(".pyalamode/")
                        or not relative.endswith(".json") or any(part in {"", ".", ".."} for part in relative.split("/"))):
                    return policy, "migration baseline must be a project-relative JSON reference below .pyalamode"
                if any(type(v) is not bool for k, v in value.items() if k.startswith("reject_")):
                    return policy, "migration gates require exact boolean values"
            elif key not in expected or type(value) is not type(expected[key]) or value != expected[key]:
                return policy, f"unsupported policy field/value {key}={value!r}; use the closed milestone 8 configuration"
        if policy.get("boundary_guards", "off") == "off" and policy.get("guarded_exports"):
            return policy, "guarded_exports conflicts with boundary_guards=off"
        if policy.get("boundary_guards") == "exports" and not policy.get("guarded_exports"):
            return policy, "boundary_guards=exports requires explicit guarded_exports selections"
        return policy, None
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        return {}, f"cannot read project policy: {error}"


def discover_paths(paths: list[str | Path], root: Path) -> tuple[list[Path], list[Diagnostic]]:
    discovered: set[Path] = set()
    errors: list[Diagnostic] = []
    for value in paths or [root]:
        physical = Path(value)
        if physical.suffix == ".pya" and (physical.is_symlink() or any(p.is_symlink() for p in physical.absolute().parents)):
            errors.append(diagnostic("PAL001", str(physical), "dialect ownership requires a regular physical source path", origin="experimental source ownership"))
            continue
        path = physical.resolve()
        if path.is_file() and path.suffix in {".py", ".pya"}:
            discovered.add(path)
        elif path.is_dir():
            for directory, children, files in os.walk(path):
                children[:] = sorted(c for c in children if c not in _EXCLUDED and not c.endswith(".egg-info") and not c.startswith(".pyalamode-build-"))
                for name in files:
                    if name.endswith((".py", ".pya")):
                        candidate = Path(directory) / name
                        if candidate.suffix == ".pya" and (candidate.is_symlink() or not candidate.is_file() or any(p.is_symlink() for p in candidate.absolute().parents)):
                            errors.append(diagnostic("PAL001", str(candidate), "dialect ownership requires a regular physical source path", origin="experimental source ownership"))
                            continue
                        discovered.add(candidate.resolve())
        else:
            errors.append(diagnostic("PAL001", str(path), "source path must be an existing Python file or directory"))
    if not discovered and not errors:
        errors.append(diagnostic("PAL001", str(root), "no Python source files were selected"))
    module_owners = {}
    runtime_owners = {}
    for path in sorted(discovered):
        try:
            owner = source_owner(str(path), root)
            row = as_owner(owner)
        except (ValueError, OSError) as error:
            if path.suffix == ".pya":
                errors.append(diagnostic("PAL001", str(path), str(error), origin="experimental source ownership"))
            continue
        module_owners.setdefault((row["module"] or "").casefold(), []).append(path)
        runtime_owners.setdefault(row["runtime_path"].casefold(), []).append(path)
    for group in [*module_owners.values(), *runtime_owners.values()]:
        if len(group) > 1 and any(path.suffix == ".pya" for path in group):
            errors.append(diagnostic("PAL001", str(group[0]), "ambiguous dialect/module/package/generated ownership: " + ", ".join(str(path) for path in group), origin="experimental source ownership"))
    return sorted(discovered), errors


def as_owner(owner):
    from dataclasses import asdict, is_dataclass
    return asdict(owner) if is_dataclass(owner) else owner


def _cache_read(cache: Path, key: str, path: str, audit: bool) -> CheckResult | None:
    identity = (os.getpid(), key, path, "audit" if audit else "strict")
    authority = _SOURCE_CACHE_IDENTITIES.get(identity)
    if authority is None:
        return None
    try:
        envelope = json.loads((cache / f"{key}.json").read_text())
        payload = envelope["payload"]
        if "source_provenance" not in payload:
            return None
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if envelope["checksum"] != digest or payload["fingerprint"] != key or payload["path"] != path:
            return None
        if digest != authority:
            return None
        result = CheckResult(path, key,
                             diagnostics=[Diagnostic(**d) for d in payload["diagnostics"]],
                             contracts=[FunctionContract(**c) for c in payload["contracts"]],
                             eligible_functions=payload["eligible_functions"],
                             selected_functions=payload["selected_functions"],
                             analyzed_call_sites=payload["analyzed_call_sites"], cache_hit=True,
                             mode="audit" if audit else "strict", module_mode=payload.get("module_mode", False),
                             initialization_evidence=payload.get("initialization_evidence", "unchecked ordinary module initialization"),
                             dependencies=payload.get("dependencies", {}), initialization_failures=payload.get("initialization_failures", []),
                             binding_context=payload.get("binding_context", []), records=payload.get("records", []), oneofs=payload.get("oneofs", []), cases=payload.get("cases", []),
                             setup_observations=payload.get("setup_observations", []),
                             unsafe_adapters=payload.get("unsafe_adapters", []), integration_inputs=payload.get("integration_inputs", {}),
                             source_provenance=payload["source_provenance"])
        # Audit and strict are distinct cache keys; never upgrade cached audit evidence.
        if payload["mode"] != result.mode:
            return None
        return result
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _cache_write(cache: Path, result: CheckResult) -> None:
    payload = result.to_dict()
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    envelope = {"payload": payload, "checksum": hashlib.sha256(encoded.encode()).hexdigest()}
    try:
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=cache, delete=False) as stream:
            json.dump(envelope, stream, sort_keys=True)
            temporary = stream.name
        os.replace(temporary, cache / f"{result.fingerprint}.json")
    except OSError:
        # Disposable cache availability cannot change verification outcomes.
        pass


def check_paths(paths: list[str | Path] | None = None, *, root: str | Path | None = None,
                audit: bool = False, target: str = TARGET, cache: bool = True,
                _overlays=None, _capture=None, _read_root=None,
                _candidate_selection=None, _migration_history=True) -> ProjectResult:
    global _SOURCE_CACHE_IDENTITIES
    started = time.perf_counter()
    _capture = _capture if _capture is not None else {}
    project_root = Path(root or Path.cwd()).resolve()
    result = ProjectResult(audit=audit)
    error = runtime_error(target)
    if error:
        result.tooling.append(diagnostic("PAL002", str(project_root), error, origin="runtime target"))
    policy, error = load_policy(project_root, _read_root)
    result.selected_edition = policy.get("edition", EDITION)
    result.boundary_guards = policy.get("boundary_guards", "off")
    if error:
        result.tooling.append(diagnostic("PAL001", str(project_root / "pyproject.toml"), error, origin="project policy"))
    if _candidate_selection is not None:
        if (type(_candidate_selection) is not dict or set(_candidate_selection) != {"functions", "modules"}
                or any(type(_candidate_selection[k]) is not list or any(type(v) is not str for v in _candidate_selection[k]) for k in ("functions", "modules"))
                or audit or cache):
            result.tooling.append(diagnostic("PAL001", str(project_root), "candidate selection requires fresh strict analysis and exact physical identities", origin="migration candidate"))
    if policy.get("required_exports") or "migration" in policy:
        _read_root = project_root
        if any(not Path(p).resolve().is_relative_to(project_root) for p in (paths or [project_root])):
            result.tooling.append(diagnostic("PAL001", str(project_root), "team policy source selection resolves outside project; refused before reading", origin="migration ownership"))
    files, errors = discover_paths(paths or [], project_root)
    if _capture is not None:
        _capture["selected_paths"] = [str(path) for path in files]
    result.tooling.extend(errors)
    if result.tooling:
        result.elapsed_seconds = time.perf_counter() - started
        return result
    from .distribution import distribution_snapshot, public_receipts
    distributions = distribution_snapshot(policy, project_root)
    _capture["distribution_snapshot"] = distributions
    _capture["policy"] = policy
    if "products" not in _capture:_capture["products"] = foundation_identities()
    _capture["requested"] = paths or [project_root]
    _capture["distribution_cache_inputs"] = public_receipts(distributions)
    result.distribution_inputs = public_receipts(distributions)
    result.checked_dependencies = list(result.distribution_inputs.values())
    result.tooling.extend(diagnostic("PAL001", str(project_root), reason, origin="installed distribution resolution") for reason in distributions["errors"])
    if result.tooling: return result
    cache_path = project_root / ".pyalamode-cache"
    cache_policy = {**policy, "analysis_mode": "audit" if audit else "strict", "platform": sys.platform}
    raw_sources = {}
    sources, errors = load_sources(files, project_root, raw_sources, _overlays, _read_root)
    if _capture is not None:
        _capture.update(sources=sources, raw_sources=raw_sources)
    result.tooling.extend(errors)
    if errors:
        result.elapsed_seconds = time.perf_counter() - started
        return result
    if _candidate_selection is not None:
        candidates = {}
        for path, source in sources.items():
            if Path(path).suffix == ".pya":
                prepared = syntax.prepare_source(raw_sources[path], source_owner(path, project_root), edition=policy.get("edition", EDITION), translator=translator_identity())
                source = prepared.prepared.scaffold_bytes.decode("utf-8-sig") if prepared.prepared else ""
            for node in ast.parse(source, filename=path, feature_version=(3, 13)).body:
                if isinstance(node, ast.FunctionDef) and not getattr(node, "type_params", []):
                    identity = path + "::" + node.name
                    candidates[identity] = candidates.get(identity, 0) + 1
        if (any(candidates.get(identity) != 1 for identity in _candidate_selection["functions"])
                or any(path not in sources for path in _candidate_selection["modules"])):
            result.tooling.append(diagnostic("PAL001", str(project_root), "candidate selection does not resolve to unique supported current top-level declarations", origin="migration candidate"))
            return result
    integrations = integration_snapshot(policy, project_root)
    if _capture is not None:
        _capture["integration_snapshot"] = integrations
    result.integration_catalog, result.integration_approvals = integrations["catalog"], integrations["approvals"]
    if integrations["errors"]:
        result.tooling.extend(diagnostic("PAL001", str(project_root), error, origin="integration manifests") for error in integrations["errors"])
        result.elapsed_seconds = time.perf_counter() - started
        return result
    owned_sources = dict(sources)
    sources.update(distributions["sources"])
    raw_sources.update(distributions["raw_sources"])
    try:
        graph = SourceGraph(sources, project_root, audit, {**cache_policy, "_integration_snapshot": integrations,
            "_distribution_snapshot": distributions, "_raw_sources": raw_sources}, _candidate_selection)
    except (ValueError, TypeError, UnicodeError, SyntaxError, RecursionError) as error:
        result.tooling.append(diagnostic("PAL001", str(project_root), "cannot derive captured source units: " + str(error), origin="experimental source ownership/frontend"))
        return result
    normalized_sources = {path: analyzer.source for path, analyzer in graph.analyzers.items()}
    _capture["source_units"] = graph.source_units
    dependencies = _source_dependencies(normalized_sources, project_root, graph)
    if _capture is not None:
        _capture["graph"] = graph
    contexts = {path: graph.binding_context(path, dependencies[path]) for path in sources}
    external_inputs = {path: graph.integration_context(path, dependencies[path]) for path in sources}
    keys = {path: fingerprint(raw_sources[path], {**cache_policy, "path": path,
            "source_dependencies": {d: hashlib.sha256(raw_sources[d]).hexdigest() for d in sorted(dependencies[path])},
            "binding_context": contexts[path], "integration_inputs": external_inputs[path], "checked_dependencies": public_receipts(distributions),
            "source_provenance": source_provenance(graph.source_units[path])})
            for path in sources}
    cached = {}
    if cache:
        for path, key in keys.items():
            hit = _cache_read(cache_path, key, path, audit)
            if hit is not None:
                cached[path] = hit
    # Conservatively include static import closures, including initialization requirements.
    for path, analyzer in graph.analyzers.items():
        analyzer.dependencies.update(dependencies[path])
    analyzed_results = graph.analyze(cached)
    result.analysis_counts={"writer_scan_files":len(sources),"owned_files":len(owned_sources),"installed_files":len(sources)-len(owned_sources),"source_dependency_edges":sum(len(v) for v in dependencies.values()),"selected_functions":sum(r.selected_functions for r in analyzed_results.values()),"fresh_body_files":sum(not r.cache_hit for r in analyzed_results.values()),"cached_body_files":sum(r.cache_hit for r in analyzed_results.values()),"installed_fresh_body_files":sum(not r.cache_hit for p,r in analyzed_results.items() if p not in owned_sources),"installed_cached_body_files":sum(r.cache_hit for p,r in analyzed_results.items() if p not in owned_sources)}
    for path, analyzed in sorted(analyzed_results.items()):
        analyzed.fingerprint = keys[path]
        analyzed.dependencies = {d: hashlib.sha256(raw_sources[d]).hexdigest() for d in sorted(dependencies[path])}
        analyzed.binding_context = contexts[path]
        analyzed.integration_inputs = external_inputs[path]
        if cache and path not in cached:
            identity = (os.getpid(), keys[path], path, analyzed.mode)
            encoded = json.dumps(analyzed.to_dict(), sort_keys=True, separators=(",", ":"))
            identities = _SOURCE_CACHE_IDENTITIES.copy()
            if identity not in identities and len(identities) >= 4096:
                identities.clear()
            identities[identity] = hashlib.sha256(encoded.encode()).hexdigest()
            # Detached publication keeps every table bounded across overlapping checks.
            _SOURCE_CACHE_IDENTITIES = identities
            _cache_write(cache_path, analyzed)
        if path in owned_sources:
            result.results.append(analyzed)
        else:
            _capture.setdefault("installed_results", []).append(analyzed)
    intrinsic, intrinsic_dependencies = _intrinsic_distribution_graph(distributions, cache_policy, integrations, project_root)
    result.analysis_counts.update(intrinsic_graphs=int(intrinsic is not None),
        intrinsic_writer_scan_files=len(intrinsic.analyzers) if intrinsic else 0,
        intrinsic_source_dependency_edges=sum(len(v) for v in intrinsic_dependencies.values()),
        intrinsic_selected_functions=sum(a.result.selected_functions for a in intrinsic.analyzers.values()) if intrinsic else 0,
        intrinsic_fresh_body_files=len(intrinsic.analyzers) if intrinsic else 0)
    _finish_distributions(result, distributions, graph, project_root, intrinsic)
    selected = {graph.module_name(file.path) + ":" + contract.name for file in analyzed_results.values() for contract in file.contracts}
    for selection in policy.get("effect_bounds", {}):
        if selection not in selected:
            result.tooling.append(diagnostic("PAL001", str(project_root / "pyproject.toml"), f"effect bound selection `{selection}` does not resolve to a selected function", origin="project effect policy"))
    selected_domains = {info.module + ":" + info.node.name for info in graph.oneofs.values()}
    for selection in policy.get("explicit_cases", []):
        if selection not in selected_domains:
            result.tooling.append(diagnostic("PAL001", str(project_root / "pyproject.toml"), f"explicit_cases selection `{selection}` does not resolve to a checked top-level domain", origin="project pattern policy"))
    _guard_plan(result, policy, project_root, graph)
    _integration_freshness(result, integration_snapshot(policy, project_root), "check completed")
    _distribution_check_freshness(result,distributions,policy,project_root)
    _capture["normalized_results"] = {path: copy.deepcopy(analyzer.result) for path, analyzer in graph.analyzers.items()}
    result.results = [public_result(file, graph.source_units[file.path]) for file in result.results]
    _capture["installed_results"] = [public_result(file, graph.source_units[file.path]) for file in _capture.get("installed_results", [])]
    for coverage in result.debug_coverage:
        unit = graph.source_units.get(coverage["path"])
        if unit and unit.edition != EDITION:
            public = next(file for file in result.results if file.path == coverage["path"])
            contract = next(c for c in public.contracts if c.name == coverage["name"])
            coverage["line"] = contract.line
            coverage["locals"] = [row for row in contract.data_assertions if row["name"] in {r["name"] for r in coverage["locals"]}]
    _capture["sources"] = owned_sources
    _capture["raw_sources"] = {p:raw_sources[p] for p in owned_sources}
    _capture["prepublish"] = lambda: _distribution_prepublish(result, distributions, policy, project_root, _capture)
    result.source_status = result.status
    if not _migration_history or policy.get("required_exports") or "migration" in policy:
        from .migration_views import apply_current_policy, integrate_team_policy
        if _migration_history:
            integrate_team_policy(result, project_root, policy, target, _overlays,
                                  (_capture or {}).get("overlay_versions", {}))
        else:
            apply_current_policy(result, graph, policy, project_root)
    result.elapsed_seconds = time.perf_counter() - started
    return result


def _integration_freshness(result, snapshot, stage):
    """Current external policy refusals stay status1, including crossing expiry."""
    refused = False
    rows = {row["identity"]: row for row in snapshot["catalog"]}
    result.integration_catalog, result.integration_approvals = snapshot["catalog"], snapshot["approvals"]
    for file in result.results:
        changed = {name for name, value in file.integration_inputs.items() if snapshot["inputs"].get(name) != value}
        for contract in file.contracts:
            relevant = changed & {entry["identity"] for entry in contract.external_assumptions}
            if relevant:
                refused = True
                file.diagnostics.append(diagnostic("PAL350", file.path, "integration identity/approval changed before " + stage + ": " + ", ".join(sorted(relevant)), line=contract.line, boundary=contract.name, origin="integration freshness"))
                contract.source_evidence = "unverified: integration freshness changed"
                contract.freshness = "no successful checked claim"
                contract.behavior = "unverified behavior; no certified effect bound"
                contract.external_assumptions = [SourceGraph.external_assumption(rows[entry["identity"]]) if entry["identity"] in relevant else entry for entry in contract.external_assumptions]
                contract.trust = [entry for entry in contract.trust if not any(entry.startswith("external " + name + " ") for name in relevant)]
                contract.trust.extend("external " + entry["identity"] + " contract=" + str(entry["contract_sha256"]) + " dependency=" + str(entry["dependency_sha256"]) + " approval=" + entry["admission"] for entry in contract.external_assumptions if entry["identity"] in relevant)
                contract.trust.sort()
    if refused and result.source_status is not None:
        result.source_status = max(result.source_status, int(not result.audit))
    return refused


class _IntegrationFreshnessError(Exception):
    pass


def _guard_plan(result, policy, root, graph):
    from .guardgen import record_schemas, supported_schema
    mode = policy.get("boundary_guards", "off")
    if mode == "off":
        return
    if result.status:
        return
    replacements = graph.record_dependency_replacements | graph.collection_dependency_replacements | graph.domain_dependency_replacements
    if replacements:
        result.tooling.append(diagnostic("PAL001", str(root), "guard foundation has analyzed replacements: " + ", ".join(sorted(replacements)), origin="guard dependency"))
    records = record_schemas([a.result for a in graph.analyzers.values()])
    modules = {graph.module_name(r.path): r for r in result.results}
    if len(modules) != len(result.results):
        result.tooling.append(diagnostic("PAL001", str(root), "guard selection has ambiguous duplicate module identities", origin="guard selection"))
        return
    if any(module == "pyalamode_exports" or module.startswith("pyalamode_exports.") for module in modules):
        result.tooling.append(diagnostic("PAL001", str(root), "selected source conflicts with generated pyalamode_exports namespace", origin="guard selection"))
        return
    for selection in policy.get("guarded_exports", []):
        module, name = selection.split(":", 1)
        file = modules.get(module)
        contract = next((c for c in file.contracts if c.name == name), None) if file else None
        if contract is None:
            result.tooling.append(diagnostic("PAL001", str(root), f"guard selection `{selection}` does not resolve to a selected top-level public function", origin="guard selection"))
            continue
        if not all(supported_schema(kind, records) for kind in [*contract.parameters.values(), contract.returns]):
            result.tooling.append(diagnostic("PAL001", contract.path, f"guard selection `{selection}` requires unsupported schema; guards validate exact data and refuse Callable, Effectful and live capability boundaries", line=contract.line, origin="guard coverage"))
            continue
        result.guarded_exports.append({"selection": selection, "public_boundary": "pyalamode_exports." + module + ":" + name,
                                       "original_boundary": selection, "original_protection": "unguarded" if mode == "exports" else "debug data assertions",
                                       "coverage": "exact argument and return schemas, recursive nested data; no freezing, effects, callable purity, ownership or dependency tamper detection",
                                       "parameters": dict(contract.parameters), "returns": contract.returns,
                                       "generated": False})
    if mode == "debug":
        for file in result.results:
            for contract in file.contracts:
                result.debug_coverage.append({"path": contract.path, "name": contract.name, "line": contract.line,
                                              "parameters": {name: kind for name, kind in contract.parameters.items() if supported_schema(kind, records)},
                                              "returns": contract.returns if supported_schema(contract.returns, records) else None,
                                              "locals": [item for item in contract.data_assertions if supported_schema(item["schema"], records)],
                                              "callable_validation": "excluded; caller evidence obligations remain",
                                              "capability_validation": "excluded; exact interface, allowed operation and lifetime obligations remain",
                                              "generated": False})


def _source_dependencies(sources: dict[str, str], root: Path, graph=None) -> dict[str, set[str]]:
    direct = {path: set() for path in sources}
    for path, source in sources.items():
        module = graph.module_name(path) if graph else _module_name(path, root)
        for node in ast.walk(ast.parse(source, filename=path, feature_version=(3, 13))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else []
            if isinstance(node, ast.ImportFrom):
                base = _import_name(node, module, Path(path).name in {"__init__.py", "__init__.pya"})
                names = [base] + [base + "." + a.name for a in node.names if a.name != "*"]
            for name in names:
                parts = name.split(".")
                for count in range(1, len(parts) + 1):
                    target = graph.resolve_module(".".join(parts[:count])) if graph else _local_path(root, ".".join(parts[:count]))
                    if target and str(target) in sources and str(target) != path:
                        direct[path].add(str(target))
    changed = True
    while changed:
        changed = False
        for path, values in direct.items():
            previous = len(values)
            for dependency in tuple(values):
                values.update(direct[dependency] - {path})
            changed |= previous != len(values)
    # A module that sees an open domain depends on every case contributed to it,
    # so adding or editing an extension anywhere in the project changes its key.
    from .checker import _declares_class_keyword
    open_paths = {path for path, source in sources.items() if _declares_class_keyword(source, "open")}
    extension_paths = {path for path, source in sources.items() if _declares_class_keyword(source, "of")}
    if open_paths and extension_paths:
        closure = {path: set(values) for path, values in direct.items()}
        contributed = set(extension_paths).union(*(closure[path] for path in extension_paths))
        for path, values in direct.items():
            if path in open_paths or values & open_paths:
                values.update(contributed - {path})
    return direct


def build_paths(paths: list[str | Path] | None = None, *, output: str | Path | None = None,
                root: str | Path | None = None, target: str = TARGET, artifact: str = "tree") -> ProjectResult:
    project_root = Path(root or Path.cwd()).resolve()
    destination = Path(output or project_root / "build" / "pyalamode").resolve()
    # Builds always freshly analyze source; caches accelerate check only.
    captured = {}
    result = check_paths(paths, root=project_root, target=target, cache=False, _capture=captured)
    if artifact == "wheel":
        if paths and any(Path(p).resolve()!=project_root for p in paths):
            result.tooling.append(diagnostic("PAL001", str(project_root), "wheel requires complete project selection")); return result
        if result.status: return result
        if "distribution" not in captured.get("policy", {}):
            result.tooling.append(diagnostic("PAL001", str(project_root), "wheel requires a finite distribution declaration")); return result
        from .distribution import build_wheel
        try:
            result.distribution = build_wheel(result, captured, project_root, output)
            result.output = result.distribution["path"]
        except (OSError, ValueError, TypeError, KeyError, SyntaxError, RecursionError) as error:
            if not result.status: result.tooling.append(diagnostic("PAL001", str(project_root), "wheel stopped without publishing: " + str(error), origin="wheel output"))
        return result
    if result.status:
        return result
    if not any(file.selected_functions or file.module_mode or file.records or file.oneofs for file in result.results):
        result.tooling.append(diagnostic("PAL001", str(project_root), "build requires a participating function, record declaration or functional module; no checked artifact was produced"))
        return result
    if destination.exists():
        result.tooling.append(diagnostic("PAL001", str(destination), "output already exists; choose a fresh output directory to preserve prior artifacts"))
        return result
    sources = [Path(file.path) for file in result.results]
    base = project_root if all(path.is_relative_to(project_root) for path in sources) else Path(os.path.commonpath([str(p.parent) for p in sources]))
    if any(destination == source or destination in source.parents or source.is_relative_to(destination) for source in sources):
        result.tooling.append(diagnostic("PAL001", str(destination), "output overlaps selected source files"))
        return result
    staging = None
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".pyalamode-build-", dir=destination.parent))
        evidence = result.to_dict()
        evidence["artifact_kind"] = "local compatible source tree; installed dependencies independently rechecked under current consumer policy"
        evidence["artifact_files"] = {}
        evidence["syntax_artifacts"] = {"schema": 1, "translator": None, "modules": {}}
        source_snapshots = {}
        raw_snapshots = {}
        mapped_closure = set()
        for path_, unit_ in captured["source_units"].items():
            if unit_.source_map and unit_.dependency_owner is None:
                mapped_closure.add(path_)
                mapped_closure.update(captured["normalized_results"][path_].dependencies)
        from .guardgen import debug_source, debug_derivation, generate_facades, record_schemas
        for file in result.results:
            source = Path(file.path)
            raw = _owned_source_bytes(source, project_root) if result.migration is not None else source.read_bytes()
            # Source changes during analysis/copy invalidate this gate rather than publish stale evidence.
            policy, _ = load_policy(project_root)
            dependency_bytes = {d: hashlib.sha256(_owned_source_bytes(d, project_root) if result.migration is not None else Path(d).read_bytes()).hexdigest() for d in file.dependencies}
            current_integrations = integration_snapshot(policy, project_root)
            current_inputs = {name: current_integrations["inputs"][name] for name in file.integration_inputs}
            if current_integrations["errors"] or current_inputs != file.integration_inputs:
                if not current_integrations["errors"] and _integration_freshness(result, current_integrations, "build copy"):
                    raise _IntegrationFreshnessError
                raise OSError("integration identity/manifest/approval changed after checking")
            check_key = fingerprint(raw, {**policy, "analysis_mode": "strict", "platform": sys.platform, "path": str(source), "source_dependencies": dependency_bytes, "binding_context": file.binding_context, "integration_inputs": file.integration_inputs, "checked_dependencies": captured["distribution_cache_inputs"], "source_provenance": file.source_provenance})
            if check_key != file.fingerprint:
                raise OSError(f"source changed after checking: {source}")
            unit = captured["source_units"][file.path]
            raw_snapshots[file.path] = raw
            relative = Path(unit.owner.runtime_path) if unit.source_map else source.relative_to(base)
            copied = staging / relative
            copied.parent.mkdir(parents=True, exist_ok=True)
            source_snapshots[file.path] = unit.normalized_text
            private_file = captured["normalized_results"][file.path]
            records = record_schemas(result.results+captured.get("installed_results",[]))
            if unit.source_map:
                derivation = debug_derivation(unit, private_file, records) if result.boundary_guards == "debug" else None
                artifact_bytes = derivation.generated_bytes if derivation else unit.normalized_bytes
                runtime_map = sm.compose_maps(unit.source_map, derivation.source_map, source=raw,
                    intermediate=unit.normalized_bytes, generated=artifact_bytes) if derivation else unit.source_map
                authored_path = ".pyalamode/sources/" + unit.owner.authored_path
                lowered_path = ".pyalamode/lowered/" + unit.owner.runtime_path
                map_path = ".pyalamode/maps/" + unit.owner.runtime_path + ".map.json"
                runtime_map_path = ".pyalamode/maps/" + unit.owner.runtime_path + ".runtime.map.json" if derivation else map_path
                for path_, bytes_ in {authored_path: raw, lowered_path: unit.normalized_bytes,
                        map_path: map_bytes(unit.source_map), runtime_map_path: map_bytes(runtime_map)}.items():
                    target_ = staging/path_; target_.parent.mkdir(parents=True, exist_ok=True); target_.write_bytes(bytes_)
                    evidence["artifact_files"][path_] = hashlib.sha256(bytes_).hexdigest()
                evidence["syntax_artifacts"]["translator"] = {"version": SYNTAX_VERSION, "files": dict(translator_identity().files)}
                evidence["syntax_artifacts"]["modules"][unit.owner.module] = {"owner": as_owner(unit.owner), "edition": unit.edition,
                    "authored": as_owner(unit.source_map.source), "normalized": as_owner(unit.source_map.generated),
                    "runtime": as_owner(runtime_map.generated), "authored_copy_path": authored_path, "lowered_copy_path": lowered_path,
                    "map_path": map_path, "map_sha256": evidence["artifact_files"][map_path], "runtime_map_path": runtime_map_path,
                    "runtime_map_sha256": evidence["artifact_files"][runtime_map_path], "facades": []}
            else:
                artifact_bytes = debug_source(source_snapshots[file.path], private_file, records).encode() if result.boundary_guards == "debug" else raw
                if file.path in mapped_closure:
                    authored_path = ".pyalamode/sources/" + source.relative_to(base).as_posix()
                    target_ = staging/authored_path; target_.parent.mkdir(parents=True,exist_ok=True); target_.write_bytes(raw)
                    evidence["artifact_files"][authored_path] = hashlib.sha256(raw).hexdigest()
            copied.write_bytes(artifact_bytes)
            if result.boundary_guards == "debug":
                compile(artifact_bytes, str(copied), "exec")
            evidence["artifact_files"][relative.as_posix()] = hashlib.sha256(artifact_bytes).hexdigest()
        for relative, raw in generate_facades(staging, list(captured["normalized_results"].values())+captured.get("installed_results",[]), project_root, policy.get("guarded_exports", []), source_snapshots,
                units=captured["source_units"], syntax_modules=evidence["syntax_artifacts"]["modules"]).items():
            if relative.endswith(".py"): compile(raw, str(staging / relative), "exec")
            evidence["artifact_files"][relative] = hashlib.sha256(raw).hexdigest()
        for boundary in evidence["guarded_exports"]:
            boundary["generated"] = True
        for coverage in evidence["debug_coverage"]:
            coverage["generated"] = True
        evidence["output"] = str(destination)
        (staging / "pyalamode-evidence.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        # Re-read policy before publishing: policy edits are also freshness changes.
        current_policy, current_error = load_policy(project_root)
        if current_error or current_policy != policy:
            raise OSError("project policy changed after checking")
        if foundation_identities() != evidence["product_artifacts"]:
            raise OSError("product runtime/checker bytes changed after checking")
        final_integrations = integration_snapshot(current_policy, project_root)
        if final_integrations["errors"] or any(final_integrations["inputs"].get(name) != value for file in result.results for name, value in file.integration_inputs.items()):
            if not final_integrations["errors"] and _integration_freshness(result, final_integrations, "artifact publication"):
                raise _IntegrationFreshnessError
            raise OSError("integration identity/manifest/expiry changed before artifact publication")
        for file in result.results:
            raw = _owned_source_bytes(file.path, project_root) if result.migration is not None else Path(file.path).read_bytes()
            if raw != raw_snapshots[file.path]:
                raise OSError("source changed during guard generation: " + file.path)
        if result.migration is not None:
            from .migration_views import make_prepublish
            make_prepublish(result._migration_snapshot, result._migration_state,
                            result._migration_reference_receipts)()
        captured["prepublish"]()
        staging.rename(destination)
        result.output = str(destination)
        for boundary in result.guarded_exports:
            boundary["generated"] = True
        for coverage in result.debug_coverage:
            coverage["generated"] = True
    except _IntegrationFreshnessError:
        if staging and staging.exists():
            shutil.rmtree(staging)
    except (OSError, ValueError, SyntaxError, TypeError, StopIteration, KeyError, RecursionError) as error:
        if staging and staging.exists():
            shutil.rmtree(staging)
        if not result.status:
            result.tooling.append(diagnostic("PAL001", str(destination), f"build stopped without publishing an artifact: {error}", origin="build output"))
    return result


def _producer_external_context(payload, actual, claimed, graph, producer_policy):
    """Detached birth-to-current relation; never supplies consumer permission."""
    from .distribution import DistributionError
    from .integration_contracts import _digest
    from .migration import _assumption
    context_keys = {"approval", "dependency_sha256", "installed_identity", "admission", "identity_error"}
    producer_inputs = payload["inputs"]["integration_inputs"]
    approvals = {row["operation"]: row for row in producer_policy.get("integration_approvals", [])}
    expected = copy.deepcopy(claimed)
    origins = {}
    for row in claimed["external_assumptions"]:
        operation = row["identity"]
        current = graph.integrations.get(operation.rsplit(".", 1)[-1])
        recorded = producer_inputs.get(operation)
        if current is None or recorded is None:
            raise DistributionError("external producer origin lacks captured operation inputs")
        try:
            _assumption(row, producer_inputs)
        except ValueError as error:
            raise DistributionError("external producer origin is invalid: " + str(error)) from error
        approval = approvals.get(operation)
        if (producer_policy.get("external_trust", "deny") != "approved" or approval is None
                or sum(entry["operation"] == operation for entry in producer_policy.get("integration_approvals", [])) != 1
                or row["admission"] != "approved" or recorded["admission"] != "approved"
                or recorded["identity_error"] is not None or row["approval"] != approval
                or recorded["approval"] != approval
                or approval["contract_sha256"] != row["contract_sha256"]
                or approval["dependency_sha256"] != row["dependency_sha256"]):
            raise DistributionError("external producer approval disagrees with captured original policy")
        identity = row["installed_identity"]
        if (identity is None or identity["distribution"] != "CPython-stdlib"
                or identity["version"] != "3.13.1" or identity["cache_tag"] != "cpython-313"
                or "t" in identity["abiflags"]
                or identity["platform"] not in {"darwin", "linux"}
                or identity["operation"] != operation
                or identity["invocation_backend"] != current["invocation_backend"]
                or identity["native_operations"] != current["native_operations"]
                or identity["adapter_artifact"]["sha256"] != payload["producer"]["product_artifacts"]["integrations.py"]
                or _digest(identity) != row["dependency_sha256"]):
            raise DistributionError("external producer installed identity disagrees with product/native operation")
        current_input = graph.integration_snapshot["inputs"][operation]
        if (current["admission"] != "approved" or current["identity_error"] is not None
                or {key:current[key] for key in current_input} != current_input
                or current["installed_identity"] is None
                or _digest(current["installed_identity"]) != current["dependency_sha256"]
                or current["installed_identity"]["adapter_artifact"]["sha256"] != payload["producer"]["product_artifacts"]["integrations.py"]):
            raise DistributionError("current external context is not its captured local approval/identity")
        current_assumption = SourceGraph.external_assumption(current)
        if {k:v for k,v in row.items() if k not in context_keys} != {k:v for k,v in current_assumption.items() if k not in context_keys}:
            raise DistributionError("external producer semantic contract disagrees with current catalog")
        if operation in origins:
            raise DistributionError("duplicate external producer origin")
        origins[operation] = (row, current_assumption, current)
    if {r["identity"] for r in actual["external_assumptions"]} != set(origins):
        raise DistributionError("external producer assumption closure disagrees with authored source")
    for row in actual["external_assumptions"]:
        if row != origins[row["identity"]][1]:
            raise DistributionError("current external assumption disagrees with captured local catalog")
    expected["external_assumptions"] = [copy.deepcopy(origins[r["identity"]][1]) for r in claimed["external_assumptions"]]
    for index, row in enumerate(claimed["operation_contracts"]):
        operation = row["identity"]
        if not operation.startswith("pyalamode.integrations."):
            continue
        if operation not in origins:
            raise DistributionError("external operation lacks its producer assumption")
        original, _, current = origins[operation]
        if ({k:v for k,v in row.items() if k not in context_keys} != {k:v for k,v in current.items() if k not in context_keys}
                or {key:row[key] for key in producer_inputs[operation]} != producer_inputs[operation]
                or SourceGraph.external_assumption(row) != original):
            raise DistributionError("external producer operation disagrees with original inputs/current semantic catalog")
        expected["operation_contracts"][index] = copy.deepcopy(current)
    for operation, (original, current, _) in origins.items():
        def token(row):
            return "external " + operation + " contract=" + row["contract_sha256"] + " dependency=" + str(row["dependency_sha256"]) + " approval=" + row["admission"]
        old_token, new_token = token(original), token(current)
        if claimed["trust"].count(old_token) != 1 or actual["trust"].count(new_token) != 1:
            raise DistributionError("external trust token is not the exact captured producer/current origin")
        expected["trust"] = [new_token if item == old_token else item for item in expected["trust"]]
    if origins:
        if claimed["trust"] != sorted(claimed["trust"]) or actual["trust"] != sorted(actual["trust"]):
            raise DistributionError("external origin trust order differs from actual source derivation")
        expected["trust"].sort()
    return expected


def _distribution_contract_relation(payload,actual,claimed,graph,kind,producer_policy=None):
    """Compare producer structure to current declarations; paths are provenance.

    Original source order comes from the current AST, never canonical JSON map
    iteration. Receiver external approvals/bounds are independently recomputed.
    """
    from .distribution import DistributionError
    producer_paths={}
    producer_root=None
    for row in payload["exports"]:
        m=next(m for m in payload["modules"] if m["module"]==row["selector"].split(":")[0])
        path=row["contract"]["path"];suffix="/"+m["authored_path"]
        if not path.startswith("/") or not path.endswith(suffix):raise DistributionError("producer authored path/declaration mismatch")
        prefix=path[:-len(suffix)]
        if producer_root is not None and producer_root!=prefix:raise DistributionError("conflicting producer provenance roots")
        producer_root=prefix
    for m in payload["modules"]:producer_paths[producer_root+"/"+m["authored_path"]]=m["module"]
    for receipt in payload["inputs"]["checked_dependencies"].values():
        for name,row in receipt["observed"]["authored_sources"].items():
            mod=Path(name).with_suffix("").as_posix().replace("/",".").removesuffix(".__init__")
            producer_paths[row["path"]]=mod
    current_paths={p:graph.module_name(p) for p in graph.analyzers}
    def normalized(value,paths,key=None,target=False):
        target = target or key in {"dependencies", "target", "targets", "callback", "callback_targets", "callable_targets", "callable_defaults", "return_callable_targets", "invoked_targets", "callable_dependencies", "callable_arguments"}
        if type(value) is str:
            if (key == "path" or target) and value in paths:return "source:"+paths[value]
            if target and "::" in value:
                path,tail=value.split("::",1)
                if path in paths:return "target:"+paths[path]+"::"+tail
            return value
        if type(value) is list:return [normalized(v,paths,key,target) for v in value]
        if type(value) is dict:return {k:normalized(v,paths,k,target) for k,v in value.items()}
        return value
    if kind == "function":
        owners={p:next(q for q,m in current_paths.items() if m==name) for p,name in producer_paths.items() if name in current_paths.values()}
        relation={"owners":owners,"occurrences":{},"aliases":{}}
        comparison=_contract_comparison(claimed,actual,relation=relation)
        expected=_producer_external_context(payload,actual,claimed,graph,producer_policy or {})
        counterpart=_contract_comparison(expected,actual,relation=relation)
        for row, derived in zip(comparison["fields"],counterpart["fields"]):
            if row["field"] in {"trust","operation_contracts","external_assumptions"} and expected[row["field"]] != claimed[row["field"]]:
                row.update(matched=derived["matched"],rule="verified-producer-origin-context")
        comparison["matched"]=all(row["matched"] for row in comparison["fields"])
        if not comparison["matched"]:
            mismatched = ", ".join(row["field"] for row in comparison["fields"] if not row["matched"])
            raise DistributionError("complete producer contract disagrees with current authored derivation: " + mismatched)
        return comparison
    keys=tuple(actual)
    for key in keys:
        if normalized(actual[key],current_paths,key)!=normalized(claimed[key],producer_paths,key):raise DistributionError("producer structure disagrees with current authored declaration: "+key)


class _IntrinsicSourceGraph(SourceGraph):
    """Captured installed declarations only; never resolve consumer files."""

    _intrinsic_schema_outputs = True

    def resolve_module(self, name):
        candidate=self.resolved_modules.get(name)
        if candidate is not None:return Path(candidate)
        return Path(self.modules[name].path) if name in self.modules else None


def _intrinsic_distribution_graph(snapshot, policy, integrations, root):
    """Fresh private source derivation, never consumer admission evidence.

    This adds one bounded installed-closure analysis even on warm semantic
    cache hits. Its mutable metadata and results are fully detached.
    """
    if not snapshot["sources"]:return None, {}
    detached=copy.deepcopy(snapshot)
    producer_policy = copy.deepcopy(policy)
    for receipt in detached["receipts"].values():
        if receipt.get("_producer_policy"):
            original = receipt["_producer_policy"]
            for key in ("effect_bounds",): producer_policy[key]={**producer_policy.get(key,{}),**original.get(key,{})}
            for key in ("builders","tasks"): producer_policy[key]=producer_policy.get(key,False) or original.get(key,False)
            producer_policy["explicit_cases"]=sorted(set(producer_policy.get("explicit_cases",[]))|set(original.get("explicit_cases",[])))
    intrinsic=_IntrinsicSourceGraph(detached["sources"],root,False,
        {**producer_policy,"_integration_snapshot":copy.deepcopy(integrations),"_distribution_snapshot":detached,"_raw_sources":detached["raw_sources"]})
    dependencies=_source_dependencies({p:a.source for p,a in intrinsic.analyzers.items()},root,intrinsic)
    for path,analyzer in intrinsic.analyzers.items():analyzer.dependencies.update(dependencies[path])
    intrinsic.analyze({})
    for receipt in detached["receipts"].values():
        if receipt.get("_producer_policy"):
            files=[a.result for a in intrinsic.analyzers.values() if intrinsic.source_owners.get(a.path)==receipt["declaration"]["name"]]
            projection=ProjectResult(results=files)
            _guard_plan(projection,receipt["_producer_policy"],root,intrinsic)
    return intrinsic, dependencies


def _finish_distributions(result, snapshot, graph, root, intrinsic):
    from .distribution import public_receipts, digest, DistributionError, DistributionDerivationStale, read
    from .guardgen import record_schemas, debug_source, facade_source, debug_derivation, facade_derivation
    from dataclasses import asdict
    records = record_schemas([a.result for a in intrinsic.analyzers.values()]) if intrinsic else {}
    result.dependency_events = []
    for name, receipt in snapshot["receipts"].items():
        owned_paths = [p for p, owner in graph.source_owners.items() if owner == name]
        if receipt["admission"] == "current":
            payload = receipt["_payload"]
            try:
                source_status = max((graph.analyzers[p].result.status for p in owned_paths), default=1)
                if graph.distribution_dependency_replacements:source_status=max(source_status,1)
                proven = []
                for row in payload["exports"]:
                    selector = row["selector"]
                    namespace, export = selector.split(":")
                    analyzer = intrinsic.modules.get(namespace) if intrinsic else None
                    if analyzer is None:
                        raise DistributionError("export absent from actual source")
                    public = public_result(analyzer.result,intrinsic.source_units[analyzer.path])
                    reports = [asdict(c) for c in public.contracts] if row["kind"] == "function" else public.records if row["kind"] == "record" else public.cases if row["kind"] == "case" else public.oneofs
                    actual = next((c for c in reports if c["name"] == export),None)
                    if actual is None:
                        source_status = max(source_status,1)
                        continue
                    keys = ("parameters","parameter_kinds","returns","defaults","effect_bound") if row["kind"] == "function" else ("schema","fields","defaults") if row["kind"] == "record" else ("schema","domain","fields","defaults") if row["kind"] == "case" else ("schema","cases","case_fingerprint")
                    if any(actual[k] != row["contract"][k] for k in keys):
                        raise DistributionError("producer contract disagrees with parsed declarations")
                    if analyzer.result.status==0:
                        comparison=_distribution_contract_relation(payload,actual,row["contract"],intrinsic,row["kind"],receipt.get("_producer_policy"))
                        if row["kind"]=="function":receipt.setdefault("_contract_comparisons",{})[selector]=comparison
                    current=graph.modules[namespace]
                    current_public=public_result(current.result,graph.source_units[current.path])
                    current_reports=[asdict(c) for c in current_public.contracts] if row["kind"]=="function" else current_public.records if row["kind"]=="record" else current_public.cases if row["kind"]=="case" else current_public.oneofs
                    current_actual=next((c for c in current_reports if c["name"]==export),None)
                    if current_actual is None:source_status=max(source_status,1)
                    else:proven.append({**row,"contract":current_actual})
                base = Path(receipt["_base"])
                for m in payload["modules"]:
                    analyzer = intrinsic.modules[m["module"]]
                    unit = intrinsic.source_units[analyzer.path]
                    if analyzer.result.status==0:
                        expected_init={"source_evidence":analyzer.result.initialization_evidence,"effects":[] if analyzer.module_mode and analyzer.result.verified else None,"failures":analyzer.result.initialization_failures if analyzer.module_mode and analyzer.result.verified else None}
                        if m["initialization"]!=expected_init:raise DistributionError("producer initialization disagrees with actual source")
                        def setup_normalized(rows):return [{k:v for k,v in row.items() if k!="path"} for row in rows]
                        if setup_normalized(m["setup_observations"])!=setup_normalized(public_result(analyzer.result,unit).setup_observations):raise DistributionError("producer setup disagrees with actual source")
                    raw = snapshot["raw_sources"][analyzer.path]
                    file = copy.deepcopy(analyzer.result)
                    file.path=m["authored_path"]
                    for c in file.contracts:c.path=m["authored_path"]
                    if unit.source_map:
                        if unit.normalized_bytes != read(base/m["lowered_path"],8*1024*1024) or map_bytes(unit.source_map) != read(base/m["map_path"],32*1024*1024):
                            raise DistributionDerivationStale("valid dialect lowering/map fails exact regeneration")
                        derivation = debug_derivation(unit,file,records) if payload["guards"]["mode"] == "debug" else None
                        expected = derivation.generated_bytes if derivation else unit.normalized_bytes
                        expected_map=sm.compose_maps(unit.source_map,derivation.source_map,source=raw,intermediate=unit.normalized_bytes,generated=expected) if derivation else unit.source_map
                        mapped_row=payload["guards"]["source_maps"][m["installed_path"]]
                        if map_bytes(expected_map)!=read(base/mapped_row["path"],32*1024*1024):raise DistributionDerivationStale("valid runtime map fails exact generation")
                    elif payload["guards"]["mode"] == "debug": expected = debug_source(analyzer.source,file,records).encode()
                    else: expected=raw
                    if (base/m["installed_path"]).read_bytes() != expected:
                        raise DistributionError("installed source fails authored/generator derivation")
                for alias in payload["guards"]["exports"]:
                    original, export = alias["original_boundary"].split(":")
                    rows = [r for r in payload["exports"] if r["kind"]=="function" and r["selector"].split(":")[0]==original and any(g["original_boundary"]==r["selector"] for g in payload["guards"]["exports"])]
                    contracts = [copy.deepcopy(c) for c in intrinsic.modules[original].result.contracts if original+":"+c.name in {r["selector"] for r in rows}]
                    for c in contracts:c.path=next(m["authored_path"] for m in payload["modules"] if m["module"]==original)
                    facade = alias["public_boundary"].split(":")[0]
                    analyzer = intrinsic.modules[original]
                    suffix = "/__init__.py" if Path(analyzer.path).name in {"__init__.py","__init__.pya"} else ".py"
                    target=base/(facade.replace(".","/")+suffix)
                    unit=intrinsic.source_units[analyzer.path]
                    if unit.source_map:
                        derivation=facade_derivation(unit,original,contracts,records,target.relative_to(base).as_posix())
                        expected=derivation.generated_bytes
                        expected_map=sm.compose_maps(unit.source_map,derivation.source_map,source=unit.authored_bytes,intermediate=unit.normalized_bytes,generated=expected)
                        map_row=payload["guards"]["source_maps"][target.relative_to(base).as_posix()]
                        if map_bytes(expected_map)!=read(base/map_row["path"],32*1024*1024):raise DistributionDerivationStale("valid facade map fails exact generation")
                    else:expected=facade_source(analyzer.source,original,contracts,records).encode()
                    if target.read_bytes()!=expected: raise DistributionError("generated guard facade differs from current generator")
                for path in payload["guards"]["generated_files"]:
                    if path.endswith("/__init__.py") and path not in {g["public_boundary"].split(":")[0].replace(".","/")+"/__init__.py" for g in payload["guards"]["exports"] if Path(intrinsic.modules[g["original_boundary"].split(":")[0]].path).name in {"__init__.py","__init__.pya"}}:
                        if (base/path).read_bytes()!=b'"""Selected guarded boundaries."""\n':raise DistributionError("generated namespace initializer differs")
                if all(intrinsic.modules[m["module"]].result.status==0 for m in payload["modules"]):
                    from .guardgen import supported_schema
                    expected_debug=[]
                    if payload["guards"]["mode"]=="debug":
                        for m in payload["modules"]:
                            analyzer_=intrinsic.modules[m["module"]]
                            for c in public_result(analyzer_.result,intrinsic.source_units[analyzer_.path]).contracts:
                                expected_debug.append({"path":m["authored_path"],"name":c.name,"line":c.line,"parameters":{n:s for n,s in c.parameters.items() if supported_schema(s,records)},"returns":c.returns if supported_schema(c.returns,records) else None,"locals":[r for r in c.data_assertions if supported_schema(r["schema"],records)],"callable_validation":"excluded; caller evidence obligations remain","capability_validation":"excluded; exact interface, allowed operation and lifetime obligations remain","generated":True})
                    if sorted(expected_debug,key=lambda r:(r["path"],r["line"],r["name"]))!=sorted(payload["guards"]["debug"],key=lambda r:(r["path"],r["line"],r["name"])):raise DistributionError("producer debug metadata disagrees with actual source")
                receipt["source_status"]=source_status
                receipt["verified"]=source_status==0
                receipt["exports"]=proven if source_status==0 else []
                receipt["diagnostics"]=[asdict(d) for p in owned_paths for d in public_result(graph.analyzers[p].result,graph.source_units[p]).diagnostics]
            except DistributionDerivationStale as e:
                receipt.update(admission="stale", input_status=1, complete=True, source_status=None, verified=False, exports=[])
                receipt["_stale_reason"]="stale-artifact"
            except (OSError,ValueError,TypeError,KeyError,SyntaxError,RecursionError) as e:
                receipt.update(admission="tooling", input_status=2, complete=False, source_status=2,verified=False,exports=[])
                result.tooling.append(diagnostic("PAL001",str(root),"installed derivation failed: "+str(e),origin="installed distribution derivation"))
        status=max(receipt["input_status"],receipt["source_status"] or 0)
        if status:
            rule="PAL370" if receipt["admission"] in {"missing","stale","incompatible"} else "PAL371" if receipt["admission"]=="unpublished" else "PAL371"
            upstream=None
            if receipt["source_status"]==1:
                for p in owned_paths:
                    errors=graph.analyzers[p].result.diagnostics
                    if errors:
                        error=next((d for d in errors if d.rule not in {"PAL211"}),errors[0]);namespace=graph.module_name(p)
                        upstream={"rule":error.rule,"selector":"module:"+namespace if error.boundary=="<module>" else namespace+":"+error.boundary}
                        break
            reason_code=("missing-evidence" if receipt["observed"]["owners"] else "missing-distribution") if receipt["admission"]=="missing" else receipt.get("_stale_reason","stale-artifact") if receipt["admission"]=="stale" else "incompatible-version" if receipt["admission"]=="incompatible" else "dependency-source-refused"
            required=[]
            for file in result.results:
                analyzer=graph.analyzers[file.path]
                for node in analyzer.tree.body if analyzer.tree else []:
                    imported=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or ""] if isinstance(node,ast.ImportFrom) else []
                    if any(value.split(".")[0] in receipt["declaration"]["packages"] for value in imported):
                        required.append("module:"+graph.module_name(file.path))
                        if status==1:
                            missing_names={a.asname or a.name.split(".")[0] for a in node.names} if isinstance(node,ast.Import) else {a.asname or a.name for a in node.names}
                            def consequence(d):
                                if d.origin=="dependency gate":return True
                                nodes=[n for n in ast.walk(analyzer.tree) if getattr(n,"lineno",None)==d.line and getattr(n,"col_offset",-1)+1==d.column]
                                for n in nodes:
                                    expr=n.value if isinstance(n,ast.Return) else n
                                    if d.rule=="PAL240" and isinstance(expr,ast.Name) and expr.id in missing_names:return True
                                    if d.rule in {"PAL211","PAL230"} and isinstance(expr,ast.Call):
                                        func=expr.func
                                        while isinstance(func,ast.Attribute):func=func.value
                                        if isinstance(func,ast.Name) and func.id in missing_names:return True
                                return False
                            file.diagnostics[:]=[d for d in file.diagnostics if not consequence(d)]
                            context={"dependency":{k:receipt["declaration"][k] for k in ("name","version","packages")},"selector":None,"rule":rule,"reason_code":reason_code,"site":"import","upstream":upstream}
                            file.diagnostics.append(diagnostic(rule,file.path,"checked dependency "+name+" is "+receipt["admission"]+" or its source gate failed",line=node.lineno,column=node.col_offset+1,origin="installed checked dependency",dependency_context=context))
                            for c in file.contracts:
                                info=next((i for i in analyzer.infos.values() if i.qualified==c.name),None)
                                if info and not any(p in owned_paths for p in info.dependencies) and receipt["admission"]=="current":continue
                                if info and receipt["admission"]!="current" and not any(isinstance(n,ast.Name) and n.id in missing_names for n in ast.walk(info.node)):continue
                                c.source_evidence="unverified: checked dependency refused";c.freshness="no successful checked claim";c.behavior="unverified behavior; no certified effect bound"
            result.dependency_events.append({"dependency":{k:receipt["declaration"][k] for k in ("name","version","packages")},"rule":rule,"reason_code":reason_code,"selector":None,"required_by":sorted(set(required)),"input_status":receipt["input_status"],"source_status":receipt["source_status"]})
        result.dependency_status=max(result.dependency_status,status)
    result.distribution_inputs=public_receipts(snapshot)
    result.checked_dependencies=list(result.distribution_inputs.values())


def _distribution_check_freshness(result,snapshot,policy,root):
    from .distribution import distribution_snapshot,public_receipts
    current=distribution_snapshot(policy,root)
    if current["errors"]:
        result.tooling.extend(diagnostic("PAL001",str(root),e,origin="installed freshness") for e in current["errors"])
        return False
    changed=[k for k,r in current["receipts"].items() if r["fingerprint"]!=snapshot["receipts"][k]["fingerprint"]]
    if not changed:return True
    for name in changed:
        row=current["receipts"][name]
        row.update(admission="changed",input_status=1,source_status=None,verified=False,exports=[])
        snapshot["receipts"][name]=row
        declaration={k:row["declaration"][k] for k in ("name","version","packages")}
        required=[]
        for file in result.results:
            analyzer_sources=[]
            try: tree=ast.parse(Path(file.path).read_bytes())
            except (OSError,SyntaxError):continue
            for node in tree.body:
                imports=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module or ""] if isinstance(node,ast.ImportFrom) else []
                if any(n.split(".")[0] in declaration["packages"] for n in imports):
                    required.append("module:"+_module_name(file.path,Path(root)))
                    context={"dependency":declaration,"selector":None,"rule":"PAL372","reason_code":"inputs-changed","site":"import","upstream":None}
                    file.diagnostics.append(diagnostic("PAL372",file.path,"installed inputs changed during gate",line=node.lineno,column=node.col_offset+1,origin="installed freshness",dependency_context=context))
        result.dependency_events.append({"dependency":declaration,"rule":"PAL372","reason_code":"inputs-changed","selector":None,"required_by":sorted(set(required)),"input_status":1,"source_status":None})
    result.dependency_status=max(result.dependency_status,1)
    result.distribution_inputs=public_receipts(snapshot);result.checked_dependencies=list(result.distribution_inputs.values())
    return False


def _distribution_prepublish(result,snapshot,policy,root,capture):
    from .distribution import distribution_snapshot
    if not _distribution_check_freshness(result,snapshot,policy,root):raise ValueError("installed inputs changed")
    if foundation_identities()!=capture.get("products",foundation_identities()): raise ValueError("product bytes changed")
    current_policy,error=load_policy(root)
    if error or current_policy!=policy: raise ValueError("policy changed before publication")
    for path,raw in capture["raw_sources"].items():
        if _owned_source_bytes(path,root)!=raw: raise ValueError("owned source changed before publication")
    selected,errors=discover_paths(capture.get("requested",[root]),root)
    if errors or [str(p) for p in selected]!=capture["selected_paths"]: raise ValueError("source inventory changed before publication")
    _integration_freshness(result,integration_snapshot(policy,root),"publication")
    if result.status: raise ValueError("current source/dependency gate refused")
