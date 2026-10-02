from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'MANIFEST.json').read_text())
for name,d in m['files'].items():
    p=root/name
    if not p.is_file() or p.stat().st_size!=d['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=d['sha256']:
        raise SystemExit('Failed payload: '+name)
print('Verified',len(m['files']),'declared payloads.')
