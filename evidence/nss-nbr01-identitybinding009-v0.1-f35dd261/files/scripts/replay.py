from pathlib import Path
import sys,argparse,subprocess,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import ROOT,dump,utc,np
from result_io import materialize
p=argparse.ArgumentParser();p.add_argument('--pair',type=int,default=1);p.add_argument('--out',type=Path,required=True);p.add_argument('--stages',default='A,B,CUE');a=p.parse_args()
if sys.platform=='win32':raise SystemExit('The full evaluator currently imports Unix resource telemetry. Windows replay is not supported by this release; checks/rescore were not tested on Windows.')
if a.out.resolve().is_relative_to(ROOT):raise SystemExit('Replay output must be outside the immutable release folder')
subprocess.run([sys.executable,str(ROOT/'scripts/run_main.py'),'--pair',str(a.pair),'--out',str(a.out),'--stages',a.stages],check=True)
count=0
for tag in a.stages.split(','):
 ref=ROOT/'evidence/results'/f'{tag}_pair{a.pair}.npz'
 with materialize(ref) as f,np.load(f,allow_pickle=False) as x,np.load(a.out/ref.name,allow_pickle=False) as y:
  assert x.files==y.files
  for k in x.files:
   if not np.array_equal(x[k],y[k]):raise AssertionError(tag+' '+k)
   count+=1
dump(a.out/'REPLAY_VERIFIED.json',{'status':'PASS','pair':a.pair,'stages':a.stages,'arrays':count,'utc':utc()});print('Replay PASS',count)
