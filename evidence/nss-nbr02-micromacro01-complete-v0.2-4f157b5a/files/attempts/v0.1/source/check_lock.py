from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent.parent
lock=json.loads((ROOT/'audit/SOURCE_LOCK.json').read_text())
for rel,d in lock['files'].items():
 p=ROOT/rel
 if not p.is_file() or p.stat().st_size!=d['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=d['sha256']:raise RuntimeError('SOURCE_LOCK:'+rel)
