"""Read-only SHA-256 verification of public derivatives. No study code is imported."""
import hashlib,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
rows=[json.loads(s) for s in (root/'catalog/derivations.jsonl').read_text(encoding='utf-8').splitlines()]
errors=[];checked={}
for row in rows:
    path=(root/row['public_path']).resolve()
    if not path.is_relative_to(root):
        errors.append({'path':row['public_path'],'error':'outside checkout'});continue
    if path not in checked:
        if not path.is_file():checked[path]=None
        else:
            data=path.read_bytes();checked[path]=(len(data),hashlib.sha256(data).hexdigest())
    if checked[path]!=(row['public_bytes'],row['public_sha256']):
        errors.append({'path':row['public_path'],'error':'missing or hash/size mismatch'})
print(json.dumps({'rows':len(rows),'unique_files':len(checked),'errors':errors},indent=2))
sys.exit(bool(errors))
