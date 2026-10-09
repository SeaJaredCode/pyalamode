"""M6 static/source/graph/guard regressions for finite domains and failures."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pyalamode.checker import analyze_source, analyze_sources
from pyalamode.project import check_paths, build_paths

IMPORTS = 'from pyalamode import fun, variant, case, record, Vector, Option, Some, Nothing, Result, Ok, Err, accumulate, Failure, failure_value\n'
DOMAIN = '''@variant
class Choice:
    @case
    class Number:
        value: int
    @case
    class Empty:
        pass
'''

class Domains(unittest.TestCase):
    def checked(self, source, **kwargs):
        result = analyze_source(IMPORTS + source, path='domain.py', **kwargs)
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def rejected(self, source, rule=None, **kwargs):
        result = analyze_source(IMPORTS + source, path='domain.py', **kwargs)
        self.assertFalse(result.verified)
        if rule:
            self.assertIn(rule, [d.rule for d in result.diagnostics], '\n'.join(d.format() for d in result.diagnostics))
        return result

    def test_closed_cases_option_result_and_nested_records(self):
        self.checked('''@record
class Payload:
    number: int
@variant
class Wrapped:
    @case
    class Present:
        value: Payload
    @case
    class Absent:
        pass
@fun
def read(value: Wrapped) -> int:
    match value:
        case Wrapped.Present(value=Payload(number=n)):
            return n
        case Wrapped.Absent():
            return 0
@fun
def option(value: Option[int]) -> int:
    match value:
        case Some(n): return n
        case Nothing(): return 0
@fun
def result(value: Result[int,str]) -> int:
    match value:
        case Ok(n): return n
        case Err(error=_): return 0
@fun
def make(n:int) -> Wrapped:
    return Wrapped.Present(Payload(n))
''')

    def test_accumulation_declared_schemas(self):
        result = self.checked('''@fun
def validate(a: Result[int,str], b: Result[str,str]) -> Result[tuple[int,str],Vector[str]]:
    return accumulate(a,b)
@fun
def local() -> Result[tuple[int,int],Vector[str]]:
    a: Result[int,str] = Err("left")
    b: Result[int,str] = Ok(2)
    return accumulate(a,b)
''')
        self.assertIn('Result.accumulate', result.contracts[0].operations)
        for expression in ['accumulate(Ok(1),Ok(2))', 'accumulate(left=a,right=a)', 'accumulate(a,a,a)']:
            self.rejected('@fun\ndef f(a:Result[int,str]) -> Result[tuple[int,int],Vector[str]]:\n    return ' + expression + '\n', 'PAL221')

    def test_full_case_guards_wildcard_and_partial_binding(self):
        full = DOMAIN + '''@fun
def f(v:Choice)->int:
    match v:
        case Choice.Number(n): return n
        case Choice.Empty(): return 0
'''
        self.checked(full)
        self.rejected(full.replace('Choice.Number(n)', 'Choice.Number(0)'), 'PAL330')
        self.rejected(full.replace('Choice.Number(n):', 'Choice.Number(n) if True:'), 'PAL330')
        self.rejected(full.replace('Choice.Number(n): return n', 'Choice.Number() if False: return 1'), 'PAL330')
        self.checked(full.replace('Choice.Number(n): return n', 'Choice.Number() if True: return 1'))
        wildcard = DOMAIN + '@fun\ndef f(v:Choice)->int:\n    match v:\n        case _: return 0\n'
        self.checked(wildcard)
        self.rejected(wildcard, 'PAL330', policy={'explicit_cases':['domain:Choice']})
        self.rejected('''@record
class Pair:
    left:int
    right:int
@fun
def f(p:Pair)->int:
    match p:
        case Pair(n,0): return n
        case _: return 0
''','PAL330')
        self.rejected(full.replace('def f(v:Choice)', 'def f(v:Choice,n:int)'), 'PAL101')

    def test_nested_case_constraint_is_not_payload_domain_coverage(self):
        prefix = DOMAIN + "@variant\nclass Outer:\n    @case\n    class Value:\n        item:Choice\n"
        for body in ["case Outer.Value(item=Choice.Number(n)):return n", "case Outer.Value(item=Choice.Number()):return 1"]:
            self.rejected(prefix + "@fun\ndef f(x:Outer)->int:\n    match x:\n        " + body + "\n", 'PAL330')
        self.rejected(prefix + "@fun\ndef f(x:Outer)->int:\n    match x:\n        case Outer.Value(item=Choice.Number(n)):return n\n        case _:return 0\n", 'PAL330')
        self.checked(prefix + "@fun\ndef f(x:Outer)->int:\n    match x:\n        case Outer.Value(item=Choice.Number()):return 1\n        case _:return 0\n")
        self.rejected("@variant\nclass Shadow:\n    @case\n    class case:pass\n    @case\n    class Later:pass\n", 'PAL120')

    def test_finite_boolean_and_none_patterns(self):
        self.checked('@fun\ndef f(v:bool)->int:\n    match v:\n        case True:return 1\n        case False:return 0\n')
        self.checked('@fun\ndef f(v:None)->int:\n    match v:\n        case None:return 0\n')
        self.rejected('@fun\ndef f(v:int)->int:\n    match v:\n        case 0:return 0\n        case _:return 1\n','PAL330')

    def test_declarations_and_data_exclude_hidden_behavior(self):
        sources = [DOMAIN.replace('@variant', '@variant()'), '@case\nclass Misplaced:pass\n', DOMAIN.replace('class Choice:', 'class Choice(object):'), DOMAIN.replace('class Number:', 'class Number(object):'), DOMAIN.replace('value: int', 'value: list[int]'), DOMAIN.replace('value: int','value: Choice'), DOMAIN.replace('value: int','value: "Choice.Empty"'), DOMAIN.replace('@case\n    class Number:', '@record\n    class Number:'), DOMAIN.replace('value: int','value: int\n        def hidden(self): return 0'), DOMAIN + 'Choice.Number.__match_args__ = ("other",)\n', DOMAIN + 'alias=Choice.Number\nalias.__match_args__=("other",)\n']
        for source in sources:
            with self.subTest(source=source): self.rejected(source)
        self.rejected(DOMAIN + '@fun\ndef f()->Choice:\n    return Choice.Number(True)\n','PAL221')
        self.rejected('@fun\ndef f()->Option[int]:\n    return Some([])\n')

    def test_declaration_class_default_lookup_matches_actual_python(self):
        record = "@record\nclass Pair:\n    int:int=3\n    value:int=4\n@fun\ndef f()->Pair:return Pair()\n"
        case = "@variant\nclass Lookup:\n    @case\n    class Found:\n        int:int=3\n        value:int=4\n@fun\ndef f()->Lookup:return Lookup.Found()\n"
        for source in [record,case]:
            self.rejected(source, 'PAL130')
            with self.assertRaises(TypeError):exec(compile(IMPORTS+source,'declaration.py','exec'),{})
        for source in [record.replace('int:int=3','TOKEN:bool=True').replace('value:int=4','value:int=TOKEN'),case.replace('int:int=3','TOKEN:bool=True').replace('value:int=4','value:int=TOKEN')]:
            self.rejected('TOKEN=4\n'+source, 'PAL221')
            with self.assertRaises(TypeError):exec(compile(IMPORTS+'TOKEN=4\n'+source,'declaration.py','exec'),{})
        # Explicit string and future schemas use the product's module parser;
        # prior field defaults do not shadow that separate annotation namespace.
        for source in [record.replace('int:int=3','int:"int"=3').replace('value:int=4', 'value:"int"=4'),case.replace('int:int=3','int:"int"=3').replace('value:int=4','value:"int"=4')]:
            self.checked(source)
            namespace={}
            exec(compile(IMPORTS+source,'declaration.py','exec'),namespace)
            self.assertEqual(namespace['f']().value,4)
        for source in [record,case]:
            result=analyze_source('from __future__ import annotations\n'+IMPORTS+source,path='domain.py')
            self.assertTrue(result.verified,[d.reason for d in result.diagnostics])
        self.checked('@record\nclass Pair:\n    first:int=3\n    second:int=first+1\n')

    def test_failure_conversion_remains_opaque(self):
        result = self.checked('''@fun
def f(n:int)->Result[int,Failure]:
    try: return Ok(10//n)
    except ZeroDivisionError as caught:
        return Err(failure_value(caught))
''')
        contract=result.contracts[0]
        self.assertNotIn('ZeroDivisionError',contract.failures)
        self.assertIn('RecursionError',contract.failures)
        self.assertEqual(contract.handlers[0]['target'],'caught')
        for expression in ['caught', 'caught.args', 'caught.__traceback__', 'caught.__dict__', 'str(caught)', 'Some(caught)']:
            with self.subTest(expression=expression):
                self.rejected('@fun\ndef f(n:int)->int:\n    try: return 10//n\n    except ZeroDivisionError as caught:\n        bad=' + expression + '\n        return 0\n')
        self.rejected('@fun\ndef f(n:int)->int:\n    try:return 10//n\n    except Exception:return 0\n','PAL340')
        self.rejected('@fun\ndef f(n:int)->int:\n    try:return 10//n\n    except:return 0\n','PAL340')

    def test_exception_cleanup_collisions_and_partial_try_bindings(self):
        self.rejected('@fun\ndef f(n:int)->int:\n    try:\n        caught=3\n        return 10//n\n    except ZeroDivisionError as caught:return 0\n','PAL101')
        self.rejected('@fun\ndef f(n:int)->int:\n    try:\n        partial=10//n\n        return 1//n\n    except ZeroDivisionError:\n        partial=0\n        return partial\n','PAL101')
        self.rejected('@fun\ndef f(n:int)->int:\n    try:answer=10//n\n    except ZeroDivisionError as caught:answer=0\n    caught=1\n    return answer\n','PAL340')
        self.rejected('@fun\ndef f(n:int)->int:\n    try:return 10//n\n    except ZeroDivisionError as caught:\n        def hidden()->int:\n            ignored=caught\n            return 0\n        return hidden()\n')

    def test_per_call_masks_handler_body_nested_handlers_and_effects(self):
        source='''@fun
def divide(n:int)->int:return 10//n
@fun
def caught(n:int)->int:
    try:return divide(n)
    except ZeroDivisionError:return 0
@fun
def two(n:int)->int:
    try:a=divide(n)
    except ZeroDivisionError:return 0
    return a+divide(n)
@fun
def body(n:int)->int:
    try:return divide(n)
    except ZeroDivisionError:return divide(n)
@fun
def nested(n:int)->int:
    try:
        try:return divide(n)
        except KeyError:return divide(n)
    except ZeroDivisionError:return 0
'''
        result=self.checked(source)
        contracts={c.name:c for c in result.contracts}
        self.assertNotIn('ZeroDivisionError',contracts['caught'].failures)
        self.assertIn('ZeroDivisionError',contracts['two'].failures)
        self.assertIn('ZeroDivisionError',contracts['body'].failures)
        self.assertNotIn('ZeroDivisionError',contracts['nested'].failures)
        self.assertEqual([e['handled'] for e in contracts['two'].failure_edges],[['ZeroDivisionError'],[]])
        effects=self.checked('''from pyalamode import effects,Clock,ClockCapability
@effects(Clock)
def now(cap:ClockCapability)->int:
    try:return cap.now_ns()
    except (RuntimeError,OSError,IndexError):return 0
''').contracts[0]
        self.assertEqual(effects.required_effects,['Clock'])
        self.assertEqual(effects.failures,[])
        self.rejected('''from pyalamode import ClockCapability
@fun
def now(cap:ClockCapability)->int:
    try:return cap.now_ns()
    except RuntimeError:return 0
''','PAL310')

    def test_inherited_category_overlap_and_handlers_do_not_authorize_raise(self):
        for categories in ['(RuntimeError,RecursionError)', '(ValueError,UnicodeError)']:
            self.rejected('@fun\ndef f(n:int)->int:\n    try:return 10//n\n    except '+categories+':return 0\n','PAL340')
        for suffix in ['\n    finally:pass','\n    else:return 0']:
            self.rejected('@fun\ndef f(n:int)->int:\n    try:return 10//n\n    except ZeroDivisionError:return 0'+suffix+'\n','PAL340')
        self.rejected('@fun\ndef f()->int:\n    raise ValueError("bad")\n')

    def test_private_domain_helpers_cannot_crash_or_preserve_certification(self):
        writers = ["from pyalamode.variants import _DomainType\n_DomainType.__setattr__.__code__=unknown\n", "import pyalamode.variants as helper\nhelper._case_info.__code__=unknown\n", "from pyalamode.failures import failure_value\nfailure_value.__code__=unknown\n", "from domain import Choice\nChoice.Number.__init__.__code__=unknown\n"]
        for writer in writers:
            with self.subTest(writer=writer), tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                (root/'domain.py').write_text('# mode: fun\n'+IMPORTS+DOMAIN)
                (root/'consumer.py').write_text('# mode: fun\nfrom domain import Choice\nfrom pyalamode import Result,Failure,Ok,Err,failure_value\ndef f(v:Choice)->int:\n    match v:\n        case _:return 0\ndef convert(n:int)->Result[int,Failure]:\n    try:return Ok(10//n)\n    except ZeroDivisionError as caught:return Err(failure_value(caught))\n')
                (root/'writer.py').write_text(writer)
                result=build_paths([root/'consumer.py',root/'writer.py'],root=root,output=root/'out')
                self.assertEqual(result.status,1)
                self.assertFalse(result.verified);self.assertFalse((root/'out').exists())

    def test_private_public_api_imports_retain_canonical_foundation_gates(self):
        for imports in ['from pyalamode.variants import Option,Some\n', 'import pyalamode.variants as v\n']:
            source = imports + 'import pyalamode.variants as writer\nwriter._case_info.__code__=unknown\n' + ('@fun\ndef f()->Option[int]:return Some(1)\n' if 'from ' in imports else '@fun\ndef f()->v.Option[int]:return v.Some(1)\n')
            self.rejected(source)

    def test_builtin_family_case_writers_invalidate_identity_nested_and_warm_guards(self):
        for symbol, affected, untouched in [('Some','Option[int]','Result[int,str]'),('Nothing','Option[int]','Result[int,str]'),('Ok','Result[int,str]','Option[int]'),('Err','Result[int,str]','Option[int]')]:
            for route in ['public','from_private','private_module']:
                with self.subTest(symbol=symbol,route=route),tempfile.TemporaryDirectory() as temp:
                    root=Path(temp)
                    imports = 'from pyalamode import fun,Vector\nfrom pyalamode.variants import Option,Result\n' if route=='from_private' else 'from pyalamode import fun,Vector,Option,Result\n'
                    (root/'affected.py').write_text(imports+'@fun\ndef identity(value:'+affected+')->'+affected+':return value\n@fun\ndef nested(value:Vector['+affected+'])->Vector['+affected+']:return value\n')
                    (root/'untouched.py').write_text('from pyalamode import fun,Option,Result\n@fun\ndef identity(value:'+untouched+')->'+untouched+':return value\n')
                    (root/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="exports"\nguarded_exports=["affected:identity"]\n')
                    for _ in range(2):self.assertEqual(check_paths([root/'affected.py',root/'untouched.py'],root=root).status,0)
                    writer = 'from pyalamode import '+symbol+'\n'+symbol+'.__setattr__=unknown\n' if route=='public' else 'from pyalamode.variants import '+symbol+' as alias\nalias.__setattr__=unknown\n' if route=='from_private' else 'import pyalamode.variants as v\nv.'+symbol+'.__init__.__code__=unknown\n'
                    (root/'writer.py').write_text(writer)
                    run=check_paths([root/'affected.py',root/'untouched.py',root/'writer.py'],root=root)
                    self.assertEqual(run.status,1)
                    affected_result=next(r for r in run.results if Path(r.path).name=='affected.py')
                    self.assertFalse(affected_result.cache_hit)
                    self.assertFalse(affected_result.verified)
                    self.assertTrue(next(r for r in run.results if Path(r.path).name=='untouched.py').verified)
                    self.assertEqual(check_paths([root/'affected.py',root/'untouched.py',root/'writer.py'],root=root).status,1)
                    built=build_paths([root/'affected.py',root/'writer.py'],root=root,output=root/'out')
                    self.assertEqual(built.status,1);self.assertFalse((root/'out').exists())

    def test_debug_prefix_accounts_for_unused_pattern_and_handler_targets(self):
        for capture in ['_pyalamode_guard_validate','_pyalamode_guard_return_10']:
            with self.subTest(capture=capture),tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                (root/'domain.py').write_text(IMPORTS+DOMAIN+'@fun\ndef f(v:Choice)->int:\n    match v:\n        case Choice.Number('+capture+'):return 7\n        case Choice.Empty():return 0\n')
                (root/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="debug"\n')
                result=build_paths([root/'domain.py'],root=root,output=root/'out')
                self.assertEqual(result.status,0)
                env={**os.environ,'PYTHONPATH':str(root/'out')+os.pathsep+str(Path(__file__).resolve().parents[1])}
                run=subprocess.run([sys.executable,'-c','from domain import Choice,f\nassert f(Choice.Number(5))==7'],cwd=root/'out',env=env,capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr)

    def test_debug_prefix_accounts_for_unused_handler_targets_and_schema_aliases(self):
        for target in ['_pyalamode_guard_validate','_pyalamode_guard_module0']:
            with self.subTest(target=target),tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                (root/'core.py').write_text(IMPORTS+'@fun\ndef f(n:int)->Failure:\n    try:\n        quotient=10//n\n        return Failure("ok","completed")\n    except ZeroDivisionError as '+target+':return Failure("failed","division")\n')
                (root/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="debug"\n')
                result=build_paths([root/'core.py'],root=root,output=root/'out')
                self.assertEqual(result.status,0)
                env={**os.environ,'PYTHONPATH':str(root/'out')+os.pathsep+str(Path(__file__).resolve().parents[1])}
                run=subprocess.run([sys.executable,'-c','from core import f\nassert f(0).category=="failed"\nassert f(2).category=="ok"'],cwd=root/'out',env=env,capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr)

    def test_case_addition_and_partial_warm_failure_edges(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'domain.py').write_text('# mode: fun\n'+IMPORTS+DOMAIN)
            (root/'consumer.py').write_text('# mode: fun\nfrom domain import Choice\ndef f(v:Choice)->int:\n    match v:\n        case Choice.Number(n):return n\n        case Choice.Empty():return 0\n')
            self.assertEqual(check_paths([root/'consumer.py'],root=root).status,0)
            warm=check_paths([root/'consumer.py'],root=root)
            self.assertTrue(all(r.cache_hit for r in warm.results))
            (root/'domain.py').write_text((root/'domain.py').read_text()+'    @case\n    class Added:pass\n')
            self.assertEqual(check_paths([root/'consumer.py'],root=root).status,1)
            (root/'consumer.py').write_text('# mode: fun\nfrom domain import Choice\ndef f(v:Choice)->int:\n    match v:\n        case _:return 0\n')
            self.assertEqual(check_paths([root/'consumer.py'],root=root).status,0)
            (root/'callee.py').write_text('# mode: fun\ndef divide(n:int)->int:return 10//n\n')
            (root/'caller.py').write_text('# mode: fun\nfrom callee import divide\ndef f(n:int)->int:\n    try:a=divide(n)\n    except ZeroDivisionError:return 0\n    return a+divide(n)\n')
            cold=check_paths([root/'caller.py'],root=root)
            warm=check_paths([root/'caller.py'],root=root)
            (root/'ordinary.py').write_text('unrelated=1\n')
            partial=check_paths([root/'caller.py',root/'ordinary.py'],root=root)
            def contract(run):return next(c for r in run.results for c in r.contracts if c.name=='f').__dict__
            self.assertEqual(contract(cold),contract(warm))
            self.assertEqual(contract(warm),contract(partial))
            self.assertIn('ZeroDivisionError',contract(partial)['failures'])

    def test_build_nonexecution_and_off_exports_debug_real_runs(self):
        for mode in ['off','exports','debug']:
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                (root/'domain.py').write_text(IMPORTS+DOMAIN+'@fun\ndef f(v:Choice)->int:\n    match v:\n        case Choice.Number(n):return n\n        case Choice.Empty():return 0\n')
                if mode!='off':
                    (root/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="'+mode+'"\nguarded_exports=["domain:f"]\n')
                output=root/'out'
                result=build_paths([root/'domain.py'],root=root,output=output)
                self.assertEqual(result.status,0,[d.reason for d in result.tooling]+[d.reason for r in result.results for d in r.diagnostics])
                module='domain' if mode=='off' else 'pyalamode_exports.domain'
                script='from domain import Choice\nfrom '+module+' import f\nassert f(Choice.Number(4))==4\n'
                env={**os.environ,'PYTHONPATH':str(output)+os.pathsep+str(Path(__file__).resolve().parents[1])}
                run=subprocess.run([sys.executable,'-c',script],cwd=output,env=env,capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr)
                if mode!='off':
                    bad=subprocess.run([sys.executable,'-c','from '+module+' import f\nf(object())'],cwd=output,env=env,capture_output=True,text=True)
                    self.assertNotEqual(bad.returncode,0)
                    self.assertIn('domain:f',bad.stderr)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);marker=root/'executed'
            (root/'bad.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n'+IMPORTS+DOMAIN+'@fun\ndef f(v:Choice)->int:\n    match v:\n        case Choice.Empty():return 0\n')
            result=build_paths([root/'bad.py'],root=root,output=root/'out')
            self.assertEqual(result.status,1)
            self.assertFalse(marker.exists());self.assertFalse((root/'out').exists())

if __name__=='__main__':unittest.main()
