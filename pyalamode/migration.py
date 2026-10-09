"""Detached migration evidence, conservative debt matching and local reviewed IO.

This module imports no checker, project, editor or application source. Saved
evidence is history; only the main-owned live callback authorizes publication.
"""

from __future__ import annotations

import ast
import copy
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import uuid


MAX_BYTES = 16 * 1024 * 1024
MAX_DEPTH = 64
MAX_NODES = 500_000
MAX_TEXT = 16_384
MAX_AST = 1024 * 1024
MAX_SOURCES = 16_384
MAX_ROWS = 65_536
MAX_LOCATIONS = 262_144
MAX_APPROVALS = 4_096
MAX_CHAIN = 128
IDENTITY_VERSION = "migration-identity-v1"
SOURCE_RULES = frozenset("PAL101 PAL102 PAL110 PAL120 PAL121 PAL130 PAL201 PAL210 PAL211 PAL221 PAL230 PAL240 PAL241 PAL250 PAL310 PAL320 PAL330 PAL340 PAL350 PAL351 PAL370 PAL371 PAL372".split())
EFFECTS = frozenset({"IO", "State", "Clock", "Random", "Environment"})
FAILURES = frozenset({"IndexError", "KeyError", "ValueError", "ZeroDivisionError", "RecursionError", "RuntimeError", "OSError", "UnicodeError"})
OPERATIONS = frozenset("pyalamode.integrations." + name for name in ("base64_encode", "base64_decode", "sha256_digest"))
ADMISSIONS = frozenset({"approved", "missing", "stale", "draft", "denied", "expired", "unresolved"})
CATEGORIES = ("retained_findings", "resolved_findings", "new_findings", "ambiguous_findings", "lost_strict_coverage", "new_trust", "expanded_effects", "expired_approvals", "approval_failures", "unsafe_weakening", "policy_weakening", "inputs_changed")
GATES = {"reject_new_findings": ("new_findings", "PAL360"),
         "reject_lost_strict_coverage": ("lost_strict_coverage", "PAL361"),
         "reject_new_trust": ("new_trust", "PAL362"),
         "reject_expanded_effects": ("expanded_effects", "PAL363"),
         "reject_expired_approvals": ("expired_approvals", "PAL364"),
         "reject_unsafe_weakening": ("unsafe_weakening", "PAL365"),
         "reject_policy_weakening": ("policy_weakening", "PAL367")}
STATE_KEYS = set("schema kind identity_version target runtime_environment edition checker operation_contract snapshot freshness strict_status current_policy_status current_policy_events required_operations inputs scope coverage boundaries findings policy approvals unsafe_adapters".split())
BOUNDARY_KEYS = set("id kind selector path qualified_name signature definition_sha256 selected selection_reasons strict_checked public_export required_export mode source_evidence effect_bound required_effects effect_origins external_assumptions failures guard_coverage location".split())
FINDING_KEYS = set("id identity_key birth_identity rule boundary_id logical_boundary signature context_sha256 context origin count locations review_required".split())
LEGACY_POLICY_KEYS = set("require_modules effect_bounds explicit_cases external_trust integration_manifests integration_approvals required_exports boundary_guards guarded_exports migration".split())
POLICY_KEYS = LEGACY_POLICY_KEYS | {"distribution", "checked_dependencies"}
IDENTITY_KEYS = set("identity_version rule logical_boundary signature context_sha256 origin".split())
APPROVAL_KEYS = set("operation contract_sha256 dependency_sha256 owner rationale provenance".split())
ASSUMPTION_KEYS = set("identity version effects failures initialization provenance approval contract_sha256 dependency_sha256 installed_identity admission source_evidence".split())
INSTALLED_KEYS = set("distribution version build cache_tag platform base_prefix abiflags extension_suffixes native_artifacts adapter_artifact interpreter_executable interpreter_core resolution native_setup_trust operation invocation_backend native_operations".split())
LEGACY_PRODUCTS = frozenset("__init__.py integrations.py integration_contracts.py standard.py standard_contracts.py variants.py failures.py effects.py collections.py records.py boundaries.py guardgen.py model.py checker.py project.py cli.py editor.py migration.py migration_views.py".split())
PRODUCTS = LEGACY_PRODUCTS | {"distribution.py", "encoding.py", "encoding_contracts.py"}
LEGACY_CHECKER = "migration-team-policy-10.0"
LEGACY_OPERATION = "scalar-tuple-call-collection-record-boundary-effect-domain-failure-standard-integration-ops-8"
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")


class MigrationError(ValueError):
    """A bounded tooling refusal, never a clean verification result."""

    def __init__(self, message):
        super().__init__(str(message)[:1024])


def _fail(message):
    raise MigrationError(message)


def _json_value(value):
    """Copy exact bounded JSON types without Python protocol dispatch."""
    nodes = 0

    def visit(item, depth, key=""):
        nonlocal nodes
        nodes += 1
        if nodes > MAX_NODES or depth > MAX_DEPTH:
            _fail("migration JSON exceeds node/depth limit")
        kind = type(item)
        if item is None or kind in (bool, int):
            return item
        if kind is str:
            if len(item) > (MAX_AST if key == "ast" else MAX_TEXT):
                _fail("migration text exceeds supported limit")
            return item
        if kind is list:
            return [visit(child, depth + 1) for child in item]
        if kind is dict:
            if any(type(name) is not str for name in item):
                _fail("migration JSON requires string object keys")
            return {visit(name, depth + 1): visit(child, depth + 1, name) for name, child in item.items()}
        _fail("migration JSON requires exact finite integer/boolean/string/list/object/null values")

    try:
        return visit(value, 0)
    except RecursionError:
        _fail("migration JSON recursion limit exceeded")


