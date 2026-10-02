"""Re-score the retained completed prefix using NumPy only; zero model updates."""
from pathlib import Path
import argparse,subprocess,sys,os,json,hashlib
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();out=Path(args.output).resolve()
if out.exists():raise SystemExit('Use a new output directory; preserve previous audit results.')
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
out.mkdir(parents=True)
with open(out/'stdout.log','w') as a,open(out/'stderr.log','w') as b:
 result=subprocess.run([sys.executable,str(R/'source/scorer.py'),str(R/'raw/primary'),str(out/'scores'),'--full'],stdout=a,stderr=b,env=env)
if result.returncode:raise SystemExit('Independent scorer failed. Preserve '+str(out))
expected=R/'raw/primary/final_audit';got=out/'scores';matches=[]
for f in sorted(expected.iterdir()):
 if f.suffix=='.csv' or f.name=='DECISIONS.json':
  if f.read_bytes()!=(got/f.name).read_bytes():raise SystemExit('SCORE_BYTE_MISMATCH:'+f.name)
  matches.append(f.name)
a=json.loads((expected/'AUDIT.json').read_text());b=json.loads((got/'AUDIT.json').read_text())
for key in a:
 if key!='log' and a[key]!=b[key]:raise SystemExit('AUDIT_FIELD_MISMATCH:'+key)
for key in ['intents','commits','unknown_attempts']:
 if a['log'][key]!=b['log'][key]:raise SystemExit('AUDIT_ATTEMPT_MISMATCH:'+key)
lines=(R/'raw/primary/worker/events.jsonl').read_text().splitlines();footer=json.loads(lines[-1]);rec=footer['record']
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
counts=json.loads((R/'raw/primary/COUNTERS.json').read_text())['counts']
if not (rec['event']=='WORKER_FINISH' and rec['sequence']==a['log']['events']+1==b['log']['events'] and rec['previous']==a['log']['chain'] and rec['counts']==counts and hashlib.sha256(canon(rec)).hexdigest()==footer['sha256']==b['log']['chain']):raise SystemExit('UNEXPECTED_AUDIT_LOG_SUFFIX')
r={'status':'PASS','byte_equal_result_files':matches,'count':len(matches),'independent_numerical_audit':'PASS','single_postscore_worker_finish_verified':True,'model_forwards':0,'optimizer_updates':0}
(out/'RESULT.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
