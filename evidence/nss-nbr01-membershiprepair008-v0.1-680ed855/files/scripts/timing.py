"""Local CPU implementation timings, not target-device predictions."""
from pathlib import Path
import sys,time,json,resource
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import *
from nbr008.config import *
from nbr008.pipeline import *

@torch.no_grad()
def main():
 setup();models=parents(1);h,cfg=load_gate(1001);rows=[]
 for b in (1,64):
  # Generator uses half complete/half missing; slice from two for latency1.
  p=make_problem(78000000,4,max(2,b));p={k:v[:b] for k,v in p.items()}
  for m in ('nearest','learned','A_nearest','B_nearest','A_learned','B_learned'):
   r=resolver(m,models,h,cfg);s=install(p,models['binder']);x=s.store.keys.clone()
   x+=torch.from_numpy(np.random.default_rng(100).normal(0,.02,x.shape).astype(np.float32))
   for _ in range(10):r(x,s.book,s.active)
   samples=[]
   for _ in range(50):
    t=time.perf_counter_ns();r(x,s.book,s.active);samples.append((time.perf_counter_ns()-t)/1e6)
   rows.append({'batch':b,'method':m,'operation':'one_field_16_records','median_ms':float(np.median(samples)),'p10_ms':float(np.quantile(samples,.1)),'p90_ms':float(np.quantile(samples,.9)),'repeats':50,'state_bytes_per_stream':s.bytes()/b})
   for _ in range(3):read(s,models['record_hop'],r,torch.from_numpy(p['q']),8)
   samples=[]
   for _ in range(20):
    t=time.perf_counter_ns();read(s,models['record_hop'],r,torch.from_numpy(p['q']),8);samples.append((time.perf_counter_ns()-t)/1e6)
   rows.append({'batch':b,'method':m,'operation':'eight_query_rounds_with_decodes','median_ms':float(np.median(samples)),'p10_ms':float(np.quantile(samples,.1)),'p90_ms':float(np.quantile(samples,.9)),'repeats':20})
 # Torch profiler attributes explicit CPU allocations to operators; sums are not peak RSS.
 r=resolver('B_learned',models,h,cfg);p=make_problem(7888,4,64);s=install(p,models['binder'])
 with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU],profile_memory=True) as prof:
  r(s.store.keys,s.book,s.active)
 allocs=[{'op':x.key,'self_cpu_memory_bytes':x.self_cpu_memory_usage,'cpu_memory_bytes':x.cpu_memory_usage} for x in prof.key_averages() if x.cpu_memory_usage>0]
 weight_bytes={k:sum(p.numel()*p.element_size() for p in m.parameters()) for k,m in {**models,'head':h}.items()}
 dump(ROOT/'evidence/RESOURCES.json',{'rows':rows,'resident_parameter_bytes':weight_bytes,'raw_state_example':{'record_keys_values':16*17*4*2,'presence_readability_flags':16*3,'reference_values':16*17*4,'active_mask':16,'reference_revision':8,'per_stream':s.bytes()/64},'allocation_profile':allocs,'environment':env(),'notes':['all candidate parents loaded together in harness; per-arm deployment residency differs','latencies include Python and validation; no optimized kernel or hardware-noise claim','head633 parameters; training gradient and AdamW state additionally counted','codebook is protected exact reference without graph edges; audit logs not available to inference']})
if __name__=='__main__':main()
