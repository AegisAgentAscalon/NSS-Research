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
    if f.suffix in ('.csv','.json'):
        g=out/f.name
        same=hashlib.sha256(g.read_bytes()).digest()==hashlib.sha256(f.read_bytes()).digest()
        match.append({'file':f.name,'byte_identical':same})
if not all(x['byte_identical'] for x in match):raise SystemExit('Re-score mismatch; inspect the new directory; no baseline changed.')
print(json.dumps({'status':'PASS','matched_files':match,'additional_model_calls':0},indent=2))
