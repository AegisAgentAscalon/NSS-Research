"""Verify the delivered study bytes, frozen local source and attempt ledger (no models)."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path

def digest(p:Path)->str:
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main()->None:
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--baseline',type=Path,help='Optional extracted Q010 recovery root to verify numerical dependency hashes');a=ap.parse_args()
 root=Path(__file__).resolve().parent;m=json.loads((root/'MANIFEST.json').read_text());count=0
 for rel,meta in m['files'].items():
  p=(root/rel).resolve()
  if not p.is_relative_to(root) or not p.is_file():raise ValueError('Missing/unsafe member: '+rel)
  if p.stat().st_size!=meta['bytes'] or digest(p)!=meta['sha256']:raise ValueError('Integrity mismatch: '+rel)
  count+=1
 lock=json.loads((root/'protocol/SOURCE_LOCK.json').read_text())
 for rel,h in lock['study_files'].items():
  if digest(root/rel)!=h:raise ValueError('Frozen source mismatch: '+rel)
 dep=0
 if a.baseline:
  base=a.baseline.resolve()
  for rel,h in lock['baseline_files'].items():
   if digest(base/rel)!=h:raise ValueError('Dependency mismatch: '+rel)
   dep+=1
 attempts=0;acknowledged=0;ledgers=[]
 for prefix in ('raw','failed_attempts'):
  for p in (root/prefix).rglob('ATTEMPTS.json'):
   d=json.loads(p.read_text());attempts+=d['attempted'];acknowledged+=d['completed'];ledgers.append(str(p.relative_to(root)))
 recorded=json.loads((root/'audit/GLOBAL_FORWARD_LEDGER.json').read_text())['attempted']
 if attempts!=recorded or attempts!=5995 or attempts>6000:raise ValueError('Attempt accounting mismatch')
 print(json.dumps({'status':'PASS_PACKAGE_INTEGRITY','manifest_files':count,'local_frozen_source_files':len(lock['study_files']),
  'baseline_files_verified':dep,'attempt_ledgers':len(ledgers),'attempted_forwards_all_versions':attempts,'acknowledged_completions':acknowledged,
  'models_loaded':0,'new_forwards':0,'scope':'byte/source/ledger checks, not re-execution of numerical study'},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print(f'FAILED: {type(e).__name__}: {e}',file=sys.stderr);sys.exit(1)
