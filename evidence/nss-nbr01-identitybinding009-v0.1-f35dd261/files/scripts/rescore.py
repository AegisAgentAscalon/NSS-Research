from pathlib import Path
import sys,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import ROOT,dump,utc
from nbr009.score import score_a,score_b,score_cue
from result_io import materialize
p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path);a=p.parse_args();count=0
for pair in range(1,6):
 for tag,fn in [('A',score_a),('B',score_b),('CUE',score_cue)]:
  src=ROOT/'evidence/results'/f'{tag}_pair{pair}.npz'
  with materialize(src) as f:actual=fn(f)
  expected=json.loads(src.with_name(src.stem+'_scores.json').read_text())
  if actual!=expected:raise AssertionError(str(src)+' score mismatch')
  count+=len(actual);print('RESCORED',tag,pair,len(actual),flush=True)
rec={'status':'PASS','files':15,'metric_rows':count,'independent_numpy_scorer':True,'utc':utc()}
if a.receipt:dump(a.receipt,rec)
print(rec)
