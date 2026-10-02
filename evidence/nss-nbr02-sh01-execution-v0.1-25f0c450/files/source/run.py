from __future__ import annotations
import csv,gzip,json,os,platform,resource,sys,time,traceback
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import torch
import psutil
from common import *
from store import *
ROOT=Path(__file__).resolve().parents[1]
SEEDS=[8801,8802,8803,8804];STEPS=600

def prep():
    begin=time.perf_counter()
    data={}
    for split,seed,count,n in [('train',771001,STEPS*16,8),('development',771002,32,8),
                              ('confirmation',771003,256,8),('stress',771004,64,16)]:
        ws=worlds(seed,count,n)
        with gzip.open(ROOT/f'fixtures/{split}.jsonl.gz','wt') as f:
            for w in ws:f.write(canonical(w).decode()+'\n')
        parts=batch(ws)
        data[split]=parts
        fingerprints=[sha(canonical({k:v for k,v in w.items() if k!='id'})) for w in ws]
        write_json(ROOT/f'fixtures/{split}_identities.json',{'seed':seed,'count':count,'n':n,'fingerprints':fingerprints})
        print('prepared',split,count,flush=True)
    ids={s:set(json.loads((ROOT/f'fixtures/{s}_identities.json').read_text())['fingerprints']) for s in data}
    overlap={a+':'+b:len(ids[a]&ids[b]) for a in ids for b in ids if a<b}
    assert not any(overlap.values()),overlap
    write_json(ROOT/'results/fixture_preparation.json',{'seconds':time.perf_counter()-begin,'overlap':overlap,
       'tensor_bytes':{s:sum(t.numel()*t.element_size() for t in ts) for s,ts in data.items()}})
    return data

