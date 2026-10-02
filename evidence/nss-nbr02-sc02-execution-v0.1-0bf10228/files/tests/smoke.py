from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from support import *
from runner import execute,POLICIES
from fixture_factory import episode
import traceback
setup();m,mid=load(8801)
rows=[]
for n in [8,32,128]:
 for fam in ['reuse','churn','resume','revisions','sweep','oversize']:
  ep=episode(n,932101,fam)
  for pol in POLICIES:
   try:
    out=execute(ep,m,mid,pol,audit=True)
    assert out['numeric_violations']==0 and out['changed_classes']==0,(n,fam,pol,out['max_abs'],out['numeric_violations'])
    assert out['final_model_hash']==mid
    rows.append({k:v for k,v in out.items()if k not in ['observations','trace']})
   except Exception:
    save(ROOT/'failures'/'prelock_smoke.json',{'completed':rows,'n':n,'family':fam,'policy':pol,'traceback':traceback.format_exc()})
    raise
  print(n,fam,[(r['policy'],round(r['core_seconds']*1000,2),r['stats'].get('reader_calls',0),r['stats'].get('intermediate_hits',0))for r in rows[-5:]],flush=True)
save(ROOT/'development'/'smoke.json',{'status':'PASS','rows':rows,'runtime':runtime()})
