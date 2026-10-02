"""Independent NumPy rescore of retained evidence; no training or Torch forward calls."""
from pathlib import Path
import subprocess,sys,hashlib,json,argparse
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
if out.exists() and any(out.iterdir()):raise SystemExit('Output must be new or empty; archived results will not be overwritten.')
out.mkdir(parents=True,exist_ok=True)
r=subprocess.run([sys.executable,str(ROOT/'source/scorer.py'),str(ROOT/'raw/primary'),str(out),'--full'],capture_output=True,text=True)
(out/'rescore.stdout').write_text(r.stdout);(out/'rescore.stderr').write_text(r.stderr)
if r.returncode:raise SystemExit(r.returncode)
checks=[]
for f in sorted((ROOT/'raw/primary/final_audit').iterdir()):
 if f.suffix in ('.json','.csv'):
  b=(out/f.name).read_bytes();checks.append({'file':f.name,'equal':b==f.read_bytes(),'sha256':hashlib.sha256(b).hexdigest()})
receipt={'status':'PASS' if all(c['equal'] for c in checks) else 'FAIL','checks':checks,'new_model_calls':0,'new_optimizer_updates':0}
(out/'RELOCATION_COMPARISON.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
if receipt['status']!='PASS':raise SystemExit(2)
