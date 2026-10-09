"""M10 detached-policy literals and real temporary-file publication refusals."""

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.model import CHECKER_VERSION, OPERATION_VERSION
from pyalamode import migration as m


C101 = "Assign(targets=[Name(id='value', ctx=Store())], value=BinOp(left=Name(id='value', ctx=Load()), op=Add(), right=Constant(value=1)))"
LOCATION_KEYS = {"path", "line", "column", "end_line", "end_column", "column_encoding"}


def location(path, line=1, column=1, end_line=None, end_column=None):
    return {"path": path, "line": line, "column": column, "end_line": end_line,
            "end_column": end_column, "column_encoding": "utf-8-bytes"}


def boundary(module, name=None, *, selected=True, checked=True, definition="a" * 64):
    path = (module + ".py") if module else "__init__.py"
    return {"id": None, "kind": "module" if name is None else "function",
            "selector": "module:" + module if name is None else module + ":" + name,
            "path": path, "qualified_name": module if name is None else name,
            "signature": None if name is None else "(value:int)->int",
            "definition_sha256": definition, "selected": selected, "strict_checked": checked,
            "public_export": name is not None and bool(module) and "." not in name and not name.startswith("_"),
            "required_export": False, "mode": "strict" if selected else "off",
            "selection_reasons": ["source_fun"] if selected else [],
            "source_evidence": "checked participating source" if checked else "unverified" if selected else "unchecked ordinary source",
            "effect_bound": [], "required_effects": [], "effect_origins": {},
            "external_assumptions": [], "failures": {"invocation": [], "definition": [], "initialization": []},
            "guard_coverage": {"mode": "off", "selected_export": None, "debug": None, "data_assertions": []},
            "location": location(path, 1, 1, 3, 20)}


def capture(specs=(("core", "f", 1),)):
    """Synthetic detached engine rows, never claims about an executed application."""
    modules = sorted({module for module, _, _ in specs})
    rows = [boundary(module, selected=False, checked=False) for module in modules]
    findings = []
    for module, name, count in specs:
        row = boundary(module, name, checked=count == 0)
        rows.append(row)
        if count:
            locations = [{**location(row["path"], 3 + n, 1, 3 + n, 18),
                          "first_binding": row["path"] + ":2", "reason": "already initialized",
                          "remediation": "derive a new binding"} for n in range(count)]
            findings.append({"id": None, "identity_key": None, "birth_identity": None, "rule": "PAL101",
                             "boundary_id": None, "logical_boundary": {k: row[k] for k in ("kind", "selector", "qualified_name")},
                             "signature": row["signature"], "context_sha256": None,
                             "context": {"kind": "ast-statement", "ast": C101},
                             "origin": "static source", "count": count, "locations": locations, "review_required": False})
    paths = sorted({row["path"] for row in rows})
    value = {"schema": 2, "kind": "pyalamode-migration-state", "identity_version": m.IDENTITY_VERSION,
             "target": "cpython-3.13.1", "runtime_environment": {"filesystem_encoding": "utf-8", "filesystem_errors": "surrogateescape", "utf8_mode": 0},
             "edition": "python-v1", "checker": CHECKER_VERSION, "operation_contract": OPERATION_VERSION,
             "snapshot": "b" * 64, "freshness": "current disk snapshot", "strict_status": int(bool(findings)),
             "current_dependency_status":0,"current_dependency_events":[],
             "current_policy_status": 0, "current_policy_events": {"required_exports": [], "expired_approvals": [], "approval_failures": []},
             "required_operations": [],
             "inputs": {"sources": {path: {"sha256": "c" * 64, "origin": "disk", "version": None, "disk_sha256": "c" * 64} for path in paths},
                        "policy_sha256": None, "product_artifacts": {name: "d" * 64 for name in m.PRODUCTS}, "integration_inputs": {},"checked_dependencies":{}},
             "scope": {"project_root": "/synthetic/project", "selected_paths": paths, "displayed_paths": paths, "exclusions": []},
             "coverage": {}, "boundaries": rows, "findings": findings, "policy": m._default_policy(), "approvals": [], "unsafe_adapters": []}
    recount(value)
    return value


def recount(value):
    rows = value["boundaries"]
    value["coverage"] = {
        "eligible_modules": sum(r["kind"] == "module" for r in rows),
        "selected_modules": sum(r["kind"] == "module" and r["selected"] for r in rows),
        "checked_modules": sum(r["kind"] == "module" and r["strict_checked"] for r in rows),
        "eligible_functions": sum(r["kind"] == "function" for r in rows),
        "selected_functions": sum(r["kind"] == "function" and r["selected"] for r in rows),
        "checked_functions": sum(r["kind"] == "function" and r["strict_checked"] for r in rows),
        "checked_exports": sum(r["kind"] != "module" and r["strict_checked"] and r["public_export"] for r in rows),
        "selected_records": sum(r["kind"] == "record" and r["selected"] for r in rows),
        "selected_variants": sum(r["kind"] == "variant" and r["selected"] for r in rows)}


