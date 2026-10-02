from pathlib import Path
import argparse,sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from safetensors.torch import save_file,load_file
from nbr01_recovery.evaluate import load_candidates
from nbr01_recovery.state import Session
from nbr01_recovery.util import setup,write_json,digest_tensors
ROOT=Path(__file__).resolve().parents[1]

def tail(s):
    s.event(2,5,.8);s.maintain(7);s.event(0,6,.9);s.event(1,3,.49);s.maintain(3)

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['create','verify']);a=p.parse_args()
    setup();records=[]
    for seed in range(301,306):
        _,_,cs=load_candidates(ROOT,ROOT/'evidence/main',seed,seed+200)
        for mode,c in cs.items():
            if mode=='exact_archive':continue
            base=ROOT/'evidence/snapshots'/f'{mode}_rep{seed}'
            if a.action=='create':
                s=Session(c,'StateRecovery003-test','qualified-v1')
                s.event(0,2,.9);s.event(1,1,.8);s.maintain(4);s.event(2,7,.2);s.save(base/'cutoff')
                tail(s);save_file({f'lane{i}':x for i,x in enumerate(s.state)},str(base/'expected.safetensors'))
                write_json(base/'expected.json',dict(events=s.events,rounds=s.rounds,prediction=s.read().tolist(),
                    tensor_digest=digest_tensors({f'lane{i}':x for i,x in enumerate(s.state)})))
            else:
                r=Session(c,'StateRecovery003-test','qualified-v1');r.restore(base/'cutoff');tail(r)
                expected=json.loads((base/'expected.json').read_text())
                digest=digest_tensors({f'lane{i}':x for i,x in enumerate(r.state)})
                if digest!=expected['tensor_digest'] or r.read().tolist()!=expected['prediction'] or r.events!=expected['events'] or r.rounds!=expected['rounds']:
                    raise RuntimeError(f'Resume mismatch {seed} {mode}')
                before=digest;r.read();r.read()
                if digest_tensors({f'lane{i}':x for i,x in enumerate(r.state)})!=before:raise RuntimeError('Read mutated state')
                r.clear();r.maintain(16)
                if not torch.equal(r.read(),torch.full((1,4),8,dtype=torch.long)):raise RuntimeError('Reset failed')
                records.append(dict(rep_seed=seed,mode=mode,exact_continue=True,pure_read=True,clear=True))
    if a.action=='verify':
        out=dict(status='PASS',fresh_interpreter_consumer=True,configurations=len(records),results=records,
                 scope='Research state only; no external effects, Runtime connection or power-loss durability claim')
        write_json(ROOT/'evidence/LIFECYCLE_VERIFICATION.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
