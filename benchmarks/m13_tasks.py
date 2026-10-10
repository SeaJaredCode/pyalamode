"""Held task_wave_map_v1 controller; root correctness/measurement gates apply.

One fixed scalar workload, six rows and all eighteen intervals per platform.
No smoke mode, adjustable sample count, extra condition or speedup claim.
"""

import argparse
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import statistics
import sys
import sysconfig
import time
import tracemalloc

PROTOCOL = "task_wave_map_v1"
SIZES = (8, 64)
CONDITIONS = ("vector_map", "live2", "live4")
WARMUPS = 10
INTERVALS = 3
CALLS = 5
ROOT = Path(__file__).absolute().parents[1]
POLICY = '[tool.pyalamode]\nschema=1\ntasks=true\nboundary_guards="off"\n'


def fixture_source():
    return 'from pyalamode import Task, TaskCapability, Vector, effects, fun, task_map\n\n@fun\ndef transform(value: int) -> int:\n    return value * value + 1\n\n@fun\ndef baseline(values: Vector[int]) -> Vector[int]:\n    return values.map(transform)\n\n@effects(Task)\ndef characterized(tasks: TaskCapability, values: Vector[int]) -> Vector[int]:\n    return task_map(tasks, transform, values)\n'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()



def literal_oracles():
    return {size: {"input": tuple(range(size)), "output": tuple(value * value + 1 for value in range(size))} for size in SIZES}


def description():
    source = fixture_source()
    return {"protocol": PROTOCOL, "sizes": list(SIZES), "conditions": list(CONDITIONS),
            "rows_per_platform": 6, "intervals_per_platform": 18, "calls_per_interval": CALLS,
            "measured_calls_per_platform": 90, "warmups_per_platform": 60,
            "untimed_pre_row_correctness_calls_per_platform": 6, "untimed_retained_version_calls_per_platform": 3,
            "native_worker_launches_in_measured_calls_per_platform": 2160,
            "native_worker_launches_in_warmups_per_platform": 1440,
            "controller": {"path": str(Path(__file__).absolute()), "sha256": sha(__file__)},
            "fixture": {"source": source, "bytes": len(source.encode()),
                        "sha256": hashlib.sha256(source.encode()).hexdigest(), "policy": POLICY,
                        "policy_bytes": len(POLICY.encode()), "policy_sha256": hashlib.sha256(POLICY.encode()).hexdigest()},
            "oracles": {str(size): {name: list(values) for name, values in row.items()} for size, row in literal_oracles().items()},
            "scope": {"product_mode": "one canonical frozen SOURCE copy; installed correctness separate",
                      "guard_mode": "off", "retention": "common preexisting stable messages/callback/live provider; only last successful result, no intermediate history",
                      "included": "public mechanism call, full ingress/result/final validation, waves/staging/copy, native start/join/termination/cleanup, provider reset, previous-result disposal, loop/perf_counter/tracemalloc overhead",
                      "excluded": "release/setup/import/check/fixture/input/oracle/provider creation, warmups/assertions/hashes/evidence writes",
                      "tracing": "fresh tracing/reset and baseline outside timer; current/peak after timer; native stacks/OS memory/RSS unmeasured",
                      "system_load_controlled": False, "os_caches_controlled": False},
            "release_schema": {"schema": 1, "protocol": PROTOCOL, "m13_task_measurements_authorized": True,
                               "controller_sha256": "exact current controller hash", "fixture_sha256": "exact fixed fixture hash",
                               "policy_sha256": "exact fixed policy hash", "source_files": "absolute full source paths to exact SHA256",
                               "product_artifacts": "exact current26 foundations", "interpreter_bytes": "exact actual executable/base/core file hashes"}}


def repeat(function, arguments, count):
    answer = None
    for _ in range(count):
        answer = function(*arguments)
    return answer


