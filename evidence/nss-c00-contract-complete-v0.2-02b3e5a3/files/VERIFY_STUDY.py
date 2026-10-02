from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
for entry in m['files']:
    p=root/entry['path'];b=p.read_bytes()
    if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
        raise SystemExit('Mismatch: '+entry['path'])
print(f"Verified {len(m['files'])} payloads. This checks bytes, not scientific generalization.")
