"""Full retained-panel engineering regression, not fresh confirmation or training."""
from __future__ import annotations
import gzip,time,resource
from support import *
from nss_hsa import *
import sh01_common as old

def main():
    setup();start=time.perf_counter();rows=[];comps=[];errors=[];models=[]
    for seed in [8801,8802,8804]:
        cp=torch.load(ROOT/f'checkpoints/{seed}_hsa_inference.pt',map_location='cpu',weights_only=True)
        legacy=old.Reader();legacy.load_state_dict(cp['model']);legacy.eval()
        clean=MaintenanceReader();clean.load_state_dict(cp['model']);clean.eval()
        assert model_sha(clean)==cp['model_hash']==model_sha(legacy)
        for split in ['development','confirmation','stress']:
            with gzip.open(ROOT/f'fixtures/{split}.jsonl.gz','rt') as f:ws=[json.loads(line) for line in f]
            original=np.load(ROOT/f'reference/pred_{seed}_hsa_{split}.npz');outputs=[];oldoutputs=[];targets=[]
            for off in range(0,len(ws),16):
                chunk=ws[off:off+16];x,ix,va,y=old.batch(chunk);xx,specs=prepare_worlds(chunk);assert torch.equal(x,xx);plan=compile_plan(specs)
                captures={}
                handles=[]
                def record(key):
                    return lambda module,args,out:captures.__setitem__(key,out.detach().clone())
                for j in range(2):
                    handles.append(legacy.blocks[j].register_forward_hook(record(f'old{j}')))
                    handles.append(clean.blocks[j].register_forward_hook(record(f'clean{j}')))
                with torch.no_grad():
                    a=legacy(x,ix,va,plan.tasks,'hsa');b=clean(xx,plan,checked=True)
                for h in handles:h.remove()
                with torch.no_grad():c=clean(xx,plan,'masked_reference')
                for label,aa,bb in [('logits_old',b,a),('logits_masked',b,c)]+[(f'block{j}',captures[f'clean{j}'],captures[f'old{j}']) for j in range(2)]:
                    co={'seed':seed,'split':split,'offset':off,'stage':label,**comparison(aa,bb)};comps.append(co)
                    if co['violations']:errors.append(co)
                outputs.append(b.numpy());oldoutputs.append(a.numpy());targets.append(y.numpy())
            new=np.concatenate(outputs);oldnew=np.concatenate(oldoutputs);target=np.concatenate(targets)
            assert np.array_equal(target,original['target'])
            row={'seed':seed,'split':split,'old_replay_bit_exact':bool(np.array_equal(oldnew,original['logits'])),
                 'clean_vs_saved':comparison(new,original['logits']),
                 'class_changes':int((new.argmax(-1)!=original['logits'].argmax(-1)).sum()),
                 **old.metrics(target,new.argmax(-1))}
            rows.append(row);np.savez_compressed(ROOT/f'results/clean_{seed}_{split}.npz',logits=new,target=target)
            save(ROOT/'results/regression_progress.json',{'rows':rows,'comparisons':comps,'failures':errors})
        models.append({'seed':seed,'tensor_hash':model_sha(clean),'unchanged':model_sha(clean)==cp['model_hash']})
    result={'rows':rows,'comparisons':comps,'models':models,'failures':errors,'runtime':runtime(),'optimizer_applications':0,
            'elapsed_seconds':time.perf_counter()-start,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'scope':'Exposed SH01 panels; same fitted weights; implementation regression, not new learning/generalization evidence.'}
    save(ROOT/'results/regression.json',result)
    print(json.dumps({'rows':rows,'total_stage_scalar_comparisons':sum(c['scalars'] for c in comps),'stage_violations':sum(c['violations'] for c in comps),'elapsed_seconds':result['elapsed_seconds']},indent=2))
    if errors or any(r['class_changes'] or not r['old_replay_bit_exact'] or r['clean_vs_saved']['violations'] for r in rows):raise SystemExit(1)
if __name__=='__main__':main()
