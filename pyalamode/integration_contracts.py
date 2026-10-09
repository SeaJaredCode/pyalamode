"""Static external candidates and nonexecuting installed-byte approval discovery.

This module never imports the adapter or either native backend. These dictionaries
are detached check/build evidence, not a runtime callable registry.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import _imp

INTEGRATION_VERSION = "pyalamode.integrations-v1"
INTEGRATION_NAMES = frozenset({"base64_encode", "base64_decode", "sha256_digest"})
INTEGRATION_FOUNDATIONS = {
    "builtins": frozenset({"type", "bytes", "len", "TypeError", "ValueError", "BaseException", "Exception"}),
    "binascii": frozenset({"b2a_base64", "a2b_base64", "Error"}),
    "_sha2": frozenset({"sha256", "SHA256Type"}),
    # Importer/module-table changes undermine the installed-file resolution.
    "sys": frozenset({"modules", "path", "meta_path", "path_hooks", "path_importer_cache", "base_prefix", "abiflags", "version", "version_info", "implementation", "executable", "platform"}),
    "_imp": frozenset({"extension_suffixes"}),
    "importlib": frozenset({"import_module", "util", "machinery"}),
    "importlib.util": frozenset({"find_spec", "module_from_spec"}),
    "importlib.machinery": frozenset({"PathFinder", "FileFinder", "ExtensionFileLoader", "SourceFileLoader", "BuiltinImporter", "FrozenImporter"}),
}
FAMILIES = frozenset({"IO", "State", "Clock", "Random", "Environment"})
FAILURES = frozenset({"ZeroDivisionError", "IndexError", "KeyError", "ValueError", "RecursionError", "RuntimeError", "OSError", "UnicodeError"})
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_EXPIRY = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _text(value):
    return type(value) is str and bool(value.strip())


def _name(name):
    if type(name) is not str:
        return None
    for prefix in ("pyalamode.integrations.", "integrations."):
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name if name in INTEGRATION_NAMES else None


def operation_contract(name):
    """Return an unapproved detached finite candidate; never import its implementation."""
    name = _name(name)
    if name is None:
        return None
    backend = "_sha2" if name == "sha256_digest" else "binascii"
    operations = ["_sha2.sha256(data,usedforsecurity=False)", "_sha2.SHA256Type.digest"] if backend == "_sha2" else ["binascii.b2a_base64(data,newline=False)"] if name == "base64_encode" else ["binascii.a2b_base64(data,strict_mode=True)", "binascii.Error exact construction", "binascii.b2a_base64(decoded,newline=False)"]
    behavior = {
        "base64_encode": "canonical padded standard ASCII Base64 without newline; empty bytes gives empty bytes; input <=1048576 bytes",
        "base64_decode": "strict native decode then fixed re-encode equality; canonical padding and zero unused pad bits; encoded <=1398104 and decoded <=1048576 bytes; empty bytes allowed",
        "sha256_digest": "fixed raw 32-byte SHA256 digest using private fresh CPython HACL state; input <=1048576 bytes; no OpenSSL/provider selection",
    }[name]
    return {"identity": "pyalamode.integrations." + name, "version": INTEGRATION_VERSION,
            "runtime": "CPython 3.13.1 standard GIL macOS/Linux UTF8/surrogateescape",
            "signature": "(data:bytes,/)->bytes", "inputs": ["bytes"], "output": "bytes",
            "behavior": behavior, "effects": [], "failures": ["ValueError"],
            "ordinary_invalid_inputs": ["TypeError"], "native_operations": operations, "invocation_backend": backend,
            "implicit_dispatch": "exact bytes native buffer/length/equality; fixed native exception construction; private SHA256 HACL allocation/update/digest/free; no foreign hooks, codec registries, restoration or callbacks",
            "aliases": "immutable input only; immutable output; private native buffers/hash state never escape; no retained mutable aliases or live views",
            "delayed_execution": "none; eager completing invocation", "capabilities": [],
            "initialization": {"effects": ["IO"], "failures": ["ImportError", "OSError"],
                "evidence": "ordinary adapter import and both native loaders; surrounding application initialization unchecked",
                "policy": "ordinary setup only; functional initialization/defaults cannot import/invoke integrations",
                "setup_backends": ["binascii", "_sha2"],
                "native_foundations": "CPython/native loader/libc or libSystem; binascii linked zlib is setup trust and unused by selected Base64 invocation"},
            "foundations": [module + "." + member for module, members in sorted(INTEGRATION_FOUNDATIONS.items()) for member in sorted(members)] + ["pyalamode.integrations._exact_bytes/_MAX_BYTES/_MAX_BASE64_BYTES/_binascii/_sha2 shared defining globals", "binascii.Error __new__/__init__/bases/dictionary and inherited native exception behavior"],
            "evidence": "opaque installed external native implementation plus characterized product adapter; approval is an explicit assumption, not checked backend source",
            "owner": "Pyalamode integration catalog", "rationale": "bounded immutable payload transport and content digest",
            "provenance": {"kind": "product-shipped candidate", "source": "pyalamode/integration_contracts.py", "status": "reviewed"},
            "approval": "denied by default; exact project operation/contract/installed identity approval required"}


def operation_catalog():
    return [operation_contract(name) for name in sorted(INTEGRATION_NAMES)]


def validate_policy(policy):
    """Validate only the new closed policy fields; inherited fields belong to project.py."""
    trust = policy.get("external_trust", "deny")
    if type(trust) is not str or trust not in {"deny", "approved"}:
        return "external_trust must be deny or approved"
    paths = policy.get("integration_manifests", [])
    if type(paths) is not list or any(type(p) is not str or not p or Path(p).is_absolute() or ".." in Path(p).parts or "\\" in p for p in paths) or len(paths) != len(set(paths)):
        return "integration_manifests must list unique project-relative JSON paths"
    approvals = policy.get("integration_approvals", [])
    if type(approvals) is not list:
        return "integration_approvals must be an array of exact operation approval tables"
    seen = set()
    for entry in approvals:
        required = {"operation", "contract_sha256", "dependency_sha256", "owner", "rationale", "provenance"}
        if type(entry) is not dict or not required <= entry.keys() or entry.keys() - required - {"expires_at"}:
            return "integration approval requires exact operation, contract_sha256, dependency_sha256, owner, rationale, provenance and optional expires_at"
        name = _name(entry.get("operation", "")) if type(entry.get("operation")) is str else None
        if name is None or entry["operation"] != "pyalamode.integrations." + name or name in seen:
            return "integration approvals require unique canonical catalog operation identities"
        seen.add(name)
        if any(not _text(entry[key]) for key in ("owner", "rationale", "provenance")) or any(type(entry[key]) is not str or _DIGEST.fullmatch(entry[key]) is None for key in ("contract_sha256", "dependency_sha256")):
            return "integration approval digests must be lowercase SHA256 and owner/rationale/provenance nonempty text"
        if "expires_at" in entry:
            try:
                if type(entry["expires_at"]) is not str or not _EXPIRY.fullmatch(entry["expires_at"]):
                    raise ValueError
                datetime.strptime(entry["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                return "integration expires_at must be a valid explicit UTC YYYY-MM-DDTHH:MM:SSZ string"
    return None


def _artifact(path):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("installed artifact is not a regular file: " + str(path))
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _installed(root):
    """Inspect closed filesystem candidates, never find_spec/entrypoints/import hooks."""
    if sys.implementation.name != "cpython" or tuple(sys.version_info[:3]) != (3, 13, 1) or sys.platform not in {"darwin", "linux"} or "t" in sys.abiflags:
        raise ValueError("integration identity requires the supported CPython3.13.1 standard GIL target")
    directory = (Path(sys.base_prefix) / "lib" / "python3.13" / "lib-dynload").resolve(strict=True)
    suffixes = _imp.extension_suffixes()
    if type(suffixes) is not list or not suffixes or any(type(value) is not str for value in suffixes):
        raise ValueError("unsupported native extension suffix inventory")
    suffix = suffixes[0]
    if type(suffix) is not str or not suffix.endswith((".so", ".pyd")):
        raise ValueError("unsupported native extension suffix")
    artifacts = {name: _artifact(directory / (name + suffix)) for name in ("binascii", "_sha2")}
    # Inspect ordinary candidate precedence conservatively, including the project
    # root even when a check was launched from a different cwd. No finder runs.
    inspected = []
    for raw in [str(root), *sys.path]:
        if type(raw) is not str:
            raise ValueError("unsupported non-string import path")
        candidate = Path(raw or Path.cwd()).resolve()
        if str(candidate) in inspected:
            continue
        inspected.append(str(candidate))
        if candidate.is_file():
            raise ValueError("unsupported existing archive/custom import path: " + str(candidate))
        if not candidate.is_dir():
            continue
        for path in [candidate / "pyalamode", *(candidate / ("pyalamode" + ending) for ending in (suffix, ".so", ".py", ".pyc"))]:
            importable = path.is_dir() if path.name == "pyalamode" else path.is_file()
            if importable and path.resolve() != Path(__file__).resolve().parent:
                raise ValueError("installed product adapter is shadowed by " + str(path))
        for name in artifacts:
            possible = [candidate / (name + ending) for ending in (suffix, ".abi3.so", ".so", ".py", ".pyc")]
            possible.append(candidate / name)
            for path in possible:
                importable = path.is_dir() if path.name == name else path.is_file()
                if importable and path.resolve() != Path(artifacts[name]["path"]):
                    raise ValueError("installed native operation is shadowed by " + str(path))
    executable = _artifact(sys.executable)
    if sys.platform == "darwin":
        core_path = Path(sys.base_prefix) / "Python"
    else:
        core_path = Path(sys.base_prefix) / "lib" / "libpython3.13.so.1.0"
    core = _artifact(core_path)
    adapter = _artifact(Path(__file__).resolve().with_name("integrations.py"))
    return {"distribution": "CPython-stdlib", "version": ".".join(str(n) for n in sys.version_info[:3]),
            "build": sys.version, "cache_tag": sys.implementation.cache_tag, "platform": sys.platform,
            "base_prefix": str(Path(sys.base_prefix).resolve()), "abiflags": sys.abiflags,
            "extension_suffixes": list(suffixes),
            "native_artifacts": artifacts, "adapter_artifact": adapter, "interpreter_executable": executable,
            "interpreter_core": core,
            "resolution": "fixed sys.base_prefix/lib/python3.13/lib-dynload and builtin _imp extension suffix; no sysconfig getters/config-data imports or environment selectors; visible filesystem shadows refused; ordinary importer/module bindings must remain unchanged at execution",
            "native_setup_trust": "platform loader/libc or libSystem and binascii linked zlib remain disclosed foundation assumptions; selected invocation does not use zlib"}


def integration_snapshot(policy=None, root=None, now=None):
    """Detached candidates/approvals/freshness inputs; inspect only bytes and policy."""
    policy, root = policy or {}, Path(root or Path.cwd()).resolve()
    errors = []
    error = validate_policy(policy)
    if error:
        errors.append(error)
    candidates = {row["identity"]: row for row in operation_catalog()}
    overrides = set()
    if not errors:
        for relative in policy.get("integration_manifests", []):
            try:
                path = (root / relative).resolve(strict=True)
                if not path.is_relative_to(root):
                    raise ValueError("manifest resolves outside project")
                raw = path.read_bytes()
                row = json.loads(raw)
                fields = {"schema", "operation", "status", "base_contract_sha256", "effects", "failures", "owner", "rationale", "provenance"}
                if type(row) is not dict or row.keys() != fields or type(row["schema"]) is not int or row["schema"] != 1 or row["operation"] not in candidates or row["operation"] in overrides:
                    raise ValueError("manifest requires exact schema1 fields and one unique catalog operation")
                base = candidates[row["operation"]]
                if row["status"] not in {"draft", "reviewed"} or row["base_contract_sha256"] != _digest(base):
                    raise ValueError("manifest status/base contract identity is invalid or stale")
                for key, allowed in (("effects", FAMILIES), ("failures", FAILURES)):
                    values = row[key]
                    if type(values) is not list or any(type(v) is not str or v not in allowed for v in values) or len(values) != len(set(values)) or not set(base[key]) <= set(values):
                        raise ValueError("manifest cannot remove baseline " + key + " or introduce unknown behavior")
                if any(not _text(row[key]) for key in ("owner", "rationale", "provenance")):
                    raise ValueError("manifest review text must be nonempty")
                overrides.add(row["operation"])
                base.update({"effects": sorted(row["effects"]), "failures": sorted(row["failures"]), "owner": row["owner"], "rationale": row["rationale"],
                    "provenance": {"kind": "project-local conservative override", "path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "status": row["status"], "review": row["provenance"], "base_contract_sha256": row["base_contract_sha256"]}})
            except (OSError, ValueError, TypeError, KeyError, UnicodeError) as error:
                errors.append("cannot accept integration manifest " + relative + ": " + str(error))
    try:
        installed = _installed(root)
        installed_error = None
    except (OSError, ValueError, TypeError) as error:
        installed, installed_error = None, "installed integration identity unavailable: " + str(error)
    now = now or datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset().total_seconds() != 0:
        raise ValueError("integration snapshot now requires an explicit UTC datetime")
    approvals = {entry["operation"]: entry for entry in policy.get("integration_approvals", [])} if not errors else {}
    catalog, inputs, states = [], {}, []
    for operation, row in sorted(candidates.items()):
        contract_digest = _digest(row)
        identity = copy.deepcopy(installed)
        if identity:
            identity.update({"operation": operation, "invocation_backend": row["invocation_backend"], "native_operations": list(row["native_operations"])})
        dependency_digest = _digest(identity) if identity else None
        approval = copy.deepcopy(approvals.get(operation))
        status = "denied" if policy.get("external_trust", "deny") == "deny" else "missing"
        if errors:
            status = "invalid policy"
        elif installed_error:
            status = "unresolved"
        elif row["provenance"]["status"] == "draft":
            status = "draft"
        elif approval:
            expired = "expires_at" in approval and now >= datetime.strptime(approval["expires_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            stale = approval["contract_sha256"] != contract_digest or approval["dependency_sha256"] != dependency_digest
            status = "expired" if expired else "stale" if stale else "approved" if policy.get("external_trust", "deny") == "approved" else "denied"
        freshness = {"contract_sha256": contract_digest, "dependency_sha256": dependency_digest, "admission": status,
                     "approval": approval, "identity_error": installed_error}
        inputs[operation] = freshness
        row.update({**freshness, "installed_identity": identity})
        catalog.append(row)
        if approval:
            states.append({**approval, "status": status, "expiry": approval.get("expires_at", "nonexpiring")})
    return {"catalog": catalog, "approvals": states, "inputs": inputs, "errors": errors}
