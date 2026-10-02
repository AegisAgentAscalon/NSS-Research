"""Independent NumPy-only scoring of retained evidence; no Torch or model execution."""
import argparse,subprocess,sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve()
if out.exists():raise SystemExit('Use a new output directory; retained scores are not overwritten.')
out.mkdir(parents=True)
cmd=[sys.executable,str(R/'source/scorer.py'),str(R/'raw/primary'),str(out),'--full']
r=subprocess.run(cmd)
if r.returncode:raise SystemExit(r.returncode)
match=[]
for f in (R/'raw/primary/final_audit').iterdir():
    if f.suffix in ('.csv','.json') and f.name!='AUDIT.json':
        g=out/f.name
        same=hashlib.sha256(g.read_bytes()).digest()==hashlib.sha256(f.read_bytes()).digest()
        match.append({'file':f.name,'byte_identical':same})
if not all(x['byte_identical'] for x in match):raise SystemExit('Re-score mismatch; inspect the new directory; no baseline changed.')
# The captured independent audit precedes CLOSE. Validate, rather than ignore,
# the sole additional terminal log event in a later independent re-score.
old=json.loads((R/'raw/primary/final_audit/AUDIT.json').read_text())
new=json.loads((out/'AUDIT.json').read_text())
last=json.loads((R/'raw/primary/worker/events.jsonl').read_text().splitlines()[-1])
entry=last['record']
if entry['event']!='WORKER_FINISH' or entry['previous']!=old['log']['chain'] or last['sha256']!=new['log']['chain']:
    raise SystemExit('Unexpected terminal log difference')
if new['log']['events']!=old['log']['events']+1 or entry['counts']!=json.loads((R/'raw/primary/COUNTERS.json').read_text())['counts']:
    raise SystemExit('Terminal event/count mismatch')
normalized=json.loads(json.dumps(new));normalized['log']['events']=old['log']['events'];normalized['log']['chain']=old['log']['chain']
if normalized!=old:raise SystemExit('Nonterminal audit metadata changed')
print(json.dumps({'status':'PASS','matched_files':match,'terminal_finish_event_independently_validated':True,'audit_numeric_fields_identical':True,'additional_model_calls':0},indent=2))
