"""Actual checked artifact provider/borrow measurements on CPython 3.13.1.

Build/import/setup/warmups and correctness checks are outside intervals. Every
interval includes tracemalloc. These heterogeneous conditions describe finite
operation costs, not comparative speedup, deterministic live results, or RSS.
"""

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import statistics
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks.m03_collections import environment, target_gate, _measure
from pyalamode.effects import (state, recorded_clock, live_clock, recorded_random, live_random,
                              recorded_environment, live_environment, recorded_io, live_io)
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths

FULL_IO = ("read_text", "write_text")
ENVIRONMENT_NAME = "PYALAMODE_M05_BENCHMARK"
WARMUP_CALLS = 10
FIXTURE = '''# mode: fun
from pyalamode import effects, borrow, Effectful, State, Clock, Random, Environment, IO
from pyalamode import StateCapability, ClockCapability, RandomCapability, EnvironmentCapability, IOCapability

@effects(State)
def state_step(cell: StateCapability, increment: int) -> int:
    before = cell.get()
    cell.set(before + increment)
    return cell.get()

@effects(State)
def borrowed_step(cell: StateCapability, increment: int) -> int:
    with borrow(cell) as scoped:
        before = scoped.get()
        scoped.set(before + increment)
        result = scoped.get()
    return result

@effects(Clock)
def clock_read(clock: ClockCapability) -> int:
    return clock.now_ns()

@effects(Clock)
def apply_clock(callback: Effectful[[ClockCapability], int, Clock], clock: ClockCapability) -> int:
    return callback(clock)

@effects(Random)
def random_read(random: RandomCapability, bound: int) -> int:
    return random.below(bound)

@effects(Environment)
def environment_read(environment: EnvironmentCapability, name: str) -> str:
    return environment.get(name, 'absent')

@effects(IO)
def io_roundtrip(io: IOCapability, path: str, text: str) -> str:
    io.write_text(path, text)
    return io.read_text(path)
'''


def source_snapshot():
    paths = ("pyalamode/effects.py", "tests/m05_runtime.py", "benchmarks/m05_effects.py", "benchmarks/m03_collections.py")
    return {"owned_sources": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
            "product_artifacts": foundation_identities()}


def build_fixture(directory):
    source = directory / "m05_workload.py"
    source.write_text(FIXTURE)
    policy = '[tool.pyalamode]\nboundary_guards = "off"\n'
    (directory / "pyproject.toml").write_text(policy)
    output = directory / "artifact"
    report = build_paths([source], root=directory, output=output)
    if report.status:
        messages = [item.format() for result in report.results for item in result.diagnostics]
        messages += [item.format() for item in report.tooling]
        raise RuntimeError("benchmark fixture build failed:\n" + "\n".join(messages))
    evidence = json.loads((output / "pyalamode-evidence.json").read_text())
    sys.path.insert(0, str(output))
    module = importlib.import_module("m05_workload")
    assert module.apply_clock(module.clock_read, recorded_clock((7,))) == 7
    assert module.clock_read.__code__.co_filename == str(output / "m05_workload.py")
    details = {"fixture_sha256": hashlib.sha256(FIXTURE.encode()).hexdigest(),
               "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
               "artifact_files_sha256": evidence["artifact_files"], "boundary_guards": "off",
               "checked_functions": [item.name for result in report.results for item in result.contracts],
               "effectful_capability_callback_smoke_result": 7,
               "ordinary_import_of_actual_built_artifact": True,
               "original_function_code_and_identity_preserved": True}
    return module, output, details


def repeat(function, arguments, calls):
    result = None
    for _ in range(calls):
        result = function(*arguments)
    return result


