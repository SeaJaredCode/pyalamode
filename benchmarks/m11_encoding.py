"""Unrun shared stable_invoice_encoding_v1 controller; explicit release required.

ONE Invoice, n canonical labels; 8/256 x encode/decode x off/exports/debug.
Setup/build/install/import/oracles/counts/checks/hashes are untimed. The timed
loop retains its final result only; allocations/disposal/tracing are included.
The fixed independent wire oracle never invokes or introspects a product codec.
"""

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc

PROTOCOL = "stable_invoice_encoding_v1"
SIZES = (8, 256)
MODES = ("off", "exports", "debug")
CONDITIONS = ("encode", "decode")
WARMUPS = 10
INTERVALS = 3
CALLS = 25
FIXTURE = '''# mode: fun
from pyalamode import record,oneof,case,Map,value_encode,value_decode

@oneof
class InvoiceStatus:
    @case
    class Ready:
        pass
    @case
    class Rejected:
        reason:str

@record
class Invoice:
    order_id:str
    total_cents:int
    labels:Map[str,str]
    status:InvoiceStatus

def encode_invoice(value:Invoice)->bytes:
    return value_encode(value,Invoice)

def decode_invoice(data:bytes)->Invoice:
    return value_decode(data,Invoice)
'''
SELECTED = ("checked_pricing.core:encode_invoice", "checked_pricing.core:decode_invoice")


def _u32(value):
    return bytes(((value >> 24) & 255, (value >> 16) & 255, (value >> 8) & 255, value & 255))


def _text(value):
    return _u32(len(value)) + b"".join(_u32(ord(character)) for character in value)


