#!/usr/bin/env python3
"""Independent NumPy reconstruction of retained evidence; no Torch, optimizer or new model forwards."""
import os,sys,json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Usage: python RESCORE.py /new/output/directory')
out=Path(sys.argv[1]).resolve()
if out.exists():raise SystemExit('Choose a new output directory; no historical result may be overwritten.')
out.mkdir(parents=True)
env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
with open(out/'stdout.log','wb') as f,open(out/'stderr.log','wb') as e:
 p=subprocess.run([sys.executable,str(ROOT/'source/scorer.py'),str(ROOT/'raw/primary'),str(out/'scores'),'--full'],stdout=f,stderr=e,env=env)
if p.returncode:raise SystemExit('Independent rescore failed; inspect '+str(out/'stderr.log'))
a=[]
for path in sorted((ROOT/'raw/primary/final_audit').iterdir()):
 if path.is_file():
  q=out/'scores'/path.name
  a.append({'file':path.name,'identical':q.exists() and path.read_bytes()==q.read_bytes(),'original_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
result={'status':'PASS' if all(x['identical'] for x in a) else 'FAIL','files':a,'torch_forwards':0,'optimizer_updates':0,'scope':'retained-array independent arithmetic and rescoring, not another adaptive replay'}
(out/'RESCORE_RECEIPT.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if result['status']!='PASS':raise SystemExit(1)
