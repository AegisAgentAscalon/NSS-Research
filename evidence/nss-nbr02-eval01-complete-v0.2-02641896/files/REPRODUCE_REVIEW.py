"""Explicit new policy replay only, not adaptive replay of the historical learners."""
from pathlib import Path
import argparse,subprocess,sys
r=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=False)
subprocess.run([sys.executable,str(r/'source/run_review.py'),'--root',str(r),'--out',str(a.output/'raw')],check=True)
subprocess.run([sys.executable,str(r/'source/score.py'),'--root',str(r),'--raw',str(a.output/'raw'),'--out',str(a.output/'results')],check=True)
