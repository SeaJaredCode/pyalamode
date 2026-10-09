"""Named generated-artifact guard and snapshot measurements on CPython 3.13.1.

Actual off/exports/debug builds share an entry -> eight direct checked leaf
calls. Separate untimed instrumentation counts deep assertion invocations.
Timing includes tracemalloc; Python allocation peaks are not process RSS.
"""

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import statistics
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks.m03_collections import environment, target_gate, _measure
from pyalamode import boundaries
from pyalamode.collections import Vector
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths

LEAF_CALLS = 8
FIXTURE = '''# mode: fun
from pyalamode import Vector

def leaf(data: Vector[tuple[int, bool]]) -> Vector[tuple[int, bool]]:
    return data

def entry(data: Vector[tuple[int, bool]]) -> Vector[tuple[int, bool]]:
    first = leaf(data)
    second = leaf(first)
    third = leaf(second)
    fourth = leaf(third)
    fifth = leaf(fourth)
    sixth = leaf(fifth)
    seventh = leaf(sixth)
    eighth = leaf(seventh)
    return eighth
'''


def source_snapshot():
    owned = ("pyalamode/records.py", "pyalamode/boundaries.py", "pyalamode/collections.py",
             "tests/m04_runtime.py", "benchmarks/m04_boundaries.py", "benchmarks/m03_collections.py")
    return {"owned_sources": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in owned},
            "product_artifacts": foundation_identities()}


def build_condition(directory, mode):
    project = directory / mode
    project.mkdir()
    (project / "workload.py").write_text(FIXTURE)
    policy = '[tool.pyalamode]\nboundary_guards = "' + mode + '"\n'
    if mode != "off":
        policy += 'guarded_exports = ["workload:entry"]\n'
    (project / "pyproject.toml").write_text(policy)
    output = project / "artifact"
    report = build_paths([project / "workload.py"], root=project, output=output)
    if report.status:
        messages = [diagnostic.format() for result in report.results for diagnostic in result.diagnostics]
        messages += [diagnostic.format() for diagnostic in report.tooling]
        raise RuntimeError("benchmark fixture build failed:\n" + "\n".join(messages))
    evidence = json.loads((output / "pyalamode-evidence.json").read_text())
    return output, {"mode": mode, "fixture_sha256": hashlib.sha256(FIXTURE.encode()).hexdigest(),
                    "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
                    "artifact_files_sha256": evidence["artifact_files"],
                    "guarded_exports": report.guarded_exports, "debug_coverage": report.debug_coverage}


def import_condition(output, mode, fixture):
    sys.path.insert(0, str(output))
    original_validate = boundaries.validate_data
    calls = []

    def observe(value, schema, *, path="value"):
        calls.append(path)
        return original_validate(value, schema, path=path)

    boundaries.validate_data = observe
    try:
        original = importlib.import_module("workload")
        selected = original if mode == "off" else importlib.import_module("pyalamode_exports.workload")
        returned = selected.entry(fixture)
        assert returned is fixture
        assert selected.entry.__wrapped__ is original.entry if mode != "off" else True
        expected = {"off": 0, "exports": 2, "debug": 2 + 1 + LEAF_CALLS * 3 + 1}[mode]
        assert len(calls) == expected, (mode, expected, calls)
        if mode == "exports":
            assert not any("leaf" in path for path in calls)
            assert original.entry.__code__.co_filename == str(output / "workload.py")
        observations = {"deep_assertion_calls_per_entry": len(calls), "paths": calls,
                        "internal_direct_leaf_calls_per_entry": LEAF_CALLS,
                        "generated_facade_preserves_original_function_identity": mode == "off" or selected.entry.__wrapped__ is original.entry}
        # Remove counting overhead from every imported alias before timing.
        for module in (original, selected):
            for name, value in tuple(module.__dict__.items()):
                if value is observe:
                    module.__dict__[name] = original_validate
        return selected.entry, observations
    finally:
        boundaries.validate_data = original_validate


def unload_condition(output):
    sys.path.remove(str(output))
    for name in tuple(sys.modules):
        if name == "workload" or name == "pyalamode_exports" or name.startswith("pyalamode_exports."):
            del sys.modules[name]


def repeat(function, data, calls):
    result = None
    for _ in range(calls):
        result = function(data)
    return result


def row(condition, size, calls, observations, **extra):
    return {"condition": condition, "payload_size": size, "calls_per_trial": calls,
            "observations": observations,
            "median_elapsed_seconds": statistics.median(item["elapsed_seconds"] for item in observations),
            "median_seconds_per_call": statistics.median(item["elapsed_seconds"] for item in observations) / calls,
            "maximum_traced_peak_bytes": max(item["traced_peak_bytes"] for item in observations),
            "all_correctness_obligations_passed": True, **extra}


