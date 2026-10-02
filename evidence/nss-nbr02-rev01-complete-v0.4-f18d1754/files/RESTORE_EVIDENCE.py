"""Restore only stored, losslessly encoded evidence bytes. No neural computation."""
import sys,json,hashlib,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'source'))
from envelope_codec import restore_records

def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()
def safe(s):
    p=(R/s).resolve()
    if not p.is_relative_to(R):raise ValueError('Invalid restoration path')
    return p
m=json.loads((R/'DELIVERY_MAP.json').read_text())
for row in m['encoded_records']:
    target=safe(row['target']);blob=safe(row['payload'])
    if target.exists():
        if digest(target)!=row['sha256']:raise SystemExit('Existing target differs; preserve and inspect: '+str(target))
        continue
    if digest(blob)!=row['payload_sha256']:raise SystemExit('Payload checksum mismatch')
    target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_suffix('.restoring')
    restore_records(blob.read_bytes(),tmp)
    if digest(tmp)!=row['sha256']:
        raise SystemExit('Restoration byte mismatch. The captured codec uses zlib1.3.1; retain the temporary bytes for diagnosis.')
    tmp.replace(target)
remaining=list(m['aliases'])
while remaining:
    progress=False
    for row in remaining[:]:
        src=safe(row['source']);dst=safe(row['target'])
        if not src.exists():continue
        if digest(src)!=row['sha256']:raise SystemExit('Alias source mismatch')
        dst.parent.mkdir(parents=True,exist_ok=True)
        if dst.exists():
            if digest(dst)!=row['sha256']:raise SystemExit('Existing alias target mismatch')
        else:shutil.copyfile(src,dst)
        remaining.remove(row);progress=True
    if not progress:raise SystemExit('Missing alias source or dependency loop')
print(json.dumps({'status':'RESTORED','encoded_records':len(m['encoded_records']),'exact_aliases':len(m['aliases']),'model_calls':0},indent=2))
