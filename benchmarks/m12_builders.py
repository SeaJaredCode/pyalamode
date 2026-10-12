"""Held bulk_vector_assembly_v1 controller; root measurement release is required.

Describe performs only standard-library source/oracle preparation. Measure uses
one canonical frozen SOURCE product, checks/imports one fixed fixture, then
performs exactly four rows. Fresh installed correctness is a separate gate.
There is no smoke mode, adjustable sample count or additional cost condition.
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

PROTOCOL = "bulk_vector_assembly_v1"
SIZES = (64, 4096)
CHUNKS = 64
CONDITIONS = ("builder_extend64", "persistent_concat64")
WARMUPS = 10
INTERVALS = 3
CALLS = 25
POLICY = '[tool.pyalamode]\nschema=1\nbuilders=true\nboundary_guards="off"\n'
ROOT = Path(__file__).absolute().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fixture_source():
    statements = "\n".join("        builder.extend(chunks[" + str(index) + "])" for index in range(CHUNKS))
    expression = "Vector[int].of()" + "".join(".concat(chunks[" + str(index) + "])" for index in range(CHUNKS)) + ".appended(-1)"
    return ("# mode: fun\nfrom pyalamode import Vector, VectorBuilder, vector_build\n\n"
            "def builder_assembly(chunks: Vector[Vector[int]]) -> Vector[int]:\n"
            "    def populate(builder: VectorBuilder[int]) -> None:\n" + statements + "\n"
            "        builder.append(-1)\n        return None\n    return vector_build(populate)\n\n"
            "def persistent_assembly(chunks: Vector[Vector[int]]) -> Vector[int]:\n"
            "    return " + expression + "\n")


def literal_oracles():
    # Independent plain tuple construction precedes all candidate execution.
    return {size: {"output": tuple(range(size)) + (-1,),
                   "chunks": tuple(tuple(range(index * (size // CHUNKS), (index + 1) * (size // CHUNKS)))
                                   for index in range(CHUNKS))} for size in SIZES}


def description():
    source = fixture_source()
    return {"protocol": PROTOCOL, "sizes": list(SIZES), "chunk_count": CHUNKS,
            "conditions": list(CONDITIONS), "rows_per_platform": 4, "intervals_per_platform": 12,
            "calls_per_interval": CALLS, "measured_calls_per_platform": 300, "warmups_per_platform": 40,
            "untimed_pre_row_correctness_calls_per_platform": 4, "untimed_retained_version_builder_calls_per_platform": 1,
            "controller": {"path": str(Path(__file__).absolute()), "sha256": sha(__file__)},
            "fixture": {"source": source, "bytes": len(source.encode()),
                        "sha256": hashlib.sha256(source.encode()).hexdigest(), "policy": POLICY,
                        "policy_bytes": len(POLICY.encode()), "policy_sha256": hashlib.sha256(POLICY.encode()).hexdigest()},
            "oracles": {str(size): {"output": list(row["output"]), "chunks": [list(chunk) for chunk in row["chunks"]]}
                        for size, row in literal_oracles().items()},
            "scope": {"product_mode": "one canonical frozen SOURCE copy; no mixed installed/checkout modules; installed correctness separate",
                      "guard_mode": "off", "retention": "stable source chunks throughout; no intermediate history; last complete result only",
                      "included": "lexical callback construction, token/list allocation, native/product indexing/validation/staging/copy/finalization/cleanup, result disposal, loop/perf_counter/tracemalloc overhead",
                      "excluded": "release/setup/import/fixture/check/input/oracle creation, warmups, assertions, hashes and evidence writes",
                      "tracing": "fresh tracing/reset and baseline before each timer; current/peak after timer; preexisting source chunks untraced; Python allocation, not RSS/native total",
                      "system_load_controlled": False, "os_caches_controlled": False},
            "release_schema": {"schema": 1, "protocol": PROTOCOL, "m12_builder_measurements_authorized": True,
                               "controller_sha256": "exact current controller hash", "fixture_sha256": "exact description fixture hash",
                               "source_files": "absolute file path -> exact SHA256 map", "product_artifacts": "exact current24 product map"}}


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
    keys = {"schema", "protocol", "m12_builder_measurements_authorized", "controller_sha256",
            "fixture_sha256", "source_files", "product_artifacts"}
    if type(release) is not dict or set(release) != keys or type(release["schema"]) is not int or release["schema"] != 1:
        raise RuntimeError("measurement requires the closed root release schema1")
    if release["protocol"] != PROTOCOL or release["m12_builder_measurements_authorized"] is not True:
        raise RuntimeError("root has not released bulk_vector_assembly_v1 measurements")
    if release["controller_sha256"] != sha(__file__) or release["fixture_sha256"] != hashlib.sha256(fixture_source().encode()).hexdigest():
        raise RuntimeError("released controller/fixture differs from current bytes")
    if type(release["source_files"]) is not dict or not release["source_files"] or any(not Path(path).is_absolute() for path in release["source_files"]):
        raise RuntimeError("canonical frozen SOURCE measurement requires an absolute full root source map")
    if source_map(release) != release["source_files"]:
        raise RuntimeError("released source bytes changed")
    target_gate()
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
        raise RuntimeError("canonical frozen SOURCE measurement requires the complete exact24 loaded product inventory")
    return actual


def environment(package, products):
    native_paths = {str(Path(sys.executable).absolute()), str(Path(sys._base_executable).absolute())}
    core = python_core()
    native_paths.add(core["path"])
    package_bytes = {path.name: sha(path) for path in sorted(package.glob("*.py"))}
    if set(package_bytes) != set(products) | {"__main__.py"}:
        raise RuntimeError("canonical frozen SOURCE measurement requires exact25 physical package files")
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


def verify_chunks(chunks, expected, vector_class):
    if type(chunks) is not vector_class:
        raise AssertionError("expected exact outer chunk Vector")
    values = object.__getattribute__(chunks, "_items")
    if type(values) is not tuple or len(values) != CHUNKS:
        raise AssertionError("expected exactly64 stable chunks")
    for value, literal in zip(values, expected):
        verify(value, literal, vector_class)


def repeat(function, chunks, count):
    answer = None
    for _ in range(count):
        answer = function(chunks)
    return answer


def measure(release, directory):
    # Root gate precedes all product/application imports and candidate checks.
    sys.path.insert(0, str(ROOT))
    from pyalamode import Vector, vector_build
    from pyalamode.model import foundation_identities
    from pyalamode.project import check_paths
    import pyalamode
    product_before = foundation_identities()
    if len(product_before) != 24 or product_before != release["product_artifacts"]:
        raise RuntimeError("released canonical frozen SOURCE product identities differ")
    package = Path(pyalamode.__file__).absolute().parent
    if package.resolve() != (ROOT / "pyalamode").resolve() or [Path(path).resolve() for path in pyalamode.__path__] != [package.resolve()]:
        raise RuntimeError("measurement requires one canonical frozen SOURCE product at ROOT/pyalamode")
    # Load the finite trusted foundation before the before-map, so later lazy
    # checker imports cannot create a different otherwise valid module inventory.
    # __main__.py is a launch entry and is only hashed, never imported here.
    for name in sorted(product_before):
        importlib.import_module("pyalamode" if name == "__init__.py" else "pyalamode." + name[:-3])
    provenance = environment(package, product_before)
    before = source_map(release)
    oracles = literal_oracles()
    directory.mkdir()
    fixture = directory / "fixture"
    fixture.mkdir()
    source = fixture / "bulk_core.py"
    source.write_text(fixture_source(), encoding="utf-8")
    policy_path = fixture / "pyproject.toml"
    policy_path.write_text(POLICY, encoding="utf-8")
    policy_expected = POLICY.encode()
    if policy_path.read_bytes() != policy_expected or source.read_bytes() != fixture_source().encode():
        raise RuntimeError("generated fixture source/policy differ from fixed frozen bytes")
    result = {"protocol": PROTOCOL, "status": "running", "release": release, "environment": provenance,
              "environment_before": provenance,
              "description": description(), "source_before": before, "product_before": product_before,
              "fixture_sha256": sha(source), "fixture_policy_before_sha256": sha(policy_path), "measurements": [],
              "untimed_invocations": {"pre_row_correctness": [], "retained_version_builder": []}}
    partial = directory / "partial.json"
    def persist():
        partial.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    persist()
    try:
        checked = check_paths([source], root=fixture)
        check_bytes = (json.dumps(checked.to_dict(), indent=2, sort_keys=True) + "\n").encode()
        (directory / "fixture-check.json").write_bytes(check_bytes)
        result["untimed_check"] = {"status": checked.status, "path": str(directory / "fixture-check.json"),
                                  "bytes": len(check_bytes), "sha256": hashlib.sha256(check_bytes).hexdigest()}
        persist()
        if checked.status:
            raise RuntimeError("fixed builders=true/guards=off fixture failed strict checking")
        spec = importlib.util.spec_from_file_location("m12_bulk_core", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        prepared = {size: Vector.of(*(Vector.of(*chunk) for chunk in row["chunks"])) for size, row in oracles.items()}
        functions = {"builder_extend64": module.builder_assembly, "persistent_concat64": module.persistent_assembly}
        retained_source = Vector.of(100)
        result["untimed_invocations"]["retained_version_builder"].append({"calls": 1, "status": "invoking"})
        persist()
        retained_completed = vector_build(lambda builder: builder.extend(retained_source))
        later = retained_completed.appended(101)
        for value, literal in ((retained_source, (100,)), (retained_completed, (100,)), (later, (100, 101))):
            verify(value, literal, Vector)
        result["untimed_invocations"]["retained_version_builder"][0]["status"] = "verified"
        persist()
        for size in SIZES:
            chunks, oracle = prepared[size], oracles[size]
            verify_chunks(chunks, oracle["chunks"], Vector)
            for condition in CONDITIONS:
                function = functions[condition]
                pre_row = {"size": size, "condition": condition, "calls": 1, "status": "invoking"}
                result["untimed_invocations"]["pre_row_correctness"].append(pre_row)
                persist()
                verify(function(chunks), oracle["output"], Vector)
                pre_row["status"] = "verified"
                verify(repeat(function, chunks, WARMUPS), oracle["output"], Vector)
                row = {"condition": condition, "size": size, "chunks": CHUNKS, "elements_per_chunk": size // CHUNKS,
                       "result_items": size + 1, "warmups": WARMUPS, "observations": []}
                result["measurements"].append(row)
                for sample in range(INTERVALS):
                    answer = None
                    tracemalloc.start()
                    tracemalloc.reset_peak()
                    baseline = tracemalloc.get_traced_memory()[0]
                    started = time.perf_counter()
                    answer = repeat(function, chunks, CALLS)
                    elapsed = time.perf_counter() - started
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    # Persist the actual interval before oracle checks.
                    row["observations"].append({"sample": sample + 1, "calls": CALLS, "elapsed_seconds": elapsed,
                                               "traced_baseline_bytes": baseline, "traced_current_bytes": current,
                                               "traced_peak_bytes": peak, "traced_current_delta_bytes": current - baseline,
                                               "traced_peak_delta_bytes": peak - baseline})
                    persist()
                    verify(answer, oracle["output"], Vector)
                    verify_chunks(chunks, oracle["chunks"], Vector)
                row["median_seconds_per_call"] = statistics.median(item["elapsed_seconds"] for item in row["observations"]) / CALLS
                row["median_traced_peak_delta_bytes"] = statistics.median(item["traced_peak_delta_bytes"] for item in row["observations"])
                row["correctness_passed"] = True
                persist()
        for value, literal in ((retained_source, (100,)), (retained_completed, (100,)), (later, (100, 101))):
            verify(value, literal, Vector)
        result["counts"] = {"rows": len(result["measurements"]),
                            "intervals": sum(len(row["observations"]) for row in result["measurements"]),
                            "measured_calls": sum(item["calls"] for row in result["measurements"] for item in row["observations"]),
                            "warmups": sum(row["warmups"] for row in result["measurements"]),
                            "untimed_pre_row_correctness_calls": sum(row["calls"] for row in result["untimed_invocations"]["pre_row_correctness"]),
                            "untimed_retained_version_builder_calls": sum(row["calls"] for row in result["untimed_invocations"]["retained_version_builder"])}
        if result["counts"] != {"rows": 4, "intervals": 12, "measured_calls": 300, "warmups": 40,
                                "untimed_pre_row_correctness_calls": 4, "untimed_retained_version_builder_calls": 1}:
            raise AssertionError("actual interval counts differ from fixed protocol")
        result["status"] = "completed"
    except BaseException as error:
        result["status"] = "failed"
        result["failure"] = {"category": type(error).__name__, "reason": str(error)}
        raise
    finally:
        if tracemalloc.is_tracing():
            tracemalloc.stop()
        def observe_after(name, operation):
            # Preserve every after observation even if a frozen file disappeared
            # or one provenance read refuses; any read failure forbids acceptance.
            try:
                result[name] = operation()
            except BaseException as error:
                result[name] = {"observation_failed": {"category": type(error).__name__, "reason": str(error)}}
        observe_after("source_after", lambda: source_map(release))
        observe_after("product_after", foundation_identities)
        observe_after("environment_after", lambda: environment(package, product_before))
        observe_after("fixture_after_sha256", lambda: sha(source))
        observe_after("fixture_policy_after_sha256", lambda: sha(policy_path))
        observe_after("fixture_policy_bytes_equal", lambda: policy_path.read_bytes() == policy_expected)
        observe_after("fixture_source_bytes_equal", lambda: source.read_bytes() == fixture_source().encode())
        result["frozen_inputs_equal"] = (result["source_after"] == before and result["product_after"] == product_before
                                         and result["environment_after"] == provenance
                                         and result["fixture_after_sha256"] == release["fixture_sha256"]
                                         and result["fixture_policy_after_sha256"] == hashlib.sha256(policy_expected).hexdigest()
                                         and result["fixture_policy_before_sha256"] == hashlib.sha256(policy_expected).hexdigest()
                                         and result["fixture_policy_bytes_equal"] is True and result["fixture_source_bytes_equal"] is True)
        if not result["frozen_inputs_equal"]:
            result["status"] = "failed: canonical frozen SOURCE inputs changed"
        persist()
    if not result["frozen_inputs_equal"]:
        raise RuntimeError("canonical frozen SOURCE product/native/environment/fixture inputs changed")
    return result


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
