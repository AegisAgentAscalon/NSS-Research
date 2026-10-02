"""Operational recovery: finish only not-yet-started scheduled fits; never replay uncertain updates."""
from __future__ import annotations
import gzip,json,time,resource
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import torch
from common import *
from run import save,evaluate,ROOT

def load_data():
    data={}
    for split in ['train','development','confirmation','stress']:
        with gzip.open(ROOT/f'fixtures/{split}.jsonl.gz','rt') as f:ws=[json.loads(line) for line in f]
        data[split]=batch(ws)
    return data

def main():
    setup();start=time.perf_counter();data=load_data()
    assert not (ROOT/'checkpoints/8804_dense_0000.pt').exists()
    assert not (ROOT/'checkpoints/8804_hsa_0000.pt').exists()
    # Interrupted prefix known3200 and upper3400 applications. Finish1200 =>4400..4600 <=4800.
    original=json.loads((ROOT/'SOURCE_LOCK.json').read_text())
    for name,entry in original['files'].items():
        assert sha((ROOT/name).read_bytes())==entry['sha256'],name
    write_json(ROOT/'results/interruption_receipt.json',{
        'status':'EXTERNAL_RUNNER_INTERRUPTION','observed_at_utc':datetime.now(timezone.utc).isoformat(),
        'completed_fits':[[8801,'dense'],[8801,'hsa'],[8802,'dense'],[8802,'hsa'],[8803,'dense']],
        'incomplete_fit':[8803,'hsa'],'last_durable_step':200,'unknown_suffix_updates':[0,200],
        'main_applications_lower_before':3200,'main_applications_upper_before':3400,
        'planned_remaining':[ [8804,'dense'],[8804,'hsa'] ],'remaining_applications':1200,
        'policy':'Do not replay interrupted fit or pick an intermediate endpoint. Finish untouched scheduled fits only; no replacement seed or gate change.',
        'source_extension_hash':sha(Path(__file__).read_bytes()),
        'lost_evidence':'Interrupted process exact terminal time/RSS, unsaved per-step loss list and exact applications after last checkpoint unavailable.'})
    actual=0
    with open(ROOT/'results/continuation_losses.jsonl','w',buffering=1) as f:
        for mode in ['dense','hsa']:
            torch.manual_seed(8804);m=Reader();init=model_hash(m);save(m,None,8804,mode,0)
            opt=torch.optim.AdamW(m.parameters(),lr=.002,betas=(.9,.999),eps=1e-8,weight_decay=.01,foreach=False,fused=False)
            t=time.perf_counter()
            for step in range(1,601):
                a=(step-1)*16;x,ix,v,y=[z[a:a+16] for z in data['train']]
                opt.zero_grad(set_to_none=True);log=m(x,ix,v,8,mode);loss=F.cross_entropy(log.reshape(-1,4),y.reshape(-1))
                loss.backward();norm=torch.nn.utils.clip_grad_norm_(m.parameters(),1.,error_if_nonfinite=True);opt.step();actual+=1
                f.write(canonical({'seed':8804,'mode':mode,'step':step,'loss':loss.item(),'gradnorm':norm.item()}).decode()+'\n')
                if step%200==0:
                    save(m,opt,8804,mode,step);print('train',8804,mode,step,loss.item(),flush=True)
            write_json(ROOT/f'results/fit_8804_{mode}.json',{'seed':8804,'mode':mode,'initial_hash':init,
                  'final_hash':model_hash(m),'updates':600,'seconds':time.perf_counter()-t})
    outcomes=[]
    completed=[(s,m) for s in [8801,8802,8803,8804] for m in ['dense','hsa'] if (ROOT/f'checkpoints/{s}_{m}_0600.pt').exists()]
    for seed,mode in completed:
        cp=torch.load(ROOT/f'checkpoints/{seed}_{mode}_0600.pt',weights_only=False,map_location='cpu')
        m=Reader();m.load_state_dict(cp['model']);assert model_hash(m)==cp['model_hash']
        for split,n in [('development',8),('confirmation',8),('stress',16)]:
            logits,row=evaluate(m,split,data[split],mode,n)
            np.savez_compressed(ROOT/f'results/pred_{seed}_{mode}_{split}.npz',logits=logits,target=data[split][-1].numpy())
            row.update({'seed':seed,'mode':mode,'split':split,'functional_target_met':row['accuracy']>=.95 and row['macro_recall']>=.90})
            outcomes.append(row);print('eval',seed,mode,split,row['accuracy'],row['macro_recall'],flush=True)
        if mode=='hsa':
            x,ix,v,y=[z[:8] for z in data['confirmation']]
            with torch.no_grad():
                a=m(x,ix,v,8,'hsa');b=m(x,ix,v,8,'masked');e=(a-b).abs()
            write_json(ROOT/f'results/numerical_trained_{seed}.json',{'elements':a.numel(),'outside':int((e>2e-5+2e-5*b.abs()).sum()),
                 'max_abs':e.max().item(),'argmax_disagreements':int((a.argmax(-1)!=b.argmax(-1)).sum())})
    write_json(ROOT/'results/summary.json',outcomes)
    write_json(ROOT/'results/main_outcome.json',{'status':'PARTIAL_TRAINING_COMPLETE_AVAILABLE_EVALUATION',
       'completed_fits':len(completed),'planned_fits':8,'paired_seeds':[8801,8802,8804],
       'missing_final':{'seed':8803,'mode':'hsa','reason':'external runner interruption','last_durable_step':200},
       'actual_main_applications_lower':3200+actual,'actual_main_applications_upper':3400+actual,
       'preflight_applications':4,'main_cap':4800,'no_uncertain_updates_replayed':True,
       'continuation_seconds':time.perf_counter()-start,'continuation_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
       'initial_process_terminal_seconds':None,'initial_process_peak_rss':None,'confirmation_result_rows':len(outcomes)})
if __name__=='__main__':main()
