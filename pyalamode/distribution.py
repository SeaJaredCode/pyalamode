"""Finite source wheels and passive installed evidence. No application imports."""
from __future__ import annotations
import ast
import base64
import copy
import csv
from dataclasses import asdict, fields
import hashlib
import io
import json
import marshal
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tokenize
import zipfile
from .model import CHECKER_VERSION, EDITION, OPERATION_VERSION, TARGET, FunctionContract, foundation_identities, runtime_environment

VERSION = "pyalamode.distribution-v1"
CLAIM_SCOPE = "Listed strict exports and characterized transitive assumptions; initialization and data guards separately stated; ordinary shells unchecked."
LIMIT = 1024 * 1024
MAX_JSON = 16 * LIMIT
NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
VER = re.compile(r"(?:0|[1-9][0-9]{0,5})\.(?:0|[1-9][0-9]{0,5})\.(?:0|[1-9][0-9]{0,5})\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
_RESERVED = {"pyalamode", "typing", "types", "collections", "builtins", "sys", "os", "importlib", "binascii", "_sha2", "_imp"}

class DistributionError(ValueError):
    pass

def canonical(value):
    parts=[];size=0
    for part in json.JSONEncoder(sort_keys=True,separators=(",", ":"),ensure_ascii=True,allow_nan=False).iterencode(value):
        raw=part.encode();size+=len(raw)
        if size>MAX_JSON:raise DistributionError("canonical evidence byte bounds exceeded")
        parts.append(raw)
    return b"".join(parts)

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def shape(value, names):
    if type(value) is not dict or set(value) != set(names):
        raise DistributionError("invalid closed distribution object shape")

def text(value, maximum=16384):
    if type(value) is not str or not value or len(value) > maximum or "\0" in value:
        raise DistributionError("invalid bounded distribution text")
    return value

def identifier(value):
    text(value,128)
    if not value.isidentifier():
        raise DistributionError("invalid Python identifier")
    return value

def module(value):
    text(value,1024)
    for part in value.split("."):
        identifier(part)
    return value

def selection(value):
    text(value,1024)
    if value.count(":") != 1:
        raise DistributionError("invalid export selector")
    owner, name = value.split(":")
    module(owner)
    identifier(name)
    if name.startswith("_"):
        raise DistributionError("export must be public")
    return value

def relative(value):
    text(value,4096)
    if value.startswith("/") or "\\" in value or any(p in {"", ".", ".."} for p in value.split("/")):
        raise DistributionError("invalid owned relative path")
    return value

def bounded(value, depth=0, counter=None):
    counter = counter or [0]
    counter[0] += 1
    if depth > 64 or counter[0] > 500000:
        raise DistributionError("distribution evidence bounds exceeded")
    if value is None or type(value) is bool:
        return
    if type(value) is int:
        if not -(2**63) <= value < 2**63:
            raise DistributionError("evidence integer bounds exceeded")
    elif type(value) is str:
        if len(value) > 16384:
            raise DistributionError("evidence string bounds exceeded")
    elif type(value) in {list, dict}:
        if len(value) > 16384:
            raise DistributionError("evidence container bounds exceeded")
        for k,v in value.items() if type(value) is dict else enumerate(value):
            if type(value) is dict:
                text(k)
            bounded(v,depth+1,counter)
    else:
        raise DistributionError("unknown evidence value type")

def _pairs(rows):
    result = {}
    for k,v in rows:
        if k in result:
            raise DistributionError("duplicate evidence key")
        result[k] = v
    return result

def read(path, maximum=LIMIT):
    path = Path(path)
    if path.is_symlink() or any(p.is_symlink() for p in path.parents) or not path.is_file() or path.stat().st_size > maximum:
        raise DistributionError("not a bounded regular owned file: " + str(path))
    before=path.stat()
    with path.open("rb") as stream: raw=stream.read(maximum+1)
    after=path.stat()
    if len(raw)>maximum or (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns) or len(raw)!=after.st_size:raise DistributionError("owned file changed or exceeded bound during read")
    return raw

def json_read(path):
    value = json.loads(read(path,MAX_JSON), object_pairs_hook=_pairs, parse_constant=lambda _: (_ for _ in ()).throw(DistributionError("nonfinite JSON")))
    bounded(value)
    return value

def file_receipt(path):
    path = Path(path)
    if path.is_symlink() or any(p.is_symlink() for p in path.parents): raise DistributionError("symlink owned input")
    present = path.exists()
    return {"path":str(path), "exists":present, "sha256":hashlib.sha256(read(path,MAX_JSON)).hexdigest() if present else None,"size":path.stat().st_size if present else None}

def _declaration(row, producer=False):
    shape(row, {"schema","name","version","packages"} | ({"exports"} if producer else set()))
    if type(row["schema"]) is not int or row["schema"] != 1:
        raise DistributionError("unsupported distribution policy schema")
    if not NAME.fullmatch(text(row["name"],64)) or not VER.fullmatch(text(row["version"],32)):
        raise DistributionError("unsupported distribution name/version")
    packages = row["packages"]
    if type(packages) is not list or not 1 <= len(packages) <= 64 or len(set(packages)) != len(packages):
        raise DistributionError("unique initialized top-level packages required")
    for name in packages:
        text(name,64);identifier(name)
        if name.startswith("_") or name in _RESERVED:
            raise DistributionError("reserved package namespace")
    if producer:
        exports = row["exports"]
        if type(exports) is not list or not 1 <= len(exports) <= 4096 or len(set(exports)) != len(exports):
            raise DistributionError("unique explicit exports required")
        for value in exports:
            selection(value)
            if value.split(":")[0].split(".")[0] not in packages:
                raise DistributionError("export outside owned packages")

def validate_distribution_policy(policy):
    try:
        if "distribution" in policy:
            _declaration(policy["distribution"],True)
        rows = policy.get("checked_dependencies",[])
        if type(rows) is not list or len(rows) > 64:
            raise DistributionError("bounded checked_dependencies list required")
        owners, packages = set(),set()
        for row in rows:
            _declaration(row)
            if row["name"] in owners or packages.intersection(row["packages"]):
                raise DistributionError("duplicate dependency ownership")
            owners.add(row["name"])
            packages.update(row["packages"])
        if "distribution" in policy and packages.intersection(policy["distribution"]["packages"]):
            raise DistributionError("local and installed package ownership conflicts")
    except (DistributionError,TypeError) as e:
        return str(e)
    return None

def package_files(base, packages, generated=False):
    files = {};total=0;folded=set()
    for package in packages:
        directory = base/package
        if directory.is_symlink() or not (directory/"__init__.py").is_file():
            raise DistributionError("initialized owned package required: " + package)
        for current, children, names in os.walk(directory):
            current = Path(current)
            if current.is_symlink():
                raise DistributionError("symlink package source")
            children[:] = sorted(c for c in children if c != "__pycache__")
            if not (current/"__init__.py").is_file():
                raise DistributionError("namespace package unsupported")
            if "_pyalamode_exports" in children and not generated:
                raise DistributionError("reserved generated guard namespace")
            for child in children:
                if (current/child).is_symlink():
                    raise DistributionError("symlink package directory")
            for name in sorted(names):
                path = current/name
                if not name.endswith(".py"):
                    raise DistributionError("package data/native/sourceless artifact unsupported: " + str(path))
                size=path.stat().st_size
                if len(files)>=16384 or total+size>64*LIMIT:raise DistributionError("package aggregate bounds exceeded")
                raw = read(path);total+=len(raw)
                key = path.relative_to(base).as_posix()
                if key.casefold() in folded:
                    raise DistributionError("casefold module ambiguity")
                if path.with_suffix("").is_dir():
                    raise DistributionError("package/module ambiguity")
                folded.add(key.casefold());files[key] = raw
    if len(files) > 16384 or sum(map(len,files.values())) > 64*LIMIT:
        raise DistributionError("package inventory bounds exceeded")
    return files

def integer(value, minimum=0, maximum=2**31-1):
    if type(value) is not int or not minimum <= value <= maximum:
        raise DistributionError("invalid bounded integer")

def boolean(value):
    if type(value) is not bool: raise DistributionError("exact boolean required")

def sha(value):
    if type(value) is not str or not SHA.fullmatch(value): raise DistributionError("invalid SHA256")

def array(value, maximum=16384):
    if type(value) is not list or len(value)>maximum: raise DistributionError("bounded array required")
    return value

def strings(value, allowed=None, unique=True):
    array(value)
    for v in value:
        text(v)
        if allowed is not None and v not in allowed: raise DistributionError("unknown finite evidence label")
    if unique and len(set(value))!=len(value): raise DistributionError("duplicate evidence label")

def mapping(value):
    if type(value) is not dict or len(value)>16384: raise DistributionError("bounded map required")
    return value

def _schema(value):
    from .checker import _contract_type, SCALARS, CAPABILITIES, COLLECTIONS, DOMAIN_TYPES, DOMAIN_CASES, EFFECT_FAMILIES
    text(value)
    try: spec=_contract_type(value)
    except (ValueError,TypeError,AttributeError,SyntaxError,RecursionError) as e:raise DistributionError("invalid exact schema") from e
    def valid(s, depth=0):
        if s is None:raise DistributionError("unknown exact schema")
        if depth>32: raise DistributionError("schema depth exceeded")
        if s.name.startswith(("record:","variant:","case:")):
            label=s.name.split(":",1)[1];text(label,1024)
            if label.count(":")!=(2 if s.name.startswith("case:") else 1): raise DistributionError("invalid nominal identity")
            mod,*names=label.split(":");module(mod);name=".".join(names)
            for part in name.split("."): identifier(part)
            if s.arguments or s.result: raise DistributionError("invalid nominal schema")
        elif s.name in SCALARS | CAPABILITIES.keys() | {"Nothing"}:
            if s.arguments or s.result: raise DistributionError("invalid scalar schema")
        elif s.name=="Callable":
            if s.result is None or s.variadic: raise DistributionError("invalid callable schema")
            strings(list(s.effect_bound),EFFECT_FAMILIES);valid(s.result,depth+1)
        elif s.name in {"tuple",*COLLECTIONS,*DOMAIN_TYPES,*DOMAIN_CASES}:
            arity=2 if s.name in {"Map","OrderedMap","Result"} else 1
            if s.name!="tuple" and len(s.arguments)!=arity: raise DistributionError("invalid data schema arity")
            if s.name in {"Map","OrderedMap","Set"} and s.arguments[0].name not in SCALARS: raise DistributionError("invalid scalar key schema")
            if s.result or s.variadic and (s.name!="tuple" or len(s.arguments)!=1): raise DistributionError("invalid variadic schema")
        else: raise DistributionError("unknown exact schema")
        for a in s.arguments: valid(a,depth+1)
    valid(spec)
    if str(spec)!=value: raise DistributionError("noncanonical exact schema")
    return spec

def schema_map(value):
    mapping(value)
    for name,schema in value.items(): identifier(name);_schema(schema)

def _callable(value,depth=0):
    if depth>32: raise DistributionError("callable evidence depth exceeded")
    shape(value,{"parameters","returns","targets","captures","conditional","effect_bound","wrapper","components","bound_arguments","obligation","captured_callbacks"})
    for s in array(value["parameters"]): _schema(s)
    _schema(value["returns"]);strings(value["targets"]);boolean(value["conditional"])
    from .migration import EFFECTS
    strings(value["effect_bound"],EFFECTS)
    if value["wrapper"] not in {None,"compose","partial_first"}: raise DistributionError("unknown callable wrapper")
    if value["obligation"] is not None: text(value["obligation"])
    for key in ("captures","bound_arguments"):
        for pair in array(value[key]):
            if type(pair) is not list or len(pair)!=2: raise DistributionError("invalid schema pair")
            text(pair[0]);_schema(pair[1])
    for child in array(value["components"]): _callable(child,depth+1)
    for pair in array(value["captured_callbacks"]):
        if type(pair) is not list or len(pair)!=2: raise DistributionError("invalid callback pair")
        identifier(pair[0]);_callable(pair[1],depth+1)

def _contract(value,kind):
    from .migration import EFFECTS, FAILURES, _assumption, _installed, _approval, ADMISSIONS
    if kind=="function":
        shape(value,{f.name for f in fields(FunctionContract)})
        for key in ("parameters","defaults","captures"): schema_map(value[key])
        if not set(value["defaults"])<=set(value["parameters"]): raise DistributionError("default outside parameters")
        _schema(value["returns"]);mapping(value["parameter_kinds"])
        if set(value["parameter_kinds"])!=set(value["parameters"]) or any(v not in {"positional_only","positional_or_keyword","keyword_only"} for v in value["parameter_kinds"].values()): raise DistributionError("invalid parameter kinds")
        for key in ("callable_capture_evidence","callable_default_evidence"):
            for name,entry in mapping(value[key]).items(): identifier(name);_callable(entry)
        if value["return_callable_evidence"] is not None: _callable(value["return_callable_evidence"])
        for key in ("callable_targets","callable_defaults","callable_arguments","effect_origins"):
            for name,entries in mapping(value[key]).items(): text(name);strings(entries)
        for key in ("dependencies","return_callable_targets","invoked_targets","callable_dependencies","operations","callable_operations"): strings(value[key])
        for key in ("effect_bound","required_effects"): strings(value[key],EFFECTS)
        strings(value["direct_failures"],FAILURES)
        for row in array(value["data_assertions"]):
            shape(row,{"line","name","schema"});integer(row["line"],1);identifier(row["name"]);_schema(row["schema"])
        for row in array(value["failure_edges"]):
            shape(row,{"target","line","column","handled"});text(row["target"]);integer(row["line"],1);integer(row["column"],1);strings(row["handled"],FAILURES)
        for row in array(value["borrow_scopes"]):
            shape(row,{"name","interface","line","end_line","lifetime"});identifier(row["name"]);_schema(row["interface"]);integer(row["line"],1);integer(row["end_line"],row["line"]);text(row["lifetime"])
        for row in array(value["handlers"]):
            shape(row,{"line","categories","discharged","target","target_semantics"});integer(row["line"],1);strings(row["categories"]);strings(row["discharged"],FAILURES)
            from .checker import HANDLER_CATEGORIES
            if not set(row["categories"])<=HANDLER_CATEGORIES:raise DistributionError("unknown handler category")
            if row["target"] is not None: identifier(row["target"])
            if row["target_semantics"]!="opaque actual Python exception, deleted on every handler exit": raise DistributionError("unknown exception target semantics")
        for row in array(value["patterns"]):
            shape(row,{"line","schema","case_set","covered","wildcard","case_fingerprint","policy_explicit"});integer(row["line"],1);_schema(row["schema"]);strings(row["case_set"]);strings(row["covered"]);boolean(row["wildcard"]);boolean(row["policy_explicit"])
            if not set(row["covered"])<=set(row["case_set"]): raise DistributionError("pattern covers unknown case")
            if row["case_fingerprint"]!="builtin-domains-v1":sha(row["case_fingerprint"])
        for name,row in mapping(value["capability_parameters"]).items():
            identifier(name);shape(row,{"interface","effect","operations","lifetime","permissions"});_schema(row["interface"]);strings([row["effect"]],EFFECTS);strings(row["operations"]);text(row["permissions"]);text(row["lifetime"])
            from .checker import CAPABILITIES,CAPABILITY_OPERATIONS
            if row["interface"] not in CAPABILITIES or row["effect"]!=CAPABILITIES[row["interface"]] or row["operations"]!=sorted(CAPABILITY_OPERATIONS[row["interface"]]):raise DistributionError("capability catalog disagreement")
        from .standard_contracts import operation_catalog
        from .encoding_contracts import operation_catalog as codecs
        from .integration_contracts import operation_catalog as integrations
        catalogs={r["identity"]:r for r in operation_catalog()+codecs()+integrations()}
        for row in array(value["operation_contracts"]):
            mapping(row);identity=row.get("identity")
            if type(identity) is not str or identity not in catalogs: raise DistributionError("unknown operation contract")
            if identity.startswith("pyalamode.integrations."):
                shape(row,set(catalogs[identity])|{"contract_sha256","dependency_sha256","admission","approval","identity_error","installed_identity"})
                for key,val in catalogs[identity].items():
                    if key not in {"effects","failures","provenance","owner","rationale","approval"} and row[key]!=val: raise DistributionError("changed product external catalog")
                strings(row["effects"],EFFECTS);strings(row["failures"],FAILURES);sha(row["contract_sha256"])
                if not set(catalogs[identity]["effects"])<=set(row["effects"]) or not set(catalogs[identity]["failures"])<=set(row["failures"]):raise DistributionError("external override weakens product contract")
                text(row["owner"]);text(row["rationale"])
                from .integration_contracts import _digest
                original={k:row[k] for k in catalogs[identity]};original["approval"]=catalogs[identity]["approval"]
                if _digest(original)!=row["contract_sha256"]:raise DistributionError("external contract digest disagrees with declaration")
                if row["dependency_sha256"] is not None: sha(row["dependency_sha256"])
                if row["admission"] not in ADMISSIONS: raise DistributionError("invalid external admission")
                if row["approval"] is not None: _approval(row["approval"])
                if row["identity_error"] is not None: text(row["identity_error"])
                if row["installed_identity"] is not None: _installed(row["installed_identity"])
                _assumption({k:row[k] for k in ("identity","version","effects","failures","initialization","provenance","approval","contract_sha256","dependency_sha256","installed_identity","admission")} | {"source_evidence":"producer declared external assumption"})
            elif row!=catalogs[identity]: raise DistributionError("product operation metadata changed")
        for row in array(value["external_assumptions"]): _assumption(row)
    elif kind=="record":
        shape(value,set("name schema path line fields defaults enforcement behavior source_evidence implementation_evidence trust failures definition_failures ordinary_validation_failures ordinary_representation_failures freshness boundary_protection caller_obligations equivalence".split()))
        _schema(value["schema"]);schema_map(value["fields"]);schema_map(value["defaults"])
        if not set(value["defaults"])<=set(value["fields"]): raise DistributionError("invalid record defaults")
        text(value["implementation_evidence"]);text(value["equivalence"])
        for key in ("ordinary_validation_failures","ordinary_representation_failures"):
            for name,reason in mapping(value[key]).items():strings([name],FAILURES|{"TypeError","AttributeError"});text(reason)
    elif kind=="variant":
        shape(value,set("name schema path line cases case_fingerprint enforcement behavior source_evidence trust failures definition_failures freshness boundary_protection caller_obligations equivalence".split()))
        _schema(value["schema"]);sha(value["case_fingerprint"]);text(value["equivalence"])
        for name,row in mapping(value["cases"]).items():
            identifier(name);shape(row,{"schema","fields","defaults"});_schema(row["schema"]);schema_map(row["fields"]);schema_map(row["defaults"])
            if not set(row["defaults"])<=set(row["fields"]): raise DistributionError("invalid case defaults")
    else: raise DistributionError("unknown export kind")
    identifier(value["name"]);text(value["path"],4096);integer(value["line"],1)
    for key in ("behavior","source_evidence","freshness","boundary_protection"): text(value[key])
    for key in ("trust","caller_obligations"): strings(value[key])
    for key in ("failures","definition_failures"): strings(value[key],FAILURES)
    if value["enforcement"]!="strict" or not value["source_evidence"].startswith("checked"): raise DistributionError("unverified/audit export is not a distribution claim")

def _file_row(row):
    shape(row,{"path","exists","sha256","size"});text(row["path"],4096);boolean(row["exists"])
    if not Path(row["path"]).is_absolute():raise DistributionError("input receipt path must be absolute provenance")
    if row["exists"]: sha(row["sha256"]);integer(row["size"],0,64*LIMIT)
    elif row["sha256"] is not None or row["size"] is not None: raise DistributionError("absent file has bytes")

def dependency_context(row):
    shape(row,{"dependency","selector","rule","reason_code","site","upstream"})
    shape(row["dependency"],{"name","version","packages"})
    _declaration({"schema":1,**row["dependency"]})
    if row["selector"] is not None: selection(row["selector"])
    if row["rule"] not in {"PAL370","PAL371","PAL372"} or row["reason_code"] not in {"missing-distribution","missing-evidence","stale-source","stale-policy","stale-artifact","incompatible-version","unpublished-export","dependency-source-refused","inputs-changed"} or row["site"] not in {"import","call"}: raise DistributionError("invalid dependency context")
    if row["upstream"] is not None:
        shape(row["upstream"],{"rule","selector"})
        from .migration import _selector
        text(row["upstream"]["selector"],1024)
        _selector(row["upstream"]["selector"],module=row["upstream"]["selector"].startswith("module:"))
        from .model import RULES
        if row["upstream"]["rule"] not in RULES: raise DistributionError("unknown upstream rule")

def _diagnostic(row):
    from .model import Diagnostic,RULES
    shape(row,{f.name for f in fields(Diagnostic)})
    if row["rule"] not in RULES: raise DistributionError("unknown diagnostic")
    for key in ("path","boundary","origin","reason","remediation"):text(row[key])
    integer(row["line"],1);integer(row["column"],1)
    for key in ("end_line","end_column"):
        if row[key] is not None:integer(row[key],1)
    if row["first_binding"] is not None:text(row["first_binding"])
    if row["column_encoding"] not in {"utf-8-bytes","unicode-codepoints","syntax-offset","utf-16"}:raise DistributionError("unknown diagnostic coordinate")
    if row["dependency_context"] is not None:dependency_context(row["dependency_context"])

def validate_installed_receipt(row):
    shape(row,{"schema","kind","declaration","admission","input_status","source_status","verified","complete","observed","candidate","exports","diagnostics","fingerprint"})
    if type(row["schema"]) is not int or row["schema"]!=1 or row["kind"]!="pyalamode-installed-dependency-input":raise DistributionError("unknown dependency receipt")
    _declaration(row["declaration"]);integer(row["input_status"],0,2);boolean(row["verified"]);boolean(row["complete"]);sha(row["fingerprint"])
    if row["source_status"] is not None:integer(row["source_status"],0,2)
    if row["admission"] not in {"missing","stale","incompatible","current","unpublished","changed","tooling"}:raise DistributionError("unknown dependency admission")
    if row["input_status"]!=(2 if row["admission"]=="tooling" else 0 if row["admission"]=="current" else 1) or row["complete"]!=(row["admission"]!="tooling") or row["verified"]!=(row["admission"]=="current" and row["source_status"]==0):raise DistributionError("inconsistent dependency status axes")
    if row["admission"]!="current" and (row["exports"] or row["source_status"] not in {None,2}):raise DistributionError("refused candidate invents source evidence")
    obs=row["observed"];shape(obs,{"resolution_roots","owners","metadata","evidence","policy","authored_sources","artifacts","caches"})
    for root in array(obs["resolution_roots"]):shape(root,{"path","exists","candidates_sha256"});text(root["path"],4096);boolean(root["exists"]);sha(root["candidates_sha256"])
    for owner in array(obs["owners"],1):shape(owner,{"path","name","version"});text(owner["path"],4096);text(owner["name"],64);text(owner["version"],32)
    for key in ("evidence","policy"):
        if obs[key] is not None:_file_row(obs[key])
    for key in ("metadata","authored_sources","artifacts","caches"):
        for name,value in mapping(obs[key]).items():relative(name);_file_row(value)
    if set(obs["metadata"])!=(set() if not obs["owners"] else {"METADATA","WHEEL","RECORD"}):raise DistributionError("unknown/incomplete metadata receipt inventory")
    if row["candidate"] is not None:
        c=row["candidate"];shape(c,{"identity","evidence_sha256","producer_checker","export_selectors"});_identity(c["identity"]);sha(c["evidence_sha256"]);text(c["producer_checker"]);strings(c["export_selectors"])
        for s in c["export_selectors"]:selection(s)
        if c["identity"]["name"]!=row["declaration"]["name"] or c["identity"]["packages"]!=row["declaration"]["packages"]:raise DistributionError("candidate receipt ownership mismatch")
    if row["admission"]=="current" and (row["candidate"] is None or len(obs["owners"])!=1 or row["candidate"]["identity"]["version"]!=row["declaration"]["version"]):raise DistributionError("current receipt lacks exact current candidate owner")
    for e in array(row["exports"]):_export(e)
    if row["exports"] and not row["verified"]:raise DistributionError("unverified receipt has claims")
    for d in array(row["diagnostics"]):_diagnostic(d)

def _identity(row):
    shape(row,{"name","version","packages","wheel_tag"});_declaration({"schema":1,**{k:row[k] for k in ("name","version","packages")}})
    if row["wheel_tag"]!="py3-none-any":raise DistributionError("unsupported wheel tag")

def _export(row):
    shape(row,{"selector","kind","declaration","contract","source_location","guard"});selection(row["selector"]);selection(row["declaration"])
    if row["selector"]!=row["declaration"]:raise DistributionError("export identity is not actual declaration")
    loc=row["source_location"];shape(loc,{"path","line","column","column_encoding"});relative(loc["path"]);integer(loc["line"],1);integer(loc["column"],1)
    if loc["column_encoding"]!="utf-8-bytes":raise DistributionError("unknown source coordinate")
    _contract(row["contract"],row["kind"])
    if row["contract"]["name"]!=row["selector"].split(":")[1] or row["contract"]["line"]!=loc["line"]:raise DistributionError("declaration location mismatch")
    if row["guard"] is not None:raise DistributionError("guard coverage belongs to separate inventory")

def _guard_export(row):
    shape(row,set("selection public_boundary original_boundary original_protection coverage parameters returns generated".split()))
    for key in ("selection","public_boundary","original_boundary"):selection(row[key])
    schema_map(row["parameters"]);_schema(row["returns"]);boolean(row["generated"])
    for key in ("original_protection","coverage"):text(row[key])
    if row["selection"]!=row["original_boundary"] or not row["generated"]:raise DistributionError("invalid generated export identity")
    if row["coverage"]!="exact argument and return schemas, recursive nested data; no freezing, effects, callable purity, ownership or dependency tamper detection":raise DistributionError("unknown guard coverage")
    original,name=row["selection"].split(":");top,*tail=original.split(".")
    expected=top+"._pyalamode_exports"+("."+".".join(tail) if tail else "")+":"+name
    if row["public_boundary"]!=expected:raise DistributionError("foreign guard namespace")

def _debug_row(row):
    shape(row,set("path name line parameters returns locals callable_validation capability_validation generated".split()));relative(row["path"]);text(row["name"],1024);integer(row["line"],1);schema_map(row["parameters"]);boolean(row["generated"])
    if row["returns"] is not None:_schema(row["returns"])
    for key in ("callable_validation","capability_validation"):text(row[key])
    if not row["generated"] or row["callable_validation"]!="excluded; caller evidence obligations remain" or row["capability_validation"]!="excluded; exact interface, allowed operation and lifetime obligations remain":raise DistributionError("unknown debug coverage")
    for r in array(row["locals"]):shape(r,{"line","name","schema"});integer(r["line"],1);identifier(r["name"]);_schema(r["schema"])

def _setup(row):
    mapping(row)
    if row.get("identity")=="pyalamode.integrations import":
        shape(row,{"identity","version","line","phase","effects","failures","backends","evidence","policy"})
        from .integration_contracts import INTEGRATION_VERSION
        expected={"identity":"pyalamode.integrations import","version":INTEGRATION_VERSION,"phase":"ordinary external import setup","effects":["IO"],"failures":["ImportError","OSError"],"backends":["binascii","_sha2"],"evidence":"native-loader setup is separate from approved adapter invocation; surrounding ordinary initialization/body unchecked","policy":"not admitted in functional module initialization"}
        integer(row["line"],1)
        if any(row[k]!=v for k,v in expected.items()):raise DistributionError("unknown setup observation")
    else:
        from .standard_contracts import setup_contract
        identity=row.get("identity");text(identity,128)
        name=identity.removeprefix("pyalamode.")
        if name not in {"live_io","recorded_io","state","live_clock","recorded_clock","live_random","recorded_random","live_environment","recorded_environment"}:raise DistributionError("unknown setup operation")
        base=setup_contract(name)
        if base is None:raise DistributionError("unknown setup operation")
        shape(row,set(base)|{"path","line","column","phase","inputs","input_evidence","output","allowed_operations"})
        if any(row[k]!=v for k,v in base.items()):raise DistributionError("changed setup operation")
        text(row["path"],4096);integer(row["line"],1);integer(row["column"],1);text(row["phase"]);text(row["input_evidence"]);_schema(row["output"]);strings(row["allowed_operations"])
        for s in array(row["inputs"]):_schema(s)

def validate_evidence(value):
    bounded(value);shape(value,{"schema","kind","payload","sha256"})
    if type(value["schema"]) is not int or value["schema"]!=1 or value["kind"]!="pyalamode-checked-distribution":raise DistributionError("unknown evidence schema")
    sha(value["sha256"])
    if value["sha256"]!=digest(value["payload"]):raise DistributionError("evidence checksum mismatch")
    p=value["payload"];shape(p,{"identity","target","producer","inputs","modules","exports","guards","artifacts","claim_scope"});_identity(p["identity"])
    shape(p["target"],{"python","implementation","gil","platforms","filesystem_encoding","filesystem_errors"})
    for key in ("python","implementation","gil","filesystem_encoding","filesystem_errors"):text(p["target"][key],128)
    strings(p["target"]["platforms"])
    producer=p["producer"];shape(producer,{"checker","edition","operation_contract","standard_version","integration_version","encoding_version","product_artifacts","runtime_environment"})
    for key in ("checker","edition","operation_contract","standard_version","integration_version","encoding_version"):text(producer[key])
    products=mapping(producer["product_artifacts"])
    if set(products)!=set(foundation_identities()):raise DistributionError("unknown/incomplete product inventory")
    for d in products.values():sha(d)
    env=producer["runtime_environment"];shape(env,{"filesystem_encoding","filesystem_errors","utf8_mode"});text(env["filesystem_encoding"],128);text(env["filesystem_errors"],128);integer(env["utf8_mode"],0,1)
    inp=p["inputs"];shape(inp,{"policy_sha256","sources","checked_dependencies","integration_inputs","resolution","selection"});sha(inp["policy_sha256"])
    for path,row in mapping(inp["sources"]).items():
        relative(path);shape(row,{"sha256","module","ownership","shipped","participating"});sha(row["sha256"]);boolean(row["shipped"]);boolean(row["participating"])
        if row["ownership"]!="project":raise DistributionError("unknown producer source ownership")
        if row["module"] is not None:module(row["module"])
    for name,r in mapping(inp["checked_dependencies"]).items():text(name,64);validate_installed_receipt(r)
    from .migration import _integration_input,OPERATIONS,FAILURES
    for op,r in mapping(inp["integration_inputs"]).items():
        if op not in OPERATIONS:raise DistributionError("unknown integration input")
        _integration_input(r)
    for name,path in mapping(inp["resolution"]).items():module(name);relative(path)
    for name,selected in mapping(inp["selection"]).items():module(name);boolean(selected)
    modules={}
    for row in array(p["modules"]):
        shape(row,{"module","authored_path","source_sha256","installed_path","artifact_sha256","initialization","setup_observations"});module(row["module"]);relative(row["authored_path"]);relative(row["installed_path"]);sha(row["source_sha256"]);sha(row["artifact_sha256"])
        if row["module"] in modules or row["authored_path"]!=row["installed_path"] or inp["sources"].get(row["authored_path"],{}).get("sha256")!=row["source_sha256"] or inp["resolution"].get(row["module"])!=row["authored_path"]:raise DistributionError("inconsistent module inventory")
        if row["module"].split(".")[0] not in p["identity"]["packages"]:raise DistributionError("module outside ownership")
        expected=row["installed_path"][:-3].replace("/",".");expected=expected.removesuffix(".__init__")
        if row["module"]!=expected:raise DistributionError("module/path disagreement")
        init=row["initialization"];shape(init,{"source_evidence","effects","failures"});text(init["source_evidence"])
        if inp["selection"].get(row["module"]):
            if not init["source_evidence"].startswith("checked") or init["effects"]!=[]:raise DistributionError("invalid characterized initialization")
            strings(init["failures"],FAILURES)
        elif init["effects"] is not None or init["failures"] is not None:raise DistributionError("ordinary initialization fabricates proof")
        for r in array(row["setup_observations"]):_setup(r)
        modules[row["module"]]=row
    if not modules or set(inp["resolution"])!=set(modules):raise DistributionError("incomplete module inventory")
    selectors=set()
    for row in array(p["exports"],4096):
        _export(row)
        mod=row["selector"].split(":")[0]
        if row["selector"] in selectors or mod not in modules or row["source_location"]["path"]!=modules[mod]["authored_path"]:raise DistributionError("duplicate/unowned export")
        selectors.add(row["selector"])
    guards=p["guards"];shape(guards,{"mode","exports","debug","generated_files"})
    if guards["mode"] not in {"off","exports","debug"}:raise DistributionError("unknown guard mode")
    guarded=set();published={r["selector"]:r for r in p["exports"]}
    for r in array(guards["exports"]):
        _guard_export(r)
        declaration=published.get(r["selection"])
        if r["selection"] in guarded or declaration is None or declaration["kind"]!="function":raise DistributionError("duplicate guard or guard on unpublished function")
        guarded.add(r["selection"])
        if r["parameters"]!=declaration["contract"]["parameters"] or r["returns"]!=declaration["contract"]["returns"]:raise DistributionError("guard schemas disagree with published function")
        if r["original_protection"]!=("debug data assertions" if guards["mode"]=="debug" else "unguarded"):raise DistributionError("guard protection/mode mismatch")
    expected_generated=set()
    for r in guards["exports"]:
        original=r["original_boundary"].split(":")[0];facade=r["public_boundary"].split(":")[0]
        key=facade.replace(".","/")+("/__init__.py" if modules[original]["installed_path"].endswith("/__init__.py") else ".py")
        expected_generated.add(key);parent=Path(key).parent
        while len(parent.parts)>1:
            expected_generated.add(parent.as_posix()+"/__init__.py");parent=parent.parent
    for r in array(guards["debug"]):_debug_row(r)
    for path,d in mapping(guards["generated_files"]).items():relative(path);sha(d)
    if set(guards["generated_files"])!=expected_generated:raise DistributionError("foreign/incomplete generated namespace inventory")
    if guards["mode"]=="off" and (guards["exports"] or guards["debug"] or guards["generated_files"]):raise DistributionError("off guard inventory")
    for path,row in mapping(p["artifacts"]).items():
        relative(path);shape(row,{"sha256","size","role"});sha(row["sha256"]);integer(row["size"],0,LIMIT)
        if row["role"] not in {"source","authored","metadata","generated"}:raise DistributionError("unknown artifact role")
    for m in modules.values():
        for path,d,role in ((m["installed_path"],m["artifact_sha256"],"source"),(wheel_paths({"name":p["identity"]["name"],"version":p["identity"]["version"]})[1]+"/pyalamode/sources/"+m["authored_path"],m["source_sha256"],"authored")):
            if path not in p["artifacts"] or p["artifacts"][path]["sha256"]!=d or p["artifacts"][path]["role"]!=role:raise DistributionError("missing module artifact identity")
    for path,d in guards["generated_files"].items():
        if path not in p["artifacts"] or p["artifacts"][path]["sha256"]!=d or p["artifacts"][path]["role"]!="generated":raise DistributionError("missing generated artifact")
    _,info=wheel_paths(p["identity"])
    expected_paths={m["installed_path"] for m in modules.values()}|{info+"/pyalamode/sources/"+m["authored_path"] for m in modules.values()}|set(guards["generated_files"])|{info+"/METADATA",info+"/WHEEL",info+"/pyalamode/policy.toml"}
    if set(p["artifacts"])!=expected_paths:raise DistributionError("foreign/incomplete artifact inventory")
    if p["claim_scope"]!=CLAIM_SCOPE:raise DistributionError("unknown distribution claim scope")
    return p

def _metadata(path):
    lines=read(path).decode("utf-8").splitlines()
    data={}
    for line in lines:
        if not line: break
        if ": " not in line or line.startswith((" ","\t")): raise DistributionError("unsupported metadata headers")
        k,v=line.split(": ",1)
        if k in data and k not in {"Requires-Dist"}: raise DistributionError("duplicate metadata header")
        data.setdefault(k,[]).append(v)
    return data

def _retained_bytecode(raw, filename, optimization):
    code=compile(raw,filename,"exec",dont_inherit=True,optimize=optimization)
    try:return marshal.dumps(code)
    finally:del code

def _pycs(base, artifacts):
    import importlib.util
    results={}
    known_sources={base/name for name in artifacts if name.endswith(".py")}
    cache_dirs={p.parent/"__pycache__" for p in known_sources}
    for cache_dir in cache_dirs:
        if not cache_dir.exists():continue
        if cache_dir.is_symlink() or not cache_dir.is_dir():raise DistributionError("invalid cache directory ownership")
        entries=list(cache_dir.iterdir())
        if len(entries)>16384:raise DistributionError("cache inventory bounds exceeded")
        expected_names={f"{p.stem}.cpython-313{suffix}.pyc" for p in known_sources if p.parent==cache_dir.parent for suffix in ("",".opt-1",".opt-2")}
        if any(p.name not in expected_names for p in entries):raise DistributionError("unknown/sourceless cache entry")
    for name,raw in artifacts.items():
        if not name.endswith(".py"): continue
        source=base/name
        caches=source.parent/"__pycache__"
        if not caches.exists(): continue
        for path in caches.iterdir():
            if not path.name.startswith(source.stem+"."): continue
            expected={f"{source.stem}.cpython-313.pyc":0,f"{source.stem}.cpython-313.opt-1.pyc":1,f"{source.stem}.cpython-313.opt-2.pyc":2}
            if path.name not in expected: raise DistributionError("unknown relevant bytecode cache")
            data=read(path)
            if len(data)<16 or data[:4]!=importlib.util.MAGIC_NUMBER: raise DistributionError("invalid bytecode header")
            flags=int.from_bytes(data[4:8],"little")
            valid = flags in {1,3} and data[8:16]==importlib.util.source_hash(raw) or flags==0 and int.from_bytes(data[8:12],"little")==int(source.stat().st_mtime)&0xffffffff and int.from_bytes(data[12:16],"little")==len(raw)&0xffffffff
            if not valid: raise DistributionError("bytecode differs from current compiler output")
            payload=data[16:];optimization=expected[path.name]
            if payload!=marshal.dumps(compile(raw,str(source),"exec",dont_inherit=True,optimize=optimization)) and payload!=_retained_bytecode(raw,str(source),optimization):
                raise DistributionError("bytecode differs from current compiler output")
            results[path.relative_to(base).as_posix()]=file_receipt(path)
    return results

def distribution_snapshot(policy,root):
    root=Path(root).resolve()
    result={"receipts":{},"sources":{},"raw_sources":{},"module_names":{},"resolved_modules":{},"source_owners":{},"exports":{},"required_modules":[],"aliases":{},"errors":[]}
    rows=policy.get("checked_dependencies",[])
    if not rows: return result
    roots=[]
    try:
        for raw in [str(root),*sys.path]:
            if type(raw) is not str: raise DistributionError("non-string import path")
            path=Path(raw or Path.cwd()).resolve()
            if path.is_file(): raise DistributionError("archive/custom import paths unsupported")
            if path.is_dir() and path not in roots: roots.append(path)
    except (OSError,DistributionError) as e:
        result["errors"].append(str(e));return result
    for declared in rows:
        receipt={"schema":1,"kind":"pyalamode-installed-dependency-input","declaration":copy.deepcopy(declared),"admission":"missing","input_status":1,"source_status":None,"verified":False,"complete":True,"observed":{"resolution_roots":[],"owners":[],"metadata":{},"evidence":None,"policy":None,"authored_sources":{},"artifacts":{},"caches":{}},"candidate":None,"exports":[],"diagnostics":[],"fingerprint":""}
        observed=receipt["observed"]
        try:
            owners=[]; package_candidates={p:[] for p in declared["packages"]}
            for directory in roots:
                relevant=[]
                infos=sorted(directory.glob("*.dist-info"))
                if len(infos)>16384: raise DistributionError("metadata inventory bounds exceeded")
                for info in infos:
                    if len(info.name)>256: raise DistributionError("metadata name bounds exceeded")
                    normalized=info.name.removesuffix(".dist-info").replace("_","-").lower()
                    if not normalized.startswith(declared["name"]+"-"): continue
                    meta=_metadata(info/"METADATA")
                    relevant.append(str(info)); owners.append((info,meta))
                for package in package_candidates:
                    for path in [directory/package,directory/(package+".py"),directory/(package+".pyc"),*directory.glob(package+"*.so")]:
                        if path.exists(): package_candidates[package].append(path);relevant.append(str(path))
                observed["resolution_roots"].append({"path":str(directory),"exists":True,"candidates_sha256":digest(sorted(relevant))})
            if len(owners)>1: raise DistributionError("duplicate installed distribution owners")
            if not owners:
                if any(package_candidates.values()): raise DistributionError("unowned/shadowed package")
            else:
                info,meta=owners[0]
                if info.is_symlink(): raise DistributionError("symlink metadata owner")
                if meta.get("Name")!=[declared["name"]] or len(meta.get("Version",[]))!=1 or not VER.fullmatch(meta["Version"][0]): raise DistributionError("invalid owner Name/Version")
                _,expected_info=wheel_paths({"name":declared["name"],"version":meta["Version"][0]})
                if info.name!=expected_info: raise DistributionError("metadata directory/identity mismatch")
                wheel=_metadata(info/"WHEEL")
                if set(wheel)!={"Wheel-Version","Generator","Root-Is-Purelib","Tag"} or wheel["Wheel-Version"]!=["1.0"] or wheel["Root-Is-Purelib"]!=["true"] or wheel["Tag"]!=["py3-none-any"]:raise DistributionError("unsupported WHEEL metadata")
                observed["owners"]=[{"path":str(info),"name":declared["name"],"version":meta.get("Version",[""])[0]}]
                for p,paths in package_candidates.items():
                    if len(paths)!=1 or paths[0] != info.parent/p: raise DistributionError("installed package shadow/namespace ambiguity")
                for k in ("METADATA","WHEEL","RECORD"): observed["metadata"][k]=file_receipt(info/k)
                record=[]
                for row in csv.reader(io.StringIO(read(info/"RECORD",MAX_JSON).decode())):
                    if len(record)>=16384:raise DistributionError("RECORD row bounds exceeded")
                    record.append(row)
                seen=set(); record_stale=False; record_rows={}
                for row in record:
                    if len(row)!=3: raise DistributionError("invalid RECORD row")
                    name=relative(row[0])
                    if name in seen: raise DistributionError("duplicate RECORD path")
                    seen.add(name);record_rows[name]=row
                    path=info.parent/name
                    if path.is_symlink() or not path.resolve().is_relative_to(info.parent): raise DistributionError("RECORD ownership escape")
                    if name==info.name+"/RECORD" or name.endswith(".pyc"):
                        if row[1:]!=["",""]:raise DistributionError("invalid RECORD self/cache row")
                    else:
                        if not re.fullmatch(r"sha256=[A-Za-z0-9_-]{43}",row[1]) or not re.fullmatch(r"0|[1-9][0-9]{0,8}",row[2]):raise DistributionError("invalid RECORD digest/size")
                        actual=file_receipt(path)
                        if actual["exists"]:
                            encoded="sha256="+base64.urlsafe_b64encode(bytes.fromhex(actual["sha256"])).decode().rstrip("=")
                            if row[1]!=encoded or int(row[2])!=actual["size"]:record_stale=True
                        else:record_stale=True
                installed=package_files(info.parent,declared["packages"],True)
                if any(name not in seen for name in installed): raise DistributionError("unrecorded installed source")
                observed["artifacts"]={name:file_receipt(info.parent/name) for name in installed}
                observed["caches"]=_pycs(info.parent,installed)
                if any(k.endswith(".pyc") and k not in observed["caches"] for k in seen):raise DistributionError("RECORD sourceless/unknown bytecode row")
                ep=info/"pyalamode/evidence.json";pp=info/"pyalamode/policy.toml"
                observed["evidence"]=file_receipt(ep); observed["policy"]=file_receipt(pp)
                if ep.exists():
                    payload=validate_evidence(json_read(ep))
                    identity=payload["identity"]
                    receipt["candidate"]={"identity":identity,"evidence_sha256":observed["evidence"]["sha256"],"producer_checker":payload["producer"]["checker"],"export_selectors":[r["selector"] for r in payload["exports"]]}
                    if identity["name"]!=meta["Name"][0] or identity["version"]!=meta["Version"][0] or identity["packages"]!=declared["packages"]:raise DistributionError("evidence owner identity mismatch")
                    allowed=set(payload["artifacts"])|{info.name+"/RECORD",info.name+"/pyalamode/evidence.json",info.name+"/INSTALLER",info.name+"/REQUESTED",info.name+"/direct_url.json"}|{str(Path(k).relative_to(info.parent)) for k in []}
                    if any(k not in allowed and not k.endswith(".pyc") for k in seen):raise DistributionError("unknown RECORD ownership row")
                    claimed_runtime={k for k,r in payload["artifacts"].items() if r["role"] in {"source","generated"}}
                    if not set(installed).issubset(claimed_runtime):raise DistributionError("source/artifact ownership inventory mismatch")
                    if any(name.endswith("/__init__.py") and name not in installed for name in claimed_runtime):raise DistributionError("initialized owned package required")
                    compatible = identity == {"name":declared["name"],"version":declared["version"],"packages":declared["packages"],"wheel_tag":"py3-none-any"} and payload["producer"]["checker"]==CHECKER_VERSION and payload["producer"]["operation_contract"]==OPERATION_VERSION and payload["producer"]["product_artifacts"]==foundation_identities() and payload["producer"]["edition"]==EDITION and payload["producer"]["standard_version"]=="pyalamode.standard-v1" and payload["producer"]["integration_version"]=="pyalamode.integrations-v1" and payload["producer"]["encoding_version"]=="pyalamode.encoding-v1" and payload["target"]=={"python":"3.13.1","implementation":"CPython","gil":"standard","platforms":["darwin-arm64","linux-aarch64"],"filesystem_encoding":"utf-8","filesystem_errors":"surrogateescape"}
                    receipt["admission"]="incompatible" if not compatible else "current"
                    stale=record_stale;causes=set()
                    for name,row in payload["artifacts"].items():
                        actual=file_receipt(info.parent/name)
                        if row["role"] in {"source","generated"}:observed["artifacts"][name]=actual
                        if not actual["exists"] or actual["sha256"]!=row["sha256"] or actual["size"]!=row["size"]:
                            stale=True;causes.add("stale-source" if row["role"] in {"authored","source"} else "stale-policy" if name.endswith("/pyalamode/policy.toml") else "stale-artifact")
                    if not pp.exists() or observed["policy"]["sha256"]!=payload["inputs"]["policy_sha256"]: stale=True;causes.add("stale-policy")
                    authored={}
                    for m in payload["modules"]:
                        path=info/"pyalamode/sources"/m["authored_path"]
                        actual=file_receipt(path); observed["authored_sources"][m["authored_path"]]=actual
                        if not actual["exists"] or actual["sha256"]!=m["source_sha256"]: stale=True;causes.add("stale-source")
                        else: authored[str(path)]=read(path)
                    if stale:
                        receipt["admission"]="stale"
                        receipt["_stale_reason"]=next((c for c in ("stale-source","stale-policy","stale-artifact") if c in causes),"stale-artifact")
                    if pp.exists():
                        import tomllib
                        originalpolicy=tomllib.loads(read(pp).decode()).get("tool",{}).get("pyalamode",{})
                        _declaration(originalpolicy.get("distribution"),True)
                        if receipt["admission"]=="current" and (originalpolicy.get("distribution")!={"schema":1,**{k:identity[k] for k in ("name","version","packages")},"exports":originalpolicy.get("distribution",{}).get("exports")} or set(originalpolicy.get("distribution",{}).get("exports",[]))!={e["selector"] for e in payload["exports"]}):raise DistributionError("evidence/distribution declaration disagreement")
                    if receipt["admission"]=="current":
                        receipt["input_status"]=0
                        for m in payload["modules"]:
                            path=str(info/"pyalamode/sources"/m["authored_path"])
                            raw=authored[path]
                            encoding,_=tokenize.detect_encoding(io.BytesIO(raw).readline)
                            result["sources"][path]=raw.decode(encoding); result["raw_sources"][path]=raw
                            result["module_names"][path]=m["module"];result["resolved_modules"][m["module"]]=path;result["source_owners"][path]=declared["name"]
                            if payload["inputs"]["selection"].get(m["module"]): result["required_modules"].append(path)
                        result["exports"][declared["name"]]=[r["selector"] for r in payload["exports"]]
                        receipt["_payload"]=payload;receipt["_base"]=str(info.parent)
                        for row in payload["guards"]["exports"]:
                            alias=row["public_boundary"].split(":")[0];original=row["original_boundary"].split(":")[0]
                            result["aliases"][alias]=original
        except (OSError,ValueError,TypeError,KeyError,UnicodeError,SyntaxError,RecursionError,csv.Error) as e:
            receipt.update(admission="tooling",input_status=2,complete=False)
            result["errors"].append("installed "+declared["name"]+": "+str(e))
        receipt["fingerprint"]=digest({"receipt":{k:v for k,v in receipt.items() if not k.startswith("_") and k!="fingerprint"},"consumer_policy":policy,"products":foundation_identities(),"target":TARGET,"runtime_environment":runtime_environment()})
        result["receipts"][declared["name"]]=receipt
    return result

def public_receipts(snapshot):
    return {name:{k:copy.deepcopy(v) for k,v in row.items() if not k.startswith("_")} for name,row in snapshot["receipts"].items()}

def wheel_paths(declaration):
    name=declaration["name"].replace("-","_")+"-"+declaration["version"]
    return name+"-py3-none-any.whl",name+".dist-info"

def build_wheel(result,capture,root,destination):
    from .guardgen import debug_source,facade_source,record_schemas
    root=Path(root);policy=capture["policy"];declaration=policy["distribution"]
    files=package_files(root,declaration["packages"])
    graph=capture["graph"];owned={r.path:r for r in result.results}
    records=record_schemas(result.results+capture.get("installed_results",[]))
    basename,info=wheel_paths(declaration)
    destination=Path(destination or root/"dist"/basename)
    if destination.is_symlink():raise DistributionError("symlink wheel destination")
    destination=destination.parent.resolve()/destination.name
    if destination.name!=basename or destination.exists(): raise DistributionError("fresh canonical wheel output required")
    members={}; modules=[];exports=[]
    if any(Path(p).is_relative_to(root) and str(Path(p).relative_to(root)) not in files for file in result.results for p in file.dependencies): raise DistributionError("unshipped local source dependency")
    guards=copy.deepcopy(result.guarded_exports)
    for path,raw in files.items():
        absolute=str((root/path).resolve());file=owned.get(absolute)
        if file is None: raise DistributionError("package source absent from complete check")
        encoding,_=tokenize.detect_encoding(io.BytesIO(raw).readline);source=raw.decode(encoding)
        generated_file=copy.deepcopy(file)
        generated_file.path=path
        for c in generated_file.contracts:c.path=path
        artifact=debug_source(source,generated_file,records).encode() if result.boundary_guards=="debug" else raw
        compile(artifact,str(root/path),"exec")
        members[path]=artifact;members[info+"/pyalamode/sources/"+path]=raw
        namespace=graph.module_name(absolute)
        modules.append({"module":namespace,"authored_path":path,"source_sha256":hashlib.sha256(raw).hexdigest(),"installed_path":path,"artifact_sha256":hashlib.sha256(artifact).hexdigest(),"initialization":{"source_evidence":file.initialization_evidence,"effects":[] if file.module_mode and file.verified else None,"failures":file.initialization_failures if file.module_mode and file.verified else None},"setup_observations":file.setup_observations})
        for kind,rows in (("function",[asdict(c) for c in file.contracts]),("record",file.records),("variant",file.variants)):
            for c in rows:
                selector=namespace+":"+c["name"]
                if selector in declaration["exports"]:
                    if not file.verified: raise DistributionError("unverified exported declaration")
                    exports.append({"selector":selector,"kind":kind,"declaration":selector,"contract":c,"source_location":{"path":path,"line":c["line"],"column":1,"column_encoding":"utf-8-bytes"},"guard":None})
    if {e["selector"] for e in exports}!=set(declaration["exports"]):
        from .model import diagnostic
        result.source_status=max(result.source_status or 0,1)
        result.policy_diagnostics.append(diagnostic("PAL371",str(root/"pyproject.toml"),"declared export unavailable from actual current selected source",origin="producer export declaration"))
        raise DistributionError("declared export unavailable")
    for row in result.debug_coverage:
        if row["path"] not in owned:raise DistributionError("foreign debug ownership")
    debug=[{**row,"path":str(Path(row["path"]).relative_to(root)),"generated":True} for row in result.debug_coverage]
    generated={}
    for boundary in guards:
        original,name=boundary["selection"].split(":");top,*tail=original.split(".")
        facade=top+"._pyalamode_exports"+("."+".".join(tail) if tail else "")
        boundary.update(public_boundary=facade+":"+name,generated=True)
        file=next(r for r in result.results if graph.module_name(r.path)==original)
        raw=capture["sources"][file.path]
        key=facade.replace(".","/")+("/__init__.py" if Path(file.path).name=="__init__.py" else ".py")
        group=[copy.deepcopy(c) for c in file.contracts if original+":"+c.name in policy.get("guarded_exports",[])]
        for c in group:c.path=str(Path(file.path).relative_to(root))
        generated[key]=facade_source(raw,original,group,records).encode()
        parent=Path(key).parent
        while len(parent.parts)>1:
            init=parent.as_posix()+"/__init__.py"
            generated.setdefault(init,b'"""Selected guarded boundaries."""\n');parent=parent.parent
    members.update(generated)
    policyraw=read(root/"pyproject.toml");members[info+"/pyalamode/policy.toml"]=policyraw
    deps=["pyalamode==0.1.0"]+[d["name"]+"=="+d["version"] for d in policy.get("checked_dependencies",[])]
    members[info+"/METADATA"]=("Metadata-Version: 2.1\nName: "+declaration["name"]+"\nVersion: "+declaration["version"]+"\nRequires-Python: ==3.13.1\n"+"".join("Requires-Dist: "+d+"\n" for d in sorted(deps))+"\n").encode()
    members[info+"/WHEEL"]=("Wheel-Version: 1.0\nGenerator: "+CHECKER_VERSION+"\nRoot-Is-Purelib: true\nTag: py3-none-any\n").encode()
    from .encoding_contracts import ENCODING_VERSION
    artifacts={k:{"sha256":hashlib.sha256(v).hexdigest(),"size":len(v),"role":"generated" if k in generated else "authored" if "/sources/" in k else "metadata" if k.startswith(info) else "source"} for k,v in members.items()}
    payload={"identity":{"name":declaration["name"],"version":declaration["version"],"packages":declaration["packages"],"wheel_tag":"py3-none-any"},"target":{"python":"3.13.1","implementation":"CPython","gil":"standard","platforms":["darwin-arm64","linux-aarch64"],"filesystem_encoding":"utf-8","filesystem_errors":"surrogateescape"},"producer":{"checker":CHECKER_VERSION,"edition":EDITION,"operation_contract":OPERATION_VERSION,"standard_version":"pyalamode.standard-v1","integration_version":"pyalamode.integrations-v1","encoding_version":ENCODING_VERSION,"product_artifacts":foundation_identities(),"runtime_environment":runtime_environment()},"inputs":{"policy_sha256":hashlib.sha256(policyraw).hexdigest(),"sources":{str(Path(p).relative_to(root)):{"sha256":hashlib.sha256(v).hexdigest(),"module":graph.module_name(p) if str(Path(p).relative_to(root)) in files else None,"ownership":"project","shipped":str(Path(p).relative_to(root)) in files,"participating":bool(owned[p].module_mode or owned[p].contracts or owned[p].records or owned[p].variants)} for p,v in capture["raw_sources"].items() if Path(p).is_relative_to(root)},"checked_dependencies":public_receipts(capture["distribution_snapshot"]),"integration_inputs":capture["integration_snapshot"]["inputs"],"resolution":{m["module"]:m["authored_path"] for m in modules},"selection":{graph.module_name(r.path):r.module_mode for r in result.results}},"modules":modules,"exports":exports,"guards":{"mode":result.boundary_guards,"exports":guards,"debug":debug,"generated_files":{k:hashlib.sha256(v).hexdigest() for k,v in generated.items()}},"artifacts":artifacts,"claim_scope":"Listed strict exports and characterized transitive assumptions; initialization and data guards separately stated; ordinary shells unchecked."}
    payload["claim_scope"]=CLAIM_SCOPE
    envelope={"schema":1,"kind":"pyalamode-checked-distribution","payload":payload,"sha256":digest(payload)}
    bounded(envelope);validate_evidence(envelope)
    members[info+"/pyalamode/evidence.json"]=canonical(envelope)+b"\n"
    stream=io.StringIO(newline="");writer=csv.writer(stream,lineterminator="\n")
    for name,raw in sorted(members.items()): writer.writerow([name,"sha256="+base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip("="),str(len(raw))])
    writer.writerow([info+"/RECORD","",""]);members[info+"/RECORD"]=stream.getvalue().encode()
    if len(members)>16384 or sum(len(raw)+len(name.encode())+128 for name,raw in members.items())>64*LIMIT:raise DistributionError("wheel aggregate bounds exceeded")
    destination.parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix=".pyalamode-build-",dir=destination.parent))
    try:
        temp=staging/basename
        with zipfile.ZipFile(temp,"w",compression=zipfile.ZIP_STORED) as z:
            for name,raw in sorted(members.items()):
                zi=zipfile.ZipInfo(name,(1980,1,1,0,0,0));zi.external_attr=0o100644<<16;z.writestr(zi,raw)
        receipt={"path":str(destination),"sha256":hashlib.sha256(read(temp,64*LIMIT)).hexdigest(),"size":temp.stat().st_size,"evidence_sha256":digest(envelope),"members":{k:hashlib.sha256(v).hexdigest() for k,v in members.items()},"verified":True,"status":0}
        capture["prepublish"]()
        os.link(temp,destination)
        return receipt
    finally:
        shutil.rmtree(staging)
