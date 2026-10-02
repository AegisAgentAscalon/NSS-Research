import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.train import train
p=argparse.ArgumentParser();p.add_argument('kind',choices=['split1','split4','coupled17']);p.add_argument('rep',type=int);p.add_argument('seed',type=int);p.add_argument('--out',type=Path,required=True);p.add_argument('--steps',type=int,default=1800);p.add_argument('--development',action='store_true')
a=p.parse_args();train(ROOT,a.out,a.kind,a.rep,a.seed,a.steps,a.development)
