from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
manifest=root/'MANIFEST.sha256'
if not manifest.exists():raise SystemExit('No packaged manifest present')
checked=0
for line in manifest.read_text().splitlines():
    digest,name=line.split('  ',1)
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():raise SystemExit(f'Missing/unsafe path: {name}')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise SystemExit(f'Changed file: {name}')
    checked+=1
print(f'PASS: {checked} manifest-covered files match SHA-256.')
