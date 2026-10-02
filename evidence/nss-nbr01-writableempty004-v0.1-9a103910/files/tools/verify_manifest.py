"""Verify packaged immutable files; generated __pycache__ is not packaged."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'MANIFEST.sha256';count=0
for line in manifest.read_text().splitlines():
 digest,name=line.split('  ',1);p=(ROOT/name).resolve()
 if not p.is_relative_to(ROOT.resolve()) or not p.is_file():raise SystemExit('Missing/unsafe path '+name)
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 if actual!=digest:raise SystemExit('Checksum mismatch '+name)
 count+=1
print(f'PASS: {count} manifest-covered files match.')
