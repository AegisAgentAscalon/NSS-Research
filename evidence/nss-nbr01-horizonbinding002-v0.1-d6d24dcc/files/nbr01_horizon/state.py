"""Isolated data-only research snapshots; no accepted NSS state is accessed."""
from __future__ import annotations
import json, os, shutil, tempfile
from pathlib import Path
import torch
from safetensors.torch import save_file, load_file
from .data import MAX_EVENTS, validate
from .models import WIDTH
from .util import canonical, weights_digest, sha, write_json
import hashlib


class Session:
    def __init__(self, model, scope, mode='native', threshold=.5):
        if not isinstance(scope,str) or not 1<=len(scope)<=120:
            raise ValueError('Invalid scope')
        if mode not in ('native','hard','close_low') or not 0<=threshold<=1:
            raise ValueError('Invalid transition policy')
        self.model,self.scope,self.mode,self.threshold=model,scope,mode,threshold
        self.events=0
        self.state=(torch.empty(1,0,3) if model.kind=='tape_reader' else torch.zeros(1,4,WIDTH))

    @torch.no_grad()
    def observe(self,x):
        validate(x)
        if len(x)!=1 or self.events+x.shape[1]>MAX_EVENTS:
            raise ValueError('Session event budget exceeded')
        if self.model.kind=='tape_reader':self.state=torch.cat((self.state,x),1)
        else:
            for s in range(0,x.shape[1],256):
                self.state=self.model.encode(x[:,s:s+256],self.state,self.mode,self.threshold)
        self.events+=x.shape[1]

    @torch.no_grad()
    def predict(self):
        if self.model.kind=='tape_reader':return self.model(self.state)
        return self.model.head(self.state)

    def reset(self,new_scope):
        self.__init__(self.model,new_scope,self.mode,self.threshold)

    def save(self,path):
        path=Path(path)
        if path.exists():raise FileExistsError(path)
        path.parent.mkdir(parents=True,exist_ok=True)
        tmp=Path(tempfile.mkdtemp(prefix='.state-',dir=path.parent))
        try:
            save_file({'state':self.state.contiguous()},str(tmp/'state.safetensors'))
            metadata=dict(schema=1,study='NBR-01/HorizonBinding002',scope=self.scope,
                kind=self.model.kind,model_digest=weights_digest(self.model),mode=self.mode,
                threshold=self.threshold,events=self.events,raw_state_bytes=self.state.numel()*4,
                state_sha256=sha(tmp/'state.safetensors'))
            envelope=dict(metadata,metadata_sha256=hashlib.sha256(canonical(metadata)).hexdigest())
            write_json(tmp/'metadata.json',envelope);os.rename(tmp,path)
            return envelope
        finally:
            if tmp.exists():shutil.rmtree(tmp)

    @classmethod
    def restore(cls,path,model,scope,mode='native',threshold=.5):
        path=Path(path)
        if (path/'metadata.json').stat().st_size>8192 or (path/'state.safetensors').stat().st_size>100_000:
            raise ValueError('Oversized state artifact')
        meta=json.loads((path/'metadata.json').read_text())
        mh=meta.pop('metadata_sha256',None)
        if mh!=hashlib.sha256(canonical(meta)).hexdigest():raise ValueError('Metadata integrity')
        expected=dict(schema=1,study='NBR-01/HorizonBinding002',scope=scope,kind=model.kind,
                      model_digest=weights_digest(model),mode=mode,threshold=threshold)
        if any(meta.get(k)!=v for k,v in expected.items()):raise ValueError('Incompatible state identity')
        if type(meta.get('events')) is not int or not 0<=meta['events']<=MAX_EVENTS:
            raise ValueError('Invalid event count')
        if sha(path/'state.safetensors')!=meta['state_sha256']:raise ValueError('State integrity')
        tensors=load_file(str(path/'state.safetensors'))
        if set(tensors)!={'state'}:raise ValueError('Unexpected tensors')
        h=tensors['state']
        shape=(1,meta['events'],3) if model.kind=='tape_reader' else (1,4,WIDTH)
        if tuple(h.shape)!=shape or h.dtype!=torch.float32 or not torch.isfinite(h).all():
            raise ValueError('Incompatible state tensor')
        if h.numel()*4!=meta['raw_state_bytes']:raise ValueError('Byte count mismatch')
        if model.kind=='tape_reader':validate(h)
        obj=cls(model,scope,mode,threshold);obj.events=meta['events'];obj.state=h
        return obj
