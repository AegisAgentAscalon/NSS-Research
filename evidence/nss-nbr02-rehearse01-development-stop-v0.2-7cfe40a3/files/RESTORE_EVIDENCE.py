"""Restore exact captured record bytes; no model/data generation or numerical execution."""
from pathlib import Path
import json,hashlib,sys,shutil
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source'))
from envelope_codec import restore_records

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
m=json.loads((ROOT/'DELIVERY_MAP.json').read_text())
for x in m['encoded_targets']:
 p=ROOT/x['target'];p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and sha(p)==x['sha256']:continue
 blob=ROOT/x['encoded'];assert sha(blob)==x['encoded_sha256']
 tmp=p.with_suffix('.restoring');restore_records(blob.read_bytes(),tmp)
 assert tmp.stat().st_size==x['bytes'] and sha(tmp)==x['sha256'];tmp.replace(p)
for x in m['aliases']:
 src=ROOT/x['source'];target=ROOT/x['target'];target.parent.mkdir(parents=True,exist_ok=True)
 assert sha(src)==x['sha256']
 if target.exists() and sha(target)==x['sha256']:continue
 shutil.copyfile(src,target);assert target.stat().st_size==x['bytes'] and sha(target)==x['sha256']
print('RESTORED: original captured bytes and exact replay alias, verified by hashes.')
