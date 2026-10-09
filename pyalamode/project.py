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

from .checker import SourceGraph, analyze_file, analyze_source, fingerprint, load_sources, _import_name, _local_path, _module_name
import ast
from .model import (CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, CheckResult,
                    Diagnostic, FunctionContract, diagnostic, foundation_identities, runtime_environment)
from .encoding_contracts import ENCODING_VERSION, operation_catalog as encoding_catalog
from .standard_contracts import STANDARD_VERSION, operation_catalog
from .integration_contracts import INTEGRATION_VERSION, integration_snapshot, validate_policy

_EXCLUDED = frozenset({".git", ".venv", "__pycache__", "build", "dist", ".pyalamode-cache", ".pyalamode"})


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
        return {"schema": 1, "edition": EDITION, "checker": CHECKER_VERSION, "target": TARGET,
                "operation_contract": OPERATION_VERSION, "product_artifacts": foundation_identities(),
                "runtime_environment": runtime_environment(),
                "encoding_operation_version": ENCODING_VERSION, "encoding_catalog": encoding_catalog(),
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
                             "selected_functions": sum(r.selected_functions for r in self.results),
                             "selected_records": sum(len(r.records) for r in self.results),
                             "selected_variants": sum(len(r.variants) for r in self.results),
                             "analyzed_call_sites": sum(r.analyzed_call_sites for r in self.results)},
                "claim_scope": "Selected functions, record/variant declarations, stable dependencies and functional-module initialization; ordinary shells and unrelated ordinary initialization are unchecked."}


@dataclass
class ProjectSnapshot:
    """Read-only captured full-project evidence, including explicit unsaved provenance."""
    result: ProjectResult
    sources: dict[str, str]
    inputs: dict
    freshness: str
    snapshot: str
    graph: SourceGraph | None = field(default=None, repr=False)


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
        if (not candidate.is_relative_to(project_root) or not candidate.is_file() or candidate.suffix != ".py"
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
                               "disk_sha256": overlay_disk[path] if path in normalized else hashlib.sha256(raw).hexdigest()}
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
            for declaration in [*file.records, *file.variants]:
                declaration["source_evidence"] = "unverified: stale editor snapshot"
            for contract in file.contracts:
                contract.source_evidence = "unverified: stale editor snapshot"
                contract.freshness = "stale; recheck required"
                contract.behavior = "unverified behavior; no certified effect bound"
    key = hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ProjectSnapshot(result, captured.get("sources", {}), inputs, freshness, key, captured.get("graph"))


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
                    "boundary_guards": "off", "external_trust": "deny", "builders": False,
                    "require_modules": [], "guarded_exports": [], "effect_bounds": {}, "explicit_cases": [],
                    "integration_manifests": [], "integration_approvals": [], "required_exports": [], "migration": {}, "distribution": {}, "checked_dependencies": []}
        for key, value in policy.items():
            if key in {"distribution", "checked_dependencies"}:
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
                        return policy, "effect_bounds requires unique IO/State/Clock/Random/Environment family lists; Task is reserved"
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
        path = Path(value).resolve()
        if path.is_file() and path.suffix == ".py":
            discovered.add(path)
        elif path.is_dir():
            for directory, children, files in os.walk(path):
                children[:] = sorted(c for c in children if c not in _EXCLUDED and not c.endswith(".egg-info") and not c.startswith(".pyalamode-build-"))
                for name in files:
                    if name.endswith(".py"):
                        discovered.add((Path(directory) / name).resolve())
        else:
            errors.append(diagnostic("PAL001", str(path), "source path must be an existing Python file or directory"))
    if not discovered and not errors:
        errors.append(diagnostic("PAL001", str(root), "no Python source files were selected"))
    return sorted(discovered), errors


