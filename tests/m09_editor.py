"""M9 shared-engine editor, ownership, authored ranges, previews and wire gates."""

import copy
from datetime import datetime, timezone, timedelta
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.editor import EditorSession, ProtocolError, position, _frame, _read_frame, serve
from pyalamode.integration_contracts import integration_snapshot
from pyalamode.model import Diagnostic, foundation_identities
from pyalamode.project import check_paths, check_snapshot, build_paths

SCALAR = "# mode: fun\n\ndef f(value: int) -> int:\n    return value + 1\n"
REBIND = "# mode: fun\n\ndef f(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n"
UPDATE = "# mode: fun\nfrom pyalamode import Vector\n\ndef f(values: Vector[int]) -> Vector[int]:\n    values.appended(1)\n    return values\n"


class EditorCase(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.path = self.root / "core.py"
        self.path.write_text(SCALAR)
        self.session = EditorSession(self.root)
        self.metadata = self.session.handle("initialize", {"rootUri": self.root.as_uri()})

    def open(self, text, version=1, path=None):
        path = path or self.path
        self.session.handle("textDocument/didOpen", {"textDocument": {"uri": path.as_uri(), "languageId": "python", "version": version, "text": text}})

    def change(self, text, version, path=None):
        path = path or self.path
        self.session.handle("textDocument/didChange", {"textDocument": {"uri": path.as_uri(), "version": version}, "contentChanges": [{"text": text}]})

    def project(self, **params):
        return self.session.handle("pyalamode/project", params)

    def preview_request(self):
        report = self.project()
        item = next(row for row in report["diagnostics"] if row["code"] in {"PAL101", "PAL250"})
        return {"uri": self.path.as_uri(), "version": self.session.documents[str(self.path)]["version"],
                "snapshot": report["snapshot"], "diagnosticIndex": item["data"]["diagnosticIndex"]}

    def test_actual_provenance_and_historical_diagnostic_defaults(self):
        meta = self.metadata["capabilities"]["experimental"]["pyalamode"]
        self.assertEqual(meta["pythonExecutable"], sys.executable)
        self.assertEqual(meta["pythonVersion"], [3, 13, 1])
        self.assertEqual(meta["root"], str(self.root))
        self.assertEqual(self.metadata["capabilities"]["positionEncoding"], "utf-16")
        old = Diagnostic("PAL101", "x.py", 2, 3, "f", "static", "reason", "repair")
        self.assertIsNone(old.end_line)
        self.assertEqual(old.column_encoding, "utf-8-bytes")
        self.assertIn("editor.py", foundation_identities())

    def test_command_editor_diagnostics_share_authored_fields_cold_warm(self):
        self.path.write_text(REBIND)
        expected = check_paths([self.root], root=self.root, cache=False).results[0].diagnostics[0]
        for _ in range(2):
            report = self.project()
            item = next(row for row in report["diagnostics"] if row["code"] == "PAL101")
            self.assertEqual(item["data"]["authored"], {key: getattr(expected, key) for key in ("path", "line", "column", "end_line", "end_column", "column_encoding")})
            self.assertEqual(item["data"]["reason"], expected.reason)
            self.assertEqual(item["data"]["remediation"], expected.remediation)
            self.assertEqual(item["data"]["boundary"], expected.boundary)
            self.assertEqual(item["data"]["origin"], expected.origin)
            self.assertEqual(report["report"]["status"], 1)
            self.assertIn("first binding", item["relatedInformation"][0]["message"])

    def test_unicode_astral_crlf_and_final_line_ranges(self):
        text = "# mode: fun\n\ndef f(値: int) -> int:\n    pair = ('😀', missing(値))\n    return 値"
        for value in (text, text.replace("\n", "\r\n"), text.replace("\n", "\r")):
            self.path.write_bytes(value.encode())
            report = self.project()
            item = next(row for row in report["diagnostics"] if row["code"] == "PAL230")
            self.assertEqual(item["range"]["start"], {"line": 3, "character": 18})
            self.assertEqual(item["range"]["end"], {"line": 3, "character": 28})
            self.assertEqual(item["data"]["authored"]["column"], 21)
        self.assertEqual(position("😀 café", 1, 6), {"line": 0, "character": 3})
        self.assertEqual(position("😀 café", 1, 3, "unicode-codepoints"), {"line": 0, "character": 3})

    def test_tokenize_directive_coordinates_and_syntax_fallback(self):
        text = "value = '😀'; # mode: fun\n"
        self.path.write_text(text)
        item = next(row for row in self.project()["diagnostics"] if row["code"] == "PAL121")
        self.assertEqual(item["data"]["authored"]["column_encoding"], "unicode-codepoints")
        self.assertEqual(item["range"]["start"]["character"], len(text[:text.index("#")].encode("utf-16-le")) // 2)
        self.path.write_text("def broken(:\n")
        report = self.project()
        self.assertEqual(report["report"]["status"], 2)
        self.assertTrue(all(item["code"] == "PAL001" for item in report["diagnostics"]))
        self.assertEqual(report["diagnostics"][0]["data"]["authored"]["column_encoding"], "unicode-codepoints")

    def test_versions_overlays_and_close_restore_disk(self):
        self.open(SCALAR)
        clean = self.project()
        self.change(REBIND, 2)
        failed = self.project()
        self.assertEqual(failed["report"]["status"], 1)
        self.assertNotEqual(clean["snapshot"], failed["snapshot"])
        self.assertEqual(failed["inputs"]["sources"][str(self.path)]["origin"], "overlay")
        self.assertFalse(failed["report"]["files"][0]["contracts"][0]["source_evidence"].startswith("checked"))
        for version in (1, 2, True):
            with self.assertRaises(ProtocolError):
                self.change(SCALAR, version)
        self.change(SCALAR, 3)
        self.assertEqual(self.project()["report"]["status"], 0)
        self.session.handle("textDocument/didClose", {"textDocument": {"uri": self.path.as_uri()}})
        self.assertEqual(self.project()["freshness"], "current disk snapshot")
        self.assertEqual(self.path.read_text(), SCALAR)

    def test_dependency_overlay_and_ordinary_writer_are_full_project_inputs(self):
        dependency = self.root / "dependency.py"
        dependency.write_text(SCALAR.replace("def f", "def leaf"))
        caller = "# mode: fun\nfrom dependency import leaf\n\ndef f(value: int) -> int:\n    return leaf(value)\n"
        self.path.write_text(caller)
        self.open(caller)
        self.open(dependency.read_text(), path=dependency)
        self.assertEqual(self.project()["report"]["status"], 0)
        self.change(dependency.read_text().replace("value + 1", "missing(value)"), 2, path=dependency)
        self.assertEqual(self.project()["report"]["status"], 1)
        self.change(dependency.read_text(), 3, path=dependency)
        writer = self.root / "writer.py"
        writer.write_text("import dependency\ndef ordinary(value):return value\ndependency.leaf = ordinary\n")
        report = self.project()
        self.assertEqual(report["report"]["status"], 1)
        self.assertIn("PAL240", [row["code"] for row in report["diagnostics"]])
        writer.unlink()
        self.assertEqual(self.project()["report"]["status"], 0)

    def test_audit_tooling_and_empty_coverage_never_certify(self):
        self.path.write_text(REBIND)
        audit = self.project(audit=True)
        self.assertEqual(audit["report"]["status"], 0)
        self.assertFalse(audit["report"]["verified"])
        self.assertEqual(audit["diagnostics"][0]["severity"], 2)
        (self.root / "pyproject.toml").write_text("[tool.pyalamode]\nunknown=true\n")
        self.assertEqual(self.project()["report"]["status"], 2)
        (self.root / "pyproject.toml").unlink()
        self.path.write_text("def ordinary(value):return value\n")
        report = self.project(audit=False)
        self.assertEqual(report["report"]["coverage"]["selected_functions"], 0)
        self.assertEqual(report["regions"], [])
        with patch("pyalamode.project.runtime_error", return_value="unsupported test target"):
            self.assertEqual(self.project()["report"]["status"], 2)

    def test_snapshot_source_policy_races_and_loaded_product_change_refuse(self):
        original = self.path.read_bytes
        def changed():
            raw = original()
            self.path.write_text(SCALAR.replace("+ 1", "+ 2"))
            return raw
        with patch.object(Path, "read_bytes", autospec=True, side_effect=lambda path: changed() if path == self.path else original_for(path)):
            # Keep a concrete real filesystem race rather than changing results.
            snapshot = check_snapshot([self.root], root=self.root, cache=False)
        self.assertEqual(snapshot.result.status, 2)
        self.assertEqual(snapshot.freshness, "stale; recheck required")
        self.assertTrue(snapshot.result.results)
        self.assertTrue(all(not file.to_dict()["verified"] and file.to_dict()["status"] == 2 for file in snapshot.result.results))
        products = foundation_identities()
        with patch("pyalamode.editor.foundation_identities", return_value={**products, "editor.py": "changed"}):
            replacement = EditorSession(self.root)
        replacement.handle("initialize", {"rootUri": self.root.as_uri()})
        report = replacement.handle("pyalamode/project")
        self.assertEqual(report["report"]["status"], 2)
        self.assertTrue(all(not file["verified"] and file["status"] == 2 for file in report["report"]["files"]))
        self.assertTrue(any("restart required" in row["message"] for row in report["diagnostics"]))

    def test_source_policy_and_transitive_symlink_refuse_before_read(self):
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory).resolve()
            source = outside / "outside.py"
            source.write_text("SECRET_OUTSIDE_CONTENT\n")
            policy = outside / "policy.toml"
            policy.write_text("SECRET_OUTSIDE_POLICY\n")
            for kind in ("selected", "dependency", "policy"):
                for path in (self.root / "linked.py", self.root / "dependency.py", self.root / "pyproject.toml"):
                    if path.is_symlink():
                        path.unlink()
                self.path.write_text(SCALAR)
                if kind == "selected":
                    (self.root / "linked.py").symlink_to(source)
                elif kind == "dependency":
                    (self.root / "dependency.py").symlink_to(source)
                    self.path.write_text("# mode: fun\nimport dependency\n" + SCALAR.split("\n", 1)[1])
                else:
                    (self.root / "pyproject.toml").symlink_to(policy)
                read = Path.read_bytes
                text_read = Path.read_text
                def guarded(path, *args, **kwargs):
                    self.assertFalse(path.resolve().is_relative_to(outside), "outside bytes read")
                    return read(path, *args, **kwargs)
                def guarded_text(path, *args, **kwargs):
                    self.assertFalse(path.resolve().is_relative_to(outside), "outside text read")
                    return text_read(path, *args, **kwargs)
                with patch.object(Path, "read_bytes", guarded), patch.object(Path, "read_text", guarded_text):
                    snapshot = check_snapshot([self.root], root=self.root, cache=False)
                    if kind == "policy":
                        self.assertEqual(self.session.handle("pyalamode/explain", {"symbol": "integrations"})["status"], 2)
                self.assertEqual(snapshot.result.status, 2, kind)
                self.assertNotIn("SECRET", json.dumps(snapshot.result.to_dict()))

    def test_policy_and_product_capture_races_invalidate_each_file_claim(self):
        from pyalamode import project
        policy = self.root / "pyproject.toml"
        policy.write_text("[tool.pyalamode]\n")
        identity = project._policy_identity
        calls = 0
        def changing_policy(root):
            nonlocal calls
            value = identity(root)
            calls += 1
            if calls == 1:
                policy.write_text("[tool.pyalamode]\n# changed during capture\n")
            return value
        with patch("pyalamode.project._policy_identity", side_effect=changing_policy):
            captured = check_snapshot([self.root], root=self.root, cache=False)
        self.assertEqual(captured.result.status, 2)
        self.assertTrue(all(not row["verified"] and row["status"] == 2 for row in captured.result.to_dict()["files"]))
        products = foundation_identities()
        with patch("pyalamode.project.foundation_identities", side_effect=[products, {**products, "editor.py": "changed during capture"}]):
            captured = check_snapshot([self.root], root=self.root, cache=False)
        self.assertEqual(captured.result.status, 2)
        self.assertTrue(all(not row["verified"] and row["status"] == 2 for row in captured.result.to_dict()["files"]))

    def test_uri_and_position_ownership_negative_cases(self):
        self.open(SCALAR)
        for uri in ("file:///outside.py", "file://host/tmp/a.py", self.path.as_uri() + "?x=1", "untitled:test", self.path.as_uri() + "%Q0"):
            with self.assertRaises(ProtocolError):
                self.session.handle("textDocument/documentSymbol", {"textDocument": {"uri": uri}})
        for point in ({"line": True, "character": 0}, {"line": 99, "character": 0}, {"line": 0, "character": -1}):
            with self.assertRaises(ProtocolError):
                self.session.handle("textDocument/hover", {"textDocument": {"uri": self.path.as_uri()}, "position": point})

    def test_resolved_nested_and_import_alias_navigation(self):
        source = "# mode: fun\n\ndef leaf(value:int)->int:return value+1\ndef outer(value:int)->int:\n    def leaf(value:int)->int:return value+2\n    return leaf(value)\ndef another(leaf:int)->int:return leaf\ndef caller(value:int)->int:return leaf(value)\n"
        self.path.write_text(source)
        def query(line, character):
            return self.session.handle("textDocument/definition", {"textDocument": {"uri": self.path.as_uri()}, "position": {"line": line, "character": character}})
        self.assertEqual(query(5, 12)[0]["range"]["start"], {"line": 4, "character": 8})
        self.assertEqual(query(7, 36)[0]["range"]["start"], {"line": 2, "character": 4})
        self.assertEqual(query(6, 36), [])
        references = self.session.handle("textDocument/references", {"textDocument": {"uri": self.path.as_uri()}, "position": {"line": 4, "character": 9}, "context": {"includeDeclaration": True}})
        self.assertEqual(len(references), 2)
        dependency = self.root / "dep.py"
        dependency.write_text(SCALAR.replace("def f", "def leaf"))
        self.path.write_text("# mode: fun\nfrom dep import leaf as café\ndef f(値:int)->int:return café(値)\n")
        self.assertEqual(query(2, 26)[0]["uri"], dependency.as_uri())

    def test_package_before_module_navigation_independent_of_discovery_order(self):
        dependency = self.root / "dependency.py"
        dependency.write_text(SCALAR.replace("def f", "def leaf"))
        caller = "# mode: fun\nfrom dependency import leaf as café\ndef f(value:int)->int:return café(value)\n"
        self.path.write_text(caller)
        self.open(dependency.read_text(), path=dependency)
        request = {"textDocument": {"uri": self.path.as_uri()}, "position": {"line": 2, "character": 29}}
        self.assertEqual(self.session.handle("textDocument/definition", request)[0]["uri"], dependency.as_uri())
        package = self.root / "dependency"
        package.mkdir()
        initializer = package / "__init__.py"
        initializer.write_text(dependency.read_text().replace("+ 1", "+ 2"))
        self.assertEqual(self.session.handle("textDocument/definition", request)[0]["uri"], initializer.as_uri())
        self.assertEqual(self.project()["report"]["status"], 0)
        from pyalamode.checker import analyze_sources
        sources = {str(self.path): caller, str(dependency): dependency.read_text(), str(initializer): initializer.read_text()}
        for ordered in (sources, dict(reversed(list(sources.items())))):
            results = analyze_sources(ordered, root=self.root)
            contract = results[str(self.path)].contracts[0]
            self.assertEqual(contract.invoked_targets, [str(initializer) + "::leaf"])
        # Normal Python confirms the selected authored target independently.
        result = subprocess.run([sys.executable, "-c", "import dependency;print(dependency.leaf(10))"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "12\n")
        policy = self.root / "pyproject.toml"
        policy.write_text('[tool.pyalamode]\nboundary_guards="exports"\nguarded_exports=["core:f"]\n')
        guarded = self.project()
        self.assertEqual(guarded["report"]["status"], 2)
        self.assertTrue(any("ambiguous duplicate module identities" in item["reason"] for item in guarded["report"]["tooling"]))
        policy.unlink()
        initializer.write_text('# mode: fun\n\ndef leaf(value:int)->str:\n    return "package"\n')
        report = self.project()
        self.assertEqual(report["report"]["status"], 1)
        caller_file = next(row for row in report["report"]["files"] if row["path"] == str(self.path))
        self.assertFalse(caller_file["verified"])
        self.assertIn("PAL211", [row["rule"] for row in caller_file["diagnostics"]])

    def test_package_record_schema_defaults_and_capture_override_shadow_type(self):
        module = self.root / "dependency.py"
        package = self.root / "dependency"
        package.mkdir()
        initializer = package / "__init__.py"
        prefix = "# mode: fun\nfrom pyalamode import record\n@record\nclass Item:\n"
        module.write_text(prefix + "    payload:int=1\n")
        initializer.write_text(prefix + '    payload:str="package"\n')
        self.path.write_text("# mode: fun\nfrom dependency import Item\ndef f(item:Item)->str:\n    def captured()->str:return item.payload\n    return captured()\n")
        report = self.project()
        files = {row["path"]: row for row in report["report"]["files"]}
        self.assertEqual(report["report"]["status"], 1)
        self.assertTrue(files[str(self.path)]["verified"])
        self.assertTrue(files[str(initializer)]["verified"])
        self.assertEqual(files[str(initializer)]["records"][0]["fields"], {"payload": "str"})
        self.assertEqual(files[str(initializer)]["records"][0]["defaults"], {"payload": "str"})
        self.assertEqual(files[str(module)]["records"][0]["fields"], {"payload": "int"})
        self.assertFalse(files[str(module)]["verified"])
        self.assertIn("PAL241", [row["rule"] for row in files[str(module)]["diagnostics"]])
        self.assertIn(str(initializer), files[str(self.path)]["dependencies"])
        captured = next(row for row in files[str(self.path)]["contracts"] if row["name"] == "f.captured")
        self.assertEqual(captured["captures"], {"item": "Record['dependency:Item']"})
        self.assertEqual(captured["returns"], "str")
        from pyalamode.checker import analyze_sources
        sources = {str(self.path): self.path.read_text(), str(module): module.read_text(), str(initializer): initializer.read_text()}
        for ordered in (sources, dict(reversed(list(sources.items())))):
            result = analyze_sources(ordered, root=self.root)
            self.assertTrue(result[str(self.path)].verified)
            self.assertEqual(result[str(initializer)].records[0]["fields"], {"payload": "str"})
        # Returning int from the actually selected str payload must not pass.
        self.path.write_text("# mode: fun\nfrom dependency import Item\ndef f(item:Item)->int:return item.payload\n")
        caller = next(row for row in self.project()["report"]["files"] if row["path"] == str(self.path))
        self.assertFalse(caller["verified"])
        self.assertIn("PAL211", [row["rule"] for row in caller["diagnostics"]])

    def test_package_oneof_cases_and_guard_schemas_override_shadow_catalog(self):
        module = self.root / "dependency.py"
        package = self.root / "dependency"
        package.mkdir()
        initializer = package / "__init__.py"
        prefix = "# mode: fun\nfrom pyalamode import oneof,case\n@oneof\nclass Choice:\n    @case\n    class Found:\n"
        module.write_text(prefix + "        payload:int=1\n    @case\n    class Extra:pass\n")
        initializer.write_text(prefix + '        payload:str="package"\n')
        self.path.write_text("# mode: fun\nfrom dependency import Choice\ndef f(item:Choice)->str:\n    match item:\n        case Choice.Found(payload=value):return value\n")
        report = self.project()
        files = {row["path"]: row for row in report["report"]["files"]}
        self.assertTrue(files[str(self.path)]["verified"])
        self.assertEqual(files[str(initializer)]["oneofs"][0]["cases"]["Found"]["fields"], {"payload": "str"})
        self.assertEqual(set(files[str(initializer)]["oneofs"][0]["cases"]), {"Found"})
        self.assertEqual(set(files[str(module)]["oneofs"][0]["cases"]), {"Found", "Extra"})
        self.assertFalse(files[str(module)]["verified"])
        self.assertIn("PAL241", [row["rule"] for row in files[str(module)]["diagnostics"]])
        self.path.write_text(self.path.read_text().replace("->str:", "->int:"))
        caller = next(row for row in self.project()["report"]["files"] if row["path"] == str(self.path))
        self.assertIn("PAL211", [row["rule"] for row in caller["diagnostics"]])
        self.path.write_text(self.path.read_text().replace("->int:", "->str:"))
        # A selected narrow build includes only actual resolved dependencies; its
        # generated data guard must validate the package's exact str case schema.
        (self.root / "pyproject.toml").write_text('[tool.pyalamode]\nboundary_guards="exports"\nguarded_exports=["core:f"]\n')
        built = build_paths([self.path], root=self.root, output=self.root / "build" / "canonical")
        self.assertEqual(built.status, 0, [item.format() for item in built.tooling])
        script = "from dependency import Choice\nfrom pyalamode_exports.core import f\nprint(f(Choice.Found()))\ntry:Choice.Found(1)\nexcept TypeError:print('exact-str-refused-int')\nelse:raise AssertionError('wrong payload admitted')\n"
        result = subprocess.run([sys.executable, "-c", script], cwd=self.root / "build" / "canonical", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "package\nexact-str-refused-int\n")

    def test_hover_contract_effect_origins_explanation_and_symbols(self):
        source = "from pyalamode import effects, Clock, ClockCapability\n@effects(Clock)\ndef leaf(clock:ClockCapability)->int:return clock.now_ns()\n@effects(Clock)\ndef f(clock:ClockCapability)->int:return leaf(clock)\n"
        self.path.write_text(source)
        hover = self.session.handle("textDocument/hover", {"textDocument": {"uri": self.path.as_uri()}, "position": {"line": 4, "character": 5}})
        for field in ("effect_bound", "required_effects", "effect_origins", "caller_obligations", "source_evidence", "definition_failures", "initialization", "freshness", "trust"):
            self.assertIn(field, hover["contents"]["value"])
        self.assertEqual(len(self.session.handle("textDocument/documentSymbol", {"textDocument": {"uri": self.path.as_uri()}})), 2)
        self.assertEqual(self.session.handle("pyalamode/explain", {"symbol": "core:f"})["contract"]["required_effects"], ["Clock"])
        self.assertEqual(self.session.handle("pyalamode/explain", {"symbol": "f"})["status"], 2)
        from pyalamode.cli import explain_symbol
        self.assertEqual(self.session.handle("pyalamode/explain", {"symbol": "PAL101"}), explain_symbol("PAL101", root=self.root))

    def test_external_trust_and_actual_expiry_refresh_unchanged_text(self):
        self.path.write_text("from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef f(data:bytes)->bytes:return sha256_digest(data)\n")
        row = next(row for row in integration_snapshot(root=self.root)["catalog"] if row["identity"].endswith("sha256_digest"))
        now = datetime.now(timezone.utc)
        expiry = (now + timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
        (self.root / "pyproject.toml").write_text('[tool.pyalamode]\nexternal_trust="approved"\n[[tool.pyalamode.integration_approvals]]\n' + "".join(key + "=" + json.dumps(value) + "\n" for key, value in {"operation": row["identity"], "contract_sha256": row["contract_sha256"], "dependency_sha256": row["dependency_sha256"], "owner": "test reviewer", "rationale": "bounded fixture", "provenance": "M9 test", "expires_at": expiry}.items()))
        report = self.project()
        self.assertEqual(report["report"]["status"], 0)
        self.assertEqual(report["regions"][0]["contract"]["external_assumptions"][0]["admission"], "approved")
        actual = integration_snapshot
        with patch("pyalamode.project.integration_snapshot", side_effect=lambda policy=None, root=None: actual(policy, root, now=now + timedelta(seconds=60))):
            expired = self.project()
        self.assertEqual(expired["report"]["status"], 1)
        self.assertIn("PAL350", [row["code"] for row in expired["diagnostics"]])

    def test_safe_ssa_preview_preserves_rhs_and_does_not_apply(self):
        self.open(REBIND)
        preview = self.session.handle("pyalamode/preview", self.preview_request())
        self.assertIn("result_2 = result + 1", preview["after"])
        self.assertIn("return result_2", preview["after"])
        self.assertEqual(self.session.documents[str(self.path)]["text"], REBIND)
        self.assertEqual(self.path.read_text(), SCALAR)
        self.assertEqual(preview["status"], 0)
        self.assertIn("still reads the first", preview["limits"])
        # Ordinary reference/repaired artifact execution is separate from checks.
        before, after = {}, {}
        exec(REBIND, before)
        exec(preview["after"], after)
        self.assertEqual([before["f"](x) for x in (-4, 0, 10)], [after["f"](x) for x in (-4, 0, 10)])

    def test_preview_generated_name_collision_and_stale_snapshot(self):
        text = REBIND.replace("    result = value", "    result_2 = value + 9\n    result = value").replace("return result\n", "return result + result_2\n")
        self.open(text)
        request = self.preview_request()
        preview = self.session.handle("pyalamode/preview", request)
        self.assertIn("result_2_2 = result + 1", preview["after"])
        self.change(REBIND, 2)
        with self.assertRaises(ProtocolError):
            self.session.handle("pyalamode/preview", request)

    def test_preview_capture_branch_alias_three_binding_refusals(self):
        sources = [REBIND.replace("    result = result + 1", "    def captured()->int:return result\n    result = result + 1"),
                   REBIND.replace("    result = result + 1", "    if value > 0:\n        result = result + 1"),
                   REBIND.replace("    result = result + 1", "    alias = result\n    result = result + 1"),
                   REBIND.replace("    return result", "    result = result + 2\n    return result")]
        self.open(sources[0])
        for version, text in enumerate(sources, 2):
            self.change(text, version)
            with self.assertRaises(ProtocolError):
                self.session.handle("pyalamode/preview", self.preview_request())

    def test_discarded_update_preview_keeps_original_return_and_choices(self):
        self.open(UPDATE)
        request = self.preview_request()
        preview = self.session.handle("pyalamode/preview", request)
        self.assertIn("updated_value = values.appended(1)", preview["after"])
        self.assertIn("return values", preview["after"])
        self.assertIn("unused", preview["limits"])
        actions = self.session.handle("textDocument/codeAction", {"textDocument": {"uri": self.path.as_uri()}, "range": {"start": {"line": 4, "character": 0}, "end": {"line": 4, "character": 22}}, "context": {"diagnostics": []}})
        self.assertEqual(actions[0]["command"], "pyalamode.preview")
        self.assertEqual(self.session.documents[str(self.path)]["text"], UPDATE)

    def test_static_source_and_preview_sentinels_are_not_evaluated(self):
        marker = self.root / "sentinel"
        source = "from pyalamode import fun\nfrom pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('executed')\n@fun\n@Path('decorator')\ndef f(value:Path('annotation')=Path('default'))->int:return 1\n"
        self.open(source)
        self.project()
        self.session.handle("pyalamode/explain", {"symbol": "core:f"})
        self.assertFalse(marker.exists())
        self.assertEqual(self.project()["report"]["status"], 1)

    def test_real_guard_authored_navigation_and_artifact_source_freshness(self):
        self.path.write_text("# mode: fun\n\ndef f(value:int)->int:\n    result=value+1\n    return result\n")
        policy = self.root / "pyproject.toml"
        for mode in ("exports", "debug"):
            policy.write_text('[tool.pyalamode]\nboundary_guards=' + json.dumps(mode) + '\nguarded_exports=["core:f"]\n')
            output = self.root / "build" / mode
            built = build_paths([self.path], root=self.root, output=output)
            self.assertEqual(built.status, 0, [d.format() for d in built.tooling])
            params = {"artifactUri": output.as_uri(), "publicBoundary": "pyalamode_exports.core:f", "phase": "argument", "name": "value"}
            location = self.session.handle("pyalamode/guardLocation", params)
            self.assertEqual(location["location"]["uri"], self.path.as_uri())
            self.assertEqual(location["location"]["range"]["start"]["line"], 2)
            if mode == "debug":
                local = self.session.handle("pyalamode/guardLocation", {**params, "phase": "local", "name": "result", "authoredLine": 4})
                self.assertEqual(local["location"]["range"]["start"]["line"], 3)
            evidence_path = output / "pyalamode-evidence.json"
            original = evidence_path.read_text()
            evidence = json.loads(original)
            mutations = [dict(evidence, artifact_files={}), dict(evidence, artifact_files={key: value for key, value in evidence["artifact_files"].items() if key != "pyalamode_exports/core.py"})]
            altered = copy.deepcopy(evidence)
            altered["guarded_exports"][0]["parameters"] = {}
            mutations.append(altered)
            for mutation in mutations:
                evidence_path.write_text(json.dumps(mutation))
                with self.assertRaises(ProtocolError):
                    self.session.handle("pyalamode/guardLocation", params)
            evidence_path.write_text(original)
            code = "from pyalamode_exports.core import f\ntry:f(True)\nexcept TypeError as error:print(str(error))\nelse:raise AssertionError('guard did not reject')\n"
            result = subprocess.run([sys.executable, "-c", code], cwd=output, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(self.path) + ":3", result.stdout)
            generated = output / "pyalamode_exports" / "core.py"
            generated.write_text(generated.read_text() + "# changed\n")
            with self.assertRaises(ProtocolError):
                self.session.handle("pyalamode/guardLocation", params)
        self.path.write_text(SCALAR)
        with self.assertRaises(ProtocolError):
            self.session.handle("pyalamode/guardLocation", params)


_ORIGINAL_READ_BYTES = Path.read_bytes
def original_for(path):
    return _ORIGINAL_READ_BYTES(path)


class WireCase(unittest.TestCase):
    def test_known_length_json_utf8_and_content_type_errors_recover(self):
        for body, headers in ((b"{bad", b""), (b"\xff", b""), (b"[" * 10000 + b"0" + b"]" * 10000, b""), (b'{"x":NaN}', b""), (b'{"x":Infinity}', b""), (b"{}", b"Content-Type: application/vscode-jsonrpc; charset=latin-1\r\n")):
            stream = io.BytesIO(b"Content-Length: " + str(len(body)).encode() + b"\r\n" + headers + b"\r\n" + body + _frame({"jsonrpc": "2.0", "id": 1, "method": "initialize"}))
            self.assertIsInstance(_read_frame(stream), ProtocolError)
            self.assertEqual(_read_frame(stream)["id"], 1)

    def test_invalid_envelopes_and_ids_use_null_error_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "core.py").write_text(SCALAR)
            invalid = [{}, [], {"jsonrpc": "2.0", "id": True, "method": "initialize"}, {"jsonrpc": "2.0", "id": {}, "method": "initialize"}]
            messages = b"".join(_frame(value) for value in invalid) + _frame({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"rootUri": root.as_uri()}}) + _frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}) + _frame({"jsonrpc": "2.0", "method": "exit"})
            output = io.BytesIO()
            self.assertEqual(serve(root=root, input_stream=io.BytesIO(messages), output_stream=output), 0)
            stream = io.BytesIO(output.getvalue())
            for _ in invalid:
                response = _read_frame(stream)
                self.assertIsNone(response["id"])
                self.assertEqual(response["error"]["code"], -32600)
            self.assertEqual(_read_frame(stream)["id"], 1)

    def test_unrecoverable_framing_and_truncation_refuse(self):
        for value in (b"Bad\r\n\r\n", b"Content-Length: -1\r\n\r\n", b"Content-Length: 8388609\r\n\r\n", b"Content-Length: 2\r\nContent-Length: 2\r\n\r\n{}", b"\xff: 2\r\n\r\n", b"x" * 8193):
            with self.assertRaises(ProtocolError):
                _read_frame(io.BytesIO(value))
        for value in (b"Content-Length: 3\r\n", b"Content-Length: 3\r\n\r\n{}"):
            with self.assertRaises(EOFError):
                _read_frame(io.BytesIO(value))

    def test_actual_process_frames_lifecycle_notifications_and_unicode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            path = root / "core.py"
            path.write_text(SCALAR)
            values = [{"jsonrpc": "2.0", "id": 0, "method": "pyalamode/project"},
                      {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"rootUri": root.as_uri()}},
                      {"jsonrpc": "2.0", "method": "initialized", "params": {}},
                      {"jsonrpc": "2.0", "method": "textDocument/didOpen", "params": {"textDocument": {"uri": path.as_uri(), "languageId": "python", "version": 1, "text": REBIND.replace("result", "café")}}},
                      {"jsonrpc": "2.0", "id": "report", "method": "pyalamode/project", "params": {}},
                      {"jsonrpc": "2.0", "id": 3, "method": "unknown"},
                      {"jsonrpc": "2.0", "id": 4, "method": "shutdown"},
                      {"jsonrpc": "2.0", "method": "exit"}]
            result = subprocess.run([sys.executable, "-I", "-m", "pyalamode.editor", "--stdio", "--root", str(root)], cwd=root, input=b"".join(_frame(value) for value in values), capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            stream = io.BytesIO(result.stdout)
            packets = []
            while True:
                packet = _read_frame(stream)
                if packet is None:
                    break
                packets.append(packet)
            responses = {packet["id"]: packet for packet in packets if "id" in packet}
            self.assertEqual(responses[0]["error"]["code"], -32002)
            self.assertEqual(responses["report"]["result"]["report"]["status"], 1)
            self.assertEqual(responses[3]["error"]["code"], -32601)
            self.assertTrue(any(packet.get("method") == "textDocument/publishDiagnostics" and packet["params"].get("version") == 1 for packet in packets))
            self.assertEqual(result.stderr, b"")

    def test_serve_complete_frame_error_does_not_contaminate_next_response(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "core.py").write_text(SCALAR)
            messages = b"Content-Length: 4\r\n\r\n{bad" + _frame({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"rootUri": root.as_uri()}}) + _frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}) + _frame({"jsonrpc": "2.0", "method": "exit"})
            output = io.BytesIO()
            self.assertEqual(serve(root=root, input_stream=io.BytesIO(messages), output_stream=output), 0)
            stream = io.BytesIO(output.getvalue())
            self.assertEqual(_read_frame(stream)["error"]["code"], -32700)
            self.assertEqual(_read_frame(stream)["id"], 1)


if __name__ == "__main__":
    unittest.main()
