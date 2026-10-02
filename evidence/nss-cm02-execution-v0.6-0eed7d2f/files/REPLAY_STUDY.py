"""Explicit, separately budgeted reproduction of main capture; never edits delivered evidence.
This convenience driver was syntax/CLI checked, not used for a third post-delivery neural run.
"""
from __future__ import annotations
import argparse,json,os,shutil,subprocess,sys,time
from pathlib import Path

def main()->None:
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--workdir',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent;work=a.workdir.resolve();base=a.baseline.resolve()
 if work.exists() or work.is_relative_to(root):raise ValueError('Use a new workdir outside the delivered study')
 env=dict(os.environ,CM02_BASELINE=str(base),PYTHONHASHSEED='0',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 subprocess.run([sys.executable,str(root/'VERIFY_STUDY.py'),'--baseline',str(base)],env=env,check=True)
 work.mkdir(parents=True)
 for folder in ('src','protocol'):shutil.copytree(root/folder,work/folder,ignore=shutil.ignore_patterns('__pycache__'))
 for folder in ('audit','logs','raw','failed_attempts'):(work/folder).mkdir()
 now=time.time()
 (work/'audit/SESSION_START.json').write_text(json.dumps({'budget_start_unix':now,'authorization':'Explicit invocation of REPLAY_STUDY.py; separate new reproduction, not extension of archived study'}))
 (work/'audit/GLOBAL_FORWARD_LEDGER.json').write_text(json.dumps({'attempted':0}))
 (work/'REPRODUCTION_SCOPE.json').write_text(json.dumps({'original_delivered_attempts':5995,'original_evidence_immutable':True,'new_reproduction_forward_bound':1800,'reuse_existing_model_exports':True,'training':False},indent=2))
 run=work/'raw/main/reproduction_run'
 commands=[('generate','generate.py',['--kind','main','--output',str(run/'input')]),
  ('capture','capture.py',['--kind','main','--input',str(run/'input'),'--output',str(run/'capture')]),
  ('score','score.py',['--input',str(run/'input'),'--capture',str(run/'capture'),'--output',str(run/'scores')]),
  ('compare','compare.py',['--a',str(root/'raw/main/capture_run'),'--b',str(run),'--output',str(work/'audit/REPRODUCTION_COMPARE.json')])]
 for name,script,args in commands:
  subprocess.run([sys.executable,str(work/'src/run_stage.py'),'--name',name,'--',sys.executable,str(work/'src'/script),*args],env=env,check=True)
 total=json.loads((work/'audit/GLOBAL_FORWARD_LEDGER.json').read_text())['attempted']
 if total>1800:raise AssertionError('Main reproduction exceeded its source-derived forward bound')
 print('Main reproduction completed. Original study and its 5,995-attempt ledger were not changed.')
if __name__=='__main__':main()
