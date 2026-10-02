from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description='NSS bounded state-maintenance research; no deployment/network actions')
    s=p.add_subparsers(dest='command',required=True)
    t=s.add_parser('train');t.add_argument('--kind',choices=['readout_repair','recurrent','fast_slow'],required=True)
    t.add_argument('--rep-seed',type=int,required=True);t.add_argument('--seed',type=int,required=True)
    t.add_argument('--steps',type=int,default=1800);t.add_argument('--output',type=Path,required=True)
    e=s.add_parser('evaluate');e.add_argument('--rep-seed',type=int,required=True);e.add_argument('--seed',type=int,required=True)
    e.add_argument('--models',type=Path,required=True);e.add_argument('--output',type=Path,required=True)
    e.add_argument('--development',action='store_true')
    a=p.parse_args();root=Path(__file__).resolve().parent
    if a.command=='train':
        from nbr01_recovery.train import train
        print(json.dumps(train(root,a.output,a.kind,a.rep_seed,a.seed,a.steps),indent=2))
    else:
        from nbr01_recovery.evaluate import evaluate
        print(json.dumps(evaluate(root,a.models,a.output,a.rep_seed,a.seed,a.development),indent=2))

if __name__=='__main__':main()