def _canonical(value):
    try:
        raw = json.dumps(_json_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
        if len(raw) > MAX_BYTES:
            _fail("migration record exceeds byte limit")
        return raw
    except (ValueError, TypeError, UnicodeError, RecursionError) as error:
        raise MigrationError("cannot encode migration record: " + str(error)) from error


def _hash(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _shape(value, keys, optional=()):
    if type(value) is not dict or not set(keys) <= value.keys() or value.keys() - set(keys) - set(optional):
        _fail("migration object requires exact fields: " + ", ".join(sorted(keys)))


def _text(value, *, nullable=False, nonempty=False):
    if nullable and value is None:
        return
    if type(value) is not str or len(value) > MAX_TEXT or nonempty and not value.strip():
        _fail("migration field requires bounded " + ("nonempty " if nonempty else "") + "text")


def _integer(value, minimum=0, maximum=None, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not int or value < minimum or maximum is not None and value > maximum:
        _fail("migration field requires an exact bounded integer")


def _boolean(value):
    if type(value) is not bool:
        _fail("migration field requires exact boolean")


def _digest(value, *, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not str or not _DIGEST.fullmatch(value):
        _fail("migration field requires lowercase SHA-256")


def _array(value, maximum=MAX_ROWS):
    if type(value) is not list or len(value) > maximum:
        _fail("migration array exceeds supported shape/row limit")


def _strings(value, allowed=None, *, unique=True):
    _array(value)
    for item in value:
        _text(item)
        if allowed is not None and item not in allowed:
            _fail("migration array has unsupported value " + item)
    if unique and len(set(value)) != len(value):
        _fail("migration set array contains duplicates")


def _path(value):
    _text(value, nonempty=True)
    if "\\" in value or "\x00" in value or value.startswith("/") or any(p in {"", ".", ".."} for p in value.split("/")):
        _fail("migration source path must be normalized project-relative POSIX")


def _reference_path(value):
    _path(value)
    parts = value.split("/")
    if len(parts) < 2 or parts[0] != ".pyalamode" or not parts[-1].endswith(".json"):
        _fail("migration reference must be a local .pyalamode JSON record")
    return parts


def _selector(value, *, module=False):
    _text(value)
    if module:
        if not value.startswith("module:"):
            _fail("module boundary selector requires module: prefix")
        name = value[len("module:"):]
        if name and any(not p.isidentifier() for p in name.split(".")):
            _fail("invalid module boundary selector")
    else:
        if value.count(":") != 1:
            _fail("authored boundary requires exact module:qualified-name selector")
        module_name, qualified = value.split(":")
        if not qualified or module_name and any(not p.isidentifier() for p in module_name.split(".")) or any(not p.isidentifier() for p in qualified.split(".")):
            _fail("invalid authored boundary selector")


def _public_selector(value):
    _selector(value)
    module_name, name = value.split(":")
    if not module_name or "." in name or name.startswith("_"):
        _fail("required/guarded export must be exact public top-level function")


def _named_selector(value):
    _selector(value)
    if not value.split(":")[0]:
        _fail("policy selection requires named source module")


def _utc(value):
    if type(value) is not str or not _UTC.fullmatch(value):
        _fail("migration timestamp requires explicit UTC")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as error:
        raise MigrationError("invalid migration UTC date") from error


def _location(value, *, diagnostic=False):
    if value is None:
        return
    keys = set("path line column end_line end_column column_encoding".split())
    if diagnostic:
        keys |= {"first_binding", "reason", "remediation"}
    _shape(value, keys)
    _path(value["path"])
    _integer(value["line"], 1)
    _integer(value["column"], 1)
    _integer(value["end_line"], 1, nullable=True)
    _integer(value["end_column"], 1, nullable=True)
    if value["column_encoding"] not in {"utf-8-bytes", "unicode-codepoints", "syntax-offset", "utf-16"}:
        _fail("unsupported authored coordinate encoding")
    if diagnostic:
        for key in ("first_binding", "reason", "remediation"):
            _text(value[key], nullable=key == "first_binding")


def _logical(value):
    _shape(value, {"kind", "selector", "qualified_name"})
    if value["kind"] not in {"module", "function", "record", "variant"}:
        _fail("unsupported migration boundary kind")
    _selector(value["selector"], module=value["kind"] == "module")
    _text(value["qualified_name"])


def _approval(value, *, state=False):
    _shape(value, APPROVAL_KEYS | ({"status", "expiry"} if state else set()), {"expires_at"})
    if value["operation"] not in OPERATIONS:
        _fail("approval requires actual canonical catalog operation")
    for key in ("contract_sha256", "dependency_sha256"):
        _digest(value[key])
    for key in ("owner", "rationale", "provenance"):
        _text(value[key], nonempty=True)
    if "expires_at" in value:
        _utc(value["expires_at"])
    if state:
        if value["status"] not in ADMISSIONS:
            _fail("unsupported approval state")
        if value["expiry"] != value.get("expires_at", "nonexpiring"):
            _fail("approval expiry does not match original approval")


def _integration_input(value):
    _shape(value, {"contract_sha256", "dependency_sha256", "admission", "approval", "identity_error"})
    _digest(value["contract_sha256"])
    _digest(value["dependency_sha256"], nullable=True)
    if value["admission"] not in ADMISSIONS:
        _fail("unsupported/tooling integration input cannot become migration evidence")
    _text(value["identity_error"], nullable=True)
    if value["approval"] is not None:
        _approval(value["approval"])


def _artifact(value):
    _shape(value, {"path", "sha256"})
    _text(value["path"], nonempty=True)
    _digest(value["sha256"])


def _installed(value):
    _shape(value, INSTALLED_KEYS)
    for key in INSTALLED_KEYS - {"extension_suffixes", "native_operations", "native_artifacts", "adapter_artifact", "interpreter_executable", "interpreter_core"}:
        _text(value[key])
    _strings(value["extension_suffixes"], unique=False)
    _strings(value["native_operations"], unique=False)
    _shape(value["native_artifacts"], {"binascii", "_sha2"})
    for row in value["native_artifacts"].values():
        _artifact(row)
    for key in ("adapter_artifact", "interpreter_executable", "interpreter_core"):
        _artifact(value[key])


def _assumption(value, inputs=None):
    _shape(value, ASSUMPTION_KEYS)
    if value["identity"] not in OPERATIONS or value["admission"] not in ADMISSIONS:
        _fail("external assumption requires actual operation/admission")
    for key in ("version", "source_evidence"):
        _text(value[key])
    _strings(value["effects"], EFFECTS)
    _strings(value["failures"], FAILURES)
    _shape(value["initialization"], {"effects", "failures", "evidence", "policy", "setup_backends", "native_foundations"})
    _strings(value["initialization"]["effects"], EFFECTS)
    for key in ("failures", "setup_backends"):
        _strings(value["initialization"][key])
    for key in ("evidence", "policy", "native_foundations"):
        _text(value["initialization"][key])
    provenance = value["provenance"]
    if type(provenance) is not dict:
        _fail("external provenance requires closed object")
    if provenance.get("kind") == "product-shipped candidate":
        _shape(provenance, {"kind", "source", "status"})
        if provenance["status"] != "reviewed":
            _fail("invalid product candidate status")
        _text(provenance["source"])
    elif provenance.get("kind") == "project-local conservative override":
        _shape(provenance, {"kind", "path", "sha256", "status", "review", "base_contract_sha256"})
        if provenance["status"] not in {"draft", "reviewed"}:
            _fail("invalid override status")
        for key in ("path", "review"):
            _text(provenance[key])
        for key in ("sha256", "base_contract_sha256"):
            _digest(provenance[key])
    else:
        _fail("unknown external contract provenance")
    if value["approval"] is not None:
        _approval(value["approval"])
    _digest(value["contract_sha256"])
    _digest(value["dependency_sha256"], nullable=True)
    if value["installed_identity"] is not None:
        _installed(value["installed_identity"])
        if _hash(value["installed_identity"]) != value["dependency_sha256"]:
            _fail("installed dependency content identity is corrupt")
    if inputs is not None:
        row = inputs.get(value["identity"])
        if row is None or any(row[k] != value[k] for k in ("contract_sha256", "dependency_sha256", "admission", "approval")):
            _fail("external assumption disagrees with captured integration inputs")


def _assertion(value):
    _shape(value, {"line", "name", "schema"})
    _integer(value["line"], 1)
    _text(value["name"])
    _text(value["schema"])


def _guard(value):
    _shape(value, {"mode", "selected_export", "debug", "data_assertions"})
    if value["mode"] not in {"off", "exports", "debug"}:
        _fail("invalid guard mode")
    row = value["selected_export"]
    if row is not None:
        _shape(row, set("selection public_boundary original_boundary original_protection coverage parameters returns generated".split()))
        for key in ("selection", "public_boundary", "original_boundary", "original_protection", "coverage"):
            _text(row[key])
        _parameters(row["parameters"])
        _text(row["returns"], nullable=True)
        _boolean(row["generated"])
    row = value["debug"]
    if row is not None:
        _shape(row, set("path name line parameters returns locals callable_validation capability_validation generated".split()))
        _path(row["path"])
        _integer(row["line"], 1)
        for key in ("name", "callable_validation", "capability_validation"):
            _text(row[key])
        _parameters(row["parameters"])
        _text(row["returns"], nullable=True)
        _boolean(row["generated"])
        _array(row["locals"])
        for assertion in row["locals"]:
            _assertion(assertion)
    _array(value["data_assertions"])
    for assertion in value["data_assertions"]:
        _assertion(assertion)


def _parameters(value):
    if type(value) is not dict:
        _fail("schema parameters require object")
    for name, schema in value.items():
        _text(name)
        _text(schema)


def _migration_policy(value):
    _shape(value, {"schema", "baseline"} | set(GATES))
    _integer(value["schema"], 1, 1)
    _reference_path(value["baseline"])
    for gate in GATES:
        _boolean(value[gate])


def _policy(value, legacy=False):
    _shape(value, LEGACY_POLICY_KEYS if legacy else POLICY_KEYS)
    if not legacy:
        from .distribution import validate_distribution_policy
        error = validate_distribution_policy({k:v for k,v in value.items() if k in {"distribution","checked_dependencies"} and v is not None})
        if error: _fail(error)
    for key in ("require_modules", "explicit_cases", "integration_manifests", "required_exports", "guarded_exports"):
        _strings(value[key])
    for pattern in value["require_modules"]:
        _path(pattern)
    for name in value["explicit_cases"]:
        _named_selector(name)
    for name in value["required_exports"] + value["guarded_exports"]:
        _public_selector(name)
    for path in value["integration_manifests"]:
        _path(path)
    if value["external_trust"] not in {"deny", "approved"} or value["boundary_guards"] not in {"off", "exports", "debug"}:
        _fail("unsupported trust/guard policy")
    if type(value["effect_bounds"]) is not dict:
        _fail("effect bounds require closed map")
    for selection, effects in value["effect_bounds"].items():
        _named_selector(selection)
        _strings(effects, EFFECTS)
    _array(value["integration_approvals"], MAX_APPROVALS)
    for row in value["integration_approvals"]:
        _approval(row)
    if len({r["operation"] for r in value["integration_approvals"]}) != len(value["integration_approvals"]):
        _fail("duplicate operation approvals")
    _migration_policy(value["migration"])


def _required_operation(value, inputs=None, *, legacy=None):
    _shape(value, set("operation required_by contract_sha256 dependency_sha256 admission engine_status engine_rule evidence".split()))
    if value["operation"] not in OPERATIONS or value["admission"] not in ADMISSIONS:
        _fail("required operation must be actual finite operation/admission")
    _digest(value["contract_sha256"], nullable=True)
    _digest(value["dependency_sha256"], nullable=True)
    _integer(value["engine_status"], 0, 2)
    if value["engine_rule"] not in {None, "PAL350", "PAL001"}:
        _fail("required approval evidence must preserve actual engine rule")
    _array(value["required_by"])
    if not value["required_by"]:
        _fail("required operation has no actual source requirement")
    for site in value["required_by"]:
        _shape(site, {"boundary", "path", "line", "via"} | ({"source_owner"} if legacy is False else set()), {"source_owner"} if legacy is None else set())
        if "source_owner" in site:
            owner=site["source_owner"]
            if owner != "project":
                _shape(owner,{"name","version","package"})
                from .distribution import _declaration
                _declaration({"schema":1,"name":owner["name"],"version":owner["version"],"packages":[owner["package"]]})
        _selector(site["boundary"])
        _path(site["path"])
        _integer(site["line"], 1)
        if site["via"] not in {"direct", "invoked", "retained"}:
            _fail("unsupported required-operation edge provenance")
    evidence = value["evidence"]
    _shape(evidence, {"kind", "value"})
    if evidence["kind"] == "external-assumption":
        _assumption(evidence["value"], inputs)
        if evidence["value"]["identity"] != value["operation"]:
            _fail("required operation evidence identity mismatch")
    elif evidence["kind"] == "integration-input":
        _integration_input(evidence["value"])
    else:
        _fail("unknown required-operation evidence kind")
    if any(evidence["value"][k] != value[k] for k in ("contract_sha256", "dependency_sha256", "admission")):
        _fail("required operation does not match evidence")
    if inputs is not None and inputs.get(value["operation"]) != (evidence["value"] if evidence["kind"] == "integration-input" else inputs.get(value["operation"])):
        _fail("required operation input mismatch")
    expected_status = 0 if value["admission"] == "approved" else 1
    if value["engine_status"] != expected_status or value["engine_rule"] != (None if expected_status == 0 else "PAL350"):
        _fail("approval observation cannot promote/change actual engine admission")


def _event(value):
    _shape(value, {"boundary", "before", "after", "reason", "location"})
    if value["boundary"] is not None:
        _logical(value["boundary"])
    _text(value["reason"])
    _location(value["location"])


def _current_events(value, inputs, *, legacy=None):
    _shape(value, {"required_exports", "expired_approvals", "approval_failures"})
    for rows in value.values():
        _array(rows)
        for event in rows:
            _event(event)
    for event in value["required_exports"]:
        row = event["after"]
        _shape(row, {"selector", "engine_status", "engine_rule", "source_evidence"})
        _public_selector(row["selector"])
        _integer(row["engine_status"], 1, 1)
        if row["engine_rule"] != "PAL361":
            _fail("invalid current required-export rule")
        _text(row["source_evidence"])
        if event["before"] is not None or not event["reason"].startswith("current-required-export-"):
            _fail("invalid current required-export event")
    for event in value["expired_approvals"]:
        _approval(event["after"], state=True)
        if event["before"] is not None:
            _approval(event["before"], state=True)
        if event["after"]["status"] != "expired":
            _fail("expiry event requires actual expired approval")
    for event in value["approval_failures"]:
        _required_operation(event["after"], inputs, legacy=legacy)
        if event["before"] is not None:
            _required_operation(event["before"], legacy=True if legacy else None)
        if event["after"]["admission"] == "approved":
            _fail("approved operation is not a current approval failure")


def _boundary_id(row):
    return _hash({key: row[key] for key in ("kind", "selector", "path")} | {"identity_version": IDENTITY_VERSION})


def _identity(row):
    return {"identity_version": IDENTITY_VERSION, **{key: row[key] for key in ("rule", "logical_boundary", "signature", "context_sha256", "origin")}}


def _sort_rows(rows):
    return sorted(rows, key=lambda row: _canonical(row))


def _state(state, *, retained=False):
    value = _json_value(state)
    schema=value.get("schema")
    if type(schema) is not int or schema not in {1,2}: _fail("unknown migration state schema")
    legacy=schema==1
    if legacy and not retained:_fail("recognized legacy state is historical provenance only")
    _shape(value, STATE_KEYS if legacy else STATE_KEYS | {"current_dependency_status","current_dependency_events"})
    from .model import CHECKER_VERSION,OPERATION_VERSION
    if (value["checker"],value["operation_contract"]) != ((LEGACY_CHECKER,LEGACY_OPERATION) if legacy else (CHECKER_VERSION,OPERATION_VERSION)): _fail("unrecognized checker/inventory provenance")
    if not legacy:
        _integer(value["current_dependency_status"],0,2)
        from .distribution import _declaration,dependency_context,validate_installed_receipt
        _array(value["current_dependency_events"])
        for event in value["current_dependency_events"]:
            _shape(event,{"dependency","rule","reason_code","selector","required_by","input_status","source_status"})
            dependency_context({k:event[k] for k in ("dependency","rule","reason_code","selector")} | {"site":"import","upstream":None})
            _strings(event["required_by"])
            for mod in event["required_by"]: _selector(mod,module=mod.startswith("module:"))
            _integer(event["input_status"],0,2)
            _integer(event["source_status"],0,2,nullable=True)
    if value["kind"] != "pyalamode-migration-state" or value["identity_version"] != IDENTITY_VERSION:
        _fail("incompatible migration state schema/identity")
    if value["target"] != "cpython-3.13.1" or value["edition"] != "python-v1":
        _fail("unsupported migration target/edition")
    for key in ("checker", "operation_contract"):
        _text(value[key], nonempty=True)
    _digest(value["snapshot"])
    if value["freshness"] not in {"current disk snapshot", "current overlay snapshot; unsaved", "stale; recheck required"}:
        _fail("invalid migration freshness")
    for key in ("strict_status", "current_policy_status"):
        _integer(value[key], 0, 2)
    env = value["runtime_environment"]
    _shape(env, {"filesystem_encoding", "filesystem_errors", "utf8_mode"})
    if env["filesystem_encoding"] != "utf-8" or env["filesystem_errors"] != "surrogateescape":
        _fail("unsupported migration filesystem target")
    _integer(env["utf8_mode"], 0, 1)
    inputs = value["inputs"]
    _shape(inputs, {"sources", "policy_sha256", "product_artifacts", "integration_inputs"} | (set() if legacy else {"checked_dependencies"}))
    if not legacy:
        if type(inputs["checked_dependencies"]) is not dict: _fail("dependency inventory requires map")
        for name,row in inputs["checked_dependencies"].items():
            validate_installed_receipt(row)
            if row["declaration"]["name"]!=name: _fail("dependency identity mismatch")
        expected_status=max((max(r["input_status"],r["source_status"] or 0) for r in inputs["checked_dependencies"].values()),default=0)
        if value["current_dependency_status"]!=expected_status or value["strict_status"]<expected_status: _fail("dependency source status laundered")
        event_names=[]
        for event in value["current_dependency_events"]:
            name=event["dependency"]["name"];receipt=inputs["checked_dependencies"].get(name)
            if receipt is None or event["dependency"]!={k:receipt["declaration"][k] for k in ("name","version","packages")} or (event["input_status"],event["source_status"])!=(receipt["input_status"],receipt["source_status"]) or max(receipt["input_status"],receipt["source_status"] or 0)==0:_fail("dependency event disagrees with actual receipt")
            if event["rule"]!=("PAL372" if receipt["admission"]=="changed" else "PAL370" if receipt["admission"] in {"missing","stale","incompatible"} else "PAL371"):_fail("dependency event rule disagrees with admission")
            event_names.append(name)
        if len(event_names)!=len(set(event_names)) or set(event_names)!={n for n,r in inputs["checked_dependencies"].items() if max(r["input_status"],r["source_status"] or 0)}:_fail("dependency refusal events must cover actual refused receipts")
    _digest(inputs["policy_sha256"], nullable=True)
    for key in ("sources", "product_artifacts", "integration_inputs"):
        if type(inputs[key]) is not dict:
            _fail("migration input inventory requires map")
    if len(inputs["sources"]) > MAX_SOURCES:
        _fail("migration source count exceeds supported limit")
    for path, source in inputs["sources"].items():
        _path(path)
        _shape(source, {"sha256", "origin", "version", "disk_sha256"})
        for key in ("sha256", "disk_sha256"):
            _digest(source[key])
        if source["origin"] not in {"disk", "overlay"}:
            _fail("invalid source provenance")
        if source["origin"] == "disk" and source["version"] is not None:
            _fail("disk source cannot have overlay version")
        if source["origin"] == "overlay":
            _integer(source["version"])
    for name, digest in inputs["product_artifacts"].items():
        _path(name)
        _digest(digest)
    for operation, row in inputs["integration_inputs"].items():
        if operation not in OPERATIONS:
            _fail("unknown integration input")
        _integration_input(row)
    scope = value["scope"]
    _shape(scope, {"project_root", "selected_paths", "displayed_paths", "exclusions"})
    _text(scope["project_root"], nonempty=True)
    for key in ("selected_paths", "displayed_paths"):
        _strings(scope[key])
        for path in scope[key]:
            _path(path)
        scope[key].sort()
    _array(scope["exclusions"])
    for exclusion in scope["exclusions"]:
        _shape(exclusion, {"path", "reason"})
        _path(exclusion["path"])
        _text(exclusion["reason"], nonempty=True)
    scope["exclusions"] = _sort_rows(scope["exclusions"])
    _shape(value["coverage"], set("eligible_modules selected_modules checked_modules eligible_functions selected_functions checked_functions checked_exports selected_records selected_variants".split()))
    for count in value["coverage"].values():
        _integer(count)
    _policy(value["policy"],legacy=legacy)
    _array(value["boundaries"])
    logical_buckets = {}
    for row in value["boundaries"]:
        _shape(row, BOUNDARY_KEYS)
        logical = {key: row[key] for key in ("kind", "selector", "qualified_name")}
        _logical(logical)
        _path(row["path"])
        _text(row["signature"], nullable=True)
        _digest(row["definition_sha256"])
        expected_id = _boundary_id(row)
        if row["id"] not in {None, expected_id}:
            _fail("corrupt current boundary identity")
        row["id"] = expected_id
        for key in ("selected", "strict_checked", "public_export", "required_export"):
            _boolean(row[key])
        _strings(row["selection_reasons"], {"source_fun", "source_effects", "module_marker", "required_module", "enclosing_selection"})
        if row["mode"] not in {"off", "audit", "strict"}:
            _fail("invalid boundary enforcement")
        _text(row["source_evidence"])
        for key in ("effect_bound", "required_effects"):
            _strings(row[key], EFFECTS)
            row[key].sort()
        if type(row["effect_origins"]) is not dict:
            _fail("effect origin requires map")
        for family, origins in row["effect_origins"].items():
            if family not in EFFECTS:
                _fail("unsupported effect origin family")
            _strings(origins)
            origins.sort()
        _array(row["external_assumptions"], MAX_APPROVALS)
        for assumption in row["external_assumptions"]:
            _assumption(assumption, inputs["integration_inputs"])
        row["external_assumptions"] = _sort_rows(row["external_assumptions"])
        _shape(row["failures"], {"invocation", "definition", "initialization"})
        for failures in row["failures"].values():
            _strings(failures)
            failures.sort()
        _guard(row["guard_coverage"])
        _location(row["location"])
        logical_buckets.setdefault(_hash(logical), []).append(row)
    value["boundaries"] = _sort_rows(value["boundaries"])
    _array(value["findings"])
    total_locations = 0
    grouped = {}
    for row in value["findings"]:
        _shape(row, FINDING_KEYS)
        if row["rule"] not in SOURCE_RULES:
            _fail("tooling/policy/unknown rule cannot become audit debt")
        _logical(row["logical_boundary"])
        _text(row["signature"], nullable=True)
        _text(row["origin"])
        context = row["context"]
        if type(context) is not dict:
            _fail("finding context requires explicit AST/unavailable object")
        unavailable = context.get("kind") == "unavailable"
        if unavailable:
            _shape(context, {"kind", "reason"})
            _text(context["reason"], nonempty=True)
        elif context.get("kind")=="checked-dependency":
            if legacy:_fail("historical schema cannot invent current dependency context")
            from .distribution import dependency_context
            dependency_context({k:v for k,v in context.items() if k!="kind"})
        else:
            _shape(context, {"kind", "ast"})
            if context["kind"] != "ast-statement" or type(context["ast"]) is not str or not context["ast"] or len(context["ast"]) > MAX_AST:
                _fail("finding context requires bounded statement AST")
        context_digest = _hash(context)
        if row["context_sha256"] not in {None, context_digest}:
            _fail("finding context hash is corrupt")
        row["context_sha256"] = context_digest
        identity = _identity(row)
        key = _hash(identity)
        if row["identity_key"] not in {None, key}:
            _fail("finding current identity is corrupt")
        row["identity_key"] = key
        birth = row["birth_identity"]
        if birth is None:
            birth = identity
        _shape(birth, IDENTITY_KEYS)
        _logical(birth["logical_boundary"])
        if birth["identity_version"] != IDENTITY_VERSION or any(birth[k] != identity[k] for k in ("rule", "signature", "context_sha256", "origin")):
            _fail("finding birth cannot change rule/context/signature/origin")
        if birth["logical_boundary"]["kind"] != row["logical_boundary"]["kind"] or not retained and birth != identity:
            _fail("current capture cannot promote historical birth lineage")
        row["birth_identity"] = birth
        expected_id = _hash(birth)
        if row["id"] not in {None, expected_id}:
            _fail("finding birth identity digest is corrupt")
        row["id"] = expected_id
        _array(row["locations"], MAX_LOCATIONS)
        if not row["locations"]:
            _fail("finding group has no authored locations")
        for location in row["locations"]:
            _location(location, diagnostic=True)
        total_locations += len(row["locations"])
        if total_locations > MAX_LOCATIONS:
            _fail("finding location count exceeds supported limit")
        _integer(row["count"], 1)
        if row["count"] != len(row["locations"]):
            _fail("finding multiplicity must equal location count")
        candidates = logical_buckets.get(_hash(row["logical_boundary"]), [])
        paths = {loc["path"] for loc in row["locations"]}
        ownership = [b for b in candidates if b["path"] in paths]
        if not ownership:
            _fail("finding has no captured authored boundary")
        ids = {b["id"] for b in ownership}
        if row["boundary_id"] is None and len(ids) == 1:
            row["boundary_id"] = next(iter(ids))
        if row["boundary_id"] not in ids:
            _fail("finding boundary identity mismatch")
        _boolean(row["review_required"])
        row["review_required"] = row["review_required"] or unavailable or len(candidates) != 1
        row["locations"] = _sort_rows(row["locations"])
        if key in grouped:
            prior = grouped[key]
            if prior["birth_identity"] != row["birth_identity"]:
                _fail("one finding group has conflicting birth lineage")
            prior["locations"].extend(row["locations"])
            prior["locations"] = _sort_rows(prior["locations"])
            prior["count"] += row["count"]
            prior["review_required"] |= row["review_required"]
        else:
            grouped[key] = row
    value["findings"] = _sort_rows(list(grouped.values()))
    _array(value["approvals"], MAX_APPROVALS)
    for approval in value["approvals"]:
        _approval(approval, state=True)
    value["approvals"] = _sort_rows(value["approvals"])
    _array(value["unsafe_adapters"], MAX_APPROVALS)
    for adapter in value["unsafe_adapters"]:
        _shape(adapter, set("boundary path line scope rationale valid_declaration source_evidence behavior output_boundary".split()))
        _selector(adapter["boundary"])
        _path(adapter["path"])
        _integer(adapter["line"], 1)
        _boolean(adapter["valid_declaration"])
        for key in ("scope", "rationale"):
            _text(adapter[key], nullable=True)
        for key in ("source_evidence", "behavior", "output_boundary"):
            _text(adapter[key])
    value["unsafe_adapters"] = _sort_rows(value["unsafe_adapters"])
    _array(value["required_operations"], MAX_APPROVALS)
    for required in value["required_operations"]:
        _required_operation(required, inputs["integration_inputs"], legacy=legacy)
    if not legacy:
        for operation in value["required_operations"]:
            for site in operation["required_by"]:
                if "source_owner" not in site:_fail("current required-operation site needs explicit ownership")
                owner=site["source_owner"]
                if owner=="project":
                    if site["path"] not in inputs["sources"]:_fail("project operation site is outside owned capture")
                else:
                    receipt=inputs["checked_dependencies"].get(owner["name"])
                    if receipt is None or owner["version"]!=receipt["declaration"]["version"] or owner["package"] not in receipt["declaration"]["packages"] or site["path"] not in receipt["observed"]["authored_sources"]:_fail("dependency operation site lacks exact installed ownership")
    if len({r["operation"] for r in value["required_operations"]}) != len(value["required_operations"]):
        _fail("duplicate required operation groups")
    value["required_operations"] = _sort_rows(value["required_operations"])
    _current_events(value["current_policy_events"], inputs["integration_inputs"], legacy=legacy)
    if not legacy:
        for event in value["current_policy_events"]["approval_failures"]:
            for site in event["after"]["required_by"]:
                if "source_owner" not in site:_fail("current approval event site needs explicit ownership")
    if value["strict_status"] != 2 and value["current_policy_status"] != 2:
        if set(scope["selected_paths"]) != set(inputs["sources"]) or not set(scope["displayed_paths"]) <= set(scope["selected_paths"]):
            _fail("migration scope must expose complete captured sources and a display subset")
        if set(inputs["product_artifacts"]) != (LEGACY_PRODUCTS if legacy else PRODUCTS):
            _fail("migration product inventory must include every current approved product byte identity")
        for boundary in value["boundaries"]:
            if boundary["path"] not in inputs["sources"]:
                _fail("boundary source is absent from actual input capture")
            if boundary["strict_checked"] and (not boundary["selected"] or boundary["mode"] != "strict"
                                               or "unverified" in boundary["source_evidence"].lower()
                                               or boundary["source_evidence"].lower().startswith("unchecked")):
                _fail("off/unselected/unverified boundary cannot fabricate checked coverage")
        rows = value["boundaries"]
        expected = {"eligible_modules": sum(b["kind"] == "module" for b in rows),
                    "selected_modules": sum(b["kind"] == "module" and b["selected"] for b in rows),
                    "checked_modules": sum(b["kind"] == "module" and b["strict_checked"] for b in rows),
                    "eligible_functions": sum(b["kind"] == "function" for b in rows),
                    "selected_functions": sum(b["kind"] == "function" and b["selected"] for b in rows),
                    "checked_functions": sum(b["kind"] == "function" and b["strict_checked"] for b in rows),
                    "checked_exports": sum(b["kind"] != "module" and b["public_export"] and b["strict_checked"] for b in rows),
                    "selected_records": sum(b["kind"] == "record" and b["selected"] for b in rows),
                    "selected_variants": sum(b["kind"] == "variant" and b["selected"] for b in rows)}
        if value["coverage"] != expected or expected["eligible_modules"] != len(inputs["sources"]):
            _fail("migration denominator does not match actual boundary/source inventory")
    _canonical(value)
    return value


def normalize_state(state: dict) -> dict:
    """Normalize a CURRENT detached capture; historical birth promotion refuses."""
    return _state(state)


def finding_context(source: str, diagnostic: dict, boundary: dict) -> dict:
    if diagnostic.get("dependency_context") is not None:
        from .distribution import dependency_context
        dependency_context(diagnostic["dependency_context"])
        return {"kind":"checked-dependency",**diagnostic["dependency_context"]}
    """Position-free smallest authored statement, with no application execution."""
    if type(source) is not str or len(source.encode("utf-8", "surrogatepass")) > MAX_BYTES:
        _fail("finding context requires bounded captured source")
    if type(diagnostic) is not dict or diagnostic.get("rule") not in SOURCE_RULES:
        _fail("tooling/policy diagnostic cannot become finding context")
    try:
        tree = ast.parse(source)
        # Python physical lines are CR/LF/CRLF; Unicode separators stay content.
        lines = io.StringIO(source, newline="").readlines()

        def position(line, column, encoding):
            if type(line) is not int or type(column) is not int or line < 1 or line > len(lines) or column < 1:
                raise ValueError("invalid authored context coordinate")
            text = lines[line - 1].rstrip("\r\n")
            offset = column - 1
            if encoding == "utf-8-bytes":
                if offset > len(text.encode("utf-8")):
                    raise ValueError("authored context column outside source")
                text.encode("utf-8")[:offset].decode("utf-8")
                return line, offset
            if encoding == "utf-16":
                prefix = text.encode("utf-16-le")[:offset * 2].decode("utf-16-le")
            elif encoding in {"unicode-codepoints", "syntax-offset"}:
                if offset > len(text):
                    raise ValueError("authored context column outside source")
                prefix = text[:offset]
            else:
                raise ValueError("unsupported context coordinate encoding")
            return line, len(prefix.encode("utf-8"))

        encoding = diagnostic.get("column_encoding", "utf-8-bytes")
        start = position(diagnostic.get("line"), diagnostic.get("column"), encoding)
        end = position(diagnostic.get("end_line") or diagnostic.get("line"),
                       diagnostic.get("end_column") or diagnostic.get("column"), encoding)
        if end < start:
            raise ValueError("reversed diagnostic range")
        boundary_location = boundary.get("location") if type(boundary) is dict else None
        candidates = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.stmt) or not hasattr(node, "end_lineno"):
                continue
            beginning, ending = (node.lineno, node.col_offset), (node.end_lineno, node.end_col_offset)
            if beginning <= start and end <= ending:
                if boundary_location and boundary.get("kind") != "module":
                    bstart = (boundary_location["line"], boundary_location["column"] - 1)
                    bend = (boundary_location["end_line"], boundary_location["end_column"] - 1)
                    if not bstart <= beginning or not ending <= bend:
                        continue
                candidates.append(node)
        if not candidates:
            raise ValueError("diagnostic has no captured statement/declaration context")
        candidates.sort(key=lambda n: (n.end_lineno - n.lineno, n.end_col_offset - n.col_offset))
        if len(candidates) > 1 and (candidates[0].lineno, candidates[0].col_offset, candidates[0].end_lineno, candidates[0].end_col_offset) == (candidates[1].lineno, candidates[1].col_offset, candidates[1].end_lineno, candidates[1].end_col_offset):
            raise ValueError("ambiguous statement ownership")
        dump = ast.dump(candidates[0], annotate_fields=True, include_attributes=False, show_empty=False)
        if len(dump) > MAX_AST:
            raise ValueError("statement context exceeds supported limit")
        return {"kind": "ast-statement", "ast": dump}
    except (SyntaxError, ValueError, TypeError, UnicodeError, RecursionError, KeyError) as error:
        return {"kind": "unavailable", "reason": str(error)[:MAX_TEXT]}


def _logical_row(row):
    return {key: row[key] for key in ("kind", "selector", "qualified_name")}


def _event_row(boundary, before, after, reason, location=None):
    return {"boundary": boundary, "before": before, "after": after, "reason": reason, "location": location}


def _finding_side(row, count):
    return {"finding": copy.deepcopy(row), "count": count, "path": row["locations"][0]["path"]}


def _relocation_key(row):
    logical = row["logical_boundary"]
    return _hash({"kind": logical["kind"], "qualified_name": logical["qualified_name"],
                  **{key: row[key] for key in ("signature", "rule", "context_sha256", "origin")}})


def _match_boundaries(old, new):
    matches, missing = [], []
    old_buckets, new_buckets = {}, {}
    for row in old:
        old_buckets.setdefault(_hash(_logical_row(row)), []).append(row)
    for row in new:
        new_buckets.setdefault(_hash(_logical_row(row)), []).append(row)
    old_left, new_left = [], []
    for key, rows in old_buckets.items():
        if len(rows) == 1 and len(new_buckets.get(key, [])) == 1:
            matches.append((rows[0], new_buckets[key][0]))
        elif len(rows) == 1 and not new_buckets.get(key):
            old_left += rows
        elif len(rows) != 1 or len(new_buckets.get(key, [])) > 1:
            missing += rows
    for key, rows in new_buckets.items():
        if key not in old_buckets and len(rows) == 1:
            new_left += rows
    relocation = lambda row: _hash({key: row[key] for key in ("kind", "qualified_name", "signature", "definition_sha256")})
    for before in old_left:
        possibles = [r for r in new_left if relocation(r) == relocation(before)]
        rivals = [r for r in old_left if relocation(r) == relocation(before)]
        if len(possibles) == len(rivals) == 1:
            matches.append((before, possibles[0]))
        else:
            missing.append(before)
    return matches, missing


def compare_states(reference: dict | None, current: dict) -> dict:
    """Compare independent dimensions; reference state must come from safe loading."""
    new = _state(current,retained=type(current) is dict and current.get("schema")==1)
    old = _state(reference, retained=True) if reference is not None else None
    if old is not None and old["schema"]==1:
        old["policy"]={**old["policy"],"distribution":None,"checked_dependencies":[]}
        old["inputs"]={**old["inputs"],"checked_dependencies":{}}
    out = {"schema": 1, "kind": "pyalamode-migration-comparison", "reference_observed": old is not None,
           **{name: [] for name in CATEGORIES}}
    out["lost_strict_coverage"] += copy.deepcopy(new["current_policy_events"]["required_exports"])
    out["expired_approvals"] += copy.deepcopy(new["current_policy_events"]["expired_approvals"])
    out["approval_failures"] += copy.deepcopy(new["current_policy_events"]["approval_failures"])
    # Explicit current inventory remains authoritative, never default-denied catalog.
    known_expired = {e["after"]["operation"] for e in out["expired_approvals"]}
    for approval in new["approvals"]:
        if approval["status"] == "expired" and approval["operation"] not in known_expired:
            out["expired_approvals"].append(_event_row(None, None, approval, "configured-approval-expired"))
    known_failed = {e["after"]["operation"] for e in out["approval_failures"]}
    for operation in new["required_operations"]:
        if operation["admission"] != "approved" and operation["operation"] not in known_failed:
            out["approval_failures"].append(_event_row(None, None, operation, "required-operation-approval-not-current"))
    buckets = {}
    for row in new["boundaries"]:
        buckets.setdefault(_hash(_logical_row(row)), []).append(row)
    for rows in buckets.values():
        if len(rows) > 1:
            out["ambiguous_findings"].append(_event_row(_logical_row(rows[0]), None, {"findings": [], "boundaries": rows}, "duplicate-logical-boundary"))
    for row in new["findings"]:
        if row["review_required"]:
            out["ambiguous_findings"].append(_event_row(row["logical_boundary"], None, {"findings": [row], "boundaries": []}, "current-context-review-required"))
    if old is None:
        return _json_value(out)
    unmatched_old, unmatched_new = {}, {}
    old_by_key = {r["identity_key"]: r for r in old["findings"]}
    for after in new["findings"]:
        before = old_by_key.pop(after["identity_key"], None)
        if before is not None and not before["review_required"] and not after["review_required"]:
            _compare_finding(out, before, after, "same-normalized-identity")
        else:
            unmatched_new[after["identity_key"]] = after
            if before is not None:
                unmatched_old[before["identity_key"]] = before
    unmatched_old.update(old_by_key)
    relocation_old, relocation_new = {}, {}
    for row in unmatched_old.values():
        relocation_old.setdefault(_relocation_key(row), []).append(row)
    for row in unmatched_new.values():
        relocation_new.setdefault(_relocation_key(row), []).append(row)
    ambiguous_old, ambiguous_new = set(), set()
    for key in relocation_old.keys() & relocation_new.keys():
        befores, afters = relocation_old[key], relocation_new[key]
        # A relocation cannot pair against an old/current boundary still present.
        old_selectors = {_hash(_logical_row(b)) for b in old["boundaries"]}
        new_selectors = {_hash(_logical_row(b)) for b in new["boundaries"]}
        unique_move = (len(befores) == len(afters) == 1 and not befores[0]["review_required"] and not afters[0]["review_required"]
                       and _hash(befores[0]["logical_boundary"]) not in new_selectors
                       and _hash(afters[0]["logical_boundary"]) not in old_selectors)
        if unique_move:
            before, after = befores[0], afters[0]
            _compare_finding(out, before, after, "unique-authored-relocation")
            unmatched_old.pop(before["identity_key"])
            unmatched_new.pop(after["identity_key"])
        else:
            ambiguous_old.update(r["identity_key"] for r in befores)
            ambiguous_new.update(r["identity_key"] for r in afters)
            out["ambiguous_findings"].append(_event_row(None, {"findings": befores, "boundaries": []},
                                                        {"findings": afters, "boundaries": []}, "ambiguous-relocation-pairing"))
    for key, row in unmatched_old.items():
        if key not in ambiguous_old and not row["review_required"]:
            out["resolved_findings"].append(_event_row(row["logical_boundary"], _finding_side(row, row["count"]), None, "finding-no-longer-present"))
    for key, row in unmatched_new.items():
        if key not in ambiguous_new and not row["review_required"]:
            out["new_findings"].append(_event_row(row["logical_boundary"], None, _finding_side(row, row["count"]), "new-normalized-finding"))
    matches, missing = _match_boundaries(old["boundaries"], new["boundaries"])
    for before in missing:
        if before["selected"] or before["strict_checked"] or before["required_export"]:
            out["lost_strict_coverage"].append(_event_row(_logical_row(before), before, None, "boundary-coverage-absent-or-ambiguous", before["location"]))
    for before, after in matches:
        logical = _logical_row(after)
        lost = [key for key in ("selected", "strict_checked", "required_export") if before[key] and not after[key]]
        if before["public_export"] and before["strict_checked"] and not (after["public_export"] and after["strict_checked"]):
            lost.append("checked-public-export")
        if lost:
            out["lost_strict_coverage"].append(_event_row(logical, before, after, "lost-" + ",".join(lost), after["location"]))
        trust_key = lambda a: (a["identity"], a["contract_sha256"], a["dependency_sha256"])
        prior_trust = {trust_key(a) for a in before["external_assumptions"]}
        added = [a for a in after["external_assumptions"] if trust_key(a) not in prior_trust]
        if added:
            out["new_trust"].append(_event_row(logical, {"assumptions": before["external_assumptions"]}, {"assumptions": added}, "new-external-assumption", after["location"]))
        for dimension in ("effect_bound", "required_effects"):
            if set(after[dimension]) - set(before[dimension]):
                dims = ("effect_bound", "required_effects", "effect_origins")
                out["expanded_effects"].append(_event_row(logical, {k: before[k] for k in dims}, {k: after[k] for k in dims}, "expanded-" + dimension, after["location"]))
    matched_current = {r["id"] for _, r in matches}
    for after in new["boundaries"]:
        if after["id"] not in matched_current:
            if after["external_assumptions"]:
                out["new_trust"].append(_event_row(_logical_row(after), {"assumptions": []}, {"assumptions": after["external_assumptions"]}, "new-boundary-external-assumption", after["location"]))
            if after["effect_bound"] or after["required_effects"]:
                dims = ("effect_bound", "required_effects", "effect_origins")
                out["expanded_effects"].append(_event_row(_logical_row(after), None, {k: after[k] for k in dims}, "new-boundary-effects", after["location"]))
    _compare_unsafe(out, old, new)
    _compare_policy(out, old["policy"], new["policy"], old["inputs"]["integration_inputs"], new["inputs"]["integration_inputs"])
    for name in new["inputs"]:
        if old["inputs"][name] != new["inputs"][name]:
            out["inputs_changed"].append(_event_row(None, {"input": name, "value": old["inputs"][name]},
                                                    {"input": name, "value": new["inputs"][name]}, "input-identity-changed"))
    if old["scope"]["exclusions"] != new["scope"]["exclusions"]:
        out["inputs_changed"].append(_event_row(None, {"input": "exclusions", "value": old["scope"]["exclusions"]},
                                                {"input": "exclusions", "value": new["scope"]["exclusions"]}, "source-inventory-exclusions-changed"))
    for category in CATEGORIES:
        out[category] = _sort_rows(out[category])
    return _json_value(out)


def _compare_finding(out, before, after, reason):
    retained_count = min(before["count"], after["count"])
    retained = copy.deepcopy(after)
    retained["birth_identity"], retained["id"] = before["birth_identity"], before["id"]
    out["retained_findings"].append(_event_row(after["logical_boundary"], _finding_side(before, retained_count), _finding_side(retained, retained_count), reason))
    if after["count"] > retained_count:
        out["new_findings"].append(_event_row(after["logical_boundary"], None, _finding_side(after, after["count"] - retained_count), "new-identical-occurrences"))
    if before["count"] > retained_count:
        out["resolved_findings"].append(_event_row(before["logical_boundary"], _finding_side(before, before["count"] - retained_count), None, "resolved-identical-occurrences"))


def _compare_unsafe(out, old, new):
    def body(state, adapter):
        rows = [b for b in state["boundaries"] if b["kind"] == "function" and b["selector"] == adapter["boundary"] and b["path"] == adapter["path"]]
        return rows[0]["definition_sha256"] if len(rows) == 1 else None

    for after in new["unsafe_adapters"]:
        matches = [r for r in old["unsafe_adapters"] if r["boundary"] == after["boundary"]]
        if not matches:
            name = after["boundary"].split(":")[1]
            matches = [r for r in old["unsafe_adapters"] if r["boundary"].split(":")[1] == name
                       and r["scope"] == after["scope"] and r["rationale"] == after["rationale"]]
            new_rivals = [r for r in new["unsafe_adapters"] if r["boundary"].split(":")[1] == name
                          and r["scope"] == after["scope"] and r["rationale"] == after["rationale"]]
            if len(new_rivals) != 1:
                matches = []
        before = matches[0] if len(matches) == 1 else None
        changed_body = before is not None and (body(old, before) is None or body(new, after) is None or body(old, before) != body(new, after))
        if before is None or changed_body or any(before[k] != after[k] for k in ("scope", "rationale", "valid_declaration")):
            module, name = after["boundary"].split(":")
            logical = {"kind": "function", "selector": module + ":" + name, "qualified_name": name}
            out["unsafe_weakening"].append(_event_row(logical, before, after, "unsafe-adapter-body-changed" if changed_body else "unsafe-adapter-added-or-changed"))


def _compare_policy(out, before, after, before_inputs, after_inputs):
    def weaken(field, reason):
        out["policy_weakening"].append(_event_row(None, {"field": field, "value": before[field]},
                                                 {"field": field, "value": after[field]}, reason))
    for field in ("required_exports", "require_modules", "explicit_cases"):
        if set(before[field]) - set(after[field]):
            weaken(field, "required-policy-coverage-removed-or-changed")
    for selection, bound in before["effect_bounds"].items():
        if selection not in after["effect_bounds"] or set(after["effect_bounds"][selection]) - set(bound):
            weaken("effect_bounds", "entry-effect-policy-removed-or-widened")
            break
    if before["external_trust"] == "deny" and after["external_trust"] == "approved":
        weaken("external_trust", "external-trust-enabled")
    old_approvals = {r["operation"]: r for r in before["integration_approvals"]}
    for row in after["integration_approvals"]:
        prior = old_approvals.get(row["operation"])
        if prior is None:
            weaken("integration_approvals", "external-approval-added")
            break
        if prior != row:
            # Shortening expiry alone is tightening; review identities/provenance changes.
            nonexpiry = set(row) | set(prior) - {"expires_at"}
            changed_nonexpiry = any(row.get(k) != prior.get(k) for k in nonexpiry - {"expires_at"})
            old_expiry, new_expiry = prior.get("expires_at"), row.get("expires_at")
            if changed_nonexpiry or old_expiry is not None and (new_expiry is None or _utc(new_expiry) > _utc(old_expiry)):
                weaken("integration_approvals", "external-approval-expanded-or-review-changed")
                break
    if set(after["integration_manifests"]) - set(before["integration_manifests"]):
        weaken("integration_manifests", "external-manifest-added-or-changed")
    if set(before["integration_manifests"]) & set(after["integration_manifests"]):
        for operation in before_inputs.keys() & after_inputs.keys():
            if before_inputs[operation]["contract_sha256"] != after_inputs[operation]["contract_sha256"]:
                # The configured manifest has authority to change this operation.
                # Report a review obligation, without guessing semantic implication.
                weaken("integration_manifests", "configured-manifest-contract-changed-review-required:" + operation)
    old_migration, new_migration = before["migration"], after["migration"]
    if old_migration["baseline"] != new_migration["baseline"] or any(old_migration[k] and not new_migration[k] for k in GATES):
        weaken("migration", "migration-reference-or-protection-weakened")
    ranks = {"off": 0, "exports": 1, "debug": 2}
    if ranks[after["boundary_guards"]] < ranks[before["boundary_guards"]] or set(before["guarded_exports"]) - set(after["guarded_exports"]):
        weaken("boundary_guards", "additional-boundary-protection-reduced")


def evaluate_gates(comparison: dict, policy: dict) -> dict:
    value = _json_value(comparison)
    _comparison(value)
    _migration_policy(policy)
    for category in CATEGORIES:
        _array(value[category])
        for event in value[category]:
            _event(event)
    diagnostics, decisions = [], []
    for gate, (category, rule) in GATES.items():
        observed = value["reference_observed"] or gate == "reject_expired_approvals"
        enabled = policy[gate]
        if enabled and not observed:
            _fail("enabled historical migration gate requires a valid reference")
        events = value[category]
        failures = list(events)
        if gate in {"reject_new_findings", "reject_lost_strict_coverage"}:
            failures += value["ambiguous_findings"]
        passed = not failures if observed else None
        decisions.append({"gate": gate, "enabled": enabled, "observed": observed, "passed": passed, "event_count": len(events)})
        if enabled and failures:
            for event in failures:
                diagnostics.append({"rule": "PAL366" if event in value["ambiguous_findings"] else rule,
                                    "boundary": event["boundary"], "reason": event["reason"], "location": event["location"]})
    return {"status": int(bool(diagnostics)), "diagnostics": _sort_rows(diagnostics), "decisions": decisions}


def _finding_fragment(row):
    _shape(row, FINDING_KEYS)
    if row["rule"] not in SOURCE_RULES:
        _fail("comparison finding contains policy/tooling debt")
    _logical(row["logical_boundary"])
    _text(row["signature"], nullable=True)
    _text(row["origin"])
    _digest(row["boundary_id"])
    context = row["context"]
    if context.get("kind") == "ast-statement":
        _shape(context, {"kind", "ast"})
        if type(context["ast"]) is not str or len(context["ast"]) > MAX_AST:
            _fail("invalid finding AST")
    elif context.get("kind") == "checked-dependency":
        from .distribution import dependency_context
        dependency_context({k:v for k,v in context.items() if k!="kind"})
    elif context.get("kind") == "unavailable":
        _shape(context, {"kind", "reason"})
        _text(context["reason"])
    else:
        _fail("invalid comparison finding context")
    if row["context_sha256"] != _hash(context) or row["identity_key"] != _hash(_identity(row)):
        _fail("comparison finding identity is corrupt")
    _shape(row["birth_identity"], IDENTITY_KEYS)
    _logical(row["birth_identity"]["logical_boundary"])
    if row["birth_identity"]["identity_version"] != IDENTITY_VERSION or any(row["birth_identity"][key] != _identity(row)[key] for key in ("rule", "context_sha256", "signature", "origin")) or row["id"] != _hash(row["birth_identity"]):
        _fail("comparison finding birth is corrupt")
    _array(row["locations"], MAX_LOCATIONS)
    for location in row["locations"]:
        _location(location, diagnostic=True)
    _integer(row["count"], 1)
    if row["count"] != len(row["locations"]):
        _fail("comparison group count is corrupt")
    _boolean(row["review_required"])


def _boundary_fragment(row):
    _shape(row, BOUNDARY_KEYS)
    _logical(_logical_row(row))
    _path(row["path"])
    _digest(row["definition_sha256"])
    _text(row["signature"], nullable=True)
    if row["id"] != _boundary_id(row):
        _fail("comparison boundary id is corrupt")
    for key in ("selected", "strict_checked", "public_export", "required_export"):
        _boolean(row[key])
    _strings(row["selection_reasons"], {"source_fun", "source_effects", "module_marker", "required_module", "enclosing_selection"})
    if row["mode"] not in {"off", "audit", "strict"}:
        _fail("invalid comparison boundary mode")
    _text(row["source_evidence"])
    for key in ("effect_bound", "required_effects"):
        _strings(row[key], EFFECTS)
    _effect_dimensions({key: row[key] for key in ("effect_bound", "required_effects", "effect_origins")})
    _array(row["external_assumptions"], MAX_APPROVALS)
    for assumption in row["external_assumptions"]:
        _assumption(assumption)
    _shape(row["failures"], {"invocation", "definition", "initialization"})
    for failures in row["failures"].values():
        _strings(failures)
    _guard(row["guard_coverage"])
    _location(row["location"])


def _effect_dimensions(row):
    _shape(row, {"effect_bound", "required_effects", "effect_origins"})
    for key in ("effect_bound", "required_effects"):
        _strings(row[key], EFFECTS)
    if type(row["effect_origins"]) is not dict:
        _fail("effect origins require map")
    for key, origins in row["effect_origins"].items():
        if key not in EFFECTS:
            _fail("unknown effect family")
        _strings(origins)


def _comparison(value):
    _shape(value, set(CATEGORIES) | {"schema", "kind", "reference_observed"})
    _integer(value["schema"], 1, 1)
    if value["kind"] != "pyalamode-migration-comparison":
        _fail("incompatible comparison kind")
    _boolean(value["reference_observed"])
    for category in CATEGORIES:
        _array(value[category])
        for event in value[category]:
            _event(event)
            for side in ("before", "after"):
                row = event[side]
                if row is None:
                    continue
                if category in {"retained_findings", "resolved_findings", "new_findings"}:
                    _shape(row, {"finding", "count", "path"})
                    _finding_fragment(row["finding"])
                    _integer(row["count"], 1, row["finding"]["count"])
                    _path(row["path"])
                    if row["path"] not in {r["path"] for r in row["finding"]["locations"]}:
                        _fail("finding comparison path is not authored evidence")
                elif category == "ambiguous_findings":
                    _shape(row, {"findings", "boundaries"})
                    for finding in row["findings"]:
                        _finding_fragment(finding)
                    for boundary in row["boundaries"]:
                        _boundary_fragment(boundary)
                elif category == "lost_strict_coverage":
                    if event["reason"].startswith("current-required-export-"):
                        _shape(row, {"selector", "engine_status", "engine_rule", "source_evidence"})
                        _public_selector(row["selector"])
                        _integer(row["engine_status"], 1, 1)
                        if row["engine_rule"] != "PAL361":
                            _fail("invalid current coverage evidence")
                        _text(row["source_evidence"])
                    else:
                        _boundary_fragment(row)
                elif category == "new_trust":
                    _shape(row, {"assumptions"})
                    _array(row["assumptions"], MAX_APPROVALS)
                    for assumption in row["assumptions"]:
                        _assumption(assumption)
                elif category == "expanded_effects":
                    _effect_dimensions(row)
                elif category == "expired_approvals":
                    _approval(row, state=True)
                elif category == "approval_failures":
                    _required_operation(row)
                elif category == "unsafe_weakening":
                    _shape(row, set("boundary path line scope rationale valid_declaration source_evidence behavior output_boundary".split()))
                    _selector(row["boundary"])
                    _path(row["path"])
                    _integer(row["line"], 1)
                    _boolean(row["valid_declaration"])
                    for key in ("scope", "rationale"):
                        _text(row[key], nullable=True)
                    for key in ("source_evidence", "behavior", "output_boundary"):
                        _text(row[key])
                elif category == "policy_weakening":
                    _shape(row, {"field", "value"})
                    if row["field"] not in POLICY_KEYS:
                        _fail("unknown policy comparison field")
                    # Validate the individual field through an otherwise closed default policy.
                    default = _default_policy()
                    default[row["field"]] = row["value"]
                    _policy(default)
                elif category == "inputs_changed":
                    _shape(row, {"input", "value"})
                    if row["input"] not in {"sources", "policy_sha256", "product_artifacts", "integration_inputs", "checked_dependencies", "exclusions"}:
                        _fail("unknown migration input comparison")
                    if row["input"] == "policy_sha256":
                        _digest(row["value"], nullable=True)
                    elif row["input"] == "product_artifacts":
                        for name, digest in row["value"].items():
                            _path(name)
                            _digest(digest)
                    elif row["input"] == "checked_dependencies":
                        from .distribution import validate_installed_receipt
                        if type(row["value"]) is not dict: _fail("dependency input comparison map required")
                        for name,item in row["value"].items():
                            validate_installed_receipt(item)
                            if item["declaration"]["name"]!=name: _fail("dependency identity mismatch")
                    elif row["input"] == "integration_inputs":
                        for operation, item in row["value"].items():
                            if operation not in OPERATIONS:
                                _fail("unknown input operation")
                            _integration_input(item)
                    elif row["input"] == "exclusions":
                        for item in row["value"]:
                            _shape(item, {"path", "reason"})
                            _path(item["path"])
                            _text(item["reason"])
                    else:
                        for path, item in row["value"].items():
                            _path(path)
                            _shape(item, {"sha256", "origin", "version", "disk_sha256"})
                            _digest(item["sha256"])
                            _digest(item["disk_sha256"])
                            if item["origin"] not in {"disk", "overlay"}:
                                _fail("invalid source input")
                            if item["origin"] == "disk" and item["version"] is not None:
                                _fail("disk source version mismatch")
                            if item["origin"] == "overlay":
                                _integer(item["version"])
    return value


def _default_policy():
    return {"require_modules": [], "effect_bounds": {}, "explicit_cases": [],
            "external_trust": "deny", "integration_manifests": [], "integration_approvals": [],
            "required_exports": [], "boundary_guards": "off", "guarded_exports": [], "distribution": None, "checked_dependencies": [],
            "migration": {"schema": 1, "baseline": ".pyalamode/baseline.json", **{gate: False for gate in GATES}}}


def _report(value):
    _shape(value, set("schema kind state reference_id comparison gates status verified claim_scope human_measurement".split()))
    _integer(value["schema"], 1, 1)
    if value["kind"] != "pyalamode-migration-report":
        _fail("incompatible report schema")
    state = _state(value["state"])
    _digest(value["reference_id"], nullable=True)
    _comparison(value["comparison"])
    if value["comparison"]["reference_observed"] != (value["reference_id"] is not None):
        _fail("report reference provenance is inconsistent")
    gates = value["gates"]
    _shape(gates, {"status", "diagnostics", "decisions"})
    _integer(gates["status"], 0, 2)
    _array(gates["diagnostics"])
    for row in gates["diagnostics"]:
        _shape(row, {"rule", "boundary", "reason", "location"})
        if row["rule"] not in {r for _, r in GATES.values()} | {"PAL366"}:
            _fail("invalid policy diagnostic rule")
        if row["boundary"] is not None:
            _logical(row["boundary"])
        _text(row["reason"])
        _location(row["location"])
    _array(gates["decisions"])
    if len(gates["decisions"]) != len(GATES):
        _fail("report gate decisions are incomplete")
    names = set()
    for row in gates["decisions"]:
        _shape(row, {"gate", "enabled", "observed", "passed", "event_count"})
        if row["gate"] not in GATES or row["gate"] in names:
            _fail("unknown/duplicate gate decision")
        names.add(row["gate"])
        for key in ("enabled", "observed"):
            _boolean(row[key])
        if row["passed"] is not None:
            _boolean(row["passed"])
        if row["passed"] is None and row["observed"]:
            _fail("observed gate cannot have unobserved result")
        _integer(row["event_count"])
    _integer(value["status"], 0, 2)
    _boolean(value["verified"])
    if value["verified"] and (value["status"] or state["strict_status"] or state["current_policy_status"] or gates["status"]):
        _fail("report cannot upgrade unsuccessful current evidence")
    _text(value["claim_scope"])
    _shape(value["human_measurement"], {"status", "participants", "attempts"})
    if value["human_measurement"]["status"] != "UNMEASURED":
        _fail("human migration usefulness remains UNMEASURED")
    for key in ("participants", "attempts"):
        _integer(value["human_measurement"][key], 0, 0)
    expected_gates = evaluate_gates(value["comparison"], state["policy"]["migration"])
    if _canonical(expected_gates) != _canonical(gates):
        _fail("report gate decisions do not match current closed policy")
    if value["status"] < max(state["strict_status"], state["current_policy_status"], gates["status"]):
        _fail("report status cannot waive strict source, current or selected historical policy")
    return state


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("duplicate migration JSON key")
        result[key] = value
    return result


def _decode(raw):
    if len(raw) > MAX_BYTES:
        _fail("migration record exceeds byte limit")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=lambda token: _fail("nonfinite migration JSON"))
        return _json_value(value)
    except (ValueError, TypeError, UnicodeError, RecursionError) as error:
        raise MigrationError("invalid migration JSON: " + str(error)) from error


def _pretty(value):
    raw = (json.dumps(_json_value(value), sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")
    if len(raw) > MAX_BYTES:
        _fail("published migration record exceeds byte limit")
    return raw


class _Local:
    """Directory-descriptor ownership, no-follow reads and atomic regular writes."""

    def __init__(self, root):
        if not isinstance(root, Path):
            _fail("migration IO root requires Path")
        if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
            _fail("safe migration IO unsupported on this target")
        self.root = root.resolve(strict=True)
        self.fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    def close(self):
        os.close(self.fd)

    @contextmanager
    def directory(self, parts, *, create=False):
        descriptor = os.dup(self.fd)
        try:
            for part in parts:
                if create:
                    try:
                        os.mkdir(part, mode=0o755, dir_fd=descriptor)
                    except FileExistsError:
                        pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
                os.close(descriptor)
                descriptor = child
            yield descriptor
        finally:
            os.close(descriptor)

    def read(self, relative):
        parts = _reference_path(relative)
        with self.directory(parts[:-1]) as directory:
            descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
            try:
                before = os.fstat(descriptor)
                if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > MAX_BYTES:
                    _fail("migration record requires bounded single-link regular file")
                chunks, length = [], 0
                while True:
                    raw = os.read(descriptor, min(64 * 1024, MAX_BYTES + 1 - length))
                    if not raw:
                        break
                    chunks.append(raw)
                    length += len(raw)
                    if length > MAX_BYTES:
                        _fail("migration record exceeds byte limit")
                after = os.fstat(descriptor)
                named = os.stat(parts[-1], dir_fd=directory, follow_symlinks=False)
                identity = lambda row: (row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_size, row.st_mtime_ns, row.st_ctime_ns)
                if identity(before) != identity(after) or identity(after) != identity(named):
                    _fail("migration record changed while reading")
                return b"".join(chunks)
            finally:
                os.close(descriptor)

    @contextmanager
    def transaction(self):
        with self.directory([".pyalamode"], create=True) as directory:
            name = ".write-lock"
            descriptor = os.open(name, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600, dir_fd=directory)
            identity = os.fstat(descriptor)
            try:
                os.write(descriptor, uuid.uuid4().hex.encode("ascii"))
                os.fsync(descriptor)
                yield
            finally:
                os.close(descriptor)
                current = os.stat(name, dir_fd=directory, follow_symlinks=False)
                if current.st_ino == identity.st_ino and current.st_dev == identity.st_dev:
                    os.unlink(name, dir_fd=directory)
                    # Publication already fsyncs its record directories inside the
                    # rollback scope. This ephemeral lock needs no later commit.

    @contextmanager
    def staged(self, relative, raw):
        parts = _reference_path(relative)
        with self.directory(parts[:-1], create=True) as directory:
            name = ".migration-" + uuid.uuid4().hex + ".tmp"
            descriptor = os.open(name, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600, dir_fd=directory)
            try:
                try:
                    view = memoryview(raw)
                    while view:
                        written = os.write(descriptor, view)
                        if written <= 0:
                            _fail("migration staging write failed")
                        view = view[written:]
                    os.fsync(descriptor)
                    identity = os.fstat(descriptor)
                finally:
                    os.close(descriptor)
                yield directory, name, parts[-1], identity
            finally:
                try:
                    os.unlink(name, dir_fd=directory)
                except FileNotFoundError:
                    pass

    def check_stage(self, relative, directory, temporary, identity, raw):
        with self.directory(_reference_path(relative)[:-1]) as current:
            now = os.fstat(current)
            original = os.fstat(directory)
            if (now.st_dev, now.st_ino) != (original.st_dev, original.st_ino):
                _fail("migration directory ownership changed before publication")
        descriptor = os.open(temporary, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        try:
            current = os.fstat(descriptor)
            if (current.st_dev, current.st_ino) != (identity.st_dev, identity.st_ino) or not stat.S_ISREG(current.st_mode) or current.st_nlink != 1 or current.st_size != len(raw):
                _fail("migration staging ownership/content changed before publication")
            chunks, count = [], 0
            while count < len(raw):
                block = os.read(descriptor, min(65536, len(raw) - count))
                if not block:
                    break
                chunks.append(block)
                count += len(block)
            named = os.stat(temporary, dir_fd=directory, follow_symlinks=False)
            if b"".join(chunks) != raw or (named.st_dev, named.st_ino) != (current.st_dev, current.st_ino):
                _fail("migration staging bytes changed before publication")
        finally:
            os.close(descriptor)

    def publish_immutable(self, relative, raw, prepublish, validate):
        with self.staged(relative, raw) as (directory, temporary, name, identity):
            _call_prepublish(prepublish)
            validate()
            self.check_stage(relative, directory, temporary, identity, raw)
            try:
                os.link(temporary, name, src_dir_fd=directory, dst_dir_fd=directory, follow_symlinks=False)
                os.unlink(temporary, dir_fd=directory)
                os.fsync(directory)
            except FileExistsError:
                existing = self.read(relative)
                if _canonical(_decode(existing)) != _canonical(_decode(raw)):
                    _fail("content-addressed record path has conflicting contents")
            actual = self.read(relative)
            if _canonical(_decode(actual)) != _canonical(_decode(raw)):
                _fail("published migration record did not retain expected content")

    def publish_active(self, relative, raw, prepublish, validate):
        try:
            previous_raw = self.read(relative)
        except FileNotFoundError:
            previous_raw = None
        with self.staged(relative, raw) as (directory, temporary, name, identity):
            rollback = self.staged(relative, previous_raw) if previous_raw is not None else nullcontext(None)
            with rollback as previous_stage:
                _call_prepublish(prepublish)
                validate()
                self.check_stage(relative, directory, temporary, identity, raw)
                if previous_stage is not None:
                    self.check_stage(relative, previous_stage[0], previous_stage[1], previous_stage[3], previous_raw)
                committed = False
                try:
                    os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
                    committed = True
                    os.fsync(directory)
                    if self.read(relative) != raw:
                        _fail("active migration record changed during publication")
                except (OSError, MigrationError):
                    if committed:
                        current = os.stat(name, dir_fd=directory, follow_symlinks=False)
                        # Never overwrite an independently replaced/in-place edited active file.
                        if (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns) != (identity.st_dev, identity.st_ino, identity.st_size, identity.st_mtime_ns):
                            _fail("active publication failed and ownership changed; safe rollback refused")
                        if previous_stage is None:
                            os.unlink(name, dir_fd=directory)
                        else:
                            os.replace(previous_stage[1], name, src_dir_fd=previous_stage[0], dst_dir_fd=directory)
                        try:
                            os.fsync(directory)
                        except OSError:
                            # Original failure remains status2; visible prior bytes are restored.
                            pass
                    raise


def _call_prepublish(callback):
    if not callable(callback) or callback() is not None:
        _fail("migration publication requires successful live None-return freshness callback")


def _record_id(record):
    return _hash({key: value for key, value in record.items() if key != "id"})


def _lineage(record, previous):
    _array(record["lineage"])
    previous_findings = {row["id"]: row for row in previous["state"]["findings"]} if previous else {}
    current_findings = {row["id"]: row for row in record["state"]["findings"]}
    expected = {}
    if previous is not None:
        current_capture = copy.deepcopy(record["state"])
        for finding in current_capture["findings"]:
            finding["birth_identity"] = _identity(finding)
            finding["id"] = _hash(finding["birth_identity"])
        compared = compare_states(previous["state"], current_capture)
        for event in compared["retained_findings"]:
            before, after = event["before"]["finding"], event["after"]["finding"]
            expected[before["id"]] = {"id": before["id"], "previous_identity_key": before["identity_key"],
                                      "current_identity_key": after["identity_key"], "previous_path": event["before"]["path"],
                                      "current_path": event["after"]["path"], "count": event["after"]["count"]}
    used = set()
    for row in record["lineage"]:
        _shape(row, {"id", "previous_identity_key", "current_identity_key", "previous_path", "current_path", "count"})
        for key in ("id", "previous_identity_key", "current_identity_key"):
            _digest(row[key])
        for key in ("previous_path", "current_path"):
            _path(row[key])
        _integer(row["count"], 1)
        before, after = previous_findings.get(row["id"]), current_findings.get(row["id"])
        if before is None or after is None or row["id"] in used:
            _fail("baseline lineage has no unique verified predecessor/current group")
        if expected.get(row["id"]) != row:
            _fail("baseline lineage is not a unique deterministic retained match")
        used.add(row["id"])
        if row["previous_identity_key"] != before["identity_key"] or row["current_identity_key"] != after["identity_key"] or row["count"] != min(before["count"], after["count"]):
            _fail("baseline lineage identity/count does not match history")
        if before["birth_identity"] != after["birth_identity"] or _relocation_key(before) != _relocation_key(after):
            _fail("baseline lineage changes normalized violation evidence")
        if row["previous_path"] not in {l["path"] for l in before["locations"]} or row["current_path"] not in {l["path"] for l in after["locations"]}:
            _fail("baseline lineage path does not match history")
    for row in record["state"]["findings"]:
        if row["birth_identity"] != _identity(row) and row["id"] not in used:
            _fail("relocated baseline birth lacks verified predecessor lineage")
    if previous is None and record["lineage"]:
        _fail("first baseline cannot invent a predecessor lineage")


def _load(local, relative, seen=None, depth=0):
    if depth >= MAX_CHAIN:
        _fail("migration history exceeds supported chain limit")
    raw = local.read(relative)
    record = _decode(raw)
    if type(record) is not dict:
        _fail("migration record requires envelope")
    kind = record.get("kind")
    if kind == "pyalamode-audit-baseline":
        _shape(record, {"schema", "kind", "id", "created_at", "owner", "rationale", "previous_id", "state", "lineage"})
        _integer(record["schema"], 1, 1)
        _utc(record["created_at"])
        for key in ("owner", "rationale"):
            _text(record[key], nonempty=True)
        _digest(record["previous_id"], nullable=True)
        state = _state(record["state"], retained=True)
        _recordable_state(state)
        record["state"] = state
    elif kind == "pyalamode-saved-report":
        _shape(record, {"schema", "kind", "id", "created_at", "report"})
        _integer(record["schema"], 1, 1)
        _utc(record["created_at"])
        state = _report(record["report"])
        _recordable_state(state)
        if record["report"]["status"] == 2:
            _fail("tooling report cannot be loaded as durable history")
    else:
        _fail("unsupported migration record kind")
    _digest(record["id"])
    if record["id"] != _record_id(record):
        _fail("migration record content identity is corrupt")
    parts = _reference_path(relative)
    if len(parts) == 3 and parts[1] in {"history", "reports"} and parts[2] != record["id"] + ".json":
        _fail("content-addressed record filename does not match verified identity")
    seen = set() if seen is None else set(seen)
    if record["id"] in seen:
        _fail("migration history predecessor cycle")
    seen.add(record["id"])
    if kind == "pyalamode-audit-baseline":
        history_path = ".pyalamode/history/" + record["id"] + ".json"
        if relative != history_path:
            historical = _decode(local.read(history_path))
            if _canonical(historical) != _canonical(record):
                _fail("active baseline and immutable history differ")
        previous = _load(local, ".pyalamode/history/" + record["previous_id"] + ".json", seen, depth + 1)["record"] if record["previous_id"] is not None else None
        if previous is not None and previous["kind"] != "pyalamode-audit-baseline":
            _fail("baseline predecessor must be baseline history")
        _lineage(record, previous)
    elif record["report"]["reference_id"] is not None:
        prior = None
        for directory in ("history", "reports"):
            try:
                prior = _load(local, ".pyalamode/" + directory + "/" + record["report"]["reference_id"] + ".json", seen, depth + 1)
                break
            except FileNotFoundError:
                pass
        if prior is None:
            _fail("saved report historical reference is missing")
        if _canonical(compare_states(prior["state"], state)) != _canonical(record["report"]["comparison"]):
            _fail("saved report comparison has no verified historical provenance")
    return {"record": record, "state": state,
            "receipt": {"path": relative, "id": record["id"], "sha256": hashlib.sha256(raw).hexdigest()}}


def load_reference(root: Path, relative: str) -> dict:
    """Load complete verified local history; it is never a current certificate."""
    local = _Local(root)
    try:
        return _load(local, relative)
    finally:
        local.close()


def _recordable_state(value):
    """Check original durable-capture admission without resetting saved lineage."""
    if value["strict_status"] == 2 or value["current_policy_status"] == 2 or value["freshness"] != "current disk snapshot":
        _fail("durable migration evidence requires non-tooling current disk capture")
    if any(row["origin"] != "disk" for row in value["inputs"]["sources"].values()):
        _fail("unsaved overlay evidence cannot be recorded as disk history")
    logical = [_hash(_logical_row(row)) for row in value["boundaries"]]
    if len(set(logical)) != len(logical) or any(row["review_required"] for row in value["findings"]):
        _fail("intrinsically ambiguous current identity requires source review before recording")
    return value


def _durable_state(state):
    return _recordable_state(_state(state))


def _receipt(record, path, state, history_path=None):
    return {"schema": 1, "kind": "pyalamode-migration-write-receipt", "record_kind": record["kind"],
            "id": record["id"], "path": path, "history_path": history_path,
            "previous_id": record.get("previous_id"), "status": 0, "verified": False,
            "state_strict_status": state["strict_status"], "current_policy_status": state["current_policy_status"]}


def _same_reference(local, receipt):
    loaded = _load(local, receipt["path"])
    if loaded["receipt"] != receipt:
        _fail("migration predecessor/reference changed before publication")


def write_baseline(root: Path, state: dict, *, owner: str, rationale: str,
                   replace: bool = False, prepublish) -> dict:
    value = _durable_state(state)
    _text(owner, nonempty=True)
    _text(rationale, nonempty=True)
    _boolean(replace)
    path = value["policy"]["migration"]["baseline"]
    if _reference_path(path)[1] in {"history", "reports"}:
        _fail("active baseline destination cannot use immutable history/report namespace")
    local = _Local(root)
    try:
        with local.transaction():
            try:
                previous = _load(local, path)
            except FileNotFoundError:
                previous = None
            if replace and previous is None:
                _fail("baseline replacement requires existing verified predecessor")
            if not replace and previous is not None:
                _fail("baseline exists; explicit reviewed replacement is required")
            if previous is not None and previous["record"]["kind"] != "pyalamode-audit-baseline":
                _fail("baseline predecessor has wrong record kind")
            lineage = []
            if previous is not None:
                compared = compare_states(previous["state"], value)
                for event in compared["retained_findings"]:
                    before, after = event["before"]["finding"], event["after"]["finding"]
                    current = next(row for row in value["findings"] if row["identity_key"] == after["identity_key"])
                    current["birth_identity"], current["id"] = after["birth_identity"], after["id"]
                    lineage.append({"id": current["id"], "previous_identity_key": before["identity_key"],
                                    "current_identity_key": current["identity_key"],
                                    "previous_path": event["before"]["path"], "current_path": event["after"]["path"],
                                    "count": event["after"]["count"]})
            record = {"schema": 1, "kind": "pyalamode-audit-baseline", "id": None,
                      "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "owner": owner, "rationale": rationale,
                      "previous_id": previous["record"]["id"] if previous else None,
                      "state": value, "lineage": _sort_rows(lineage)}
            record["id"] = _record_id(record)
            _lineage(record, previous["record"] if previous else None)
            raw = _pretty(record)
            history = ".pyalamode/history/" + record["id"] + ".json"

            def validate():
                if previous is not None:
                    _same_reference(local, previous["receipt"])
                else:
                    try:
                        local.read(path)
                    except FileNotFoundError:
                        return
                    _fail("active baseline appeared before initial publication")

            local.publish_immutable(history, raw, prepublish, validate)
            local.publish_active(path, raw, prepublish, validate)
            return _receipt(record, path, value, history)
    finally:
        local.close()


def save_report(root: Path, report: dict, *, prepublish) -> dict:
    value = _json_value(report)
    state = _report(value)
    _durable_state(state)
    if value["status"] == 2:
        _fail("tooling report cannot be durably recorded")
    local = _Local(root)
    try:
        with local.transaction():
            reference = None
            if value["reference_id"] is not None:
                for directory in ("history", "reports"):
                    try:
                        reference = _load(local, ".pyalamode/" + directory + "/" + value["reference_id"] + ".json")
                        break
                    except FileNotFoundError:
                        pass
                if reference is None:
                    _fail("saved report requires its actual verified reference history")
                expected = compare_states(reference["state"], state)
                if _canonical(expected) != _canonical(value["comparison"]):
                    _fail("report comparison differs from actual historical reference")
            elif _canonical(compare_states(None, state)) != _canonical(value["comparison"]):
                _fail("report current comparison does not match state")
            record = {"schema": 1, "kind": "pyalamode-saved-report", "id": None,
                      "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "report": value}
            record["id"] = _record_id(record)
            path = ".pyalamode/reports/" + record["id"] + ".json"

            def validate():
                if reference is not None:
                    _same_reference(local, reference["receipt"])

            local.publish_immutable(path, _pretty(record), prepublish, validate)
            _load(local, path)
            return _receipt(record, path, state)
    finally:
        local.close()


def _bounded(function):
    """All public malformed-data and IO paths have one bounded error contract."""
    def call(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except MigrationError:
            raise
        except (OSError, ValueError, TypeError, UnicodeError, RecursionError, KeyError, IndexError, StopIteration, RuntimeError, OverflowError) as error:
            raise MigrationError(function.__name__ + " refused: " + str(error)) from error
    call.__name__ = function.__name__
    call.__doc__ = function.__doc__
    return call


finding_context = _bounded(finding_context)
normalize_state = _bounded(normalize_state)
compare_states = _bounded(compare_states)
evaluate_gates = _bounded(evaluate_gates)
load_reference = _bounded(load_reference)
write_baseline = _bounded(write_baseline)
save_report = _bounded(save_report)
