"""Static records and optional ordinary-Python boundary build conformance."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.checker import RECORD_FOUNDATIONS, analyze_source, analyze_sources
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths, check_paths


PREFIX = 'from pyalamode import record,replace,fun,Vector,Map,OrderedMap,Set,freeze,thaw\n'
POINT = '@record\nclass Point:\n    x:int\n    tags:Vector[str]=Vector[str].of()\n'


class RecordsStatic(unittest.TestCase):
    def good(self, source):
        result = analyze_source(source, 'sample.py')
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def bad(self, source, rule=None):
        result = analyze_source(source, 'sample.py')
        self.assertFalse(result.verified, source)
        if rule:
            self.assertIn(rule, {d.rule for d in result.diagnostics})
        return result

    def test_records_defaults_fields_constructors_replacement_and_evidence(self):
        result = self.good('# mode: fun\n' + PREFIX + POINT + '''BASE=Point(1)
def f(p:Point,tag:str)->Point:
    tags=p.tags.appended(tag)
    return replace(p,tags=tags)
def make()->Point:return Point(tags=Vector.of("a"),x=2)
def same(p:Point,q:Point)->bool:return p==q
''')
        self.assertEqual(result.records[0]['fields'], {'x':'int','tags':'Vector[str]'})
        record=result.records[0]
        self.assertEqual(record['enforcement'],'strict')
        self.assertEqual(record['source_evidence'],'checked record declaration')
        self.assertIn('trusted product',record['implementation_evidence'])
        self.assertEqual(record['failures'],['RecursionError'])
        self.assertEqual(record['definition_failures'],[])
        self.assertIn('TypeError',record['ordinary_validation_failures'])
        self.assertEqual(record['freshness'],'current for recorded inputs')
        audit=analyze_source(PREFIX+POINT,'sample.py',audit=True)
        self.assertEqual(audit.records[0]['enforcement'],'audit')
        self.assertEqual(audit.records[0]['source_evidence'],'unverified record declaration')
        self.assertEqual(audit.records[0]['freshness'],'no successful checked claim')
        f = next(c for c in result.contracts if c.name == 'f')
        self.assertTrue(any('records-v1' in trust for trust in f.trust))
        self.assertIn('Record.replace', f.operations)
        self.assertIn('RecursionError', f.failures)
        self.assertEqual(f.boundary_protection, 'unguarded')
        self.good(PREFIX + '@record\nclass Names:\n    self:int\n    value:int\n@fun\ndef names()->Names:\n    original=Names(self=1,value=2)\n    return replace(original,value=3)\n')

    def test_nested_records_in_collections_and_callbacks_remain_data(self):
        self.good(PREFIX + POINT + '''@record
class Envelope:
    points:Vector[Point]
    pair:tuple[Point,int]
@fun
def x(p:Point)->int:return p.x
@fun
def f(e:Envelope)->Vector[int]:return e.points.map(x)
''')
        self.bad(PREFIX + POINT + 'from typing import Callable\n@record\nclass Bad:\n    cb:Callable[[int],int]\n', 'PAL130')

    def test_A16_nested_mutability_exact_types_and_invalid_field_signatures(self):
        for expression in ['Point(True)', 'Point(1,tags=["a"])', 'Point(1,tags=Vector.of(1))',
                           'Point()', 'Point(1,Vector.of("a"),2)', 'Point(1,unknown=2)',
                           'replace(p,x=True)', 'replace(p,unknown=2)', 'replace(p,tags=("a",))',
                           'replace(p,**{})', 'replace(p,2)']:
            with self.subTest(expression=expression):
                self.bad(PREFIX + POINT + f'@fun\ndef f(p:Point)->Point:return {expression}\n', 'PAL221')

    def test_unsupported_record_behavior_never_evaluated(self):
        declarations = ['@record\nclass P(object):\n    x:int', '@record\nclass P(metaclass=type):\n    x:int',
                        '@record\nclass P:\n    x:int\n    def __init__(self):print(1)',
                        '@record\nclass P:\n    x:int\n    @property\n    def value(self):print(1)',
                        '@record\nclass P:\n    x:int\n    _private:int',
                        '@record\nclass P:\n    x:int=1\n    y:int',
                        '@record\nclass P:\n    x:int=[]', '@record\nclass P:\n    x:int=print(1)',
                        '@record\nclass P:\n    x:int\n    x:int',
                        '@record\nclass P:\n    x:int\n    extra=1']
        for declaration in declarations:
            with self.subTest(declaration=declaration):
                self.bad(PREFIX + declaration + '\n')

    def test_forward_and_recursive_record_schemas_refused(self):
        for annotation in ['Later', 'Vector[Later]', 'tuple[Later]', 'Vector[First]', '"Later"']:
            self.bad('from __future__ import annotations\n' + PREFIX + f'@record\nclass First:\n    x:{annotation}\n@record\nclass Later:\n    y:int\n')
        self.bad(PREFIX + '@record\nclass First:\n    x:Later\n@record\nclass Later:\n    y:int\n')
        self.bad(PREFIX + '@record\nclass First:\n    x:int=LATER\nLATER=1\n')
        for decorator, imported in [('record','from pyalamode import record,fun'),
                                    ('pal.record','import pyalamode as pal\nfrom pyalamode import fun'),
                                    ('mark','from pyalamode import record as mark,fun')]:
            self.bad(f'@{decorator}\nclass P:\n    x:int\n{imported}\n@fun\ndef f(p:P)->int:return p.x\n', 'PAL120')
        self.bad('mark=record\nfrom pyalamode import record,fun\n@mark\nclass P:\n    x:int\n@fun\ndef f(p:P)->int:return p.x\n', 'PAL120')
        self.bad('from pyalamode import fun\n@fun\ndef f(x:tuple[int]=V)->int:return x[0]\nV=(1,)\n')
        self.bad('from pyalamode import fun\n@fun\ndef f(x:"Vector[int]"=Vector.of(1))->int:return len(x)\nfrom pyalamode import Vector\n', 'PAL221')

    def test_default_dependency_and_class_writers_refused(self):
        for writer in ['Point.x=1', 'Point.__eq__=print', 'alias=Point\nalias.__init__=print',
                       'setattr(Point,"__eq__",print)', 'from builtins import setattr as put\nput(Point,"__eq__",print)',
                       'import builtins as b\nb.setattr(Point,"__eq__",print)', 'put=setattr\nput(Point,"__eq__",print)',
                       'from builtins import delattr as put\nput(Point,"__eq__")',
                       'Point.__dict__.__setitem__("__eq__",print)']:
            with self.subTest(writer=writer):
                self.bad(PREFIX + POINT + writer + '\n@fun\ndef f(p:Point)->bool:return p==p\n')

    def test_record_runtime_finite_foundation_writers_refused(self):
        for module, names in RECORD_FOUNDATIONS.items():
            for name in names:
                with self.subTest(module=module,name=name):
                    self.bad(PREFIX + POINT + f'import {module} as backend\nbackend.{name}=print\n@fun\ndef f(p:Point)->Point:return replace(p,x=2)\n')
        for writer in ['import pyalamode.records as r\nr._RECORDS=()',
                       'import pyalamode.records as r\nr._record_values=print',
                       'from pyalamode.records import replace as replacement\nreplacement.__code__=print',
                       'import pyalamode.boundaries as r\nr.validate_data=print']:
            self.bad(PREFIX + POINT + writer + '\n@fun\ndef f(p:Point)->Point:return replace(p,x=2)\n')
        self.good('from pyalamode import fun\nimport sys\n@fun\ndef f(x:int)->int:return x\nsys.modules={}\n')

    def test_ignored_replace_and_unknown_record_dispatch_refused(self):
        self.bad(PREFIX + POINT + '@fun\ndef f(p:Point)->int:\n    replace(p,x=2)\n    return 1\n', 'PAL250')
        for expression in ['p.unknown', 'p.__dict__', 'p.__eq__(p)', 'p<p', 'hash(p)', 'str(p)', 'f"{p}"']:
            self.bad(PREFIX + POINT + f'@fun\ndef f(p:Point)->int:\n    item={expression}\n    return 1\n')
        self.bad(PREFIX + POINT + '@record\nclass Other:\n    x:int\n@fun\ndef f(p:Point,o:Other)->bool:return p==o\n', 'PAL210')

    def test_shell_explicit_snapshot_schema_establishes_call_data_only(self):
        self.good(PREFIX + '''@fun
def total(v:Vector[int])->int:return v[0]
def shell(raw):
    snapshot=freeze(raw,exclusive=True,schema=Vector[int])
    return total(snapshot)
''')
        self.good(PREFIX + POINT + '''@fun
def coordinate(p:Point)->int:return p.x
def shell(raw,adapter):
    snapshot=freeze(raw,exclusive=True,adapter=adapter,schema=Point)
    return coordinate(snapshot)
''')
        for conversion in ['freeze(raw,schema=Vector[int])', 'freeze(raw,exclusive=False,schema=Vector[int])',
                           'freeze(raw,exclusive=True)', 'raw', 'thaw(raw)']:
            self.bad(PREFIX + f'@fun\ndef total(v:Vector[int])->int:return len(v)\ndef shell(raw):\n    snapshot={conversion}\n    return total(snapshot)\n', 'PAL221')

    def test_freeze_thaw_are_not_pure_body_default_or_initializer_operations(self):
        for expression in ['freeze(v,exclusive=True,schema=Vector[int])','thaw(v)']:
            self.bad(PREFIX + f'@fun\ndef f(v:Vector[int])->Vector[int]:return {expression}\n', 'PAL230')
        self.bad('# mode: fun\n' + PREFIX + 'V=freeze([1],exclusive=True,schema=Vector[int])\n')
        self.bad(PREFIX + '@fun\ndef f(v:Vector[int]=freeze([1],exclusive=True,schema=Vector[int]))->int:return len(v)\n')

    def test_import_alias_and_cross_module_record_identity(self):
        sources = {'/tmp/core.py':'# mode: fun\nfrom pyalamode import record\n@record\nclass P:\n    x:int\n',
                   '/tmp/app.py':'# mode: fun\nfrom core import P as Point\nfrom pyalamode import replace\ndef f(p:Point)->Point:return replace(p,x=2)\n'}
        results = analyze_sources(sources,root='/tmp')
        self.assertTrue(all(r.verified for r in results.values()), [d.format() for r in results.values() for d in r.diagnostics])
        self.assertEqual(results['/tmp/app.py'].contracts[0].parameters,{'p':"Record['core:P']"})

    def test_boundary_schema_names_cannot_be_shadowed_by_shell_parameters(self):
        self.bad(PREFIX + '''@fun
def total(v:Vector[int])->int:return len(v)
def shell(raw,Vector):
    snapshot=freeze(raw,exclusive=True,schema=Vector[int])
    return total(snapshot)
''', 'PAL221')

    def test_checked_initialization_cycles_refuse_eager_member_imports(self):
        cases = [('from b import g\ndef f(x:int)->int:return g(x)', 'from a import f\ndef g(x:int)->int:return x'),
                 ('import b\nVALUE=b.VALUE\ndef f(x:int)->int:return x', 'import a\nVALUE=1\ndef g(x:int)->int:return x'),
                 ('import b\ndef f(x:int=b.VALUE)->int:return x', 'import a\nVALUE=1\ndef g(x:int)->int:return x')]
        for a,b in cases:
            with self.subTest(a=a,b=b):
                results=analyze_sources({'/tmp/a.py':'# mode: fun\n'+a+'\n','/tmp/b.py':'# mode: fun\n'+b+'\n'},root='/tmp')
                self.assertTrue(any(d.rule=='PAL241' and d.origin=='checked initialization cycle' for r in results.values() for d in r.diagnostics))
                self.assertTrue(any(r.initialization_evidence.startswith('unverified') for r in results.values()))
        results=analyze_sources({'/tmp/a.py':'# mode: fun\nimport b\ndef f(x:int)->int:return b.g(x)\n',
                                 '/tmp/b.py':'# mode: fun\nimport a\ndef g(x:int)->int:return x\n'},root='/tmp')
        self.assertTrue(all(r.verified for r in results.values()),[d.format() for r in results.values() for d in r.diagnostics])


class RecordsBuild(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.source=self.root/'core.py'
        self.source.write_text('from pyalamode import fun\n@fun\ndef inner(x:int)->int:return x+1\n@fun\ndef outer(x:int)->int:return inner(x)+1\n')

    def tearDown(self):
        self.temp.cleanup()

    def policy(self, mode, exports=('core:outer',)):
        (self.root/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards='+json.dumps(mode)+'\nguarded_exports='+json.dumps(list(exports))+'\n')

    def build(self, name='artifact'):
        output=self.root/name
        sources=[self.source]+[self.root/name for name in ('other.py','writer.py') if (self.root/name).exists()]
        result=build_paths(sources,root=self.root,output=output)
        self.assertEqual(result.status,0,[d.format() for d in result.tooling]+[d.format() for r in result.results for d in r.diagnostics])
        return output,result

    def run_artifact(self, output, code):
        env={**os.environ,'PYTHONPATH':str(output)+os.pathsep+str(Path(__file__).resolve().parents[1])}
        result=subprocess.run([sys.executable,'-c',code],cwd=output,env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        return result.stdout

    def test_A34_default_unguarded_artifact_and_export_facade(self):
        plain,_=self.build('plain')
        self.assertFalse((plain/'pyalamode_exports').exists())
        self.assertEqual((plain/'core.py').read_bytes(),self.source.read_bytes())
        self.policy('exports')
        output,result=self.build()
        self.assertEqual((output/'core.py').read_bytes(),self.source.read_bytes())
        self.assertEqual(result.guarded_exports[0]['public_boundary'],'pyalamode_exports.core:outer')
        self.assertEqual(result.guarded_exports[0]['original_protection'],'unguarded')
        self.run_artifact(output,'''import core
from pyalamode_exports.core import outer
assert outer(1)==3
assert outer.__wrapped__ is core.outer
assert core.outer(True)==3
try: outer(True)
except TypeError as error: assert 'argument x' in str(error)
else: raise AssertionError('bool admitted as exact int')
''')

    def test_record_only_boundary_builds_and_invalid_class_never_publishes(self):
        self.source.write_text('from pyalamode import record\n@record\nclass Point:\n    x:int\n')
        output,result=self.build()
        self.assertEqual(result.to_dict()['coverage']['selected_records'],1)
        self.assertEqual(result.to_dict()['coverage']['selected_functions'],0)
        self.run_artifact(output,'from core import Point\nassert Point(2).x==2\n')
        self.source.write_text('from pyalamode import record\n@record\nclass Bad:\n    x:int=[]\n')
        invalid=self.root/'invalid-record'
        self.assertEqual(build_paths([self.source],root=self.root,output=invalid).status,1)
        self.assertFalse(invalid.exists())

    def test_A35_export_guard_validation_not_repeated_on_internal_calls(self):
        self.policy('exports')
        output,_=self.build()
        self.run_artifact(output,'''import sys,pyalamode.boundaries as boundary
from pyalamode_exports.core import outer
events=[]
def profile(frame,event,arg):
    if event=='call' and frame.f_code is boundary.validate_data.__code__: events.append(1)
sys.setprofile(profile)
assert outer(3)==5
sys.setprofile(None)
assert len(events)==2,events
''')

    def test_guard_invalid_nested_input_rejected_before_body_and_no_hooks(self):
        self.source.write_text('from pyalamode import fun,record,Vector\n@record\nclass P:\n    tags:Vector[int]\n@fun\ndef outer(p:P)->int:return len(p.tags)\n')
        self.policy('exports')
        output,_=self.build()
        self.run_artifact(output,'''import sys,core
from pyalamode import Vector
from pyalamode_exports.core import outer
v=object.__new__(Vector);object.__setattr__(v,'_items',([1],))
p=core.P(Vector.of(1));object.__setattr__(p,'tags',v)
calls=[]
def profile(frame,event,arg):
    if event=='call' and frame.f_code is core.outer.__code__:calls.append(1)
sys.setprofile(profile)
try:outer(p)
except TypeError as error:assert 'tags' in str(error)
else:raise AssertionError('mutable nested input accepted')
assert calls==[]
assert core.outer(p)==1
assert calls==[1]
sys.setprofile(None)
''')

    def test_guard_exact_subclass_and_return_validation(self):
        self.policy('exports')
        output,_=self.build()
        self.run_artifact(output,'''from pyalamode_exports.core import outer
class Evil(int):
    def __add__(self,other):raise AssertionError('foreign hook called')
try:outer(Evil(1))
except TypeError:pass
else:raise AssertionError('subclass accepted')
''')
        self.source.write_text('from pyalamode import fun\n@fun\ndef outer()->int:return VALUE\nVALUE=1\n')
        output,_=self.build('return_checked')
        self.run_artifact(output,'''import core
from pyalamode_exports.core import outer
core.VALUE=[]
try:outer()
except TypeError as error:assert 'return' in str(error)
else:raise AssertionError('invalid return accepted')
''')

    def test_facade_preserves_positional_keyword_only_defaults_and_identity(self):
        self.source.write_text('from pyalamode import fun,Vector\nBASE=Vector.of(1)\n@fun\ndef outer(x:int=1,/,y:int=2,*,v:Vector[int]=BASE)->int:return x+y+len(v)\n')
        self.policy('exports')
        output,_=self.build()
        self.run_artifact(output,'''import inspect,core
from pyalamode_exports.core import outer
assert inspect.signature(outer)==inspect.signature(core.outer)
assert outer.__kwdefaults__['v'] is core.BASE
assert outer()==4
assert outer(3,y=4)==8
for invoke in (lambda:outer(x=3),lambda:outer(1,2,3),lambda:outer(1,y=2,unknown=1)):
    try:invoke()
    except TypeError:pass
    else:raise AssertionError('Python signature was changed')
''')

    def test_debug_data_assertions_coverage_internal_cost_and_source_semantics(self):
        self.source.write_text('from pyalamode import fun\nimport pyalamode as _pyalamode_guard_validate\n@fun\ndef inner(x:int)->int:\n    y=x+1\n    return y\n@fun\ndef outer(x:int)->int:return inner(x)+1\n')
        self.policy('debug')
        output,result=self.build()
        self.assertNotEqual((output/'core.py').read_bytes(),self.source.read_bytes())
        self.assertEqual(len(result.debug_coverage),2)
        self.run_artifact(output,'''import sys,core,pyalamode.boundaries as boundary
from pyalamode_exports.core import outer
events=[]
def profile(frame,event,arg):
    if event=='call' and frame.f_code is boundary.validate_data.__code__:events.append(1)
sys.setprofile(profile)
assert outer(2)==4
sys.setprofile(None)
assert len(events)==7,events
try:core.outer(True)
except TypeError:pass
else:raise AssertionError('debug did not validate parameter')
''')

    def test_debug_own_records_script_runs_once_without_self_import(self):
        self.source.write_text('from pyalamode import record,fun\nprint("init")\n@record\nclass P:\n    x:int\n@fun\ndef outer(p:P)->int:return p.x\nif __name__=="__main__":\n    print(outer(P(3)))\n')
        self.policy('debug')
        output,_=self.build()
        result=subprocess.run([sys.executable,str(output/'core.py')],env={**os.environ,'PYTHONPATH':str(Path(__file__).resolve().parents[1])},capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout,'init\n3\n')

    def test_debug_cross_module_future_annotations_keep_import_order(self):
        self.source.write_text('from __future__ import annotations\nfrom pyalamode import record,fun\n@record\nclass A:\n    x:int\nimport other\n@fun\ndef outer(p:other.B)->int:return p.x\n')
        (self.root/'other.py').write_text('from __future__ import annotations\nfrom pyalamode import record,fun\nimport core\n@record\nclass B:\n    x:int\n@fun\ndef f(p:core.A)->int:return p.x\n')
        self.policy('debug')
        output,_=self.build()
        self.run_artifact(output,'import core,other\nassert core.outer(other.B(2))==2\nassert other.f(core.A(3))==3\n')

    def test_unknown_duplicate_conflicting_callable_and_ambiguous_exports_fail(self):
        for mode,exports in [('off',['core:outer']),('exports',[]),('exports',['core:outer','core:outer']),
                             ('exports',['missing:outer']),('exports',['core:outre']),('exports',['core:inner.local'])]:
            with self.subTest(mode=mode,exports=exports):
                self.policy(mode,exports)
                output=self.root/'invalid'
                result=build_paths([self.root],root=self.root,output=output)
                self.assertEqual(result.status,2)
                self.assertFalse(output.exists())
        self.source.write_text('from pyalamode import fun\nfrom typing import Callable\n@fun\ndef outer(x:Callable[[int],int])->int:return x(1)\n')
        self.policy('exports')
        result=build_paths([self.root],root=self.root,output=self.root/'callback')
        self.assertEqual(result.status,2)
        self.assertTrue(any('Callable' in d.reason for d in result.tooling))
        self.source.write_text('from pyalamode import fun\n@fun\ndef outer(x:int)->int:return x\n')
        (self.root/'pyalamode_exports.py').write_text('VALUE=1\n')
        self.assertEqual(check_paths([self.root],root=self.root).status,2)
        (self.root/'pyalamode_exports.py').unlink()
        (self.root/'core').mkdir()
        (self.root/'core'/'__init__.py').write_text('from pyalamode import fun\n@fun\ndef outer(x:int)->int:return x\n')
        self.assertEqual(check_paths([self.root],root=self.root).status,2)

    def test_cache_records_runtime_guard_policy_and_writer_freshness(self):
        self.source.write_text(PREFIX+POINT+'@fun\ndef outer(p:Point)->Point:return replace(p,x=2)\n')
        cold=check_paths([self.root],root=self.root)
        self.assertEqual(cold.status,0)
        warm=check_paths([self.root],root=self.root)
        self.assertTrue(warm.results[0].cache_hit)
        self.assertEqual(warm.results[0].records,cold.results[0].records)
        for artifact in ['records.py','boundaries.py','guardgen.py']:
            with patch('pyalamode.checker.foundation_identities',return_value={**foundation_identities(),artifact:'changed'}):
                self.assertFalse(check_paths([self.root],root=self.root).results[0].cache_hit)
        self.policy('exports')
        self.assertFalse(check_paths([self.root],root=self.root).results[0].cache_hit)
        (self.root/'writer.py').write_text('from core import Point\nfrom builtins import setattr as put\nput(Point,"__eq__",print)\n')
        cached=check_paths([self.root],root=self.root)
        fresh=check_paths([self.root],root=self.root,cache=False)
        self.assertEqual(cached.status,1)
        self.assertEqual(fresh.status,1)
        self.assertTrue(any('record behavior' in identity for file in cached.results for identity in file.binding_context))

    def test_bad_source_guard_generation_and_changed_runtime_are_atomic(self):
        sentinel=self.root/'sentinel'
        self.source.write_text(PREFIX+f'open({str(sentinel)!r},"w").write("ran")\n'+POINT+'@fun\ndef outer(p:Point)->Point:return replace(p,tags=[1])\n')
        self.policy('exports')
        result=build_paths([self.root],root=self.root,output=self.root/'invalid')
        self.assertEqual(result.status,1)
        self.assertFalse(sentinel.exists())
        self.assertFalse((self.root/'invalid').exists())
        self.source.write_text('from pyalamode import fun\n@fun\ndef outer(x:int)->int:return x\n')
        for failure in [SyntaxError('generated failure'),TypeError('generated failure'),StopIteration('generated failure')]:
            with patch('pyalamode.guardgen.generate_facades',side_effect=failure):
                result=build_paths([self.root],root=self.root,output=self.root/'generation')
                self.assertEqual(result.status,2)
                self.assertFalse((self.root/'generation').exists())
        self.assertFalse(list(self.root.glob('.pyalamode-build-*')))


if __name__=='__main__':
    unittest.main()
