"""Development controls for actual wheels and current consumer static evidence."""
import copy
import hashlib
import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from pyalamode.project import build_paths,check_paths,check_snapshot,load_policy
from pyalamode import distribution as d, migration as m
from pyalamode.migration_views import capture_state,inventory,observe

POLICY='[tool.pyalamode.distribution]\nschema=1\nname="checked-pricing"\nversion="1.0.0"\npackages=["checked_pricing"]\nexports=["checked_pricing.core:quote"]\n'
CONSUMER='[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="checked-pricing"\nversion="1.0.0"\npackages=["checked_pricing"]\n'
class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name).resolve();self.producer=self.base/'producer';self.site=self.base/'site';self.consumer=self.base/'consumer'
        for p in (self.producer,self.site,self.consumer):p.mkdir()
        (self.producer/'checked_pricing').mkdir();(self.producer/'checked_pricing/__init__.py').write_text('# mode: fun\n')
        (self.producer/'checked_pricing/core.py').write_text('from pyalamode import fun\n@fun\ndef quote(value:int)->int:\n    return value+2\n')
        (self.producer/'pyproject.toml').write_text(POLICY)
        (self.consumer/'pyproject.toml').write_text(CONSUMER)
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import quote\n@fun\ndef total(value:int)->int:\n    return quote(value)\n')
        self.paths=patch.object(sys,'path',[str(self.site),*sys.path]);self.paths.start()
    def tearDown(self):self.paths.stop();self.temp.cleanup()
    def wheel(self,mode='off'):
        if mode!='off':(self.producer/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="'+mode+'"\nguarded_exports=["checked_pricing.core:quote"]\n'+POLICY)
        out=self.base/'out'/d.wheel_paths({'name':'checked-pricing','version':'1.0.0'})[0]
        r=build_paths([self.producer],root=self.producer,artifact='wheel',output=out)
        self.assertEqual(r.status,0,[x.reason for x in r.tooling]);self.assertTrue(out.is_file())
        with zipfile.ZipFile(out)as z:z.extractall(self.site)
        return out
    def check(self,**kwargs):return check_paths([self.consumer],root=self.consumer,cache=False,**kwargs)
    def test_wheel_separate_consumer_build_and_owned_capture(self):
        self.wheel();r=self.check();self.assertEqual(r.status,0,r.to_dict());self.assertTrue(r.checked_dependencies[0]['verified']);self.assertEqual(len(r.results),1)
        built=build_paths([self.consumer],root=self.consumer,output=self.base/'built');self.assertEqual(built.status,0,built.to_dict())
        snap,state,report,_=observe(self.consumer);self.assertEqual(state['schema'],4);self.assertEqual(state['coverage']['eligible_modules'],1);self.assertEqual(state['coverage']['eligible_functions'],1);self.assertEqual(report['status'],0)
    def test_missing_used_complete_semantic_and_recordable(self):
        r=self.check();self.assertEqual(r.status,1);self.assertIn('PAL370',[x.rule for f in r.results for x in f.diagnostics]);self.assertTrue(r.checked_dependencies[0]['complete'])
        self.assertEqual(next(x for f in r.results for x in f.diagnostics if x.rule=='PAL370').dependency_context['reason_code'],'missing-distribution')
        snap,state,report,_=observe(self.consumer,bootstrap=True);self.assertEqual(state['strict_status'],1);self.assertEqual(state['current_dependency_status'],1);self.assertTrue(any(f['context']['kind']=='checked-dependency'for f in state['findings']))
        receipt=m.write_baseline(self.consumer,state,owner='team',rationale='reviewed dependency refusal',prepublish=lambda:None);self.assertEqual(receipt['status'],0);self.assertFalse(receipt['verified']);self.assertEqual(receipt['state_strict_status'],1)
        self.wheel();(self.site/'checked_pricing-1.0.0.dist-info/pyalamode/evidence.json').unlink()
        r=self.check();self.assertEqual(r.status,1);self.assertTrue(r.checked_dependencies[0]['complete']);self.assertEqual(next(x for f in r.results for x in f.diagnostics if x.rule=='PAL370').dependency_context['reason_code'],'missing-evidence')
        self.assertEqual(self.check(audit=True).status,0)
    def test_unused_missing_has_event_no_fabricated_finding(self):
        (self.consumer/'use.py').write_text('from pyalamode import fun\n@fun\ndef total(value:int)->int:\n    return value\n')
        _,state,report,_=observe(self.consumer,bootstrap=True);self.assertEqual(state['strict_status'],1);self.assertEqual(state['findings'],[]);self.assertEqual(state['current_dependency_events'][0]['required_by'],[]);self.assertEqual(state['coverage']['eligible_functions'],1)
    def test_stale_installed_source_preserves_source_axis(self):
        self.wheel();(self.site/'checked_pricing/core.py').write_text('from pyalamode import fun\n@fun\ndef quote(value:int)->int:\n    return value+3\n')
        r=self.check();self.assertEqual(r.status,1);self.assertEqual(r.checked_dependencies[0]['admission'],'stale');self.assertIsNone(r.checked_dependencies[0]['source_status'])
        _,state,_,_=observe(self.consumer,bootstrap=True);self.assertEqual(state['strict_status'],1);self.assertEqual(state['coverage']['eligible_modules'],1)
        out=self.base/'refused';r=build_paths([self.consumer],root=self.consumer,output=out);self.assertEqual(r.status,1);self.assertFalse(out.exists())
    def test_unrelated_metadata_not_read_and_relevant_symlink_refuses(self):
        self.wheel();unrelated=self.site/'other-1.0.0.dist-info';unrelated.mkdir();(unrelated/'METADATA').write_text('Classifier: one\nClassifier: two\n')
        self.assertEqual(self.check().status,0)
        owner=self.site/'checked_pricing-1.0.0.dist-info';saved=owner/'saved';(owner/'pyalamode').rename(saved);(owner/'pyalamode').symlink_to(saved,target_is_directory=True)
        r=self.check();self.assertEqual(r.status,2);self.assertFalse(r.results)
    def test_guard_exports_and_debug_regenerate(self):
        for mode in ('exports','debug'):
            with self.subTest(mode=mode):
                if (self.base/'out').exists():shutil.rmtree(self.base/'out')
                for p in self.site.iterdir():shutil.rmtree(p)
                self.wheel(mode);r=self.check();self.assertEqual(r.status,0,r.to_dict())
                facade=self.site/'checked_pricing/_pyalamode_exports/core.py';facade.write_text(facade.read_text()+'\n# changed\n');self.assertEqual(self.check().status,1)
    def test_missing_claimed_facade_and_extra_sources_preserve_receipts_and_layout(self):
        wheel=self.wheel('exports');info=self.site/'checked_pricing-1.0.0.dist-info'
        with zipfile.ZipFile(wheel)as z:evidence=json.loads(z.read(info.name+'/pyalamode/evidence.json'))['payload']
        name=evidence['guards']['exports'][0]['public_boundary'].split(':')[0].replace('.','/')+'.py';facade=self.site/name
        self.assertIn(name,evidence['guards']['generated_files']);self.assertEqual(evidence['artifacts'][name]['role'],'generated')
        current=self.check();self.assertEqual(current.status,0,current.to_dict());before=current.checked_dependencies[0];original=facade.read_bytes()
        def no_artifact(label,status):
            out=self.base/label;r=build_paths([self.consumer],root=self.consumer,output=out)
            self.assertEqual(r.status,status,r.to_dict());self.assertFalse(out.exists());self.assertIsNone(r.output)
            return r
        facade.unlink()
        try:
            r=self.check();self.assertEqual(r.status,1,r.to_dict());self.assertEqual(r.tooling,[])
            findings=[x for f in r.results for x in f.diagnostics];self.assertEqual([x.rule for x in findings],['PAL370'])
            self.assertEqual(findings[0].path,str(self.consumer/'use.py'));self.assertEqual(findings[0].dependency_context['reason_code'],'stale-artifact');self.assertEqual(findings[0].dependency_context['site'],'import')
            row=r.checked_dependencies[0];self.assertEqual(row['admission'],'stale');self.assertEqual(row['input_status'],1);self.assertIsNone(row['source_status']);self.assertFalse(row['verified']);self.assertTrue(row['complete']);self.assertEqual(row['exports'],[])
            self.assertEqual(row['observed']['artifacts'][name],{'path':str(facade),'exists':False,'sha256':None,'size':None})
            for key in ('metadata','evidence','policy'):self.assertEqual(row['observed'][key],before['observed'][key])
            audit=self.check(audit=True);self.assertEqual(audit.status,0);self.assertFalse(audit.verified)
            built=no_artifact('missing-facade',1);self.assertEqual([x.rule for f in built.results for x in f.diagnostics],['PAL370'])
        finally:facade.write_bytes(original)
        self.assertEqual(facade.read_bytes(),original);self.assertEqual(self.check().status,0)
        extra=facade.parent/'invented.py';record=info/'RECORD';record_before=record.read_bytes();extra.write_bytes(b'raise AssertionError("unclaimed application executed")\n')
        try:
            for updated in (False,True):
                if updated:self.rewrite_record()
                r=self.check();self.assertEqual(r.status,2,r.to_dict());self.assertEqual([x.rule for x in r.tooling],['PAL001'])
                self.assertIn('unknown RECORD ownership row' if updated else 'unrecorded installed source',r.tooling[0].reason)
                policy,error=load_policy(self.consumer);self.assertIsNone(error);snapshot=d.distribution_snapshot(policy,self.consumer);row=snapshot['receipts']['checked-pricing']
                self.assertEqual(row['admission'],'tooling');self.assertEqual(row['input_status'],2);self.assertIsNone(row['source_status']);self.assertFalse(row['verified']);self.assertFalse(row['complete']);self.assertEqual(row['exports'],[])
                no_artifact('extra-source-'+str(updated),2)
        finally:extra.unlink();record.write_bytes(record_before)
        self.assertEqual(record.read_bytes(),record_before);self.assertEqual(self.check().status,0)
        parent_init=facade.parent/'__init__.py';parent_bytes=parent_init.read_bytes();parent_init.unlink()
        try:self.assertEqual(self.check().status,2);no_artifact('missing-parent-init',2)
        finally:parent_init.write_bytes(parent_bytes)
        self.assertEqual(self.check().status,0)
        saved=self.base/'saved-generated-package';facade.parent.rename(saved)
        try:self.assertEqual(self.check().status,2);no_artifact('missing-parent-directory',2)
        finally:saved.rename(facade.parent)
        self.assertEqual(self.check().status,0);self.assertEqual(facade.read_bytes(),original)
    def test_nested_malformed_exact_json_types_refuse(self):
        self.wheel();ep=self.site/'checked_pricing-1.0.0.dist-info/pyalamode/evidence.json';original=json.loads(ep.read_text())
        for mutate in (lambda p:p['exports'][0]['contract'].__setitem__('returns','tuple[unknown]'),lambda p:p['exports'][0]['contract'].__setitem__('parameters',[]),lambda p:p['modules'][0]['initialization'].__setitem__('effects',{}),lambda p:p['producer']['product_artifacts'].__setitem__('arbitrary.py','0'*64),lambda p:p['guards'].__setitem__('exports',{})):
            v=copy.deepcopy(original);mutate(v['payload']);v['sha256']=d.digest(v['payload']);ep.write_bytes(d.canonical(v));self.assertEqual(self.check().status,2)
        ep.write_bytes(d.canonical(original))
    def test_late_installed_change_no_artifact(self):
        self.wheel();original=d.build_wheel
        # Tree publication's callback sees the installed write after the genuine check.
        from pyalamode import project
        actual=project.check_paths
        def changed(*args,**kwargs):
            result=actual(*args,**kwargs);(self.site/'checked_pricing/core.py').write_text('from pyalamode import fun\n@fun\ndef quote(value:int)->int:\n    return value+9\n');return result
        out=self.base/'late'
        with patch.object(project,'check_paths',changed):r=build_paths([self.consumer],root=self.consumer,output=out)
        self.assertEqual(r.status,1,r.to_dict());self.assertIn('PAL372',[x.rule for f in r.results for x in f.diagnostics]);self.assertFalse(out.exists())
    def test_bytecode_raw_comparison_and_absence(self):
        import importlib.util,marshal,py_compile
        (self.producer/'checked_pricing/cache_shape.py').write_text('"""Compiler-only ordinary sibling."""\nassert False\nraise AssertionError("source evaluated")\n')
        self.wheel();source=self.site/'checked_pricing/core.py';py_compile.compile(str(source),doraise=True);self.assertEqual(self.check().status,0)
        cache=next(source.parent.glob('__pycache__/core.*.pyc'));old=cache.read_bytes();cache.write_bytes(old[:-1]+b'x');self.assertEqual(self.check().status,2);cache.write_bytes(old)
        sources=[source,source.parent/'__init__.py',source.parent/'cache_shape.py'];artifacts={p.relative_to(self.site).as_posix():p.read_bytes()for p in sources}
        def payload(path,optimization,retained):
            raw=path.read_bytes()
            if not retained:return marshal.dumps(compile(raw,str(path),'exec',dont_inherit=True,optimize=optimization))
            code=compile(raw,str(path),'exec',dont_inherit=True,optimize=optimization)
            try:return marshal.dumps(code)
            finally:del code
        def header(path,flags):
            raw=path.read_bytes();suffix=importlib.util.source_hash(raw)if flags else (int(path.stat().st_mtime)&0xffffffff).to_bytes(4,'little')+(len(raw)&0xffffffff).to_bytes(4,'little')
            return importlib.util.MAGIC_NUMBER+flags.to_bytes(4,'little')+suffix
        for retained in (False,True):
            for flags in (0,1,3):
                expected={}
                for path in sources:
                    for optimization,suffix in ((0,''),(1,'.opt-1'),(2,'.opt-2')):
                        cache=path.parent/'__pycache__'/f'{path.stem}.cpython-313{suffix}.pyc';cache.parent.mkdir(exist_ok=True)
                        raw=header(path,flags)+payload(path,optimization,retained);cache.write_bytes(raw);expected[cache.relative_to(self.site).as_posix()]=hashlib.sha256(raw).hexdigest()
                with patch.object(marshal,'loads',side_effect=AssertionError('input unmarshalled'))as loads,patch.object(marshal,'load',side_effect=AssertionError('input unmarshalled'))as load:
                    receipts=d._pycs(self.site,artifacts)
                    self.assertFalse(loads.called);self.assertFalse(load.called)
                self.assertEqual({name:row['sha256']for name,row in receipts.items()},expected);self.assertEqual(self.check().status,0)
        for path in sources:
            for optimization in (0,1,2):py_compile.compile(str(path),doraise=True,optimize=optimization)
        self.assertEqual(self.check().status,0)
        cache=source.parent/'__pycache__/core.cpython-313.pyc';old=cache.read_bytes()
        for malformed in (b'bad!'+old[4:],old[:4]+b'\x02\x00\x00\x00'+old[8:],header(source,3)[:8]+b'\0'*8+old[16:],old[:-1]+b'x'):
            try:cache.write_bytes(malformed);self.assertEqual(self.check().status,2)
            finally:cache.write_bytes(old)
        option=source.parent/'cache_shape.py';cache=option.parent/'__pycache__/cache_shape.cpython-313.opt-1.pyc';old=cache.read_bytes()
        try:cache.write_bytes(header(option,3)+payload(option,0,False));self.assertEqual(self.check().status,2)
        finally:cache.write_bytes(old)
        shutil.rmtree(source.parent/'__pycache__');self.assertEqual(self.check().status,0)
    def test_late_valid_bytecode_changes_are_semantic_no_artifact(self):
        import importlib.util,marshal
        from pyalamode import project
        self.wheel();source=self.site/'checked_pricing/core.py';cache=source.parent/'__pycache__/core.cpython-313.pyc';original=project._distribution_prepublish
        for kind in ('temporary','retained','invalid'):
            phases=[]
            def changed(result,snapshot,policy,root,capture):
                self.assertEqual(result.status,0,result.to_dict());self.assertEqual(result.checked_dependencies[0]['input_status'],0);self.assertEqual(result.checked_dependencies[0]['source_status'],0);self.assertTrue(result.checked_dependencies[0]['verified']);phases.append('checked')
                raw=source.read_bytes();header=importlib.util.MAGIC_NUMBER+b'\x03\x00\x00\x00'+importlib.util.source_hash(raw)
                if kind=='retained':
                    code=compile(raw,str(source),'exec',dont_inherit=True,optimize=0)
                    try:payload=marshal.dumps(code)
                    finally:del code
                else:payload=marshal.dumps(compile(raw,str(source),'exec',dont_inherit=True,optimize=0))
                cache.parent.mkdir(exist_ok=True);cache.write_bytes(header+payload if kind!='invalid'else b'bad-cache')
                return original(result,snapshot,policy,root,capture)
            out=self.base/('late-cache-'+kind)
            try:
                with patch.object(project,'_distribution_prepublish',changed):r=build_paths([self.consumer],root=self.consumer,output=out)
                self.assertEqual(phases,['checked']);self.assertFalse(out.exists());self.assertIsNone(r.output)
                if kind=='invalid':self.assertEqual(r.status,2,r.to_dict());self.assertEqual([x.rule for x in r.tooling],['PAL001'])
                else:
                    self.assertEqual(r.status,1,r.to_dict());self.assertEqual(r.tooling,[])
                    self.assertEqual([x.rule for f in r.results for x in f.diagnostics],['PAL372']);self.assertEqual(next(x for f in r.results for x in f.diagnostics).dependency_context['reason_code'],'inputs-changed')
                    receipt=r.checked_dependencies[0];self.assertEqual(receipt['input_status'],1);self.assertIsNone(receipt['source_status']);self.assertFalse(receipt['verified']);self.assertTrue(receipt['complete'])
            finally:
                if cache.parent.exists():shutil.rmtree(cache.parent)
    def test_reproducible_fresh_outputs_and_prior_preservation(self):
        out=self.wheel();other=self.base/'out2'/out.name;r=build_paths([self.producer],root=self.producer,artifact='wheel',output=other);self.assertEqual(r.status,0,r.to_dict());self.assertEqual(out.read_bytes(),other.read_bytes())
        old=out.read_bytes();r=build_paths([self.producer],root=self.producer,artifact='wheel',output=out);self.assertEqual(r.status,2);self.assertEqual(out.read_bytes(),old)

    def test_nonalphabetical_signature_record_and_variant_order(self):
        source="""# mode: fun
from pyalamode import record, variant, case
@record
class Invoice:
    zulu: int
    alpha: str
@variant
class State:
    @case
    class Zulu:
        zulu: int
        alpha: str
    @case
    class Alpha:
        pass
def quote(zulu:int,alpha:int)->int:
    return zulu-alpha
"""
        (self.producer/'checked_pricing/core.py').write_text(source)
        policy=POLICY.replace('exports=["checked_pricing.core:quote"]','exports=["checked_pricing.core:quote","checked_pricing.core:Invoice","checked_pricing.core:State"]')
        (self.producer/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="exports"\nguarded_exports=["checked_pricing.core:quote"]\n'+policy)
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import quote\n@fun\ndef total(value:int)->int:\n    return quote(value,2)\n')
        self.wheel();r=self.check();self.assertEqual(r.status,0,[x.reason for x in r.tooling]);self.assertEqual(list(next(e['contract']['fields'] for e in r.checked_dependencies[0]['exports'] if e['kind']=='record')),['zulu','alpha'])
    def test_unpublished_function_has_no_source_admission(self):
        p=self.producer/'checked_pricing/core.py';p.write_text(p.read_text()+'\n@fun\ndef hidden(value:int)->int:\n    return value+4\n');self.wheel()
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import hidden\n@fun\ndef total(value:int)->int:\n    return hidden(value)\n')
        r=self.check();self.assertEqual(r.status,1);self.assertIn('PAL371',[x.rule for f in r.results for x in f.diagnostics])
    def test_application_backend_parent_default_and_annotation_never_execute(self):
        (self.producer/'checked_pricing/__init__.py').write_text('raise RuntimeError("must remain static")\n')
        (self.producer/'pyproject.toml').write_text('[build-system]\nrequires=[]\nbuild-backend="evil_backend"\n'+POLICY)
        (self.producer/'evil_backend.py').write_text('raise RuntimeError("backend must remain static")\n')
        out=self.wheel();self.assertTrue(out.exists());self.assertEqual(self.check().status,0)
    def test_source_writer_in_unexported_installed_module_refuses(self):
        (self.producer/'checked_pricing/writer.py').write_text('import builtins\nbuiltins.abs=lambda x:x\n')
        p=self.producer/'checked_pricing/core.py';p.write_text(p.read_text().replace('value+2','abs(value)'))
        out=self.base/'out'/d.wheel_paths({'name':'checked-pricing','version':'1.0.0'})[0];r=build_paths([self.producer],root=self.producer,artifact='wheel',output=out);self.assertEqual(r.status,1);self.assertFalse(out.exists())

    def test_direct_codec_warm_native_and_defining_globals_writer_closure(self):
        root=self.consumer
        (root/'pyproject.toml').unlink()
        (root/'use.py').write_text('from pyalamode import fun\nfrom pyalamode.encoding import value_encode\n@fun\ndef total(value:int)->bytes:\n    return value_encode(value,int)\n')
        for writer in ('import builtins\nbuiltins.ord=lambda x:1\n','from pyalamode.encoding import value_encode\nvalue_encode.__globals__["_MAX_WIRE_BYTES"]=4\n'):
            with self.subTest(writer=writer):
                path=root/'writer.py';path.unlink(missing_ok=True)
                self.assertEqual(check_paths([root],root=root).status,0)
                self.assertTrue(check_paths([root],root=root).results[0].cache_hit)
                path.write_text(writer)
                cold=check_paths([root],root=root,cache=False);warm=check_paths([root],root=root)
                self.assertEqual(cold.status,1);self.assertEqual(warm.status,1)
                self.assertEqual([(d.rule,d.reason)for f in cold.results for d in f.diagnostics],[(d.rule,d.reason)for f in warm.results for d in f.diagnostics])
    def test_consumer_require_modules_does_not_select_installed_ordinary_sibling(self):
        (self.producer/'checked_pricing/ordinary.py').write_text('def unsafe_ordinary(value):\n    return unknown(value)\n');self.wheel()
        (self.consumer/'pyproject.toml').write_text('[tool.pyalamode]\nrequire_modules=["*.py"]\n'+CONSUMER)
        # Consumer module initialization needs checked package parents/core here.
        (self.producer/'checked_pricing/core.py').write_text('# mode: fun\ndef quote(value:int)->int:\n    return value+2\n')
        shutil.rmtree(self.base/'out');[shutil.rmtree(p)for p in self.site.iterdir()];self.wheel()
        r=self.check();self.assertEqual(r.status,0,[d.reason for f in r.results for d in f.diagnostics]);self.assertEqual(r.coverage if hasattr(r,'coverage') else len(r.results),1)


    def rewrite_record(self):
        import base64,csv
        info=self.site/'checked_pricing-1.0.0.dist-info';members={p.relative_to(self.site).as_posix():p.read_bytes() for p in self.site.rglob('*') if p.is_file() and p!=info/'RECORD'}
        with (info/'RECORD').open('w',newline='')as stream:
            writer=csv.writer(stream,lineterminator='\n')
            for name,raw in sorted(members.items()):writer.writerow([name,'sha256='+base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip('='),str(len(raw))])
            writer.writerow([info.name+'/RECORD','',''])
    def test_current_forged_bytes_reanalyze_source_and_preserve_unrelated_proof(self):
        self.wheel();ep=self.site/'checked_pricing-1.0.0.dist-info/pyalamode/evidence.json';v=json.loads(ep.read_text());p=v['payload']
        raw=b'from pyalamode import fun\n@fun\ndef quote(value:int)->int:\n    return unknown(value)\n';sha=hashlib.sha256(raw).hexdigest()
        for path in ('checked_pricing/core.py','checked_pricing-1.0.0.dist-info/pyalamode/sources/checked_pricing/core.py'):
            (self.site/path).write_bytes(raw);p['artifacts'][path].update(sha256=sha,size=len(raw))
        p['inputs']['sources']['checked_pricing/core.py']['sha256']=sha
        next(r for r in p['modules'] if r['module']=='checked_pricing.core').update(source_sha256=sha,artifact_sha256=sha)
        v['sha256']=d.digest(p);ep.write_bytes(d.canonical(v));self.rewrite_record()
        use=self.consumer/'use.py';use.write_text(use.read_text()+'\n@fun\ndef unrelated(value:int)->int:\n    return value+1\n')
        r=self.check();self.assertEqual(r.status,1,r.to_dict());receipt=r.checked_dependencies[0]
        self.assertEqual((receipt['input_status'],receipt['source_status']),(0,1));self.assertEqual(receipt['exports'],[])
        diagnostics=[x for f in r.results for x in f.diagnostics];self.assertEqual({x.rule for x in diagnostics},{'PAL371'})
        context=diagnostics[0].dependency_context;self.assertEqual(context['reason_code'],'dependency-source-refused');self.assertIsNotNone(context['upstream']);self.assertEqual(context['upstream']['selector'],'checked_pricing.core:quote')
        self.assertTrue(next(c for f in r.results for c in f.contracts if c.name=='unrelated').source_evidence.startswith('checked'))
        _,state,_,_=observe(self.consumer,bootstrap=True);self.assertEqual(state['coverage']['eligible_functions'],2);self.assertEqual(state['current_dependency_status'],1)
    def test_consumer_approvals_are_its_own_current_operation_permissions(self):
        from pyalamode.integration_contracts import integration_snapshot
        operation='pyalamode.integrations.sha256_digest'
        def approval(root):
            row=integration_snapshot({},root)['inputs'][operation]
            return '[tool.pyalamode]\nexternal_trust="approved"\n[[tool.pyalamode.integration_approvals]]\noperation="'+operation+'"\ncontract_sha256="'+row['contract_sha256']+'"\ndependency_sha256="'+row['dependency_sha256']+'"\nowner="local team"\nrationale="current exact operation"\nprovenance="independent review"\n'
        (self.producer/'checked_pricing/core.py').write_text('from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef quote(value:bytes)->bytes:\n    return sha256_digest(value)\n')
        (self.producer/'pyproject.toml').write_text(approval(self.producer)+POLICY)
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import quote\n@fun\ndef total(value:bytes)->bytes:\n    return quote(value)\n')
        self.wheel();r=self.check();self.assertEqual(r.status,1,r.to_dict());self.assertEqual(r.checked_dependencies[0]['source_status'],1)
        self.assertTrue(any(x.dependency_context and x.dependency_context['upstream']['rule']=='PAL350' for f in r.results for x in f.diagnostics))
        (self.consumer/'pyproject.toml').write_text(approval(self.consumer)+CONSUMER);self.assertEqual(self.check().status,0)
    def test_duplicate_noncanonical_owner_and_closed_guard_metadata_refuse(self):
        self.wheel('exports');info=self.site/'checked_pricing-1.0.0.dist-info';duplicate=self.site/'checked_pricing-1.0.0-copy.dist-info';shutil.copytree(info,duplicate)
        self.assertEqual(self.check().status,2);shutil.rmtree(duplicate)
        ep=info/'pyalamode/evidence.json';original=json.loads(ep.read_text())
        for mutate in (lambda p:p['guards']['exports'][0]['parameters'].__setitem__('value','str'),lambda p:p['guards']['exports'].append(copy.deepcopy(p['guards']['exports'][0])),lambda p:p.__setitem__('claim_scope','arbitrary claim')):
            v=copy.deepcopy(original);mutate(v['payload']);v['sha256']=d.digest(v['payload']);ep.write_bytes(d.canonical(v));self.assertEqual(self.check().status,2)
    def test_stale_causes_record_report_axes_and_malformed_no_writes(self):
        from pyalamode.cli import main
        wheel=self.wheel('exports');info=self.site/'checked_pricing-1.0.0.dist-info'
        with zipfile.ZipFile(wheel)as z:evidence=json.loads(z.read(info.name+'/pyalamode/evidence.json'))['payload']
        facade=evidence['guards']['exports'][0]['public_boundary'].split(':')[0].replace('.','/')+'.py'
        self.assertIn(facade,evidence['guards']['generated_files']);self.assertEqual(evidence['artifacts'][facade]['role'],'generated')
        for path,cause in ((info/'pyalamode/sources/checked_pricing/core.py','stale-source'),(info/'pyalamode/policy.toml','stale-policy'),(self.site/'checked_pricing/core.py','stale-source'),(self.site/facade,'stale-artifact')):
            old=path.read_bytes()
            try:
                path.write_bytes(old+b'\n# current change\n');r=self.check();self.assertEqual(r.status,1)
                self.assertEqual(next(x for f in r.results for x in f.diagnostics if x.rule=='PAL370').dependency_context['reason_code'],cause)
                receipt=r.checked_dependencies[0];self.assertEqual(receipt['input_status'],1);self.assertIsNone(receipt['source_status']);self.assertFalse(receipt['verified']);self.assertTrue(receipt['complete'])
            finally:path.write_bytes(old)
        path=info/'pyalamode/sources/checked_pricing/core.py';path.write_bytes(path.read_bytes()+b'\n# changed\n')
        stream=io.StringIO()
        with redirect_stdout(stream):status=main(['report','--root',str(self.consumer),'--save','--json'])
        payload=json.loads(stream.getvalue());self.assertEqual(status,1);self.assertEqual(payload['written']['status'],0);self.assertFalse(payload['report']['verified']);self.assertEqual(payload['report']['state']['strict_status'],1)
        stream=io.StringIO()
        with redirect_stdout(stream):status=main(['baseline','--root',str(self.consumer),'--owner','team','--rationale','review current dependency debt','--json'])
        payload=json.loads(stream.getvalue());self.assertEqual(status,0);self.assertEqual(payload['written']['state_strict_status'],1);self.assertFalse(payload['written']['verified'])
        before={p.relative_to(self.consumer).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.consumer/'.pyalamode').rglob('*') if p.is_file()}
        (info/'pyalamode/evidence.json').write_text('{}')
        for command in (['report','--save'],['baseline','--replace','--owner','team','--rationale','invalid candidate']):
            with redirect_stdout(io.StringIO()):status=main([*command,'--root',str(self.consumer),'--json'])
            self.assertEqual(status,2)
        after={p.relative_to(self.consumer).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.consumer/'.pyalamode').rglob('*') if p.is_file()};self.assertEqual(before,after)
    def test_declared_unselected_producer_export_is_semantic_no_artifact(self):
        (self.producer/'checked_pricing/core.py').write_text('def quote(value:int)->int:\n    return value+2\n')
        out=self.base/'out'/d.wheel_paths({'name':'checked-pricing','version':'1.0.0'})[0];r=build_paths([self.producer],root=self.producer,artifact='wheel',output=out)
        self.assertEqual(r.status,1,r.to_dict());self.assertEqual([x.rule for x in r.policy_diagnostics],['PAL371']);self.assertFalse(out.exists());self.assertEqual(r.tooling,[])
    def test_genuine_m10_history_remains_closed_provenance_only(self):
        archive=json.loads((Path(__file__).parent/'fixtures/m11/legacy-m10.json').read_text());manifest=archive['manifest'];root=self.base/'legacy';root.mkdir()
        self.assertEqual(set(archive['files']),set(manifest['files']))
        for name,text in archive['files'].items():
            raw=text.encode();self.assertEqual(hashlib.sha256(raw).hexdigest(),manifest['files'][name]['sha256']);self.assertEqual(len(raw),manifest['files'][name]['bytes']);target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        reference=m.load_reference(root,'.pyalamode/baseline.json');self.assertEqual(reference['record']['id'],manifest['active_id']);self.assertEqual(reference['record']['previous_id'],manifest['previous_id']);self.assertEqual(len(reference['state']['inputs']['product_artifacts']),19);self.assertEqual(reference['state']['schema'],1)
        legacy=copy.deepcopy(reference['state']);operation='pyalamode.integrations.sha256_digest'
        inputs={'contract_sha256':'a'*64,'dependency_sha256':'b'*64,'admission':'denied','approval':None,'identity_error':None}
        boundary=next(r for r in legacy['boundaries'] if r['kind']=='function')
        required={'operation':operation,'required_by':[{'boundary':boundary['selector'],'path':boundary['path'],'line':3,'via':'direct'}],'contract_sha256':inputs['contract_sha256'],'dependency_sha256':inputs['dependency_sha256'],'admission':'denied','engine_status':1,'engine_rule':'PAL350','evidence':{'kind':'integration-input','value':inputs}}
        legacy['inputs']['integration_inputs'][operation]=inputs;legacy['required_operations']=[required]
        event={'boundary':None,'before':copy.deepcopy(required),'after':copy.deepcopy(required),'reason':'current-approval-refused','location':None}
        legacy['current_policy_events']['approval_failures']=[event]
        self.assertEqual(m._state(legacy,retained=True)['schema'],1)
        for sites in ('required','event-before','event-after'):
            corrupted=copy.deepcopy(legacy)
            row=corrupted['required_operations'][0] if sites=='required' else corrupted['current_policy_events']['approval_failures'][0]['before' if sites=='event-before' else 'after']
            row['required_by'][0]['source_owner']='project'
            with self.subTest(sites=sites),self.assertRaises(m.MigrationError):m._state(corrupted,retained=True)
        _,state,report,_=observe(root);self.assertEqual(state['schema'],4);self.assertEqual(len(state['inputs']['product_artifacts']),26);self.assertEqual(state['strict_status'],1);self.assertEqual(len(report['comparison']['retained_findings']),2);self.assertEqual(report['comparison']['new_findings'],[])
        with self.assertRaises(m.MigrationError):m.write_baseline(root,reference['state'],owner='team',rationale='cannot recertify historical inputs',replace=True,prepublish=lambda:None)
        for name,text in archive['files'].items():self.assertEqual((root/name).read_bytes(),text.encode())


    def test_tree_guards_and_readiness_keep_installed_nominal_and_prerequisite_evidence(self):
        from pyalamode.migration_views import ready_view
        source=self.producer/'checked_pricing/core.py';source.write_text(source.read_text()+'\nfrom pyalamode import record\n@record\nclass Invoice:\n    total: int\n')
        (self.producer/'pyproject.toml').write_text(POLICY.replace('exports=["checked_pricing.core:quote"]','exports=["checked_pricing.core:quote","checked_pricing.core:Invoice"]'));self.wheel()
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import Invoice\n@fun\ndef total(value:Invoice)->Invoice:\n    return value\n')
        (self.consumer/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards="exports"\nguarded_exports=["use:total"]\n'+CONSUMER)
        built=build_paths([self.consumer],root=self.consumer,output=self.base/'guarded-tree');self.assertEqual(built.status,0,built.to_dict());self.assertIn('checked_pricing.core',(self.base/'guarded-tree/pyalamode_exports/use.py').read_text())
        (self.consumer/'pyproject.toml').write_text(CONSUMER);(self.consumer/'use.py').write_text('from checked_pricing.core import quote\ndef total(value:int)->int:\n    return quote(value)\n')
        snapshot,state,report,_=observe(self.consumer,bootstrap=True);ready=ready_view(snapshot,state)
        rows=[r for r in ready['groups'] if 'use:total' in r['members']];self.assertEqual(len(rows),1);prerequisite=rows[0]['external_prerequisites'][0]
        self.assertEqual(prerequisite['selector'],'checked_pricing.core:quote');self.assertEqual(set(prerequisite),{'selector','dependency','source_evidence','failures','trust','effect_bound','required_effects','initialization'});self.assertTrue(prerequisite['initialization']);self.assertEqual(state['coverage']['eligible_functions'],1)


    def test_ordinary_and_absent_installed_callables_have_exact_unpublished_context(self):
        (self.producer/'checked_pricing/ordinary.py').write_text('raise RuntimeError("must remain static")\ndef ordinary(value:int)->int:\n    return value+1\n')
        self.wheel()
        cases=(('from checked_pricing.ordinary import ordinary','ordinary(value)','checked_pricing.ordinary:ordinary'),('import checked_pricing.ordinary as ordinary_module','ordinary_module.ordinary(value)','checked_pricing.ordinary:ordinary'),('from checked_pricing.ordinary import absent','absent(value)','checked_pricing.ordinary:absent'),('from checked_pricing import ordinary','ordinary.ordinary(value)','checked_pricing.ordinary:ordinary'))
        for imported,called,selector in cases:
            with self.subTest(imported=imported,called=called):
                (self.consumer/'use.py').write_text('from pyalamode import fun\n'+imported+'\n@fun\ndef total(value:int)->int:\n    return '+called+'\n')
                for cache in (False,True,True):
                    result=check_paths([self.consumer],root=self.consumer,cache=cache);self.assertEqual(result.status,1,result.to_dict());self.assertEqual(result.to_dict()['source_status'],1);self.assertFalse(result.verified)
                    diagnostics=[x for file in result.results for x in file.diagnostics];self.assertEqual([x.rule for x in diagnostics],['PAL371']);context=diagnostics[0].dependency_context
                    self.assertEqual(context,{'dependency':{'name':'checked-pricing','version':'1.0.0','packages':['checked_pricing']},'selector':selector,'rule':'PAL371','reason_code':'unpublished-export','site':'call','upstream':None});self.assertEqual(diagnostics[0].boundary,'total');self.assertEqual(diagnostics[0].line,5)
                    self.assertTrue(all(e['selector']!=selector for row in result.checked_dependencies for e in row['exports']))
                    self.assertFalse(result.results[0].contracts[0].source_evidence.startswith('checked'))
        # Module imports still reach the published original; writers still deny it.
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing import core\n@fun\ndef total(value:int)->int:\n    return core.quote(value)\n')
        self.assertEqual(self.check().status,0)
        (self.consumer/'writer.py').write_text('import checked_pricing.core as core\ncore.quote=lambda value:value\n')
        self.assertEqual(self.check().status,1)


    def test_cross_distribution_reexport_uses_actual_owner_approvals_and_parents(self):
        from pyalamode.integration_contracts import integration_snapshot
        operation='pyalamode.integrations.sha256_digest'
        def approval(root,owner):
            row=integration_snapshot({},root)['inputs'][operation]
            return '[tool.pyalamode]\nexternal_trust="approved"\n[[tool.pyalamode.integration_approvals]]\noperation="'+operation+'"\ncontract_sha256="'+row['contract_sha256']+'"\ndependency_sha256="'+row['dependency_sha256']+'"\nowner="'+owner+'"\nrationale="current exact operation"\nprovenance="independent review"\n'
        (self.producer/'checked_pricing/core.py').write_text('from pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef quote(value:bytes)->bytes:\n    return sha256_digest(value)\n@fun\ndef hidden(value:bytes)->bytes:\n    return value\n')
        (self.producer/'pyproject.toml').write_text(approval(self.producer,'base producer')+POLICY);self.wheel()
        bridge=self.base/'bridge';(bridge/'checked_bridge').mkdir(parents=True)
        (bridge/'checked_bridge/__init__.py').write_text('from checked_pricing.core import quote,hidden\n')
        (bridge/'checked_bridge/core.py').write_text('from pyalamode import fun\n@fun\ndef anchor(value:int)->int:\n    return value\n')
        bridge_policy='[tool.pyalamode.distribution]\nschema=1\nname="checked-bridge"\nversion="1.0.0"\npackages=["checked_bridge"]\nexports=["checked_bridge.core:anchor"]\n'
        bridge_dependency='[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="checked-bridge"\nversion="1.0.0"\npackages=["checked_bridge"]\n'
        (bridge/'pyproject.toml').write_text(approval(bridge,'bridge producer')+bridge_policy+CONSUMER)
        wheel=self.base/'bridge-out/checked_bridge-1.0.0-py3-none-any.whl';built=build_paths([bridge],root=bridge,artifact='wheel',output=wheel);self.assertEqual(built.status,0,built.to_dict())
        with zipfile.ZipFile(wheel)as archive:
            evidence=json.loads(archive.read('checked_bridge-1.0.0.dist-info/pyalamode/evidence.json'))['payload']
            parent=next(r for r in evidence['modules'] if r['module']=='checked_bridge');self.assertIsNone(parent['initialization']['effects']);self.assertIsNone(parent['initialization']['failures']);self.assertFalse(parent['initialization']['source_evidence'].startswith('checked'))
            archive.extractall(self.site)
        source='from pyalamode import fun\nfrom checked_bridge import quote\n@fun\ndef total(value:bytes)->bytes:\n    return quote(value)\n'
        (self.consumer/'use.py').write_text(source);(self.consumer/'pyproject.toml').write_text(CONSUMER+bridge_dependency)
        denied=self.check();self.assertEqual(denied.status,1);self.assertFalse(denied.verified);self.assertEqual(next(r for r in denied.checked_dependencies if r['declaration']['name']=='checked-pricing')['source_status'],1)
        (self.consumer/'pyproject.toml').write_text(approval(self.consumer,'consumer team')+CONSUMER+bridge_dependency)
        accepted=self.check();self.assertEqual(accepted.status,0,accepted.to_dict());contract=accepted.results[0].contracts[0]
        self.assertTrue(any('checked_pricing-1.0.0.dist-info/pyalamode/sources/checked_pricing/core.py::quote' in target for target in contract.invoked_targets));self.assertEqual(contract.external_assumptions[0]['approval']['owner'],'consumer team')
        for imported,called in (('from checked_bridge import hidden','hidden(value)'),('import checked_bridge as bridge','bridge.hidden(value)')):
            (self.consumer/'use.py').write_text('from pyalamode import fun\n'+imported+'\n@fun\ndef total(value:bytes)->bytes:\n    return '+called+'\n')
            refused=self.check();self.assertEqual(refused.status,1,refused.to_dict());diagnostics=[x for f in refused.results for x in f.diagnostics];self.assertEqual([x.rule for x in diagnostics],['PAL371']);context=diagnostics[0].dependency_context
            self.assertEqual(context['dependency'],{'name':'checked-pricing','version':'1.0.0','packages':['checked_pricing']});self.assertEqual(context['selector'],'checked_pricing.core:hidden');self.assertEqual(context['reason_code'],'unpublished-export')
        (self.consumer/'use.py').write_text('# mode: fun\nfrom checked_bridge import quote\ndef total(value:bytes)->bytes:\n    return quote(value)\n')
        strict=self.check();self.assertEqual(strict.status,1);self.assertTrue(any(x.rule=='PAL241' and 'checked_bridge' in x.reason for f in strict.results for x in f.diagnostics))

    def test_guard_parent_alias_and_child_binding_writers_refuse_current_evidence(self):
        import ast
        from pyalamode import project
        from pyalamode.checker import SourceGraph
        core=self.producer/'checked_pricing/core.py';core.write_text('raise AssertionError("producer application executed")\n'+core.read_text())
        self.wheel('exports');(self.consumer/'independent.py').write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value\n')
        parent='checked_pricing._pyalamode_exports';alias=parent+'.core';original_module='checked_pricing.core';private=[];original=project._intrinsic_distribution_graph
        def observed(snapshot,*args):
            graph,dependencies=original(snapshot,*args);private.append(graph);return graph,dependencies
        def refusal(result):
            self.assertEqual(result.status,1,result.to_dict());self.assertEqual(result.tooling,[]);self.assertFalse(result.verified)
            row=result.checked_dependencies[0];self.assertEqual(row['input_status'],0);self.assertEqual(row['source_status'],1);self.assertTrue(row['complete']);self.assertFalse(row['verified']);self.assertEqual(row['exports'],[])
            findings=[d for f in result.results for d in f.diagnostics if d.rule=='PAL371'];self.assertTrue(any(d.path==str(self.consumer/'use.py')for d in findings));self.assertTrue(all(d.path in {f.path for f in result.results} and Path(d.path).is_relative_to(self.consumer) and d.dependency_context['upstream']['rule']=='PAL240'for d in findings))
            independent=next(c for f in result.results if Path(f.path).name=='independent.py'for c in f.contracts);self.assertTrue(independent.source_evidence.startswith('checked'))
        cases=(('from-parent','from '+alias+' import quote','quote(value)','from '+parent+' import core\ncore.quote=lambda cents,discount:0\n','core','module:'+alias),('parent-binding','import '+alias+' as core','core.quote(value)','import '+parent+' as guards\nguards.core=0\n','guards','module:'+parent))
        for label,imports,call,writer_source,name,reference in cases:
            with self.subTest(label=label):
                (self.consumer/'use.py').write_text('from pyalamode import fun\n'+imports+'\n@fun\ndef total(value:int)->int:\n    return '+call+'\n')
                self.assertEqual(check_paths([self.consumer],root=self.consumer,cache=True).status,0)
                writer=self.consumer/'writer.py';writer.write_text('raise AssertionError("consumer writer executed")\n'+writer_source);captured={};private.clear()
                try:
                    with patch.object(project,'_intrinsic_distribution_graph',observed):r=self.check(_capture=captured)
                    refusal(r);graph=captured['graph'];target=graph.modules[original_module].path+'::quote'
                    self.assertNotIn(parent,graph.modules);self.assertIs(graph.modules[alias],graph.modules[original_module]);self.assertEqual(graph.reference(graph.analyzers[str(writer)],ast.Name(id=name)),reference)
                    self.assertIn(target,graph.replaced_functions);self.assertIn((alias,'*'),graph.replaced_foundations);self.assertNotIn(target,private[0].replaced_functions);self.assertNotIn(str(writer),private[0].analyzers)
                    self.assertTrue(any(target+'.<behavior>'in f.binding_context or alias+'.*.<behavior>'in f.binding_context for f in r.results if Path(f.path).name=='use.py'))
                    for _ in range(2):refusal(check_paths([self.consumer],root=self.consumer,cache=True))
                    out=self.base/('guard-parent-'+label);built=build_paths([self.consumer],root=self.consumer,output=out);refusal(built);self.assertFalse(out.exists());self.assertIsNone(built.output)
                    # Dotted captured module presence cannot invent an absent namespace.
                    policy=copy.deepcopy(captured['policy']);snapshot=copy.deepcopy(captured['distribution_snapshot']);snapshot['aliases']={};policy['_distribution_snapshot']=snapshot
                    detached=SourceGraph({p:a.source for p,a in graph.analyzers.items()},self.consumer,False,policy);detached.modules[alias]=detached.modules[original_module]
                    self.assertEqual(detached._module_writer_targets(parent),[]);self.assertNotIn(target,detached.replaced_functions)
                    if label=='from-parent':self.assertIsNone(detached.reference(detached.analyzers[str(writer)],ast.Name(id='core')))
                finally:writer.unlink()
                restored=check_paths([self.consumer],root=self.consumer,cache=True);self.assertEqual(restored.status,0,restored.to_dict());self.assertTrue(restored.checked_dependencies[0]['exports'])

    def test_package_child_alias_writers_invalidate_current_and_installed_sources(self):
        import ast
        from pyalamode import project
        from pyalamode.checker import SourceGraph
        (self.producer/'checked_pricing/writer.py').write_text('raise AssertionError("installed writer source executed")\n')
        self.wheel();(self.consumer/'independent.py').write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value\n')
        original=project._intrinsic_distribution_graph
        def current_refusal(result):
            self.assertEqual(result.status,1,result.to_dict());self.assertEqual(result.tooling,[]);self.assertFalse(result.verified)
            receipt=result.checked_dependencies[0];self.assertEqual(receipt['input_status'],0);self.assertEqual(receipt['source_status'],1);self.assertTrue(receipt['complete']);self.assertFalse(receipt['verified']);self.assertEqual(receipt['exports'],[])
            findings=[d for f in result.results for d in f.diagnostics if d.rule=='PAL371'];self.assertTrue(any(d.path==str(self.consumer/'use.py')for d in findings));self.assertTrue(all(d.path in {f.path for f in result.results} and Path(d.path).is_relative_to(self.consumer) and d.dependency_context['upstream']['rule']=='PAL240'for d in findings))
            independent=next(c for f in result.results if Path(f.path).name=='independent.py'for c in f.contracts);self.assertTrue(independent.source_evidence.startswith('checked'))
        for label,bindings,name in (('exact','from checked_pricing import core','core'),('renamed','from checked_pricing import core as changed','changed'),('assignment','from checked_pricing import core\nchanged=core','changed')):
            with self.subTest(label=label):
                self.assertEqual(check_paths([self.consumer],root=self.consumer,cache=True).status,0)
                writer=self.consumer/'writer.py';writer.write_text('raise AssertionError("consumer writer executed")\n'+bindings+'\n'+name+'.quote=lambda cents,discount:0\n')
                captured={};private=[]
                def observed(snapshot,*args):
                    graph,dependencies=original(snapshot,*args);private.append(graph);return graph,dependencies
                try:
                    with patch.object(project,'_intrinsic_distribution_graph',observed):r=self.check(_capture=captured)
                    current_refusal(r);graph=captured['graph'];target=graph.modules['checked_pricing.core'].path+'::quote'
                    self.assertEqual(graph.reference(graph.analyzers[str(writer)],ast.Name(id=name)),'module:checked_pricing.core');self.assertIn(target,graph.replaced_functions);self.assertNotIn(target,private[0].replaced_functions)
                    self.assertTrue(any(target+'.<behavior>'in f.binding_context for f in r.results if Path(f.path).name=='use.py'))
                    for _ in range(2):current_refusal(check_paths([self.consumer],root=self.consumer,cache=True))
                    out=self.base/('child-writer-'+label);built=build_paths([self.consumer],root=self.consumer,output=out);current_refusal(built);self.assertFalse(out.exists());self.assertIsNone(built.output)
                finally:writer.unlink()
                restored=check_paths([self.consumer],root=self.consumer,cache=True);self.assertEqual(restored.status,0,restored.to_dict());self.assertTrue(restored.checked_dependencies[0]['exports'])
        info=self.site/'checked_pricing-1.0.0.dist-info';ep=info/'pyalamode/evidence.json';record=info/'RECORD';ep_before=ep.read_bytes();record_before=record.read_bytes();runtime=self.site/'checked_pricing/writer.py';authored=info/'pyalamode/sources/checked_pricing/writer.py';runtime_before=runtime.read_bytes();authored_before=authored.read_bytes()
        changed=b'raise AssertionError("installed writer source executed")\nfrom checked_pricing import core\ncore.quote=lambda cents,discount:0\n';sha=hashlib.sha256(changed).hexdigest();runtime.write_bytes(changed);authored.write_bytes(changed);envelope=json.loads(ep_before);payload=envelope['payload']
        for path in ('checked_pricing/writer.py',info.name+'/pyalamode/sources/checked_pricing/writer.py'):payload['artifacts'][path].update(sha256=sha,size=len(changed))
        payload['inputs']['sources']['checked_pricing/writer.py']['sha256']=sha;next(row for row in payload['modules']if row['module']=='checked_pricing.writer').update(source_sha256=sha,artifact_sha256=sha);envelope['sha256']=d.digest(payload);ep.write_bytes(d.canonical(envelope));self.rewrite_record()
        captured={};private=[]
        try:
            with patch.object(project,'_intrinsic_distribution_graph',observed):r=self.check(_capture=captured)
            current_refusal(r);target=captured['graph'].modules['checked_pricing.core'].path+'::quote';self.assertIn(target,captured['graph'].replaced_functions);self.assertIn(target,private[0].replaced_functions)
            out=self.base/'installed-child-writer';built=build_paths([self.consumer],root=self.consumer,output=out);current_refusal(built);self.assertFalse(out.exists())
        finally:runtime.write_bytes(runtime_before);authored.write_bytes(authored_before);ep.write_bytes(ep_before);record.write_bytes(record_before)
        self.assertEqual(self.check().status,0)
        cases=(('absent','', 'module:pkg.core'),('constant','core=0\n',None),('function','def core():\n    return 0\n',None),('class','class core:\n    pass\n',None),('compound','if True:\n    core=0\n',None),('star','from unknown import *\n',None),('known','from pyalamode import fun\n@fun\ndef core(value:int)->int:\n    return value\n','function'),('module','import other as core\n','module:other'),('nonpackage','',None))
        for label,parent_source,expected in cases:
            with self.subTest(parent=label):
                root=self.base/'precedence'/label;package=root/'pkg';package.mkdir(parents=True);parent=root/'pkg.py'if label=='nonpackage'else package/'__init__.py';child=package/'core.py';caller=root/'use.py';parent.write_text(parent_source);child.write_text('from pyalamode import fun\n@fun\ndef quote(value:int)->int:\n    return value\n');caller.write_text('from pkg import core\n')
                sources={str(parent):parent_source,str(child):child.read_text(),str(caller):caller.read_text()};graph=SourceGraph(sources,root,False,{})
                if expected=='function':expected=str(parent)+'::core'
                self.assertEqual(graph.reference(graph.analyzers[str(caller)],ast.Name(id='core')),expected)
                if label=='absent':
                    shadow=root/'pkg.py';shadow.write_text('core=0\n')
                    for ordered in ({str(shadow):shadow.read_text(),**sources},{**sources,str(shadow):shadow.read_text()}):
                        graph=SourceGraph(ordered,root,False,{});self.assertEqual(graph.modules['pkg'].path,str(parent));self.assertEqual(graph.reference(graph.analyzers[str(caller)],ast.Name(id='core')),'module:pkg.core')

    def test_denied_native_approval_keeps_intrinsic_debug_local_schema_without_proof(self):
        from pyalamode import project
        from pyalamode.integration_contracts import integration_snapshot
        operation='pyalamode.integrations.sha256_digest'
        def approval(root,owner,debug=False):
            row=integration_snapshot({},root)['inputs'][operation]
            text='[tool.pyalamode]\nexternal_trust="approved"\n'
            if debug:text+='boundary_guards="debug"\nguarded_exports=["checked_pricing.core:quote"]\n'
            return text+'[[tool.pyalamode.integration_approvals]]\noperation="'+operation+'"\ncontract_sha256="'+row['contract_sha256']+'"\ndependency_sha256="'+row['dependency_sha256']+'"\nowner="'+owner+'"\nrationale="current exact operation"\nprovenance="independent local review"\n'
        source='raise AssertionError("application source executed")\nfrom pyalamode import fun\nfrom pyalamode.integrations import sha256_digest\n@fun\ndef quote(value:bytes)->bytes:\n    local=sha256_digest(value)\n    return local\n'
        (self.producer/'checked_pricing/core.py').write_text(source);(self.producer/'pyproject.toml').write_text(approval(self.producer,'producer team',True)+POLICY)
        wheel=self.wheel();(self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import quote\n@fun\ndef total(value:bytes)->bytes:\n    return quote(value)\n')
        captured={};private=[];original=project._intrinsic_distribution_graph
        def observed(snapshot,*args):
            graph,dependencies=original(snapshot,*args);private.append((snapshot,graph,dependencies));return graph,dependencies
        with patch.object(project,'_intrinsic_distribution_graph',observed):r=self.check(_capture=captured)
        def semantic_refusal(result):
            self.assertEqual(result.status,1,result.to_dict());self.assertEqual(result.tooling,[]);self.assertFalse(result.verified)
            row=result.checked_dependencies[0];self.assertEqual(row['input_status'],0);self.assertEqual(row['source_status'],1);self.assertTrue(row['complete']);self.assertFalse(row['verified']);self.assertEqual(row['exports'],[])
            self.assertTrue(any(d.rule=='PAL371' and d.dependency_context['upstream']['rule']=='PAL350' for f in result.results for d in f.diagnostics))
        semantic_refusal(r);self.assertEqual(len(private),1);snapshot,intrinsic,_=private[0];current=captured['graph']
        self.assertFalse(current._intrinsic_schema_outputs);self.assertTrue(intrinsic._intrinsic_schema_outputs)
        for graph in (current,intrinsic):
            self.assertEqual(graph.integration_snapshot['inputs'][operation]['admission'],'denied');self.assertIsNone(graph.integration_snapshot['inputs'][operation]['approval']);self.assertEqual(graph.integrations['sha256_digest']['admission'],'denied')
            self.assertEqual(graph.modules['checked_pricing.core'].result.status,1);self.assertTrue(any(d.rule=='PAL350'for d in graph.modules['checked_pricing.core'].result.diagnostics))
        private_contract=intrinsic.modules['checked_pricing.core'].result.contracts[0];current_contract=current.modules['checked_pricing.core'].result.contracts[0]
        self.assertEqual(private_contract.data_assertions,[{'line':6,'name':'local','schema':'bytes'}]);self.assertEqual(current_contract.data_assertions,[]);self.assertFalse(private_contract.source_evidence.startswith('checked'))
        for _ in range(2):semantic_refusal(check_paths([self.consumer],root=self.consumer,cache=True))
        out=self.base/'native-denied';built=build_paths([self.consumer],root=self.consumer,output=out);semantic_refusal(built);self.assertFalse(out.exists());self.assertIsNone(built.output)
        info=self.site/'checked_pricing-1.0.0.dist-info';ep=info/'pyalamode/evidence.json';record=info/'RECORD';ep_before=ep.read_bytes();record_before=record.read_bytes();core=self.site/'checked_pricing/core.py';core_before=core.read_bytes()
        with zipfile.ZipFile(wheel)as archive:envelope=json.loads(archive.read(info.name+'/pyalamode/evidence.json'))
        self.assertNotIn('checked_pricing/core.py',envelope['payload']['guards']['generated_files'])
        corrupted=copy.deepcopy(envelope);changed=core_before+b'\n# counterfeit debug runtime bytes\n';core.write_bytes(changed);p=corrupted['payload'];p['artifacts']['checked_pricing/core.py'].update(sha256=hashlib.sha256(changed).hexdigest(),size=len(changed));next(m for m in p['modules']if m['module']=='checked_pricing.core')['artifact_sha256']=hashlib.sha256(changed).hexdigest();corrupted['sha256']=d.digest(p);ep.write_bytes(d.canonical(corrupted));self.rewrite_record()
        try:
            forged=self.check();self.assertEqual(forged.status,2,forged.to_dict());self.assertEqual([x.rule for x in forged.tooling],['PAL001']);self.assertEqual(forged.tooling[0].origin,'installed distribution derivation');self.assertIn('authored/generator derivation',forged.tooling[0].reason)
            out=self.base/'native-forged';built=build_paths([self.consumer],root=self.consumer,output=out);self.assertEqual(built.status,2);self.assertFalse(out.exists())
        finally:core.write_bytes(core_before);ep.write_bytes(ep_before);record.write_bytes(record_before)
        semantic_refusal(self.check())
        writer=self.consumer/'writer.py';writer.write_text('raise AssertionError("consumer writer executed")\nimport _sha2\n_sha2.sha256=lambda value:b"x"\n')
        try:
            refused=self.check();self.assertEqual(refused.status,1,refused.to_dict());self.assertEqual(refused.tooling,[]);self.assertEqual(refused.checked_dependencies[0]['input_status'],0);self.assertEqual(refused.checked_dependencies[0]['source_status'],1);self.assertEqual(refused.checked_dependencies[0]['exports'],[]);self.assertTrue(any(d.rule=='PAL371' and d.dependency_context['upstream']['rule']=='PAL240'for f in refused.results for d in f.diagnostics))
        finally:writer.unlink()
        self.assertEqual(self.check().status,1)
        policy=captured['policy'];integrations=captured['integration_snapshot'];path=intrinsic.modules['checked_pricing.core'].path
        for label,call in (('arity','sha256_digest(value,value)'),('type','sha256_digest("wrong")'),('writer','sha256_digest(value)')):
            with self.subTest(label=label):
                altered=copy.deepcopy(snapshot);altered['sources'][path]=source.replace('sha256_digest(value)',call)
                if label=='writer':altered['sources'][path]+='\nimport _sha2\n_sha2.sha256=lambda value:b"x"\n'
                derived,_=original(altered,policy,integrations,self.consumer);result=derived.modules['checked_pricing.core'].result;contract=result.contracts[0]
                self.assertEqual(result.status,1);self.assertEqual(contract.data_assertions,[]);self.assertFalse(contract.source_evidence.startswith('checked'));self.assertTrue(any(x.rule==('PAL240'if label=='writer'else 'PAL221')for x in result.diagnostics));self.assertEqual(derived.integrations['sha256_digest']['admission'],'denied')
        (self.consumer/'pyproject.toml').write_text(approval(self.consumer,'independent consumer team')+CONSUMER);accepted=self.check();self.assertEqual(accepted.status,0,accepted.to_dict());self.assertEqual(accepted.checked_dependencies[0]['source_status'],0);self.assertTrue(accepted.checked_dependencies[0]['exports'])

    def nominal_writer_install(self,mode):
        if (self.base/'out').exists():(self.base/'out').rename(self.base/('retained-out-'+mode))
        for p in self.site.iterdir():shutil.rmtree(p)
        (self.producer/'checked_pricing/core.py').write_text('''# mode: fun
from pyalamode import record, variant, case
@record
class Invoice:
    order_id: str
@record
class Wrapper:
    item: Invoice
@variant
class Message:
    @case
    class Has:
        item: Invoice
    @case
    class Empty:
        pass
def quote(value:int)->int:
    return value+2
def echo(value:Invoice)->Invoice:
    local=value
    typed:Invoice=local
    made=Invoice(typed.order_id)
    boxed=Wrapper(made)
    tag=Message.Has(boxed.item)
    return tag.item
def carry(value:tuple[Invoice,...])->tuple[Invoice,...]:
    return value
''')
        (self.producer/'checked_pricing/ordinary.py').write_text('raise AssertionError("installed ordinary source executed")\n')
        exports=['checked_pricing.core:'+name for name in ('quote','echo','carry','Invoice','Wrapper','Message')];guards=exports[:3]
        (self.producer/'pyproject.toml').write_text('[tool.pyalamode]\nboundary_guards='+json.dumps(mode)+'\n'+('guarded_exports='+json.dumps(guards)+'\n'if mode!='off'else '')+POLICY.replace('exports=["checked_pricing.core:quote"]','exports='+json.dumps(exports)))
        wheel=self.wheel()
        (self.consumer/'use.py').write_text('from pyalamode import fun\nfrom checked_pricing.core import echo,Invoice\n@fun\ndef total(value:Invoice)->Invoice:\n    return echo(value)\n')
        (self.consumer/'independent.py').write_text('from pyalamode import fun\n@fun\ndef independent(value:int)->int:\n    return value\n')
        info=self.site/'checked_pricing-1.0.0.dist-info'
        with zipfile.ZipFile(wheel)as z:envelope=json.loads(z.read(info.name+'/pyalamode/evidence.json'))
        return info,envelope

    def test_nominal_writer_keeps_current_semantics_and_intrinsic_guard_derivation_separate(self):
        from pyalamode import project
        for mode in ('off','exports','debug'):
            with self.subTest(mode=mode):
                info,envelope=self.nominal_writer_install(mode);self.assertEqual(self.check().status,0)
                before={p.relative_to(self.site).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in self.site.rglob('*')if p.is_file()}
                writer=self.consumer/'writer.py';writer.write_text('raise AssertionError("consumer writer executed")\nfrom checked_pricing.core import Invoice\nInvoice.order_id=property(lambda self:"x")\n')
                captured={};private=[];original=project._intrinsic_distribution_graph
                def observed(snapshot,*args):
                    graph,dependencies=original(snapshot,*args);private.append((snapshot,graph,dependencies));return graph,dependencies
                try:
                    with patch.object(project,'_intrinsic_distribution_graph',observed):r=check_paths([self.consumer],root=self.consumer,cache=False,_capture=captured)
                    self.assertEqual(r.status,1,r.to_dict());self.assertEqual(r.tooling,[]);self.assertFalse(r.verified)
                    row=r.checked_dependencies[0];self.assertEqual(row['admission'],'current');self.assertEqual(row['input_status'],0);self.assertEqual(row['source_status'],1);self.assertTrue(row['complete']);self.assertFalse(row['verified']);self.assertEqual(row['exports'],[])
                    dependency=[x for f in r.results for x in f.diagnostics if x.rule=='PAL371'];self.assertTrue(dependency);self.assertTrue(all(x.dependency_context['reason_code']=='dependency-source-refused' for x in dependency));self.assertTrue(any(x.dependency_context['upstream']['rule']=='PAL240'for x in dependency))
                    independent=next(c for f in r.results if Path(f.path).name=='independent.py'for c in f.contracts);self.assertTrue(independent.source_evidence.startswith('checked'))
                    self.assertEqual(len(private),1);snapshot,intrinsic,dependencies=private[0];semantic=captured['graph']
                    self.assertIsNot(intrinsic.distributions,snapshot);self.assertIsNot(intrinsic.source_owners,semantic.source_owners);self.assertEqual(set(intrinsic.analyzers),set(snapshot['sources']));self.assertNotIn(str(writer),intrinsic.analyzers);self.assertIsNone(intrinsic.resolve_module('use'))
                    self.assertEqual(intrinsic.source_owners,semantic.source_owners);self.assertIsNot(intrinsic.integration_snapshot,semantic.integration_snapshot)
                    for path in intrinsic.analyzers:
                        self.assertIsNot(intrinsic.analyzers[path].result,semantic.analyzers[path].result);self.assertIsNot(intrinsic.analyzers[path].tree,semantic.analyzers[path].tree)
                    identity="Record['checked_pricing.core:Invoice']";self.assertTrue(intrinsic.records[identity].valid);self.assertFalse(semantic.records[identity].valid)
                    core=intrinsic.modules['checked_pricing.core'];echo=next(c for c in core.result.contracts if c.name=='echo');self.assertTrue({'local','typed','made','boxed','tag'}<=set(x['name']for x in echo.data_assertions))
                    self.assertEqual(intrinsic.records["Record['checked_pricing.core:Wrapper']"].fields['item'],identity);self.assertEqual(intrinsic.variants["Variant['checked_pricing.core:Message']"].cases['Has'].fields['item'],identity)
                    self.assertEqual(r.analysis_counts['intrinsic_graphs'],1);self.assertEqual(r.analysis_counts['intrinsic_writer_scan_files'],3);self.assertEqual(r.analysis_counts['intrinsic_fresh_body_files'],3);self.assertEqual(r.analysis_counts['intrinsic_source_dependency_edges'],sum(map(len,dependencies.values())))
                    self.assertEqual(r.to_dict()['coverage']['eligible_functions'],2)
                    for _ in range(2):
                        warm=check_paths([self.consumer],root=self.consumer,cache=True);self.assertEqual(warm.status,1,warm.to_dict());self.assertEqual(warm.checked_dependencies[0]['exports'],[]);self.assertEqual(warm.analysis_counts['intrinsic_fresh_body_files'],3)
                    out=self.base/('writer-refused-'+mode);built=build_paths([self.consumer],root=self.consumer,output=out);self.assertEqual(built.status,1,built.to_dict());self.assertFalse(out.exists());self.assertIsNone(built.output)
                    after={p.relative_to(self.site).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in self.site.rglob('*')if p.is_file()};self.assertEqual(before,after)
                finally:writer.unlink()
                restored=self.check();self.assertEqual(restored.status,0,restored.to_dict());self.assertTrue(restored.checked_dependencies[0]['exports'])

    def test_nominal_writer_does_not_hide_forged_contracts_or_generated_bytes(self):
        for mode in ('off','exports','debug'):
            with self.subTest(mode=mode):
                info,envelope=self.nominal_writer_install(mode);self.assertEqual(self.check().status,0)
                ep=info/'pyalamode/evidence.json';record=info/'RECORD';ep_before=ep.read_bytes();record_before=record.read_bytes();writer=self.consumer/'writer.py'
                writer.write_text('raise AssertionError("consumer writer executed")\nfrom checked_pricing.core import Invoice\nInvoice.order_id=property(lambda self:"x")\n')
                def write_payload(value):
                    value['sha256']=d.digest(value['payload']);ep.write_bytes(d.canonical(value));self.rewrite_record()
                try:
                    self.assertEqual(self.check().status,1)
                    for name,key,value in (('quote','returns','str'),('echo','returns','str'),('echo','parameters',{'value':"Record['checked_pricing.core:Wrapper']"}),('echo','parameters',[])):
                        corrupted=copy.deepcopy(envelope);next(r for r in corrupted['payload']['exports']if r['selector']=='checked_pricing.core:'+name)['contract'][key]=value
                        if key=='returns' or type(value)is dict:
                            for row in corrupted['payload']['guards']['exports']:
                                if row['original_boundary']=='checked_pricing.core:'+name:row[key]=copy.deepcopy(value)
                            for row in corrupted['payload']['guards']['debug']:
                                if row['path']=='checked_pricing/core.py' and row['name']==name:row[key]=copy.deepcopy(value)
                        try:
                            write_payload(corrupted);r=self.check();self.assertEqual(r.status,2,r.to_dict());self.assertEqual([x.rule for x in r.tooling],['PAL001'])
                            if type(value)is not list:self.assertEqual(r.tooling[0].origin,'installed distribution derivation')
                            out=self.base/('forged-'+mode+'-'+name+'-'+key+'-'+str(type(value).__name__));built=build_paths([self.consumer],root=self.consumer,output=out);self.assertEqual(built.status,2);self.assertFalse(out.exists())
                        finally:ep.write_bytes(ep_before);record.write_bytes(record_before)
                        self.assertEqual(self.check().status,1)
                    from pyalamode.standard_contracts import setup_contract
                    setup={**setup_contract('live_clock'),'path':next(r for r in envelope['payload']['exports']if r['selector']=='checked_pricing.core:quote')['contract']['path'],'line':2,'column':1,'phase':'ordinary module initialization','inputs':[],'input_evidence':'exact established source expressions; surrounding shell remains unchecked','output':'ClockCapability','allowed_operations':['now_ns']}
                    for label,key,value in (('evidence','source_evidence','checked functional module initialization; counterfeit evidence'),('failure','failures',['OSError']),('setup','setup_observations',[setup])):
                        corrupted=copy.deepcopy(envelope);module=next(r for r in corrupted['payload']['modules']if r['module']=='checked_pricing.core')
                        if key=='setup_observations':module[key]=value
                        else:module['initialization'][key]=value
                        try:
                            write_payload(corrupted);r=self.check();self.assertEqual(r.status,2,r.to_dict());self.assertEqual([x.rule for x in r.tooling],['PAL001']);self.assertEqual(r.tooling[0].origin,'installed distribution derivation')
                            out=self.base/('counterfeit-init-'+mode+'-'+label);built=build_paths([self.consumer],root=self.consumer,output=out);self.assertEqual(built.status,2);self.assertFalse(out.exists())
                        finally:ep.write_bytes(ep_before);record.write_bytes(record_before)
                        self.assertEqual(self.check().status,1)
                    corrupted=copy.deepcopy(envelope);p=corrupted['payload'];target='checked_pricing/core.py'
                    if mode=='exports':target=p['guards']['exports'][0]['public_boundary'].split(':')[0].replace('.','/')+'.py'
                    artifact=self.site/target;artifact_before=artifact.read_bytes();changed=artifact_before+b'\n# counterfeit derived artifact\n';artifact.write_bytes(changed)
                    p['artifacts'][target].update(sha256=hashlib.sha256(changed).hexdigest(),size=len(changed))
                    if target in p['guards']['generated_files']:p['guards']['generated_files'][target]=hashlib.sha256(changed).hexdigest()
                    for module in p['modules']:
                        if module['installed_path']==target:module['artifact_sha256']=hashlib.sha256(changed).hexdigest()
                    try:
                        write_payload(corrupted);r=self.check();self.assertEqual(r.status,2,r.to_dict());self.assertIn('derivation',r.tooling[0].origin)
                        out=self.base/('counterfeit-derived-'+mode);built=build_paths([self.consumer],root=self.consumer,output=out);self.assertEqual(built.status,2);self.assertFalse(out.exists())
                    finally:artifact.write_bytes(artifact_before);ep.write_bytes(ep_before);record.write_bytes(record_before)
                    self.assertEqual(self.check().status,1)
                finally:writer.unlink()
                self.assertEqual(self.check().status,0)

if __name__=='__main__':unittest.main()
