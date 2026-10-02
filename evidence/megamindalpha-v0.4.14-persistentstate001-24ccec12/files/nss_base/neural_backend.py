"""Optional CPU PyTorch backend; deliberately small linear neural smoke test.

No transformer, network access, arbitrary checkpoint code, packed ternary kernel,
learned router/evaluator, or production execution authority is implemented here.
"""
from contextlib import contextmanager
from copy import deepcopy
import math
import os
from pathlib import Path
from hashlib import sha256
import platform
import sys
import time

import torch
from torch import nn
from torch.nn import functional as F

from .neural_contracts import (CODEC, MODES, encoded, fields, fingerprint,
    mapping, protocol, validate_pairs)
from .runtime import fail


@contextmanager
def deterministic_cpu(seed):
    threads=torch.get_num_threads();enabled=torch.are_deterministic_algorithms_enabled()
    warn=torch.is_deterministic_algorithms_warn_only_enabled()
    precision=torch.get_float32_matmul_precision(); dtype=torch.get_default_dtype()
    # CPU-only fork preserves caller RNG; no CUDA initialization.
    with torch.random.fork_rng(devices=[]):
        try:
            torch.set_num_threads(1);torch.use_deterministic_algorithms(True);torch.manual_seed(seed)
            torch.set_float32_matmul_precision('highest');torch.set_default_dtype(torch.float32)
            with torch.autocast(device_type='cpu', enabled=False):
                yield
        finally:
            torch.use_deterministic_algorithms(enabled,warn_only=warn);torch.set_num_threads(threads)
            torch.set_float32_matmul_precision(precision);torch.set_default_dtype(dtype)


