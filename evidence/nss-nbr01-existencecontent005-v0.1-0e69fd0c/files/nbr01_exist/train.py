"""Paired synthetic supervised preparation; never trains during evaluation."""
from pathlib import Path
import hashlib,time,threading
import torch
from torch import nn
from safetensors.torch import load_file,save_file
from .models import Representation,Repair,Presence,Coupled,D,UNKNOWN,KINDS
from .util import setup,write_json,sha,array_digest,digest_tensors,environment,source_identity

def batch(rep,g,n=128):
    y=torch.randint(0,8,(n,),generator=g)
    y=torch.where(torch.rand(n,generator=g)<.5,UNKNOWN,y)
    labels=torch.where(y<8,1.,-1.)[:,None].expand(n,4).clone()
    sig=torch.tensor([0.,.15,.35,.60])[torch.randint(0,4,(n,),generator=g)]
    z=rep.codes[y]+sig[:,None]*torch.randn(n,D,generator=g)
    p=labels+sig[:,None]*torch.randn(n,4,generator=g)
    depth=(1,2,4,8,16)[int(torch.randint(0,5,(),generator=g))]
    sigma=torch.tensor([0.,.05,.10,.15])[torch.randint(0,4,(n,),generator=g)]
    nz=torch.randn(depth,n,D,generator=g)*sigma[None,:,None]
    np=torch.randn(depth,n,4,generator=g)*sigma[None,:,None]
    r=torch.rand(depth,n,generator=g);writes=r<.04;clears=(r>=.04)&(r<.08)
    values=torch.randint(0,8,(depth,n),generator=g)
    return z,p,y,nz,np,writes,clears,values

