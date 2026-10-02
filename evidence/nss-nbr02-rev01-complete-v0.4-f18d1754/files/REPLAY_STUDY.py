"""Explicit separate adaptive reproduction; never extends the archived execution ledger."""
import argparse,subprocess,sys,shutil,json,time
from pathlib import Path
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,help='New independent reproduction directory; source/data recipes are copied here.');a=p.parse_args();out=Path(a.output).resolve()
if out.exists():raise SystemExit('Output must not already exist.')
out.mkdir(parents=True)
for name in ('source','protocol'):shutil.copytree(R/name,out/name)
(out/'audit').mkdir()
for name in ('SOURCE_LOCK.json','HISTORICAL_SUMMARY.json'):shutil.copy2(R/'audit'/name,out/'audit'/name)
(out/'audit/START.json').write_text(json.dumps({'epoch':time.time(),'new_separate_reproduction':True,'parent_evidence_read_only':str(R)},indent=2))
code=subprocess.call([sys.executable,str(out/'source/supervise.py'),'primary'])
result=json.loads((out/'audit/supervisor_primary/RESULT.json').read_text())
if code or result['returncode']:raise SystemExit('Reproduction stopped; preserve its new ledger and evidence.')
print(json.dumps({'status':'SEPARATE_REPRODUCTION_FINISHED','new_directory':str(out),'parent_ledger_unchanged':True,'counts':json.loads((out/'raw/primary/COUNTERS.json').read_text())},indent=2))
