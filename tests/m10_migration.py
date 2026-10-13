"""M10 current-source capture, policy axes, queues and read-only previews."""
import contextlib
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.cli import main
from pyalamode.migration import MigrationError, load_reference
from pyalamode.migration_views import observe, ready_view, convert_preview, make_prepublish
from pyalamode.project import check_paths, check_snapshot, build_paths

GOOD = "from pyalamode import fun\n\n@fun\ndef total(value: int) -> int:\n    return value + 1\n"
DEBT = "from pyalamode import fun\n\n@fun\ndef total(value: int) -> int:\n    result = value\n    result = result + 1\n    return result\n"


class MigrationCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.path = self.root / "core.py"
        self.path.write_text(GOOD)

    def policy(self, text):
        (self.root / "pyproject.toml").write_text(text)

    def command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main([*args, "--root", str(self.root), "--json"])
        return status, json.loads(output.getvalue())

    def approval_policy(self, *, expires=None, migration=""):
        from pyalamode.integration_contracts import integration_snapshot
        snapshot = integration_snapshot({"external_trust": "approved"}, self.root)
        rows = []
        for entry in snapshot["catalog"]:
            row = {"operation": entry["identity"], "contract_sha256": entry["contract_sha256"],
                   "dependency_sha256": entry["dependency_sha256"], "owner": "test", "rationale": "bounded fixture", "provenance": "owned regression"}
            if expires:
                row["expires_at"] = expires
            rows.append(row)
        self.policy('[tool.pyalamode]\nexternal_trust="approved"\n' + ''.join('[[tool.pyalamode.integration_approvals]]\n' + '\n'.join(key+'='+json.dumps(value) for key,value in item.items()) + '\n' for item in rows) + migration)

    def test_baseline_receipt_report_source_and_audit_axes(self):
        self.path.write_text(DEBT)
        self.policy('[tool.pyalamode.migration]\nschema=1\nreject_new_findings=true\n')
        status, result = self.command("baseline", "--owner", "maintainer", "--rationale", "existing debt")
        self.assertEqual(status, 0)
        self.assertFalse(result["written"]["verified"])
        self.assertEqual(result["written"]["state_strict_status"], 1)
        before = (self.root / ".pyalamode/baseline.json").read_bytes()
        self.assertEqual(check_paths([self.root], root=self.root, audit=True).status, 0)
        self.assertEqual(check_paths([self.root], root=self.root).status, 1)
        self.assertEqual(build_paths(root=self.root, output=self.root / "rejected").status, 1)
        self.assertFalse((self.root / "rejected").exists())
        status, saved = self.command("report", "--save")
        self.assertEqual(status, 1)
        self.assertEqual(saved["written"]["status"], 0)
        self.assertEqual(saved["report"]["status"], 1)
        self.assertEqual((self.root / ".pyalamode/baseline.json").read_bytes(), before)
        self.path.write_text(DEBT.replace("result + 1", "result + 2"))
        self.assertEqual(check_paths(root=self.root, audit=True).status, 1)

    def test_custom_active_baseline_bootstrap_and_replacement_keep_default(self):
        self.path.write_text(DEBT)
        self.policy('[tool.pyalamode.migration]\nschema=1\nreject_new_findings=true\n')
        self.assertEqual(self.command("baseline", "--owner", "maintainer", "--rationale", "default debt")[0], 0)
        default = self.root / ".pyalamode/baseline.json"
        original_default = default.read_bytes()
        self.policy('[tool.pyalamode]\nrequired_exports=["core:missing"]\n[tool.pyalamode.migration]\nschema=1\nbaseline=".pyalamode/custom.json"\nreject_new_findings=true\n')
        status, initial = self.command("baseline", "--owner", "maintainer", "--rationale", "custom debt")
        self.assertEqual(status, 0, initial)
        receipt = initial["written"]
        self.assertEqual(receipt["path"], ".pyalamode/custom.json")
        self.assertIsNone(receipt["previous_id"])
        self.assertEqual((receipt["state_strict_status"], receipt["current_policy_status"]), (1, 1))
        self.assertTrue(initial["report"]["state"]["current_policy_events"]["required_exports"])
        current = self.root / receipt["path"]
        initial_custom = current.read_bytes()
        self.assertEqual(default.read_bytes(), original_default)
        self.assertEqual(self.command("baseline", "--owner", "maintainer", "--rationale", "must replace")[0], 2)
        self.assertEqual(current.read_bytes(), initial_custom)
        self.assertEqual(default.read_bytes(), original_default)
        status, replacement = self.command("baseline", "--replace", "--owner", "maintainer", "--rationale", "reviewed custom replacement")
        self.assertEqual(status, 0, replacement)
        self.assertEqual(replacement["written"]["path"], ".pyalamode/custom.json")
        self.assertEqual(replacement["written"]["previous_id"], receipt["id"])
        self.assertEqual(default.read_bytes(), original_default)

    def test_exact_eligible_denominator_and_display_subset(self):
        (self.root / "__init__.py").write_text("")
        self.path.write_text('''from pyalamode import fun, record, oneof, case, effects, Clock, ClockCapability, unsafe
@record
class Customer:
    value: int
@oneof
class Choice:
    @case
    class First:
        pass
    @case
    class Second:
        pass
@fun
def total(value: int) -> int:
    def plus(value: int) -> int:
        return value + 1
    return plus(value)
@effects(Clock)
def now(clock: ClockCapability) -> int:
    return clock.now_ns()
def ordinary(value: int) -> int:
    return value
async def deferred():
    pass
class Service:
    def method(self):
        pass
@unsafe(scope="legacy", rationale="ordinary shell")
def raw():
    pass
''')
        (self.root / "plain.py").write_text("def unused(value: int) -> int:\n    return value\n")
        (self.root / "strict.py").write_text("# mode: fun\ndef double(value: int) -> int:\n    return value * 2\n")
        _, state, _, _ = observe(self.root, [self.root / "plain.py"])
        self.assertEqual(state["coverage"], {"eligible_modules": 4, "selected_modules": 1, "checked_modules": 1,
            "eligible_functions": 9, "selected_functions": 4, "checked_functions": 4,
            "checked_exports": 5, "selected_records": 1, "selected_oneofs": 1})
        self.assertEqual(state["scope"]["displayed_paths"], ["plain.py"])
        root_module = next(row for row in state["boundaries"] if row["path"] == "__init__.py")
        self.assertEqual((root_module["selector"], root_module["qualified_name"]), ("module:", ""))

    def test_current_required_export_is_not_baseline_waived(self):
        self.path.write_text("def total(value: int) -> int:\n    return value + 1\n")
        self.policy('[tool.pyalamode]\nrequired_exports=["core:total"]\n')
        status, result = self.command("baseline", "--owner", "maintainer", "--rationale", "coverage work")
        self.assertEqual(status, 0)
        self.assertEqual(result["written"]["state_strict_status"], 0)
        self.assertEqual(result["written"]["current_policy_status"], 1)
        self.assertEqual(check_paths(root=self.root, audit=True).status, 1)
        self.assertEqual(check_paths(root=self.root).status, 1)

    def test_current_source_proof_survives_unrelated_policy_refusal(self):
        self.policy('[tool.pyalamode]\nrequired_exports=["core:missing"]\n')
        captured = check_snapshot(root=self.root, cache=False)
        self.assertEqual(captured.result.status, 1)
        self.assertEqual(captured.result.source_status, 0)
        self.assertTrue(captured.result.results[0].contracts[0].source_evidence.startswith("checked"))
        self.assertFalse(captured.result.verified)
        self.assertTrue(captured.result.policy_diagnostics)

    def test_required_operation_approval_visibility_preserves_audit(self):
        self.path.write_text('''from pyalamode import fun
from pyalamode.integrations import sha256_digest
from typing import Callable
@fun
def digest(value: bytes) -> bytes:
    return sha256_digest(value)
@fun
def factory() -> Callable[[bytes],bytes]:
    return digest
''')
        _, state, report, _ = observe(self.root)
        self.assertEqual(state["strict_status"], 1)
        self.assertEqual(state["current_policy_status"], 0)
        self.assertEqual(len(state["required_operations"]), 1)
        requirements = state["required_operations"][0]["required_by"]
        self.assertTrue(any(row["boundary"] == "core:digest" and row["via"] == "direct" for row in requirements))
        self.assertTrue(any(row["boundary"] == "core:factory" and row["via"] == "retained" for row in requirements))
        self.assertEqual(len(report["comparison"]["approval_failures"]), 1)
        self.assertEqual(check_paths(root=self.root, audit=True).status, 0)
        (self.root / "writer.py").write_text("import pyalamode.integrations as external\nexternal.sha256_digest.__code__ = other\n")
        _, changed, _, _ = observe(self.root)
        self.assertFalse(changed["required_operations"])
        self.assertTrue(any(row["rule"] == "PAL240" for row in changed["findings"]))

    def test_unused_expiry_is_current_policy_without_fabricated_source_call(self):
        self.approval_policy(expires="2000-01-01T00:00:00Z", migration='[tool.pyalamode.migration]\nschema=1\nreject_expired_approvals=true\n')
        status, result = self.command("baseline", "--owner", "maintainer", "--rationale", "renewal backlog")
        self.assertEqual(status, 0)
        state = result["report"]["state"]
        self.assertEqual(state["strict_status"], 0)
        self.assertEqual(state["current_policy_status"], 1)
        self.assertFalse(state["required_operations"])
        self.assertFalse(state["current_policy_events"]["approval_failures"])
        self.assertEqual(len(state["current_policy_events"]["expired_approvals"]), 3)
        self.assertEqual(check_paths(root=self.root, audit=True).status, 1)

    def test_marker_loss_and_exact_current_export_remain_independent(self):
        self.policy('[tool.pyalamode]\nrequired_exports=["core:total"]\n[tool.pyalamode.migration]\nschema=1\nreject_lost_strict_coverage=true\n')
        self.assertEqual(self.command("baseline", "--owner", "maintainer", "--rationale", "current core")[0], 0)
        self.path.write_text(GOOD.replace("@fun\n", ""))
        _, _, report, _ = observe(self.root)
        self.assertTrue(report["comparison"]["lost_strict_coverage"])
        self.assertEqual(report["status"], 1)
        status, replaced = self.command("baseline", "--replace", "--owner", "maintainer", "--rationale", "coverage work")
        self.assertEqual(status, 0)
        self.assertEqual(replaced["written"]["current_policy_status"], 1)
        self.assertEqual(check_paths(root=self.root).status, 1)

    def test_canonical_required_export_and_ambiguous_authored_conversion(self):
        package = self.root / "same"
        package.mkdir()
        (package / "__init__.py").write_text(GOOD)
        (self.root / "same.py").write_text(GOOD)
        self.policy('[tool.pyalamode]\nrequired_exports=["same:total"]\n')
        result = check_paths(root=self.root, cache=False)
        self.assertEqual(result.status, 0, result.to_dict())
        snapshot, state, _, _ = observe(self.root)
        with self.assertRaises(MigrationError):
            convert_preview(snapshot, state, "function:same:total")
        status, _ = self.command("baseline", "--owner", "maintainer", "--rationale", "duplicate physical declarations")
        self.assertEqual(status, 2)

    def test_overlay_policy_provenance_and_editor_projection(self):
        from pyalamode.editor import EditorSession
        self.policy('[tool.pyalamode]\nrequired_exports=["core:total"]\n')
        session = EditorSession(self.root)
        session.documents[str(self.path)] = {"text": GOOD.replace("@fun\n", ""), "version": 42}
        snapshot = session.refresh()
        self.assertEqual(snapshot.result.status, 1)
        state = snapshot.result.migration["state"]
        self.assertEqual(state["inputs"]["sources"]["core.py"]["version"], 42)
        self.assertIn("unsaved", state["freshness"])
        self.assertTrue(any(row["code"] == "PAL361" for row in session.diagnostics))

    def test_build_rechecks_reference_after_guard_staging(self):
        self.policy('[tool.pyalamode.migration]\nschema=1\nreject_new_findings=true\n')
        self.assertEqual(self.command("baseline", "--owner", "maintainer", "--rationale", "passing core")[0], 0)
        from pyalamode.guardgen import generate_facades
        original = (self.root / ".pyalamode/baseline.json").read_bytes()
        def mutate_reference(*args, **kwargs):
            output = generate_facades(*args, **kwargs)
            (self.root / ".pyalamode/baseline.json").write_bytes(original + b" ")
            return output
        with patch("pyalamode.guardgen.generate_facades", side_effect=mutate_reference):
            result = build_paths(root=self.root, output=self.root / "changed-reference")
        self.assertEqual(result.status, 2)
        self.assertFalse((self.root / "changed-reference").exists())

    def test_readiness_actual_direct_retained_and_recursive_components(self):
        self.path.write_text('''from pyalamode import fun
from typing import Callable
@fun
def checked(value: int) -> int:
    return value
def leaf(value: int) -> int:
    return value + 1
def middle(value: int) -> int:
    return leaf(value)
def outer(value: int) -> int:
    return middle(value)
def left(value: int) -> int:
    return right(value)
def right(value: int) -> int:
    return left(value)
def factory() -> Callable[[int], int]:
    return leaf
def shadow(leaf: Callable[[int], int], value: int) -> int:
    return leaf(value)
def unknown(value: int) -> int:
    return absent(value)
''')
        snapshot, state, _, _ = observe(self.root)
        ready = ready_view(snapshot, state)
        groups = [set(row["members"]) for row in ready["groups"]]
        self.assertIn({"core:left", "core:right"}, groups)
        positions = {member: index for index, group in enumerate(groups) for member in group}
        self.assertLess(positions["core:leaf"], positions["core:middle"])
        self.assertLess(positions["core:middle"], positions["core:outer"])
        self.assertTrue(any(row["kind"] == "retained" and row["caller"].endswith("::factory") and row["callee"].endswith("::leaf") for row in ready["edges"]))
        self.assertFalse(any(row["caller"].endswith("::shadow") and row["callee"].endswith("::leaf") for row in ready["edges"]))
        refused = convert_preview(snapshot, state, "function:core:outer")
        self.assertEqual(refused["status"], 1)
        self.assertFalse(refused["edits"])
        source = self.path.read_bytes()
        preview = convert_preview(snapshot, state, "function:core:leaf")
        self.assertEqual(preview["status"], 1)
        self.assertTrue(any(row.get("rule") == "PAL221" for row in preview["blockers"] if type(row) is dict))
        self.assertIn("@fun\ndef leaf", preview["edits"][0]["after"])
        self.assertEqual(self.path.read_bytes(), source)
        self.assertFalse(preview["verified"])
        self.assertEqual(preview["candidate"]["source_status"], 1)
        demotions = [row for row in preview["blockers"] if type(row) is dict and row.get("reason") == "candidate source refusal demotes existing local evidence"]
        self.assertTrue(demotions)
        self.assertEqual(demotions[0]["demotion_fields"], ["behavior", "freshness", "source_evidence"])
        self.assertEqual(len(demotions[0]["contract_comparison"]["fields"]), 44)
        self.assertEqual({row["field"] for row in demotions[0]["contract_comparison"]["fields"] if not row["matched"]}, {"behavior", "freshness", "source_evidence"})
        actual_snapshot = check_snapshot
        def altered_existing(*args, **kwargs):
            candidate = actual_snapshot(*args, **kwargs)
            if kwargs.get("overlays") and kwargs.get("_candidate_selection") is None:
                contract = next(contract for file in candidate.result.results for contract in file.contracts if contract.name == "checked")
                contract.effect_bound.append("Clock")
            return candidate
        with patch("pyalamode.project.check_snapshot", side_effect=altered_existing):
            changed_contract = convert_preview(snapshot, state, "function:core:leaf")
        self.assertEqual(changed_contract["status"], 2)
        self.assertTrue(any("existing participating dimensions changed" in row for row in changed_contract["blockers"] if type(row) is str))
        self.assertEqual(self.path.read_bytes(), source)
        self.assertNotEqual(ready["candidate_snapshot"], snapshot.snapshot)
        self.assertTrue(ready["candidate_analysis"]["candidate_selection"]["functions"])
        self.path.write_text("from pyalamode import fun\ndef leaf(value: int) -> int:\n    return value + 1\n")
        snapshot, state, _, _ = observe(self.root)
        preview = convert_preview(snapshot, state, "function:core:leaf")
        self.assertEqual(preview["status"], 0, preview["blockers"])

    def test_module_preview_preserves_docstring_crlf_and_bodies(self):
        text = '#!/usr/bin/python\r\n# coding: utf-8\r\n"""ordinary core"""\r\ndef total(value: int) -> int:\r\n    return value + 1\r\n'
        self.path.write_bytes(text.encode())
        snapshot, state, _, _ = observe(self.root)
        preview = convert_preview(snapshot, state, "module:core")
        self.assertEqual(preview["status"], 0, preview["blockers"])
        self.assertEqual(preview["edits"][0]["after"], text.replace('"""ordinary core"""\r\n', '"""ordinary core"""\r\n# mode: fun\r\n'))
        self.assertEqual(self.path.read_bytes(), text.encode())

    def test_no_edit_conversion_preserves_current_historical_gate(self):
        self.path.write_text(GOOD + "\n@fun\ndef earlier(value: int) -> int:\n    return value\n")
        self.policy('[tool.pyalamode.migration]\nschema=1\nreject_lost_strict_coverage=true\n')
        self.assertEqual(self.command("baseline", "--owner", "maintainer", "--rationale", "two exports")[0], 0)
        self.path.write_text(GOOD + "\ndef earlier(value: int) -> int:\n    return value\n")
        status, preview = self.command("convert", "function:core:total", "--preview")
        self.assertEqual(status, 1)
        self.assertFalse(preview["edits"])
        self.assertIsNone(preview["candidate"])
        self.assertEqual(preview["report"]["state"]["strict_status"], 0)
        self.assertEqual(preview["report"]["gates"]["status"], 1)

    def test_readiness_unverified_selected_prerequisite_is_not_checked(self):
        self.path.write_text(DEBT + "\ndef follower(value: int) -> int:\n    return total(value)\n")
        snapshot, state, _, _ = observe(self.root)
        ready = ready_view(snapshot, state)
        group = next(row for row in ready["groups"] if row["members"] == ["core:follower"])
        self.assertFalse(group["checked_prerequisites"])
        self.assertTrue(any(row["reason"] == "prerequisite lacks current disk strict source proof" for row in group["blockers"]))
        self.assertTrue(any(row["caller"].endswith("::follower") and row["callee"].endswith("::total") for row in ready["edges"]))
        self.assertTrue(all(row["source_evidence"].startswith("hypothetical candidate analysis:") for row in group["contracts"]))

    def test_repair_reuses_current_full_project_m9_preview(self):
        self.path.write_text(DEBT)
        snapshot, state, _, _ = observe(self.root)
        preview = convert_preview(snapshot, state, "function:core:total")
        self.assertEqual(preview["status"], 0, preview["blockers"])
        self.assertIn("result_2 = result + 1", preview["edits"][0]["after"])
        self.assertIn("return result_2", preview["edits"][0]["after"])
        self.assertEqual(self.path.read_text(), DEBT)

    def test_published_isolated_example_repair_then_adoption(self):
        fixture = Path(__file__).resolve().parents[1] / "examples/migration"
        self.path.write_bytes((fixture / "core.py").read_bytes())
        (self.root / "pyproject.toml").write_bytes((fixture / "pyproject.toml").read_bytes())
        self.assertEqual(self.command("baseline", "--owner", "maintainer", "--rationale", "reviewed existing debt")[0], 0)
        self.assertEqual(self.command("ready")[0], 1)
        self.assertEqual(check_paths(root=self.root, audit=True).status, 0)
        status, repair = self.command("convert", "function:core:total", "--preview")
        self.assertEqual(status, 0, repair["blockers"])
        self.path.write_text(repair["edits"][0]["after"])
        self.assertEqual(check_paths(root=self.root).status, 0)
        self.assertEqual(self.command("report", "--save")[0], 0)
        status, adoption = self.command("convert", "function:core:doubled", "--preview")
        self.assertEqual(status, 0, adoption["blockers"])
        self.path.write_text(adoption["edits"][0]["after"])
        self.assertEqual(check_paths(root=self.root).status, 0)
        self.assertFalse(self.command("ready")[1]["groups"])

    def test_live_freshness_includes_new_ordinary_writer(self):
        snapshot, state, _, _ = observe(self.root)
        callback = make_prepublish(snapshot, state, [])
        (self.root / "writer.py").write_text("import core\ncore.total.__code__ = other\n")
        with self.assertRaises(MigrationError):
            callback()

    def test_excluded_display_and_outside_symlink_refuse_before_read(self):
        excluded = self.root / ".pyalamode"
        excluded.mkdir()
        (excluded / "poison.py").write_text("raise RuntimeError('excluded')\n")
        with self.assertRaises(MigrationError):
            observe(self.root, [excluded / "poison.py"])
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        target = Path(outside.name) / "outside.py"
        target.write_text("raise RuntimeError('outside')\n")
        (self.root / "alias.py").symlink_to(target)
        self.policy('[tool.pyalamode]\nrequired_exports=["core:total"]\n')
        self.assertEqual(check_paths(root=self.root, cache=False).status, 2)

    def test_snapshot_reread_refuses_new_outside_symlink_before_bytes(self):
        from pyalamode.project import _integration_freshness
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        target = Path(outside.name) / "outside.py"
        target.write_text(GOOD)
        original_read = Path.read_bytes
        opened = []
        def trace_read(path):
            opened.append(path)
            return original_read(path)
        def replace_after_analysis(*args, **kwargs):
            answer = _integration_freshness(*args, **kwargs)
            self.path.unlink()
            self.path.symlink_to(target)
            return answer
        with patch("pyalamode.project._integration_freshness", side_effect=replace_after_analysis), patch.object(Path, "read_bytes", trace_read):
            snapshot = check_snapshot(root=self.root, cache=False, _migration_history=False)
        self.assertEqual(snapshot.result.status, 2)
        self.assertNotIn(target, opened)
        self.assertFalse(snapshot.result.verified)

    def test_build_reserved_staging_and_current_reference_recheck(self):
        self.policy('[tool.pyalamode]\nrequired_exports=["core:total"]\n')
        accepted = build_paths(root=self.root, output=self.root / "accepted")
        self.assertEqual(accepted.status, 0, accepted.to_dict())
        self.assertTrue((self.root / "accepted/core.py").exists())
        self.assertEqual((self.root / "accepted/core.py").read_bytes(), self.path.read_bytes())

    def test_late_source_refusal_after_saved_source_axis_remains_failure(self):
        from pyalamode.project import _integration_freshness
        from pyalamode.integration_contracts import integration_snapshot
        policy = {"external_trust": "approved"}
        snapshot = integration_snapshot(policy, self.root)
        row = next(row for row in snapshot["catalog"] if row["identity"].endswith("sha256_digest"))
        policy["integration_approvals"] = [{"operation": row["identity"], "contract_sha256": row["contract_sha256"], "dependency_sha256": row["dependency_sha256"], "owner": "test", "rationale": "fixed regression", "provenance": "test", "expires_at": "2099-01-01T00:00:00Z"}]
        self.policy('[tool.pyalamode]\nexternal_trust="approved"\n' + ''.join('[[tool.pyalamode.integration_approvals]]\n' + '\n'.join(key+'='+json.dumps(value) for key,value in item.items()) + '\n' for item in policy["integration_approvals"]))
        self.path.write_text('from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef total(value: bytes) -> bytes:\n    return sha256_digest(value)\n')
        result = check_paths(root=self.root, cache=False)
        self.assertEqual(result.source_status, 0)
        late = integration_snapshot(policy, self.root, now=datetime(2100, 1, 1, tzinfo=timezone.utc))
        self.assertTrue(_integration_freshness(result, late, "artifact publication"))
        self.assertEqual(result.status, 1)
        self.assertEqual(result.source_status, 1)
        current = integration_snapshot(policy, self.root)
        calls = []
        def snapshot_at_publication(*args, **kwargs):
            calls.append(None)
            return current if len(calls) <= 3 else late
        with patch("pyalamode.project.integration_snapshot", side_effect=snapshot_at_publication):
            built = build_paths(root=self.root, output=self.root / "expired-build")
        self.assertEqual(built.status, 1)
        self.assertEqual(built.source_status, 1)
        self.assertFalse((self.root / "expired-build").exists())


if __name__ == "__main__":
    unittest.main()
