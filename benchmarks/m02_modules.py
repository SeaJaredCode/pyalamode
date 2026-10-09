"""Measure a bounded M2 call graph and selective disk-cache reuse.

Run from an installed CPython 3.13.1 checkout with:
    python benchmarks/m02_modules.py --output /tmp/pyalamode-m02-modules.json

The generated application source is analyzed through check_paths, never imported
or executed. Elapsed times include tracemalloc overhead; interpreter startup,
checker imports, fixture generation, and evidence serialization are excluded.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import sysconfig
import tempfile
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

import pyalamode
from pyalamode.model import CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET
from pyalamode.project import check_paths


WORKLOAD_NAME = "branched_integer_rollup_v1"
CHECK_NAMES = (
    "cold_check",
    "warm_unchanged_check",
    "unrelated_module_edit_check",
    "branch_leaf_edit_check",
)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_digest(value: object) -> str:
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def fixture_sources(branches: int, depth: int, functions: int) -> tuple[dict[str, str], list[list[str]]]:
    """Create a closed DAG with explicit direct calls and no dynamic dispatch."""
    sources = {}
    edges = []
    foundation = [
        '"""Shared scalar and recursively immutable tuple constants."""\n# mode: fun\n',
        'BASE = 100\nLABELS = ("cents", ("USD", b"minor"))\n\n',
    ]
    for index in range(functions):
        foundation.append(
            f"def seed_{index:04d}(cents: int, adjustment: int = {index}) -> int:\n"
            "    remainder = cents - adjustment\n"
            "    if remainder < 0:\n"
            "        result = BASE + len(LABELS)\n"
            "    else:\n"
            "        result = BASE + remainder\n"
            "    return result\n\n"
        )
    sources["foundation.py"] = "".join(foundation)
    for branch in range(branches):
        for level in range(depth):
            module = f"branch_{branch:04d}_level_{level:04d}"
            previous = "foundation" if level == 0 else f"branch_{branch:04d}_level_{level - 1:04d}"
            prefix = "seed" if level == 0 else "rollup"
            imported = ", ".join(f"{prefix}_{index:04d}" for index in range(functions))
            chunks = [f"# mode: fun\nfrom {previous} import {imported}\n\n"]
            for index in range(functions):
                name = f"rollup_{index:04d}"
                if level == 0:
                    chunks.append(
                        f"def {name}(cents: int) -> int:\n"
                        f"    return seed_{index:04d}(cents) + {branch}\n\n"
                    )
                    edges.append([f"{module}.py::{name}", f"foundation.py::seed_{index:04d}"])
                else:
                    next_index = (index + 1) % functions
                    chunks.append(
                        f"def {name}(cents: int) -> int:\n"
                        f"    left = rollup_{index:04d}(cents)\n"
                        f"    right = rollup_{next_index:04d}(cents)\n"
                        "    return left + right\n\n"
                    )
                    # The local function has the same spelling as an imported
                    # function, so use aliases to keep resolution unambiguous.
                    chunks[-1] = chunks[-1].replace(
                        f"left = rollup_{index:04d}(cents)",
                        f"left = previous_{index:04d}(cents)",
                    ).replace(
                        f"right = rollup_{next_index:04d}(cents)",
                        f"right = previous_{next_index:04d}(cents)",
                    )
                    for target in {index, next_index}:
                        edges.append([f"{module}.py::{name}", f"{previous}.py::rollup_{target:04d}"])
            if level:
                aliases = ", ".join(f"rollup_{index:04d} as previous_{index:04d}" for index in range(functions))
                chunks[0] = f"# mode: fun\nfrom {previous} import {aliases}\n\n"
            sources[module + ".py"] = "".join(chunks)
    unrelated = ["# mode: fun\nUNRELATED_OFFSET = 7\n\n"]
    for index in range(functions):
        unrelated.append(
            f"def standalone_{index:04d}(cents: int) -> int:\n"
            f"    return cents + UNRELATED_OFFSET + {index}\n\n"
        )
    sources["unrelated.py"] = "".join(unrelated)
    return sources, sorted(edges)


def hardware_metadata() -> dict:
    hardware = {"machine": platform.machine(), "processor": platform.processor(),
                "logical_cpu_count": os.cpu_count()}
    if sys.platform == "darwin":
        for name, key in (("hw.model", "model"), ("machdep.cpu.brand_string", "processor"),
                          ("hw.memsize", "physical_memory_bytes")):
            try:
                value = subprocess.check_output(["sysctl", "-n", name], text=True,
                                                stderr=subprocess.DEVNULL).strip()
                hardware[key] = int(value) if key == "physical_memory_bytes" else value
            except (OSError, subprocess.CalledProcessError, ValueError):
                pass
    elif sys.platform == "linux":
        try:
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith("model name"):
                    hardware["processor"] = line.split(":", 1)[1].strip()
                    break
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemTotal:"):
                    hardware["physical_memory_bytes"] = int(line.split()[1]) * 1024
                    break
        except (OSError, ValueError, IndexError):
            pass
        # Container limits can differ substantially from host hardware.
        limits = {}
        for name in ("cpu.max", "memory.max", "cpuset.cpus.effective"):
            path = Path("/sys/fs/cgroup") / name
            try:
                limits[name] = path.read_text().strip()
            except OSError:
                pass
        if limits:
            hardware["cgroup_v2_limits"] = limits
    return hardware


def implementation_metadata() -> dict:
    package = Path(pyalamode.__file__).resolve().parent
    digests = {source.relative_to(package).as_posix(): digest(source.read_bytes())
               for source in sorted(package.rglob("*.py"))}
    metadata = {"package_version": pyalamode.__version__, "checker": CHECKER_VERSION,
                "edition": EDITION, "operation_contract": OPERATION_VERSION,
                "target": TARGET, "package_directory": str(package),
                "source_sha256": digests, "source_snapshot_sha256": canonical_digest(digests)}
    try:
        repository = Path(__file__).resolve().parents[1]
        metadata["git_head"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repository, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        metadata["git_worktree_status"] = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=repository, text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
    except (OSError, subprocess.CalledProcessError):
        pass
    return metadata


def source_snapshot(root: Path, selected: list[Path]) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): digest(path.read_bytes()) for path in selected}


def relative_identity(identity: str, root: Path) -> str:
    path, separator, name = identity.partition("::")
    if not separator:
        raise RuntimeError(f"not a checked function identity: {identity}")
    return f"{Path(path).relative_to(root).as_posix()}::{name}"


def measure(root: Path, selected: list[Path], name: str, expected_misses: set[str],
            expected_functions: int, expected_edges: list[list[str]]) -> dict:
    sources = source_snapshot(root, selected)
    gc.collect()
    tracemalloc.start()
    started = time.perf_counter_ns()
    try:
        result = check_paths(selected, root=root, cache=True)
        elapsed = (time.perf_counter_ns() - started) / 1_000_000_000
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    if result.status != 0 or not result.verified:
        raise RuntimeError(f"{name} did not pass its strict gate: {json.dumps(result.to_dict())}")
    if source_snapshot(root, selected) != sources:
        raise RuntimeError(f"{name}: generated source changed during checking")
    per_file = {}
    observed_edges = []
    for file in result.results:
        relative = Path(file.path).relative_to(root).as_posix()
        file_edges = []
        for contract in file.contracts:
            caller = relative + "::" + contract.name
            for dependency in contract.dependencies:
                if "::" in dependency:
                    file_edges.append([caller, relative_identity(dependency, root)])
        observed_edges.extend(file_edges)
        per_file[relative] = {
            "cache_hit": file.cache_hit, "source_sha256": sources[relative],
            "fingerprint": file.fingerprint, "selected_functions": file.selected_functions,
            "checked_function_contracts": len(file.contracts),
            "direct_checked_function_call_edges": len(file_edges),
            "source_dependency_sha256": {
                Path(path).relative_to(root).as_posix(): value
                for path, value in sorted(file.dependencies.items())
            },
        }
    if set(per_file) != set(sources):
        raise RuntimeError(f"{name}: the selected file set changed")
    misses = {path for path, item in per_file.items() if not item["cache_hit"]}
    if misses != expected_misses:
        raise RuntimeError(f"{name}: expected misses {sorted(expected_misses)}, found {sorted(misses)}")
    coverage = result.to_dict()["coverage"]
    contracts = sum(item["checked_function_contracts"] for item in per_file.values())
    if coverage["selected_functions"] != expected_functions or contracts != expected_functions:
        raise RuntimeError(f"{name}: checked function coverage changed: {coverage}, contracts={contracts}")
    observed_edges.sort()
    if observed_edges != expected_edges:
        raise RuntimeError(f"{name}: published direct checked call graph changed")
    if any(not file.module_mode for file in result.results):
        raise RuntimeError(f"{name}: functional module coverage changed")
    return {
        "name": name, "elapsed_seconds": elapsed,
        "checker_elapsed_seconds": result.elapsed_seconds,
        "tracemalloc_current_bytes": current, "tracemalloc_peak_bytes": peak,
        "status": result.status, "verified": result.verified,
        "explicitly_selected_file_count": len(selected), "checked_file_count": len(per_file),
        "checked_function_count": contracts, "coverage": coverage,
        "checked_function_count_in_cache_miss_files": sum(
            per_file[path]["checked_function_contracts"] for path in misses
        ),
        "direct_checked_function_call_edge_count": len(observed_edges),
        "direct_call_graph_sha256": canonical_digest(observed_edges),
        "cache_hit_count": len(per_file) - len(misses), "cache_miss_count": len(misses),
        "cache_miss_files": sorted(misses), "per_file": per_file,
        "workload_source_snapshot_sha256": canonical_digest(sources),
    }


def summarize(runs: list[dict]) -> dict:
    summaries = {}
    for name in CHECK_NAMES:
        samples = [next(check for check in run["checks"] if check["name"] == name) for run in runs]
        elapsed = [sample["elapsed_seconds"] for sample in samples]
        peaks = [sample["tracemalloc_peak_bytes"] for sample in samples]
        summaries[name] = {
            "trials": len(samples), "elapsed_seconds_min": min(elapsed),
            "elapsed_seconds_median": statistics.median(elapsed), "elapsed_seconds_max": max(elapsed),
            "tracemalloc_peak_bytes_min": min(peaks),
            "tracemalloc_peak_bytes_median": statistics.median(peaks),
            "tracemalloc_peak_bytes_max": max(peaks),
            "cache_hit_count_each_trial": [sample["cache_hit_count"] for sample in samples],
            "cache_miss_count_each_trial": [sample["cache_miss_count"] for sample in samples],
        }
    return summaries


def run_benchmark(branches: int, depth: int, functions: int, repetitions: int) -> dict:
    before = implementation_metadata()
    script_sha256 = digest(Path(__file__).read_bytes())
    sources, edges = fixture_sources(branches, depth, functions)
    unrelated = "unrelated.py"
    leaf = "branch_0000_level_0000.py"
    unrelated_edit = sources[unrelated].replace("UNRELATED_OFFSET = 7", "UNRELATED_OFFSET = 8", 1)
    leaf_edit = sources[leaf].replace("return seed_0000(cents) + 0", "return seed_0000(cents) + 1", 1)
    if unrelated_edit == sources[unrelated] or leaf_edit == sources[leaf]:
        raise RuntimeError("generated edits failed to change their source")
    selected_functions = len(sources) * functions
    affected_leaf_files = {f"branch_0000_level_{level:04d}.py" for level in range(depth)}
    runs = []
    snapshots = {}
    with tempfile.TemporaryDirectory(prefix="pyalamode-m02-modules-") as temporary:
        root = Path(temporary).resolve()
        selected = [root / relative for relative in sorted(sources)]
        for trial in range(1, repetitions + 1):
            for relative, source in sources.items():
                (root / relative).write_text(source, encoding="utf-8")
            shutil.rmtree(root / ".pyalamode-cache", ignore_errors=True)
            snapshots["base"] = source_snapshot(root, selected)
            cold = measure(root, selected, CHECK_NAMES[0], set(sources), selected_functions, edges)
            warm = measure(root, selected, CHECK_NAMES[1], set(), selected_functions, edges)
            (root / unrelated).write_text(unrelated_edit, encoding="utf-8")
            snapshots["unrelated_edit"] = source_snapshot(root, selected)
            unrelated_result = measure(root, selected, CHECK_NAMES[2], {unrelated}, selected_functions, edges)
            # Retain the unrelated edit: its new evidence is already warm when
            # the branch leaf changes, so only that branch should miss.
            (root / leaf).write_text(leaf_edit, encoding="utf-8")
            snapshots["leaf_and_unrelated_edit"] = source_snapshot(root, selected)
            leaf_result = measure(root, selected, CHECK_NAMES[3], affected_leaf_files, selected_functions, edges)
            runs.append({"trial": trial, "checks": [cold, warm, unrelated_result, leaf_result]})
    after = implementation_metadata()
    if before["source_sha256"] != after["source_sha256"] or script_sha256 != digest(Path(__file__).read_bytes()):
        raise RuntimeError("implementation or benchmark source changed during the measured run; rerun after freezing source")
    cross_file_edges = sum(edge[0].split("::", 1)[0] != edge[1].split("::", 1)[0] for edge in edges)
    cross_module_import_edges = branches * depth
    return {
        "schema": 1, "benchmark": "m02_modules_check_cache_tracemalloc",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "invocation": {"executable": sys.executable, "argv": sys.argv,
                       "benchmark_script_sha256": script_sha256},
        "implementation": before, "implementation_source_snapshot_after": after["source_sha256"],
        "implementation_source_unchanged_during_run": True,
        "python": {"implementation": platform.python_implementation(), "version": platform.python_version(),
                   "full_version": sys.version, "build": list(platform.python_build()),
                   "compiler": platform.python_compiler(), "free_threaded": bool(sysconfig.get_config_var("Py_GIL_DISABLED"))},
        "os": {"platform": sys.platform, "description": platform.platform(),
               "release": platform.release(), "macos_version": platform.mac_ver()[0]},
        "hardware": hardware_metadata(),
        "workload": {
            "name": WORKLOAD_NAME, "branches": branches, "modules_per_branch": depth,
            "checked_functions_per_module": functions, "explicitly_selected_file_count": len(sources),
            "checked_file_count": len(sources), "checked_function_count": selected_functions,
            "source_bytes_before_edit": sum(len(source.encode()) for source in sources.values()),
            "source_lines_before_edit": sum(len(source.splitlines()) for source in sources.values()),
            "source_sha256_snapshots": snapshots,
            "direct_checked_function_call_edges": edges,
            "direct_checked_function_call_edge_count": len(edges),
            "cross_file_checked_function_call_edge_count": cross_file_edges,
            "direct_call_graph_sha256": canonical_digest(edges),
            "dependency_fanout": {
                "direct_source_import_edges": cross_module_import_edges,
                "max_distinct_checked_callees_per_function": min(functions, 2) if depth > 1 else 1,
                "max_checked_call_sites_per_function": 2 if depth > 1 else 1,
                "max_call_chain_edges": depth,
                "foundation_direct_importer_modules": branches,
                "foundation_transitive_importer_modules": branches * depth,
                "branch_leaf_transitive_importer_modules": depth - 1,
                "unrelated_transitive_importer_modules": 0,
            },
            "edits": {
                "unrelated_module_edit": {"file": unrelated, "change": "Change a stable integer offset from 7 to 8.",
                                          "expected_cache_miss_files": [unrelated]},
                "branch_leaf_edit": {"file": leaf, "change": "Add one to the first checked leaf function's scalar result.",
                                     "expected_cache_miss_files": sorted(affected_leaf_files)},
            },
        },
        "conditions": {
            "repetitions": repetitions, "cache": "enabled content-addressed disk analysis cache",
            "cold": "Remove the complete analysis-cache directory before each trial; checker imports are already loaded.",
            "warm": "Check unchanged sources immediately after the cold check.",
            "unrelated_edit": "Edit only unrelated.py immediately after the warm check; no other module imports it.",
            "leaf_edit": "Edit only branch 0's bottom module immediately after the unrelated edit check; retain the now-cached unrelated edit.",
            "timing": "perf_counter_ns wall time around check_paths, including tracemalloc overhead and disk cache I/O.",
            "memory": "tracemalloc current/peak Python allocations per check; result retained at sampling; not RSS or total process memory.",
            "cache_hit_meaning": "The public CheckResult.cache_hit flag; warm checks still read source, construct graph metadata and fingerprint inputs.",
            "checked_function_count_meaning": "Published checked function contracts, including evidence reused from cache; miss-file count is reported separately.",
            "call_edges": "Distinct direct checked function target edges from published FunctionContract.dependencies; repeated call sites share one edge.",
            "application_execution": "None: generated source is only written and statically checked, never imported or executed.",
            "excluded": ["interpreter startup", "checker imports", "fixture generation and edits", "source digest snapshots", "result validation", "JSON serialization", "application runtime"],
            "gc": "gc.collect before each interval; cyclic GC remains enabled",
            "filesystem_cache": "OS page cache uncontrolled; cold describes analysis-cache state only.",
            "working_directory": str(Path.cwd()), "temporary_filesystem_directory": tempfile.gettempdir(),
        },
        "summary": summarize(runs), "runs": runs,
        "interpretation": "Workload-specific traced checker measurements with asserted per-file cache reuse and unchanged direct call graph. Neither a universal latency target nor application runtime performance is established.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branches", type=int, default=8)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--functions-per-module", type=int, default=8)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--output", type=Path, help="write JSON here; otherwise print JSON")
    args = parser.parse_args()
    if min(args.branches, args.depth, args.functions_per_module, args.repetitions) < 1:
        parser.error("branches, depth, functions-per-module, and repetitions must be positive")
    evidence = run_benchmark(args.branches, args.depth, args.functions_per_module, args.repetitions)
    rendered = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output.resolve()}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
