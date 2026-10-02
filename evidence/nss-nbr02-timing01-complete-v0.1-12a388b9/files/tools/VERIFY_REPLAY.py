"""Recheck the retained independent adaptive run's bytes, not launch new adaptation."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
r=json.loads((R/'audit/ADAPTIVE_REPLAY_COMPARISON.json').read_text())
for c in r['checks']:
 a=R/'raw/primary'/c['path'];b=R/'raw/replay'/c['path']
 assert a.stat().st_size==b.stat().st_size==c['bytes']
 assert sha(a)==sha(b)==c['primary_sha256']==c['replay_sha256']
print(json.dumps({'status':'PASS','retained_byte_pairs':len(r['checks']),'new_model_calls':0,'new_learning_replay':False,'historical_full_adaptive_replay_receipt':'audit/ADAPTIVE_REPLAY_COMPARISON.json'},indent=2))
