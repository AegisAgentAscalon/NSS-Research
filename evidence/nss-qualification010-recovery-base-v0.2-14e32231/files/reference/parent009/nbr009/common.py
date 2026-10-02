"""Local deterministic research utilities. No model downloads or external services."""
from . import ROOT,PARENT
from nbr008.common import parents,model_hashes
from nbr008.config import load_gate,resolver as parent_resolver
from nbr006.common import setup,utc,sha,dump,weights_hash,save_model,env
from nbr006 import data,models
from pathlib import Path
from safetensors.torch import load_file
import json,time,hashlib
import numpy as np
import torch

def load_pair(pair):
    ms=parents(pair);head,cfg=load_gate(1000+pair)
    return ms,head,cfg

def make_resolver(method,ms,head,cfg):return parent_resolver(method,ms,head,cfg)

def load_binder(pair,kind):
    m=models.make('binder')
    if kind=='parent': p=PARENT/'reference/parent_checkpoints'/f'binder_{800+pair}.safetensors'
    else:p=ROOT/'checkpoints'/f'binder_{kind}_{1100+pair}.safetensors'
    m.load_state_dict(load_file(str(p)));m.eval()
    for w in m.parameters():w.requires_grad_(False)
    return m

def array_digest(arrays):
    h=hashlib.sha256()
    for k,a in sorted(arrays.items()):
        a=np.ascontiguousarray(a);h.update(k.encode());h.update(str(a.dtype).encode());h.update(str(a.shape).encode());h.update(a.tobytes())
    return h.hexdigest()

def save_arrays(path,arrays,info):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise FileExistsError(path)
    np.savez_compressed(path,**arrays)
    dump(path.with_suffix('.json'),{**info,'array_sha256':sha(path),'array_digest':array_digest(arrays),'n_arrays':len(arrays)})

def hashes_source():
    return {str(p.relative_to(ROOT)):sha(p) for d in ('nbr009','reference','spec','checkpoints') for p in (ROOT/d).rglob('*') if p.is_file() and p.suffix not in ('.pyc',) and '__pycache__' not in p.parts}
