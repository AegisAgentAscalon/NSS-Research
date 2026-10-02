"""I/O, dependency paths and deterministic execution only; no scientific rules."""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def load(p):return json.loads(Path(p).read_text())
def dump(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(x,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')
def lines(p):
    with Path(p).open() as f:return [json.loads(s) for s in f if s.strip()]
def write_lines(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('wb') as f:
        for r in x:f.write(canonical(r)+b'\n')
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def array_digest(data):
    h=hashlib.sha256()
    for k,v in sorted(data.items()):
        a=np.ascontiguousarray(v);h.update(k.encode());h.update(a.dtype.str.encode());h.update(str(a.shape).encode());h.update(a.tobytes())
    return h.hexdigest()
def baseline():
    p=Path(os.environ.get('CM02_BASELINE','/mnt/data/_cm02_deps/Q010_InferenceRecovery_v1.6')).resolve()
    if not (p/'VERIFY_CONTEXT.py').is_file():raise FileNotFoundError('Set CM02_BASELINE to verified extracted Q010 recovery folder')
    return p
def paths(producer=False):
    b=baseline();s=b/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0'
    sys.path[:0]=[str(b/'source'),str(s/'verification_B')]
    if producer:sys.path[:0]=[str(b/'recovery'),str(s/'implementation_A')]
    return b,s
def configure():
    import torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True);torch.manual_seed(0)
    def forbidden(*a,**kw):raise RuntimeError('CM02_INFERENCE_ONLY: optimizer/backpropagation forbidden')
    torch.optim.Optimizer.__init__=forbidden;torch.autograd.backward=forbidden;torch.autograd.grad=forbidden;torch.set_grad_enabled(False)
def check_lock():
    x=load(ROOT/'protocol/SOURCE_LOCK.json')
    for p,h in x['study_files'].items():
        if sha(ROOT/p)!=h:raise ValueError('Study source drift: '+p)
    for p,h in x['baseline_files'].items():
        if sha(baseline()/p)!=h:raise ValueError('Dependency source drift: '+p)
    return sha(ROOT/'protocol/SOURCE_LOCK.json')
def read_arrays(x):
    return {k:np.asarray(v,dtype=np.bool_ if k in ('valid','active') else np.int64 if k=='symbols' else np.float32) for k,v in x.items()}
def csv_write(path, rows, fields=None):
    import csv
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
