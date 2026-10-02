from support import *
from run import execute,POLICIES
import argparse,gc,statistics

def main():
    p=argparse.ArgumentParser();p.add_argument('--n',required=True,type=int);args=p.parse_args()
    setup();m,mid=load(8801);r=np.random.default_rng(932901+args.n)
    families=['reuse','sweep','churn','resume'];rows=[];start=time.perf_counter()
    for family in families:
        ep=json.loads((ROOT/'fixtures'/f'n{args.n}_s932101_{family}.json').read_text())
        # One whole-episode warmup per policy, discarded only as prospectively specified.
        for policy in POLICIES:execute(ep,m,mid,policy,audit=False)
        samples={p:[]for p in POLICIES};whole={p:[]for p in POLICIES};counts={}
        for rep in range(9):
            for pol in r.permutation(POLICIES):
                gc.collect();t=time.perf_counter();out=execute(ep,m,mid,str(pol),audit=False);total=time.perf_counter()-t
                samples[pol].append(out['core_seconds']);whole[pol].append(total)
                counts[pol]={'stats':out['stats'],'accounting_peak_payload':out['accounting_peak_payload'],
                             'ingest_seconds':out['ingest_seconds'],'snapshots':out['snapshots']}
        for pol in POLICIES:
            rows.append({'n':args.n,'family':family,'policy':pol,'repetitions':9,'samples_seconds':samples[pol],
                         'observed_whole_seconds':whole[pol],'median_ms':statistics.median(samples[pol])*1000,
                         'minimum_ms':min(samples[pol])*1000,'maximum_ms':max(samples[pol])*1000,**counts[pol]})
        save(ROOT/'results'/f'benchmark_n{args.n}_progress.json',{'rows':rows,'elapsed':time.perf_counter()-start,'runtime':runtime()})
        print('benchmark',args.n,family,[(p,round(statistics.median(samples[p])*1000,3))for p in POLICIES],flush=True)
    save(ROOT/'results'/f'benchmark_n{args.n}.json',{'status':'COMPLETE','model':mid,'rows':rows,'elapsed':time.perf_counter()-start,'runtime':runtime(),'optimizer_applications':0})
if __name__=='__main__':main()
