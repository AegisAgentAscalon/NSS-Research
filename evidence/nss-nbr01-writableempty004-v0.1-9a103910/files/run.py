"""User entrypoint: keep packaged evidence/checkpoints unchanged.
Verification and reproduction run in a temporary COPY and save new receipts
beside the package. No package install, download or external service is used.
"""
from pathlib import Path
import argparse,subprocess,sys,tempfile,shutil,os,datetime
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('action',choices=('checks','verify','resume','reproduce-one','train'))
p.add_argument('--output',type=Path,help='Required for train; optional output directory for receipts/logs')
a=p.parse_args();env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
if a.action=='checks':
 for args in [('tools/verify_manifest.py',),('-m','unittest','discover','-s','tests','-v')]:
  code=subprocess.call([sys.executable,*args],cwd=ROOT,env=env)
  if code:raise SystemExit(code)
 raise SystemExit(0)
if a.action=='train':
 if a.output is None:p.error('train requires --output pointing outside the release directory')
 out=a.output.resolve()
 if out==ROOT or out.is_relative_to(ROOT):p.error('Training output must be outside the release')
 from nbr01_empty.train import train
 for seed in range(301,306):
  for kind in ('replay','contract','local_empty'):train(ROOT,out,kind,seed,seed+300)
 raise SystemExit(0)
out=(a.output or ROOT.parent/(ROOT.name+'_run_outputs')).resolve()
if out==ROOT or out.is_relative_to(ROOT):p.error('Receipts must be outside the release')
runout=out/(a.action+'_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));runout.mkdir(parents=True,exist_ok=False)
command,receipt={
 'verify':(['tools/verify_results.py'],'INDEPENDENT_VERIFICATION.json'),
 'resume':(['tools/verify_resume.py','verify'],'RESUME_VERIFICATION.json'),
 'reproduce-one':(['tools/reproduce_training.py'],'TRAINING_REPRODUCTION.json')
}[a.action]
with tempfile.TemporaryDirectory(prefix='nbr004-') as tmp:
 work=Path(tmp)/ROOT.name
 shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 with (runout/'execution.log').open('w') as log:
  result=subprocess.run([sys.executable,'-u',*command],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
 if (work/'evidence'/receipt).exists() and result.returncode==0:shutil.copy2(work/'evidence'/receipt,runout/receipt)
 print(f'Exit {result.returncode}. New log/receipt directory: {runout}')
 raise SystemExit(result.returncode)
