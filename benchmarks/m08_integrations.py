"""Bounded approved adapter calls through actual checked ordinary artifacts.

Backend setup/build/import/approval preparation and correctness are untimed.
Invocation loops, assertions, transient disposal and tracemalloc are measured.
The protocol requires root approval and joint source freeze before intervals.
"""

import argparse
import binascii
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
from pyalamode.integration_contracts import integration_snapshot
from pyalamode.model import foundation_identities, runtime_environment
from pyalamode.project import build_paths

CONDITIONS = ("encode", "decode", "digest", "transport_digest")
SELECTED = ("encode_payload", "decode_payload", "content_digest", "transport_digest")
WARMUP_CALLS = 10
FIXTURE = '''from pyalamode import fun
from pyalamode.integrations import base64_encode, base64_decode, sha256_digest

@fun
def encode_payload(data: bytes) -> bytes:
    return base64_encode(data)

@fun
def decode_payload(data: bytes) -> bytes:
    return base64_decode(data)

@fun
def content_digest(data: bytes) -> bytes:
    return sha256_digest(data)

@fun
def transport_digest(data: bytes) -> tuple[bytes, bytes]:
    encoded = base64_encode(data)
    decoded = base64_decode(encoded)
    return (encoded, sha256_digest(decoded))
'''


def source_snapshot():
    paths = ("pyalamode/integrations.py", "tests/m08_runtime.py",
             "benchmarks/m08_integrations.py", "benchmarks/m03_collections.py")
    snapshot = integration_snapshot(root=ROOT)
    assert not snapshot["errors"], snapshot["errors"]
    assert all(row["installed_identity"] for row in snapshot["catalog"])
    return {
        "owned_sources": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
        "product_artifacts": foundation_identities(),
        "full_package_sources": {"pyalamode/" + path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in sorted((ROOT / "pyalamode").glob("*.py"))},
        "installed_dependencies": {row["identity"]: {"identity": row["installed_identity"],
                                                    "dependency_sha256": row["dependency_sha256"],
                                                    "contract_sha256": row["contract_sha256"]}
                                   for row in snapshot["catalog"]},
    }


def fixture_policy(project, name, mode):
    """Explicit root-authorized benchmark approvals, never production approval."""
    snapshot = integration_snapshot(root=project)
    assert not snapshot["errors"], snapshot["errors"]
    assert all(row["installed_identity"] for row in snapshot["catalog"])
    policy = '[tool.pyalamode]\nexternal_trust = "approved"\nboundary_guards = ' + json.dumps(mode) + "\n"
    if mode != "off":
        policy += "guarded_exports = " + json.dumps([name + ":" + function for function in SELECTED]) + "\n"
    for row in snapshot["catalog"]:
        entry = {"operation": row["identity"], "contract_sha256": row["contract_sha256"],
                 "dependency_sha256": row["dependency_sha256"], "owner": "root-authorized M8 benchmark fixture",
                 "rationale": "bounded engineering support measurement, not a production approval",
                 "provenance": "Docs/evidence/m08-runtime-contract.md approved protocol"}
        policy += "\n[[tool.pyalamode.integration_approvals]]\n"
        policy += "".join(key + " = " + json.dumps(value) + "\n" for key, value in entry.items())
    return policy


def checked_build(directory, mode):
    name = "m08_workload_" + mode
    project = directory / name
    project.mkdir()
    source = project / (name + ".py")
    source.write_text(FIXTURE)
    policy = fixture_policy(project, name, mode)
    (project / "pyproject.toml").write_text(policy)
    output = project / "artifact"
    report = build_paths([source], root=project, output=output)
    if report.status:
        messages = [item.format() for result in report.results for item in result.diagnostics]
        messages += [item.format() for item in report.tooling]
        raise RuntimeError("integration benchmark fixture build failed:\n" + "\n".join(messages))
    if mode != "debug":
        assert (output / source.name).read_bytes() == FIXTURE.encode(), "authored source changed"
    contracts = [contract for result in report.results for contract in result.contracts]
    assert {contract.name for contract in contracts} == set(SELECTED)
    assert all(contract.external_assumptions for contract in contracts), "external trust disappeared"
    assert all(not contract.required_effects for contract in contracts), "approved invocation effect changed"
    assert all("ValueError" in contract.failures for contract in contracts)
    assert all(not result.module_mode and result.initialization_evidence == "unchecked ordinary module initialization"
               for result in report.results)
    setup = [row for result in report.results for row in result.setup_observations]
    assert any(row["identity"] == "pyalamode.integrations import" for row in setup), "ordinary setup disappeared"
    evidence = json.loads((output / "pyalamode-evidence.json").read_text())
    details = {
        "mode": mode, "module": name, "fixture_sha256": hashlib.sha256(FIXTURE.encode()).hexdigest(),
        "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
        "artifact_files_sha256": evidence["artifact_files"], "guarded_exports": report.guarded_exports,
        "debug_coverage": report.debug_coverage,
        "actual_off_or_exports_original_source_unchanged": mode != "debug",
        "contracts": [contract.__dict__ for contract in contracts],
        "file_initialization": [{"module_mode": result.module_mode,
                                 "initialization_evidence": result.initialization_evidence,
                                 "setup_observations": result.setup_observations} for result in report.results],
        "integration_catalog": report.to_dict()["integration_catalog"],
        "integration_approvals": report.to_dict()["integration_approvals"],
        "checked_runtime_environment": report.to_dict()["runtime_environment"],
    }
    return output, details


