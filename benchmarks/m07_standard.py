"""Actual checked standard/toolkit artifacts with optional data assertions.

Six eager named paths are built/imported before timing. Inputs, guard counting,
warmups and correctness checks are excluded; tracemalloc and disposal are included.
These observations do not measure human usefulness or general application speed.
"""

import argparse
import builtins
import codecs
import hashlib
import importlib
import json
from pathlib import Path
import statistics
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks.m03_collections import environment, target_gate, _measure
from pyalamode import boundaries, records, sums
from pyalamode import Vector, OrderedMap, Ok, Err
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths

CONDITIONS = ("text_decimal", "encoding_roundtrip", "scan", "grouping", "composition", "traversal_first_error")
SELECTED = ("text_decimal", "encoding_roundtrip", "scan", "grouping", "composition", "traversal")
WARMUP_CALLS = 10
FIXTURE = '''# mode: fun
from pyalamode import Vector, OrderedMap, Result, Ok, Err
from pyalamode import text_split, text_join, text_replace, integer_clamp, integer_parse_decimal, integer_format_decimal
from pyalamode import utf8_encode, utf8_decode, hex_encode, hex_decode, vector_scan, vector_group_by, compose, partial_first, result_traverse

def parse_piece(text: str) -> int:
    return integer_parse_decimal(text)

def render_piece(value: int) -> str:
    return integer_format_decimal(integer_clamp(value, -1000000, 1000000))

def text_decimal(text: str) -> str:
    normalized = text_replace(text, ";", ",")
    pieces = text_split(normalized, ",")
    numbers = pieces.map(parse_piece)
    rendered = numbers.map(render_piece)
    return text_join(rendered, "|")

def encoding_roundtrip(text: str) -> str:
    return utf8_decode(hex_decode(hex_encode(utf8_encode(text))))

def add(accumulator: int, value: int) -> int:
    return accumulator + value

def scan(values: Vector[int]) -> Vector[int]:
    return vector_scan(values, add, 0)

def bucket(value: int) -> int:
    return value % 7

def grouping(values: Vector[int]) -> OrderedMap[int, Vector[int]]:
    return vector_group_by(values, bucket)

def multiply(rate: int, value: int) -> int:
    return rate * value

def increment(value: int) -> int:
    return value + 1

def composition(values: Vector[int]) -> Vector[int]:
    scaled = partial_first(multiply, 2)
    revised = compose(increment, scaled)
    return values.map(revised)

def nonnegative(value: int) -> Result[int, str]:
    if value < 0:
        return Err("negative")
    return Ok(value + 1)

def traversal(values: Vector[int]) -> Result[Vector[int], str]:
    return result_traverse(values, nonnegative)
'''
SMOKE_TEMPLATE = '''from pyalamode import fun, effects, IO, Clock, Environment, IOCapability, ClockCapability, EnvironmentCapability
from pyalamode import live_io, recorded_clock, recorded_environment, text_startswith, text_slice

io = live_io(ROOT_LITERAL, allowed_ops=("read_text", "write_text"))
clock = recorded_clock((7,))
environment = recorded_environment((("MODE", "test"),))

@effects(IO)
def read_file(capability: IOCapability) -> str:
    return capability.read_text("payload")

@effects(IO)
def write_file(capability: IOCapability, text: str) -> None:
    capability.write_text("payload", text)
    return None

@effects(IO)
def read_named(capability: IOCapability, path: str) -> str:
    return capability.read_text(path)

@effects(IO)
def write_named(capability: IOCapability, path: str, text: str) -> None:
    capability.write_text(path, text)
    return None

@effects(Clock)
def timestamp(capability: ClockCapability) -> int:
    return capability.now_ns()

@effects(Environment)
def configuration(capability: EnvironmentCapability) -> str:
    return capability.get("MODE", "unset")

@effects(Environment)
def configuration_named(capability: EnvironmentCapability, name: str) -> str:
    return capability.get(name, "unset")

@fun
def pure_tail(text: str) -> str:
    if text_startswith(text, "+"):
        return text_slice(text, 1, len(text))
    return text
'''


