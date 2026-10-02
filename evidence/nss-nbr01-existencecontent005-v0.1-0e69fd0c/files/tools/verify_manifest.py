import sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
count=0
for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
 digest,name=line.split('  ',1);p=(ROOT/name).resolve()
 if not p.is_relative_to(ROOT.resolve()) or not p.is_file() or sha(p)!=digest:raise SystemExit(f'Manifest mismatch: {name}')
 count+=1
print(f'PASS: {count} manifest-covered files')
