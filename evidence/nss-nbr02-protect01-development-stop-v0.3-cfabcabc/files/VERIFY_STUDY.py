"""Verify delivered logical bytes and the frozen scientific source. No inference."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
m=json.loads((R/'MANIFEST.json').read_text());fail=[]
for row in m['files']:
 p=(R/row['path']).resolve()
 if not p.is_relative_to(R) or not p.is_file():fail.append({'path':row['path'],'error':'MISSING'});continue
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 if p.stat().st_size!=row['bytes'] or h.hexdigest()!=row['sha256']:fail.append({'path':row['path'],'error':'IDENTITY'})
for n in ['raw/primary/worker/records.bin','raw/replay/worker/records.bin','raw/primary/private/PLAN.json','raw/replay/private/PLAN.json','audit/SOURCE_LOCK.json','audit/REPLAY_COMPARISON.json','raw/primary/A0_AND_GUARDS_LOCK.json','REPORT.md','RETURN_TICKET.md']:
 if not (R/n).is_file():fail.append({'path':n,'error':'REQUIRED'})
lock=json.loads((R/'audit/SOURCE_LOCK.json').read_text())
for n,row in lock['files'].items():
 p=R/n
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:fail.append({'path':n,'error':'LOCKED_SOURCE'})
print(json.dumps({'status':'PASS' if not fail else 'FAIL','manifest_files':len(m['files']),'frozen_source_entries':len(lock['files']),'failures':fail,'numerical_reproduction_performed':False},indent=2));raise SystemExit(bool(fail))
