from __future__ import annotations
import gzip,json,math,resource,time
from pathlib import Path
import numpy as np
import torch
from common import *
from store import *
ROOT=Path(__file__).resolve().parents[1]

def load_model(seed,mode):
    cp=torch.load(ROOT/f'checkpoints/{seed}_{mode}_0600.pt',weights_only=False,map_location='cpu')
    m=Reader();m.load_state_dict(cp['model']);m.eval();return m

def integration():
    # Exposed only after training. Same distribution but a separate fixture seed, prospective here.
    ws=worlds(776001,16,8);rows=[];all_preds={};store_stats=[]
    with gzip.open(ROOT/'fixtures/integration.jsonl.gz','wt') as f:
        for w in ws:f.write(canonical(w).decode()+'\n')
    for seed in [8801,8802,8803,8804]:
        for mode in ['dense','hsa']:
            m=load_model(seed,mode)
            for persistent in [False,True]:
                preds=[];targets=[];trace=[];mt=0.;ct=0.;nt=0.;cold=0.;outbytes=0;sourcebytes=0;hits=0;builds=0;inval=0
                for wi,w in enumerate(ws):
                    start=time.perf_counter();s=store_from_world(w);manager=Manager(s,persistent);cold+=time.perf_counter()-start
                    for job in range(6):
                        if job==3:
                            r=s.get(1,'P');r['revision']+=1;r['progress']=1-r['progress'];r['source']+=':changed';s.publish(r)
                        if job==4:
                            # A true serialized checkpoint/restore, with receipts and caches.
                            snap=canonical({'store':s.dump(),'manager':manager.snapshot()})
                            decoded=json.loads(snap);s=VersionedStore.restore(decoded['store']);old=manager
                            hits+=old.hits;builds+=old.builds;inval+=old.invalidations;sourcebytes+=old.store.read_bytes
                            manager=Manager.restore(s,decoded['manager']);s.read_bytes=0
                        t=time.perf_counter();b=manager.packet(list(range(8)),freeze=w['freeze']);mt+=time.perf_counter()-t
                        outbytes+=len(b);t=time.perf_counter();ww=world_from_packet(b);x,ix,v,y=batch([ww]);ct+=time.perf_counter()-t
                        t=time.perf_counter()
                        with torch.no_grad():p=m(x,ix,v,8,mode).argmax(-1).numpy()[0]
                        nt+=time.perf_counter()-t
                        preds.append(p);targets.append(y.numpy()[0]);trace.append({'world':wi,'job':job,'packet_sha':sha(b)})
                    hits+=manager.hits;builds+=manager.builds;inval+=manager.invalidations;sourcebytes+=s.read_bytes
                p=np.stack(preds);y=np.stack(targets);row=metrics(y,p)
                row.update({'seed':seed,'reader':mode,'manager':'segmented' if persistent else 'simple','jobs':len(y),
                    'manager_seconds':mt,'compile_seconds':ct,'reader_seconds':nt,'cold_index_seconds':cold,
                    'packet_bytes_delivered':outbytes,'source_bytes_decoded':sourcebytes,'cache_hits':hits,
                    'packet_builds':builds,'invalidations':inval})
                rows.append(row);name=f"integration_{seed}_{mode}_{row['manager']}"
                np.savez_compressed(ROOT/f'results/{name}.npz',pred=p,target=y)
                write_json(ROOT/f'results/{name}_packets.json',trace)
                all_preds[(seed,mode,persistent)]=(p,trace)
    eq=[]
    for seed in [8801,8802,8803,8804]:
        for mode in ['dense','hsa']:
            a,at=all_preds[(seed,mode,False)];b,bt=all_preds[(seed,mode,True)]
            eq.append({'seed':seed,'reader':mode,'packet_equal':at==bt,'pred_equal':bool(np.array_equal(a,b))})
    write_json(ROOT/'results/integration.json',{'rows':rows,'manager_equivalence':eq,
          'caveat':'Record decode and full reader compilation still occur on cache hits; no hidden KV-cache reuse. Resume serialization latency is separately benchmarked; timeline rows exclude that checkpoint operation.'})

