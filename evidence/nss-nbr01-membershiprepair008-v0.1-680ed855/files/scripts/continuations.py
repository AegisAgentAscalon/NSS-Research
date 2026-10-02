"""Fresh-process state/RNG and mid-query replay after mutable reference events."""
from pathlib import Path
import sys,argparse,json
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import *
from nbr008.config import *
from nbr008.pipeline import *
from nbr008.state import State

@torch.no_grad()
def save(out):
    setup();out=Path(out);out.mkdir(parents=True,exist_ok=True);items=[]
    for pair in range(1,6):
        models=parents(pair);h,cfg=load_gate(1000+pair)
        for method in ('nearest','A_nearest','B_nearest','B_learned'):
            r=resolver(method,models,h,cfg);con=contract(r,models)
            for phase in ('registered','corrected','unreadable','midquery'):
                p=make_problem(700000000+pair,4,8,n=12);s=install(p,models['binder'],r,True);rng=np.random.default_rng(700100000+pair)
                new=torch.zeros(8,17);new[:,:16]=torch.from_numpy(data.normalize(rng.normal(size=(8,16))).astype(np.float32));s.register(new)
                dest=torch.from_numpy(p['codes'][np.arange(8),p['rooms'][:,0]]);s.event(new,dest,1,r)
                if phase=='corrected':s.event(new,torch.from_numpy(p['codes'][np.arange(8),p['rooms'][:,1]]),1,r)
                elif phase=='unreadable':s.store.vals[s.present]=0;s.maintain(r)
                q=init_query(new)
                if phase=='midquery':q,_=step_query(s,models['record_hop'],r,q)
                key=f'{pair}_{method}_{phase}';path=out/(key+'.npz');s.save(path,rng,con,q)
                for _ in range(16):s.add_noise(rng,.02);s.maintain(r)
                ans=read(s,models['record_hop'],r,q['h'],4,qs=q)
                np.savez_compressed(out/(key+'_expected.npz'),signature=np.array(s.signature()),rng=np.array(json.dumps(rng.bit_generator.state,sort_keys=True)),pred=ans['pred'].numpy(),h=ans['qs']['h'].numpy(),alive=ans['qs']['alive'].numpy())
                items.append({'pair':pair,'method':method,'phase':phase,'file':path.name})
    dump(out/'INDEX.json',{'cases':items});print('SAVED',len(items))

@torch.no_grad()
def verify(out):
    setup();out=Path(out);items=json.loads((out/'INDEX.json').read_text())['cases'];done=[]
    for item in items:
        models=parents(item['pair']);h,cfg=load_gate(1000+item['pair']);r=resolver(item['method'],models,h,cfg)
        s,rng,q=State.load(out/item['file'],models['binder'],contract(r,models))
        for _ in range(16):s.add_noise(rng,.02);s.maintain(r)
        ans=read(s,models['record_hop'],r,q['h'],4,qs=q)
        with np.load(out/(Path(item['file']).stem+'_expected.npz'),allow_pickle=False) as a:
            assert str(a['signature'])==s.signature();assert str(a['rng'])==json.dumps(rng.bit_generator.state,sort_keys=True)
            for n in ('h','alive'):assert np.array_equal(a[n],ans['qs'][n].numpy())
            assert np.array_equal(a['pred'],ans['pred'].numpy())
        done.append(item)
    dump(out/'VERIFIED.json',{'status':'PASS','cases':len(done),'records':done,'fresh_process':True});print('VERIFIED',len(done))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['save','verify']);p.add_argument('--out',required=True);a=p.parse_args();globals()[a.mode](a.out)
