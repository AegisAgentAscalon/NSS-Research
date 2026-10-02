from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
m=json.loads((r/'MANIFEST.json').read_text())
fail=[]
for k,v in m['files'].items():
 p=r/k
 if not p.is_file() or p.stat().st_size!=v['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:fail.append(k)
print(json.dumps({'status':'PASS' if not fail else 'FAIL','manifest_files':len(m['files']),'failures':fail,'numerical_reproduction':False},indent=2))
raise SystemExit(bool(fail))
