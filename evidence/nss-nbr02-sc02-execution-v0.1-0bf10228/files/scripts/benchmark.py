from support import *
from runner import execute,POLICIES
from fixture_factory import episode
import argparse,gc,statistics

def main():
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,required=True);p.add_argument('--fresh',action='store_true');a=p.parse_args()
 setup();model,mid=load(8801);start=time.perf_counter()
 seed=942203 if a.fresh else 932101
 families=['resume','churn','revisions','sweep']if a.fresh else ['reuse','sweep','churn','resume']
 reps=7 if a.fresh else 11
 r=np.random.default_rng((943901 if a.fresh else 942901)+a.n)
 scope='fresh'if a.fresh else 'retained'
 rows=[]
 for fam in families:
  ep=episode(a.n,seed,fam)
  save(ROOT/'results'/'timing_fixtures'/f'{scope}_{ep["id"]}.json',ep)
  # Explicit one complete-episode warmup per candidate/cell.
  for variant in POLICIES:execute(ep,model,mid,variant,audit=False)
  samples={v:[]for v in POLICIES};whole={v:[]for v in POLICIES};phases={v:[]for v in POLICIES};counts={};order=[]
  for rep in range(reps):
   gc.collect()
   round_order=[str(v)for v in r.permutation(POLICIES)];order.append(round_order)
   for variant in round_order:
    t=time.perf_counter();out=execute(ep,model,mid,variant,audit=False);whole[variant].append(time.perf_counter()-t)
    samples[variant].append(out['core_seconds']);phases[variant].append(out['phase_seconds'])
    counts[variant]={k:out[k]for k in ['stats','accounting_peak_payload','ingest_encoded_bytes','snapshots']}
  for variant in POLICIES:
   rows.append({'n':a.n,'family':fam,'variant':variant,'scope':scope,'seed':seed,'repetitions':reps,'samples_seconds':samples[variant],
                'whole_seconds':whole[variant],'phases':phases[variant],'median_ms':statistics.median(samples[variant])*1000,
                'q25_ms':float(np.quantile(samples[variant],.25))*1000,'q75_ms':float(np.quantile(samples[variant],.75))*1000,
                'minimum_ms':min(samples[variant])*1000,'maximum_ms':max(samples[variant])*1000,'order':order,**counts[variant]})
  save(ROOT/'results'/f'benchmark_{scope}_n{a.n}_progress.json',{'status':'PARTIAL','rows':rows,'runtime':runtime(),'elapsed_seconds':time.perf_counter()-start})
  print(scope,a.n,fam,[(v,round(statistics.median(samples[v])*1000,3))for v in POLICIES],flush=True)
  if runtime()['peak_rss_bytes']>2*1024**3 or time.perf_counter()-start>180:raise RuntimeError('BENCHMARK_RESOURCE_GUARD')
 save(ROOT/'results'/f'benchmark_{scope}_n{a.n}.json',{'status':'COMPLETE','rows':rows,'model_hash':mid,'runtime':runtime(),'elapsed_seconds':time.perf_counter()-start,'optimizer_applications':0})
if __name__=='__main__':main()
