from pathlib import Path
import sys,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_empty.train import train
from nbr01_empty.evaluate import evaluate_one
from nbr01_empty.models import MODES
p=argparse.ArgumentParser();p.add_argument('action',choices=('train','evaluate'));p.add_argument('--output',type=Path);a=p.parse_args()
if a.action=='train':
 for seed in range(301,306):
  for kind in ('replay','contract','local_empty'):train(ROOT,a.output or ROOT/'evidence/main',kind,seed,seed+300)
else:
 for seed in range(301,306):
  for mode in MODES:evaluate_one(ROOT,a.output or ROOT/'evidence/results',seed,mode)
