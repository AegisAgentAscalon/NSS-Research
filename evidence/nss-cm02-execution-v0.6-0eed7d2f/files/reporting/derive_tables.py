"""Post-run descriptive aggregation only. Never changes frozen scoring or decisions."""
from pathlib import Path
import csv,json,statistics,collections
R=Path(__file__).resolve().parents[1]; S=R/'raw/main/capture_run/scores'; O=R/'results';O.mkdir(exist_ok=True)
def read(n):
 with (S/n).open(newline='') as f:return list(csv.DictReader(f))
def write(n,rows):
 if not rows:return
 with (O/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def nsum(rows,field):return sum(int(x[field]) for x in rows)
def summarize(rr,fields):
 groups=collections.defaultdict(list)
 for x in rr:groups[tuple(x[k] for k in fields)].append(x)
 result=[]
 for key,rows in sorted(groups.items()):
  d=dict(zip(fields,key)); d.update(n=len(rows),correct=nsum(rows,'correct'),accuracy=nsum(rows,'correct')/len(rows))
  for field in ['known','hidden_intent_wrong_binding','management_abstention','safe_but_lost_recall','correct_unknown']:
   if field in rows[0]:d[field]=nsum(rows,field)
  result.append(d)
 return result
D=read('DECISIONS.csv');X=read('EXACT_CONTROLS.csv');M=read('MEMORY_AND_READ_WORK.csv');E=read('EVENT_WORK.csv');C=read('COST_FAMILY_GRID.csv')
held=[x for x in D if x['split']=='heldout'];cx=[x for x in X if x['split']=='heldout'];cm=[x for x in M if x['split']=='heldout' and x['model_seed']=='1201']
write('HELDOUT_TEMPLATE.csv',summarize(held,['template','arm']))
write('EXACT_CONTROL_POOLED.csv',summarize(X,['split','control']))
write('HELDOUT_NOISE_POOLED.csv',summarize(held,['sigma','arm']))
write('HELDOUT_CHECKPOINTS.csv',summarize(held,['template','checkpoint','arm']))
write('HELDOUT_READER_SEEDS.csv',summarize(held,['model_seed','arm']))
write('HELDOUT_MANAGEMENT_ROUTES.csv',summarize(held,['route','reason','arm']))
pairs=[]
for family in sorted({x['family'] for x in C}):
 cc={x['arm']:x for x in C if x['family']==family};d=dict(family=family,split=cc['W']['split'])
 for field in list(cc['W'])[5:]:
  try:d[field+'_W_minus_I']=int(cc['W'][field])-int(cc['I'][field])
  except ValueError:pass
 pairs.append(d)
write('COST_PAIRED_DIFFERENCES.csv',pairs)
mem=[]
for arm in ['W','I','O']:
 r=[x for x in cm if x['arm']==arm]
 for field in ['whole_unique_python_graph_bytes','query_peak_transient_controller_graph_bytes','canonical_state_metadata_bytes','query_returned_bytes']:
  vals=[int(x[field]) for x in r if x.get(field)]
  if vals:mem.append(dict(arm=arm,metric=field,n=len(vals),min=min(vals),max=max(vals),mean=sum(vals)/len(vals),median=statistics.median(vals)))
write('HELDOUT_MEMORY_DESCRIPTIVE.csv',mem)
# Exact-control costs are non-neural; once per query, not once per model seed.
queries=[json.loads(x) for x in (R/'raw/main/capture_run/capture/queries.jsonl').read_text().splitlines()]
gold={x['query_id']:x for x in [json.loads(x) for x in (R/'raw/main/capture_run/input/protected_queries.jsonl').read_text().splitlines()]}
qr=[]
for q in queries:
 g=gold[q['query_id']]
 for control in ('X_W','X_I','X_S','X_latest'):
  work=q['exact_work'][control]
  qr.append(dict(query_id=q['query_id'],family=g['family'],split=g['split'],template=g['template'],checkpoint=g['checkpoint'],control=control,**work))
write('EXACT_CONTROL_WORK.csv',qr)
groups=collections.defaultdict(list)
for x in qr:groups[(x['split'],x['control'])].append(x)
ct=[]
for (split,arm),rows in sorted(groups.items()):
 d=dict(split=split,control=arm,query_occasions=len(rows))
 for f in rows[0]:
  if f not in ('query_id','family','split','template','checkpoint','control'):
   d[f]=max(x[f] for x in rows) if f=='peak_transient_unique_graph_bytes' else sum(x[f] for x in rows)
 ct.append(d)
write('EXACT_CONTROL_WORK_POOLED.csv',ct)
# Runtime medians/ranges include every observed timing; never a speedup pass.
t=[]
for run in ('capture_run','replay_run'):
 p=R/f'raw/main/{run}/capture/timing.jsonl'
 if p.exists():
  for l in p.read_text().splitlines():
   z=json.loads(l)
   for arm,ns in z['timing_ns'].items():t.append(dict(run=run,kind=z['kind'],arm=arm,nanoseconds=ns))
g=collections.defaultdict(list)
for x in t:g[(x['run'],x['kind'],x['arm'])].append(x['nanoseconds'])
write('TIMING_DESCRIPTIVE.csv',[dict(run=k[0],kind=k[1],arm=k[2],n=len(v),min_ns=min(v),median_ns=statistics.median(v),mean_ns=sum(v)/len(v),max_ns=max(v)) for k,v in sorted(g.items())])
summary={'descriptive_only':True,'heldout':summarize(held,['arm']),'heldout_exact':summarize(cx,['control']),
 'main_incorrect':sum(1-int(x['correct']) for x in D),'main_control_incorrect':sum(1-int(x['correct']) for x in X),
 'resident_memory_observation_count_per_arm':120,'extra_neural_calls':0,'derivation_inputs':'Frozen main score files + raw costs/timing, no decisions changed'}
(R/'results/DESCRIPTIVE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