def benchmark(sizes, trials, calls):
    before = source_snapshot()
    measurements, builds = [], []
    with tempfile.TemporaryDirectory(prefix="pyalamode-m04-benchmark-") as temporary:
        directory = Path(temporary)
        for mode in ("off", "exports", "debug"):
            output, details = build_condition(directory, mode)
            function, observed = import_condition(output, mode, Vector.of((1, True), (2, False)))
            details["instrumented_call_graph"] = observed
            builds.append(details)
            try:
                for size in sizes:
                    fixture = Vector.of(*((index, bool(index % 2)) for index in range(size)))
                    observations = []
                    for _ in range(trials):
                        result, measured = _measure(lambda: repeat(function, fixture, calls))
                        assert result is fixture
                        observations.append(measured)
                    measurements.append(row("generated_" + mode, size, calls, observations,
                                            deep_assertion_calls_per_entry=observed["deep_assertion_calls_per_entry"]))
            finally:
                unload_condition(output)
        for size in sizes:
            source = {"items": [[index, bool(index % 2)] for index in range(size)]}
            stable = freeze_fixture(source)
            for condition, function, data in (("freeze_nested_mutable", freeze_fixture, source),
                                               ("thaw_nested_snapshot", boundaries.thaw, stable)):
                observations = []
                for _ in range(trials):
                    result, measured = _measure(lambda: repeat(function, data, calls))
                    if condition == "freeze_nested_mutable":
                        assert result == stable
                        source["items"][0][0] = -1
                        assert result["items"][0][0] == 0
                        source["items"][0][0] = 0
                    else:
                        assert result == source
                        independent = boundaries.thaw(stable)
                        result["items"][0][0] = -1
                        assert independent["items"][0][0] == 0 and stable["items"][0][0] == 0
                    observations.append(measured)
                measurements.append(row(condition, size, calls, observations))
    after = source_snapshot()
    if before != after:
        raise RuntimeError("product/harness/test sources changed during measurement; evidence not written")
    return {"schema": 1, "workload": "M04 generated entry -> eight direct checked leaf calls; nested exact tuple payload; nested list/dict snapshots",
            "target": "cpython-3.13.1", "environment": environment(),
            "source_sha256": after["owned_sources"], "product_artifacts_sha256": after["product_artifacts"],
            "source_snapshot_unchanged": True, "builds": builds,
            "conditions": {"sizes": sizes, "trials": trials, "calls_per_trial": calls,
                           "guard_payload": "Vector of n exact (int,bool) tuples; data-returning entry with eight direct leaves",
                           "snapshot_payload": "exact insertion-ordered dict {'items': n exact [int,bool] lists}",
                           "included": "runtime assertions/conversion, container allocation, calls/loop, perf_counter and tracemalloc overhead",
                           "excluded": "build/import, fixtures, counter instrumentation, correctness probes, environment/source hashing, JSON writing",
                           "memory": "tracemalloc Python allocation only, not RSS; fixture/result bases preexist tracing",
                           "OS_page_cache": "uncontrolled; no cold-cache claim",
                           "source_gate": "all product artifacts plus runtime/test/harness files equal before/after every platform run"},
            "cost_contract": {"records": "f fixed fields: construction/replacement O(f + D); field access O(1); equality O(f + compared data)",
                              "registry": "identity-only tuple search O(R) in number of declared record classes, multiplied by record-recognition visits",
                              "exports": "one recursive argument assertion and one result assertion per selected entry; no generated internal guards",
                              "debug": "exports plus supported parameter/local/return assertions; this fixture has 28 deep assertions per selected entry",
                              "snapshots": "by-value recursive copying; no identity deduplication; O(N*h + scalar-key sorting), constructor validation can revisit ancestors' payload",
                              "thaw": "O(D + R*record_recognition_visits), fresh container per occurrence; generic validation precedes allocation",
                              "limits": "depth/path construction, arbitrary scalar lengths, garbage collection and allocations add costs; no universal latency/speedup claim"},
            "measurements": measurements}


def freeze_fixture(source):
    return boundaries.freeze(source, exclusive=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sizes", type=int, nargs="+", default=[100, 1000])
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--calls", type=int, default=25)
    args = parser.parse_args()
    target_gate()
    if any(size < 1 for size in args.sizes) or args.trials < 1 or args.calls < 1:
        parser.error("sizes, trials and calls must be positive")
    result = benchmark(args.sizes, args.trials, args.calls)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Recorded {len(result['measurements'])} conditions; generated guard counts and snapshot assertions passed: {args.output}")


if __name__ == "__main__":
    main()
