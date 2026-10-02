"""Synthetic continuation: matched input/label/step arms, not matched compute.
No external training data, core changes, or generic Forge implementation.
"""
from pathlib import Path
import time,hashlib,threading
import torch
from torch import nn
from safetensors.torch import save_file,load_file
from .models import Representation,Repair,LocalEmpty,D,UNKNOWN
from .util import setup,write_json,digest_tensors,array_digest,sha,environment,source_identity

def batch(rep,g,n=128):
    # Approximately half empty starts. All inputs generated before any model use.
    y=torch.randint(0,8,(n,),generator=g)
    y=torch.where(torch.rand(n,generator=g)<.5,UNKNOWN,y)
    sigma=torch.tensor([0.,.1,.25,.5])[torch.randint(0,4,(n,),generator=g)]
    z=rep.codes[y]+sigma[:,None]*torch.randn(n,D,generator=g)
    depth=(1,2,4,8,16)[int(torch.randint(0,5,(),generator=g))]
    sig=torch.tensor([0.,.05,.10,.15])[torch.randint(0,4,(n,),generator=g)]
    noises=torch.randn(depth,n,D,generator=g)*sig[None,:,None]
    draws=torch.rand(depth,n,generator=g)
    # Disjoint exact writes (0.04 probability) and clears (0.04 probability).
    writes=draws<.04;clears=(draws>=.04)&(draws<.08)
    values=torch.randint(0,8,(depth,n),generator=g)
    probe_sigma=.02+.23*torch.rand(32,1,generator=g)
    probes=probe_sigma*torch.randn(32,D,generator=g)
    return z,y,noises,writes,clears,values,probes

