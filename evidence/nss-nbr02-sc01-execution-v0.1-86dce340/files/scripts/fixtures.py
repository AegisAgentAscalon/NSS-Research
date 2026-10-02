"""Fixed fresh episodes. Generates observable records, never selected for scores."""
from support import *
from sh01_common import worlds
FAMILIES=['reuse','sweep','churn','revisions','resume','oversize']
SIZES=[8,32,128]
CAPS={8:40,32:128,128:384}
LOW_CAPS={8:16,32:32,128:128}
SEEDS=[932101,932102]

def episode(n,seed,family):
    import copy
    w=worlds(seed+n*1000,1,n)[0]
    r=np.random.default_rng(seed+n*1000+13)
    base=r.choice(n,min(8,n),replace=False).tolist()
    ev=[]
    if family=='resume':
        tasks=list(range(min(n,12)))
        ev.extend([{'op':'job','id':'paused','tasks':tasks,'limit_tasks':2},
                   {'op':'checkpoint'},
                   {'op':'change','change':{'field':'progress','task':w['deps'][tasks[0]][0]}}])
    for j in range(12):
        if family=='sweep':targets=[int((8*j+k)%n)for k in range(min(8,n))]
        else:targets=base[j%len(base):]+base[:j%len(base)]
        if family=='churn':ev.append({'op':'change','change':{'field':'progress','task':base[j%len(base)]}})
        if family=='revisions' and j in [3,6,9]:
            if j==3:change={'field':'receipts','task':int((base[0]+n//2)%n)}
            elif j==6:
                t=base[0];choices=[i for i in range(n)if i!=t and i not in w['deps'][t]]
                change={'field':'dependency','task':t,'value':choices[:2]}
            else:change={'field':'freeze'}
            ev.append({'op':'change','change':change})
        if family=='resume' and j==6:
            ev.extend([{'op':'checkpoint'},{'op':'job','id':'paused','tasks':tasks}])
        ev.append({'op':'job','id':f'J{j}','tasks':targets})
    return {'schema':'nss.sc01.episode.v1','id':f'n{n}_s{seed}_{family}','n':n,'seed':seed,'family':family,
            'record_cap':LOW_CAPS[n]if family=='oversize'else CAPS[n], 'result_cap':32,'world':w,'events':ev}

def generate():
    for n in SIZES:
        for seed in SEEDS:
            for family in FAMILIES:
                e=episode(n,seed,family);save(ROOT/'fixtures'/f"{e['id']}.json",e)
if __name__=='__main__':generate()