def train(root,out,kind,rep_seed,learn_seed,steps=1800,development=False):
    setup();root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    if kind not in KINDS:raise ValueError('Unknown training kind')
    stem=f'{kind}_rep{rep_seed}_seed{learn_seed}'
    if any((out/(stem+ext)).exists() for ext in ('.json','.safetensors')):raise FileExistsError('Immutable completed run')
    rep=Representation(root/'reference'/f'soft_slots_wide_seed{rep_seed}.safetensors')
    parent=root/'reference'/f'recurrent_rep{rep_seed}_seed{441 if rep_seed==141 else rep_seed+200}.safetensors'
    old=Repair();old.load_state_dict(load_file(str(parent)));old.requires_grad_(False)
    oldid=digest_tensors(old.state_dict());repid=digest_tensors(rep.state_dict())
    torch.manual_seed(learn_seed)
    m=Coupled(old) if kind=='coupled17' else Presence(1 if kind=='split1' else 4)
    initial={k:v.detach().clone() for k,v in m.state_dict().items()}
    opt=torch.optim.AdamW(m.parameters(),lr=.0015,weight_decay=.0001)
    g=torch.Generator().manual_seed(12_000_000+learn_seed)
    start_info=dict(status='NOT_RUN',time_unix=time.time(),kind=kind,rep_seed=rep_seed,learn_seed=learn_seed,steps=steps,
        development=development,initial_digest=digest_tensors(initial),source_identity=source_identity(root),parent_sha256=sha(parent),
        protocol_sha256=sha(root/'spec/protocol.json'))
    write_json(out/(stem+'.prerun.json'),start_info)
    import psutil
    proc=psutil.Process();rss=[];stop=threading.Event()
    def sample():
        while not stop.wait(.01):rss.append(proc.memory_info().rss)
    th=threading.Thread(target=sample,daemon=True);th.start()
    begin=time.perf_counter();cpu=time.process_time();logs=[];digest=hashlib.sha256();events=0;rounds=0
    try:
        for t in range(steps):
            z,p,y,nz,np,writes,clears,values=batch(rep,g)
            digest.update(array_digest(z,p,y,nz,np,writes,clears,values).encode())
            if kind!='split4':p=p[:,:1]
            opt.zero_grad(set_to_none=True);losses=[]
            for k in range(len(nz)):
                z=torch.where(writes[k,:,None],rep.codes[values[k]],z)
                z=torch.where(clears[k,:,None],torch.zeros_like(z),z)
                p=torch.where(writes[k,:,None],torch.ones_like(p),p)
                p=torch.where(clears[k,:,None],-torch.ones_like(p),p)
                y=torch.where(clears[k],UNKNOWN,torch.where(writes[k],values[k],y))
                target_p=torch.where(y<8,1.,-1.)[:,None].expand_as(p)
                if kind=='coupled17':
                    allstate=m(torch.cat((z+nz[k],p+np[k,:,:1]),-1))
                    z,p=allstate[:,:D],allstate[:,D:]
                    # Same inferred sign guard as the deployed research cell.
                    z=torch.where(p>0,z,torch.zeros_like(z))
                    content=(z-rep.codes[y]).square().mean()
                    ce=nn.functional.cross_entropy(rep(z),y)
                else:
                    p=m(p+np[k,:,:p.shape[1]])
                    # Frozen content is not trained by presence labels.
                    content=torch.tensor(0.);ce=torch.tensor(0.)
                ploss=(p-target_p).square().mean()
                losses.append(ploss+content+.2*ce)
            task=torch.stack(losses).mean()
            if kind=='coupled17':
                anchor_codes=torch.cat((rep.codes,torch.tensor([1.]*8+[-1.])[:,None]),-1)
                anchor=(m(anchor_codes)-anchor_codes).square().mean()
            else:
                anchors=torch.tensor([-1.,1.])[:,None].expand(2,m.width)
                anchor=(m(anchors)-anchors).square().mean()
            loss=task+2.*anchor
            if not torch.isfinite(loss):raise RuntimeError('Nonfinite training loss')
            loss.backward()
            if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in m.parameters()):raise RuntimeError('Nonfinite gradient')
            gn=nn.utils.clip_grad_norm_(m.parameters(),1.);opt.step()
            events+=len(nz)*128;rounds+=len(nz)
            if t==0 or (t+1)%300==0 or t+1==steps:
                row=dict(step=t+1,loss=float(loss.detach()),task=float(task.detach()),anchor=float(anchor.detach()),
                    presence_mse=float(ploss.detach()),content_mse=float(content.detach()),depth=len(nz),grad=float(gn))
                logs.append(row);print(stem,row,flush=True)
    finally:
        stop.set();th.join();rss.append(proc.memory_info().rss)
    if digest_tensors(old.state_dict())!=oldid or digest_tensors(rep.state_dict())!=repid:raise RuntimeError('Frozen source changed')
    weights={k:v.detach().contiguous() for k,v in m.state_dict().items()}
    changed=sum(int((weights[k]!=initial[k]).sum()) for k in weights)
    if changed==0:raise RuntimeError('No learned parameter change')
    checkpoint=out/(stem+'.safetensors');save_file(weights,str(checkpoint))
    result=dict(status='RUN',kind=kind,rep_seed=rep_seed,learn_seed=learn_seed,steps=steps,development=development,
        source_identity=start_info['source_identity'],protocol_sha256=start_info['protocol_sha256'],parent_sha256=sha(parent),
        reference_sha256=rep.source_sha256,initial_digest=digest_tensors(initial),final_digest=digest_tensors(weights),checkpoint_sha256=sha(checkpoint),
        changed_parameter_elements=changed,trainable_parameters=sum(p.numel() for p in m.parameters()),
        parameter_bytes=sum(p.numel()*p.element_size() for p in m.parameters()),
        gradient_bytes=sum(p.grad.numel()*p.grad.element_size() for p in m.parameters() if p.grad is not None),
        optimizer_tensor_bytes=sum(v.numel()*v.element_size() for s in opt.state.values() for v in s.values() if torch.is_tensor(v)),
        sequence_presentations=steps*128,supervised_event_presentations=events,training_maintenance_rounds=rounds,
        training_data_digest=digest.hexdigest(),frozen_sources_unchanged=True,logs=logs,
        train_wall_seconds=time.perf_counter()-begin,train_cpu_seconds=time.process_time()-cpu,sampled_process_peak_rss_bytes=max(rss),environment=environment(),
        matching='same generated episodes, labels, steps and optimizer settings; selected coordinates/objectives/trainable weights differ, NOT compute matched',
        scope='supervised maintenance of an explicitly encoded existence state; not learned admission or entity binding')
    write_json(out/(stem+'.json'),result);return result