NUMERICAL_ENV_KEYS = ('MKL_CBWR', 'MKL_ENABLE_INSTRUCTIONS', 'MKL_NUM_THREADS',
    'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'ATEN_CPU_CAPABILITY', 'ONEDNN_MAX_CPU_ISA')


def numerical_environment():
    # CPU identity without machine serials, paths or variable clock measurements.
    try:
        cpu = sorted(set(line.strip() for line in Path('/proc/cpuinfo').read_text().splitlines()
                         if line.split(':', 1)[0].strip() in ('vendor_id', 'model name', 'cpu family', 'model', 'stepping', 'flags')))
    except OSError:
        cpu = [platform.processor(), platform.machine()]
    return {'schema_version': 1, 'torch_build_sha256': sha256(torch.__config__.show().encode()).hexdigest(),
            'cpu_identity_sha256': fingerprint(cpu), 'cpu_capability': torch.backends.cpu.get_cpu_capability(),
            'backend_environment': {k: os.environ.get(k) for k in NUMERICAL_ENV_KEYS},
            'float32_matmul_precision': 'highest', 'cpu_autocast': False,
            'score_path': 'reloaded_checkpoints_no_grad_v2', 'mse_rule': 'torch_fp32_mean_exact'}


def environment():
    return {'python':sys.version,'torch':str(torch.__version__),'platform':platform.platform(),
            'machine':platform.machine(),'device':'cpu','dtype':'float32','threads':1,
            'deterministic_algorithms':True,'cuda_used':False,'packed_ternary':False,
            'energy_measured':False, 'numerics': numerical_environment()}


class Core(nn.Module):
    def __init__(self, mode):
        super().__init__()
        if mode not in MODES: fail('INCOMPATIBLE_CONFIGURATION','Unsupported numerical mode')
        self.mode=mode
        self.w1=nn.Parameter(torch.randn(16,16)*.2)
        self.w2=nn.Parameter(torch.randn(16,16)*.2)

    def effective(self,w):
        if self.mode=='fp32':return w
        # Fixed-scale ternary numerical reference, NOT a BitLinear implementation.
        quantized=w.clamp(-1,1).round()
        return w+(quantized-w).detach() if w.requires_grad else quantized

    def forward(self,x,a=None,b=None):
        h=F.linear(x,self.effective(self.w1))
        if a is not None:h=h+a(x)
        y=F.linear(h,self.effective(self.w2))
        if b is not None:y=y+b(h)
        return y


class Overlay(nn.Module):
    def __init__(self,rank):
        super().__init__()
        if type(rank) is not int or rank not in (4,8):fail('VALIDATION_FAILED','Unsupported rank')
        self.rank=rank
        self.down=nn.Parameter(torch.randn(rank,16)*.1)
        self.up=nn.Parameter(torch.zeros(16,rank))

    def forward(self,x):return F.linear(F.linear(x,self.down),self.up)


def encode_pairs(value):
    return F.one_hot(torch.tensor(validate_pairs(value),dtype=torch.long),num_classes=16).float()


def targets(value,name):
    table=mapping(name)
    return encode_pairs([[table[x] for x in row] for row in validate_pairs(value)])


def checkpoint(module):
    if type(module) is Core:
        kind='core';meta={'mode':module.mode}
    elif type(module) is Overlay:
        kind='overlay';meta={'rank':module.rank,'mode':'fp32'}
    else:fail('VALIDATION_FAILED','Unknown module type')
    tensors={}
    for name,t in module.state_dict().items():
        if t.dtype!=torch.float32 or t.device.type!='cpu' or not torch.isfinite(t).all():
            fail('VALIDATION_FAILED','Only finite CPU fp32 checkpoint tensors supported')
        tensors[name]={'shape':list(t.shape),'dtype':'float32','values':t.flatten().tolist()}
    result={'schema_version':1,'architecture':'two_linear_symbol_blocks_v1',
            'kind':kind,'metadata':meta,'tensors':tensors}
    encoded(result)
    return result


def load_checkpoint(value,expected_sha256):
    """Data-only exact architecture; never torch.load, pickle, remote or custom code."""
    encoded(value)
    if fingerprint(value)!=expected_sha256:fail('VALIDATION_FAILED','Checkpoint hash mismatch')
    fields(value,('schema_version','architecture','kind','metadata','tensors'))
    if type(value['schema_version']) is not int or value['schema_version']!=1 or value['architecture']!='two_linear_symbol_blocks_v1':
        fail('INCOMPATIBLE_CONFIGURATION','Unknown checkpoint format')
    meta=value['metadata']
    if value['kind']=='core':
        fields(meta,('mode',)); expected={'w1':[16,16],'w2':[16,16]}
        if meta['mode'] not in MODES:fail('INCOMPATIBLE_CONFIGURATION','Unknown precision')
    elif value['kind']=='overlay':
        fields(meta,('mode','rank'))
        if type(meta['rank']) is not int or meta['rank'] not in (4,8) or meta['mode']!='fp32':
            fail('INCOMPATIBLE_CONFIGURATION','Unknown overlay metadata')
        expected={'down':[meta['rank'],16],'up':[16,meta['rank']]}
    else:fail('INCOMPATIBLE_CONFIGURATION','Unknown checkpoint kind')
    fields(value['tensors'],expected)
    for k,shape in expected.items():
        t=value['tensors'][k];fields(t,('shape','dtype','values'))
        if t['shape']!=shape or any(type(x) is not int for x in t['shape']) or t['dtype']!='float32':
            fail('VALIDATION_FAILED','Wrong tensor shape/dtype')
        if type(t['values']) is not list or len(t['values'])!=math.prod(shape):
            fail('VALIDATION_FAILED','Wrong tensor length')
        if any(type(x) not in (float,int) or not math.isfinite(x) or abs(x)>1e6 for x in t['values']):
            fail('VALIDATION_FAILED','Out-of-range/nonfinite tensor')
    with torch.random.fork_rng(devices=[]):
        obj=Core(meta['mode']) if value['kind']=='core' else Overlay(meta['rank'])
    obj.load_state_dict({k:torch.tensor(v['values'],dtype=torch.float32).reshape(v['shape']) for k,v in value['tensors'].items()},strict=True)
    freeze(obj)
    # Reject serialized non-fp32 numbers that would round into a different artifact.
    if fingerprint(checkpoint(obj))!=expected_sha256:fail('VALIDATION_FAILED','Lossy checkpoint representation')
    return obj


def freeze(module):
    module.eval()
    for p in module.parameters():p.requires_grad_(False);p.grad=None
    return module


def assert_frozen(module,expected):
    if any(p.requires_grad or p.grad is not None for p in module.parameters()):
        fail('VALIDATION_FAILED','Frozen parameter/gradient ownership violated')
    if fingerprint(checkpoint(module))!=expected:fail('VALIDATION_FAILED','Accepted weights changed')


def fit(parameters,objective,steps,lr,gate):
    ps=list(parameters)
    if not ps or any(not p.requires_grad for p in ps):fail('VALIDATION_FAILED','Invalid optimizer owner')
    optimizer=torch.optim.Adam(ps,lr=lr); first=None;last=None;start=time.perf_counter()
    gate()
    for step in range(steps):
        if step and step%25==0:gate()
        optimizer.zero_grad(set_to_none=True);loss=objective()
        if not torch.isfinite(loss):fail('VALIDATION_FAILED','Nonfinite training loss')
        if first is None:first=float(loss.detach())
        loss.backward()
        if any(p.grad is None or not torch.isfinite(p.grad).all() for p in ps):
            fail('VALIDATION_FAILED','Missing/nonfinite candidate gradients')
        optimizer.step();last=float(loss.detach())
    gate()
    return {'updates':steps,'first_loss':first,'last_loss':last,'seconds':time.perf_counter()-start}


def metric(pred,value,name):
    truth=targets(value,name)
    if pred.shape!=truth.shape or not torch.isfinite(pred).all():fail('VALIDATION_FAILED','Invalid neural prediction')
    correct=pred.argmax(-1)==truth.argmax(-1)
    return {'pair_accuracy':float(correct.all(-1).float().mean()),
            'token_accuracy':float(correct.float().mean()),
            'mse':float(F.mse_loss(pred,truth)),'pairs':len(value)}


def train_trial(p,seed,mode,train_pairs,test_pairs,gate):
    p=protocol(p);validate_pairs(train_pairs,'train');validate_pairs(test_pairs,'test')
    if seed not in p['seeds'] or mode not in p['precisions']:fail('VALIDATION_FAILED','Unplanned trial')
    with deterministic_cpu(seed):
        x=encode_pairs(train_pairs);core=Core(mode);start=checkpoint(core)
        core_log=fit(core.parameters(),lambda:F.mse_loss(core(x),x)+
            F.mse_loss(F.linear(x,core.effective(core.w1)),x)+
            F.mse_loss(F.linear(x,core.effective(core.w2)),x),p['core_steps'],p['learning_rate'],gate)
        freeze(core);core_ck=checkpoint(core);core_hash=fingerprint(core_ck)
        def train_overlay(name,slot,rank,steps):
            assert_frozen(core,core_hash);o=Overlay(rank)
            with torch.no_grad():
                zero=torch.equal(core(x),core(x,a=o) if slot==1 else core(x,b=o))
            if not zero:fail('VALIDATION_FAILED','Blank overlay is not a no-op')
            target=targets(train_pairs,name);initial=fingerprint(checkpoint(o))
            log=fit(o.parameters(),lambda:F.mse_loss(core(x,a=o) if slot==1 else core(x,b=o),target),steps,p['learning_rate'],gate)
            freeze(o);assert_frozen(core,core_hash)
            log.update(blank_noop=zero,weights_changed=initial!=fingerprint(checkpoint(o)),train_input_tokens=steps*len(train_pairs)*2)
            return o,log
        a,alog=train_overlay('A',1,4,p['overlay_steps']);a_ck=checkpoint(a)
        b,blog=train_overlay('B',2,4,p['overlay_steps']);b_ck=checkpoint(b)
        joint,jlog=train_overlay('AB',2,8,2*p['overlay_steps'])
        a2,a2log=train_overlay('A2',1,4,p['overlay_steps'])
        assert_frozen(a,fingerprint(a_ck));assert_frozen(b,fingerprint(b_ck));assert_frozen(core,core_hash)
        gate()
        artifacts={'core':core_ck,'A':a_ck,'B':b_ck,'joint':checkpoint(joint),'A2':checkpoint(a2)}
        metrics=evaluate_checkpoints(artifacts,{k:fingerprint(v) for k,v in artifacts.items()},test_pairs)
        effective=sorted(set(core.effective(core.w1).flatten().tolist()+core.effective(core.w2).flatten().tolist()))
        result={'seed':seed,'precision':mode,'metrics':metrics,
            'training':{'core':core_log,'A':alog,'B':blog,'joint':jlog,'A2':a2log},
            'invariants':{'core_trained':fingerprint(start)!=core_hash,'core_unchanged_after_freeze':True,
                'previous_overlays_unchanged':True,'gen2_reuses_exact_B':True,
                'blank_overlays_noop':all(l['blank_noop'] for l in (alog,blog,jlog,a2log))},
            'parameters':{'core':512,'A':128,'B':128,'modular_total':256,'joint':256,'A2':128},
            'effective_core_values':effective if mode=='ternary_core_reference' else None,
            'core_storage':'float32 master tensors; no packed kernel',
            'overlay_precision':'float32',
            'checkpoint_hashes':{k:fingerprint(v) for k,v in artifacts.items()}}
        return result,artifacts


def evaluate_checkpoints(artifacts, hashes, test_pairs):
    """Canonical fresh-score and replay path. Exact comparison, no epsilon patch."""
    mods={k:load_checkpoint(v,hashes[k]) for k,v in artifacts.items()}
    core=mods['core']; test=validate_pairs(test_pairs); x=encode_pairs(test)
    with torch.no_grad():
        preds={'core':(core(x),'CORE'),'A':(core(x,a=mods['A']),'A'),
               'B':(core(x,b=mods['B']),'B'),'AB':(core(x,a=mods['A'],b=mods['B']),'AB'),
               'joint':(core(x,b=mods['joint']),'AB'),'gen2':(core(x,a=mods['A2'],b=mods['B']),'A2B'),
               'ablation_A':(core(x,b=mods['B']),'AB'),'ablation_B':(core(x,a=mods['A']),'AB'),
               'ablation_core':(core(x),'AB')}
        metrics={k:metric(y,test,n) for k,(y,n) in preds.items()}
        retained=[r for r in test if all(v not in (5,6) for v in r)]
        metrics['gen2_retained']=metric(core(encode_pairs(retained),a=mods['A2'],b=mods['B']),retained,'AB')
    return metrics
