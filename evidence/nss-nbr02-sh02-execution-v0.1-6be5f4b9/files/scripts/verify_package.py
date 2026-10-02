"""Verify this extracted package against MANIFEST.json, without model execution."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'MANIFEST.json').read_text());bad=[]
for rel,info in manifest['files'].items():
    p=(ROOT/rel).resolve()
    if not p.is_relative_to(ROOT.resolve()) or not p.is_file():bad.append({'file':rel,'reason':'missing_or_invalid'});continue
    data=p.read_bytes()
    if len(data)!=info['bytes'] or hashlib.sha256(data).hexdigest()!=info['sha256']:bad.append({'file':rel,'reason':'hash_or_size'})
print(json.dumps({'verified_members':len(manifest['files']),'failures':bad},indent=2))
sys.exit(bool(bad))
