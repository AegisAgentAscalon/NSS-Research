"""Deterministic evidence utilities. No model or oracle imports."""
from __future__ import annotations
import hashlib,json,os,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'protocol/CONFIG.json').read_text())
def seed(name:str)->int:
    return int.from_bytes(hashlib.sha256((CFG['study']+'/v0.1/'+name).encode()).digest()[:8],'big')%(2**63-1)
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def canon(obj)->bytes:return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def json_write(p:Path,obj):
    p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp')
    with open(tmp,'wb') as f:f.write(canon(obj)+b'\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
def npz(p:Path,**arrays):
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'wb') as f:np.savez_compressed(f,**arrays);f.flush();os.fsync(f.fileno())
def arrhash(a):
    d=hashlib.sha256()
    for k,v in sorted(a.items()):
        v=np.ascontiguousarray(v);d.update(canon([k,str(v.dtype),list(v.shape)]));d.update(v.tobytes())
    return d.hexdigest()
def source_check():
    lock=json.loads((ROOT/'SOURCE_LOCK.json').read_text())
    for x in lock['files']:
        if sha((ROOT/x['path']).read_bytes())!=x['sha256']:raise RuntimeError('SOURCE_CHANGED: '+x['path'])
    return sha((ROOT/'SOURCE_LOCK.json').read_bytes())
class Journal:
    def __init__(self,folder:Path):
        self.folder=folder;folder.mkdir(parents=True,exist_ok=True)
        self.f=open(folder/'attempts.jsonl','xb');self.seq=0;self.tail='0'*64
        self.count={'updates':0,'backwards':0,'cells':0,'heads':0};self.commits=0
    def write(self,kind,**fields):
        self.seq+=1;r={'seq':self.seq,'previous':self.tail,'kind':kind,**fields}
        b=canon(r);self.tail=sha(b);r['hash']=self.tail
        self.f.write(canon(r)+b'\n');self.f.flush();os.fsync(self.f.fileno());return self.seq
    def intent(self,op,updates=0,backwards=0,cells=0,heads=0,**data):
        vals=locals().copy();vals.pop('self');vals.pop('op');vals.pop('data')
        for k in self.count:
            self.count[k]+=vals[k]
            cap=CFG[{'updates':'update_cap_all','backwards':'backward_cap_all','cells':'cell_cap_all','heads':'head_cap_all'}[k]]//2
            if self.count[k]>cap:raise RuntimeError('PER_PASS_RESERVATION_CAP '+k)
        return self.write('INTENT',op=op,cost={k:vals[k] for k in self.count},**data)
    def commit(self,ref,**data):self.commits+=1;self.write('COMMIT',intent=ref,**data)
    def close(self):
        self.f.close();json_write(self.folder/'COUNTS.json',{'counts':self.count,'commits':self.commits,'events':self.seq,'terminal_hash':self.tail})
