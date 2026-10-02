"""Restore exact recorded bytes, never rerun a learner. Requires NumPy, not Torch."""
from pathlib import Path
import argparse, hashlib, io, json, lzma, os, shutil, struct, sys
import numpy as np

def sha_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def safe(root,name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe relative path')
    out=root/p
    if not out.resolve().is_relative_to(root.resolve()):raise ValueError('Escaping path')
    return out
def exact(f,n):
    b=f.read(n)
    if len(b)!=n:raise ValueError('Truncated numerical envelope')
    return b
def checked_existing(p,n,h):
    if p.exists():
        if p.stat().st_size!=n or sha_file(p)!=h:raise ValueError('Conflicting existing file: '+str(p))
        return True
    return False
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default=str(Path(__file__).resolve().parent));args=ap.parse_args();root=Path(args.root).resolve()
    spec=json.loads((root/'DELIVERY_ENCODING.json').read_text());payload=safe(root,spec['payload'])
    if payload.stat().st_size!=spec['payload_bytes'] or sha_file(payload)!=spec['sha256']:raise ValueError('Encoded payload identity mismatch')
    expected={e['path']:e for e in spec['entries']};seen=set();writes=0
    with lzma.open(payload,'rb') as f:
        if exact(f,20)!=b'NSS_NPZ_ENVELOPE_V1\n':raise ValueError('Wrong envelope magic')
        while True:
            n=struct.unpack('<Q',exact(f,8))[0]
            if not n:break
            if n>16*1024*1024:raise ValueError('Oversized metadata frame')
            header=json.loads(exact(f,n));name=header['path'];p=safe(root,name)
            if name not in expected or name in seen:raise ValueError('Unlisted/duplicate numerical target')
            ent=expected[name]
            if header['bytes']!=ent['bytes'] or header['sha256']!=ent['sha256']:raise ValueError('Header identity mismatch')
            arrays={}
            for d in header['arrays']:
                dtype=np.dtype(d['dtype']);shape=tuple(d['shape']);order=d['order']
                if dtype.hasobject or order not in ('C','F') or any(type(x)!=int or x<0 for x in shape):raise ValueError('Invalid numeric dtype or shape')
                count=1
                for x in shape:count*=x
                if count*dtype.itemsize!=d['bytes'] or d['bytes']>128*1024*1024:raise ValueError('Invalid array byte count')
                b=exact(f,d['bytes'])
                if hashlib.sha256(b).hexdigest()!=d['sha256']:raise ValueError('Array identity mismatch')
                if d['name'] in arrays:raise ValueError('Duplicate array name')
                arrays[d['name']]=np.frombuffer(b,dtype=dtype).reshape(shape,order=order).copy(order=order)
            buf=io.BytesIO();np.savez_compressed(buf,**arrays);raw=buf.getvalue()
            if len(raw)!=ent['bytes'] or hashlib.sha256(raw).hexdigest()!=ent['sha256']:
                raise RuntimeError('Exact NPZ reconstruction differs (possibly library/compression version); do not overwrite evidence: '+name)
            if not checked_existing(p,ent['bytes'],ent['sha256']):
                p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.restore-tmp');tmp.write_bytes(raw);os.replace(tmp,p);writes+=1
            seen.add(name)
        if f.read(1):raise ValueError('Unexpected trailing envelope data')
    if seen!=set(expected):raise ValueError('Missing numerical targets')
    aliases=json.loads((root/'DELIVERY_ALIASES.json').read_text())['entries'];alias_writes=0
    for e in aliases:
        s=safe(root,e['source']);p=safe(root,e['path'])
        if s.stat().st_size!=e['bytes'] or sha_file(s)!=e['sha256']:raise ValueError('Replay alias source mismatch')
        if not checked_existing(p,e['bytes'],e['sha256']):
            p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,p);alias_writes+=1
    print(json.dumps({'encoded_targets_verified':len(seen),'encoded_targets_written':writes,'genuine_replay_aliases_verified':len(aliases),'aliases_written':alias_writes,'model_operations':0,'original_numeric_gate':'FAILED_UNCHANGED'}))
if __name__=='__main__': main()
