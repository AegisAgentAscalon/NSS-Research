"""Recompute independent numerical audit/scores; zero Torch models or learning updates."""
from pathlib import Path
import subprocess,sys,hashlib,json,argparse,os
R=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args();out=a.output.resolve()
if out.exists() and any(out.iterdir()):raise SystemExit('Output must be new or empty')
if not (R/'raw/primary/worker/records.bin').is_file():raise SystemExit('Run RESTORE_EVIDENCE.py first')
out.mkdir(parents=True,exist_ok=True)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
r=subprocess.run([sys.executable,str(R/'source/scorer.py'),str(R/'raw/primary'),str(out),'--full'],capture_output=True,text=True,env=env)
(out/'rescore.stdout').write_text(r.stdout);(out/'rescore.stderr').write_text(r.stderr)
if r.returncode:raise SystemExit(r.returncode)
checks=[]
for f in sorted((R/'raw/primary/final_audit').iterdir()):
 if f.suffix in ('.json','.csv'):
  b=(out/f.name).read_bytes();checks.append({'file':f.name,'equal':b==f.read_bytes(),'sha256':hashlib.sha256(b).hexdigest()})
receipt={'status':'PASS' if all(x['equal'] for x in checks) else 'FAIL','checks':checks,'new_model_calls':0,'new_optimizer_updates':0}
(out/'RELOCATION_COMPARISON.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
if receipt['status']!='PASS':raise SystemExit(2)
