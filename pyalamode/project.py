"""Local check/build gate and disposable content-addressed analysis cache."""

from __future__ import annotations

import hashlib
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
                    Diagnostic, FunctionContract, diagnostic, foundation_identities)

_EXCLUDED = frozenset({".git", ".venv", "__pycache__", "build", "dist", ".pyalamode-cache"})


@dataclass
class ProjectResult:
    results: list[CheckResult] = field(default_factory=list)
    tooling: list[Diagnostic] = field(default_factory=list)
    audit: bool = False
    elapsed_seconds: float = 0.0
    output: str | None = None

    @property
    def status(self) -> int:
        return max([0] + [r.status for r in self.results] + ([2] if self.tooling else []))

    @property
    def verified(self) -> bool:
        return not self.audit and self.status == 0

    def to_dict(self) -> dict:
        from dataclasses import asdict
        return {"schema": 1, "edition": EDITION, "checker": CHECKER_VERSION, "target": TARGET,
                "operation_contract": OPERATION_VERSION, "product_artifacts": foundation_identities(),
                "mode": "audit" if self.audit else "strict",
                "verified": self.verified, "status": self.status,
                "elapsed_seconds": self.elapsed_seconds, "output": self.output,
                "tooling": [asdict(d) for d in self.tooling],
                "files": [r.to_dict() for r in self.results],
                "coverage": {"eligible_functions": sum(r.eligible_functions for r in self.results),
                             "selected_functions": sum(r.selected_functions for r in self.results),
                             "analyzed_call_sites": sum(r.analyzed_call_sites for r in self.results)},
                "claim_scope": "Selected functions, stable dependencies and functional-module initialization; ordinary shells and unrelated ordinary initialization are unchecked."}


def runtime_error(target: str = TARGET) -> str | None:
    if target != TARGET:
        return f"unsupported requested target {target}; published target is {TARGET}"
    if platform.python_implementation() != "CPython" or tuple(sys.version_info[:3]) != (3, 13, 1):
        return f"unsupported running interpreter {platform.python_implementation()} {platform.python_version()}; use CPython 3.13.1"
    if sys.platform not in {"darwin", "linux"}:
        return f"unsupported platform {sys.platform}; supported platforms are macOS and Linux"
    if sysconfig_free_threaded():
        return "free-threaded CPython builds are outside the supported target"
    return None


def sysconfig_free_threaded() -> bool:
    import sysconfig
    return bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


