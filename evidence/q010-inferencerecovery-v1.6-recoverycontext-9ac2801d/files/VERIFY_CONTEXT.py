from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
m=json.loads((R/'CONTEXT_MANIFEST.json').read_text())
for n,r in m['files'].items():
 p=R/n
 if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(R):raise ValueError('Unsafe/missing member: '+n)
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 if p.stat().st_size!=r['bytes'] or h!=r['sha256']:raise ValueError('Hash mismatch: '+n)
print(json.dumps({'status':'PASS_CONTEXT_FILES','files':len(m['files']),'full_raw_evidence_archive':False}))