def lock():
    files=[ROOT/'PROTOCOL.md']+sorted((ROOT/'source').glob('*.py'))+sorted((ROOT/'fixtures').glob('*'))
    receipt={'locked_at_utc':datetime.now(timezone.utc).isoformat(),'files':{
        str(p.relative_to(ROOT)):{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in files},
        'python':sys.version,'torch':torch.__version__,'numpy':np.__version__,'platform':platform.platform(),
        'cpu':platform.processor(),'threads':torch.get_num_threads(),'cuda':torch.cuda.is_available(),
        'seeds':SEEDS,'updates_per_fit':STEPS,'parameters':sum(p.numel() for p in Reader().parameters()),
        'main_limit':4800,'preflight_actual':4}
    write_json(ROOT/'SOURCE_LOCK.json',receipt)
    return receipt

def evaluate(model,split,parts,mode,n,batch_size=16):
    model.eval();outs=[]
    with torch.no_grad():
        for a in range(0,len(parts[0]),batch_size):
            x,ix,v,y=[t[a:a+batch_size] for t in parts]
            outs.append(model(x,ix,v,n,mode).numpy())
    logits=np.concatenate(outs);ys=parts[-1].numpy();pred=logits.argmax(-1)
    return logits,metrics(ys,pred)

def save(model,opt,seed,mode,step):
    p=ROOT/f'checkpoints/{seed}_{mode}_{step:04d}.pt'
    torch.save({'model':model.state_dict(),'optimizer':None if opt is None else opt.state_dict(),
       'seed':seed,'mode':mode,'step':step,'model_hash':model_hash(model),'rng':torch.get_rng_state()},p)
    return sha(p.read_bytes())

def main():
    setup();data=prep();receipt=lock();start=time.perf_counter();process=psutil.Process();updates=0
    losses=[];outcomes=[];phase='training'
    def guard():
        if time.perf_counter()-start>900:raise RuntimeError('RESOURCE_WALL_STOP')
        if process.memory_info().rss>2.5*2**30:raise RuntimeError('RESOURCE_RSS_STOP')
        if sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())>112*2**20:raise RuntimeError('RESOURCE_STORAGE_STOP')
    try:
        for seed in SEEDS:
            for mode in ['dense','hsa']:
                torch.manual_seed(seed);m=Reader();init=model_hash(m);save(m,None,seed,mode,0)
                opt=torch.optim.AdamW(m.parameters(),lr=.002,betas=(.9,.999),eps=1e-8,weight_decay=.01,foreach=False,fused=False)
                fit_start=time.perf_counter();m.train()
                for step in range(1,STEPS+1):
                    a=(step-1)*16;x,ix,v,y=[t[a:a+16] for t in data['train']]
                    opt.zero_grad(set_to_none=True);logits=m(x,ix,v,8,mode)
                    loss=F.cross_entropy(logits.reshape(-1,4),y.reshape(-1));loss.backward()
                    norm=torch.nn.utils.clip_grad_norm_(m.parameters(),1.0,error_if_nonfinite=True)
                    opt.step();updates+=1
                    losses.append({'seed':seed,'mode':mode,'step':step,'loss':loss.item(),'preclip_gradnorm':norm.item(),
                         'batch_correct':int((logits.argmax(-1)==y).sum()),'batch_decisions':y.numel()})
                    if step%200==0:
                        save(m,opt,seed,mode,step);print('train',seed,mode,step,round(loss.item(),6),flush=True);guard()
                write_json(ROOT/f'results/fit_{seed}_{mode}.json',{'seed':seed,'mode':mode,'initial_hash':init,
                    'final_hash':model_hash(m),'updates':STEPS,'seconds':time.perf_counter()-fit_start})
        phase='evaluation'
        # Confirmation starts only after all prescribed fits have completed.
        for seed in SEEDS:
            for mode in ['dense','hsa']:
                cp=torch.load(ROOT/f'checkpoints/{seed}_{mode}_0600.pt',weights_only=False,map_location='cpu')
                m=Reader();m.load_state_dict(cp['model']);assert model_hash(m)==cp['model_hash']
                for split,n in [('development',8),('confirmation',8),('stress',16)]:
                    logits,row=evaluate(m,split,data[split],mode,n)
                    np.savez_compressed(ROOT/f'results/pred_{seed}_{mode}_{split}.npz',logits=logits,target=data[split][-1].numpy())
                    row.update({'seed':seed,'mode':mode,'split':split,'functional_target_met':row['accuracy']>=.95 and row['macro_recall']>=.90})
                    outcomes.append(row)
                    print('eval',seed,mode,split,round(row['accuracy'],4),round(row['macro_recall'],4),flush=True)
                # Same trained HSA weights and mask, dense vs sparse numerical check.
                if mode=='hsa':
                    x,ix,v,y=[a[:8] for a in data['confirmation']]
                    with torch.no_grad():
                        a=m(x,ix,v,8,'hsa');b=m(x,ix,v,8,'masked');e=(a-b).abs();tol=2e-5+2e-5*b.abs()
                    write_json(ROOT/f'results/numerical_trained_{seed}.json',{'elements':a.numel(),'outside':int((e>tol).sum()),
                        'max_abs':e.max().item(),'argmax_disagreements':int((a.argmax(-1)!=b.argmax(-1)).sum())})
                guard()
        write_json(ROOT/'results/summary.json',outcomes)
        status='COMPLETE'
    except Exception as e:
        status='TECHNICAL_STOP';write_json(ROOT/'failures/main_exception.json',{'phase':phase,'error':str(e),'trace':traceback.format_exc()})
        print(traceback.format_exc(),flush=True)
    finally:
        with open(ROOT/'results/losses.jsonl','w') as f:
            for row in losses:f.write(canonical(row).decode()+'\n')
        write_json(ROOT/'results/main_outcome.json',{'status':status,'phase':phase,'updates':updates,
            'seconds':time.perf_counter()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'payload_bytes':sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file()),'outcome_rows':len(outcomes)})
    return 0 if status=='COMPLETE' else 2
if __name__=='__main__':raise SystemExit(main())