def load_policy(root: Path) -> tuple[dict, str | None]:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}, None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        tool = data.get("tool", {})
        if not isinstance(tool, dict):
            return {}, "pyproject tool must be a table"
        policy = tool.get("pyalamode", {})
        if not isinstance(policy, dict):
            return {}, "tool.pyalamode must be a table"
        expected = {"schema": 1, "edition": EDITION, "runtime": "cpython-3.13",
                    "boundary_guards": "off", "external_trust": "deny", "builders": False,
                    "require_modules": []}
        for key, value in policy.items():
            if key == "require_modules":
                if type(value) is not list or any(type(pattern) is not str or not pattern or pattern.startswith("/") or ".." in Path(pattern).parts or "\\" in pattern for pattern in value):
                    return policy, "require_modules must be a list of nonempty project-relative glob patterns"
            elif key not in expected or type(value) is not type(expected[key]) or value != expected[key]:
                return policy, f"unsupported policy field/value {key}={value!r}; milestone 2 admits only its closed module configuration"
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
                children[:] = sorted(c for c in children if c not in _EXCLUDED and not c.endswith(".egg-info"))
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
                             binding_context=payload.get("binding_context", []))
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
                audit: bool = False, target: str = TARGET, cache: bool = True) -> ProjectResult:
    started = time.perf_counter()
    project_root = Path(root or Path.cwd()).resolve()
    result = ProjectResult(audit=audit)
    error = runtime_error(target)
    if error:
        result.tooling.append(diagnostic("PAL002", str(project_root), error, origin="runtime target"))
    policy, error = load_policy(project_root)
    if error:
        result.tooling.append(diagnostic("PAL001", str(project_root / "pyproject.toml"), error, origin="project policy"))
    files, errors = discover_paths(paths or [], project_root)
    result.tooling.extend(errors)
    if result.tooling:
        result.elapsed_seconds = time.perf_counter() - started
        return result
    cache_path = project_root / ".pyalamode-cache"
    cache_policy = {**policy, "analysis_mode": "audit" if audit else "strict", "platform": sys.platform}
    raw_sources = {}
    sources, errors = load_sources(files, project_root, raw_sources)
    result.tooling.extend(errors)
    if errors:
        result.elapsed_seconds = time.perf_counter() - started
        return result
    dependencies = _source_dependencies(sources, project_root)
    graph = SourceGraph(sources, project_root, audit, cache_policy)
    contexts = {path: graph.binding_context(path, dependencies[path]) for path in sources}
    keys = {path: fingerprint(raw_sources[path], {**cache_policy, "path": path,
            "source_dependencies": {d: hashlib.sha256(raw_sources[d]).hexdigest() for d in sorted(dependencies[path])},
            "binding_context": contexts[path]})
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
    for path, analyzed in sorted(analyzed_results.items()):
        analyzed.fingerprint = keys[path]
        analyzed.dependencies = {d: hashlib.sha256(raw_sources[d]).hexdigest() for d in sorted(dependencies[path])}
        analyzed.binding_context = contexts[path]
        if cache and path not in cached:
            _cache_write(cache_path, analyzed)
        result.results.append(analyzed)
    result.elapsed_seconds = time.perf_counter() - started
    return result


def _source_dependencies(sources: dict[str, str], root: Path) -> dict[str, set[str]]:
    direct = {path: set() for path in sources}
    for path, source in sources.items():
        module = _module_name(path, root)
        for node in ast.walk(ast.parse(source, filename=path, feature_version=(3, 13))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else []
            if isinstance(node, ast.ImportFrom):
                base = _import_name(node, module, Path(path).name == "__init__.py")
                names = [base] + [base + "." + a.name for a in node.names if a.name != "*"]
            for name in names:
                parts = name.split(".")
                for count in range(1, len(parts) + 1):
                    target = _local_path(root, ".".join(parts[:count]))
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
                root: str | Path | None = None, target: str = TARGET) -> ProjectResult:
    project_root = Path(root or Path.cwd()).resolve()
    destination = Path(output or project_root / "build" / "pyalamode").resolve()
    # Builds always freshly analyze source; caches accelerate check only.
    result = check_paths(paths, root=project_root, target=target, cache=False)
    if result.status:
        return result
    if not any(file.selected_functions or file.module_mode for file in result.results):
        result.tooling.append(diagnostic("PAL001", str(project_root), "build requires a participating function or functional module; no checked artifact was produced"))
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
        evidence["artifact_kind"] = "local compatible source tree; package distribution/consumer verification is not implemented"
        evidence["artifact_files"] = {}
        for file in result.results:
            source = Path(file.path)
            raw = source.read_bytes()
            # Source changes during analysis/copy invalidate this gate rather than publish stale evidence.
            policy, _ = load_policy(project_root)
            dependency_bytes = {d: hashlib.sha256(Path(d).read_bytes()).hexdigest() for d in file.dependencies}
            check_key = fingerprint(raw, {**policy, "analysis_mode": "strict", "platform": sys.platform, "path": str(source), "source_dependencies": dependency_bytes, "binding_context": file.binding_context})
            if check_key != file.fingerprint:
                raise OSError(f"source changed after checking: {source}")
            relative = source.relative_to(base)
            copied = staging / relative
            copied.parent.mkdir(parents=True, exist_ok=True)
            copied.write_bytes(raw)
            evidence["artifact_files"][relative.as_posix()] = hashlib.sha256(raw).hexdigest()
        evidence["output"] = str(destination)
        (staging / "pyalamode-evidence.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        # Re-read policy before publishing: policy edits are also freshness changes.
        current_policy, current_error = load_policy(project_root)
        if current_error or current_policy != policy:
            raise OSError("project policy changed after checking")
        staging.rename(destination)
        result.output = str(destination)
    except (OSError, ValueError) as error:
        if staging and staging.exists():
            shutil.rmtree(staging)
        result.tooling.append(diagnostic("PAL001", str(destination), f"build stopped without publishing an artifact: {error}", origin="build output"))
    return result
