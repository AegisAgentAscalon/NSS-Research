"""Publish diagnostic independent NumPy scores with the original failure explicitly retained."""
from pathlib import Path
import argparse,os,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();root=Path(__file__).resolve().parent
out=Path(a.output).resolve()
if out.exists():raise SystemExit('Use a new output path; existing evidence cannot be overwritten.')
env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
print('Diagnostic rescoring only. The original whole-trajectory numerical gate remains failed.',flush=True)
subprocess.run([sys.executable,str(root/'analysis/PUBLISH_DIAGNOSTICS.py'),'--input',str(root/'primary'),'--output',str(out),'--config',str(root/'protocol/CONFIG.json')],cwd=root,env=env,check=True)
