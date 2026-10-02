"""Scoped, data-only research snapshots. No external effects or model promotion."""
from __future__ import annotations
import json,os,shutil,tempfile
from pathlib import Path
import torch
from safetensors.torch import save_file,load_file
from .models import D,KEYS
from .util import write_json,sha,digest_tensors

class Session:
    SCHEMA='state-recovery003/qualified-maintenance-v1'
    def __init__(self,candidate,scope,revision):
        if not isinstance(scope,str) or not scope or len(scope)>200:raise ValueError('Invalid scope')
        self.c=candidate;self.scope=scope;self.revision=revision
        self.state=candidate.state(torch.full((1,KEYS),8,dtype=torch.long))
        self.events=0;self.rounds=0
    def identity(self):
        out=dict(schema=self.SCHEMA,scope=self.scope,revision=self.revision,mode=self.c.mode,
                 reference_sha256=self.c.rep.source_sha256)
        if self.c.repair is not None:out['repair']=digest_tensors(self.c.repair.state_dict())
        if self.c.fastslow is not None:out['fastslow']=digest_tensors(self.c.fastslow.state_dict())
        return out
    @torch.no_grad()
    def event(self,key,value,score):
        if type(key)!=int or not 0<=key<KEYS or type(value)!=int or not 0<=value<8:
            raise ValueError('Invalid address/value')
        if not isinstance(score,(int,float)) or not 0<=score<=1:raise ValueError('Invalid score')
        if score>=.5:
            y=torch.zeros((1,KEYS),dtype=torch.long);y[0,key]=value
            mask=torch.zeros((1,KEYS),dtype=torch.bool);mask[0,key]=True
            self.state=self.c.write(self.state,y,mask)
        self.events+=1
    @torch.no_grad()
    def maintain(self,n):
        if type(n)!=int or not 0<=n<=4096:raise ValueError('Invalid maintenance budget')
        for _ in range(n):self.state=self.c.step(self.state)
        self.rounds+=n
    def clear(self):self.state=self.c.reset(self.state);self.events+=1
    @torch.no_grad()
    def read(self):
        if self.c.mode=='exact_archive':raise ValueError('Archive control not a neural-state session')
        return self.c.predict(self.state).clone()
    def save(self,path):
        path=Path(path)
        if path.exists():raise FileExistsError('Snapshot immutable')
        path.parent.mkdir(parents=True,exist_ok=True)
        temp=Path(tempfile.mkdtemp(prefix='.snapshot-',dir=path.parent))
        try:
            save_file({f'lane{i}':x.detach().contiguous() for i,x in enumerate(self.state)},str(temp/'state.safetensors'))
            write_json(temp/'metadata.json',dict(identity=self.identity(),events=self.events,rounds=self.rounds,
                                                tensor_sha256=sha(temp/'state.safetensors')))
            os.replace(temp,path)
        finally:
            if temp.exists():shutil.rmtree(temp)
    def restore(self,path):
        path=Path(path);meta=json.loads((path/'metadata.json').read_text())
        if meta.get('identity')!=self.identity():raise ValueError('Scope, weights, mode or revision mismatch')
        if (path/'state.safetensors').stat().st_size>1<<20:raise ValueError('Snapshot too large')
        if sha(path/'state.safetensors')!=meta.get('tensor_sha256'):raise ValueError('Checksum mismatch')
        t=load_file(str(path/'state.safetensors'))
        expected={f'lane{i}' for i in range(2 if self.c.dual else 1)}
        if set(t)!=expected:raise ValueError('State lane mismatch')
        if any(x.shape!=(1,KEYS,D) or x.dtype!=torch.float32 or not torch.isfinite(x).all() for x in t.values()):
            raise ValueError('State shape, type or finite check failed')
        for k in ('events','rounds'):
            if type(meta.get(k))!=int or meta[k]<0:raise ValueError('Invalid event clock')
        self.state=tuple(t[f'lane{i}'] for i in range(len(t)))
        self.events,self.rounds=meta['events'],meta['rounds']
