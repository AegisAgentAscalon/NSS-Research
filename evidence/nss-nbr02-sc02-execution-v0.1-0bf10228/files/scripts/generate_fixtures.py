from support import *
from fixture_factory import episode

def create():
    all_f=[]
    for n in [8,32,128]:
      for seed in [942201,942202]:
        for fam in ['reuse','sweep','churn','revisions','resume','oversize','eviction','global']:
            src='sweep'if fam=='eviction'else'reuse'if fam=='global'else fam
            ep=episode(n,seed,src);ep['family']=fam;ep['id']=f'n{n}_s{seed}_{fam}'
            if fam=='eviction':
                ep['result_cap']=4;ep['events'].insert(6,{'op':'checkpoint'})
            if fam=='global':
                events=[]
                for i,event in enumerate(ep['events']):
                    if i%3==0:events.append({'op':'change','change':{'field':'freeze'}})
                    if i==6:events.append({'op':'checkpoint'})
                    events.append(event)
                ep['events']=events
            dest=ROOT/'fixtures'/f'{ep["id"]}.json'
            if dest.exists():raise RuntimeError('fixture already exists')
            save(dest,ep);all_f.append({'file':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    save(ROOT/'FIXTURE_LOCK.json',{'fixtures':all_f,'generated_utc':runtime()['utc'],'count':len(all_f)})
    print('generated',len(all_f),'fresh episodes')
if __name__=='__main__':create()
