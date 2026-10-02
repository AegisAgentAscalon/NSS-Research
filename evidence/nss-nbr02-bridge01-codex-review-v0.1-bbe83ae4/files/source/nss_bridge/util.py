from __future__ import annotations
import hashlib,json,os
from pathlib import Path

def canonical(value) -> bytes:
    return json.dumps(value,sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False).encode('utf-8')

def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()

def file_hash(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def strict_json(text):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise ValueError('DUPLICATE_JSON_KEY')
            out[k]=v
        return out
    def constant(s): raise ValueError('NONFINITE_JSON')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=constant)

def atomic_json(path,value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('wb') as f:
        f.write(canonical(value)+b'\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
