"""M8 reviewed external operations, current identities, latent trust and unsafe boundaries."""
import copy
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.checker import analyze_source, analyze_sources
from pyalamode.integration_contracts import integration_snapshot, operation_contract, INTEGRATION_NAMES
from pyalamode.project import check_paths, build_paths
from pyalamode import unsafe

PREFIX = '''from typing import Callable
from pyalamode import fun, effects, Effectful, IO, State, Vector, compose, partial_first, vector_scan, vector_group_by, result_traverse, Result, Ok, Err, Failure, failure_value, unsafe, freeze
from pyalamode.integrations import base64_encode, base64_decode, sha256_digest
'''


def approvals(snapshot):
    return [{"operation": row["identity"], "contract_sha256": row["contract_sha256"], "dependency_sha256": row["dependency_sha256"],
             "owner": "fixture reviewer", "rationale": "reviewed bounded attachment workflow", "provenance": "root-authorized local test fixture"} for row in snapshot["catalog"]]


def policy(root=None, **extra):
    base = {"external_trust": "approved", **extra}
    return {**base, "integration_approvals": approvals(integration_snapshot(base, root))}


def write_policy(root, data):
    text = "[tool.pyalamode]\n"
    for key, value in data.items():
        if key == "integration_approvals":
            continue
        text += key + "=" + json.dumps(value) + "\n"
    for approval in data.get("integration_approvals", []):
        text += "\n[[tool.pyalamode.integration_approvals]]\n" + "".join(key + "=" + json.dumps(value) + "\n" for key, value in approval.items())
    (root / "pyproject.toml").write_text(text)


def manifest(root, *, status="reviewed", effects=(), failures=("ValueError",)):
    baseline = next(row for row in integration_snapshot(root=root)["catalog"] if row["identity"].endswith("base64_encode"))
    row = {"schema": 1, "operation": baseline["identity"], "status": status, "base_contract_sha256": baseline["contract_sha256"],
           "effects": list(effects), "failures": list(failures), "owner": "integration owner", "rationale": "conservative review policy", "provenance": "review 2026-10-09"}
    (root / "contract.json").write_text(json.dumps(row, indent=2))
    return row


class ExternalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = policy()

    def checked(self, source, **kwargs):
        result = analyze_source(PREFIX + source, path="integrations_core.py", policy=kwargs.pop("policy", self.policy), **kwargs)
        self.assertTrue(result.verified, [d.format() for d in result.diagnostics])
        return result

    def rejected(self, source, rule=None, **kwargs):
        result = analyze_source(PREFIX + source, path="integrations_core.py", policy=kwargs.pop("policy", self.policy), **kwargs)
        self.assertFalse(result.verified)
        if rule:
            self.assertIn(rule, [d.rule for d in result.diagnostics], [d.format() for d in result.diagnostics])
        return result

    def test_three_operations_resolve_actual_alias_namespace_contracts(self):
        for name in sorted(INTEGRATION_NAMES):
            for spelling, importing in [(name, ""), ("alias", f"from pyalamode.integrations import {name} as alias\n"), ("adapter." + name, "import pyalamode.integrations as adapter\n"), ("pyalamode.integrations." + name, "import pyalamode.integrations\n")]:
                with self.subTest(name=name, spelling=spelling):
                    result = self.checked(importing + f"@fun\ndef f(data:bytes)->bytes:return {spelling}(data)\n")
                    contract = result.contracts[0]
                    self.assertEqual(contract.failures, ["ValueError"])
                    self.assertEqual(contract.required_effects, [])
                    self.assertEqual(contract.source_evidence, "checked participating source")
                    external = contract.external_assumptions[0]
                    self.assertEqual(external["identity"], "pyalamode.integrations." + name)
                    self.assertEqual(external["admission"], "approved")
                    self.assertEqual(external["approval"]["owner"], "fixture reviewer")
                    self.assertEqual(external["installed_identity"]["version"], "3.13.1")
                    self.assertEqual(set(external["installed_identity"]["native_artifacts"]), {"binascii", "_sha2"})
                    self.assertTrue(any(external["identity"] in trust for trust in contract.trust))
                    self.assertEqual(result.initialization_evidence, "unchecked ordinary module initialization")
                    self.assertTrue(any(row["phase"] == "ordinary external import setup" for row in result.setup_observations))

    def test_default_deny_absent_wrong_operation_and_stale_approvals(self):
        source = "@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n"
        for selected in [{}, {"external_trust": "approved"}, {**self.policy, "external_trust": "deny"}, {**self.policy, "integration_approvals": self.policy["integration_approvals"][:1]}]:
            self.rejected(source, "PAL350", policy=selected)
        for field in ("contract_sha256", "dependency_sha256"):
            selected = copy.deepcopy(self.policy)
            for row in selected["integration_approvals"]:
                row[field] = "0" * 64
            result = self.rejected(source, "PAL350", policy=selected)
            self.assertEqual(result.contracts[0].external_assumptions[0]["admission"], "stale")
        audited = analyze_source(PREFIX + source, path="audit.py", audit=True)
        self.assertEqual(audited.status, 0)
        self.assertFalse(audited.verified)
        self.assertTrue(any(d.rule == "PAL350" for d in audited.diagnostics))

    def test_exact_signatures_and_unsupported_native_hooks_are_refused(self):
        for call in ["base64_encode()", "base64_encode(data=b'x')", "base64_encode(b'x',b'y')", "base64_encode('x')", "base64_decode(True)", "sha256_digest(bytearray(b'x'))", "base64_encode(*data)", "compose(base64_encode,sha256_digest)"]:
            with self.subTest(call=call):
                self.rejected("@fun\ndef f(data:bytes)->bytes:return " + call + "\n")
        self.rejected("import binascii\n@fun\ndef f(data:bytes)->bytes:return binascii.b2a_base64(data)\n", "PAL230")
        self.rejected("import _sha2\n@effects(IO,State)\ndef f(data:bytes)->bytes:return _sha2.sha256(data).digest()\n")
        self.rejected("class Sub(bytes):pass\n@fun\ndef f(data:Sub)->bytes:return base64_encode(data)\n", "PAL130")
        self.rejected("base64_encode=print\n@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n", "PAL240")

    def test_import_setup_defaults_and_functional_initializers_are_distinct(self):
        source = "# mode: fun\nfrom pyalamode.integrations import base64_encode\ndef f(data:bytes)->bytes:return base64_encode(data)\n"
        result = analyze_source(source, path="init.py", policy=self.policy)
        self.assertFalse(result.verified)
        self.assertIn("PAL241", [d.rule for d in result.diagnostics])
        self.rejected("@fun\ndef f(data:bytes=base64_encode(b'x'))->bytes:return data\n", "PAL241")
        self.rejected("VALUE=base64_encode(b'x')\n@fun\ndef f()->bytes:return VALUE\n", "PAL241")
        # Importing only the package does not establish its separately imported
        # integrations namespace in ordinary execution.
        r = analyze_source("import pyalamode as p\n@p.fun\ndef f(data:bytes)->bytes:return p.integrations.base64_encode(data)\n",path="namespace.py",policy=self.policy)
        self.assertFalse(r.verified)

    def test_trust_retained_by_calls_latent_conditional_captures_and_wrappers(self):
        result = self.checked('''@fun
def encode(data:bytes)->bytes:return base64_encode(data)
@fun
def digest(data:bytes)->bytes:return sha256_digest(data)
@fun
def pair(prefix:bytes,data:bytes)->bytes:return encode(prefix+data)
@fun
def chosen(flag:bool)->Callable[[bytes],bytes]:
    if flag:return encode
    return digest
@fun
def factory()->Callable[[bytes],bytes]:return compose(digest,encode)
@fun
def captured()->Callable[[bytes],bytes]:
    callback=compose(digest,encode)
    def inner(data:bytes)->bytes:return callback(data)
    return inner
@fun
def retained()->Callable[[bytes],bytes]:return partial_first(pair,b'prefix')
@fun
def eager(values:Vector[bytes])->Vector[bytes]:return values.map(compose(digest,encode))
''')
        expected = {"pyalamode.integrations.base64_encode", "pyalamode.integrations.sha256_digest"}
        contracts = {c.name: c for c in result.contracts}
        for name in ("chosen", "factory", "captured", "captured.inner", "eager"):
            self.assertEqual({a["identity"] for a in contracts[name].external_assumptions}, expected, name)
        for name in ("chosen", "factory", "captured", "retained"):
            self.assertEqual(contracts[name].required_effects, [])
            self.assertEqual(contracts[name].failures, [])
        self.assertEqual(contracts["eager"].failures, ["ValueError"])
        self.assertEqual(len(contracts["retained"].external_assumptions), 1)

    def test_eager_toolkit_and_handling_keep_external_assumptions(self):
        result = self.checked('''@fun
def encode(data:bytes)->bytes:return base64_encode(data)
@fun
def add(total:bytes,data:bytes)->bytes:return base64_encode(total+data)
@fun
def key(data:bytes)->bytes:return sha256_digest(data)
@fun
def converted(data:bytes)->Result[bytes,Failure]:
    try:return Ok(base64_decode(data))
    except ValueError as caught:return Err(failure_value(caught))
@fun
def f(values:Vector[bytes])->Vector[bytes]:return vector_scan(values,add,b'')
@fun
def traversed(values:Vector[bytes])->Result[Vector[bytes],Failure]:return result_traverse(values,converted)
''')
        contracts = {c.name: c for c in result.contracts}
        self.assertEqual(contracts["converted"].failures, ["RecursionError"])
        self.assertEqual(contracts["converted"].external_assumptions[0]["identity"], "pyalamode.integrations.base64_decode")
        self.assertTrue(contracts["traversed"].external_assumptions)
        self.assertTrue(contracts["f"].external_assumptions)

    def test_native_error_class_private_shared_globals_and_importer_writers(self):
        writers = [
            "import binascii\nbinascii.b2a_base64=print",
            "from binascii import Error as error\nerror.__init__=print",
            "from binascii import Error as error\nerror.__bases__=()",
            "import binascii\nalias=binascii.Error.__dict__\nalias['__new__']=print",
            "import _sha2\n_sha2.SHA256Type.digest=print",
            "from pyalamode.integrations import _exact_bytes as helper\nhelper.__globals__['len']=print",
            "from pyalamode.integrations import base64_decode as sibling\nsibling.__globals__['__builtins__']['type']=print",
            "from pyalamode.integrations import _binascii as native\nnative.b2a_base64=print",
            "import pyalamode.integrations as adapter\nadapter._MAX_BYTES=0",
            "import sys\nsys.modules['binascii']=None",
            "from sys import modules as table\ntable['binascii']=None",
            "import sys\nsys.meta_path=()",
            "import sys\nsys.meta_path.append(print)",
            "from sys import path_hooks as hooks\nhooks.clear()",
            "from binascii import Error as error\nbase=error.__mro__[1]\nbase.__init__=print",
            "import binascii\nnamespace=binascii.b2a_base64.__self__.__dict__\nnamespace.update({'Error':ValueError})",
            "import _sha2\n_sha2.sha256.__self__.__dict__['_replacement']=print",
            "import _imp\n_imp.extension_suffixes=print",
            "import sys\nsys.base_prefix='elsewhere'",
            "import sys\nsys.abiflags='t'",
            "import sys\nsys.implementation.cache_tag='changed'",
            "def unknown(value):pass\nimport binascii\nunknown(binascii.Error)",
        ]
        for writer in writers:
            with self.subTest(writer=writer):
                self.rejected(writer + "\n@fun\ndef f(data:bytes)->bytes:return base64_decode(data)\n", "PAL240")

    def test_checked_module_alias_mutator_spellings_keep_external_evidence(self):
        for name in ("add", "append", "clear", "update", "pop", "__setitem__"):
            with self.subTest(name=name):
                sources = {"/tmp/m08-alias/core.py": PREFIX + f"@fun\ndef {name}(data:bytes)->bytes:return base64_encode(data)\n",
                           "/tmp/m08-alias/app.py": "from pyalamode import fun\nimport core as adapter\nfrom core import " + name + " as action\n@fun\ndef f(data:bytes)->bytes:return adapter." + name + "(action(data))\n"}
                results = analyze_sources(sources, root="/tmp/m08-alias", policy=self.policy)
                self.assertTrue(all(result.verified for result in results.values()), [d.format() for result in results.values() for d in result.diagnostics])
                self.assertEqual(results["/tmp/m08-alias/app.py"].contracts[0].external_assumptions[0]["identity"], "pyalamode.integrations.base64_encode")

    def test_unsafe_marker_identity_and_new_snapshot_computation(self):
        def original():
            return [1, 2]
        self.assertIs(unsafe(scope="application adapter", rationale="unknown ordinary hook")(original), original)
        result = self.checked('''@unsafe(scope="application adapter",rationale="uncharacterized source")
def adapter():return [1,2]
@fun
def add(total:int,item:int)->int:return total+item
@fun
def total(values:Vector[int])->int:return values.fold(add,0)
raw=adapter()
snapshot=freeze(raw,exclusive=True,schema=Vector[int])
answer=total(snapshot)
''')
        self.assertEqual(result.unsafe_adapters[0]["scope"], "application adapter")
        self.assertEqual(result.unsafe_adapters[0]["source_evidence"], "unchecked ordinary unsafe adapter")
        self.assertEqual(result.contracts[-1].external_assumptions, [])
        self.rejected('@unsafe(scope="ordinary",rationale="unknown")\ndef adapter():return 1\n@fun\ndef f()->int:return adapter()\n', "PAL230")
        self.rejected('@unsafe(scope="ordinary",rationale="unknown")\ndef adapter():return 1\n@effects(IO,State)\ndef f()->int:return adapter()\n', "PAL230")
        self.rejected('@unsafe(scope="ordinary",rationale="unknown")\n@fun\ndef f()->int:return 1\n', "PAL351")
        self.rejected('@unsafe(scope="",rationale="unknown")\ndef adapter():return 1\n', "PAL351")
        self.rejected('@unsafe(scope="ordinary",rationale="unknown")\ndef adapter():return [1]\n@fun\ndef f(v:Vector[int])->int:return len(v)\nraw=adapter()\nsnapshot=freeze(raw,schema=Vector[int])\nanswer=f(snapshot)\n', "PAL221")


