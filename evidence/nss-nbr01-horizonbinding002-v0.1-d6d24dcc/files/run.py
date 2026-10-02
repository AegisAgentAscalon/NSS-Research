from __future__ import annotations
import argparse
from pathlib import Path
from nbr01_horizon.util import configure

def main():
    p=argparse.ArgumentParser(description='Standalone synthetic NBR-01 follow-up; never deploys models.')
    p.add_argument('command', choices=['train','train-all','evaluate','verify','tests'])
    p.add_argument('--kind', choices=['soft_slots','hard_slots','gru_slots','tape_reader'])
    p.add_argument('--seed', type=int, default=141)
    p.add_argument('--curriculum', choices=['short','wide'], default='wide')
    p.add_argument('--steps',type=int,default=2400)
    p.add_argument('--output',type=Path, required=True)
    args=p.parse_args(); configure();root=Path(__file__).resolve().parent
    if args.command=='train':
        if args.kind is None: p.error('--kind required')
        from nbr01_horizon.train import train
        train(root,args.output,args.kind,args.seed,args.curriculum,args.steps)
    elif args.command=='train-all':
        from nbr01_horizon.train import train
        for seed in [301,302,303,304,305]:
            for curriculum in ['short','wide']:
                for kind in ['soft_slots','hard_slots','gru_slots','tape_reader']:
                    train(root,args.output,kind,seed,curriculum,args.steps)
    elif args.command=='evaluate':
        from nbr01_horizon.evaluate import evaluate_all
        evaluate_all(root,args.output)
    elif args.command=='verify':
        from nbr01_horizon.verify import verify
        verify(root,args.output)
    else:
        import unittest
        suite=unittest.defaultTestLoader.discover(str(root/'tests'))
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful(): raise SystemExit(1)
if __name__=='__main__': main()
