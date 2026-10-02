"""Research entrypoint. No installs, uploads, source merges or live deployment."""
import argparse,os,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent

def call(args):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
 subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,check=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['checks','replay']);p.add_argument('--output',type=Path);a=p.parse_args()
 if a.action=='checks':
  call(['tools/verify_manifest.py']);call(['-m','unittest','discover','-s','tests','-v'])
  with tempfile.TemporaryDirectory(prefix='NSS_Existence005_Checks_') as t:
   call(['tools/verify_results.py','--receipt',Path(t)/'score_check.json'])
  print('Research checks passed. This did not retrain or deploy a model.')
 else:
  if a.output is None:raise SystemExit('Replay needs a NEW --output directory outside this source package.')
  out=a.output.resolve()
  if out.exists() or out.is_relative_to(ROOT):raise SystemExit('Use a new directory outside the release.')
  out.mkdir(parents=True)
  call(['tools/verify_results.py','--replay','--out',out/'results','--receipt',out/'VERIFICATION.json'])
if __name__=='__main__':
 try:main()
 except subprocess.CalledProcessError as e:raise SystemExit(e.returncode)
