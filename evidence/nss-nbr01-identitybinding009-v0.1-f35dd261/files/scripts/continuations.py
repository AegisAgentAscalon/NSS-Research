"""Independent-process state/RNG/transaction/query continuation, no fitting."""
from pathlib import Path
import sys,argparse,subprocess,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import *
from nbr009.state import OwnedState
from nbr009.episodes import paired,build_state
from nbr009.readout import neural_read
from nbr009.stage_b import maintain

def finish(s,rng,query,tx,c,ms,rs):
    if c['case'] in ('precommit','stale_precommit'):s.commit(tx)
    if c['case']=='mid_recovery':
        for _ in range(24):
            s.add_noise(rng,.02)
            if s.tick%8==0:maintain(s,'internal_A',rs)
    q=torch.from_numpy(np.asarray(c['query'],np.float32))
    result=neural_read(s,ms['record_hop'],rs['nearest'],q,5 if c['case']=='mid_query' else 8,qs=query or None)
    out=s.arrays();out.update(answer=result['pred'].numpy(),next_rng=rng.normal(size=(17,)).astype(np.float32),final_h=result['qs']['h'].numpy(),final_alive=result['qs']['alive'].numpy(),final_round=result['qs']['round'].numpy())
    return out

def create(folder):
    folder.mkdir(parents=True,exist_ok=True);cases=[]
    for pair in range(1,6):
        ms,h,cfg=load_pair(pair);rs={k:make_resolver(k,ms,h,cfg) for k in ('nearest','A_nearest','B_nearest')}
        for name,mode,kind in [('identity','identity','parent'),('parent','learned','parent'),('near','learned','near'),('guard_near','guarded','near')]:
            binder=load_binder(pair,kind)
            for ci,case in enumerate(('precommit','stale_precommit','mid_recovery','mid_query')):
                seed=74900000+pair*1000+ci;p=paired(seed,8,'ordinary');s=build_state(p,binder,mode);rng=np.random.default_rng(seed+33)
                old,new,room=[p['ids'][:,j] for j in (0,1,2)];r=np.arange(8);query={};tx={}
                if case in ('precommit','stale_precommit'):
                    tx=s.prepare(old,torch.from_numpy(p['codes'][r,room]))
                    if case=='stale_precommit':s.event(old,torch.from_numpy(p['codes'][r,p['ids'][:,3]]))
                elif case=='mid_recovery':
                    for _ in range(8):s.add_noise(rng,.02)
                    maintain(s,'internal_A',rs)
                else:query=neural_read(s,ms['record_hop'],rs['nearest'],torch.from_numpy(p['codes'][r,old]),3)['qs']
                label=f'p{pair}_{name}_{case}';contract={'case':case,'models':model_hashes(ms),'kind':kind,'scope':'study','source_abi':'nbr009-owner-state-v1'}
                config={'pair':pair,'kind':kind,'case':case,'label':label,'contract':contract,'query':p['codes'][r,old].tolist()}
                path=folder/(label+'.npz');s.save(path,rng,contract,query=query,transaction=tx)
                expected=finish(s,rng,query,tx,config,ms,rs);np.savez_compressed(folder/(label+'_expected.npz'),**expected);cases.append(config)
    dump(folder/'cases.json',cases)

def child(folder):
    cases=json.loads((folder/'cases.json').read_text());ok=[]
    for c in cases:
        ms,h,cfg=load_pair(c['pair']);rs={k:make_resolver(k,ms,h,cfg) for k in ('nearest','A_nearest','B_nearest')};binder=load_binder(c['pair'],c['kind'])
        s,rng,q,tx=OwnedState.load(folder/(c['label']+'.npz'),binder,c['contract']);actual=finish(s,rng,q,tx,c,ms,rs)
        with np.load(folder/(c['label']+'_expected.npz'),allow_pickle=False) as a:
            assert set(a.files)==set(actual)
            for k in a.files:
                if not np.array_equal(a[k],actual[k]):raise AssertionError(c['label']+' '+k)
        ok.append(c['label'])
    dump(folder/'CONTINUATION_RESULT.json',{'status':'PASS','fresh_interpreter':True,'count':len(ok),'cases':ok,'utc':utc()});print('continuations PASS',len(ok))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True);p.add_argument('--child',action='store_true');p.add_argument('--verify-only',action='store_true');a=p.parse_args();setup()
    if a.child:child(a.folder)
    else:
        if not a.verify_only:create(a.folder)
        subprocess.run([sys.executable,__file__,'--folder',str(a.folder),'--child'],check=True)
