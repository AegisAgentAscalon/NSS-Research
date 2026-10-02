"""Verify delivered bytes, not scientific qualification. No Torch import or model work."""
from pathlib import Path
import hashlib,json,sys

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def main():
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());bad=[];missing=[];total=0
 for e in manifest['files']:
  p=root/e['path']
  if not p.resolve().is_relative_to(root):raise RuntimeError('Escaping manifest path')
  if not p.is_file():missing.append(e['path']);continue
  if p.stat().st_size!=e['bytes'] or digest(p)!=e['sha256']:bad.append(e['path'])
  total+=p.stat().st_size
 lock=json.loads((root/'SOURCE_LOCK.json').read_text())
 for e in lock['files']:
  p=root/e['path']
  if not p.is_file() or p.stat().st_size!=e['bytes'] or digest(p)!=e['sha256']:bad.append('SOURCE_LOCK:'+e['path'])
 result={'manifest_payloads':len(manifest['files']),'logical_bytes':total,'source_lock_files':len(lock['files']),'missing':missing,'mismatched':bad,'integrity_pass':not missing and not bad,'scientific_qualification':'NOT_QUALIFIED','original_whole_trajectory_numeric_gate':'FAILED_UNCHANGED','note':'Run RESTORE_EVIDENCE.py first for omitted numeric targets/replay aliases. Passing hashes is not numerical qualification.'}
 print(json.dumps(result,indent=2))
 if missing or bad:sys.exit(1)
if __name__=='__main__':main()
