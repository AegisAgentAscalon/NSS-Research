"""Bounded synthetic dynamics training. This is not generic Forge."""
from __future__ import annotations
import hashlib,time,threading
from pathlib import Path
import torch
from torch import nn
from safetensors.torch import save_file,load_file
from .models import Representation,Repair,FastSlow
from .data import training_batch
from .util import setup,write_json,digest_tensors,array_digest,sha,environment,source_identity

KINDS=('readout_repair','recurrent','fast_slow')

def make(kind):
    if kind=='fast_slow':return FastSlow()
    if kind in ('readout_repair','recurrent'):return Repair()
    raise ValueError('Unknown training kind')

def train(root,output,kind,rep_seed,learn_seed,steps=1800):
    setup();root=Path(root);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    stem=f'{kind}_rep{rep_seed}_seed{learn_seed}'
    dest=output/(stem+'.safetensors')
    if dest.exists() or (output/(stem+'.json')).exists():raise FileExistsError('No overwrite of completed runs')
    rep=Representation(root/'reference'/f'soft_slots_wide_seed{rep_seed}.safetensors')
    rep_identity=digest_tensors(rep.state_dict())
    torch.manual_seed(learn_seed)
    model=make(kind)
    initial={k:v.detach().clone() for k,v in model.state_dict().items()}
    opt=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.0001)
    g=torch.Generator().manual_seed(700_000+learn_seed)
    write_json(output/(stem+'.prerun.json'),dict(status='NOT_RUN',time_unix=time.time(),
               source_identity=source_identity(root),kind=kind,rep_seed=rep_seed,learn_seed=learn_seed,steps=steps,
               initial_digest=digest_tensors(initial),reference_sha256=rep.source_sha256,
               protocol_sha256=sha(root/'spec/protocol.json') if (root/'spec/protocol.json').exists() else 'DEVELOPMENT'))
    h=hashlib.sha256();logs=[];rss=[];stop=threading.Event()
    import psutil
    proc=psutil.Process()
    def sampler():
        while not stop.wait(.005):rss.append(proc.memory_info().rss)
    thread=threading.Thread(target=sampler,daemon=True);thread.start()
    t0,c0=time.perf_counter(),time.process_time()
    updates=0
    try:
        for step in range(steps):
            b=training_batch(rep,g)
            h.update(array_digest(b['f'],b['s'],b['new'],b['write'],b['target']).encode())
            h.update(str(b['depth']).encode())
            target=rep.codes[b['target']]
            opt.zero_grad(set_to_none=True)
            if kind=='fast_slow':
                f,s=model.write(b['f'],b['s'],rep.codes[b['new']],b['write'])
            else:
                f=torch.where(b['write'][:,None],rep.codes[b['new']],b['f'])
            losses=[]
            rounds=1 if kind=='readout_repair' else b['depth']
            for k in range(rounds):
                if kind=='fast_slow':f,s=model(f,s)
                else:f=model(f)
                mse=(f-target).square().mean()
                ce=nn.functional.cross_entropy(rep(f),b['target'])
                losses.append(mse+.2*ce)
            loss=torch.stack(losses).mean()
            if not torch.isfinite(loss):raise RuntimeError('Nonfinite loss')
            loss.backward()
            if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in model.parameters()):raise RuntimeError('Nonfinite gradients')
            grad_norm=nn.utils.clip_grad_norm_(model.parameters(),1.)
            opt.step();updates+=1
            if step==0 or (step+1)%150==0 or step+1==steps:
                row=dict(step=step+1,loss=float(loss.detach()),mse=float(mse.detach()),
                         accuracy=float((rep(f).argmax(-1)==b['target']).float().mean()),
                         grad_norm=float(grad_norm),rounds=rounds)
                logs.append(row);print(stem,row,flush=True)
    finally:
        stop.set();thread.join();rss.append(proc.memory_info().rss)
    model.eval();tensor_state={k:v.detach().contiguous() for k,v in model.state_dict().items()}
    changed=sum(int((v!=initial[k]).sum()) for k,v in tensor_state.items())
    if not changed or updates!=steps:raise RuntimeError('No learning or incomplete training')
    if digest_tensors(rep.state_dict())!=rep_identity:raise RuntimeError('Frozen source changed')
    save_file(tensor_state,str(dest))
    optbytes=sum(v.numel()*v.element_size() for s in opt.state.values() for v in s.values() if torch.is_tensor(v))
    result=dict(status='RUN',kind=kind,rep_seed=rep_seed,learn_seed=learn_seed,steps=steps,
        examples=steps*128,answer_labels=steps*128,target_code_scalars=steps*128*16,
        direct_state_target_supervision=True,training_data_digest=h.hexdigest(),
        initial_digest=digest_tensors(initial),final_digest=digest_tensors(tensor_state),
        changed_parameter_elements=changed,trainable_parameters=sum(p.numel() for p in model.parameters()),
        parameter_bytes=sum(p.numel()*p.element_size() for p in model.parameters()),optimizer_tensor_bytes=optbytes,
        gradient_bytes=sum(p.numel()*p.element_size() for p in model.parameters()),
        reference_sha256=rep.source_sha256,frozen_reference_unchanged=True,
        checkpoint_sha256=sha(dest),train_wall_seconds=time.perf_counter()-t0,train_cpu_seconds=time.process_time()-c0,
        rss_process_peak_5ms_sample_bytes=max(rss),logs=logs,environment=environment(),
        evaluation_parameter_updates=0,matching='Same corrupt inputs, labels, code targets and optimizer steps; different rounds/compute/state bytes',
        source_preparation='Reused prior 2400-step wide soft model (development141 differs); prior preparation is not free',
        fast_slow_rates=[float(v) for v in model.rates().detach()] if kind=='fast_slow' else None)
    write_json(output/(stem+'.json'),result)
    return result
