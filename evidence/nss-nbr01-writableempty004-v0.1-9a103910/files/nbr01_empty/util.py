from __future__ import annotations
import hashlib, json, os, platform, sys, time
from pathlib import Path
import numpy as np
import torch

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()

def digest_tensors(tensors):
    h=hashlib.sha256()
    for k,v in sorted(tensors.items()):
        a=v.detach().cpu().contiguous()
        h.update(k.encode());h.update(str(tuple(a.shape)).encode());h.update(str(a.dtype).encode());h.update(a.numpy().tobytes())
    return h.hexdigest()

def array_digest(*items):
    h=hashlib.sha256()
    for x in items:
        a=x.detach().cpu().contiguous().numpy() if torch.is_tensor(x) else np.ascontiguousarray(x)
        h.update(str(a.shape).encode());h.update(str(a.dtype).encode());h.update(a.tobytes())
    return h.hexdigest()

def write_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
    os.replace(tmp,p)

def setup():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

def environment():
    return dict(python=sys.version,platform=platform.platform(),torch=torch.__version__,
                numpy=np.__version__,cuda_available=torch.cuda.is_available(),threads=torch.get_num_threads(),
                cpu_count=os.cpu_count(),time_unix=time.time(),device='sandbox CPU, not user PC',energy='NOT_MEASURED')

def source_identity(root):
    root=Path(root)
    return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*.py')) if '__pycache__' not in str(p)}
