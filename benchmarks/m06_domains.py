"""Actual checked domain/result/failure artifacts with optional data guards.

Build/import/setup/counting/warmups/verification are outside measured intervals.
All three modules are preloaded before intervals to hold catalog size fixed.
tracemalloc is included; no speedup, process RSS or human-benefit claim is made.
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
from pyalamode import boundaries, variants, records
from pyalamode import Some, Ok, Err, Failure, Vector, recorded_clock
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths

WARMUP_CALLS = 10
CONDITIONS = ("domain_construct", "domain_match", "option_match", "result_success", "result_failure", "validation_errors")
SELECTED = ("construct", "domain_size", "option_size", "quotient", "validate_pair")
FIXTURE = '''# mode: fun
from pyalamode import variant, case, Option, Some, Nothing, Result, Ok, Err, Vector, Failure, failure_value, accumulate

@variant
class Batch:
    @case
    class Ready:
        payload: Vector[tuple[int, bool]]
        tag: int
    @case
    class Empty:
        pass

def construct(payload: Vector[tuple[int, bool]], tag: int) -> Batch:
    return Batch.Ready(payload, tag)

def domain_size(value: Batch) -> int:
    match value:
        case Batch.Ready(payload=data):
            return len(data)
        case Batch.Empty():
            return 0

def option_size(value: Option[Vector[tuple[int, bool]]]) -> int:
    match value:
        case Some(value=data):
            return len(data)
        case Nothing():
            return 0

def quotient(payload: Vector[tuple[int, bool]], divisor: int) -> Result[Vector[tuple[int, bool]], Failure]:
    try:
        count = len(payload) // divisor
        return Ok(payload)
    except ZeroDivisionError as caught:
        failure = failure_value(caught)
        return Err(failure)

def validate_pair(left: Result[int, Vector[tuple[int, bool]]], right: Result[str, Vector[tuple[int, bool]]]) -> Result[tuple[int, str], Vector[Vector[tuple[int, bool]]]]:
    return accumulate(left, right)
'''
SMOKE = '''from pyalamode import effects, Clock, ClockCapability, Effectful, Result, Ok, Err, Failure, failure_value, borrow

@effects(Clock)
def read(clock: ClockCapability) -> Result[int, Failure]:
    try:
        return Ok(clock.now_ns())
    except IndexError as caught:
        return Err(failure_value(caught))

@effects(Clock)
def apply(callback: Effectful[[ClockCapability], Result[int, Failure], Clock], clock: ClockCapability) -> Result[int, Failure]:
    with borrow(clock) as scoped:
        return callback(scoped)
'''


def source_snapshot():
    paths = ("pyalamode/variants.py", "pyalamode/failures.py", "pyalamode/records.py",
             "pyalamode/collections.py", "pyalamode/boundaries.py", "tests/m06_runtime.py",
             "benchmarks/m06_domains.py", "benchmarks/m03_collections.py")
    return {"owned_sources": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
            "product_artifacts": foundation_identities()}


def checked_build(directory, name, source, mode, selected=()):
    project = directory / name
    project.mkdir()
    path = project / (name + ".py")
    path.write_text(source)
    policy = '[tool.pyalamode]\nboundary_guards = "' + mode + '"\n'
    if mode != "off":
        policy += "guarded_exports = " + json.dumps([name + ":" + function for function in selected]) + "\n"
    (project / "pyproject.toml").write_text(policy)
    output = project / "artifact"
    report = build_paths([path], root=project, output=output)
    if report.status:
        messages = [item.format() for result in report.results for item in result.diagnostics]
        messages += [item.format() for item in report.tooling]
        raise RuntimeError("benchmark fixture build failed:\n" + "\n".join(messages))
    evidence = json.loads((output / "pyalamode-evidence.json").read_text())
    if mode != "debug":
        assert (output / path.name).read_bytes() == source.encode(), "original artifact changed source"
    return output, {"mode": mode, "module": name,
                    "fixture_sha256": hashlib.sha256(source.encode()).hexdigest(),
                    "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
                    "artifact_files_sha256": evidence["artifact_files"],
                    "guarded_exports": report.guarded_exports, "debug_coverage": report.debug_coverage,
                    "checked_functions": [item.name for result in report.results for item in result.contracts],
                    "actual_off_or_exports_original_source_unchanged": mode != "debug"}


def clear_facades():
    for name in tuple(sys.modules):
        if name == "pyalamode_exports" or name.startswith("pyalamode_exports."):
            del sys.modules[name]


def import_mode(output, name, mode):
    clear_facades()
    sys.path.insert(0, str(output))
    original = importlib.import_module(name)
    selected = original if mode == "off" else importlib.import_module("pyalamode_exports." + name)
    assert original.construct.__code__.co_filename == str(output / (name + ".py"))
    if mode != "off":
        assert all(getattr(selected, function).__wrapped__ is getattr(original, function) for function in SELECTED)
    return original, selected


def prepare(original, selected, condition, size):
    payload = Vector.of(*((index, bool(index % 2)) for index in range(size)))
    if condition == "domain_construct":
        function, arguments = selected.construct, (payload, size)
        verify = lambda result: type(result) is original.Batch.Ready and result.payload is payload and result.tag == size
        work = {"case_payload_nodes": size, "scalar_tuple_width": 2, "case_fields": 2}
    elif condition == "domain_match":
        function, arguments = selected.domain_size, (original.Batch.Ready(payload, size),)
        verify = lambda result: type(result) is int and result == size
        work = {"case_payload_nodes": size, "scalar_tuple_width": 2, "native_full_case_patterns": 2}
    elif condition == "option_match":
        function, arguments = selected.option_size, (Some(payload),)
        verify = lambda result: type(result) is int and result == size
        work = {"option_payload_nodes": size, "scalar_tuple_width": 2, "native_full_case_patterns": 2}
    elif condition in ("result_success", "result_failure"):
        divisor = 1 if condition == "result_success" else 0
        function, arguments = selected.quotient, (payload, divisor)
        verify = ((lambda result: type(result) is Ok and result.value is payload) if divisor else
                  (lambda result: type(result) is Err and result.error == Failure("ZeroDivisionError", "division by zero")))
        work = {"input_payload_nodes": size, "scalar_tuple_width": 2, "division_operations_per_call": 1,
                "actual_zero_division_failures_per_call": int(not divisor),
                "fixed_failure_copies_per_call": int(not divisor), "success_reuses_input_payload": bool(divisor)}
    else:
        other = Vector.of(*((index, bool((index + 1) % 2)) for index in range(size)))
        left, right = Err(payload), Err(other)
        function, arguments = selected.validate_pair, (left, right)
        verify = lambda result: type(result) is Err and len(result.error) == 2 and result.error[0] is payload and result.error[1] is other
        work = {"independent_error_payload_nodes_each": size, "scalar_tuple_width": 2,
                "errors_retained_in_left_to_right_order": 2, "callbacks_invoked_by_accumulate": 0}
    return function, arguments, verify, work


def repeat(function, arguments, calls):
    result = None
    for _ in range(calls):
        result = function(*arguments)
    return result


def count_guards(original, selected, conditions, counter):
    counts = {}
    for condition in conditions:
        function, arguments, verify, _ = prepare(original, selected, condition, 2)
        counter.clear()
        assert verify(function(*arguments))
        counts[condition] = {"deep_assertion_calls_per_invocation": len(counter), "paths": list(counter)}
    return counts


def smoke_build(directory):
    name = "m06_capability_smoke"
    output, details = checked_build(directory, name, SMOKE, "off")
    sys.path.insert(0, str(output))
    module = importlib.import_module(name)
    success = module.apply(module.read, recorded_clock((7,)))
    failure = module.apply(module.read, recorded_clock(()))
    assert success == Ok(7)
    assert failure == Err(Failure("IndexError", "index out of range"))
    details.update({"effectful_exact_capability_callback_success": 7,
                    "borrowed_recorded_clock_exhaustion_failure_category": failure.error.category,
                    "actual_built_off_artifact_imported": True,
                    "scope": "separate untimed callable/capability/lifetime/failure smoke; no capability guards"})
    return details, output, name


def build_and_smoke(directory):
    """Untimed fixture/API gate; no timing or allocation measurements."""
    modes = []
    old_validate = boundaries.validate_data
    counter = []
    def observe(value, schema, *, path="value"):
        counter.append(path)
        return old_validate(value, schema, path=path)
    boundaries.validate_data = observe
    try:
        for mode in ("off", "exports", "debug"):
            name = "m06_workload_" + mode
            output, details = checked_build(directory, name, FIXTURE, mode, SELECTED)
            original, selected = import_mode(output, name, mode)
            details["instrumented_guard_calls"] = count_guards(original, selected, CONDITIONS, counter)
            assert all(details["instrumented_guard_calls"][condition]["deep_assertion_calls_per_invocation"] == 0 for condition in CONDITIONS) if mode == "off" else True
            modes.append((original, selected, details, output, name))
    finally:
        boundaries.validate_data = old_validate
        for original, selected, _, _, _ in modes:
            for module in (original, selected):
                for name, value in tuple(module.__dict__.items()):
                    if value is observe:
                        module.__dict__[name] = old_validate
    smoke, smoke_output, smoke_name = smoke_build(directory)
    for original, selected, details, _, _ in modes:
        for condition in CONDITIONS:
            function, arguments, verify, _ = prepare(original, selected, condition, 2)
            assert verify(function(*arguments))
    return modes, smoke, smoke_output, smoke_name


def benchmark(sizes, trials, calls):
    before = source_snapshot()
    rows = []
    with tempfile.TemporaryDirectory(prefix="pyalamode-m06-benchmark-") as temporary:
        modes, smoke, smoke_output, smoke_name = build_and_smoke(Path(temporary))
        catalog = {"record_classes": len(records._RECORDS), "case_classes": len(variants._CASES), "domain_classes": len(variants._VARIANTS)}
        try:
            for original, selected, details, _, _ in modes:
                for condition in CONDITIONS:
                    for size in sizes:
                        function, arguments, verify, workload = prepare(original, selected, condition, size)
                        assert verify(repeat(function, arguments, WARMUP_CALLS))
                        observations = []
                        for _ in range(trials):
                            result, observed = _measure(lambda: repeat(function, arguments, calls))
                            assert verify(result), (details["mode"], condition)
                            observations.append(observed)
                        rows.append({"mode": details["mode"], "condition": condition, "workload_size": size,
                                     "workload": workload, "calls_per_trial": calls, "warmup_calls_before_trials": WARMUP_CALLS,
                                     "deep_assertion_calls_per_invocation": details["instrumented_guard_calls"][condition]["deep_assertion_calls_per_invocation"],
                                     "observations": observations,
                                     "median_elapsed_seconds": statistics.median(item["elapsed_seconds"] for item in observations),
                                     "median_seconds_per_call": statistics.median(item["elapsed_seconds"] for item in observations) / calls,
                                     "maximum_traced_peak_bytes": max(item["traced_peak_bytes"] for item in observations),
                                     "all_correctness_obligations_passed": True})
            assert catalog == {"record_classes": len(records._RECORDS), "case_classes": len(variants._CASES), "domain_classes": len(variants._VARIANTS)}
        finally:
            for _, _, _, output, name in modes:
                sys.path.remove(str(output))
                sys.modules.pop(name, None)
            sys.path.remove(str(smoke_output))
            sys.modules.pop(smoke_name, None)
            clear_facades()
    after = source_snapshot()
    assert before == after, "source changed during measurement"
    return {"schema": "pyalamode-m06-runtime-measurements-v1", "environment": environment(),
            "workload_sizes": sizes, "trials": trials, "calls_per_trial": calls,
            "measurement_scope": {"tracemalloc_included": True, "allocation_is_python_traced_not_rss": True,
                                  "build_import_setup_counting_warmup_correctness_json_outside_intervals": True,
                                  "gc_collect_before_each_interval": True,
                                  "cache_policy": "all three modules preloaded, process warm; no source-check-cache timing; OS caches uncontrolled",
                                  "catalog_fixed_before_all_intervals": catalog,
                                  "system_load_controlled": False, "retained_history": "last result only; earlier allocation disposal included"},
            "source_identity_before": before, "source_identity_after": after,
            "built_artifacts": [details for _, _, details, _, _ in modes],
            "untimed_effectful_capability_failure_smoke": smoke, "measurements": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[10, 100])
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--calls", type=int, default=25)
    parser.add_argument("--output", default="-")
    arguments = parser.parse_args()
    if any(size < 1 for size in arguments.sizes) or arguments.trials <= 0 or arguments.calls <= 0:
        parser.error("sizes, calls and trials must be positive")
    target_gate()
    result = benchmark(arguments.sizes, arguments.trials, arguments.calls)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output == "-":
        sys.stdout.write(serialized)
    else:
        Path(arguments.output).write_text(serialized)


if __name__ == "__main__":
    main()
