#!/usr/bin/env python3
"""Verify physical and restored evidence against exact retained identities."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def verify():
 m=json.loads((ROOT/'MANIFEST.json').read_text());missing=[];errors=[]
 for rel,d in m['files'].items():
  p=(ROOT/rel).resolve()
  if not p.is_relative_to(ROOT):raise RuntimeError('INVALID_MANIFEST_PATH')
  if not p.is_file():missing.append(rel)
  elif p.stat().st_size!=d['bytes'] or sha(p)!=d['sha256']:errors.append(rel)
 lock=json.loads((ROOT/'audit/SOURCE_LOCK.json').read_text());source_errors=[]
 for rel,d in lock['files'].items():
  p=ROOT/rel
  if not p.exists() or p.stat().st_size!=d['bytes'] or sha(p)!=d['sha256']:source_errors.append(rel)
 result={'status':'PASS' if not(missing or errors or source_errors) else 'FAIL','manifest_files':len(m['files']),'source_lock_files':len(lock['files']),'missing':missing,'mismatched':errors,'source_errors':source_errors,'new_model_computations':0}
 print(json.dumps(result,indent=2))
 if result['status']!='PASS':raise SystemExit('Run RESTORE_EVIDENCE.py first; never overwrite a mismatched target silently.')
if __name__=='__main__':verify()