def normalized(specs=(("core", "f", 1),)):
    return m.normalize_state(capture(specs))


def report(state, reference=None):
    compared = m.compare_states(reference["state"] if reference else None, state)
    gates = m.evaluate_gates(compared, state["policy"]["migration"])
    return {"schema": 1, "kind": "pyalamode-migration-report", "state": state,
            "reference_id": reference["record"]["id"] if reference else None,
            "comparison": compared, "gates": gates, "status": max(state["strict_status"], gates["status"], state["current_policy_status"]),
            "verified": False, "claim_scope": "Synthetic audit observation; no source certification.",
            "human_measurement": {"status": "UNMEASURED", "participants": 0, "attempts": 0}}


class DetachedPolicyTests(unittest.TestCase):
    def test_fixed_context_literals_and_full_declaration(self):
        literals = [
            ("PAL101", "value = value + 1", C101),
            ("PAL221", "return leaf(True)", "Return(value=Call(func=Name(id='leaf', ctx=Load()), args=[Constant(value=True)]))"),
            ("PAL230", "return unknown(value)", "Return(value=Call(func=Name(id='unknown', ctx=Load()), args=[Name(id='value', ctx=Load())]))"),
            ("PAL241", "import os", "Import(names=[alias(name='os')])"),
            ("PAL250", "values.appended(1)", "Expr(value=Call(func=Attribute(value=Name(id='values', ctx=Load()), attr='appended', ctx=Load()), args=[Constant(value=1)]))"),
            ("PAL350", "return sha256_digest(data)", "Return(value=Call(func=Name(id='sha256_digest', ctx=Load()), args=[Name(id='data', ctx=Load())]))")]
        for rule, source, expected in literals:
            with self.subTest(rule=rule):
                diagnostic = {"rule": rule, **location("core.py", 1, 1, 1, len(source) + 1)}
                self.assertEqual(m.finding_context(source + "\n", diagnostic, {"kind": "module"}), {"kind": "ast-statement", "ast": expected})
        source = "@effects(Clock)\ndef now(clock: ClockCapability) -> int:\n    return clock.now_ns()\n"
        expected = "FunctionDef(name='now', args=arguments(args=[arg(arg='clock', annotation=Name(id='ClockCapability', ctx=Load()))]), body=[Return(value=Call(func=Attribute(value=Name(id='clock', ctx=Load()), attr='now_ns', ctx=Load())))], decorator_list=[Call(func=Name(id='effects', ctx=Load()), args=[Name(id='Clock', ctx=Load())])], returns=Name(id='int', ctx=Load()))"
        diagnostic = {"rule": "PAL310", **location("core.py", 2, 1, 3, 26)}
        self.assertEqual(m.finding_context(source, diagnostic, {"kind": "module"})["ast"], expected)

    def test_physical_lines_unicode_and_crlf_without_hook_execution(self):
        for ending in ("\n", "\r", "\r\n"):
            source = 'label = "é\u2028x"' + ending + "value = value + 1" + ending
            diagnostic = {"rule": "PAL101", **location("core.py", 2, 1, 2, 18)}
            self.assertEqual(m.finding_context(source, diagnostic, {"kind": "module"})["ast"], C101)
        bad = {"rule": "PAL101", **location("core.py", 30, 1)}
        self.assertEqual(m.finding_context("value = 1\n", bad, {"kind": "module"})["kind"], "unavailable")
        for rule in ("PAL001", "PAL002", "PAL360", "PAL367"):
            with self.assertRaises(m.MigrationError):
                m.finding_context("raise RuntimeError()\n", {"rule": rule}, {})

    def test_counts_are_multisets_and_coordinate_noise_retains_identity(self):
        old = normalized()
        moved_lines = copy.deepcopy(old)
        moved_lines["findings"][0]["locations"][0]["line"] = 99
        moved_lines["findings"][0]["locations"][0]["first_binding"] = "core.py:98"
        moved_lines["findings"][0]["locations"][0]["reason"] = "wording changed"
        result = m.compare_states(old, moved_lines)
        self.assertEqual(result["retained_findings"][0]["after"]["finding"]["id"], old["findings"][0]["id"])
        self.assertFalse(result["new_findings"])
        for old_count, new_count, retained, new, resolved in ((1, 2, 1, 1, 0), (2, 1, 1, 0, 1), (2, 2, 2, 0, 0)):
            compared = m.compare_states(normalized((("core", "f", old_count),)), normalized((("core", "f", new_count),)))
            amount = lambda category, side: sum(e[side]["count"] for e in compared[category])
            self.assertEqual((amount("retained_findings", "after"), amount("new_findings", "after"), amount("resolved_findings", "before")), (retained, new, resolved))

    def test_lower_total_does_not_erase_new_debt(self):
        old = normalized((("core", "a", 1), ("core", "b", 1), ("core", "c", 1)))
        current = normalized((("core", "a", 0), ("core", "b", 0), ("core", "c", 1), ("core", "d", 1)))
        compared = m.compare_states(old, current)
        self.assertEqual(len(compared["resolved_findings"]), 2)
        self.assertEqual(len(compared["new_findings"]), 1)
        policy = copy.deepcopy(current["policy"]["migration"])
        policy["reject_new_findings"] = True
        gates = m.evaluate_gates(compared, policy)
        self.assertEqual(gates["status"], 1)
        self.assertIn("PAL360", {d["rule"] for d in gates["diagnostics"]})

    def test_unique_relocation_and_ambiguous_pairings(self):
        old = normalized((("old", "f", 1),))
        current = normalized((("moved", "f", 1),))
        compared = m.compare_states(old, current)
        retained = compared["retained_findings"][0]
        self.assertEqual(retained["after"]["finding"]["id"], old["findings"][0]["id"])
        self.assertEqual((retained["before"]["path"], retained["after"]["path"]), ("old.py", "moved.py"))
        self.assertFalse(compared["new_findings"])
        ambiguous = m.compare_states(normalized((("a", "f", 1), ("b", "f", 1))), normalized((("c", "f", 1), ("d", "f", 1))))
        self.assertTrue(ambiguous["ambiguous_findings"])
        self.assertFalse(ambiguous["retained_findings"])
        self.assertFalse(ambiguous["resolved_findings"])
        policy = copy.deepcopy(current["policy"]["migration"])
        policy["reject_new_findings"] = True
        self.assertIn("PAL366", {d["rule"] for d in m.evaluate_gates(ambiguous, policy)["diagnostics"]})

    def test_current_birth_cannot_promote_history(self):
        old = normalized((("old", "f", 1),))
        moved = normalized((("moved", "f", 1),))
        moved["findings"][0]["birth_identity"] = old["findings"][0]["birth_identity"]
        moved["findings"][0]["id"] = old["findings"][0]["id"]
        with self.assertRaises(m.MigrationError):
            m.normalize_state(moved)

    def test_closed_fields_booleans_floats_counts_scope_and_inventory(self):
        mutations = [
            lambda s: s.update(schema=True),
            lambda s: s.update(unknown=1),
            lambda s: s["coverage"].update(checked_exports=99),
            lambda s: s["coverage"].update(eligible_functions=True),
            lambda s: s["scope"].update(displayed_paths=["outside.py"]),
            lambda s: s["inputs"]["product_artifacts"].pop("migration.py"),
            lambda s: s["inputs"].update(policy_sha256=0.5),
            lambda s: s["boundaries"][0].update(strict_checked=True),
            lambda s: s["findings"][0].update(rule="PAL360"),
            lambda s: s["findings"][0]["context"].update(extra="forged"),
            lambda s: s["boundaries"][0]["guard_coverage"].update(unknown={})]
        for mutation in mutations:
            state = capture()
            mutation(state)
            with self.subTest(mutation=mutation), self.assertRaises(m.MigrationError):
                m.normalize_state(state)
        state = capture((("", "f", 1),))
        self.assertEqual(m.normalize_state(state)["coverage"]["eligible_modules"], 1)

    def test_current_required_export_and_approval_visibility_preserve_audit_axis(self):
        state = normalized((("core", "f", 0),))
        event = {"boundary": {"kind": "function", "selector": "core:absent", "qualified_name": "absent"},
                 "before": None, "after": {"selector": "core:absent", "engine_status": 1, "engine_rule": "PAL361", "source_evidence": "unverified"},
                 "reason": "current-required-export-absent", "location": None}
        state["current_policy_events"]["required_exports"] = [event]
        state["current_policy_status"] = 1
        compared = m.compare_states(None, state)
        self.assertFalse(compared["reference_observed"])
        self.assertEqual(compared["lost_strict_coverage"], [event])
        self.assertEqual(m.evaluate_gates(compared, state["policy"]["migration"])["status"], 0)
        operation = "pyalamode.integrations.sha256_digest"
        inputs = {"contract_sha256": "a" * 64, "dependency_sha256": "b" * 64, "admission": "denied", "approval": None, "identity_error": None}
        state["inputs"]["integration_inputs"][operation] = inputs
        state["required_operations"] = [{"operation": operation, "required_by": [{"boundary": "core:f", "path": "core.py", "line": 3, "via": "retained", "source_owner": "project"}],
                                         "contract_sha256": inputs["contract_sha256"], "dependency_sha256": inputs["dependency_sha256"],
                                         "admission": "denied", "engine_status": 1, "engine_rule": "PAL350",
                                         "evidence": {"kind": "integration-input", "value": inputs}}]
        state["strict_status"] = 1
        compared = m.compare_states(None, state)
        self.assertEqual(len(compared["approval_failures"]), 1)
        self.assertEqual(m.evaluate_gates(compared, state["policy"]["migration"])["status"], 0)
        state["required_operations"] = []
        self.assertFalse(m.compare_states(None, state)["approval_failures"], "unused denied catalog is not consumed failure")

    def test_marker_effect_policy_and_unsafe_body_events_independent_of_debt(self):
        old = normalized((("core", "f", 0),))
        current = copy.deepcopy(old)
        function = next(b for b in current["boundaries"] if b["kind"] == "function")
        function.update(selected=False, strict_checked=False, mode="off", source_evidence="unchecked ordinary source", selection_reasons=[])
        function["effect_bound"] = ["Clock"]
        function["required_effects"] = ["Clock"]
        function["effect_origins"] = {"Clock": ["f -> clock.now_ns"]}
        recount(current)
        compared = m.compare_states(old, current)
        self.assertTrue(compared["lost_strict_coverage"])
        self.assertEqual(len(compared["expanded_effects"]), 2)
        unsafe = {"boundary": "core:f", "path": "core.py", "line": 1, "scope": "legacy", "rationale": "review",
                  "valid_declaration": True, "source_evidence": "unchecked ordinary unsafe adapter",
                  "behavior": "unknown", "output_boundary": "snapshot starts a new computation"}
        old["unsafe_adapters"] = [unsafe]
        current["unsafe_adapters"] = [unsafe]
        function["definition_sha256"] = "e" * 64
        self.assertEqual(m.compare_states(old, current)["unsafe_weakening"][0]["reason"], "unsafe-adapter-body-changed")

    def test_unused_same_path_manifest_contract_change_is_policy_event(self):
        operation = "pyalamode.integrations.sha256_digest"
        old = normalized((("core", "f", 0),))
        old["policy"]["integration_manifests"] = ["contracts/hash.json"]
        old["inputs"]["integration_inputs"] = {operation: {"contract_sha256": "a" * 64, "dependency_sha256": "b" * 64, "admission": "denied", "approval": None, "identity_error": None}}
        current = copy.deepcopy(old)
        current["inputs"]["integration_inputs"][operation]["contract_sha256"] = "e" * 64
        compared = m.compare_states(old, current)
        self.assertTrue(compared["policy_weakening"])
        self.assertFalse(compared["new_trust"])
        self.assertFalse(compared["approval_failures"])

    def test_nested_comparison_payload_cannot_bypass_closed_schema(self):
        compared = m.compare_states(normalized(), normalized((("core", "f", 2),)))
        compared["new_findings"][0]["after"]["finding"]["context"]["unknown"] = True
        with self.assertRaises(m.MigrationError):
            m.evaluate_gates(compared, m._default_policy()["migration"])
        empty = m.compare_states(None, normalized())
        policy = m._default_policy()["migration"]
        policy["reject_new_findings"] = True
        with self.assertRaises(m.MigrationError):
            m.evaluate_gates(empty, policy)


class LocalRecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def baseline(self, state=None, **kwargs):
        return m.write_baseline(self.root, state or normalized(), owner="team", rationale="reviewed audit debt",
                                prepublish=kwargs.pop("prepublish", lambda: None), **kwargs)

    def test_record_status_is_independent_and_explicit_replace_preserves_history(self):
        state = normalized()
        state["current_policy_status"] = 1
        receipt = self.baseline(state)
        self.assertEqual((receipt["status"], receipt["verified"], receipt["state_strict_status"], receipt["current_policy_status"]), (0, False, 1, 1))
        active = self.root / receipt["path"]
        history = self.root / receipt["history_path"]
        self.assertEqual(active.read_bytes(), history.read_bytes())
        with self.assertRaises(m.MigrationError):
            self.baseline()
        second = self.baseline(normalized((("moved", "f", 1),)), replace=True)
        loaded = m.load_reference(self.root, second["path"])
        self.assertEqual(loaded["state"]["findings"][0]["id"], m.load_reference(self.root, receipt["history_path"])["state"]["findings"][0]["id"])
        self.assertEqual(second["previous_id"], receipt["id"])
        self.assertEqual(active.read_bytes(), (self.root / second["history_path"]).read_bytes())
        self.assertEqual(loaded["record"]["lineage"][0]["previous_path"], "core.py")

    def test_first_bootstrap_records_existing_debt_without_evaluating_history_gate(self):
        state = normalized()
        state["policy"]["migration"]["reject_new_findings"] = True
        receipt = self.baseline(state)
        self.assertEqual(receipt["status"], 0)
        self.assertEqual(m.load_reference(self.root, receipt["path"])["state"]["strict_status"], 1)

    def test_configured_baseline_first_replace_receipts_preserve_default(self):
        default = self.baseline()
        default_raw = (self.root / default["path"]).read_bytes()
        state = normalized()
        state["current_policy_status"] = 1
        state["policy"]["migration"].update(baseline=".pyalamode/team/review.json", reject_new_findings=True)
        first = self.baseline(state)
        self.assertEqual(first["path"], ".pyalamode/team/review.json")
        self.assertEqual(first["previous_id"], None)
        self.assertEqual((first["status"], first["state_strict_status"], first["current_policy_status"], first["verified"]), (0, 1, 1, False))
        loaded = m.load_reference(self.root, first["path"])
        self.assertEqual(loaded["state"]["policy"]["migration"]["baseline"], first["path"])
        self.assertEqual(loaded["record"]["previous_id"], None)
        self.assertEqual(first["history_path"], ".pyalamode/history/" + first["id"] + ".json")
        self.assertEqual((self.root / first["path"]).read_bytes(), (self.root / first["history_path"]).read_bytes())
        with self.assertRaises(m.MigrationError):
            self.baseline(state)
        self.assertEqual((self.root / default["path"]).read_bytes(), default_raw)
        replacement = normalized((("moved", "f", 1),))
        replacement["current_policy_status"] = 1
        replacement["policy"] = copy.deepcopy(state["policy"])
        second = self.baseline(replacement, replace=True)
        self.assertEqual(second["path"], first["path"])
        self.assertEqual(second["previous_id"], first["id"])
        self.assertEqual((second["status"], second["state_strict_status"], second["current_policy_status"]), (0, 1, 1))
        current = m.load_reference(self.root, second["path"])
        self.assertEqual(current["state"]["findings"][0]["id"], loaded["state"]["findings"][0]["id"])
        self.assertEqual(current["record"]["previous_id"], first["id"])
        self.assertEqual((self.root / second["path"]).read_bytes(), (self.root / second["history_path"]).read_bytes())
        self.assertEqual((self.root / default["path"]).read_bytes(), default_raw)

    def test_unsafe_configured_baseline_refuses_before_outside_access(self):
        for path in ("../outside.json", "/outside.json", ".pyalamode/../outside.json", ".pyalamode\\outside.json",
                     ".pyalamode/history/team.json", ".pyalamode/reports/team.json", ".pyalamode/history/nested/team.json"):
            state = normalized()
            state["policy"]["migration"]["baseline"] = path
            with self.subTest(path=path), patch.object(m.os, "open") as opened:
                with self.assertRaises(m.MigrationError):
                    self.baseline(state)
                opened.assert_not_called()
        self.assertFalse((self.root / ".pyalamode").exists())
        with tempfile.TemporaryDirectory() as outside:
            outside_path = Path(outside)
            outside_file = outside_path / "review.json"
            outside_file.write_bytes(b"outside sentinel")
            (self.root / ".pyalamode").mkdir()
            (self.root / ".pyalamode/escape").symlink_to(outside_path, target_is_directory=True)
            state = normalized()
            state["policy"]["migration"]["baseline"] = ".pyalamode/escape/review.json"
            with patch.object(m, "_decode") as decoded:
                with self.assertRaises(m.MigrationError):
                    self.baseline(state)
                decoded.assert_not_called()
            self.assertEqual(outside_file.read_bytes(), b"outside sentinel")
            self.assertFalse((self.root / ".pyalamode/baseline.json").exists())

    def test_report_save_has_no_baseline_or_latest_cursor_and_preserves_status(self):
        state = normalized()
        saved = m.save_report(self.root, report(state), prepublish=lambda: None)
        self.assertEqual(saved["status"], 0)
        self.assertFalse((self.root / ".pyalamode/baseline.json").exists())
        self.assertFalse((self.root / ".pyalamode/latest.json").exists())
        loaded = m.load_reference(self.root, saved["path"])
        self.assertEqual(loaded["record"]["report"]["verified"], False)
        self.assertEqual(loaded["state"]["strict_status"], 1)
        self.assertEqual({p.name for p in (self.root / ".pyalamode/reports").iterdir()}, {saved["id"] + ".json"})

    def test_missing_corrupt_predecessor_duplicate_json_and_forged_lineage_refuse(self):
        with self.assertRaises(m.MigrationError):
            self.baseline(replace=True)
        receipt = self.baseline()
        raw = (self.root / receipt["path"]).read_bytes()
        path = self.root / receipt["path"]
        path.write_bytes(raw.replace(b'"schema": 1', b'"schema": 1, "schema": 1', 1))
        with self.assertRaises(m.MigrationError):
            m.load_reference(self.root, receipt["path"])
        path.write_bytes(raw)
        (self.root / receipt["history_path"]).unlink()
        with self.assertRaises(m.MigrationError):
            self.baseline(replace=True)
        self.assertEqual(path.read_bytes(), raw)

    def test_record_symlink_hardlink_directory_escape_and_callback_missing(self):
        outside = self.root / "outside.json"
        outside.write_text('{"poison": true}')
        (self.root / ".pyalamode").mkdir()
        (self.root / ".pyalamode/baseline.json").symlink_to(outside)
        for relative in (".pyalamode/baseline.json", "../outside.json", "/outside.json", ".pyalamode/../outside.json", ".pyalamode\\outside.json"):
            with self.subTest(relative=relative), self.assertRaises(m.MigrationError):
                m.load_reference(self.root, relative)
        (self.root / ".pyalamode/baseline.json").unlink()
        import os
        os.link(outside, self.root / ".pyalamode/baseline.json")
        with self.assertRaises(m.MigrationError):
            m.load_reference(self.root, ".pyalamode/baseline.json")
        (self.root / ".pyalamode/baseline.json").unlink()
        (self.root / ".pyalamode/history").symlink_to(self.root)
        with self.assertRaises(m.MigrationError):
            self.baseline()
        self.assertEqual(outside.read_text(), '{"poison": true}')
        (self.root / ".pyalamode/history").unlink()
        with self.assertRaises(m.MigrationError):
            self.baseline(prepublish=lambda: True)

    def test_reference_changes_at_each_publication_and_active_failure_leave_old_active(self):
        receipt = self.baseline()
        active = self.root / receipt["path"]
        original = active.read_bytes()
        callbacks = []

        def stale():
            callbacks.append(True)
            if len(callbacks) == 2:
                raise m.MigrationError("source changed before active publication")

        with self.assertRaises(m.MigrationError):
            self.baseline(normalized((("core", "g", 1),)), replace=True, prepublish=stale)
        self.assertEqual(len(callbacks), 2)
        self.assertEqual(active.read_bytes(), original)
        self.assertGreaterEqual(len(list((self.root / ".pyalamode/history").glob("*.json"))), 2)
        self.assertFalse(list((self.root / ".pyalamode").rglob("*.tmp")))
        self.assertFalse((self.root / ".pyalamode/.write-lock").exists())

        def changed_reference():
            active.write_bytes(original + b" ")

        with self.assertRaises(m.MigrationError):
            self.baseline(replace=True, prepublish=changed_reference)
        self.assertEqual(active.read_bytes(), original + b" ")

    def test_staged_content_and_directory_ownership_change_refuse_before_active(self):
        receipt = self.baseline()
        original = (self.root / receipt["path"]).read_bytes()

        def stage_changed():
            for temporary in (self.root / ".pyalamode").rglob("*.tmp"):
                temporary.write_bytes(b"{}")

        with self.assertRaises(m.MigrationError):
            self.baseline(replace=True, prepublish=stage_changed)
        self.assertEqual((self.root / receipt["path"]).read_bytes(), original)

    def test_tooling_overlay_missing_context_duplicate_boundaries_and_limits_not_recordable(self):
        cases = []
        state = normalized()
        state["strict_status"] = 2
        cases.append(state)
        state = normalized()
        state["freshness"] = "current overlay snapshot; unsaved"
        state["inputs"]["sources"]["core.py"].update(origin="overlay", version=1)
        cases.append(state)
        state = capture()
        state["findings"][0]["context"] = {"kind": "unavailable", "reason": "source missing"}
        cases.append(m.normalize_state(state))
        state = capture()
        state["boundaries"].append(copy.deepcopy(state["boundaries"][-1]))
        recount(state)
        cases.append(m.normalize_state(state))
        for state in cases:
            with self.subTest(state=state["freshness"]), self.assertRaises(m.MigrationError):
                self.baseline(state)
        self.assertFalse((self.root / ".pyalamode/baseline.json").exists())
        with patch.object(m, "MAX_BYTES", 100):
            with self.assertRaises(m.MigrationError):
                self.baseline()

    def test_preyield_write_and_fsync_failures_remove_stage_and_lock(self):
        for operation in ("write", "fsync"):
            original = getattr(os, operation)
            calls = []

            def fail_staging(*args):
                calls.append(args)
                # First call persists the transaction lock; second is the stage.
                if len(calls) == 2:
                    raise OSError("injected stage " + operation + " failure")
                return original(*args)

            with self.subTest(operation=operation), patch.object(m.os, operation, side_effect=fail_staging):
                with self.assertRaises(m.MigrationError):
                    self.baseline()
            self.assertFalse((self.root / ".pyalamode/baseline.json").exists())
            self.assertFalse(list((self.root / ".pyalamode").rglob("*.tmp")))
            self.assertFalse((self.root / ".pyalamode/.write-lock").exists())

    def test_postreplace_fsync_failure_restores_prior_active_and_initial_absence(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    receipt = self.baseline()
                    before = (self.root / receipt["path"]).read_bytes()
                else:
                    before = None
                real_replace, real_fsync = os.replace, os.fsync
                committed, failed = [], []

                def observe_replace(source, destination, **kwargs):
                    result = real_replace(source, destination, **kwargs)
                    if destination == "baseline.json":
                        committed.append(True)
                    return result

                def failure_after_replace(descriptor):
                    if committed and not failed:
                        failed.append(True)
                        raise OSError("injected postreplace directory fsync failure")
                    return real_fsync(descriptor)

                with patch.object(m.os, "replace", side_effect=observe_replace), patch.object(m.os, "fsync", side_effect=failure_after_replace):
                    with self.assertRaises(m.MigrationError):
                        self.baseline(normalized((("core", "new", 1),)), replace=existing)
                active = self.root / ".pyalamode/baseline.json"
                if before is None:
                    self.assertFalse(active.exists())
                else:
                    self.assertEqual(active.read_bytes(), before)
                self.assertEqual(len(failed), 1)
                self.assertFalse(list((self.root / ".pyalamode").rglob("*.tmp")))
                self.assertFalse((self.root / ".pyalamode/.write-lock").exists())

    def test_postreplace_readback_failure_restores_prior_active(self):
        receipt = self.baseline()
        before = (self.root / receipt["path"]).read_bytes()
        real_replace, real_read = os.replace, m._Local.read
        committed, failed = [], []

        def observe_replace(source, destination, **kwargs):
            result = real_replace(source, destination, **kwargs)
            if destination == "baseline.json":
                committed.append(True)
            return result

        def fail_readback(local, relative):
            if committed and relative == ".pyalamode/baseline.json" and not failed:
                failed.append(True)
                raise OSError("injected active readback failure")
            return real_read(local, relative)

        with patch.object(m.os, "replace", side_effect=observe_replace), patch.object(m._Local, "read", new=fail_readback):
            with self.assertRaises(m.MigrationError):
                self.baseline(normalized((("core", "new", 1),)), replace=True)
        self.assertEqual((self.root / receipt["path"]).read_bytes(), before)
        self.assertFalse(list((self.root / ".pyalamode").rglob("*.tmp")))

    def test_loaded_digests_do_not_admit_nonrecordable_capture(self):
        receipt = self.baseline()
        original = json.loads((self.root / receipt["path"]).read_text())
        cases = []
        state = normalized()
        state["strict_status"] = 2
        cases.append(state)
        state = normalized()
        state["freshness"] = "stale; recheck required"
        cases.append(state)
        state = normalized()
        state["freshness"] = "current overlay snapshot; unsaved"
        state["inputs"]["sources"]["core.py"].update(origin="overlay", version=1)
        cases.append(state)
        state = capture()
        state["findings"][0]["context"] = {"kind": "unavailable", "reason": "source missing"}
        cases.append(m.normalize_state(state))
        state = capture()
        state["boundaries"].append(copy.deepcopy(state["boundaries"][-1]))
        recount(state)
        cases.append(m.normalize_state(state))
        for state in cases:
            with self.subTest(freshness=state["freshness"], strict=state["strict_status"]):
                forged = copy.deepcopy(original)
                forged["state"] = state
                forged["id"] = m._record_id(forged)
                raw = m._pretty(forged)
                (self.root / receipt["path"]).write_bytes(raw)
                (self.root / ".pyalamode/history" / (forged["id"] + ".json")).write_bytes(raw)
                with self.assertRaises(m.MigrationError):
                    m.load_reference(self.root, receipt["path"])

    def test_lock_cleanup_adds_no_postcommit_durability_operation(self):
        real_fsync = os.fsync
        late_syncs = []

        def refuse_late_sync(descriptor):
            if not (self.root / ".pyalamode/.write-lock").exists():
                late_syncs.append(True)
                raise OSError("ephemeral lock removed after record commit")
            return real_fsync(descriptor)

        with patch.object(m.os, "fsync", side_effect=refuse_late_sync):
            receipt = self.baseline()
        self.assertEqual(receipt["status"], 0)
        self.assertFalse(late_syncs)
        self.assertFalse((self.root / ".pyalamode/.write-lock").exists())
        self.assertEqual(m.load_reference(self.root, receipt["path"])["record"]["id"], receipt["id"])

    def test_changed_noncooperating_active_is_not_blindly_rolled_back(self):
        receipt = self.baseline()
        active = self.root / receipt["path"]
        real_replace, real_fsync = os.replace, os.fsync
        committed, failed = [], []
        other_writer = b'{"another_writer":true}\n'

        def observe_replace(source, destination, **kwargs):
            result = real_replace(source, destination, **kwargs)
            if destination == "baseline.json":
                committed.append(True)
            return result

        def independently_changed(descriptor):
            if committed and not failed:
                failed.append(True)
                active.write_bytes(other_writer)
                raise OSError("postcommit failure after independent active write")
            return real_fsync(descriptor)

        with patch.object(m.os, "replace", side_effect=observe_replace), patch.object(m.os, "fsync", side_effect=independently_changed):
            with self.assertRaisesRegex(m.MigrationError, "safe rollback refused"):
                self.baseline(normalized((("core", "new", 1),)), replace=True)
        self.assertEqual(active.read_bytes(), other_writer)

    def test_valid_digest_cannot_forge_ambiguous_historical_pairing(self):
        first = self.baseline(normalized((("a", "f", 1), ("b", "f", 1))))
        old = m.load_reference(self.root, first["path"])
        replacement = self.baseline(normalized((("c", "f", 1), ("d", "f", 1))), replace=True)
        record = json.loads((self.root / replacement["path"]).read_text())
        self.assertFalse(record["lineage"], "explicit ambiguous reset uses fresh births")
        record["lineage"] = []
        for before, after in zip(old["state"]["findings"], record["state"]["findings"]):
            after["birth_identity"], after["id"] = before["birth_identity"], before["id"]
            record["lineage"].append({"id": before["id"], "previous_identity_key": before["identity_key"],
                                      "current_identity_key": after["identity_key"], "previous_path": before["locations"][0]["path"],
                                      "current_path": after["locations"][0]["path"], "count": 1})
        record["id"] = m._record_id(record)
        forged = m._pretty(record)
        (self.root / replacement["path"]).write_bytes(forged)
        (self.root / ".pyalamode/history" / (record["id"] + ".json")).write_bytes(forged)
        with self.assertRaisesRegex(m.MigrationError, "unique deterministic"):
            m.load_reference(self.root, replacement["path"])

    def test_saved_report_cannot_waive_gate_or_lose_reference_provenance(self):
        first = self.baseline()
        reference = m.load_reference(self.root, first["path"])
        state = normalized((("core", "f", 2),))
        state["policy"]["migration"]["reject_new_findings"] = True
        document = report(state, reference)
        self.assertEqual(document["status"], 1)
        saved = m.save_report(self.root, document, prepublish=lambda: None)
        loaded = m.load_reference(self.root, saved["path"])
        self.assertEqual(loaded["record"]["report"]["status"], 1)
        forged = copy.deepcopy(document)
        forged["gates"]["status"] = 0
        forged["gates"]["diagnostics"] = []
        forged["status"] = 0
        with self.assertRaises(m.MigrationError):
            m.save_report(self.root, forged, prepublish=lambda: None)
        (self.root / first["history_path"]).unlink()
        with self.assertRaises(m.MigrationError):
            m.load_reference(self.root, saved["path"])

    def test_saved_report_cannot_hide_strict_source_behind_recording_status(self):
        state = normalized()
        document = report(state)
        self.assertEqual((document["status"], document["gates"]["status"], state["current_policy_status"]), (1, 0, 0))
        forged = copy.deepcopy(document)
        forged["status"] = 0
        with self.assertRaisesRegex(m.MigrationError, "cannot waive strict source"):
            m.save_report(self.root, forged, prepublish=lambda: None)
        self.assertFalse((self.root / ".pyalamode").exists())
        saved = m.save_report(self.root, document, prepublish=lambda: None)
        self.assertEqual(saved["status"], 0)
        loaded = m.load_reference(self.root, saved["path"])
        self.assertEqual(loaded["record"]["report"]["status"], 1)
        envelope = loaded["record"]
        envelope["report"]["status"] = 0
        envelope["id"] = m._record_id(envelope)
        path = ".pyalamode/reports/" + envelope["id"] + ".json"
        (self.root / path).write_bytes(m._pretty(envelope))
        with self.assertRaisesRegex(m.MigrationError, "cannot waive strict source"):
            m.load_reference(self.root, path)


if __name__ == "__main__":
    unittest.main()
