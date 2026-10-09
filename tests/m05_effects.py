"""Finite static effects, capability lending, freshness and ordinary artifact gates."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from pyalamode.checker import EFFECT_FOUNDATIONS, analyze_source, analyze_sources
from pyalamode.model import foundation_identities
from pyalamode.project import build_paths, check_paths

PREFIX = 'from pyalamode import fun,effects,Effectful,IO,State,Clock,Random,Environment,IOCapability,StateCapability,ClockCapability,RandomCapability,EnvironmentCapability,borrow,Vector,record,recorded_clock,recorded_io,live_io,state\n'
READER = '@effects(Clock)\ndef read(c:ClockCapability)->int:return c.now_ns()\n'


class EffectsStatic(unittest.TestCase):
    def good(self, source, policy=None):
        result = analyze_source(source, 'sample.py', policy=policy)
        self.assertTrue(result.verified, '\n'.join(d.format() for d in result.diagnostics))
        return result

    def bad(self, source, rule=None):
        result = analyze_source(source, 'sample.py')
        self.assertFalse(result.verified, source)
        if rule:
            self.assertIn(rule, {d.rule for d in result.diagnostics})
        return result

    def test_A17_all_families_operations_and_independent_evidence(self):
        source = PREFIX + '''@effects(IO,State,Clock,Random,Environment)
@fun
def shell(io:IOCapability,s:StateCapability,c:ClockCapability,r:RandomCapability,e:EnvironmentCapability)->tuple[str,int]:
    content=io.read_text("input.txt")
    io.write_text("output.txt",content)
    value=s.get()
    s.set(value+1)
    stamp=c.now_ns()
    random=r.below(10)
    name=e.get("NAME","")
    return (name,stamp+random)
'''
        result=self.good(source)
        contract=result.contracts[0]
        self.assertEqual(contract.effect_bound,['Clock','Environment','IO','Random','State'])
        self.assertEqual(contract.required_effects,contract.effect_bound)
        self.assertIn('IOCapability.write_text',contract.operations)
        self.assertEqual(contract.initialization if hasattr(contract,'initialization') else result.initialization_evidence,'unchecked ordinary module initialization')
        self.assertIn('OSError',contract.failures)
        self.assertIn('IndexError',contract.failures)
        self.assertEqual(contract.definition_failures,[])
        self.assertTrue(any('effects-v1' in trust for trust in contract.trust))
        self.assertIn('full interface',contract.capability_parameters['io']['permissions'])

    def test_effects_declaration_identity_aliases_and_invalid_shapes(self):
        self.good('from pyalamode import effects as mark,Clock,ClockCapability\n@mark(Clock)\ndef f(c:ClockCapability)->int:return c.now_ns()\n')
        self.good('import pyalamode as p\n@p.effects(p.Clock)\ndef f(c:p.ClockCapability)->int:return c.now_ns()\n')
        self.good('from pyalamode import effects,Clock\nmark=effects\n@mark(Clock)\ndef f()->int:return 1\n')
        for declaration in ['@effects()', '@effects(Clock,Clock)', '@effects("Clock")', '@effects(unknown)', '@effects(Clock,key=Clock)', '@effects', '@effects(Clock)\n@effects(Clock)']:
            self.bad(PREFIX+declaration+'\ndef f()->int:return 1\n','PAL120')
        self.bad(PREFIX+'@effects(Task)\ndef f()->int:return 1\n','PAL120')
        self.bad('@effects(Clock)\ndef f()->int:return 1\n'+PREFIX,'PAL120')

    def test_pure_to_effectful_transitive_recursive_and_alias_refusals(self):
        self.bad(PREFIX+READER+'@fun\ndef f(c:ClockCapability)->int:return read(c)\n','PAL310')
        self.bad(PREFIX+'@effects(Clock)\ndef declared()->int:return 1\n@fun\ndef pure()->int:return declared()\n','PAL310')
        result=self.good(PREFIX+READER+'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    alias=read\n    return alias(c)\n')
        self.assertEqual(result.contracts[-1].required_effects,['Clock'])
        self.good(PREFIX+'@effects(Clock)\ndef a(c:ClockCapability,n:int)->int:\n    if n==0:return c.now_ns()\n    return b(c,n-1)\n@effects(Clock)\ndef b(c:ClockCapability,n:int)->int:return a(c,n)\n')

    def test_A18_explicit_higher_order_capability_slot_and_conditional_evidence(self):
        source=PREFIX+READER+'''@effects(Clock)
def apply(cb:Effectful[[ClockCapability],int,Clock],c:ClockCapability)->int:return cb(c)
@effects(Clock)
def outer(c:ClockCapability)->int:return apply(read,c)
'''
        result=self.good(source)
        apply=next(c for c in result.contracts if c.name=='apply')
        self.assertEqual(apply.required_effects,['Clock'])
        self.assertIn('IndexError',apply.failures)
        self.bad(PREFIX+READER+'from typing import Callable\n@fun\ndef apply(cb:Callable[[ClockCapability],int])->int:return 1\n','PAL130')
        self.bad(PREFIX+'@effects(Clock)\ndef f(cb:Effectful[[StateCapability],int,Clock])->int:return 1\n','PAL130')
        self.bad(source.replace('@effects(Clock)\ndef outer','@effects(State)\ndef outer'),'PAL310')
        mixed=PREFIX+'''@effects(Clock)
def clock(x:int)->int:return x
@effects(State)
def stateful(x:int)->int:return x
@effects(Clock,State)
def invoke(cb:Effectful[[int],int,Clock],flag:bool,x:int)->int:
    chosen=cb if flag else stateful
    return chosen(x)
'''
        contract=self.good(mixed).contracts[-1]
        self.assertEqual(contract.required_effects,['Clock','State'])
        self.assertIn('OSError',contract.failures)
        self.bad(mixed.replace('@effects(Clock,State)','@effects(Clock)'),'PAL310')

    def test_vector_callback_unions_without_capability_capture(self):
        source=PREFIX+'@effects(Clock)\ndef cb(x:int)->int:return x+1\n@effects(Clock)\ndef map_values(v:Vector[int])->Vector[int]:return v.map(cb)\n'
        self.good(source)
        self.bad(source.replace('@effects(Clock)\ndef map_values','@fun\ndef map_values'),'PAL221')
        self.good(PREFIX+'@effects(State)\ndef pred(x:int)->bool:return x>0\n@effects(State)\ndef acc(a:int,x:int)->int:return a+x\n@effects(State)\ndef f(v:Vector[int])->int:\n    selected=v.filter(pred)\n    return selected.fold(acc,0)\n')
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability,v:Vector[int])->Vector[int]:\n    @effects(Clock)\n    def cb(x:int)->int:return c.now_ns()+x\n    return v.map(cb)\n','PAL320')

    def test_capabilities_cannot_be_data_aliases_defaults_captures_or_returns(self):
        for body in ['alias=c\n    return 1','x=(c,)\n    return 1','x=Vector.of(c)\n    return 1','return c','return c if True else c']:
            self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    '+body+'\n')
        self.bad(PREFIX+'@record\nclass Bad:\n    c:ClockCapability\n','PAL130')
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability=recorded_clock((1,)))->int:return c.now_ns()\n','PAL320')
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability)->ClockCapability:return c\n','PAL320')
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability)->Effectful[[],int,Clock]:\n    @effects(Clock)\n    def nested()->int:return c.now_ns()\n    return nested\n','PAL320')
        self.bad(PREFIX+'C=recorded_clock((1,))\n@effects(Clock)\ndef f()->int:return C.now_ns()\n')

    def test_borrow_region_nested_return_expired_and_unknown_contexts(self):
        source=PREFIX+READER+'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    with borrow(c) as first:\n        with borrow(first) as second:\n            return read(second)\n'
        result=self.good(source)
        self.assertEqual(len(result.contracts[-1].borrow_scopes),2)
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    with borrow(c) as b:\n        stamp=b.now_ns()\n    return b.now_ns()\n','PAL102')
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    with borrow(c) as c:return 1\n','PAL101')
        for context in ['c','unknown(c)','reading(c,"file")']:
            self.bad(PREFIX+f'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    with {context} as b:return 1\n','PAL320')

    def test_unknown_implicit_dispatch_remains_refused_with_all_effects(self):
        for expr in ['open("x")','c.unknown()','c.now_ns(x=1)','c+1','not c','c==c','str(c)','hash(c)','f"{c}"','c.__class__','c.now_ns','c[0]']:
            self.bad(PREFIX+f'@effects(IO,State,Clock,Random,Environment)\ndef f(c:ClockCapability)->int:\n    x={expr}\n    return 1\n')
        self.bad(PREFIX+'@effects(IO)\ndef f(io:IOCapability)->int:\n    print(1)\n    return 1\n','PAL230')

    def test_factory_callers_permissions_and_closed_aliases(self):
        self.good(PREFIX+READER+'c=recorded_clock((1,2))\nanswer=read(c)\n')
        self.bad(PREFIX+READER+'def shell(c:ClockCapability):return read(c)\n','PAL221')
        for close in ['c.close()','alias=c\nalias.close()','unknown(c)','c.some_operation()']:
            self.bad(PREFIX+READER+'c=recorded_clock((1,2))\n'+close+'\nanswer=read(c)\n','PAL221')
        io=PREFIX+'@effects(IO)\ndef writer(io:IOCapability)->None:io.write_text("x","y")\n'
        self.good(io+'cap=recorded_io((),allowed_ops=("write_text","read_text"))\nwriter(cap)\n')
        for factory in ['recorded_io(())','recorded_io((),allowed_ops=("read_text",))','recorded_io((),allowed_ops=("read_text","read_text"))','live_io("/tmp")']:
            self.bad(io+f'cap={factory}\nwriter(cap)\n','PAL221')

    def test_effects_module_initialization_remains_distinct(self):
        self.good('# mode: fun\n'+PREFIX+READER)
        self.bad('# mode: fun\n'+PREFIX+'C=recorded_clock((1,))\n'+READER,'PAL230')
        self.bad(PREFIX+'@effects(Clock)\ndef f(c:ClockCapability)->int:\n    other=recorded_clock((1,))\n    return 1\n','PAL230')

    def test_foundation_interface_and_helper_writer_routes_fail(self):
        for writer in ['ClockCapability.now_ns=print','alias=ClockCapability\nalias.now_ns=print','setattr(ClockCapability,"now_ns",print)','import pyalamode.effects as backend\nbackend._lease=print', 'from pyalamode.effects import _Borrow as manager\nmanager.__enter__.__code__=print.__code__']:
            self.bad(PREFIX+writer+'\n'+READER)
        self.bad(PREFIX+'from pyalamode.effects import _Borrow as manager\ndef replacement(self):return self._capability\nmanager.__enter__.__code__=replacement.__code__\n'+READER)
        for module,names in EFFECT_FOUNDATIONS.items():
            for name in names:
                with self.subTest(module=module,name=name):
                    self.bad(PREFIX+f'import {module} as backend\nbackend.{name}=print\n'+READER)


class EffectsBuild(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.source=self.root/'core.py'
        self.source.write_text(PREFIX+READER+'@effects(Clock)\ndef apply(cb:Effectful[[ClockCapability],int,Clock],c:ClockCapability)->int:return cb(c)\n@effects(Clock)\ndef outer(c:ClockCapability)->int:return apply(read,c)\n')
    def tearDown(self):self.temp.cleanup()
    def policy(self,text): (self.root/'pyproject.toml').write_text('[tool.pyalamode]\n'+text)

    def test_build_normal_python_identity_and_fake_provider_retains_effect(self):
        output=self.root/'artifact';result=build_paths([self.source],root=self.root,output=output)
        self.assertEqual(result.status,0,[d.format() for r in result.results for d in r.diagnostics])
        self.assertEqual((output/'core.py').read_bytes(),self.source.read_bytes())
        report=json.loads((output/'pyalamode-build.json').read_text()) if (output/'pyalamode-build.json').exists() else result.to_dict()
        self.assertIn('effects.py',report['product_artifacts'])
        run=subprocess.run([sys.executable,'-c','import core\nfrom pyalamode import effects,Clock,fun,recorded_clock\nassert effects(Clock)(core.read) is core.read\nassert fun(core.read) is core.read\nassert core.outer(recorded_clock((123,)))==123\n'],cwd=output,env={**os.environ,'PYTHONPATH':str(output)+os.pathsep+str(Path(__file__).resolve().parents[1])},capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(next(c for c in result.results[0].contracts if c.name=='outer').effect_bound,['Clock'])

    def test_policy_bound_selectors_weakening_and_malformed_values(self):
        self.policy('[tool.pyalamode.effect_bounds]\n"core:outer"=["Clock"]\n')
        self.assertEqual(check_paths([self.source],root=self.root,cache=False).status,0)
        self.policy('[tool.pyalamode.effect_bounds]\n"core:outer"=[]\n')
        self.assertEqual(check_paths([self.source],root=self.root,cache=False).status,1)
        for text in ['effect_bounds=[]','[tool.pyalamode.effect_bounds]\n"core:missing"=["Clock"]','[tool.pyalamode.effect_bounds]\n"core:outer"=["Task"]','[tool.pyalamode.effect_bounds]\n"core:outer"=["Clock","Clock"]']:
            self.policy(text+'\n');output=self.root/'bad'
            self.assertEqual(build_paths([self.source],root=self.root,output=output).status,2)
            self.assertFalse(output.exists())

    def test_warm_effects_callable_and_runtime_byte_freshness(self):
        cold=check_paths([self.source],root=self.root)
        self.assertEqual(cold.status,0)
        warm=check_paths([self.source],root=self.root)
        self.assertTrue(warm.results[0].cache_hit)
        self.assertEqual(cold.results[0].contracts,warm.results[0].contracts)
        with patch('pyalamode.checker.foundation_identities',return_value={**foundation_identities(),'effects.py':'changed'}):
            self.assertFalse(check_paths([self.source],root=self.root).results[0].cache_hit)
        self.source.write_text(self.source.read_text().replace('return c.now_ns()','return 5'))
        changed=check_paths([self.source],root=self.root)
        self.assertFalse(changed.results[0].cache_hit)
        self.assertEqual(next(c for c in changed.results[0].contracts if c.name=='outer').required_effects,['Clock'])

    def test_partial_warm_returned_callable_evidence_preserves_tighter_bounds(self):
        library=self.root/'library.py'
        library.write_text('# mode: fun\n'+PREFIX+READER+'def factory()->Effectful[[ClockCapability],int,Clock,State]:return read\n')
        self.source.write_text('# mode: fun\n'+PREFIX+'from library import factory\n@effects(Clock)\ndef outer(c:ClockCapability)->int:return factory()(c)+1\n')
        cold=check_paths([self.source],root=self.root)
        self.assertEqual(cold.status,0)
        self.source.write_text(self.source.read_text().replace('+1','+2'))
        partial=check_paths([self.source],root=self.root)
        fresh=check_paths([self.source],root=self.root,cache=False)
        self.assertEqual(partial.status,0)
        self.assertTrue(next(r for r in partial.results if r.path==str(library.resolve())).cache_hit)
        outer=next(c for r in partial.results for c in r.contracts if c.name=='outer')
        expected=next(c for r in fresh.results for c in r.contracts if c.name=='outer')
        self.assertEqual(outer,expected)
        self.assertEqual(outer.required_effects,['Clock'])
        factory=next(c for r in partial.results for c in r.contracts if c.name=='factory')
        self.assertEqual(factory.return_callable_evidence['effect_bound'],['Clock'])
        self.assertFalse(factory.return_callable_evidence['conditional'])
        self.assertTrue(any(target.endswith('::read') for target in factory.callable_dependencies))

    def test_conditional_return_capture_warm_evidence_and_uninvoked_bound(self):
        self.source.write_text(PREFIX+'@effects(Clock)\ndef clock(x:int)->int:return x\n@effects(State)\ndef stateful(x:int)->int:return x\n@fun\ndef factory(cb:Effectful[[int],int,Clock],flag:bool)->Effectful[[int],int,Clock,State]:\n    chosen=cb if flag else stateful\n    @effects(Clock,State)\n    def nested(x:int)->int:return chosen(x)\n    return nested\n')
        cold=check_paths([self.source],root=self.root)
        self.assertEqual(cold.status,0,[d.format() for r in cold.results for d in r.diagnostics])
        warm=check_paths([self.source],root=self.root)
        self.assertEqual(cold.results[0].contracts,warm.results[0].contracts)
        nested=next(c for c in warm.results[0].contracts if c.name=='factory.nested')
        evidence=nested.callable_capture_evidence['chosen']
        self.assertTrue(evidence['conditional'])
        self.assertEqual(evidence['effect_bound'],['Clock','State'])
        self.assertIn('RuntimeError',nested.failures)
        factory=next(c for c in warm.results[0].contracts if c.name=='factory')
        self.assertEqual(factory.required_effects,[])
        self.assertEqual(factory.behavior,'pure')

    def test_caps_callback_guard_refusal_debug_data_only_and_atomic_failure(self):
        self.policy('boundary_guards="exports"\nguarded_exports=["core:outer"]\n')
        result=build_paths([self.source],root=self.root,output=self.root/'guarded')
        self.assertEqual(result.status,2)
        self.assertFalse((self.root/'guarded').exists())
        self.policy('boundary_guards="debug"\n')
        result=build_paths([self.source],root=self.root,output=self.root/'debug')
        self.assertEqual(result.status,0)
        self.assertTrue(all(not item['parameters'] for item in result.debug_coverage))
        sentinel=self.root/'sentinel'
        self.source.write_text(PREFIX+f'open({str(sentinel)!r},"w").write("executed")\n@effects(Clock)\ndef f()->int:return unknown()\n')
        result=build_paths([self.source],root=self.root,output=self.root/'invalid')
        self.assertEqual(result.status,1)
        self.assertFalse(sentinel.exists());self.assertFalse((self.root/'invalid').exists())

    def test_cross_module_effect_graph_and_writer_warm_freshness(self):
        (self.root/'reader.py').write_text('# mode: fun\n'+PREFIX+READER)
        self.source.write_text('# mode: fun\n'+PREFIX+'from reader import read\n@effects(Clock)\ndef outer(c:ClockCapability)->int:return read(c)\n')
        self.assertEqual(check_paths([self.source],root=self.root).status,0)
        self.assertTrue(all(r.cache_hit for r in check_paths([self.source],root=self.root).results))
        writer=self.root/'writer.py';writer.write_text('import time\ntime.time_ns=print\n')
        warm=check_paths([self.source,writer],root=self.root)
        fresh=check_paths([self.source,writer],root=self.root,cache=False)
        self.assertEqual(warm.status,1);self.assertEqual(fresh.status,1)
        self.assertTrue(any('effect dependency' in identity for file in warm.results for identity in file.binding_context))


if __name__=='__main__':unittest.main()
