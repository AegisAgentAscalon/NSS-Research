from pathlib import Path
import sys,time,traceback
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from support import *
from runner import execute,POLICIES
setup();start=time.perf_counter();done=[];existing=[]
for seed in [942201,942202]:
 for ms in [8801,8802,8804]:
  m=None;mid=None
  for p in sorted((ROOT/'fixtures').glob(f'n128_s{seed}_*.json')):
   ep=json.loads(p.read_text())
   for variant in POLICIES:
    dest=ROOT/'results/episodes'/f'{ep["id"]}_m{ms}_{variant}.json'
    if dest.exists():existing.append({'file':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()});continue
    if m is None:m,mid=load(ms)
    out=execute(ep,m,mid,variant,audit=True,snap_dir=(ROOT/'results'/'snapshots')if ms==8801 and ep['family']=='resume'and variant in('P','I')else None)
    out['model_seed']=ms;out['runtime']=runtime();out['operational_completion']='inference-only continuation after caller interruption'
    save(dest,out);done.append({'file':dest.name,'numeric_violations':out['numeric_violations'],'changed_classes':out['changed_classes']})
    print(dest.name,'completed',flush=True)
    if time.perf_counter()-start>180 or runtime()['peak_rss_bytes']>2*1024**3:raise RuntimeError('RESOURCE_GUARD')
# Exact pre-existing hashes remain unchanged.
for d in existing:assert hashlib.sha256((ROOT/'results/episodes'/d['file']).read_bytes()).hexdigest()==d['sha256']
save(ROOT/'results/main_n128_completion.json',{'status':'COMPLETE','preexisting':existing,'new_conditions':done,'runtime':runtime(),'elapsed_seconds':time.perf_counter()-start,'optimizer_applications':0})
