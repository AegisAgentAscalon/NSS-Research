from __future__ import annotations
import os,sys,json,hashlib,platform,time
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'reference'))

def setup():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)

def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');os.replace(temp,path)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def model_sha(m):
    h=hashlib.sha256()
    for key,value in sorted(m.state_dict().items()):h.update(key.encode());h.update(value.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def comparison(a,b):
    aa=a.detach().cpu().numpy() if isinstance(a,torch.Tensor) else np.asarray(a)
    bb=b.detach().cpu().numpy() if isinstance(b,torch.Tensor) else np.asarray(b)
    atol,rtol=(1e-10,1e-9) if aa.dtype==np.float64 else (2e-5,2e-5)
    err=np.abs(aa-bb);limit=atol+rtol*np.abs(bb)
    finite=np.isfinite(aa)&np.isfinite(bb)
    return {'scalars':int(aa.size),'violations':int(((err>limit)|~finite).sum()),'max_abs':float(err.max()) if err.size else 0.,'max_normalized':float((err/limit).max()) if err.size else 0.,'atol':atol,'rtol':rtol}

def runtime():
    return {'torch':torch.__version__,'numpy':np.__version__,'python':sys.version,'platform':platform.platform(),'threads':torch.get_num_threads(),'cuda_available':torch.cuda.is_available(),'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
