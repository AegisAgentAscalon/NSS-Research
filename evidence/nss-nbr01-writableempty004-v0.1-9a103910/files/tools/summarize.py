from pathlib import Path
import sys,json,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_empty.util import write_json
from nbr01_empty.models import MODES
results=[json.loads(p.read_text()) for p in sorted((ROOT/'evidence/results').glob('*.json'))]
if len(results)!=40:raise RuntimeError('Need all40 runs, not a selected subset')
rows=[row for run in results for row in run['rows']]
def stats(values):return {'mean':statistics.mean(values),'sample_std':statistics.stdev(values) if len(values)>1 else 0.,'values':values,'n':len(values)}
def select(**filters):return [r for r in rows if all(r.get(k)==v for k,v in filters.items())]
tables={}
for name,filters in {
 'nominal_empty_1024':dict(case='lifecycle',sigma=.15,phase='empty',round=1024),
 'nominal_final_1024':dict(case='lifecycle',sigma=.15,phase='rewritten',round=1024),
 'stress_empty_1024':dict(case='lifecycle',sigma=.3,phase='empty',round=1024),
 'stress_final_1024':dict(case='lifecycle',sigma=.3,phase='rewritten',round=1024),
 'extended_4096':dict(case='extended_empty',round=4096),
 'shock1_round4':dict(case='shock',sigma=1.,round=4),
 'shock05_round4':dict(case='shock',sigma=.5,round=4),
}.items():
 table={}
 for mode in MODES:
  x=select(mode=mode,**filters);assert len(x)==5,(name,mode,len(x))
  table[mode]={k:stats([r[k] for r in x]) for k in ['known_accuracy','unknown_accuracy','focus_accuracy','neighbors_accuracy','all_read_stream_success'] if k in x[0] and x[0][k] is not None}
 tables[name]=table
criteria={}
for mode in MODES:
 perseed=[]
 for seed in range(301,306):
  clean=select(mode=mode,seed=seed,case='lifecycle',sigma=0.)
  nominal_end=select(mode=mode,seed=seed,case='lifecycle',sigma=.15,round=1024)
  nominal_writes=[r for r in select(mode=mode,seed=seed,case='lifecycle',sigma=.15,round=0) if r['phase'] in ('first_write','correction','rewritten')]
  final=select(mode=mode,seed=seed,case='lifecycle',sigma=.15,phase='rewritten',round=1024)[0]
  ext=select(mode=mode,seed=seed,case='extended_empty',round=4096)[0]
  ew=select(mode=mode,seed=seed,case='extended_first_write')
  cleanpass=all(r[k]>=.95 for r in clean for k in ('known_accuracy','unknown_accuracy','focus_accuracy') if r[k] is not None)
  nominalpass=all(r[k]>=.95 for r in nominal_end for k in ('known_accuracy','unknown_accuracy')) and all(r['focus_accuracy']>=.95 for r in nominal_writes) and final['all_read_stream_success']>=.95
  extendedpass=ext['known_accuracy']>=.95 and ext['unknown_accuracy']>=.95 and all(r['focus_accuracy']>=.95 for r in ew)
  perseed.append(dict(seed=seed,clean_pass=cleanpass,nominal_joint_pass=nominalpass,extended_pass=extendedpass,
                       nominal_all_reads_success=final['all_read_stream_success']))
 criteria[mode]={'per_seed':perseed,**{k:sum(r[k] for r in perseed) for k in ('clean_pass','nominal_joint_pass','extended_pass')}}
atten={}
for mode in MODES:
 atten[mode]={old:{str(alpha):stats([r['focus_accuracy'] for r in select(mode=mode,case='attenuated_write',old_kind=old,alpha=alpha,round=16)]) for alpha in [.05,.1,.25,.5,.75,1.]} for old in ['empty','populated']}
local={mode:[dict(seed=r['seed'],empty=[x for x in r['stability'] if x['code']==8],known_max_rho=max(x['spectral_radius'] for x in r['stability'] if x['code']<8 and x['epsilon']==.001)) for r in results if r['mode']==mode] for mode in ('historical','replay','contract','local_empty')}
summary=dict(status='ALL_MAIN_RESULTS',runs=len(results),metric_rows=len(rows),saved_answer_evaluations=sum(r['answer_evaluations'] for r in results),
             evaluate_wall_seconds=sum(r['elapsed_seconds'] for r in results),tables=tables,criteria=criteria,attenuated=atten,local_stability=local)
write_json(ROOT/'SUMMARY.json',summary)
for name in ['nominal_empty_1024','nominal_final_1024','extended_4096','stress_final_1024','shock1_round4']:
 print('\n',name)
 for m,v in tables[name].items():print(m, {k:round(s['mean']*100,2) for k,s in v.items()})
print('\nCriteria', {m:(v['clean_pass'],v['nominal_joint_pass'],v['extended_pass']) for m,v in criteria.items()})
