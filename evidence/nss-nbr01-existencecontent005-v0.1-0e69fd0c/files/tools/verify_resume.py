import sys,json,argparse
from pathlib import Path
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.models import *
from nbr01_exist.evaluate import initialize,generators,noisy_step
from nbr01_exist.snapshot import save,restore
from nbr01_exist.util import setup,write_json,digest_tensors,array_digest

def state_digest(m,gc,gp):
    a={'z':m.z,'gc':gc.get_state(),'gp':gp.get_state()}
    if m.p is not None:a['p']=m.p
    if m.flag is not None:a['flag']=m.flag
    return digest_tensors(a)
@torch.no_grad()
def continuation(m,gc,gp):
    base=torch.arange(len(m.z))%8;pred=[]
    for t in range(64):
        if t==16:m.event('write',0,(base+2)%8)
        if t==32:m.event('clear',1)
        if t==48:m.event('write',1,(base+5)%8)
        noisy_step(m,gc,gp,.15);pred.append(torch.stack((m.read(),m.existence().long()),-1).numpy())
    return dict(final_state_digest=state_digest(m,gc,gp),prediction_digest=array_digest(np.stack(pred)),events=m.events,rounds=m.rounds)

def main():
    setup();p=argparse.ArgumentParser();p.add_argument('action',choices=['create','verify']);p.add_argument('--out',type=Path,required=True);a=p.parse_args();records=[]
    if a.action=='create':
        for seed in range(301,306):
            for mode in MODES:
                rep,old,new=load_components(ROOT,seed,mode)
                for cut in ['empty','written']:
                    m=Memory(rep,mode,old,new,32);initialize(m);gc,gp=generators(seed,7000)
                    for _ in range(128):noisy_step(m,gc,gp,.15)
                    if cut=='written':m.event('write',0,4)
                    path=ROOT/'evidence/snapshots'/f'{mode}_{seed}_{cut}';save(m,gc,gp,path)
                    records.append(dict(mode=mode,seed=seed,cut=cut,path=str(path.relative_to(ROOT)),expected=continuation(m,gc,gp)))
        write_json(a.out,dict(status='CREATED',cases=records))
    else:
        exp=json.loads((ROOT/'evidence/RESUME_EXPECTATIONS.json').read_text())
        for row in exp['cases']:
            rep,old,new=load_components(ROOT,row['seed'],row['mode']);m=Memory(rep,row['mode'],old,new,32);gc,gp=generators(0,0)
            restore(m,gc,gp,ROOT/row['path']);got=continuation(m,gc,gp)
            assert got==row['expected'],row
            records.append(dict(mode=row['mode'],seed=row['seed'],cut=row['cut'],status='PASS'))
        write_json(a.out,dict(status='PASS',cases=records,count=len(records)))
    print(a.action,len(records),'cases')
if __name__=='__main__':main()
