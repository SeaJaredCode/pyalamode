"""M7 exact standard catalog, latent wrappers, setup and ordinary build gates."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.checker import analyze_source, analyze_sources
from pyalamode.project import check_paths, build_paths
from pyalamode.model import runtime_environment
from pyalamode.checker import fingerprint
from pyalamode.standard_contracts import operation_catalog, operation_contract, SCALAR_SIGNATURES

PREFIX = '''from typing import Callable
from pyalamode import fun, Vector, OrderedMap, Result, Ok, Err, Failure, failure_value
from pyalamode import text_split, text_join, text_replace, text_startswith, text_slice
from pyalamode import integer_clamp, integer_parse_decimal, integer_format_decimal
from pyalamode import utf8_encode, utf8_decode, hex_encode, hex_decode
from pyalamode import vector_scan, vector_group_by, compose, partial_first, result_traverse
from pyalamode import effects, Effectful, Clock, ClockCapability, IO, IOCapability, Environment, EnvironmentCapability
from pyalamode import live_io, live_clock, live_environment, recorded_clock
'''
FUNCTIONS = '''@fun
def increment(x:int)->int:return x+1
@fun
def double(x:int)->int:return x*2
@fun
def multiply(rate:int,value:int)->int:return rate*value
@fun
def add(total:int,value:int)->int:return total+value
@fun
def key(value:int)->int:return value%2
@fun
def checked(value:int)->Result[int,str]:
    if value<0:return Err("negative")
    return Ok(value)
'''


class StandardSource(unittest.TestCase):
    def checked(self, source, **kwargs):
        result = analyze_source(PREFIX + source, path="standard_core.py", **kwargs)
        self.assertTrue(result.verified, "\n".join(d.format() for d in result.diagnostics))
        return result

    def rejected(self, source, rule=None, **kwargs):
        result = analyze_source(PREFIX + source, path="standard_core.py", **kwargs)
        self.assertFalse(result.verified)
        if rule:
            self.assertIn(rule, [d.rule for d in result.diagnostics], "\n".join(d.format() for d in result.diagnostics))
        return result

    def test_every_scalar_catalog_signature_alias_and_failure(self):
        for name, (parameters, returned, failures) in SCALAR_SIGNATURES.items():
            args = ",".join(f"p{i}:{kind}" for i, kind in enumerate(parameters))
            call = ",".join(f"p{i}" for i in range(len(parameters)))
            for spelling, importing in [(name, ""), ("alias", f"from pyalamode.standard import {name} as alias\n"), ("std."+name, "import pyalamode.standard as std\n"), ("pa.standard."+name, "import pyalamode as pa\n")]:
                with self.subTest(name=name, spelling=spelling):
                    result = self.checked(importing + f"@fun\ndef f({args})->{returned}:return {spelling}({call})\n")
                    self.assertEqual(result.contracts[0].failures, sorted(failures))
                    row = result.contracts[0].operation_contracts[0]
                    self.assertEqual(row["identity"], "pyalamode.standard."+name)
                    self.assertEqual(row["version"], "pyalamode.standard-v1")
                    self.assertEqual(row["effects"], [])

    def test_catalog_is_fully_detached(self):
        rows = operation_catalog()
        self.assertEqual(len(rows), 22)
        for row in rows:
            self.assertTrue(all(field in row for field in ("identity", "version", "inputs", "output", "effects", "failures", "aliases", "initialization", "evidence", "foundations", "approval")))
        rows[0]["initialization"]["effects"].append("IO")
        rows[0]["foundations"].append("foreign")
        self.assertEqual(operation_catalog()[0]["initialization"]["effects"], [])
        self.assertNotIn("foreign", operation_catalog()[0]["foundations"])

    def test_scalar_signature_foreign_and_dynamic_operations_refuse(self):
        for expression in ["text_split(s)", "text_split(text=s,separator=',')", "text_split(s,1)", "text_slice(s,True,2)", "integer_clamp(True,0,1)", "utf8_encode(s,'utf-8')", "hex_decode(s,'ignore')", "s.encode('utf-8')", "s.format()", "int(s)", "str(1)", "__import__('json').loads(s)"]:
            with self.subTest(expression=expression):
                self.rejected("@fun\ndef f(s:str)->str:return " + expression + "\n")
        self.rejected("class Foreign(str):pass\n@fun\ndef f(s:Foreign)->str:return text_replace(s,'a','b')\n", "PAL130")
        self.rejected("text_replace=print\n@fun\ndef f(s:str)->str:return text_replace(s,'a','b')\n")

    def test_pure_scalar_definition_initialization_is_distinct(self):
        result = self.checked("# filler\n@fun\ndef f(x:int=integer_parse_decimal('12'))->int:return x\n")
        self.assertEqual(result.contracts[0].definition_failures, ["ValueError"])
        module = analyze_source("# mode: fun\n" + PREFIX + "STAMP=utf8_encode('abc')\nNUMBER=integer_parse_decimal('12')\n", path="init.py")
        self.assertTrue(module.verified, [d.format() for d in module.diagnostics])
        self.assertEqual(module.initialization_evidence, "checked pure source initialization")
        self.assertEqual(module.initialization_failures, ["UnicodeError", "ValueError"])
        self.rejected(FUNCTIONS + "@fun\ndef f(c:Callable[[int],int]=compose(increment,double))->int:return c(1)\n", "PAL221")

    def test_eager_scan_grouping_result_traversal_exact_schemas(self):
        result = self.checked(FUNCTIONS + '''@fun
def scan(v:Vector[int])->Vector[int]:return vector_scan(v,add,0)
@fun
def grouped(v:Vector[int])->OrderedMap[int,Vector[int]]:return vector_group_by(v,key)
@fun
def traversed(v:Vector[int])->Result[Vector[int],str]:return result_traverse(v,checked)
''')
        self.assertTrue(all(c.operation_contracts for c in result.contracts[-3:]))
        self.rejected(FUNCTIONS + "@fun\ndef f(v:Vector[int])->Vector[int]:return vector_scan(v,increment,0)\n", "PAL221")
        self.rejected(FUNCTIONS + "@fun\ndef f(v:Vector[int])->Vector[int]:return vector_scan(v,add,True)\n", "PAL221")
        self.rejected(FUNCTIONS + "@fun\ndef f(v:Vector[int])->Result[Vector[int],str]:return result_traverse(v,increment)\n", "PAL221")
        self.rejected("@fun\ndef key(v:int)->Vector[int]:return Vector.of(v)\n@fun\ndef f(v:Vector[int])->OrderedMap[int,Vector[int]]:return vector_group_by(v,key)\n", "PAL221")

    def test_composition_and_partial_invoke_wrapper_signature(self):
        result = self.checked(FUNCTIONS + '''@fun
def f(v:Vector[int])->Vector[int]:
    scaled=partial_first(multiply,3)
    action=compose(increment,scaled)
    return v.map(action)
''')
        last = result.contracts[-1]
        self.assertEqual({target.rsplit("::",1)[-1] for target in last.invoked_targets}, {"multiply","increment"})
        self.assertIn("standard.compose.invoke", last.operations)
        self.assertIn("standard.partial_first.invoke", last.operations)
        for expression in ["compose(multiply,increment)", "partial_first(increment,2)", "partial_first(multiply,True)"]:
            self.rejected(FUNCTIONS+"@fun\ndef f()->Callable[[int],int]:return "+expression+"\n", "PAL221")
        self.rejected(FUNCTIONS+"@fun\ndef f()->int:\n    c=partial_first(multiply,2)\n    return c(1,2)\n", "PAL221")

    def test_latent_callback_effects_failures_and_trust(self):
        result = self.checked('''@effects(Clock)
def read(prefix:int,c:ClockCapability)->int:return prefix+c.now_ns()
@fun
def factory()->Effectful[[ClockCapability],int,Clock]:return partial_first(read,2)
@effects(Clock)
def use(c:ClockCapability)->int:
    action=factory()
    return action(c)
''')
        factory = next(c for c in result.contracts if c.name == "factory")
        used = next(c for c in result.contracts if c.name == "use")
        self.assertEqual(factory.required_effects, [])
        self.assertEqual(factory.failures, [])
        self.assertEqual(factory.invoked_targets, [])
        self.assertTrue(any(t.endswith("::read") for t in factory.callable_dependencies))
        self.assertEqual(factory.return_callable_evidence["effect_bound"], ["Clock"])
        self.assertTrue(any("effects-v1" in trust for trust in factory.trust))
        self.assertEqual(used.required_effects, ["Clock"])
        self.assertIn("OSError", used.failures)
        self.rejected('''@effects(Clock)
def read(x:int,c:ClockCapability)->int:return c.now_ns()
@effects(Clock)
def bad(c:ClockCapability)->Callable[[int],int]:return partial_first(read,c)
''', "PAL221")

    def test_factory_specialization_retains_actual_tight_choices(self):
        result = self.checked(FUNCTIONS + '''@fun
def factory(cb:Effectful[[int],int,Clock],flag:bool)->Effectful[[int],int,Clock]:
    choice=compose(increment,cb) if flag else partial_first(multiply,2)
    return choice
@fun
def use(n:int,flag:bool)->int:
    chosen=factory(double,flag)
    return chosen(n)
''')
        used = next(c for c in result.contracts if c.name == "use")
        self.assertEqual(used.required_effects, [])
        self.assertEqual(used.failures, [])
        self.assertTrue({"increment","double","multiply"}.issubset({t.rsplit("::",1)[-1] for t in used.invoked_targets}))

    def test_unicode_conditional_envelope_and_occurrence_masks(self):
        result = self.checked('''@fun
def encoding(s:str)->bytes:return utf8_encode(s)
@fun
def size(data:bytes)->int:return len(data)
@fun
def invoke(cb:Callable[[str],bytes],s:str)->bytes:return cb(s)
@fun
def both(s:str)->int:
    action=compose(size,encoding)
    try:
        first=action(s)
    except UnicodeError:
        return action(s)
    return first
''')
        self.assertIn("UnicodeError", next(c for c in result.contracts if c.name == "invoke").failures)
        both = next(c for c in result.contracts if c.name == "both")
        edges = [edge for edge in both.failure_edges if edge["target"].endswith("::encoding")]
        self.assertEqual(len(edges), 2)
        self.assertEqual({tuple(edge["handled"]) for edge in edges}, {(), ("UnicodeError",)})
        self.assertIn("UnicodeError", both.failures)

    def test_capture_wrapper_descriptor_and_bound_schema(self):
        result = self.checked(FUNCTIONS + '''@fun
def factory(rate:int)->Callable[[int],int]:
    bound=partial_first(multiply,rate)
    @fun
    def inner(n:int)->int:return bound(n)
    return compose(increment,inner)
''')
        nested = next(c for c in result.contracts if c.name == "factory.inner")
        self.assertEqual(nested.callable_capture_evidence["bound"]["bound_arguments"][0][0], "int")
        evidence = next(c for c in result.contracts if c.name == "factory").return_callable_evidence
        self.assertTrue(evidence["components"][1]["captured_callbacks"])
        self.rejected(FUNCTIONS + "@fun\ndef f(rate:int)->Callable[[int],int]:\n    action=partial_first(multiply,rate)\n    rate=2\n    return action\n", "PAL101")

    def test_wrapper_intermediate_validation_failure_in_map_and_handlers(self):
        result = self.checked('''@fun
def wrap(n:int)->Vector[int]:return Vector.of(n)
@fun
def size(v:Vector[int])->int:return len(v)
@fun
def direct(n:int)->int:
    action=compose(size,wrap)
    return action(n)
@fun
def mapped(v:Vector[int])->Vector[int]:
    action=compose(size,wrap)
    return v.map(action)
@fun
def handled(n:int)->int:
    action=compose(size,wrap)
    try:return action(n)
    except RecursionError:return 0
''')
        for name in ["direct", "mapped"]:
            self.assertIn("RecursionError", next(c for c in result.contracts if c.name == name).failures)
        self.assertNotIn("RecursionError", next(c for c in result.contracts if c.name == "handled").failures)

    def test_native_helper_and_data_writers_refuse(self):
        writers = ["import builtins\nbuiltins.ord=print\n", "from builtins import ord as native\nnative.__code__=print.__code__\n", "import pyalamode.standard as std\nstd._exact=print\n", "from pyalamode.standard import _exact as helper\nhelper.__code__=print.__code__\n", "import pyalamode as pa\npa.standard.utf8_encode=print\n", "import pyalamode.collections as col\ncol.Vector=print\n", "import pyalamode.standard_contracts as meta\nmeta.SCALAR_SIGNATURES.clear()\n"]
        body = "@fun\ndef f(s:str)->bytes:return utf8_encode(s)\n"
        for writer in writers:
            with self.subTest(writer=writer):
                self.rejected(writer+body)

    def test_shared_product_function_globals_alias_writers_refuse(self):
        for owner in ["std.text_replace", "std.compose", "failure_value", "live_io", "effects", "freeze", "thaw", "record", "variant", "Vector.fold"]:
            for writing in [f"{owner}.__globals__['str']=print", f"namespace={owner}.__globals__\nnamespace['str']=print", f"{owner}.__globals__.update({{'str':print}})"]:
                with self.subTest(owner=owner, writing=writing):
                    self.rejected("import pyalamode.standard as std\nfrom pyalamode import freeze,thaw,record,variant\n"+writing+"\n@fun\ndef f(s:str)->bytes:return utf8_encode(s)\n")
        self.rejected(FUNCTIONS+"action=compose(increment,double)\naction.__globals__['str']=print\n@fun\ndef f(s:str)->bytes:return utf8_encode(s)\n")
        for writing in ["std.text_replace.__globals__['__builtins__']['str']=print", "namespace=std._exact.__globals__['__builtins__']\nnamespace.update(str=print)", "namespace=std._exact.__globals__.get('__builtins__')\nnamespace['str']=print"]:
            self.rejected("import pyalamode.standard as std\n"+writing+"\n@fun\ndef f(s:str)->bool:return text_startswith(s,'a')\n")
        local=self.rejected("@fun\ndef holder()->int:return 1\nnamespace=holder.__globals__\nnamespace['utf8_encode']=print\n@fun\ndef sibling(s:str)->bytes:return utf8_encode(s)\n", "PAL240")
        self.assertTrue(any(d.boundary=="sibling" and d.rule=="PAL240" for d in local.diagnostics))


class StandardProjects(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "core.py"

    def tearDown(self):
        self.temp.cleanup()

    def test_full_partial_warm_recursive_descriptor_equivalence(self):
        library = self.root / "library.py"
        library.write_text("# mode: fun\n"+PREFIX+FUNCTIONS+'''@fun
def factory(cb:Callable[[int],int],flag:bool)->Callable[[int],int]:
    bound=partial_first(multiply,3)
    return compose(bound,cb) if flag else compose(cb,bound)
''')
        self.source.write_text("# mode: fun\n"+PREFIX+"from library import factory,increment\n@fun\ndef f(x:int,flag:bool)->int:\n    action=factory(increment,flag)\n    return action(x)+1\n")
        cold = check_paths([self.source], root=self.root)
        self.assertEqual(cold.status, 0, [d.format() for r in cold.results for d in r.diagnostics])
        warm = check_paths([self.source], root=self.root)
        self.assertTrue(all(r.cache_hit for r in warm.results))
        self.assertEqual([r.contracts for r in cold.results], [r.contracts for r in warm.results])
        self.source.write_text(self.source.read_text().replace("+1", "+2"))
        partial = check_paths([self.source], root=self.root)
        fresh = check_paths([self.source], root=self.root, cache=False)
        self.assertEqual(partial.status, 0)
        self.assertTrue(next(r for r in partial.results if r.path == str(library)).cache_hit)
        self.assertEqual([r.contracts for r in partial.results], [r.contracts for r in fresh.results])
        used = next(c for r in partial.results for c in r.contracts if c.name == "f")
        self.assertTrue(any(t.endswith("::multiply") for t in used.invoked_targets))

    def test_setup_report_and_strict_import_initialization_policy(self):
        setup = self.root / "setup.py"
        setup.write_text(PREFIX+f"provider=live_io({str(self.root)!r},allowed_ops=('read_text','write_text'))\nclock=live_clock()\nenvironment=live_environment()\n@fun\ndef pure(s:str)->str:return text_replace(s,'a','b')\n")
        result = check_paths([setup], root=self.root)
        self.assertEqual(result.status, 0)
        file = result.results[0]
        self.assertEqual(file.initialization_evidence, "unchecked ordinary module initialization")
        by_name = {r["identity"]: r for r in file.setup_observations}
        self.assertEqual(by_name["pyalamode.live_io"]["effects"], ["IO"])
        self.assertEqual(by_name["pyalamode.live_clock"]["effects"], [])
        self.assertEqual(file.contracts[0].behavior, "pure")
        self.assertEqual(file.contracts[0].required_effects, [])
        warm = check_paths([setup], root=self.root)
        self.assertEqual(file.setup_observations, warm.results[0].setup_observations)
        self.source.write_text("# mode: fun\n"+PREFIX+"from setup import pure\n@fun\ndef f(s:str)->str:return pure(s)\n")
        denied = check_paths([self.source], root=self.root)
        self.assertEqual(denied.status, 1)
        self.assertTrue(any(d.rule == "PAL241" for r in denied.results for d in r.diagnostics))

    def test_new_native_writer_invalidates_warm_evidence_and_binary_io(self):
        self.source.write_text(PREFIX+"@effects(IO)\ndef f(c:IOCapability,p:str)->str:return c.read_text(p)\n@fun\ndef encode(s:str)->bytes:return utf8_encode(s)\n")
        self.assertEqual(check_paths([self.source], root=self.root).status, 0)
        self.assertTrue(check_paths([self.source], root=self.root).results[0].cache_hit)
        writer = self.root / "writer.py"
        writer.write_text("from builtins import chr as native\nnative.__code__=print.__code__\n")
        warm = check_paths([self.source, writer], root=self.root)
        fresh = check_paths([self.source, writer], root=self.root, cache=False)
        self.assertEqual(warm.status, 1)
        self.assertEqual(fresh.status, 1)
        self.assertFalse(next(r for r in warm.results if r.path == str(self.source)).cache_hit)
        self.assertTrue(any("standard dependency" in identity for r in warm.results for identity in r.binding_context))

    def test_failed_unknown_default_full_warm_is_not_tooling_crash(self):
        sentinel=self.root/"sentinel"
        self.source.write_text(PREFIX+f"from pathlib import Path\ndef mark(*args):\n    Path({str(sentinel)!r}).write_text('executed')\n    return '1'\n@fun\ndef f(s:str=mark())->int:return integer_parse_decimal(s)\n")
        cold=check_paths([self.source],root=self.root)
        warm=check_paths([self.source],root=self.root)
        self.assertEqual(cold.status,1)
        self.assertEqual(warm.status,1)
        self.assertTrue(warm.results[0].cache_hit)
        self.assertEqual(cold.results[0].contracts,warm.results[0].contracts)
        self.assertFalse(sentinel.exists())

    def test_native_filesystem_configuration_gate_and_fingerprint(self):
        self.source.write_text(PREFIX+"@fun\ndef f(s:str)->bytes:return utf8_encode(s)\n")
        supported=check_paths([self.source],root=self.root)
        self.assertEqual(supported.status,0)
        self.assertEqual(supported.to_dict()["runtime_environment"],runtime_environment())
        original=fingerprint(self.source.read_bytes())
        with patch("sys.getfilesystemencoding",return_value="ascii"):
            denied=check_paths([self.source],root=self.root)
            self.assertEqual(denied.status,2)
            self.assertNotEqual(original,fingerprint(self.source.read_bytes()))
            self.assertIn("filesystem",denied.tooling[0].reason)
        with patch("sys.getfilesystemencodeerrors",return_value="strict"):
            self.assertEqual(check_paths([self.source],root=self.root).status,2)

    def test_actual_cli_off_exports_debug_and_nonexecuting_failure(self):
        self.source.write_text(PREFIX+'''@fun
def f(s:str)->str:
    values=text_split(s,",")
    return text_join(values,"|")
''')
        for mode in ["off", "exports", "debug"]:
            with self.subTest(mode=mode):
                policy = "[tool.pyalamode]\nboundary_guards="+repr(mode)+"\n"
                if mode == "exports":
                    policy += 'guarded_exports=["core:f"]\n'
                (self.root / "pyproject.toml").write_text(policy)
                output = self.root / mode
                build = subprocess.run([sys.executable,"-m","pyalamode","build",str(self.source),"--root",str(self.root),"--output",str(output),"--json"],capture_output=True,text=True)
                self.assertEqual(build.returncode,0,build.stdout+build.stderr)
                report=json.loads(build.stdout)
                self.assertEqual(report["standard_operation_version"],"pyalamode.standard-v1")
                self.assertEqual(len(report["product_artifacts"]),26)
                module="pyalamode_exports.core" if mode=="exports" else "core"
                run=subprocess.run([sys.executable,"-c",f"from {module} import f;print(f('1,2,3'))"],cwd=output,capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr)
                self.assertEqual(run.stdout.strip(),"1|2|3")
                if mode in {"off","exports"}:
                    self.assertEqual((output/"core.py").read_bytes(),self.source.read_bytes())
                if mode!="off":
                    bad=subprocess.run([sys.executable,"-c",f"from {module} import f;f(['mutable'])"],cwd=output,capture_output=True,text=True)
                    self.assertNotEqual(bad.returncode,0)
                    self.assertIn("TypeError",bad.stderr)
        sentinel=self.root/"sentinel"
        self.source.write_text(PREFIX+f"open({str(sentinel)!r},'w').write('executed')\n@fun\ndef f(s:str)->bytes:return s.encode('utf-8')\n")
        failed=build_paths([self.source],root=self.root,output=self.root/"failed")
        self.assertEqual(failed.status,1)
        self.assertFalse(sentinel.exists())
        self.assertFalse((self.root/"failed").exists())


if __name__ == "__main__":
    unittest.main()
