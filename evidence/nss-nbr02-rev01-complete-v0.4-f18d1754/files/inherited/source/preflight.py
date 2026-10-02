"""Source-bound static, seed, and deterministic pre-heldout input checks. No model execution."""
import os,sys,json,hashlib,zipfile,re,time,importlib.metadata
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'protocol';manifest=json.loads((p/'MANIFEST.json').read_text())
checks=[]
for r in manifest['files']:
 f=p/r['path'];checks.append({'file':r['path'],'ok':f.exists() and len(f.read_bytes())==r['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']})
assert all(x['ok'] for x in checks)
recipe=json.loads((p/'SEED_RECIPE.json').read_text());seeds=recipe['seeds'];assert len(seeds)==120 and len(set(seeds.values()))==120
for label,v in seeds.items():assert v==int.from_bytes(hashlib.sha256((recipe['namespace']+'|'+label).encode()).digest()[:8],'big')
# Scope: previous unrelated directly readable proposal/evidence text. Current proposal and its source-derived repetitions excluded explicitly.
needle=set(str(s) for s in seeds.values());hits=[];n=0;nb=0;archives=[]
for z in Path('/mnt/data').glob('*.zip'):
 if z.name.startswith(('NSS_NBR02_DC01_Integrated_Review','NSS_Failure_First')):continue
 try:
  with zipfile.ZipFile(z) as f:
   eligible=[x for x in f.infolist() if x.filename.endswith(('.json','.md','.py','.csv','.txt')) and x.file_size<8*1024**2]
   for x in eligible:
    data=f.read(x);n+=1;nb+=len(data)
    text=data.decode('utf8',errors='ignore')
    # Current seed namespace can occur in archived forward references; record it rather than assert global uniqueness.
    found=needle.intersection(re.findall(r'(?<![0-9])[0-9]{10,20}(?![0-9])',text))
    for v in found:hits.append({'archive':z.name,'member':x.filename,'seed':v,'namespace_present':recipe['namespace'] in text})
   archives.append({'archive':z.name,'text_members':len(eligible)})
 except (zipfile.BadZipFile,EOFError) as e:archives.append({'archive':z.name,'unavailable':type(e).__name__})
if hits:raise RuntimeError('HISTORICAL_SEED_OVERLAP:'+repr(hits[:3]))
env={'python':sys.version,'numpy':importlib.metadata.version('numpy'),'torch':importlib.metadata.version('torch'),'cpu_affinity':sorted(os.sched_getaffinity(0)),'memory_max':Path('/sys/fs/cgroup/memory.max').read_text().strip(),'cpu_max':Path('/sys/fs/cgroup/cpu.max').read_text().strip()}
(ROOT/'audit/SEED_AND_SOURCE_PREFLIGHT.json').write_text(json.dumps({'manifest_checks':checks,'direct_seed_count':120,'historical_text_members':n,'historical_text_bytes':nb,'hits':hits,'archives':archives,'limitations':['Nested compressed evidence, binary records, unknown historical RNG draws not scanned','Different seed literals do not prove PRNG or scientific independence'],'environment':env},indent=2))
# Independently validate the full initial/development schedule before any main fit. No held-out labels/fillers generated.
from driver import init,order,labels,fillers
from auditor import verify_plan
import numpy as np
plan={'targets':{},'sessions':{},'heldout_generated':False}
for group in ('old','dev'):plan['targets'].update(labels(group)[0])
for fit in range(4):
 tx=[{'cue':c,'target':plan['targets'][c],'fillers':[]} for c in order(seeds[f'order/main/{fit}'],100)[0]]
 plan['sessions'][f'initial{fit}']={'phase':'initial','fit':fit,'transactions':tx}
for base,(f,c) in enumerate([(8,4),(9,5),(10,0),(11,1)]):
 for d in (0,8,32):
  for rev in (0,1):
   tx=[{'cue':cc,'target':plan['targets'][cc]^int(rev and i>=3 and cc==f),'fillers':fillers(cc,f'filler/base/{base:02}/trial/{i}',d)} for i,cc in enumerate((f,c,f,f,c,f),1)]
   plan['sessions'][f'dev{base}/{d}/{rev}']={'phase':'development','fit':-1,'base':base,'focal':f,'protected':c,'delay':d,'reversal':rev,'transactions':tx}
count=verify_plan(plan,seeds,plan['targets']);(ROOT/'audit/PREFIT_INPUT_CHECK.json').write_text(json.dumps({'checked_transactions':count,'status':'PASS','heldout_generated':False,'identity':hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()},indent=2))
print(json.dumps({'status':'PASS','text_members':n,'prefit_transactions':count,'environment':env}),flush=True)