def _cache_read(cache: Path, key: str, path: str, audit: bool) -> CheckResult | None:
    try:
        envelope = json.loads((cache / f"{key}.json").read_text())
        payload = envelope["payload"]
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if envelope["checksum"] != digest or payload["fingerprint"] != key or payload["path"] != path:
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
                             binding_context=payload.get("binding_context", []), records=payload.get("records", []), variants=payload.get("variants", []),
                             setup_observations=payload.get("setup_observations", []),
                             unsafe_adapters=payload.get("unsafe_adapters", []), integration_inputs=payload.get("integration_inputs", {}))
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
    started = time.perf_counter()
    _capture = _capture if _capture is not None else {}
    project_root = Path(root or Path.cwd()).resolve()
    result = ProjectResult(audit=audit)
    error = runtime_error(target)
    if error:
        result.tooling.append(diagnostic("PAL002", str(project_root), error, origin="runtime target"))
    policy, error = load_policy(project_root, _read_root)
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
    graph = SourceGraph(sources, project_root, audit, {**cache_policy, "_integration_snapshot": integrations, "_distribution_snapshot": distributions}, _candidate_selection)
    dependencies = _source_dependencies(sources, project_root, graph)
    if _capture is not None:
        _capture["graph"] = graph
    contexts = {path: graph.binding_context(path, dependencies[path]) for path in sources}
    external_inputs = {path: graph.integration_context(path, dependencies[path]) for path in sources}
    keys = {path: fingerprint(raw_sources[path], {**cache_policy, "path": path,
            "source_dependencies": {d: hashlib.sha256(raw_sources[d]).hexdigest() for d in sorted(dependencies[path])},
            "binding_context": contexts[path], "integration_inputs": external_inputs[path], "checked_dependencies": public_receipts(distributions)})
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
    selected_domains = {info.module + ":" + info.node.name for info in graph.variants.values()}
    for selection in policy.get("explicit_cases", []):
        if selection not in selected_domains:
            result.tooling.append(diagnostic("PAL001", str(project_root / "pyproject.toml"), f"explicit_cases selection `{selection}` does not resolve to a checked top-level domain", origin="project pattern policy"))
    _guard_plan(result, policy, project_root, graph)
    _integration_freshness(result, integration_snapshot(policy, project_root), "check completed")
    _distribution_check_freshness(result,distributions,policy,project_root)
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
    modules = {_module_name(r.path, root): r for r in result.results}
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
                base = _import_name(node, module, Path(path).name == "__init__.py")
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
    if not any(file.selected_functions or file.module_mode or file.records or file.variants for file in result.results):
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
        source_snapshots = {}
        from .guardgen import debug_source, generate_facades, record_schemas
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
            check_key = fingerprint(raw, {**policy, "analysis_mode": "strict", "platform": sys.platform, "path": str(source), "source_dependencies": dependency_bytes, "binding_context": file.binding_context, "integration_inputs": file.integration_inputs, "checked_dependencies": captured["distribution_cache_inputs"]})
            if check_key != file.fingerprint:
                raise OSError(f"source changed after checking: {source}")
            relative = source.relative_to(base)
            copied = staging / relative
            copied.parent.mkdir(parents=True, exist_ok=True)
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            source_snapshots[file.path] = raw.decode(encoding)
            artifact_bytes = debug_source(source_snapshots[file.path], file, record_schemas(result.results+captured.get("installed_results",[]))).encode() if result.boundary_guards == "debug" else raw
            copied.write_bytes(artifact_bytes)
            if result.boundary_guards == "debug":
                compile(artifact_bytes, str(copied), "exec")
            evidence["artifact_files"][relative.as_posix()] = hashlib.sha256(artifact_bytes).hexdigest()
        for relative, raw in generate_facades(staging, result.results+captured.get("installed_results",[]), project_root, policy.get("guarded_exports", []), source_snapshots).items():
            compile(raw, str(staging / relative), "exec")
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
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            if raw.decode(encoding) != source_snapshots[file.path]:
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


def _distribution_contract_relation(payload,actual,claimed,graph,kind):
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
            mod=name[:-3].replace("/",".").removesuffix(".__init__")
            producer_paths[row["path"]]=mod
    current_paths={p:graph.module_name(p) for p in graph.analyzers}
    def normalized(value,paths):
        if type(value) is str:
            if value in paths:return "source:"+paths[value]
            if "::" in value:
                path,tail=value.split("::",1)
                if path in paths:return "target:"+paths[path]+"::"+tail
            return value
        if type(value) is list:return [normalized(v,paths) for v in value]
        if type(value) is dict:return {k:normalized(v,paths) for k,v in value.items()}
        return value
    keys=("name","line","parameters","parameter_kinds","returns","defaults","captures","callable_targets","callable_defaults","return_callable_targets","callable_capture_evidence","callable_default_evidence","return_callable_evidence","invoked_targets","callable_dependencies","callable_arguments","callable_operations","operations","data_assertions","borrow_scopes","effect_bound","capability_parameters") if kind=="function" else ("name","line","schema","fields","defaults") if kind=="record" else ("name","line","schema","cases","case_fingerprint")
    for key in keys:
        if normalized(actual[key],current_paths)!=normalized(claimed[key],producer_paths):raise DistributionError("producer structure disagrees with current authored declaration: "+key)
    if kind=="function":
        for key in ("failure_edges","handlers","patterns"):
            left=normalized(actual[key],current_paths);right=normalized(claimed[key],producer_paths)
            excluded={"discharged"} if key=="handlers" else {"policy_explicit"} if key=="patterns" else set()
            if [{k:v for k,v in r.items() if k not in excluded} for r in left]!=[{k:v for k,v in r.items() if k not in excluded} for r in right]:raise DistributionError("producer source row disagrees with current AST: "+key)
    stable=lambda rows:sorted(v for v in rows if not v.startswith("external "))
    if stable(actual["trust"])!=stable(claimed["trust"]):raise DistributionError("producer trust identity disagrees with actual current foundations")


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
    intrinsic=_IntrinsicSourceGraph(detached["sources"],root,False,
        {**copy.deepcopy(policy),"_integration_snapshot":copy.deepcopy(integrations),"_distribution_snapshot":detached})
    dependencies=_source_dependencies(detached["sources"],root,intrinsic)
    for path,analyzer in intrinsic.analyzers.items():analyzer.dependencies.update(dependencies[path])
    intrinsic.analyze({})
    return intrinsic, dependencies


def _finish_distributions(result, snapshot, graph, root, intrinsic):
    from .distribution import public_receipts, digest, DistributionError
    from .guardgen import record_schemas, debug_source, facade_source
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
                    reports = [asdict(c) for c in analyzer.result.contracts] if row["kind"] == "function" else analyzer.result.records if row["kind"] == "record" else analyzer.result.variants
                    actual = next((c for c in reports if c["name"] == export),None)
                    if actual is None:
                        source_status = max(source_status,1)
                        continue
                    keys = ("parameters","parameter_kinds","returns","defaults","effect_bound") if row["kind"] == "function" else ("schema","fields","defaults") if row["kind"] == "record" else ("schema","cases","case_fingerprint")
                    if any(actual[k] != row["contract"][k] for k in keys):
                        raise DistributionError("producer contract disagrees with parsed declarations")
                    if analyzer.result.status==0:_distribution_contract_relation(payload,actual,row["contract"],intrinsic,row["kind"])
                    current=graph.modules[namespace]
                    current_reports=[asdict(c) for c in current.result.contracts] if row["kind"]=="function" else current.result.records if row["kind"]=="record" else current.result.variants
                    current_actual=next((c for c in current_reports if c["name"]==export),None)
                    if current_actual is None:source_status=max(source_status,1)
                    else:proven.append({**row,"contract":current_actual})
                base = Path(receipt["_base"])
                for m in payload["modules"]:
                    analyzer = intrinsic.modules[m["module"]]
                    if analyzer.result.status==0:
                        expected_init={"source_evidence":analyzer.result.initialization_evidence,"effects":[] if analyzer.module_mode and analyzer.result.verified else None,"failures":analyzer.result.initialization_failures if analyzer.module_mode and analyzer.result.verified else None}
                        if m["initialization"]!=expected_init:raise DistributionError("producer initialization disagrees with actual source")
                        def setup_normalized(rows):return [{k:v for k,v in row.items() if k!="path"} for row in rows]
                        if setup_normalized(m["setup_observations"])!=setup_normalized(analyzer.result.setup_observations):raise DistributionError("producer setup disagrees with actual source")
                    raw = snapshot["raw_sources"][analyzer.path]
                    if payload["guards"]["mode"] == "debug":
                        file = copy.deepcopy(analyzer.result)
                        file.path=m["authored_path"]
                        for c in file.contracts:c.path=m["authored_path"]
                        expected = debug_source(analyzer.source,file,records).encode()
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
                    suffix = "/__init__.py" if Path(analyzer.path).name=="__init__.py" else ".py"
                    target=base/(facade.replace(".","/")+suffix)
                    expected=facade_source(analyzer.source,original,contracts,records).encode()
                    if target.read_bytes()!=expected: raise DistributionError("generated guard facade differs from current generator")
                for path in payload["guards"]["generated_files"]:
                    if path.endswith("/__init__.py") and path not in {g["public_boundary"].split(":")[0].replace(".","/")+"/__init__.py" for g in payload["guards"]["exports"] if Path(intrinsic.modules[g["original_boundary"].split(":")[0]].path).name=="__init__.py"}:
                        if (base/path).read_bytes()!=b'"""Selected guarded boundaries."""\n':raise DistributionError("generated namespace initializer differs")
                if all(intrinsic.modules[m["module"]].result.status==0 for m in payload["modules"]):
                    from .guardgen import supported_schema
                    expected_debug=[]
                    if payload["guards"]["mode"]=="debug":
                        for m in payload["modules"]:
                            for c in intrinsic.modules[m["module"]].result.contracts:
                                expected_debug.append({"path":m["authored_path"],"name":c.name,"line":c.line,"parameters":{n:s for n,s in c.parameters.items() if supported_schema(s,records)},"returns":c.returns if supported_schema(c.returns,records) else None,"locals":[r for r in c.data_assertions if supported_schema(r["schema"],records)],"callable_validation":"excluded; caller evidence obligations remain","capability_validation":"excluded; exact interface, allowed operation and lifetime obligations remain","generated":True})
                    if sorted(expected_debug,key=lambda r:(r["path"],r["line"],r["name"]))!=sorted(payload["guards"]["debug"],key=lambda r:(r["path"],r["line"],r["name"])):raise DistributionError("producer debug metadata disagrees with actual source")
                receipt["source_status"]=source_status
                receipt["verified"]=source_status==0
                receipt["exports"]=proven if source_status==0 else []
                receipt["diagnostics"]=[asdict(d) for p in owned_paths for d in graph.analyzers[p].result.diagnostics]
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