def prepare(module, directory, condition, size, calls):
    if condition in {"state_direct", "state_borrow"}:
        provider = state(0)
        function = module.state_step if condition == "state_direct" else module.borrowed_step
        arguments = (provider, size)
        expected = size * calls
        verify = lambda result: result == expected and provider.get() == expected
        workload = {"increment": size, "get_operations_per_call": 2, "set_operations_per_call": 1,
                    "logical_borrows_per_call": int(condition == "state_borrow"), "borrow_depth": int(condition == "state_borrow")}
    elif condition in {"clock_recorded", "clock_live"}:
        provider = recorded_clock(tuple(range(max(size, calls)))) if condition == "clock_recorded" else live_clock()
        function, arguments = module.clock_read, (provider,)
        verify = (lambda result: result == calls - 1) if condition == "clock_recorded" else (lambda result: type(result) is int)
        workload = {"clock_reads_per_call": 1, "recorded_pool_size": max(size, calls) if condition == "clock_recorded" else None,
                    "live_clock_has_no_size_parameter": condition == "clock_live"}
    elif condition in {"random_recorded", "random_live"}:
        provider = recorded_random((size - 1,) * calls) if condition == "random_recorded" else live_random()
        function, arguments = module.random_read, (provider, size)
        verify = (lambda result: result == size - 1) if condition == "random_recorded" else (lambda result: type(result) is int and 0 <= result < size)
        workload = {"bound": size, "random_operations_per_call": 1, "recorded_pool_size": calls if condition == "random_recorded" else None}
    elif condition in {"environment_recorded", "environment_live"}:
        entries = tuple(("M05_KEY_" + str(index), "unused") for index in range(size - 1)) + ((ENVIRONMENT_NAME, "present"),)
        provider = recorded_environment(entries) if condition == "environment_recorded" else live_environment()
        function, arguments = module.environment_read, (provider, ENVIRONMENT_NAME)
        verify = lambda result: result == "present"
        workload = {"environment_lookups_per_call": 1, "recorded_entries": size if condition == "environment_recorded" else None,
                    "selected_recorded_position": size - 1 if condition == "environment_recorded" else None,
                    "live_environment_has_no_size_parameter": condition == "environment_live"}
    else:
        text = "x" * size
        provider = recorded_io((), allowed_ops=FULL_IO) if condition == "io_recorded" else live_io(str(directory), allowed_ops=FULL_IO)
        function, arguments = module.io_roundtrip, (provider, "roundtrip.txt", text)
        verify = lambda result: result == text
        workload = {"utf8_text_bytes": size, "write_operations_per_call": 1, "read_operations_per_call": 1,
                    "allowed_ops": list(FULL_IO), "existing_recorded_entries_after_first_write": 1 if condition == "io_recorded" else None,
                    "filesystem_cache_uncontrolled": condition == "io_live"}
    return function, arguments, verify, workload


def benchmark(sizes, trials, calls):
    before = source_snapshot()
    rows = []
    previous_environment = os.environ.get(ENVIRONMENT_NAME)
    os.environ[ENVIRONMENT_NAME] = "present"
    try:
        with tempfile.TemporaryDirectory(prefix="pyalamode-m05-benchmark-") as temporary:
            directory = Path(temporary)
            module, output, built = build_fixture(directory)
            try:
                for condition in ("state_direct", "state_borrow", "clock_recorded", "clock_live", "random_recorded", "random_live",
                                  "environment_recorded", "environment_live", "io_recorded", "io_live"):
                    for size in sizes:
                        warm_function, warm_arguments, warm_verify, _ = prepare(module, directory, condition, size, WARMUP_CALLS)
                        assert warm_verify(repeat(warm_function, warm_arguments, WARMUP_CALLS))
                        observations = []
                        for _ in range(trials):
                            function, arguments, verify, workload = prepare(module, directory, condition, size, calls)
                            result, observed = _measure(lambda: repeat(function, arguments, calls))
                            assert verify(result), condition
                            observations.append(observed)
                        rows.append({"condition": condition, "workload_size": size, "workload": workload,
                                     "calls_per_trial": calls, "warmup_calls_before_trials": WARMUP_CALLS,
                                     "observations": observations,
                                     "median_elapsed_seconds": statistics.median(item["elapsed_seconds"] for item in observations),
                                     "median_seconds_per_call": statistics.median(item["elapsed_seconds"] for item in observations) / calls,
                                     "maximum_traced_peak_bytes": max(item["traced_peak_bytes"] for item in observations),
                                     "all_correctness_obligations_passed": True})
            finally:
                sys.path.remove(str(output))
                sys.modules.pop("m05_workload", None)
    finally:
        if previous_environment is None:
            del os.environ[ENVIRONMENT_NAME]
        else:
            os.environ[ENVIRONMENT_NAME] = previous_environment
    after = source_snapshot()
    assert before == after, "source changed during measurement"
    return {"schema": "pyalamode-m05-runtime-measurements-v1", "environment": environment(),
            "workload_sizes": sizes, "trials": trials, "calls_per_trial": calls,
            "measurement_scope": {"tracemalloc_included": True, "allocation_is_python_traced_not_rss": True,
                                  "build_import_setup_warmup_correctness_json_outside_intervals": True,
                                  "gc_collect_before_each_interval": True,
                                  "cache_policy": "in-process warm imports; no source-check-cache timing; filesystem/OS caches uncontrolled",
                                  "live_results_nondeterministic": True, "system_load_controlled": False,
                                  "state_trial_reset": True, "recorded_cursor_trial_reset": True},
            "source_identity_before": before, "source_identity_after": after,
            "built_artifact": built, "measurements": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", type=int, nargs="+", default=[100, 1000])
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--calls", type=int, default=25)
    parser.add_argument("--output", default="-")
    arguments = parser.parse_args()
    if any(size <= 1 for size in arguments.sizes) or arguments.trials <= 0 or arguments.calls <= 0:
        parser.error("sizes must exceed one and calls/trials must be positive")
    target_gate()
    result = benchmark(arguments.sizes, arguments.trials, arguments.calls)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output == "-":
        sys.stdout.write(serialized)
    else:
        Path(arguments.output).write_text(serialized)


if __name__ == "__main__":
    main()
