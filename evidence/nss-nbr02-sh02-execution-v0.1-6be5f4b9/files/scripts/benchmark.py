"""Fixed-condition interleaved CPU timings, cold-plan costs and operator profiles."""
from __future__ import annotations
import resource,time,os
from support import *
from nss_hsa import *
import sh01_common as old

def stats(times):return {'ns':times,'median_ms':float(np.median(times)/1e6),'q25_ms':float(np.percentile(times,25)/1e6),'q75_ms':float(np.percentile(times,75)/1e6)}

def main():
    setup();start=time.perf_counter();rng=np.random.default_rng(952001);rows=[];cold=[];profiles=[]
    cp=torch.load(ROOT/'checkpoints/8801_hsa_inference.pt',weights_only=True,map_location='cpu')
    oldm=old.Reader();oldm.load_state_dict(cp['model']);oldm.eval()
    newm=MaintenanceReader();newm.load_state_dict(cp['model']);newm.eval()
    for batch,n in [(1,8),(1,32),(1,128),(1,512),(16,8),(16,32),(16,128)]:
        ws=old.worlds(951000+n+batch, batch,n);x,ix,va,y=old.batch(ws);xx,ss=prepare_worlds(ws);assert torch.equal(x,xx);plan=compile_plan(ss)
        fns={'old_gather':lambda:oldm(x,ix,va,n,'hsa'),'packed_hsa':lambda:newm(xx,plan),'full_dense':lambda:newm(xx,plan,'full_dense')}
        samples={name:[] for name in fns};orders=[]
        with torch.no_grad():
            for _ in range(5):
                for fn in fns.values():fn()
            for rep in range(31):
                order=list(rng.permutation(list(fns)));orders.append(order)
                for name in order:
                    ts=time.perf_counter_ns();fns[name]();samples[name].append(time.perf_counter_ns()-ts)
        accounting=plan.accounting();accounting['legacy_kv_payload_bytes_per_layer']=2*batch*x.shape[1]*ix.shape[-1]*32*4
        accounting['legacy_padded_pairs_per_head_layer_batch']=batch*x.shape[1]*ix.shape[-1]
        for name,ts in samples.items():rows.append({'batch':batch,'tasks':n,'positions':plan.positions,'backend':name,**stats(ts)})
        sizes={'batch':batch,'tasks':n,'accounting':accounting,'order':orders}
        # Cold compilation and plan-cache lookup are outside reader-only timings.
        cc={'graph_plan':[],'features_and_specs':[],'warm_cache_lookup':[],'full_cold_pipeline':[],'checked_entry_reader':[]}
        cache=PlanCache(2);cache.get(ss)
        with torch.no_grad():
            for rep in range(15):
                ts=time.perf_counter_ns();compile_plan(ss);cc['graph_plan'].append(time.perf_counter_ns()-ts)
                ts=time.perf_counter_ns();prepare_worlds(ws);cc['features_and_specs'].append(time.perf_counter_ns()-ts)
                ts=time.perf_counter_ns();cache.get(ss);cc['warm_cache_lookup'].append(time.perf_counter_ns()-ts)
                ts=time.perf_counter_ns();x0,s0=prepare_worlds(ws);p0=compile_plan(s0);newm(x0,p0);cc['full_cold_pipeline'].append(time.perf_counter_ns()-ts)
                ts=time.perf_counter_ns();newm(xx,plan,checked=True);cc['checked_entry_reader'].append(time.perf_counter_ns()-ts)
        sizes['costs']={k:stats(v) for k,v in cc.items()};cold.append(sizes)
        print('BENCH',batch,n,{k:round(stats(v)['median_ms'],4) for k,v in samples.items()},flush=True)
        save(ROOT/'results/benchmark_progress.json',{'reader_rows':rows,'preparation':cold})
        if n==128:
            for name,fn in fns.items():
                with torch.no_grad():
                    for _ in range(3):fn()
                    with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU],record_shapes=True,profile_memory=True) as prof:
                        for _ in range(5):fn()
                ops=[]
                for e in prof.key_averages(group_by_input_shape=True):
                    ops.append({'operator':e.key,'count':e.count,'self_cpu_us':e.self_cpu_time_total,'total_cpu_us':e.cpu_time_total,
                                'self_cpu_memory_bytes':e.self_cpu_memory_usage,'total_cpu_memory_bytes':e.cpu_memory_usage,'input_shapes':e.input_shapes})
                ops.sort(key=lambda a:a['self_cpu_us'],reverse=True)
                profiles.append({'batch':batch,'tasks':n,'backend':name,'calls':5,'operators':ops,
                                 'profiled_positive_self_alloc_bytes':sum(max(0,o['self_cpu_memory_bytes']) for o in ops),
                                 'note':'Positive allocation sum over 5 forwards, not peak-live memory; profiler adds overhead and may hold tensors.'})
                save(ROOT/f'results/profile_b{batch}_{name}.json',profiles[-1])
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024>2*1024**3:raise RuntimeError('PROCESS_RSS_CAP')
    result={'runtime':runtime(),'reader_rows':rows,'preparation':cold,'profile_files':[f"profile_b{p['batch']}_{p['backend']}.json" for p in profiles],
            'optimizer_applications':0,'elapsed_seconds':time.perf_counter()-start,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'limitations':['CPU one machine/session; no GPU or energy measurement','full_dense is different graph; only old_gather/packed preserve operator','512-task size is cost only, not competence testing','reader timing excludes plan preparation; cold costs reported separately','native allocation totals are not whole-process peak advantage']}
    save(ROOT/'results/benchmark.json',result);print('COMPLETE',result['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
