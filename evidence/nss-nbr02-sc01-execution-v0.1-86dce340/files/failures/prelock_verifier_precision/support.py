from pathlib import Path
import sys,hashlib,json,platform,time,resource
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
import numpy as np
import torch
from nss_hsa import MaintenanceReader
from sc01 import save,canonical

def setup():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)

def model_hash(model):
    h=hashlib.sha256()
    for k,v in sorted(model.state_dict().items()):h.update(k.encode());h.update(v.detach().numpy().tobytes())
    return h.hexdigest()

def load(seed):
    m=MaintenanceReader();ck=torch.load(ROOT/'checkpoints'/f'{seed}_hsa_inference.pt',map_location='cpu',weights_only=False)
    m.load_state_dict(ck['model']);m.eval();return m,model_hash(m)

def compare(a,b):
    a=np.asarray(a);b=np.asarray(b);atol,rtol=(1e-10,1e-9)if a.dtype==np.float64 else(2e-5,2e-5)
    err=np.abs(a-b);lim=atol+rtol*np.abs(b);bad=(err>lim)|~np.isfinite(a)|~np.isfinite(b)
    return {'scalars':int(a.size),'violations':int(bad.sum()),'max_abs':float(err.max())if a.size else 0.,'max_normalized':float((err/lim).max())if a.size else 0.}

def runtime():
    return {'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'python':sys.version,'torch':torch.__version__,
            'numpy':np.__version__,'platform':platform.platform(),'threads':torch.get_num_threads(),
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
