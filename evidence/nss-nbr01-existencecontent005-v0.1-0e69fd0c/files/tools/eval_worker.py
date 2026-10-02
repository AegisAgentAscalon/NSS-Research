import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.evaluate import evaluate_one
p=argparse.ArgumentParser();p.add_argument('mode');p.add_argument('rep',type=int);p.add_argument('--out',type=Path,required=True);p.add_argument('--checkpoint-dir',type=Path);p.add_argument('--learn-seed',type=int);p.add_argument('--development',action='store_true')
a=p.parse_args();evaluate_one(ROOT,a.out,a.rep,a.mode,a.learn_seed,a.checkpoint_dir,a.development)
