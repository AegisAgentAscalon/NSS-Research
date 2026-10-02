from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
for row in m['files']:
 p=root/row['path']; assert p.is_file(),row['path']
 b=p.read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
print(json.dumps({'status':'PASS','verified_files':len(m['files']),'model_calls':0}))
