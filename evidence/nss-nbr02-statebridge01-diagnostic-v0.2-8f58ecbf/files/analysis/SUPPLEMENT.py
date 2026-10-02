"""Retained-evidence score breakdowns; no new model or gradient calls."""
from pathlib import Path
import csv,json,hashlib,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from reference import oracle
root=Path(__file__).resolve().parents[1];out=root/'analysis/tables';out.mkdir(parents=True,exist_ok=True)
def rows(p):return list(csv.DictReader(open(p)))
def read(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
def write(name,rs):
 with open(out/name,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
a=rows(root/'scores_diagnostic/A_QUERIES.csv');p=rows(root/'scores_diagnostic/PAIRED_CONTEXTS.csv');b=rows(root/'scores_diagnostic/B_QUERIES.csv')
points=[]
for stage in range(3):
 for mode in ['CARRY','REBUILD','RESET','PINNED']:
  for at in [0,1,2,4,8]:
   r=[x for x in a if x['split']=='test' and int(x['stage'])==stage and x['mode']==mode and int(x['suffix_position'])==at]
   points.append({'stage':stage,'mode':mode,'suffix_position':at,'correct':sum(int(x['joint_correct']) for x in r),'n':len(r),'mean_loss':float(np.mean([float(x['loss']) for x in r]))})
write('CONTINUATION_BY_POSITION.csv',points)
pa=[]
for stage in [1,2]:
 r=[x for x in p if x['split']=='test' and int(x['stage'])==stage]
 pa.append({'stage':stage,'contexts':len(r),'carry_better_contexts':sum(int(x['carry_correct'])>int(x['rebuild_correct']) for x in r),
 'rebuild_better_contexts':sum(int(x['carry_correct'])<int(x['rebuild_correct']) for x in r),'rebuild_rescue_readouts':sum(int(x['rebuild_rescues']) for x in r),
 'carry_rescue_readouts':sum(int(x['carry_rescues']) for x in r)})
write('PAIRED_DIRECTION.csv',pa)
update_rows=[]
for ctx in sorted((root/'primary/contexts').iterdir()):
 meta=json.loads((ctx/'CONTEXT.json').read_text());labels=np.array(meta['old_B_labels']);labels[meta['focal_cue']]=1-labels[meta['focal_cue']]
 for k in range(12):
  u=read(ctx/f'update_{k:02d}.npz')
  if k<8:
   z=float(u['B_logits'][0,-1,0]);target=int(u['B_labels'][0]);c=int(u['B_events'][0,-1])-12
   update_rows.append({'split':meta['split'],'fit':meta['fit'],'case':meta['case'],'update':k,'surface':'PRE_REAL_RECEIPT','cue':c,'target':target,'correct':int((z>0)==bool(target)),'loss':float(np.logaddexp(0,z)-target*z)})
  bp=read(ctx/f'B_post_update_{k:02d}.npz')
  for c in range(4):
   z=float(bp['logits'][c,0]);target=int(labels[c])
   update_rows.append({'split':meta['split'],'fit':meta['fit'],'case':meta['case'],'update':k,'surface':'POST_UPDATE_B_INVENTORY','cue':c,'target':target,'correct':int((z>0)==bool(target)),'loss':float(np.logaddexp(0,z)-target*z)})
write('ALL_B_UPDATE_OBSERVATIONS.csv',update_rows);write('B_UPDATE_NEGATIVES.csv',[r for r in update_rows if not r['correct']])
# Normatively fixed A data support checks, using only captured inputs.
nov=[]
for fit in range(4):
 t=read(root/f'primary/train/fit{fit}/INPUTS.npz');seen=set();duplicates=0
 for u,n in enumerate(t['lengths']):
  for seq in t['events'][u,:,:int(n)]:
   key=bytes(seq)
   duplicates+=key in seen;seen.add(key)
 for split,fn in [('dev','DEV_INPUTS.npz'),('test','TEST_INPUTS.npz')]:
  e=read(root/'primary'/fn);overlap=sum(bytes(x[:int(n)]) in seen for x,n in zip(e['events'],e['lengths']))
  nov.append({'fit':fit,'split':split,'full_prefix_train_matches':int(overlap),'prefixes':len(e['lengths']),'training_semantic_duplicate_excess':int(duplicates),
   'scope':'Whole-stream novelty only; final four SET/CLEAR commands and task grammar are deliberately familiar.'})
write('INPUT_SUPPORT.csv',nov)
summary={'main_queries':5120,'rebuild_extra_transitions_per32_histories':int(read(root/'primary/TEST_INPUTS.npz')['lengths'].sum()),
 'ordinary_continuation_transitions_per32_histories':256,'pinned_parameter_tensor_bytes':65316,'per_task_state_bytes':256,'32_task_state_bytes':8192,
 'parameter_sets_pinned_plus_candidate':2,'parameter_tensor_total':130632,
 'B_update_observations':len(update_rows),'B_update_negatives':sum(not x['correct'] for x in update_rows),
 'stored_B_post_update_inventory_target_note':'Research scorer uses current scenario target even before the first changed-label receipt; pre-evidence surprises are not learning failures.',
 'controls':'Pinned weights do not learn reversed B. Many A states share one immutable weight object; simultaneous live execution not tested.'}
(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