def _label(prefix, index):
    # Fixed 0..255 index oracle, no candidate integer formatter.
    digits = "0123456789"
    return prefix + digits[index // 100] + digits[(index // 10) % 10] + digits[index % 10]


def literal_schema():
    """Independent literal grammar for exactly the fixed Invoice schema."""
    status = (b"\x21" + _text("checked_pricing.core:InvoiceStatus") + _u32(2)
              + _text("Ready") + _u32(0)
              + _text("Rejected") + _u32(1) + _text("reason") + b"\x03")
    schema = (b"\x20" + _text("checked_pricing.core:Invoice") + _u32(4)
              + _text("order_id") + b"\x03"
              + _text("total_cents") + b"\x02"
              + _text("labels") + b"\x14\x03\x03"
              + _text("status") + status)
    assert len(schema) == 508  # hand-derived before candidate observations
    return schema


def literal_invoice(size):
    """Independent fixed payload; never generated from measured encode output."""
    if size not in SIZES:
        raise ValueError("fixed Invoice oracle supports only 8/256 labels")
    schema = literal_schema()
    labels = b"\x14" + _u32(size)
    labels += b"".join(b"\x03" + _text(_label("k", index)) + b"\x03" + _text(_label("v", index))
                       for index in range(size))
    body = (b"\x20" + _u32(4) + b"\x03" + _text("order-41")
            + bytes.fromhex("020000000000000513") + labels
            + b"\x21" + _u32(0) + _u32(0))
    packet = b"PALV\x01" + _u32(508) + schema + body
    assert len(body) == 65 + 42 * size
    assert len(packet) == (918 if size == 8 else 11334)
    return packet


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def controller_identity():
    return {"path": str(Path(__file__).absolute()), "sha256": sha(__file__), "bytes": Path(__file__).stat().st_size}


def source_snapshot():
    from pyalamode.model import foundation_identities
    import pyalamode
    package = Path(pyalamode.__file__).absolute().parent
    root = Path(__file__).absolute().parent.parent
    owned = ("pyalamode/encoding.py", "pyalamode/encoding_contracts.py", "tests/m11_encoding.py", "benchmarks/m11_encoding.py")
    return {"product_artifacts": foundation_identities(),
            "full_parent_package": {path.name: sha(path) for path in sorted(package.glob("*.py"))},
            "owned_source_inputs": {name: sha(root / name) for name in owned}}


def target_gate():
    if sys.implementation.name != "cpython" or tuple(sys.version_info[:3]) != (3, 13, 1):
        raise RuntimeError("controller requires exact CPython 3.13.1")
    if sys.platform not in {"darwin", "linux"} or platform.machine() not in {"arm64", "aarch64"}:
        raise RuntimeError("controller requires supported macOS arm64/Linux aarch64")
    if not sys._is_gil_enabled() or sys.getfilesystemencoding() != "utf-8" or sys.getfilesystemencodeerrors() != "surrogateescape":
        raise RuntimeError("controller requires standard GIL and UTF8/surrogateescape")


def environment():
    return {"executable_literal": sys.executable, "executable_resolved_observation_only": str(Path(sys.executable).resolve()),
            "base_executable": sys._base_executable, "prefix": sys.prefix, "base_prefix": sys.base_prefix,
            "implementation": sys.implementation.name, "version": sys.version, "cache_tag": sys.implementation.cache_tag,
            "abiflags": sys.abiflags, "gil_enabled": sys._is_gil_enabled(), "platform": platform.platform(),
            "machine": platform.machine(), "python_build": platform.python_build(), "python_compiler": platform.python_compiler(),
            "processor": platform.processor(), "logical_cpus": os.cpu_count(), "sys_flags": repr(sys.flags),
            "filesystem_encoding": sys.getfilesystemencoding(), "filesystem_errors": sys.getfilesystemencodeerrors(),
            "utf8_mode": sys.flags.utf8_mode, "hash_seed_environment": os.environ.get("PYTHONHASHSEED"),
            "system_load_controlled": False, "os_caches_controlled": False}


def policy(mode):
    source = '[tool.pyalamode]\nschema=1\nboundary_guards=' + json.dumps(mode) + "\n"
    if mode != "off":
        source += "guarded_exports=" + json.dumps(list(SELECTED)) + "\n"
    return source + '''\n[tool.pyalamode.distribution]
schema=1
name="m11-encoding-fixture"
version="1.0.0"
packages=["checked_pricing"]
exports=["checked_pricing.core:Invoice","checked_pricing.core:InvoiceStatus","checked_pricing.core:encode_invoice","checked_pricing.core:decode_invoice"]
'''


def command(argv, directory, label):
    observed = subprocess.run(argv, cwd=directory, capture_output=True)
    raw = Path(directory) / (label + ".stdout")
    raw.write_bytes(observed.stdout)
    errors = Path(directory) / (label + ".stderr")
    errors.write_bytes(observed.stderr)
    receipt = {"argv": argv, "cwd": str(directory), "status": observed.returncode,
               "stdout": {"path": str(raw), "sha256": sha(raw), "bytes": raw.stat().st_size},
               "stderr": {"path": str(errors), "sha256": sha(errors), "bytes": errors.stat().st_size}}
    if observed.returncode:
        raise RuntimeError("untimed fixture command failed: " + json.dumps(receipt))
    return receipt


def prepare(directory, mode, product_wheel):
    producer = directory / "producer"
    producer.mkdir()
    package = producer / "checked_pricing"
    package.mkdir()
    (package / "__init__.py").write_text('# mode: fun\n', encoding="utf-8")
    (package / "core.py").write_text(FIXTURE, encoding="utf-8")
    (producer / "pyproject.toml").write_text(policy(mode), encoding="utf-8")
    wheel = directory / "m11_encoding_fixture-1.0.0-py3-none-any.whl"
    build = command([sys.executable, "-I", "-m", "pyalamode", "build", "--wheel", "--root", str(producer),
                     "--output", str(wheel), "--json"], directory, "build")
    assert wheel.is_file()
    virtualenv = directory / "installed"
    create = command([sys.executable, "-I", "-m", "venv", "--without-pip", str(virtualenv)], directory, "venv")
    python = virtualenv / "bin" / "python"  # literal venv path, never resolved for invocation
    install = command([sys.executable, "-I", "-m", "pip", "--python", str(python), "install", "--no-index", "--no-deps", "--no-compile",
                       str(product_wheel), str(wheel)], directory, "install")
    return python, {"mode": mode, "producer_sources": {str(path.relative_to(producer)): sha(path)
                                                       for path in sorted(producer.rglob("*")) if path.is_file()},
                    "fixture_wheel": {"path": str(wheel), "sha256": sha(wheel), "bytes": wheel.stat().st_size},
                    "product_wheel": {"path": str(product_wheel), "sha256": sha(product_wheel), "bytes": product_wheel.stat().st_size},
                    "untimed_commands": [build, create, install]}


def installed_snapshot():
    from pyalamode.model import foundation_identities
    import pyalamode
    import checked_pricing.core as core
    product = Path(pyalamode.__file__).absolute().parent
    source = Path(core.__file__).absolute()
    prefix = Path(sys.prefix).absolute()
    assert product.is_relative_to(prefix) and source.is_relative_to(prefix), "physical product/fixture must be installed"
    return {"product_path": str(product), "fixture_source_path": str(source),
            "product_artifacts": foundation_identities(),
            "full_installed_package": {path.name: sha(path) for path in sorted(product.glob("*.py"))},
            "fixture_source_sha256": sha(source), "controller": controller_identity()}


def check_invoice(value, original, size):
    from pyalamode import Map, Vector
    assert type(value) is original.Invoice and type(value.status) is original.InvoiceStatus.Ready
    assert type(value.order_id) is str and value.order_id == "order-41"
    assert type(value.total_cents) is int and value.total_cents == 1299
    assert type(value.labels) is Map
    expected = Vector.of(*((_label("k", index), _label("v", index)) for index in range(size)))
    assert value.labels.ordered_entries() == expected


def repeat(function, argument, count):
    result = None
    for _ in range(count):
        result = function(argument)
    return result


def worker(mode, measure):
    target_gate()
    from pyalamode import boundaries, Map
    native = boundaries.validate_data
    counts = []
    def observe(value, schema, *, path="value"):
        counts.append(path)
        return native(value, schema, path=path)
    # Untimed temporary counting, then every imported alias is restored to the
    # actual native function before warmups/intervals.
    boundaries.validate_data = observe
    try:
        original = importlib.import_module("checked_pricing.core")
        selected = original if mode == "off" else importlib.import_module("checked_pricing._pyalamode_exports.core")
        rows = []
        prepared = []
        for size in SIZES:
            invoice = original.Invoice("order-41", 1299,
                                       Map.of(*((_label("k", index), _label("v", index)) for index in range(size))),
                                       original.InvoiceStatus.Ready())
            literal = literal_invoice(size)
            for condition in CONDITIONS:
                function = selected.encode_invoice if condition == "encode" else selected.decode_invoice
                argument = invoice if condition == "encode" else literal
                counts.clear()
                answer = function(argument)
                if condition == "encode":
                    assert type(answer) is bytes and answer == literal
                else:
                    check_invoice(answer, original, size)
                expected_count = 0 if mode == "off" else 2 if mode == "exports" else 4
                assert len(counts) == expected_count, (mode, condition, size, len(counts), expected_count)
                prepared.append((size, condition, function, argument, literal,
                                 {"calls": len(counts), "paths": list(counts)}))
    finally:
        boundaries.validate_data = native
        for module in (locals().get("original"), locals().get("selected")):
            if module is not None:
                for name, value in tuple(module.__dict__.items()):
                    if value is observe:
                        module.__dict__[name] = native
    before = installed_snapshot()
    for size, condition, function, argument, literal, guard in prepared:
        def verify(answer):
            if condition == "encode":
                assert type(answer) is bytes and answer == literal
            else:
                check_invoice(answer, original, size)
        verify(repeat(function, argument, WARMUPS))
        observations = []
        if measure:
            for _ in range(INTERVALS):
                tracemalloc.start()
                tracemalloc.reset_peak()
                baseline = tracemalloc.get_traced_memory()[0]
                started = time.perf_counter()
                answer = repeat(function, argument, CALLS)
                elapsed = time.perf_counter() - started
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                verify(answer)
                observations.append({"calls": CALLS, "elapsed_seconds": elapsed,
                                     "traced_current_delta_bytes": current - baseline,
                                     "traced_peak_delta_bytes": peak - baseline})
        row = {"mode": mode, "condition": condition, "labels": size, "schema_bytes": 508,
               "schema_nodes": 8, "schema_depth": 2, "value_nodes": 5 + 2 * size, "value_depth": 2,
               "wire_bytes": len(literal), "independent_literal_sha256": hashlib.sha256(literal).hexdigest(),
               "independent_literal_hex": literal.hex(), "guard_counts_untimed": guard,
               "warmups": WARMUPS, "observations": observations, "correctness_passed": True}
        if measure:
            row["median_seconds_per_call"] = statistics.median(item["elapsed_seconds"] for item in observations) / CALLS
            row["median_traced_peak_delta_bytes"] = statistics.median(item["traced_peak_delta_bytes"] for item in observations)
        rows.append(row)
    after = installed_snapshot()
    assert before == after, "installed/controller inputs changed"
    return {"protocol": PROTOCOL, "environment": environment(), "mode": mode, "measurements": rows,
            "identity_before": before, "identity_after": after, "intervals_authorized": measure}


def protocol_description():
    return {"protocol": PROTOCOL, "sizes": list(SIZES), "modes": list(MODES), "conditions": list(CONDITIONS),
            "rows_per_platform": 12, "intervals_per_platform": 36, "calls_per_interval": 25,
            "measured_calls_per_platform": 900, "warmups_per_platform": 120,
            "fixture_sha256": hashlib.sha256(FIXTURE.encode()).hexdigest(), "controller": controller_identity(),
            "literal_oracles": {str(size): {"bytes": len(literal_invoice(size)), "hex": literal_invoice(size).hex(),
                                             "sha256": hashlib.sha256(literal_invoice(size)).hexdigest()} for size in SIZES},
            "scope": {"build_install_import_fixture_oracle_count_warmup_checks_hash_json": "outside intervals",
                      "codec_schema_validation_guards_output_disposal_tracing": "inside intervals",
                      "retention": "final result only", "tracemalloc": "fresh/reset before each timer; fixture outside traced scope; current/peak read after timer; Python traced allocation, not RSS/native total",
                      "system_load_and_os_caches_controlled": False}}


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--describe", action="store_true")
    action.add_argument("--measure", action="store_true")
    action.add_argument("--untimed-smoke", action="store_true")
    parser.add_argument("--worker", choices=MODES)
    parser.add_argument("--product-wheel", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--work-directory", type=Path)
    args = parser.parse_args()
    if args.describe:
        result = protocol_description()  # independent oracle only, no product import
    elif args.worker:
        result = worker(args.worker, args.measure)
    else:
        target_gate()
        if args.product_wheel is None or not args.product_wheel.is_file() or args.work_directory is None:
            parser.error("actual runs require --product-wheel and a fresh --work-directory to preserve all raw evidence")
        directory = args.work_directory.absolute()
        directory.mkdir()  # existing evidence directories are never replaced
        product_wheel = args.product_wheel.absolute()
        before = source_snapshot()
        result = protocol_description()
        result.update({"parent_environment": environment(), "prepared_artifacts": [], "measurements": [], "worker_raw": []})
        for mode in MODES:
            location = directory / mode
            location.mkdir()
            python, setup = prepare(location, mode, product_wheel)
            output = location / "worker.json"
            invocation = [str(python), "-I", str(Path(__file__).absolute()), "--worker", mode,
                          "--measure" if args.measure else "--untimed-smoke", "--output", str(output)]
            receipt = command(invocation, location, "worker")
            observed = json.loads(output.read_text())
            assert observed["protocol"] == PROTOCOL and observed["mode"] == mode
            assert observed["identity_before"]["product_artifacts"] == before["product_artifacts"], "build and installed product inputs differ"
            result["prepared_artifacts"].append(setup)
            result["measurements"].extend(observed["measurements"])
            result["worker_raw"].append({"command": receipt, "json_path": str(output), "json_sha256": sha(output), "json_bytes": output.stat().st_size,
                                         "environment": observed["environment"], "identity_before": observed["identity_before"], "identity_after": observed["identity_after"]})
        assert len(result["measurements"]) == 12
        after = source_snapshot()
        assert before == after, "source/product inputs changed"
        result["source_identity_before"], result["source_identity_after"] = before, after
        result["intervals_authorized"] = args.measure
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