def clear_facades():
    for name in tuple(sys.modules):
        if name == "pyalamode_exports" or name.startswith("pyalamode_exports."):
            del sys.modules[name]


def import_mode(output, name, mode):
    clear_facades()
    sys.path.insert(0, str(output))
    original = importlib.import_module(name)
    selected = original if mode == "off" else importlib.import_module("pyalamode_exports." + name)
    assert original.encode_payload.__code__.co_filename == str(output / (name + ".py"))
    if mode != "off":
        assert all(getattr(selected, function).__wrapped__ is getattr(original, function) for function in SELECTED)
    return original, selected


def prepare(selected, condition, size):
    payload = (bytes(range(256)) * ((size + 255) // 256))[:size]
    encoded = binascii.b2a_base64(payload, newline=False)
    digest = hashlib.sha256(payload).digest()
    work = {"payload_bytes": size, "encoded_bytes": len(encoded), "sha256_result_bytes": 32}
    if condition == "encode":
        function, arguments, expected = selected.encode_payload, (payload,), encoded
        work.update({"adapter_encode_calls": 1, "native_base64_encode_calls": 1})
    elif condition == "decode":
        function, arguments, expected = selected.decode_payload, (encoded,), payload
        work.update({"adapter_decode_calls": 1, "native_base64_decode_calls": 1,
                     "native_canonical_reencode_calls": 1, "encoded_input_bytes": len(encoded)})
    elif condition == "digest":
        function, arguments, expected = selected.content_digest, (payload,), digest
        work.update({"adapter_digest_calls": 1, "private_native_sha256_state": 1,
                     "native_sha256_digest_calls": 1})
    else:
        function, arguments, expected = selected.transport_digest, (payload,), (encoded, digest)
        work.update({"adapter_encode_decode_digest_calls_each": 1,
                     "native_base64_encode_calls_including_canonical_check": 2,
                     "native_base64_decode_calls": 1, "private_native_sha256_state": 1})
    def verify(result):
        if condition == "transport_digest":
            return type(result) is tuple and len(result) == 2 and all(type(value) is bytes for value in result) and result == expected
        return type(result) is bytes and result == expected
    return function, arguments, verify, work


def repeat(function, arguments, calls):
    result = None
    for _ in range(calls):
        result = function(*arguments)
    return result


def build_and_smoke(directory, sizes=(32, 4096)):
    """Untimed actual artifacts, exact assertions, trust and setup evidence."""
    modes = []
    native_validate = boundaries.validate_data
    counter = []
    def observe(value, schema, *, path="value"):
        counter.append(path)
        return native_validate(value, schema, path=path)
    boundaries.validate_data = observe
    try:
        for mode in ("off", "exports", "debug"):
            output, details = checked_build(directory, mode)
            original, selected = import_mode(output, details["module"], mode)
            counts = {}
            for condition in CONDITIONS:
                counts[condition] = {}
                for size in sizes:
                    function, arguments, verify, _ = prepare(selected, condition, size)
                    counter.clear()
                    assert verify(function(*arguments)), (mode, condition, size)
                    expected_count = 0 if mode == "off" else 2 if mode == "exports" else 6 if condition == "transport_digest" else 4
                    assert len(counter) == expected_count, (mode, condition, size, len(counter), expected_count)
                    counts[condition][str(size)] = {"deep_assertion_calls_per_invocation": len(counter),
                                                   "paths": list(counter)}
            if mode == "off":
                assert all(row["deep_assertion_calls_per_invocation"] == 0
                           for per_size in counts.values() for row in per_size.values())
            details["instrumented_guard_calls"] = counts
            modes.append((original, selected, details, output))
    finally:
        boundaries.validate_data = native_validate
        for original, selected, _, _ in modes:
            for module in (original, selected):
                for name, value in tuple(module.__dict__.items()):
                    if value is observe:
                        module.__dict__[name] = native_validate
    for original, selected, details, _ in modes:
        for condition in CONDITIONS:
            function, arguments, verify, _ = prepare(selected, condition, 0)
            assert verify(function(*arguments)), (details["mode"], "empty", condition)
        try:
            selected.decode_payload(b"Zh==")
        except ValueError as error:
            assert type(error) is ValueError and error.__context__ is None and error.__cause__ is None
        else:
            raise AssertionError("noncanonical input escaped actual artifact")
        if details["mode"] != "off":
            try:
                selected.encode_payload(bytearray(b"data"))
            except TypeError:
                pass
            else:
                raise AssertionError("selected export did not refuse mutable input")
    return modes


def cleanup(modes):
    for _, _, details, output in modes:
        sys.modules.pop(details["module"], None)
        if str(output) in sys.path:
            sys.path.remove(str(output))
    clear_facades()


def benchmark(sizes, trials, calls):
    before = source_snapshot()
    rows = []
    with tempfile.TemporaryDirectory(prefix="pyalamode-m08-benchmark-") as temporary:
        modes = build_and_smoke(Path(temporary), sizes)
        try:
            for original, selected, details, _ in modes:
                for condition in CONDITIONS:
                    for size in sizes:
                        function, arguments, verify, work = prepare(selected, condition, size)
                        assert verify(repeat(function, arguments, WARMUP_CALLS))
                        observations = []
                        for _ in range(trials):
                            result, measured = _measure(lambda: repeat(function, arguments, calls))
                            assert verify(result), (details["mode"], condition, size)
                            observations.append(measured)
                        rows.append({"mode": details["mode"], "condition": condition, "size": size,
                                     "workload": work, "warmup_calls": WARMUP_CALLS,
                                     "actual_guard_calls_per_invocation": details["instrumented_guard_calls"][condition][str(size)],
                                     "observations": observations,
                                     "median_seconds_per_call": statistics.median(row["elapsed_seconds"] for row in observations) / calls,
                                     "median_traced_peak_bytes": statistics.median(row["traced_peak_bytes"] for row in observations),
                                     "correctness_passed": True})
        finally:
            cleanup(modes)
    after = source_snapshot()
    assert before == after, "source/dependency identities changed during measurements"
    return {"schema": "pyalamode-m08-measurements-v1", "environment": {**environment(), **runtime_environment()},
            "workload_sizes": list(sizes), "trials": trials, "calls_per_trial": calls,
            "built_artifacts": [details for _, _, details, _ in modes], "measurements": rows,
            "source_identity_before": before, "source_identity_after": after,
            "measurement_scope": {
                "build_import_backend_setup_inputs_approval_guard_count_warmup_correctness_hash_json_outside_intervals": True,
                "tracemalloc_included": True, "allocation_is_python_traced_not_rss": True,
                "native_hacl_allocations_may_be_untraced": True, "gc_collect_before_each_interval": True,
                "retained_history": "last result only; transient disposal included",
                "cache_policy": "three modules and both native backends preloaded, warm process; OS caches uncontrolled",
                "system_load_controlled": False, "guard_counts": "each exact measured condition/size counted untimed",
                "approval_scope": "explicit root-authorized temporary benchmark fixtures only; no production approval"}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[32, 4096])
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--calls", type=int, default=25)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--untimed-smoke", action="store_true")
    args = parser.parse_args()
    target_gate()
    if runtime_environment()["filesystem_encoding"] != "utf-8" or runtime_environment()["filesystem_errors"] != "surrogateescape":
        raise SystemExit("benchmark requires UTF-8/surrogateescape filesystem configuration")
    if any(size < 0 or size > 1_048_576 for size in args.sizes) or args.trials < 1 or args.calls < 1:
        raise SystemExit("invalid bounded sizes/trials/calls")
    if args.untimed_smoke:
        before = source_snapshot()
        with tempfile.TemporaryDirectory(prefix="pyalamode-m08-smoke-") as temporary:
            modes = build_and_smoke(Path(temporary), args.sizes)
            try:
                result = {"schema": "pyalamode-m08-untimed-smoke-v1",
                          "environment": {**environment(), **runtime_environment()},
                          "built_artifacts": [details for _, _, details, _ in modes],
                          "source_identity_before": before, "source_identity_after": source_snapshot(),
                          "intervals": 0, "scope": "untimed artifact correctness/trust/setup/guard-count smoke"}
                assert result["source_identity_before"] == result["source_identity_after"]
            finally:
                cleanup(modes)
    else:
        result = benchmark(args.sizes, args.trials, args.calls)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
