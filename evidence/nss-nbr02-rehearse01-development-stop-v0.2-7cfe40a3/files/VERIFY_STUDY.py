from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'MANIFEST.json').read_text());fail=[]
for name,v in m['files'].items():
 p=ROOT/name
 if not p.is_file():fail.append((name,'missing'));continue
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 if p.stat().st_size!=v['bytes'] or h.hexdigest()!=v['sha256']:fail.append((name,'identity'))
if fail:print(json.dumps({'status':'FAIL','failures':fail},indent=2));sys.exit(1)
print(json.dumps({'status':'PASS','manifest_files':len(m['files']),'numerical_execution':False}))
