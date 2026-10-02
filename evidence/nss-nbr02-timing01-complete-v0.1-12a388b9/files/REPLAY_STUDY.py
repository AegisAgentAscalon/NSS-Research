"""Optional new, explicitly separate adaptive reproduction. Not invoked to produce this delivery."""
from pathlib import Path
import argparse,shutil,json,time,subprocess,sys
R=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--execute-new-learning-run',action='store_true');a=p.parse_args()
if not a.execute_new_learning_run:raise SystemExit('Requires --execute-new-learning-run; this performs new parameter updates, not byte restoration.')
out=a.output.resolve()
if out==R or out.is_relative_to(R):raise SystemExit('New reproduction must be outside the historical study')
if out.exists() and any(out.iterdir()):raise SystemExit('Output must be new or empty')
out.mkdir(parents=True,exist_ok=True)
for d in ('source','protocol'):shutil.copytree(R/d,out/d,ignore=shutil.ignore_patterns('__pycache__'))
(out/'audit').mkdir();(out/'raw').mkdir()
for rel in ('SOURCE_LOCK.json','HISTORICAL_SUMMARY.json'):shutil.copyfile(R/'audit'/rel,out/'audit'/rel)
(out/'audit/START.json').write_text(json.dumps({'epoch':time.time(),'separate_reproduction':True,'historical_ledger_unchanged':True}))
raise SystemExit(subprocess.call([sys.executable,str(out/'source/supervise.py'),'reproduction']))