def train(root,output,kind,rep_seed,learn_seed,steps=1800,development=False):
    setup();root=Path(root);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    if kind not in ('replay','contract','local_empty'):raise ValueError('Invalid training kind')
    stem=f'{kind}_rep{rep_seed}_seed{learn_seed}'
    dest=output/(stem+'.safetensors')
    if dest.exists() or (output/(stem+'.json')).exists():raise FileExistsError('Completed run cannot be overwritten')
    rep=Representation(root/'reference'/f'soft_slots_wide_seed{rep_seed}.safetensors')
    frozen=digest_tensors(rep.state_dict())
    torch.manual_seed(learn_seed);m=LocalEmpty() if kind=='local_empty' else Repair()
    parent=root/'reference'/f'recurrent_rep{rep_seed}_seed{441 if development else rep_seed+200}.safetensors'
    missing=m.load_state_dict(load_file(str(parent)),strict=kind!='local_empty')
    if kind=='local_empty' and (missing.missing_keys!=['raw_radius'] or missing.unexpected_keys):raise RuntimeError('Wrong local parent')
    initial={k:v.detach().clone() for k,v in m.state_dict().items()}
    opt=torch.optim.AdamW([p for p in m.parameters() if p.requires_grad],lr=.01 if kind=='local_empty' else .0015,weight_decay=.0001)
    g=torch.Generator().manual_seed(4_000_000+learn_seed)
    write_json(output/(stem+'.prerun.json'),dict(status='NOT_RUN',time_unix=time.time(),kind=kind,
        representation=rep_seed,learning_seed=learn_seed,steps=steps,development=development,
        initial_digest=digest_tensors(initial),source_identity=source_identity(root),
        protocol_sha256=sha(root/'spec/protocol.json') if (root/'spec/protocol.json').exists() else 'DEVELOPMENT',
        parent_sha256=sha(parent) if parent else None))
    # RSS is a sampled process footprint, not a tensor-only or exact peak.
    import psutil
    proc=psutil.Process();rss=[];stop=threading.Event()
    def sample():
        while not stop.wait(.01):rss.append(proc.memory_info().rss)
    th=threading.Thread(target=sample,daemon=True);th.start()
    start=time.perf_counter();cpu=time.process_time();logs=[];h=hashlib.sha256();rounds=0;labels=0
    try:
        for t in range(steps):
            z,y,noises,writes,clears,values,probes=batch(rep,g)
            h.update(array_digest(z,y,noises,writes,clears,values,probes).encode())
            opt.zero_grad(set_to_none=True);losses=[]
            for k in range(len(noises)):
                z=torch.where(writes[k,:,None],rep.codes[values[k]],z)
                z=torch.where(clears[k,:,None],torch.zeros_like(z),z)
                y=torch.where(clears[k],UNKNOWN,torch.where(writes[k],values[k],y))
                z=m(z+noises[k])
                mse=(z-rep.codes[y]).square().mean()
                ce=nn.functional.cross_entropy(rep(z),y)
                losses.append(mse+.2*ce)
            task=torch.stack(losses).mean()
            # Both arms evaluate the same probes. The intervention is the loss
            # coefficient; ratio bounds are sampled, not a contraction theorem.
            out=m(probes)
            ratios=out.square().sum(-1)/probes.square().sum(-1).clamp_min(1e-8)
            contract=nn.functional.relu(ratios-.64).mean()
            anchor=(m(rep.codes)-rep.codes).square().mean()
            loss=task+2.*anchor+(.5 if kind=='contract' else 0.)*contract
            if not torch.isfinite(loss):raise RuntimeError('Nonfinite loss')
            loss.backward()
            if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in m.parameters()):raise RuntimeError('Nonfinite gradient')
            grad=nn.utils.clip_grad_norm_(m.parameters(),1.);opt.step()
            rounds+=len(noises);labels+=len(noises)*128
            if t==0 or (t+1)%150==0 or t+1==steps:
                row=dict(step=t+1,loss=float(loss.detach()),task=float(task.detach()),contract=float(contract.detach()),
                         mse=float(mse.detach()),anchor=float(anchor.detach()),rounds=len(noises),probe_mean_ratio=float(ratios.detach().mean()),grad=float(grad))
                logs.append(row);print(stem,row,flush=True)
    finally:
        stop.set();th.join();rss.append(proc.memory_info().rss)
    m.eval();weights={k:v.detach().contiguous() for k,v in m.state_dict().items()}
    changed=sum(int((v!=initial[k]).sum()) for k,v in weights.items())
    if not changed:raise RuntimeError('No learned change')
    if frozen!=digest_tensors(rep.state_dict()):raise RuntimeError('Frozen source mutated')
    save_file(weights,str(dest))
    result=dict(status='RUN',kind=kind,rep_seed=rep_seed,learn_seed=learn_seed,steps=steps,development=development,
        training_data_digest=h.hexdigest(),parent_sha256=sha(parent) if parent else None,
        initial_digest=digest_tensors(initial),final_digest=digest_tensors(weights),checkpoint_sha256=sha(dest),
        changed_parameter_elements=changed,trainable_parameters=sum(p.numel() for p in m.parameters() if p.requires_grad),total_parameters=sum(p.numel() for p in m.parameters()),fitted_radius=float(m.radius().detach()) if kind=='local_empty' else None,
        parameter_bytes=sum(p.numel()*p.element_size() for p in m.parameters()),
        gradient_bytes=sum(p.grad.numel()*p.grad.element_size() for p in m.parameters() if p.grad is not None),
        optimizer_tensor_bytes=sum(v.numel()*v.element_size() for s in opt.state.values() for v in s.values() if torch.is_tensor(v)),
        sequence_presentations=steps*128,supervised_event_presentations=labels,maintenance_training_rounds=rounds,
        contraction_probe_presentations=steps*32,shared_exact_anchor_presentations=steps*9,reference_sha256=rep.source_sha256,frozen_reference_unchanged=True,
        train_wall_seconds=time.perf_counter()-start,train_cpu_seconds=time.process_time()-cpu,
        sampled_process_peak_rss_bytes=max(rss),logs=logs,environment=environment(),
        evaluation_parameter_updates=0,matching='Paired initial weights, random inputs, direct code targets, labels and optimizer steps. Objective differs; not exact wall-time/FLOP match.',
        source_preparation='HorizonBinding002 representation + StateRecovery003 recurrent parent are reused, not free or newly trained here.')
    write_json(output/(stem+'.json'),result);return result
