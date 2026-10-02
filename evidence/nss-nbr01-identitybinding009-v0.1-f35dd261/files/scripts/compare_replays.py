from pathlib import Path
import sys,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import *
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();rows=[];array_count=0;prediction_entries=0
for pair in range(1,6):
 for tag in ('A','B','CUE'):
  name=f'{tag}_pair{pair}';orig=ROOT/'evidence/results'/f'{name}.npz';rep=a.work/f'replay_pair{pair}'/f'{name}.npz'
  with np.load(orig,allow_pickle=False) as x,np.load(rep,allow_pickle=False) as y:
   if x.files!=y.files:raise AssertionError(name+' keys')
   for k in x.files:
    if not np.array_equal(x[k],y[k]):raise AssertionError(name+' '+k)
    array_count+=1
    if '__pred_' in k:prediction_entries+=x[k].size
   rows.append({'file':name,'arrays':len(x.files),'array_digest':array_digest({k:x[k] for k in x.files}),'original_sha':sha(orig),'replay_sha':sha(rep),'equal_array_values':True})
  s1=json.loads((orig.with_name(name+'_scores.json')).read_text());s2=json.loads((rep.with_name(name+'_scores.json')).read_text())
  if s1!=s2:raise AssertionError(name+' independent score mismatch')
dump(ROOT/'evidence/verification/FULL_REPLAY.json',{'status':'PASS','fresh_interpreters':True,'files':rows,'total_arrays':array_count,'saved_prediction_elements':prediction_entries,'metric_rows':sum(len(json.loads(p.read_text())) for p in (ROOT/'evidence/results').glob('*_scores.json')),'utc':utc()});print('All replay PASS',array_count,prediction_entries)
