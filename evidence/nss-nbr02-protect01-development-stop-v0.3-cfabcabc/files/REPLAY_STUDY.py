"""Explicit new reproduction in another directory. Never overwrites this closed ledger.
This performs learning again and needs a separately authorized budget.
"""
import argparse,os,json,sys,shutil,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--destination',required=True);p.add_argument('--authorize-new-learning',action='store_true');a=p.parse_args()
if not a.authorize_new_learning:raise SystemExit('This reproduces actual learning; explicitly authorize its new budget first.')
d=Path(a.destination).resolve()
if d.exists() or d.is_relative_to(R):raise SystemExit('Choose a new external destination.')
d.mkdir(parents=True)
for n in ['source','protocol','program']:shutil.copytree(R/n,d/n)
(d/'audit').mkdir();(d/'raw').mkdir()
for n in ['SOURCE_LOCK.json','HISTORICAL_SUMMARY.json']:shutil.copy2(R/'audit'/n,d/'audit'/n)
(d/'audit/START.json').write_text(json.dumps({'epoch':time.time(),'separate_reproduction':True,'archived_attempts_not_reset':True}))
env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
r=subprocess.run([sys.executable,str(d/'source/supervise.py'),'reproduction'],env=env)
raise SystemExit(r.returncode)
