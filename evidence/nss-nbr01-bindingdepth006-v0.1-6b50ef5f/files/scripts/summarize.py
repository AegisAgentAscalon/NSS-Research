from pathlib import Path
import json,statistics,collections
from nbr006 import common as c
ROOT=c.ROOT
all_files=sorted((ROOT/'results').glob('*.json'));docs=[json.loads(p.read_text()) for p in all_files];groups=collections.defaultdict(list)
for doc in docs:
 for row in doc['rows']:groups[(doc['kind'],row['case'],row['depth'])].append(row)
agg=[]
for (kind,case,depth),items in sorted(groups.items()):
 r={'kind':kind,'case':case,'depth':depth,'seeds':[x['seed'] for x in items]}
 for m in ['answer_accuracy','known_accuracy','unknown_accuracy','unsupported_room_rate','unresolved_rate']:
  vals=[x[m] for x in items if x[m] is not None]
  r[m]={'mean':statistics.mean(vals),'sample_sd':statistics.stdev(vals) if len(vals)>1 else None} if vals else None
 agg.append(r)
gates=[]
for d in docs:
 rows={(r['case'],r['depth']):r for r in d['rows']}
 competent=all(rows[(f'visible/h{h}/missing{u}',4)]['answer_accuracy']>=.95 for h in [1,2,4] for u in [0,1])
 transfer=all(rows[(f'visible/h8/missing{u}',8)]['answer_accuracy']>=.95 for u in [0,1])
 lifecycle=all(rows[(f'lifecycle/{name}',4)]['answer_accuracy']>=.95 for name in ['initial','correction','clear','rewrite','global_reset','new_scope_fresh_records'])
 gates.append({'kind':d['kind'],'seed':d['seed'],'visible_competence':competent,'h8_depth8_target':transfer,'lifecycle':lifecycle,'weights_unchanged':d['weights_unchanged']})
training=[json.loads(p.read_text()) for p in sorted((ROOT/'checkpoints').glob('*.json'))]
data_equivalence=[]
for seed in range(801,806):
 group=[d for d in training if d['seed']==seed and d['kind']!='binder']
 same=all(d['data_checks']==group[0]['data_checks'] for d in group)
 data_equivalence.append({'seed':seed,'readers':len(group),'sampled_batch_fingerprints_equal':same})
 assert same
result={'study':'NBR-01 BindingDepth006','status':'RUN; NBR-01 OPEN','main_fitted_checkpoints':len(training),'training_steps':sum(d['steps'] for d in training),'example_presentations':sum(d['steps']*d['batch'] for d in training),'training_loop_seconds_sum':sum(d['training_seconds'] for d in training),'evaluation_configurations':len(docs),'result_rows':sum(len(d['rows']) for d in docs),'scored_answers':sum(d['counts']['predictions'] for d in docs),'gates':gates,'aggregates':agg,'matched_reader_data_checks':data_equivalence,'parameter_counts':{d['kind']:d['parameters'] for d in training}}
c.dump(ROOT/'SUMMARY.json',result)
print({k:v for k,v in result.items() if k not in ['gates','aggregates','matched_reader_data_checks']})
for kind in sorted({g['kind'] for g in gates}):
 gg=[g for g in gates if g['kind']==kind]
 print(kind,{k:sum(g[k] for g in gg) for k in ['visible_competence','h8_depth8_target','lifecycle']})
