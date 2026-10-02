from __future__ import annotations
from pathlib import Path
import json,statistics,collections,sys
r=Path(sys.argv[1]);results=r/'evidence/results'
rows=[]
for p in sorted(results.glob('*.eval.json')):
 a=json.loads(p.read_text());rows.extend(a['rows'])

def ratio(a,num,den):return a[num]/a[den] if a[den] else None
aggregates=[]
groups=collections.defaultdict(list)
for a in rows:groups[(a['kind'],a['curriculum'],a['variant'],a['condition'],a['horizon'])].append(a)
for key,aa in sorted(groups.items()):
 o=dict(zip(['kind','curriculum','variant','condition','horizon'],key));o['seeds']=[a['seed'] for a in aa]
 for label,num,den in [('accuracy','correct','n_answers'),('known_accuracy','known_correct','known'),('unknown_accuracy','unknown_correct','unknown'),('all_four_accuracy','all_four_correct','n_streams'),('protected_accuracy','protected_correct','n_streams')]:
  vv=[ratio(a,num,den) for a in aa if a[den]]
  o[label]=dict(mean=statistics.mean(vv),sd=statistics.stdev(vv) if len(vv)>1 else 0.,min=min(vv),max=max(vv),per_seed=vv) if vv else None
 aggregates.append(o)
byarm=collections.defaultdict(list)
for a in rows:byarm[(a['kind'],a['curriculum'],a['variant'],a['seed'])].append(a)
screens=[]
for key,aa in sorted(byarm.items()):
 d={(a['condition'],a['horizon']):a for a in aa}
 baseline=all(ratio(d[(c,h)],n,den)>=.95 for h in [0,16] for c,n,den in [('retain','known_correct','known'),('overwrite','known_correct','known'),('mixed_unknown','unknown_correct','unknown'),('reset','unknown_correct','unknown')])
 longpass=all(ratio(d[(c,4096)],n,den)>=.95 for c,n,den in [('retain','known_correct','known'),('overwrite','known_correct','known'),('mixed_unknown','unknown_correct','unknown'),('reset','unknown_correct','unknown')])
 drop=ratio(d[('retain',16)],'known_correct','known')-ratio(d[('retain',4096)],'known_correct','known')
 margin=all(ratio(d[(c,4096)],'known_correct','known')>=.95 for c in ['near_reject','near_write'])
 screens.append(dict(zip(['kind','curriculum','variant','seed'],key),baseline_pass=baseline,clean_long_pass=baseline and longpass and drop<=.01,retention_drop=drop,low_margin_pass=margin))
training=[json.loads(p.read_text()) for p in sorted((r/'evidence/main').glob('*.json')) if '.prerun' not in p.name]
exact=json.loads((results/'EXACT_CONTROL.json').read_text())['rows']
summary=dict(study='NBR-01/HorizonBinding002',main_checkpoints=len(training),model_cells=len(rows),exact_cells=len(exact),
 unique_eval_streams=sum(a['n_streams'] for a in exact),main_model_answer_evaluations=sum(a['n_answers'] for a in rows),
 main_steps=sum(a['steps'] for a in training),main_example_presentations=sum(a['examples'] for a in training),main_supervised_key_answers=sum(a['supervised_key_answers'] for a in training),
 main_observed_event_presentations=sum(a['observed_events'] for a in training),main_train_seconds=sum(a['train_wall_seconds'] for a in training),
 extra_gate_calibration_label_presentations=2048*len([a for a in training if a['kind']=='soft_slots']),
 unique_extra_gate_calibration_labels=10240,aggregates=aggregates,screens=screens)
(results/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print({k:v for k,v in summary.items() if k not in ('aggregates','screens')})
for curriculum in ['short','wide']:
 print('\n',curriculum)
 for a in aggregates:
  if a['curriculum']==curriculum and a['horizon']==4096 and a['condition'] in ['retain','mixed_unknown','near_reject','near_write','noisy_observation']:
   print(a['kind'],a['variant'],a['condition'], 'overall',round(a['accuracy']['mean']*100,3), 'sd',round(a['accuracy']['sd']*100,3), 'all4',round(a['all_four_accuracy']['mean']*100,3))
print('\nSCREENS')
ss=collections.defaultdict(list)
for a in screens:ss[(a['kind'],a['curriculum'],a['variant'])].append(a)
for k,aa in sorted(ss.items()):print(k,*[(v,sum(x[v] for x in aa)) for v in ['baseline_pass','clean_long_pass','low_margin_pass']])