def benchmark():
    rows=[];torch.manual_seed(778000)
    # Same model weights for both kernels: execution comparison, not a new fit.
    model=load_model(8801,'dense')
    for n in [8,32,128]:
        w=worlds(777000+n,1,n)[0];x,idx,valid,y=batch([w]);tt=x.shape[1];kw=idx.shape[-1]
        with torch.no_grad():
            for _ in range(3):
                model(x,idx,valid,n,'dense');model(x,idx,valid,n,'hsa')
            samples={'dense':[],'hsa':[]}
            for rep in range(15):
                for mode in (['dense','hsa'] if rep%2==0 else ['hsa','dense']):
                    t=time.perf_counter_ns();model(x,idx,valid,n,mode);samples[mode].append(time.perf_counter_ns()-t)
        for mode,times in samples.items():
            rows.append({'tasks':n,'positions':tt,'mode':mode,'ns':times,'median_ms':float(np.median(times)/1e6),
                'q25_ms':float(np.percentile(times,25)/1e6),'q75_ms':float(np.percentile(times,75)/1e6),
                'logical_score_cells_per_head_layer':tt*tt if mode=='dense' else int(valid.sum()),
                'padded_score_cells_per_head_layer':tt*tt if mode=='dense' else tt*kw,
                'sparse_kv_gather_bytes_per_layer':2*tt*kw*32*4 if mode=='hsa' else None,
                'input_and_indices_bytes':sum(z.numel()*z.element_size() for z in (x,idx,valid)),
                'note':'Dense SDPA may avoid materializing logical T*T scores. Gather bytes are actual tensor payload, not peak RSS.'})
    # Timed lifecycle cycles charge cold indexing, changed dependency, and serialized restart.
    managerial=[]
    for n in [8,32,128]:
        w=worlds(778000+n,1,n)[0]
        for persistent in [False,True]:
            samples=[];cache_sizes=[];read_sizes=[];delivered=[];buildcounts=[]
            for rep in range(15):
                t=time.perf_counter_ns();s=store_from_world(w);m=Manager(s,persistent,budget=500_000)
                roots=list(range(n));total=0
                for job in range(6):
                    if job==3:
                        r=s.get(1,'P');r['revision']+=1;r['progress']=1-r['progress'];s.publish(r)
                    if job==4:
                        raw=canonical({'store':s.dump(),'manager':m.snapshot()});d=json.loads(raw)
                        s2=VersionedStore.restore(d['store']);s2.read_bytes=s.read_bytes
                        old_builds=m.builds;s=s2;m=Manager.restore(s,d['manager']);m.builds=old_builds
                    b=m.packet(roots,freeze=w['freeze']);total+=len(b)
                    world_from_packet(b)
                samples.append(time.perf_counter_ns()-t);cache_sizes.append(len(canonical(m.snapshot())))
                read_sizes.append(s.read_bytes);delivered.append(total);buildcounts.append(m.builds)
            managerial.append({'tasks':n,'manager':'segmented' if persistent else 'simple','cycle_ns':samples,
                'median_cycle_ms':float(np.median(samples)/1e6),'cache_snapshot_bytes':cache_sizes,
                'source_bytes_decoded':read_sizes,'packet_bytes_delivered':delivered,'builds':buildcounts,
                'includes':'6 jobs, store/index construction, packet JSON decode, one source update, checkpoint serialization and restore. Excludes neural reader and feature compilation.'})
    write_json(ROOT/'results/benchmark.json',{'reader_rows':rows,'manager_rows':managerial,
              'threads':torch.get_num_threads(),'batch_size':1,'scope':'CPU first-prototype timings; no energy or language-token measurement.'})

def audit():
    # Fresh-process final-weight replay for all saved development/confirmation/stress arrays.
    rows=[];recounts=[];checkpoints=[]
    datasets={}
    for split in ['development','confirmation','stress']:
        with gzip.open(ROOT/f'fixtures/{split}.jsonl.gz','rt') as f:ws=[json.loads(line) for line in f]
        datasets[split]=batch(ws)
    for p in sorted((ROOT/'checkpoints').glob('*.pt')):
        cp=torch.load(p,weights_only=False,map_location='cpu');m=Reader();m.load_state_dict(cp['model'])
        checkpoints.append({'file':p.name,'model_hash_ok':model_hash(m)==cp['model_hash']})
    summary=json.loads((ROOT/'results/summary.json').read_text())
    for seed in [8801,8802,8803,8804]:
        for mode in ['dense','hsa']:
            model=load_model(seed,mode)
            for split,n in [('development',8),('confirmation',8),('stress',16)]:
                p=ROOT/f'results/pred_{seed}_{mode}_{split}.npz';a=np.load(p);parts=datasets[split];logs=[]
                with torch.no_grad():
                    for i in range(0,len(parts[0]),16):
                        x,ix,v,y=[z[i:i+16] for z in parts];logs.append(model(x,ix,v,n,mode).numpy())
                new=np.concatenate(logs);exact=np.array_equal(new,a['logits'])
                rows.append({'file':p.name,'bit_exact':exact,'max_abs':float(np.max(np.abs(new-a['logits'])))})
                # Scalar-loop independent recount (does not call metrics()).
                p2=np.argmax(a['logits'],axis=-1);tar=a['target'];correct=0;whole=0;falsec=0
                for yy,pp in zip(tar.tolist(),p2.tolist()):
                    c=sum(int(u==v) for u,v in zip(yy,pp));correct+=c;whole+=int(c==len(yy))
                    falsec+=sum(int(v==1 and u!=1) for u,v in zip(yy,pp))
                row=next(r for r in summary if r['seed']==seed and r['mode']==mode and r['split']==split)
                recounts.append({'file':p.name,'ok':correct==row['correct'] and whole==row['whole_correct'] and falsec==row['false_complete']})
    write_json(ROOT/'results/audit.json',{'replays':rows,'recounts':recounts,'checkpoints':checkpoints,
       'optimizer_updates':0,'scope':'same-source fresh-process replay plus independent scalar count; not external replication.'})

if __name__=='__main__':
    setup();t=time.perf_counter();integration();benchmark();audit()
    write_json(ROOT/'results/post_execution_cost.json',{'seconds':time.perf_counter()-t,'optimizer_updates':0,
       'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024})
    print('integration benchmark audit complete',flush=True)
