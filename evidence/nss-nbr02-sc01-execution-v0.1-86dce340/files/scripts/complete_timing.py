"""Post-lock operational continuation only; no changes to experiment semantics."""
from support import *
from run import execute,POLICIES
import gc,statistics

def main():
    setup();n=8;m,mid=load(8801);r=np.random.default_rng(932901+n)
    for _ in range(27):r.permutation(POLICIES)
    old=json.loads((ROOT/'results/benchmark_n8_progress.json').read_text())
    assert {x['family']for x in old['rows']}=={'reuse','sweep','churn'}
    ep=json.loads((ROOT/'fixtures/n8_s932101_resume.json').read_text());start=time.perf_counter()
    for policy in POLICIES:execute(ep,m,mid,policy,audit=False)
    samples={p:[]for p in POLICIES};whole={p:[]for p in POLICIES};counts={}
    for rep in range(9):
        for pol in r.permutation(POLICIES):
            gc.collect();t=time.perf_counter();out=execute(ep,m,mid,str(pol),audit=False);total=time.perf_counter()-t
            samples[pol].append(out['core_seconds']);whole[pol].append(total)
            counts[pol]={'stats':out['stats'],'accounting_peak_payload':out['accounting_peak_payload'],'ingest_seconds':out['ingest_seconds'],'snapshots':out['snapshots']}
    added=[]
    for pol in POLICIES:
        added.append({'n':n,'family':'resume','policy':pol,'repetitions':9,'samples_seconds':samples[pol],
                      'observed_whole_seconds':whole[pol],'median_ms':statistics.median(samples[pol])*1000,
                      'minimum_ms':min(samples[pol])*1000,'maximum_ms':max(samples[pol])*1000,**counts[pol]})
    save(ROOT/'results/benchmark_n8_completion.json',{'rows':added,'runtime':runtime(),'elapsed':time.perf_counter()-start})
    save(ROOT/'results/benchmark_n8.json',{'status':'COMPLETE_TWO_PROCESSES','model':mid,'rows':old['rows']+added,
                'elapsed':'first terminal unavailable; first saved prefix and continuation separately retained','runtime':runtime(),'optimizer_applications':0})
    print([(x['policy'],x['median_ms'])for x in added])
if __name__=='__main__':main()
