"""Named M1 check/cache measurements on a disposable, generated scalar project.

Run from an installed checkout with:
    python benchmarks/m01_scalar.py --output /tmp/pyalamode-m01-scalar.json

Elapsed times include tracemalloc overhead; imports and fixture generation are
outside the measured intervals. This does not measure application runtime.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import platform
import shutil
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


def fixture_source(functions: int) -> str:
    chunks = ['"""Generated M1 scalar workload; never executed by this benchmark."""\n',
              "from pyalamode import fun\n\n"]
    for index in range(functions):
        chunks.append(
            f"@fun\ndef discounted_total_{index:04d}(cents: int, discount_cents: int) -> int:\n"
            "    remainder = cents - discount_cents\n"
            "    if remainder < 0:\n"
            "        result = 0\n"
            "    else:\n"
            "        result = max(0, remainder)\n"
            "    return result\n\n"
        )
    for index in range(functions):
        chunks.append(f"total_{index:04d} = discounted_total_{index:04d}(1500, 200)\n")
    return "".join(chunks)


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
    return hardware


def implementation_metadata() -> dict:
    package = Path(pyalamode.__file__).resolve().parent
    digests = {}
    for name in ("__init__.py", "checker.py", "cli.py", "model.py", "project.py"):
        source = package / name
        if source.exists():
            digests[name] = hashlib.sha256(source.read_bytes()).hexdigest()
    return {"package_version": pyalamode.__version__, "checker": CHECKER_VERSION,
            "edition": EDITION, "operation_contract": OPERATION_VERSION,
            "target": TARGET, "package_directory": str(package), "source_sha256": digests}


def measure(root: Path, selected: list[Path], name: str, expected_misses: set[str],
            expected_functions: int) -> dict:
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
    per_file = {Path(file.path).relative_to(root).as_posix(): file.cache_hit
                for file in result.results}
    if set(per_file) != {path.relative_to(root).as_posix() for path in selected}:
        raise RuntimeError(f"{name}: the selected file set changed")
    misses = {path for path, hit in per_file.items() if not hit}
    if misses != expected_misses:
        raise RuntimeError(f"{name}: expected misses {sorted(expected_misses)}, found {sorted(misses)}")
    coverage = result.to_dict()["coverage"]
    if coverage["selected_functions"] != expected_functions or coverage["analyzed_call_sites"] != expected_functions:
        raise RuntimeError(f"{name}: generated workload coverage changed: {coverage}")
    return {"name": name, "elapsed_seconds": elapsed,
            "checker_elapsed_seconds": result.elapsed_seconds,
            "tracemalloc_current_bytes": current, "tracemalloc_peak_bytes": peak,
            "status": result.status, "verified": result.verified, "coverage": coverage,
            "cache_hit_count": sum(per_file.values()), "cache_miss_count": len(misses),
            "per_file_cache_hits": per_file}


def run_benchmark(files: int, functions: int, repetitions: int) -> dict:
    source = fixture_source(functions)
    edited = source.replace("remainder = cents - discount_cents\n",
                            "remainder = cents - discount_cents + 1\n", 1)
    with tempfile.TemporaryDirectory(prefix="pyalamode-m01-scalar-") as temporary:
        root = Path(temporary).resolve()
        selected = [root / f"scalar_{index:04d}.py" for index in range(files)]
        for path in selected:
            path.write_text(source, encoding="utf-8")
        names = {path.name for path in selected}
        runs = []
        for trial in range(1, repetitions + 1):
            selected[0].write_text(source, encoding="utf-8")
            shutil.rmtree(root / ".pyalamode-cache", ignore_errors=True)
            cold = measure(root, selected, "cold_check", names, files * functions)
            warm = measure(root, selected, "warm_unchanged_check", set(), files * functions)
            selected[0].write_text(edited, encoding="utf-8")
            incremental = measure(root, selected, "single_source_edit_check", {selected[0].name},
                                  files * functions)
            runs.append({"trial": trial, "checks": [cold, warm, incremental]})
    summaries = {}
    for index, name in enumerate(("cold_check", "warm_unchanged_check", "single_source_edit_check")):
        samples = [run["checks"][index] for run in runs]
        elapsed = sorted(sample["elapsed_seconds"] for sample in samples)
        middle = len(elapsed) // 2
        median = elapsed[middle] if len(elapsed) % 2 else (elapsed[middle - 1] + elapsed[middle]) / 2
        summaries[name] = {"elapsed_seconds_min": min(elapsed), "elapsed_seconds_median": median,
                           "elapsed_seconds_max": max(elapsed),
                           "tracemalloc_peak_bytes_min": min(s["tracemalloc_peak_bytes"] for s in samples),
                           "tracemalloc_peak_bytes_max": max(s["tracemalloc_peak_bytes"] for s in samples)}
    return {
        "schema": 1, "benchmark": "m01_scalar_check_cache_tracemalloc",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "invocation": {"executable": sys.executable, "argv": sys.argv,
                       "benchmark_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "implementation": implementation_metadata(),
        "python": {"implementation": platform.python_implementation(), "version": platform.python_version(),
                   "full_version": sys.version, "build": list(platform.python_build()),
                   "compiler": platform.python_compiler(), "free_threaded": bool(sysconfig.get_config_var("Py_GIL_DISABLED"))},
        "os": {"platform": sys.platform, "description": platform.platform(),
               "release": platform.release(), "macos_version": platform.mac_ver()[0]},
        "hardware": hardware_metadata(),
        "workload": {"files": files, "selected_functions_per_file": functions,
                     "selected_functions": files * functions, "ordinary_same_file_call_sites": files * functions,
                     "source_bytes_before_edit": len(source.encode("utf-8")) * files,
                     "source_lines_before_edit": len(source.splitlines()) * files,
                     "unchanged_file_source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                     "changed_file_source_sha256": hashlib.sha256(edited.encode("utf-8")).hexdigest(),
                     "changed_file": "scalar_0000.py", "changed_files_per_incremental_check": 1,
                     "edit": "Add exact integer literal + 1 to the first function's scalar subtraction.",
                     "dependency_fanout": {"checked_cross_file_edges": 0, "checked_function_call_edges": 0,
                                           "ordinary_same_file_calls_per_export": 1,
                                           "approved_max_calls_per_function": 1,
                                           "shared_foundation": ["pyalamode.fun", "CPython scalar operations and max"]}},
        "conditions": {"repetitions": repetitions, "cache": "enabled content-addressed disk cache",
                       "cold": "Cache directory removed before each trial; same process with checker imports already loaded.",
                       "warm": "All selected source files unchanged immediately after cold_check.",
                       "incremental": "One source file edited immediately after warm_unchanged_check; shared dependencies unchanged.",
                       "timing": "perf_counter_ns wall time around check_paths; includes tracemalloc overhead and disk cache reads/writes.",
                       "memory": "tracemalloc current/peak Python allocations per check; result retained at sampling; not process RSS.",
                       "excluded": ["interpreter startup", "imports", "fixture generation", "JSON serialization", "application execution"],
                       "gc": "gc.collect before each interval; cyclic GC remains enabled",
                       "filesystem_cache": "OS page cache is uncontrolled; cold denotes analysis cache state only",
                       "working_directory": str(Path.cwd()),
                       "temporary_filesystem_directory": tempfile.gettempdir()},
        "summary": summaries, "runs": runs,
        "interpretation": "Workload-specific traced check measurements. Warm checks still read and fingerprint every source file. M1 has no checked cross-file call graph; this edit measures per-file source invalidation, not transitive dependency invalidation. No universal performance claim.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", type=int, default=32)
    parser.add_argument("--functions-per-file", type=int, default=8)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--output", type=Path, help="write JSON here; otherwise print JSON")
    args = parser.parse_args()
    if min(args.files, args.functions_per_file, args.repetitions) < 1:
        parser.error("files, functions-per-file, and repetitions must be positive")
    result = run_benchmark(args.files, args.functions_per_file, args.repetitions)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output.resolve()}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
