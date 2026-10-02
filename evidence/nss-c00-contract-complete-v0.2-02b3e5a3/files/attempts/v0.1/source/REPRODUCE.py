"""Run the fixed engineering harness into a new directory; no neural work."""
from pathlib import Path
import argparse,subprocess,sys,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
root=Path(__file__).resolve().parent.parent; dest=args.out.resolve()
if dest.exists():raise SystemExit('Use a new output directory; evidence must not be overwritten.')
dest.mkdir(parents=True)
for rel,ident in json.loads((root/'protocol/SOURCE_LOCK.json').read_text())['files'].items():
    data=(root/rel).read_bytes()
    if hashlib.sha256(data).hexdigest()!=ident['sha256']:raise SystemExit('Source changed: '+rel)
for passid in ('primary','replay'):
    inp=dest/(passid+'_inputs')
    subprocess.run([sys.executable,str(root/'source/build_cases.py'),str(inp)],check=True)
    subprocess.run([sys.executable,str(root/'source/run.py'),str(inp),str(dest/passid)],check=True)
    subprocess.run([sys.executable,str(root/'source/check.py'),str(inp),str(dest/passid),str(dest/(passid+'_scores'))],check=True)
excluded={'RESOURCE.json'}
left={str(x.relative_to(dest/'primary')):x for x in (dest/'primary').rglob('*')if x.is_file() and x.name not in excluded}
right={str(x.relative_to(dest/'replay')):x for x in (dest/'replay').rglob('*')if x.is_file() and x.name not in excluded}
assert left.keys()==right.keys()
assert all(left[k].read_bytes()==right[k].read_bytes() for k in left)
for x in (dest/'primary_scores').iterdir():assert x.read_bytes()==(dest/'replay_scores'/x.name).read_bytes()
print('Fresh deterministic contract replay passed. No model training or inference.')
