"""Shared I/O and environment only; no scientific decision rules."""
from __future__ import annotations
import hashlib, json, os, sys, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(path): return json.loads(Path(path).read_text())
def dump(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')
def write_lines(path,rows):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('wb') as f:
        for r in rows: f.write(canonical(r)+b'\n')
def read_lines(path):
    with Path(path).open() as f:return [json.loads(s) for s in f if s.strip()]
def base():
    r=Path(os.environ.get('CM01_BASELINE','/mnt/data/cm01_work/recovery/Q010_InferenceRecovery_v1.6')).resolve()
    if not (r/'VERIFY_CONTEXT.py').is_file(): raise FileNotFoundError('Set CM01_BASELINE to the extracted verified recovery folder')
    return r
def paths(producer=False):
    r=base();s=r/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0'
    sys.path[:0]=[str(r/'source'),str(s/'verification_B')]
    if producer:sys.path[:0]=[str(r/'recovery'),str(s/'implementation_A')]
    return r,s

def configure():
    import torch
    torch.set_num_threads(1);torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True);torch.manual_seed(0)
    def forbidden(*a,**kw): raise RuntimeError('CM01_INFERENCE_ONLY: no optimizer or gradients')
    torch.optim.Optimizer.__init__=forbidden;torch.autograd.backward=forbidden;torch.autograd.grad=forbidden
    torch.set_grad_enabled(False)

def check_lock():
    lock=load(ROOT/'protocol/SOURCE_LOCK.json')
    for name,h in lock['study_files'].items():
        if sha(ROOT/name)!=h:raise ValueError('Locked study source mismatch: '+name)
    r=base()
    for name,h in lock['baseline_files'].items():
        if sha(r/name)!=h:raise ValueError('Locked baseline source mismatch: '+name)
    if sha(ROOT/'protocol/PROTOCOL.json')!=lock['protocol_sha256']:raise ValueError('protocol drift')
    return sha(ROOT/'protocol/SOURCE_LOCK.json')

def arrays(path):
    with np.load(path,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def digest_arrays(d):
    h=hashlib.sha256()
    for k,a in sorted(d.items()):
        a=np.ascontiguousarray(a);h.update(k.encode());h.update(a.dtype.str.encode());h.update(str(a.shape).encode());h.update(a.tobytes())
    return h.hexdigest()
