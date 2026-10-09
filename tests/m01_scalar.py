import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode import fun
from pyalamode.checker import analyze_source
from pyalamode.model import TARGET
from pyalamode.project import build_paths, check_paths

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "from pyalamode import fun\n"


class ScalarAcceptance(unittest.TestCase):
    def check(self, source):
        return analyze_source(PREFIX + source, "sample.py")

    def assertRule(self, source, rule):
        result = self.check(source)
        self.assertIn(rule, [d.rule for d in result.diagnostics], result.to_dict())
        self.assertFalse(result.verified)
        return result

    def test_A01_scalar_and_ordinary_execution(self):
        source = (ROOT / "examples/pricing.py").read_text()
        result = analyze_source(source)
        self.assertTrue(result.verified, result.to_dict())
        self.assertEqual(result.analyzed_call_sites, 1)
        namespace = {"__name__": "example"}
        exec(source, namespace)
        self.assertEqual(namespace["discounted_total"](1500, 200), 1300)
        self.assertEqual(namespace["discounted_total"](100, 200), 0)
        self.assertEqual(result.contracts[0].boundary_protection, "unguarded")

    def test_A02_reassignment_first_binding(self):
        result = self.assertRule("@fun\ndef f(x: int) -> int:\n    y = x\n    y = 1\n    return y\n", "PAL101")
        self.assertEqual(next(d for d in result.diagnostics if d.rule == "PAL101").first_binding, "sample.py:4")
        result = self.assertRule("@fun\ndef f(x: int) -> int:\n    x += 1\n    return x\n", "PAL101")
        self.assertEqual(result.diagnostics[0].first_binding, "sample.py:3")

    def test_A03_exclusive_branches_and_early_return(self):
        for body in [
            "if flag:\n        y = 1\n    else:\n        y = 2\n    return y",
            "if flag:\n        y = 1\n        return y\n    y = 2\n    return y",
            "if flag:\n        return 1\n    else:\n        y = 2\n    return y",
            "if True:\n        y = 1\n    else:\n        y = 2\n    return y",
        ]:
            with self.subTest(body=body):
                result = self.check("@fun\ndef f(flag: bool) -> int:\n    " + body + "\n")
                self.assertTrue(result.verified, result.to_dict())
        self.assertRule("@fun\ndef f(flag: bool) -> int:\n    if flag:\n        y = 1\n    return y\n", "PAL102")
        self.assertRule("@fun\ndef f(flag: bool) -> int:\n    if flag:\n        y = 1\n    y = 2\n    return y\n", "PAL101")

    def test_A04_exact_inputs_subclass_mutable_unknown(self):
        function = "@fun\ndef f(x: int) -> int:\n    return x + 1\n"
        for caller in ["f(True)", "f([])", "class IntChild(int): pass\nf(IntChild(1))",
                       "def shell(x: int):\n    return f(x)", "f(unknown)"]:
            with self.subTest(caller=caller):
                self.assertRule(function + caller + "\n", "PAL221")
        self.assertTrue(self.check(function + "value = 1\nf(value)\n").verified)
        self.assertRule(function + "value = 1\nvalue = []\nf(value)\n", "PAL221")

    def test_A05_audit_no_certificate_or_execution(self):
        result = analyze_source(PREFIX + "@fun\ndef f(x: int) -> int:\n    print(x)\n    return x\n", audit=True)
        self.assertEqual(result.status, 0)
        self.assertFalse(result.verified)
        self.assertEqual(result.contracts[0].source_evidence, "unverified: audit or failed selected gate")
        self.assertTrue(result.diagnostics)

    def test_A06_unknown_calls_shadowing_and_constructs(self):
        for expression in ["print(x)", "hash(x)", "x / 2", "x ** 2", "x.__add__(1)", "unknown(x)", "[x]", "(x,)", "x[0]", "f'{x}'", "(y := x)"]:
            with self.subTest(expression=expression):
                result = self.check(f"@fun\ndef f(x: int) -> int:\n    return {expression}\n")
                self.assertFalse(result.verified, result.to_dict())
        self.assertRule("abs = lambda x: x\n@fun\ndef f(x: int) -> int:\n    return abs(x)\n", "PAL240")
        self.assertRule("@fun\ndef f(x: int) -> int:\n    y = abs(x)\n    abs = x\n    return y\n", "PAL240")
        for statement in ["for y in x:\n        pass", "while True:\n        pass", "import os", "raise ValueError()", "global x", "del x", "def nested():\n        return 1", "match x:\n        case _: pass"]:
            with self.subTest(statement=statement):
                self.assertFalse(self.check(f"@fun\ndef f(x: int) -> int:\n    {statement}\n    return x\n").verified)

    def test_A07_defaults_and_decorators_not_evaluated(self):
        for declaration in ["@fun\ndef f(x: int = explode()) -> int:\n    return x\n",
                            "@explode()\n@fun\ndef f(x: int) -> int:\n    return x\n",
                            "@fun()\ndef f(x: int) -> int:\n    return x\n",
                            "@fun\ndef f(x: explode()) -> int:\n    return 1\n"]:
            self.assertFalse(self.check(declaration).verified)
        # Importing this source would touch a file; checker must only parse it.
        with tempfile.TemporaryDirectory() as directory:
            flag = Path(directory) / "executed"
            result = self.check(f"open({str(flag)!r}, 'w').write('bad')\n@fun\ndef f(x: int = explode()) -> int:\n    return x\n")
            self.assertFalse(result.verified)
            self.assertFalse(flag.exists())

    def test_A33_identity_has_ordinary_behavior(self):
        def ordinary(x):
            x.append(1)
            return x
        self.assertIs(fun(ordinary), ordinary)
        self.assertEqual(fun(ordinary)([]), [1])
        self.assertEqual(set(ordinary.__dict__), set())
        @fun
        def accepts_subclass(x: int) -> int:
            return x + 1
        class Child(int):
            pass
        self.assertEqual(accepts_subclass(Child(1)), 2)

    def test_published_operations_and_failures(self):
        for parameters, returns, expression in [
            ("x: int", "int", "abs(-x) + min(x, 2, 3) * max(x, 1) // 2 % 3"),
            ("x: str", "str", "min(x, 'z') + max(x, 'a')"),
            ("x: bytes", "int", "len(x + b'a')"),
            ("x: bool, y: bool", "bool", "not x and y or x == y"),
            ("x: int", "bool", "1 < x <= 10"),
            ("x: int", "bool", "x is not None"),
            ("x: bool", "int", "1 if x else 2"),
            ("x: None", "None", "None"),
        ]:
            result = self.check(f"@fun\ndef f({parameters}) -> {returns}:\n    return {expression}\n")
            self.assertTrue(result.verified, result.to_dict())
        result = self.check("@fun\ndef f(x: int, divisor: int) -> int:\n    return x // divisor\n")
        self.assertEqual(result.contracts[0].failures, ["ZeroDivisionError"])

    def test_wrong_operands_fail_closed(self):
        for expression in ["True + 1", "1 == True", "1 + 'a'", "not 1", "1 and 2", "True < False", "1 is 1", "None == None", "len(1)", "abs(True)", "min(1)", "max(1, True)", "min(1, 2, key=abs)", "min([1, 2])"]:
            self.assertFalse(self.check(f"@fun\ndef f() -> int:\n    return {expression}\n").verified, expression)
        self.assertRule("@fun\ndef f(x: int) -> int:\n    if x:\n        return 1\n    return 2\n", "PAL210")
        self.assertRule("@fun\ndef f(x: bool) -> int:\n    if x:\n        return 1\n", "PAL211")

    def test_dead_source_still_has_closed_expression_vocabulary(self):
        for body in ["return 1\n    value = unknown_operation()", "if False:\n        value = []\n    return 1",
                     "return 1\n    value = x / 2", "return 1\n    value = f'{x}'",
                     "return 1\n    value = True + 1", "return 1\n    value: float = 1",
                     "return 1\n    a = b = 1"]:
            self.assertFalse(self.check("@fun\ndef f(x: int) -> int:\n    " + body + "\n").verified, body)
        result = self.check("@fun\ndef f(x: int) -> int:\n    return x\n    x = x + 1\n    x = x + 2\n")
        self.assertTrue(result.verified, result.to_dict())

    def test_annotations_nonexecuted_whitelist(self):
        self.assertTrue(self.check("@fun\ndef f(x: 'int') -> 'int':\n    return x\n").verified)
        self.assertTrue(analyze_source("from types import NoneType\n" + PREFIX + "@fun\ndef f(x: NoneType) -> NoneType:\n    return x\n").verified)
        for annotation in ["Any", "list[int]", "int | float", "bool | int", "'open(1)'", "float", "Child", "typing.Any"]:
            self.assertRule(f"@fun\ndef f(x: {annotation}) -> int:\n    return 1\n", "PAL130")
        self.assertRule("int = str\n@fun\ndef f(x: int) -> int:\n    return 1\n", "PAL130")
        self.assertRule("import types\nalias = types\nalias.NoneType = int\nfrom types import NoneType\n@fun\ndef f(x: NoneType) -> NoneType:\n    return None\n", "PAL130")

    def test_global_and_local_alias_regressions(self):
        function = "@fun\ndef checked(x: int) -> int:\n    return abs(x)\n"
        for mutation in ["import builtins as b\nalias = b\nalias.abs = lambda x: 1\n",
                         "globals()['abs'] = lambda x: 1\n",
                         "namespace = globals()\nnamespace['abs'] = lambda x: 1\n",
                         "import builtins as b\nb.__dict__['abs'] = lambda x: 1\n",
                         "import builtins as b\nsetattr(b, 'abs', lambda x: 1)\n"]:
            self.assertRule(mutation + function, "PAL240")
        self.assertRule("import builtins as b\nalias = b\nalias.int = str\n" + function, "PAL130")
        for mutation in ["import pyalamode as p\np.fun = lambda x: x\n",
                         "import pyalamode as p\nalias = p\nalias.fun = lambda x: x\n"]:
            self.assertFalse(analyze_source(mutation + PREFIX + function).verified)
        result = self.check(function + "def shell(checked):\n    return checked(True)\n")
        self.assertTrue(result.verified, result.to_dict())
        self.assertEqual(result.analyzed_call_sites, 0)
        result = self.check(function + "def one():\n    alias = checked\n    return alias(1)\ndef two(alias):\n    return alias(True)\n")
        self.assertTrue(result.verified, result.to_dict())
        self.assertEqual(result.analyzed_call_sites, 1)
        self.assertRule(function + "alias = checked\nalias(True)\n", "PAL221")
        self.assertRule(function + "first = second = checked\nfirst(True)\n", "PAL221")
        self.assertRule(function + "shell = lambda checked=checked(True): checked\n", "PAL221")
        result = self.check(function + "def shell(*checked):\n    return checked(True)\ndef shell2(**checked):\n    return checked(True)\n")
        self.assertTrue(result.verified, result.to_dict())
        self.assertEqual(result.analyzed_call_sites, 0)
        result = self.check(function + "def shell(flag):\n    if flag:\n        value = 1\n        return checked(value)\n")
        self.assertTrue(result.verified, result.to_dict())
        self.assertEqual(result.analyzed_call_sites, 1)

    def test_marker_resolution_and_duplicate_exports(self):
        for declaration in ["from pyalamode import fun as scalar\n@scalar\ndef f(x: int) -> int:\n    return x\n",
                            "import pyalamode as p\n@p.fun\ndef f(x: int) -> int:\n    return x\n"]:
            self.assertTrue(analyze_source(declaration).verified)
        self.assertRule("fun = lambda x: x\n@fun\ndef f(x: int) -> int:\n    return x\n", "PAL120")
        result = analyze_source("@unrelated.fun\ndef ordinary():\n    print('shell')\n")
        self.assertEqual(result.selected_functions, 0)
        result = self.check('@fun\ndef f() -> int:\n    """A literal:\n# mode: fun\n    """\n    return 1\n')
        self.assertTrue(result.verified, result.to_dict())
        result = analyze_source("def fun(f): return f\n@fun\ndef ordinary():\n    print('shell')\n")
        self.assertEqual(result.selected_functions, 0)
        duplicate = "@fun\ndef selected(x: int) -> int:\n    return x\nalias = selected\n@fun\ndef selected(x: str) -> str:\n    return x\nalias('wrong')\n"
        self.assertRule(duplicate, "PAL240")
        self.assertRule("@fun\ndef f(x: int) -> int:\n    return x\nf = replacement\n", "PAL240")

    def test_all_binding_forms_and_direct_caller_sites(self):
        function = "@fun\ndef checked(x: int) -> int:\n    return abs(x)\n"
        self.assertRule("match (lambda value: value):\n    case abs:\n        pass\n" + function, "PAL240")
        self.assertRule("def patch():\n    import builtins as library\n    library.abs = lambda value: 1\n" + function, "PAL240")
        self.assertRule("class Patch:\n    global abs\n    abs = lambda value: 1\n" + function, "PAL240")
        for site in ["class C(checked([])): pass", "def shell(x: checked([])): pass",
                     "match 1:\n    case 1:\n        checked([])",
                     "def shell(x=checked([])): pass", "f = lambda: checked([])",
                     "[checked(x) for x in [1]]"]:
            self.assertRule(function + site + "\n", "PAL221")
        result = self.check(function + "lambda checked: checked([])\n[checked([]) for checked in functions]\n")
        self.assertTrue(result.verified, result.to_dict())
        self.assertEqual(result.analyzed_call_sites, 0)

    def test_parameters_and_keyword_call_signatures(self):
        function = "@fun\ndef f(x: int, /, y: str, *, flag: bool) -> int:\n    return x if flag else len(y)\n"
        self.assertTrue(self.check(function + "f(1, 'a', flag=True)\n").verified)
        for call in ["f(x=1,y='a',flag=True)", "f(1,'a')", "f(1,'a',True)", "f(1,'a',flag=True,other=1)", "f(*args)", "f(1,'a',flag=1)"]:
            self.assertRule(function + call + "\n", "PAL221")