class ExternalPolicyProject(unittest.TestCase):
    def test_sysconfig_selectors_and_shadows_never_execute_in_fresh_tooling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source = root / "core.py"
            source.write_text(PREFIX + "@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n")
            selected = policy(root)
            write_policy(root, selected)
            sentinel = root / "sentinel"
            hook = "from pathlib import Path\nPath(" + repr(str(sentinel)) + ").write_text('executed')\nbuild_time_vars={}\n"
            defaults = list((Path(sys.base_prefix) / "lib/python3.13").glob("_sysconfigdata*.py"))
            self.assertTrue(defaults, "supported installation contains static config-data bytes")
            for name in ["m08_config_hook.py", "sysconfig.py", *(path.name for path in defaults)]:
                (root / name).write_text(hook)
            base_env = dict(os.environ)
            base_env["PYTHONPATH"] = os.pathsep.join([str(root), str(Path(__file__).resolve().parents[1])])
            for key in ("_PYTHON_SYSCONFIGDATA_NAME", "_PYTHON_SYSCONFIGDATA_PATH", "_PYTHON_PROJECT_BASE", "_PYTHON_HOST_PLATFORM"):
                base_env.pop(key, None)
            environments = [base_env, {**base_env, "_PYTHON_SYSCONFIGDATA_NAME": "m08_config_hook", "_PYTHON_SYSCONFIGDATA_PATH": str(root), "_PYTHON_PROJECT_BASE": str(root), "_PYTHON_HOST_PLATFORM": "untrusted-config-selector"}]
            snapshot_command = "from pyalamode.integration_contracts import integration_snapshot; from pathlib import Path; import json; print(json.dumps(integration_snapshot(root=Path(" + repr(str(root)) + "))))"
            for index, environment in enumerate(environments):
                with self.subTest(selectors=index):
                    direct = subprocess.run([sys.executable, "-c", snapshot_command], env=environment, capture_output=True, text=True)
                    self.assertEqual(direct.returncode, 0, direct.stderr)
                    snapshot = json.loads(direct.stdout)
                    self.assertTrue(all(row["installed_identity"] is not None and row["admission"] == "denied" for row in snapshot["catalog"]))
                    for command in [("check", str(source)), ("build", str(source), "--output", str(root / ("artifact-" + str(index)))), ("explain", "integrations")]:
                        executed = subprocess.run([sys.executable, "-m", "pyalamode", *command, "--root", str(root), "--json"], env=environment, capture_output=True, text=True)
                        self.assertEqual(executed.returncode, 0, executed.stdout + executed.stderr)
                    self.assertFalse(sentinel.exists())

    def test_missing_supported_layout_refuses_without_valid_identity(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(sys, "base_prefix", tmp):
            snapshot = integration_snapshot()
            self.assertTrue(all(row["admission"] == "unresolved" and row["dependency_sha256"] is None and row["installed_identity"] is None for row in snapshot["catalog"]))

    def test_detached_installed_identity_reads_actual_bytes_without_dependency_import(self):
        with patch("importlib.util.find_spec", side_effect=AssertionError("finder executed")), patch("importlib.import_module", side_effect=AssertionError("dependency imported")):
            snapshot = integration_snapshot()
        self.assertEqual(snapshot["errors"], [])
        for row in snapshot["catalog"]:
            identity = row["installed_identity"]
            self.assertIsNotNone(identity)
            for artifact in [*identity["native_artifacts"].values(), identity["adapter_artifact"], identity["interpreter_executable"], identity["interpreter_core"]]:
                self.assertEqual(artifact["sha256"], hashlib.sha256(Path(artifact["path"]).read_bytes()).hexdigest())
            self.assertEqual(len(row["contract_sha256"]), 64)
            self.assertEqual(len(row["dependency_sha256"]), 64)
        snapshot["catalog"][0]["initialization"]["effects"].append("State")
        self.assertEqual(operation_contract("base64_decode")["initialization"]["effects"], ["IO"])

    def test_snapshot_expiry_is_exact_utc_and_approval_metadata_is_visible(self):
        now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
        selected = policy()
        for row in selected["integration_approvals"]:
            row["expires_at"] = "2026-10-09T12:00:00Z"
        before = integration_snapshot(selected, now=now-timedelta(seconds=1))
        after = integration_snapshot(selected, now=now)
        self.assertTrue(all(row["admission"] == "approved" for row in before["catalog"]))
        self.assertTrue(all(row["admission"] == "expired" for row in after["catalog"]))
        self.assertTrue(all(row["expiry"] == "2026-10-09T12:00:00Z" for row in after["approvals"]))

    def test_malformed_approvals_and_manifests_are_tooling_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve(); source = root / "core.py"; source.write_text(PREFIX + "@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n")
            good = policy(root)
            samples = []
            bad = copy.deepcopy(good); bad["integration_approvals"][0].pop("owner"); samples.append(bad)
            bad = copy.deepcopy(good); bad["integration_approvals"].append(bad["integration_approvals"][0]); samples.append(bad)
            bad = copy.deepcopy(good); bad["integration_approvals"][0]["expires_at"] = "2026-10-09"; samples.append(bad)
            bad = copy.deepcopy(good); bad["integration_approvals"][0]["unexpected"] = True; samples.append(bad)
            bad = {**good, "integration_manifests": ["../foreign.json"]}; samples.append(bad)
            for selected in samples:
                write_policy(root, selected)
                result = check_paths([source], root=root)
                self.assertEqual(result.status, 2, result.to_dict())
            row = manifest(root, effects=("Unknown",))
            write_policy(root, {**good, "integration_manifests": ["contract.json"]})
            self.assertEqual(check_paths([source],root=root).status, 2)
            row["effects"] = []; row["failures"] = []
            (root / "contract.json").write_text(json.dumps(row))
            self.assertEqual(check_paths([source],root=root).status, 2)

    def test_drafts_and_conservative_effect_overrides_preserve_handlers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'
            row=manifest(root,effects=("IO",))
            selected=policy(root,integration_manifests=["contract.json"]); write_policy(root,selected)
            source.write_text(PREFIX+'''@effects(IO)
def f(data:bytes)->bytes:
    try:return base64_encode(data)
    except ValueError:return b'failed'
@effects(IO)
def outer(data:bytes)->bytes:return f(data)
''')
            result=check_paths([source],root=root)
            self.assertEqual(result.status,0,[d.format() for file in result.results for d in file.diagnostics])
            for contract in result.results[0].contracts:
                self.assertEqual(contract.required_effects,["IO"])
                self.assertEqual(contract.failures,[])
                self.assertEqual(contract.external_assumptions[0]["effects"],["IO"])
                self.assertEqual(contract.external_assumptions[0]["provenance"]["kind"],"project-local conservative override")
            source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n")
            self.assertEqual(check_paths([source],root=root).status,1)
            row['status']='draft'; (root/'contract.json').write_text(json.dumps(row))
            write_policy(root,policy(root,integration_manifests=['contract.json']))
            denied=check_paths([source],root=root)
            self.assertEqual(denied.status,1)
            self.assertTrue(any(d.rule=='PAL350' for file in denied.results for d in file.diagnostics))

    def test_project_native_product_shadows_do_not_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'; source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return sha256_digest(data)\n")
            write_policy(root,policy(root))
            for relative in ('binascii.py','_sha2.py','pyalamode/__init__.py'):
                path=root/relative; path.parent.mkdir(exist_ok=True); path.write_text("raise RuntimeError('DEPENDENCY HOOK EXECUTED')\n")
                snapshot=integration_snapshot(root=root)
                self.assertTrue(all(row['admission']=='unresolved' for row in snapshot['catalog']))
                result=check_paths([source],root=root)
                self.assertEqual(result.status,1)
                path.unlink()
                if path.parent!=root:path.parent.rmdir()
            # Extensionless files are ordinary console/script data, not import
            # candidates; a package directory with the same spelling is.
            for name in ("pyalamode", "binascii", "_sha2"):
                (root / name).write_text("raise RuntimeError('not importable')\n")
            self.assertTrue(all(row["installed_identity"] is not None for row in integration_snapshot(root=root)["catalog"]))

    def test_check_expiry_crossing_guard_planning_keeps_current_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'; source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n")
            selected=policy(root)
            for entry in selected['integration_approvals']:entry['expires_at']='2030-01-01T00:00:00Z'
            write_policy(root,selected)
            now=[datetime(2029,1,1,tzinfo=timezone.utc)]
            def advance(*args):now[0]=datetime(2030,1,1,tzinfo=timezone.utc)
            with patch('pyalamode.project._guard_plan',side_effect=advance), patch('pyalamode.project.integration_snapshot',side_effect=lambda p,r:integration_snapshot(p,r,now=now[0])):
                checked=check_paths([source],root=root)
            self.assertEqual(checked.status,1)
            contract=checked.results[0].contracts[0]
            self.assertEqual(contract.external_assumptions[0]['admission'],'expired')
            self.assertTrue(any('approval=expired' in entry for entry in contract.trust))
            self.assertFalse(any('approval=approved' in entry for entry in contract.trust))

    def test_full_partial_cache_keeps_rich_latent_evidence_and_installed_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); leaf=root/'leaf.py'; caller=root/'caller.py'; unrelated=root/'unrelated.py'
            leaf.write_text(PREFIX+"@fun\ndef encode(data:bytes)->bytes:return base64_encode(data)\n@fun\ndef digest(data:bytes)->bytes:return sha256_digest(data)\n@fun\ndef factory()->Callable[[bytes],bytes]:return compose(digest,encode)\n")
            caller.write_text("from typing import Callable\nfrom pyalamode import fun\nfrom leaf import factory\n@fun\ndef f(data:bytes)->bytes:\n    action=factory()\n    return action(data)\n")
            unrelated.write_text("from pyalamode import fun\n@fun\ndef g(value:int)->int:return value+1\n")
            write_policy(root,policy(root))
            cold=check_paths([root],root=root); warm=check_paths([root],root=root)
            self.assertEqual(cold.status,0); self.assertEqual(warm.status,0)
            def contracts(result):return {file.path:[c.__dict__ for c in file.contracts] for file in result.results}
            self.assertEqual(contracts(cold),contracts(warm))
            self.assertTrue(all(file.cache_hit for file in warm.results))
            caller.write_text(caller.read_text()+'\n# caller edit\n')
            partial=check_paths([root],root=root)
            self.assertEqual(partial.status,0); self.assertEqual(contracts(partial),contracts(check_paths([root],root=root,cache=False)))
            real_read=Path.read_bytes
            native=next(iter(warm.integration_catalog[0]['installed_identity']['native_artifacts'].values()))['path']
            def changed_read(path):
                raw=real_read(path)
                return raw+b'changed installed artifact' if str(path.resolve())==native else raw
            with patch.object(Path,'read_bytes',changed_read):
                stale=check_paths([root],root=root)
            self.assertEqual(stale.status,1)
            self.assertTrue(next(file for file in stale.results if file.path==str(unrelated)).cache_hit)
            self.assertFalse(next(file for file in stale.results if file.path==str(caller)).cache_hit)
            self.assertTrue(any(d.rule=='PAL350' for file in stale.results for d in file.diagnostics))

    def test_expired_approval_cannot_reuse_warm_body_or_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'; source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n")
            selected=policy(root)
            for entry in selected['integration_approvals']:entry['expires_at']='2030-01-01T00:00:00Z'
            write_policy(root,selected)
            self.assertEqual(check_paths([source],root=root).status,0)
            real_snapshot=integration_snapshot
            with patch('pyalamode.project.integration_snapshot',side_effect=lambda p,r:real_snapshot(p,r,now=datetime(2030,1,1,tzinfo=timezone.utc))):
                result=check_paths([source],root=root)
                built=build_paths([source],root=root,output=root/'failed')
            self.assertEqual(result.status,1); self.assertFalse(result.results[0].cache_hit)
            self.assertEqual(built.status,1); self.assertFalse((root/'failed').exists())

    def test_build_rechecks_identity_and_expiry_after_successful_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'; source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return base64_encode(data)\n")
            selected=policy(root)
            for entry in selected['integration_approvals']:entry['expires_at']='2030-01-01T00:00:00Z'
            write_policy(root,selected)
            calls=0
            def advancing(p,r):
                nonlocal calls
                calls+=1
                return integration_snapshot(p,r,now=datetime(2029,1,1,tzinfo=timezone.utc) if calls<=2 else datetime(2030,1,1,tzinfo=timezone.utc))
            with patch('pyalamode.project.integration_snapshot',side_effect=advancing):
                result=build_paths([source],root=root,output=root/'failed')
            self.assertEqual(result.status,1)
            self.assertFalse((root/'failed').exists())

    def test_analyzed_writer_invalidates_previously_warm_external_bodies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'; source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return base64_decode(data)\n")
            write_policy(root,policy(root)); self.assertEqual(check_paths([root],root=root).status,0)
            self.assertTrue(check_paths([root],root=root).results[0].cache_hit)
            (root/'writer.py').write_text("from binascii import Error as error\nnamespace=error.__dict__\nnamespace.update({'__init__':print})\n")
            result=check_paths([root],root=root)
            self.assertEqual(result.status,1)
            core=next(file for file in result.results if file.path==str(source))
            self.assertFalse(core.cache_hit); self.assertIn('PAL240',[d.rule for d in core.diagnostics])

    def test_actual_cli_build_guard_modes_and_rejected_nonexecuting_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve(); source=root/'core.py'; source.write_text(PREFIX+"@fun\ndef f(data:bytes)->bytes:return base64_decode(base64_encode(data))\n")
            for mode in ('off','exports','debug'):
                selected=policy(root,boundary_guards=mode,**({'guarded_exports':['core:f']} if mode!='off' else {})); write_policy(root,selected)
                output=root/('artifact-'+mode)
                run=subprocess.run([sys.executable,'-m','pyalamode','build',str(source),'--root',str(root),'--output',str(output),'--json'],capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                evidence=json.loads((output/'pyalamode-evidence.json').read_text())
                self.assertEqual(len(evidence['files'][0]['contracts'][0]['external_assumptions']),2)
                imported='core' if mode=='off' else 'pyalamode_exports.core'
                command=f"from {imported} import f; assert f(b'attachment')==b'attachment'"
                if mode!='off':command+="\ntry:f(bytearray(b'bad'))\nexcept TypeError:pass\nelse:raise AssertionError('guard accepted mutable input')"
                executed=subprocess.run([sys.executable,'-c',command],cwd=output,capture_output=True,text=True)
                self.assertEqual(executed.returncode,0,executed.stdout+executed.stderr)
                if mode=='off':self.assertEqual((output/'core.py').read_bytes(),source.read_bytes())
            explanation=subprocess.run([sys.executable,'-m','pyalamode','explain','base64_decode','--root',str(root),'--json'],capture_output=True,text=True)
            self.assertEqual(explanation.returncode,0,explanation.stderr)
            self.assertEqual(json.loads(explanation.stdout)['catalog'][0]['admission'],'approved')
            sentinel=root/'sentinel'; source.write_text(f"from pyalamode import fun\n@fun\ndef f(x:int=open({str(sentinel)!r},'w').write('executed'))->int:return x\n")
            rejected=subprocess.run([sys.executable,'-m','pyalamode','build',str(source),'--root',str(root),'--output',str(root/'failed')],capture_output=True,text=True)
            self.assertEqual(rejected.returncode,1,rejected.stdout+rejected.stderr)
            self.assertFalse(sentinel.exists()); self.assertFalse((root/'failed').exists())


if __name__ == '__main__':
    unittest.main()