def measure(release, directory):
    # No product/fixture import or check occurs before the closed release gate.
    sys.path.insert(0, str(ROOT))
    from pyalamode import Vector, live_tasks
    from pyalamode.model import foundation_identities
    from pyalamode.project import check_paths
    import pyalamode
    product_before = foundation_identities()
    if len(product_before) != 26 or product_before != release["product_artifacts"]:
        raise RuntimeError("released source product identities differ")
    package = Path(pyalamode.__file__).absolute().parent
    if package.resolve() != (ROOT / "pyalamode").resolve() or [Path(path).resolve() for path in pyalamode.__path__] != [package.resolve()]:
        raise RuntimeError("measurement refuses mixed source/installed product")
    for name in sorted(product_before):
        importlib.import_module("pyalamode" if name == "__init__.py" else "pyalamode." + name[:-3])
    provenance = environment(package, product_before)
    before = source_map(release)
    oracles = literal_oracles()
    directory.mkdir()
    fixture = directory / "fixture"
    fixture.mkdir()
    source = fixture / "task_core.py"
    source.write_text(fixture_source(), encoding="utf-8")
    policy_path = fixture / "pyproject.toml"
    policy_path.write_text(POLICY, encoding="utf-8")
    result = {"protocol": PROTOCOL, "status": "running", "release": release, "description": description(),
              "environment_before": provenance, "source_before": before, "product_before": product_before,
              "fixture_sha256": sha(source), "fixture_policy_before_sha256": sha(policy_path), "measurements": [],
              "untimed_invocations": {"pre_row_correctness": [], "retained_version": []}}
    partial = directory / "partial.json"
    def persist():
        partial.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    persist()
    try:
        if source.read_bytes() != fixture_source().encode() or policy_path.read_bytes() != POLICY.encode():
            raise RuntimeError("fixed generated fixture/policy bytes differ")
        checked = check_paths([source], root=fixture)
        check_bytes = (json.dumps(checked.to_dict(), indent=2, sort_keys=True) + "\n").encode()
        (directory / "fixture-check.json").write_bytes(check_bytes)
        result["untimed_check"] = {"status": checked.status, "path": str(directory / "fixture-check.json"),
                                  "bytes": len(check_bytes), "sha256": hashlib.sha256(check_bytes).hexdigest()}
        persist()
        if checked.status:
            raise RuntimeError("fixed tasks=true/guards=off fixture failed strict checking")
        spec = importlib.util.spec_from_file_location("m13_task_core", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        prepared = {size: Vector.of(*row["input"]) for size, row in oracles.items()}
        retained_input = Vector.of(7)
        retained = []
        for condition in CONDITIONS:
            provider = None if condition == "vector_map" else live_tasks(2 if condition == "live2" else 4, max_tasks=64)
            function = module.baseline if provider is None else module.characterized
            arguments = (retained_input,) if provider is None else (provider, retained_input)
            record = {"condition": condition, "calls": 1, "status": "invoking"}
            result["untimed_invocations"]["retained_version"].append(record)
            persist()
            completed = function(*arguments)
            later = completed.appended(9)
            verify(retained_input, (7,), Vector); verify(completed, (50,), Vector); verify(later, (50, 9), Vector)
            retained.append((completed, later))
            record["status"] = "verified"
            persist()
        for size in SIZES:
            values, oracle = prepared[size], oracles[size]
            verify(values, oracle["input"], Vector)
            for condition in CONDITIONS:
                provider = None if condition == "vector_map" else live_tasks(2 if condition == "live2" else 4, max_tasks=64)
                function = module.baseline if provider is None else module.characterized
                arguments = (values,) if provider is None else (provider, values)
                record = {"size": size, "condition": condition, "calls": 1, "status": "invoking"}
                result["untimed_invocations"]["pre_row_correctness"].append(record)
                persist()
                verify(function(*arguments), oracle["output"], Vector)
                record["status"] = "verified"
                verify(repeat(function, arguments, WARMUPS), oracle["output"], Vector)
                row = {"size": size, "condition": condition, "warmups": WARMUPS, "observations": []}
                result["measurements"].append(row)
                for sample in range(INTERVALS):
                    answer = None
                    tracemalloc.start(); tracemalloc.reset_peak()
                    baseline = tracemalloc.get_traced_memory()[0]
                    started = time.perf_counter()
                    answer = repeat(function, arguments, CALLS)
                    elapsed = time.perf_counter() - started
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    row["observations"].append({"sample": sample + 1, "calls": CALLS, "elapsed_seconds": elapsed,
                                               "traced_baseline_bytes": baseline, "traced_current_bytes": current,
                                               "traced_peak_bytes": peak, "traced_current_delta_bytes": current - baseline,
                                               "traced_peak_delta_bytes": peak - baseline})
                    persist()
                    verify(answer, oracle["output"], Vector); verify(values, oracle["input"], Vector)
                row["median_seconds_per_call"] = statistics.median(item["elapsed_seconds"] for item in row["observations"]) / CALLS
                row["median_traced_current_delta_bytes"] = statistics.median(item["traced_current_delta_bytes"] for item in row["observations"])
                row["median_traced_peak_delta_bytes"] = statistics.median(item["traced_peak_delta_bytes"] for item in row["observations"])
                row["correctness_passed"] = True
                persist()
        verify(retained_input, (7,), Vector)
        for completed, later in retained:
            verify(completed, (50,), Vector); verify(later, (50, 9), Vector)
        result["counts"] = {"rows": len(result["measurements"]),
                            "intervals": sum(len(row["observations"]) for row in result["measurements"]),
                            "measured_calls": sum(item["calls"] for row in result["measurements"] for item in row["observations"]),
                            "warmups": sum(row["warmups"] for row in result["measurements"]),
                            "untimed_pre_row_correctness_calls": sum(row["calls"] for row in result["untimed_invocations"]["pre_row_correctness"]),
                            "untimed_retained_version_calls": sum(row["calls"] for row in result["untimed_invocations"]["retained_version"])}
        if result["counts"] != {"rows": 6, "intervals": 18, "measured_calls": 90, "warmups": 60,
                                "untimed_pre_row_correctness_calls": 6, "untimed_retained_version_calls": 3}:
            raise AssertionError("actual counts differ from fixed task_wave_map_v1")
        result["status"] = "completed"
    except BaseException as error:
        result["status"] = "failed"
        result["failure"] = {"category": type(error).__name__, "reason": str(error)}
        raise
    finally:
        if tracemalloc.is_tracing():
            tracemalloc.stop()
        def observe(name, operation):
            try:
                result[name] = operation()
            except BaseException as error:
                result[name] = {"observation_failed": {"category": type(error).__name__, "reason": str(error)}}
        observe("source_after", lambda: source_map(release))
        observe("product_after", foundation_identities)
        observe("environment_after", lambda: environment(package, product_before))
        observe("fixture_after_sha256", lambda: sha(source))
        observe("fixture_policy_after_sha256", lambda: sha(policy_path))
        observe("fixture_source_bytes_equal", lambda: source.read_bytes() == fixture_source().encode())
        observe("fixture_policy_bytes_equal", lambda: policy_path.read_bytes() == POLICY.encode())
        result["frozen_inputs_equal"] = (result["source_after"] == before and result["product_after"] == product_before
                                         and result["environment_after"] == provenance
                                         and result["fixture_after_sha256"] == release["fixture_sha256"]
                                         and result["fixture_policy_after_sha256"] == release["policy_sha256"]
                                         and result["fixture_policy_before_sha256"] == release["policy_sha256"]
                                         and result["fixture_source_bytes_equal"] is True and result["fixture_policy_bytes_equal"] is True)
        if not result["frozen_inputs_equal"]:
            result["status"] = "failed: frozen source/product/core/fixture changed"
        persist()
    if not result["frozen_inputs_equal"]:
        raise RuntimeError("frozen source/product/core/fixture changed")
    return result

def target_gate():
    if sys.implementation.name != "cpython" or tuple(sys.version_info[:3]) != (3, 13, 1):
        raise RuntimeError("measurement requires exact CPython 3.13.1")
    if (sys.platform, platform.machine()) not in {("darwin", "arm64"), ("linux", "aarch64")}:
        raise RuntimeError("measurement requires macOS arm64 or Linux aarch64")
    if not sys._is_gil_enabled() or sys.getfilesystemencoding() != "utf-8" or sys.getfilesystemencodeerrors() != "surrogateescape":
        raise RuntimeError("measurement requires standard GIL and UTF8/surrogateescape")


def source_map(release):
    return {path: sha(path) for path in release["source_files"]}


def release_gate(path):
    release = json.loads(path.read_text())
    keys = {"schema", "protocol", "m13_task_measurements_authorized", "controller_sha256",
            "fixture_sha256", "policy_sha256", "source_files", "product_artifacts", "interpreter_bytes"}
    if type(release) is not dict or set(release) != keys or type(release["schema"]) is not int or release["schema"] != 1:
        raise RuntimeError("measurement requires the closed root release schema1")
    if release["protocol"] != PROTOCOL or release["m13_task_measurements_authorized"] is not True:
        raise RuntimeError("root has not released task_wave_map_v1 measurements")
    if release["controller_sha256"] != sha(__file__) or release["fixture_sha256"] != hashlib.sha256(fixture_source().encode()).hexdigest():
        raise RuntimeError("released controller/fixture differs from current bytes")
    if type(release["source_files"]) is not dict or not release["source_files"] or any(not Path(path).is_absolute() for path in release["source_files"]):
        raise RuntimeError("canonical frozen SOURCE measurement requires an absolute full root source map")
    if source_map(release) != release["source_files"]:
        raise RuntimeError("released source bytes changed")
    if release["policy_sha256"] != hashlib.sha256(POLICY.encode()).hexdigest():
        raise RuntimeError("released fixed policy differs")
    target_gate()
    if type(release["product_artifacts"]) is not dict or len(release["product_artifacts"]) != 26:
        raise RuntimeError("measurement requires exact26 foundation release")
    package = ROOT / "pyalamode"
    physical = {path.name: sha(path) for path in package.glob("*.py")}
    if len(physical) != 27 or set(physical) != set(release["product_artifacts"]) | {"__main__.py"}:
        raise RuntimeError("measurement requires exact27 physical product files")
    if {name: physical[name] for name in release["product_artifacts"]} != release["product_artifacts"]:
        raise RuntimeError("released physical product bytes changed")
    if any(release["source_files"].get(str((package / name).absolute())) != value for name, value in physical.items()):
        raise RuntimeError("full source release must include every exact product file")
    core = python_core()
    native = {str(Path(sys.executable).absolute()), str(Path(sys._base_executable).absolute()), core["path"]}
    if type(release["interpreter_bytes"]) is not dict or {path: sha(path) for path in sorted(native)} != release["interpreter_bytes"]:
        raise RuntimeError("released actual interpreter/core bytes changed")
    return release


def python_core():
    library = sysconfig.get_config_var("LDLIBRARY")
    library_directory = sysconfig.get_config_var("LIBDIR")
    framework_prefix = sysconfig.get_config_var("PYTHONFRAMEWORKPREFIX")
    if type(library) is not str or not library:
        raise RuntimeError("canonical frozen SOURCE measurement requires an actual Python core library identity")
    candidates = []
    if type(library_directory) is str and library_directory:
        candidates.append(("LIBDIR/LDLIBRARY", Path(library_directory) / library))
    if sys.platform == "darwin" and type(framework_prefix) is str and framework_prefix:
        candidates.append(("PYTHONFRAMEWORKPREFIX/LDLIBRARY", Path(framework_prefix) / library))
    for method, path in candidates:
        if path.is_file():
            return {"path": str(path.absolute()), "resolved_path": str(path.resolve()), "bytes": path.stat().st_size, "sha256": sha(path),
                    "resolution": method, "LIBDIR": library_directory, "LDLIBRARY": library,
                    "PYTHONFRAMEWORKPREFIX": framework_prefix,
                    "candidate_paths": [str(candidate.absolute()) for _, candidate in candidates]}
    raise RuntimeError("canonical frozen SOURCE measurement requires one existing Python core file on the supported target")


def product_sources(package, products):
    expected = {"pyalamode" if name == "__init__.py" else "pyalamode." + name[:-3]: (package / name).resolve()
                for name in products}
    actual = {}
    for name, module in tuple(sys.modules.items()):
        if name == "pyalamode" or name.startswith("pyalamode."):
            path = getattr(module, "__file__", None)
            if name not in expected or type(path) is not str or Path(path).resolve() != expected[name]:
                raise RuntimeError("canonical frozen SOURCE measurement refuses mixed installed/checkout product modules")
            actual[name] = {"path": str(Path(path).absolute()), "resolved_path": str(Path(path).resolve()), "sha256": sha(path)}
    if set(actual) != set(expected):
        raise RuntimeError("canonical frozen SOURCE measurement requires the complete exact26 loaded product inventory")
    return actual


def environment(package, products):
    native_paths = {str(Path(sys.executable).absolute()), str(Path(sys._base_executable).absolute())}
    core = python_core()
    native_paths.add(core["path"])
    package_bytes = {path.name: sha(path) for path in sorted(package.glob("*.py"))}
    if set(package_bytes) != set(products) | {"__main__.py"}:
        raise RuntimeError("canonical frozen SOURCE measurement requires exact27 physical package files")
    return {"executable_literal": sys.executable, "executable_resolved_observation_only": str(Path(sys.executable).resolve()),
            "base_executable": sys._base_executable, "interpreter_bytes": {path: sha(path) for path in sorted(native_paths)},
            "interpreter_byte_counts": {path: Path(path).stat().st_size for path in sorted(native_paths)},
            "python_core": core,
            "prefix": sys.prefix, "base_prefix": sys.base_prefix, "implementation": sys.implementation.name,
            "version": sys.version, "cache_tag": sys.implementation.cache_tag, "abiflags": sys.abiflags,
            "gil_enabled": sys._is_gil_enabled(), "sys_flags": repr(sys.flags), "platform": platform.platform(),
            "machine": platform.machine(), "python_build": platform.python_build(), "python_compiler": platform.python_compiler(),
            "processor": platform.processor(), "logical_cpus": os.cpu_count(), "filesystem_encoding": sys.getfilesystemencoding(),
            "filesystem_errors": sys.getfilesystemencodeerrors(), "utf8_mode": sys.flags.utf8_mode,
            "hash_seed_environment": os.environ.get("PYTHONHASHSEED"), "import_package": str(package), "sys_path": list(sys.path),
            "product_mode": "one canonical frozen SOURCE copy; installed correctness separate",
            "loaded_product_sources": product_sources(package, products), "full_package_bytes": package_bytes,
            "system_load_controlled": False, "os_caches_controlled": False}


def verify(value, expected, vector_class):
    if type(value) is not vector_class:
        raise AssertionError("expected exact Vector result")
    items = object.__getattribute__(value, "_items")
    if type(items) is not tuple or len(items) != len(expected) or any(type(item) is not int for item in items):
        raise AssertionError("expected complete exact integer result schema")
    if items != expected:
        raise AssertionError("result differs from independent literal oracle")


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--describe", action="store_true")
    action.add_argument("--measure", action="store_true")
    parser.add_argument("--release", type=Path)
    parser.add_argument("--work-directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.describe:
        result = description()
    else:
        if args.release is None or args.work_directory is None or args.output is None:
            parser.error("--measure requires --release, --work-directory and --output")
        release = release_gate(args.release)
        result = measure(release, args.work_directory)
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(raw, end="")
    else:
        with args.output.open("x", encoding="utf-8") as output:
            output.write(raw)


if __name__ == "__main__":
    main()