class ProjectAcceptance(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "pricing.py"
        self.source.write_text((ROOT / "examples/pricing.py").read_text())

    def cli(self, *arguments):
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        return subprocess.run([sys.executable, "-m", "pyalamode", *map(str, arguments)], cwd=self.root,
                              env=env, capture_output=True, text=True)

    def test_A01_build_source_unchanged_and_stock_python(self):
        output = self.root / "artifact"
        result = build_paths([self.source], root=self.root, output=output)
        self.assertEqual(result.status, 0, result.to_dict())
        self.assertEqual((output / "pricing.py").read_bytes(), self.source.read_bytes())
        evidence = json.loads((output / "pyalamode-evidence.json").read_text())
        self.assertTrue(evidence["verified"])
        self.assertEqual(evidence["files"][0]["contracts"][0]["boundary_protection"], "unguarded")
        process = subprocess.run([sys.executable, output / "pricing.py"], env={**os.environ, "PYTHONPATH": str(ROOT)}, capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout.strip(), "1300")

    def test_failed_build_no_artifact_and_existing_artifact_retained(self):
        self.source.write_text((ROOT / "tests/fixtures/m01/invalid_reassignment.py").read_text())
        output = self.root / "failed"
        result = build_paths([self.source], root=self.root, output=output)
        self.assertEqual(result.status, 1)
        self.assertFalse(output.exists())
        existing = self.root / "old"
        existing.mkdir()
        (existing / "retained").write_text("old evidence")
        self.assertEqual(build_paths([self.source], root=self.root, output=existing).status, 1)
        self.assertEqual((existing / "retained").read_text(), "old evidence")

    def test_A08_tooling_target_and_audit_statuses(self):
        self.assertEqual(self.cli("check", "missing.py").returncode, 2)
        self.assertEqual(self.cli("check", self.source, "--target", "cpython-3.14.0").returncode, 2)
        unsupported = self.root / "unsupported"
        self.assertEqual(self.cli("build", self.source, "--target", "cpython-3.14.0", "--output", unsupported).returncode, 2)
        self.assertFalse(unsupported.exists())
        self.source.write_text("bad syntax (\n")
        self.assertEqual(self.cli("check", "--audit", self.source).returncode, 2)
        self.source.write_text((ROOT / "tests/fixtures/m01/invalid_reassignment.py").read_text())
        self.assertEqual(self.cli("check", self.source).returncode, 1)
        process = self.cli("check", "--audit", "--json", self.source)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertFalse(json.loads(process.stdout)["verified"])

    def test_cache_freshness_cold_warm_source_policy_and_loss(self):
        cold = check_paths([self.source], root=self.root)
        warm = check_paths([self.source], root=self.root)
        self.assertEqual(cold.status, 0)
        self.assertFalse(cold.results[0].cache_hit)
        self.assertTrue(warm.results[0].cache_hit)
        self.source.write_text(self.source.read_text().replace("result = 0", "result = []"))
        changed = check_paths([self.source], root=self.root)
        self.assertEqual(changed.status, 1)
        self.assertFalse(changed.results[0].cache_hit)
        cache_file = self.root / ".pyalamode-cache" / f"{changed.results[0].fingerprint}.json"
        cache_file.write_text("corrupt")
        repeated = check_paths([self.source], root=self.root)
        self.assertEqual(repeated.status, changed.status)
        cache_file.unlink()
        self.assertEqual(check_paths([self.source], root=self.root).status, changed.status)
        (self.root / "pyproject.toml").write_text('[tool.pyalamode]\nschema = 1\nexternal_trust = "allow"\n')
        self.assertEqual(check_paths([self.source], root=self.root).status, 2)

    def test_build_bypasses_cache_and_freshness_failure_is_atomic(self):
        check_paths([self.source], root=self.root)
        original = self.source.read_bytes()
        real_read = Path.read_bytes
        counter = 0
        def changing(path):
            nonlocal counter
            if path.resolve() == self.source.resolve():
                counter += 1
                if counter == 2:
                    return original + b"# relevant changed bytes\n"
            return real_read(path)
        output = self.root / "changed"
        with patch.object(Path, "read_bytes", changing):
            result = build_paths([self.source], root=self.root, output=output)
        self.assertEqual(result.status, 2, result.to_dict())
        self.assertFalse(output.exists())
        self.assertFalse(list(self.root.glob(".pyalamode-build-*")))

    def test_actual_product_artifact_changes_invalidate_cache(self):
        from pyalamode.model import foundation_identities
        first = check_paths([self.source], root=self.root)
        self.assertTrue(check_paths([self.source], root=self.root).results[0].cache_hit)
        different = {**foundation_identities(), "__init__.py": "different-product-bytes"}
        with patch("pyalamode.checker.foundation_identities", return_value=different):
            changed = check_paths([self.source], root=self.root)
        self.assertFalse(changed.results[0].cache_hit)
        self.assertNotEqual(changed.results[0].fingerprint, first.results[0].fingerprint)

    def test_explanation_and_empty_build(self):
        self.assertEqual(self.cli("explain", "PAL101").returncode, 0)
        self.assertIn("exact int", self.cli("explain", "abs").stdout)
        self.assertEqual(self.cli("explain", "missing").returncode, 2)
        self.source.write_text("def ordinary():\n    print('ordinary')\n")
        result = build_paths([self.source], root=self.root, output=self.root / "empty")
        self.assertEqual(result.status, 2)
        self.assertFalse((self.root / "empty").exists())

    def test_malformed_policy_returns_tooling_status(self):
        for policy in ['tool = "invalid"\n', '[tool]\npyalamode = [1]\n', '[tool.pyalamode]\nschema = true\n']:
            (self.root / "pyproject.toml").write_text(policy)
            process = self.cli("check", self.source, "--json")
            self.assertEqual(process.returncode, 2, process.stderr)
            self.assertFalse(json.loads(process.stdout)["verified"])


if __name__ == "__main__":
    unittest.main()
