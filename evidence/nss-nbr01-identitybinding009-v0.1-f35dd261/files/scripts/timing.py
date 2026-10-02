"""Current-host measured microbenchmarks, not target-device claims."""
from pathlib import Path
import sys,time,statistics,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import *
from nbr009.episodes import paired,build_state
from nbr009.stage_b import make_problem,install,maintain
from nbr009.readout import neural_read
setup();ms,h,cfg=load_pair(1);rs={k:make_resolver(k,ms,h,cfg) for k in ('nearest','A_nearest','B_nearest')};rows=[]

def bench(label,b,fn):
    for _ in range(5):fn()
    vals=[]
    for _ in range(50):
        t=time.perf_counter();fn();vals.append((time.perf_counter()-t)*1000)
    rows.append({'label':label,'batch':b,'repetitions':50,'warmups':5,'median_ms':float(np.median(vals)),'mean_ms':float(np.mean(vals)),'p95_ms':float(np.quantile(vals,.95))})

with torch.no_grad():
 for b in (1,64):
    p=paired(74950000,b,'source10');rr=np.arange(b);new=p['ids'][:,1];v=torch.from_numpy(p['codes'][rr,p['ids'][:,3]])
    for mode,kind in (('identity','parent'),('learned','near'),('guarded','near')):
        s=build_state(p,load_binder(1,kind),mode=mode);rg=s.register(torch.from_numpy(p['codes'][rr,new]))
        bench('clone_plus_write_'+mode,b,lambda:s.clone().event(rg['handle'],v))
    # make_problem uses half missing halves, so batch-one is sliced from paired b2.
    pp=make_problem(74950100,8,max(2,b));pp={k:x[:b] for k,x in pp.items()};s=install(pp,ms['binder']);s.add_noise(np.random.default_rng(3),.02)
    for policy in ('shared_A','internal_A','nearest'):
        bench('clone_plus_sweep_'+policy,b,lambda:maintain(s.clone(),policy,rs))
    for depth in (1,2,4,8):bench('query_d'+str(depth),b,lambda:neural_read(s,ms['record_hop'],rs['A_nearest'],torch.from_numpy(pp['q']),depth))
    rows.append({'label':'raw_state','batch':b,'bytes':s.bytes(),'bytes_per_stream':s.bytes()/b,'fields':{k:getattr(s,k).numel()*getattr(s,k).element_size()/b for k in s.tensor_names}})
dump(ROOT/'evidence/TIMING.json',{'status':'RUN','notes':['Single process one PyTorch thread; old and new learned weights frozen.','Write/sweep timings explicitly include state clone. Query includes signature checks and decoding.','Not a best-tuned architecture comparison; interpreter RSS includes framework and fixture.','Original fitting peak was not separately instrumented.'], 'env':env(),'rss_max_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'rows':rows})
