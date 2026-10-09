"""installed_checked_quote_v1: exactly 12 public CLI check intervals/platform.

Use an already prepared installed-product CPython3.13.1 environment via --python.
Wheel build/install, consumer build and ordinary calls are untimed controls.
No intervals run without --measure; root releases measurement after freeze.
This stdlib controller never places a product checkout on a consumer import path.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import time

PROTOCOL='installed_checked_quote_v1'
SHAPES=('one_package','two_transitive_packages')
COMMANDS=[]
PARTIAL=None
PARTIAL_OWNER=None
TARGET_CODE='''import sys,platform,json,hashlib
from pathlib import Path
import pyalamode
from pyalamode.model import foundation_identities,runtime_environment
from pyalamode.project import runtime_error
assert runtime_error() is None
package=Path(pyalamode.__file__).parent
files={p.name:{"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in package.glob("*.py")}
print(json.dumps(dict(python=platform.python_version(),platform=sys.platform,machine=platform.machine(),executable=sys.executable,interpreter_sha256=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),product_artifacts=foundation_identities(),package_files=files,runtime_environment=runtime_environment())))
'''

def sha(raw):return hashlib.sha256(raw).hexdigest()

def run(python,args,cwd):
    env=dict(os.environ);env.pop('PYTHONPATH',None)
    return subprocess.run([python,*args],cwd=cwd,env=env,capture_output=True,check=False)

def record(p,cwd,kind,nanoseconds=None):
    row={'argv':p.args,'cwd':str(cwd),'kind':kind,'status':p.returncode}
    if nanoseconds is not None:row['nanoseconds']=nanoseconds
    for label,raw in (('stdout',p.stdout),('stderr',p.stderr)):
        row[label]={'bytes':len(raw),'sha256':sha(raw),'base64':base64.b64encode(raw).decode('ascii')}
    COMMANDS.append(row)
    fd=os.open(PARTIAL,os.O_WRONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'w',encoding='utf-8')as stream:
        stat=os.fstat(stream.fileno())
        if (stat.st_dev,stat.st_ino)!=PARTIAL_OWNER:raise RuntimeError('partial evidence ownership changed')
        stream.truncate(0)
        json.dump({'schema':1,'protocol':PROTOCOL,'status':'partial; commands captured before return-status/oracle checks','commands':COMMANDS},stream,indent=2,sort_keys=True);stream.write('\n');stream.flush()
    return len(COMMANDS)-1

def checked(python,args,cwd):
    p=run(python,args,cwd);record(p,cwd,'untimed correctness/input capture')
    if p.returncode:raise RuntimeError(str(args)+': '+repr(p.stdout)+repr(p.stderr))
    return p

def source(root,package,text,characterized_parent=False):
    (root/package).mkdir(parents=True)
    (root/package/'__init__.py').write_text('# mode: fun\n' if characterized_parent else '"""Ordinary parent initialization; no static purity claim."""\n')
    (root/package/'core.py').write_text('# mode: fun\n'+text)
    (root/package/'ordinary.py').write_text('def ordinary(value):\n    return value\n')

def source_map(area):
    return {str(p.relative_to(area)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in area.rglob('*') if p.is_file() and (p.suffix=='.py' or p.name=='pyproject.toml') and not any(x in {'dist','built','.pyalamode-cache','__pycache__'} for x in p.relative_to(area).parts)}

def installed_map(report):
    rows={}
    for name,receipt in report['distribution_inputs'].items():
        observed=receipt['observed']
        for key in ('metadata','authored_sources','artifacts','caches'):
            for label,row in observed[key].items():rows[name+'/'+key+'/'+label]=row
        for key in ('evidence','policy'):rows[name+'/'+key]=observed[key]
    return rows

def producer(python,root,name,package,text,exports,deps=(),characterized_parent=False):
    root.mkdir();source(root,package,text,characterized_parent)
    policy='[tool.pyalamode.distribution]\nschema=1\nname="'+name+'"\nversion="1.0.0"\npackages=["'+package+'"]\nexports='+json.dumps([package+'.core:'+n for n in exports])+'\n'
    for dep,owned in deps:policy+='\n[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="'+dep+'"\nversion="1.0.0"\npackages=["'+owned+'"]\n'
    (root/'pyproject.toml').write_text(policy)
    wheel=root/'dist'/(name.replace('-','_')+'-1.0.0-py3-none-any.whl')
    receipt=json.loads(checked(python,['-m','pyalamode','build','--wheel','--root',str(root),'--output',str(wheel),'--json'],root).stdout)
    checked(python,['-m','pip','install','--no-deps','--no-compile',str(wheel)],root)
    return {'wheel':str(wheel),'bytes':wheel.stat().st_size,'sha256':sha(wheel.read_bytes()),'members':receipt['distribution']['members'],'producer_coverage':receipt['coverage'],'analysis_counts':receipt['analysis_counts']}

def prepare(python,workspace,shape):
    area=workspace/shape;area.mkdir();wheels=[]
    if shape=='one_package':
        package='checked_scalar';name='checked-scalar'
        wheels.append(producer(python,area/'producer',name,package,'def quote(quantity:int)->int:\n    return quantity*30\ndef fee(value:int)->int:\n    return value+5\ndef label(value:int)->str:\n    return "scalar"\n',('quote','fee','label')))
        deps=((name,package),)
    else:
        wheels.append(producer(python,area/'base','checked-base','checked_base','def net(quantity:int)->int:\n    return quantity*20\ndef tax(value:int)->int:\n    return value//2\ndef label(value:int)->str:\n    return "base"\n',('net','tax','label'),characterized_parent=True))
        package='checked_transitive';name='checked-transitive'
        wheels.append(producer(python,area/'producer',name,package,'from checked_base.core import net,tax\ndef quote(quantity:int)->int:\n    subtotal=net(quantity)\n    return subtotal+tax(subtotal)\ndef fee(value:int)->int:\n    return value+5\ndef label(value:int)->str:\n    return "transitive"\n',('quote','fee','label'),(('checked-base','checked_base'),)))
        deps=(('checked-base','checked_base'),(name,package))
    consumer=area/'consumer';consumer.mkdir()
    (consumer/'application.py').write_text('from pyalamode import fun\nfrom '+package+'.core import quote\n@fun\ndef checked_total(quantity:int)->int:\n    return quote(quantity)\n')
    (consumer/'ordinary.py').write_text('def ordinary(value):\n    return value\n')
    policy=''
    for dep,owned in deps:policy+='[[tool.pyalamode.checked_dependencies]]\nschema=1\nname="'+dep+'"\nversion="1.0.0"\npackages=["'+owned+'"]\n'
    (consumer/'pyproject.toml').write_text(policy)
    built=area/'built';checked(python,['-m','pyalamode','build','--root',str(consumer),'--output',str(built),'--json'],consumer)
    call=checked(python,['-c','from application import checked_total; value=checked_total(40); assert type(value) is int and value==1200; print(value)'],built)
    if call.stdout.strip()!=b'1200':raise RuntimeError('ordinary value oracle failed')
    observed=json.loads(checked(python,['-m','pyalamode','check','--root',str(consumer),'--json'],consumer).stdout)
    return consumer,{'wheels':wheels,'source_before':source_map(area),'installed_before':installed_map(observed),'consumer_coverage':observed['coverage'],'analysis_counts_before':observed['analysis_counts'],'dependency_receipts':observed['distribution_inputs'],'ordinary_result':1200,'build_output':str(built),'dependency_count':len(deps)}

def main():
    global PARTIAL,PARTIAL_OWNER
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python',required=True,help='literal fresh installed consumer venv/bin/python; never resolve its symlink')
    parser.add_argument('--workspace',required=True,help='fresh outside setup directory')
    parser.add_argument('--output',required=True,help='fresh JSON observation output')
    parser.add_argument('--measure',action='store_true',help='only root may release these 12 intervals after freeze')
    args=parser.parse_args();python=os.path.abspath(args.python);workspace=Path(args.workspace).resolve();output=Path(args.output)
    PARTIAL=output.with_name(output.name+'.partial.json')
    if workspace.exists() or output.exists() or PARTIAL.exists() or PARTIAL.is_symlink():raise SystemExit('fresh workspace/output/partial evidence required')
    output.parent.mkdir(parents=True,exist_ok=True)
    with PARTIAL.open('x',encoding='utf-8')as stream:
        json.dump({'schema':1,'protocol':PROTOCOL,'status':'partial; no command yet','commands':[]},stream);stream.write('\n')
        stat=os.fstat(stream.fileno());PARTIAL_OWNER=(stat.st_dev,stat.st_ino)
    controller_before={'bytes':Path(__file__).stat().st_size,'sha256':sha(Path(__file__).read_bytes())}
    workspace.mkdir(parents=True);target_before=json.loads(checked(python,['-c',TARGET_CODE],workspace).stdout)
    rows=[]
    for shape in SHAPES:
        consumer,inventory=prepare(python,workspace,shape);intervals=[]
        if args.measure:
            for trial in range(3):
                for phase in ('cold','warm'):
                    if phase=='cold':shutil.rmtree(consumer/'.pyalamode-cache',ignore_errors=True)
                    start=time.perf_counter_ns();p=run(python,['-m','pyalamode','check','--root',str(consumer),'--json'],consumer);duration=time.perf_counter_ns()-start
                    command=record(p,consumer,'timed check '+shape+' '+phase+' '+str(trial),duration);data=json.loads(p.stdout)
                    if p.returncode or not data['verified'] or data['status']!=0:raise RuntimeError('timed check correctness oracle failed')
                    intervals.append({'trial':trial,'phase':phase,'nanoseconds':duration,'command':command,'analysis_counts':data['analysis_counts'],'owned_body_cache_hits':sum(f['cache_hit'] for f in data['files']),'report_bytes':len(p.stdout)})
        after=json.loads(checked(python,['-m','pyalamode','check','--root',str(consumer),'--json'],consumer).stdout)
        inventory.update(source_after=source_map(consumer.parent),installed_after=installed_map(after),analysis_counts_after=after['analysis_counts'])
        if inventory['source_before']!=inventory['source_after'] or inventory['installed_before']!=inventory['installed_after']:raise RuntimeError('fixture/installed bytes changed across intervals')
        rows.append({'shape':shape,'inventory':inventory,'intervals':intervals,'medians_nanoseconds':{phase:statistics.median(i['nanoseconds'] for i in intervals if i['phase']==phase) for phase in ('cold','warm')} if intervals else {}})
    target_after=json.loads(checked(python,['-c',TARGET_CODE],workspace).stdout);controller_after={'bytes':Path(__file__).stat().st_size,'sha256':sha(Path(__file__).read_bytes())}
    if target_before!=target_after or controller_before!=controller_after:raise RuntimeError('product/runtime/controller changed across observations')
    result={'protocol':PROTOCOL,'status':'measured' if args.measure else 'prepared only; no intervals','target_before':target_before,'target_after':target_after,'controller_before':controller_before,'controller_after':controller_after,'commands':COMMANDS,'rows':rows,'interval_count':sum(len(r['intervals']) for r in rows),'analysis_count_scope':'writer scan covers every relevant owned and installed source; fresh/cached body-file counts include ordinary files and are separate from selected function count; dependency edges count the static transitive source closure per file','timed_scope':'public CLI startup, passive installed/source IO, static checking, captured stdout/stderr and JSON serialization; installed ownership/writers/raw bytes are re-inspected','untimed_scope':'wheel build/install, consumer build/ordinary call, inventory/hashes/raw command encoding/oracles/JSON parsing and output','human_measurement':{'status':'UNMEASURED','participants':0,'attempts':0}}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x')as stream:json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')

if __name__=='__main__':main()
