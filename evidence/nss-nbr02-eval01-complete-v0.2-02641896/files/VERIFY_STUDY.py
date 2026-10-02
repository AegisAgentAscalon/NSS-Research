"""Verify exact delivered bytes; this is not numerical reproduction."""
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent;m=json.loads((r/'MANIFEST.json').read_text());n=0
for item in m['files']:
 p=(r/item['path']).resolve()
 if not p.is_relative_to(r):raise RuntimeError('UNSAFE_PATH')
 b=p.read_bytes()
 if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:raise RuntimeError('IDENTITY_MISMATCH:'+item['path'])
 n+=1
print(json.dumps({'status':'PASS','manifest_payloads':n,'model_calls':0}))
