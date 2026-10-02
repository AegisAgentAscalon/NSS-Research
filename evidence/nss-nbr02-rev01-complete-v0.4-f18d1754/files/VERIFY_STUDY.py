"""Verify every manifest-listed byte and required scientific artifact."""
import hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
m=json.loads((R/'MANIFEST.json').read_text());fail=[]
for row in m['files']:
    p=(R/row['path']).resolve()
    if not p.is_relative_to(R) or not p.is_file():fail.append({'path':row['path'],'error':'MISSING'});continue
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    if p.stat().st_size!=row['bytes'] or h.hexdigest()!=row['sha256']:fail.append({'path':row['path'],'error':'IDENTITY'})
for rel in ('raw/primary/private/PLAN.json','raw/replay/private/PLAN.json','raw/primary/worker/records.bin','raw/replay/worker/records.bin','audit/SOURCE_LOCK.json','audit/REPLAY_VERIFICATION.json','raw/primary/final_audit/DECISIONS.json','DREAM_MAINTENANCE.md','attempts/v0.3/STATUS.json'):
    if not (R/rel).exists():fail.append({'path':rel,'error':'REQUIRED_MISSING'})
lock=json.loads((R/'audit/SOURCE_LOCK.json').read_text())
for rel,rec in lock['files'].items():
    p=R/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=rec['sha256']:fail.append({'path':rel,'error':'FROZEN_SOURCE'})
print(json.dumps({'status':'PASS' if not fail else 'FAIL','manifest_files':len(m['files']),'frozen_source_entries':len(lock['files']),'failures':fail,'numerical_reproduction_performed':False},indent=2))
raise SystemExit(bool(fail))
