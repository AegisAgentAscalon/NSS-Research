from pathlib import Path
import hashlib,json,datetime,os,platform,sys,time
import numpy as np
import torch
from safetensors.torch import save_file,load_file
ROOT=Path(__file__).resolve().parents[1]
def setup(seed=0):
 torch.set_num_threads(1)
 torch.set_num_interop_threads(1) if torch.get_num_interop_threads()!=1 else None
 torch.use_deterministic_algorithms(True)
 torch.manual_seed(seed)
 np.random.seed(seed)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,obj):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
def weights_hash(model):
 h=hashlib.sha256()
 for k,v in sorted(model.state_dict().items()):
  a=v.detach().cpu().contiguous().numpy();h.update(k.encode());h.update(str(a.shape).encode());h.update(a.tobytes())
 return h.hexdigest()
def save_model(path,model):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 save_file({k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()},str(p))
def tensor(x):return torch.from_numpy(np.asarray(x))
def env():
 return {'utc':utc(),'python':sys.version,'platform':platform.platform(),'torch':torch.__version__,'numpy':np.__version__,'cuda':torch.cuda.is_available(),'torch_threads':torch.get_num_threads(),'pid':os.getpid()}