def source_snapshot():
    paths = ("pyalamode/standard.py", "pyalamode/effects.py", "tests/m07_runtime.py",
             "benchmarks/m07_standard.py", "benchmarks/m03_collections.py")
    return {"owned_sources": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
            "product_artifacts": foundation_identities(),
            "full_package_sources": {"pyalamode/" + path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                     for path in sorted((ROOT / "pyalamode").glob("*.py"))}}


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
        assert (output / path.name).read_bytes() == source.encode(), "original source changed"
    return output, {"mode": mode, "module": name,
                    "fixture_sha256": hashlib.sha256(source.encode()).hexdigest(),
                    "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
                    "artifact_files_sha256": evidence["artifact_files"],
                    "guarded_exports": report.guarded_exports, "debug_coverage": report.debug_coverage,
                    "checked_functions": [item.name for result in report.results for item in result.contracts],
                    "file_initialization": [{"module_mode": result.module_mode,
                                             "initialization_evidence": result.initialization_evidence,
                                             "setup_observations": result.setup_observations}
                                            for result in report.results],
                    "checked_runtime_environment": report.to_dict()["runtime_environment"],
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
    assert original.text_decimal.__code__.co_filename == str(output / (name + ".py"))
    if mode != "off":
        assert all(getattr(selected, function).__wrapped__ is getattr(original, function) for function in SELECTED)
    return original, selected


def prepare(selected, condition, size):
    values = tuple(range(size))
    if condition == "text_decimal":
        text = ";".join(str(value) for value in values)
        expected = "|".join(str(value) for value in values)
        function, arguments = selected.text_decimal, (text,)
        verify = lambda result: type(result) is str and result == expected
        work = {"decimal_items": size, "text_code_points": len(text), "parse_and_format_calls_each": size,
                "ordered_maps": 2, "native_replace_split_join_each": 1}
    elif condition == "encoding_roundtrip":
        text = ("é𐀀\r\n\ufeff" * ((size + 4) // 5))[:size]
        function, arguments = selected.encoding_roundtrip, (text,)
        verify = lambda result: type(result) is str and result == text
        work = {"text_code_points": size, "utf8_bytes": len(text.encode("utf-8")),
                "utf8_encode_decode_hex_encode_decode_each": 1}
    elif condition == "scan":
        function, arguments = selected.scan, (Vector.of(*values),)
        expected = Vector.of(*(index * (index - 1) // 2 for index in range(size + 1)))
        verify = lambda result: type(result) is Vector and result == expected
        work = {"input_items": size, "binary_callback_invocations": size, "accumulator_outputs": size + 1}
    elif condition == "grouping":
        payload = Vector.of(*values)
        function, arguments = selected.grouping, (payload,)
        expected = OrderedMap.of(*((key, Vector.of(*(value for value in values if value % 7 == key)))
                                   for key in range(min(size, 7))))
        verify = lambda result: type(result) is OrderedMap and result == expected and result[0][0] is payload[0]
        work = {"input_items": size, "unary_key_callback_invocations": size, "groups": min(size, 7),
                "first_key_appearance_and_within_group_order": True}
    elif condition == "composition":
        function, arguments = selected.composition, (Vector.of(*values),)
        expected = Vector.of(*(value * 2 + 1 for value in values))
        verify = lambda result: type(result) is Vector and result == expected
        work = {"input_items": size, "partial_and_compose_constructions_each": 1,
                "inner_and_outer_callback_invocations_each": size, "stable_bound": 2}
    else:
        cutoff = size // 2
        payload = Vector.of(*(value if index != cutoff else -1 for index, value in enumerate(values)))
        function, arguments = selected.traversal, (payload,)
        verify = lambda result: type(result) is Err and result.error == "negative"
        work = {"input_items": size, "first_error_index": cutoff, "callback_invocations": cutoff + 1,
                "later_callbacks_skipped": size - cutoff - 1, "successful_values_discarded_on_error": cutoff}
    return function, arguments, verify, work


def repeat(function, arguments, calls):
    result = None
    for _ in range(calls):
        result = function(*arguments)
    return result


def smoke_build(directory):
    io_root = directory / "io_root"
    io_root.mkdir()
    source = SMOKE_TEMPLATE.replace("ROOT_LITERAL", repr(str(io_root)))
    name = "m07_effect_setup_smoke"
    output, details = checked_build(directory, name, source, "off")
    sys.path.insert(0, str(output))
    module = importlib.import_module(name)
    native_open = builtins.open
    streams, handler_calls = [], []
    previous = {name: codecs.lookup_error(name) for name in ("strict", "surrogateescape")}
    def observed_open(*args, **kwargs):
        stream = native_open(*args, **kwargs)
        streams.append(stream)
        return stream
    def replacement(error):
        handler_calls.append(type(error).__name__)
        return ("replacement", error.end)
    for name in previous:
        codecs.register_error(name, replacement)
    try:
        with patch("builtins.open", observed_open):
            text = "\ufeffé\r\nline\r\n𐀀"
            assert module.write_file(module.io, text) is None
            assert module.read_file(module.io) == text
            (io_root / "payload").write_bytes(b"\xff")
            try:
                module.read_file(module.io)
            except UnicodeDecodeError:
                pass
            else:
                raise AssertionError("malformed rooted UTF8 read did not fail")
            try:
                module.write_file(module.io, "\ud800")
            except UnicodeEncodeError:
                pass
            else:
                raise AssertionError("surrogate rooted UTF8 write did not fail")
            for call in (lambda:module.read_named(module.io, "\ud800"),
                         lambda:module.write_named(module.io, "\udc80", "text"),
                         lambda:module.configuration_named(module.environment, "\ud800")):
                try:
                    call()
                except ValueError:
                    pass
                else:
                    raise AssertionError("surrogate OS name was not refused")
        assert (io_root / "payload").read_bytes() == b""
        assert len(streams) == 4 and all(stream.closed for stream in streams)
        assert handler_calls == []
    finally:
        for name, handler in previous.items():
            codecs.register_error(name, handler)
    assert module.timestamp(module.clock) == 7
    assert module.configuration(module.environment) == "test"
    assert module.pure_tail("+12") == "12"
    assert all(not item["module_mode"] and item["initialization_evidence"] == "unchecked ordinary module initialization"
               for item in details["file_initialization"])
    assert sum(len(item["setup_observations"]) for item in details["file_initialization"]) == 3
    from pyalamode import live_io
    restricted = live_io(str(io_root), allowed_ops=("read_text",))
    try:
        module.write_file(restricted, "denied")
    except PermissionError:
        pass
    else:
        raise AssertionError("ordinary full-interface IO permission gate missing")
    details.update({"registered_strict_and_surrogateescape_handler_calls": 0, "crlf_bom_nonbmp_roundtrip": True,
                    "acquired_native_streams": len(streams), "all_streams_closed_on_success_and_failure": True,
                    "failed_encode_preserves_open_truncation": True, "permission_denial_checked": True,
                    "surrogate_rooted_paths_and_environment_names_refused": True,
                    "recorded_clock_value": 7, "recorded_environment_value": "test",
                    "setup_is_ordinary_initialization_separate_from_pure_export": True,
                    "scope": "separate untimed actual off-artifact IO/Clock/Environment/setup smoke"})
    return details, output, name


def build_and_smoke(directory, sizes=(10, 100)):
    """Untimed API/artifact gate, no intervals or allocation measurement."""
    modes = []
    native_validate = boundaries.validate_data
    counter = []
    def observe(value, schema, *, path="value"):
        counter.append(path)
        return native_validate(value, schema, path=path)
    boundaries.validate_data = observe
    try:
        for mode in ("off", "exports", "debug"):
            name = "m07_workload_" + mode
            output, details = checked_build(directory, name, FIXTURE, mode, SELECTED)
            original, selected = import_mode(output, name, mode)
            guard_counts = {}
            for condition in CONDITIONS:
                guard_counts[condition] = {}
                for size in sizes:
                    function, arguments, verify, _ = prepare(selected, condition, size)
                    counter.clear()
                    assert verify(function(*arguments)), condition
                    guard_counts[condition][str(size)] = {"deep_assertion_calls_per_invocation": len(counter), "paths": list(counter)}
            if mode == "off":
                assert all(row["deep_assertion_calls_per_invocation"] == 0 for sizes_row in guard_counts.values() for row in sizes_row.values())
            details["instrumented_guard_calls"] = guard_counts
            modes.append((original, selected, details, output, name))
    finally:
        boundaries.validate_data = native_validate
        for original, selected, _, _, _ in modes:
            for module in (original, selected):
                for name, value in tuple(module.__dict__.items()):
                    if value is observe:
                        module.__dict__[name] = native_validate
    smoke, smoke_output, smoke_name = smoke_build(directory)
    for original, selected, details, _, _ in modes:
        assert selected.traversal(Vector.of(1, 2)) == Ok(Vector.of(2, 3))
        for condition in CONDITIONS:
            function, arguments, verify, _ = prepare(selected, condition, 2)
            assert verify(function(*arguments)), (details["mode"], condition)
    return modes, smoke, smoke_output, smoke_name


def benchmark(sizes, trials, calls):
    before = source_snapshot()
    rows = []
    with tempfile.TemporaryDirectory(prefix="pyalamode-m07-benchmark-") as temporary:
        modes, smoke, smoke_output, smoke_name = build_and_smoke(Path(temporary), sizes)
        catalog = {"record_classes": len(records._RECORDS), "case_classes": len(sums._CASES),
                   "domain_classes": len(sums._ONEOFS)}
        try:
            for original, selected, details, _, _ in modes:
                for condition in CONDITIONS:
                    for size in sizes:
                        function, arguments, verify, workload = prepare(selected, condition, size)
                        assert verify(repeat(function, arguments, WARMUP_CALLS))
                        observations = []
                        for _ in range(trials):
                            result, observed = _measure(lambda: repeat(function, arguments, calls))
                            assert verify(result), (details["mode"], condition)
                            observations.append(observed)
                        rows.append({"mode": details["mode"], "condition": condition, "workload_size": size,
                                     "workload": workload, "calls_per_trial": calls,
                                     "warmup_calls_before_trials": WARMUP_CALLS, "observations": observations,
                                     "deep_assertion_calls_per_invocation": details["instrumented_guard_calls"][condition][str(size)]["deep_assertion_calls_per_invocation"],
                                     "median_elapsed_seconds": statistics.median(item["elapsed_seconds"] for item in observations),
                                     "median_seconds_per_call": statistics.median(item["elapsed_seconds"] for item in observations) / calls,
                                     "maximum_traced_peak_bytes": max(item["traced_peak_bytes"] for item in observations),
                                     "all_correctness_obligations_passed": True})
            assert catalog == {"record_classes": len(records._RECORDS), "case_classes": len(sums._CASES),
                               "domain_classes": len(sums._ONEOFS)}
        finally:
            for _, _, _, output, name in modes:
                sys.path.remove(str(output))
                sys.modules.pop(name, None)
            sys.path.remove(str(smoke_output))
            sys.modules.pop(smoke_name, None)
            clear_facades()
    after = source_snapshot()
    assert before == after, "source changed during measurement"
    runtime_environment = environment()
    runtime_environment.update({"filesystem_encoding": sys.getfilesystemencoding(),
                                "filesystem_encode_errors": sys.getfilesystemencodeerrors(),
                                "utf8_mode": sys.flags.utf8_mode})
    return {"schema": "pyalamode-m07-runtime-measurements-v1", "environment": runtime_environment,
            "workload_sizes": sizes, "trials": trials, "calls_per_trial": calls,
            "measurement_scope": {"tracemalloc_included": True, "allocation_is_python_traced_not_rss": True,
                                  "build_import_inputs_guard_count_warmup_correctness_hash_json_outside_intervals": True,
                                  "gc_collect_before_each_interval": True,
                                  "cache_policy": "three modules preloaded, warm process; OS caches uncontrolled",
                                  "fixed_catalog_before_all_intervals": catalog, "system_load_controlled": False,
                                  "retained_history": "last result only; earlier transient disposal included",
                                  "guard_counts": "each exact measured condition/size counted untimed; debug count may scale with callbacks"},
            "source_identity_before": before, "source_identity_after": after,
            "built_artifacts": [details for _, _, details, _, _ in modes],
            "untimed_effectful_setup_smoke": smoke, "measurements": rows}


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
