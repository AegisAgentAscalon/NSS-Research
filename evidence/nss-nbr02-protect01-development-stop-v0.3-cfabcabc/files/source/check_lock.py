import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
for n,d in json.loads((R/'audit/SOURCE_LOCK.json').read_text())['files'].items():
 b=(R/n).read_bytes()
 if len(b)!=d['bytes'] or hashlib.sha256(b).hexdigest()!=d['sha256']:raise RuntimeError('SOURCE_LOCK:'+n)
print('SOURCE_LOCK_OK')
