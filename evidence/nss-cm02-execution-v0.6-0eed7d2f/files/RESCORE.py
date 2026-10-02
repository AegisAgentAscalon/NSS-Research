"""Re-score all completed main and inherited fixture evidence without model inference."""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path

def main()->None:
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent;out=a.output.resolve();base=a.baseline.resolve()
 if out.exists():raise FileExistsError('Use a new output directory; existing evidence is never overwritten')
 if out.is_relative_to(root):raise ValueError('Place re-score outputs outside the immutable delivered study')
 env=dict(os.environ,CM02_BASELINE=str(base),PYTHONHASHSEED='0',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 subprocess.run([sys.executable,str(root/'VERIFY_STUDY.py'),'--baseline',str(base)],env=env,check=True)
 out.mkdir(parents=True);checks=[]
 for name,code,evidence in [('main',root,root/'raw/main/capture_run'),('fixture',root/'failed_attempts/NSS_CM02_Execution_v0.5',root/'failed_attempts/NSS_CM02_Execution_v0.5/raw/fixture/capture_run')]:
  command=[sys.executable,str(code/'src/score.py'),'--input',str(evidence/'input'),'--capture',str(evidence/'capture'),'--output',str(out/name)]
  subprocess.run(command,env=env,check=True)
  for f in (evidence/'scores').iterdir():
   if f.is_file():
    q=out/name/f.name
    if f.read_bytes()!=q.read_bytes():raise AssertionError('Re-score differs: '+name+'/'+f.name)
    checks.append({'file':name+'/'+f.name,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
 receipt={'status':'PASS_RELOCATABLE_INDEPENDENT_RESCORING','byte_identical_files':len(checks),'files':checks,'new_model_forwards':0,'new_scientific_samples':0}
 (out/'RESCORE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
