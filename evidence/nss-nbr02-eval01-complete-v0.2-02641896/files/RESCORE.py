"""Re-score archived review records from stored logits; no neural calls."""
from pathlib import Path
import argparse,subprocess,sys
r=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args()
if a.output.exists():raise SystemExit('Choose a new output directory; do not overwrite evidence.')
subprocess.run([sys.executable,str(r/'source/score.py'),'--root',str(r),'--raw',str(r/'raw/primary'),'--out',str(a.output)],check=True)
