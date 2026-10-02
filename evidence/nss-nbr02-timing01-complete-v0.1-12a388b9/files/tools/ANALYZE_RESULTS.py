"""Post-execution descriptive timing tables from saved scores only; no model imports."""
from pathlib import Path
import argparse,csv,json
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path);a=p.parse_args()
R=a.root;out=a.output or R/'analysis';out.mkdir(parents=True,exist_ok=True);d=R/'raw/primary/final_audit'
def read(n):
 with open(d/n,newline='') as f:return list(csv.DictReader(f))
def write(n,rows):
 with open(out/n,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['empty']);w.writeheader();w.writerows(rows)
def mean(v):return float(np.mean(v))
q=read('QUERY_ROWS.csv');dec=json.loads((d/'DECISIONS.json').read_text());ret=read('RETENTION_INDIVIDUAL.csv');batch=read('BATCH_UPDATES.csv');trans=read('RECOVERY_TRANSITIONS.csv')
phases=sorted({r['phase'] for r in q});neg=[]
for phase in phases:
 for method in sorted({r['arm'] for r in q if r['phase']==phase}):
  z=[r for r in q if r['phase']==phase and r['arm']==method];neg.append({'phase':phase,'method':method,'query_rows':len(z),'incorrect':sum(int(r['correct'])==0 for r in z)})
write('NEGATIVE_COUNTS.csv',neg)
trajectory=[];contrast=[];context=[];batches=[];change_summary=[];summary={'interpretation':'Post-execution descriptive tables; no new model/gradient calls. Full-trajectory screens were frozen before data. Timing comparisons are exploratory.'}
for arm in ('G','L'):
 D=dec[arm];summ={'first_correction':{},'retention':{},'late_final':{},'batches':{}}
 for br in ('B1','U','E','LATE'):
  z=D['branches'][br];summ['first_correction'][br]={'correct':z['first_correct'],'total':32,'loss':z['first_loss']}
  summ['retention'][br]={k:z[k] for k in ('all_boundary_old_labels_pass','all_boundary_old_confidence_pass','full_trajectory_screen_pass','confidence_failing_base_boundaries')}
  for stage in z['pooled']:
   trajectory.append({'method':arm,'branch':br,**stage})
  rr=[r for r in ret if r['arm']==arm and r['branch']==br]
  summ['retention'][br]['worst_observed_old_probability']=min((float(r['probability_margin'])+1)/2 for r in rr)
  summ['retention'][br]['old_observations']=len(rr);summ['retention'][br]['old_correct']=sum(int(r['candidate_correct']) for r in rr)
 for c in D['timing_contrasts']:contrast.append({'method':arm,**c})
 for base in range(4,12):
  for fit in range(4):
   pair={'method':arm,'base':base,'fit':fit}
   for br in ('E','LATE'):
    rr=[r for r in ret if r['arm']==arm and r['branch']==br and int(r['base'])==base and int(r['fit'])==fit and int(r['trial'])==6]
    assert len(rr)==8
    pair[br+'_final_old_mean_loss']=mean([float(r['loss']) for r in rr]);pair[br+'_final_focal_loss']=float(rr[0]['focal_loss'])
   pair['late_minus_early_final_old_loss']=pair['LATE_final_old_mean_loss']-pair['E_final_old_mean_loss'];context.append(pair)
 cx=[r for r in context if r['method']==arm]
 summ['late_final']={'better_old_loss_contexts':sum(r['late_minus_early_final_old_loss']<0 for r in cx),'total_contexts':32,'better_bases':D['late_final_loss_lower_bases'],'total_bases':8,'pooled_old_loss_difference':D['late_minus_early_final_mean_loss']}
 for br in ('E','LATE'):
  bb=[r for r in batch if r['phase']=='heldout' and r['arm']==arm and r['branch']==br]
  assert len(bb)==32
  b={'method':arm,'branch':br,'batch_updates':len(bb),'example_gradients':8*len(bb),'mean_raw_norm':mean([float(r['gradient_norm']) for r in bb]),'max_raw_norm':max(float(r['gradient_norm']) for r in bb),'mean_actual_norm':mean([float(r['actual_step_norm']) for r in bb]),'clipped':sum(float(r['clip_factor'])<1 for r in bb),'mean_cancellation_ratio':mean([float(r['cancellation_ratio']) for r in bb])}
  batches.append(b);summ['batches'][br]=b
  meanold=[];focal=[];oldflips=oldfix=0
  for base in range(4,12):
   for fit in range(4):
    zz=[r for r in trans if r['arm']==arm and r['branch']==br and int(r['base'])==base and int(r['fit'])==fit]
    old=[r for r in zz if r['kind']=='old'];ff=[r for r in zz if r['kind']=='focal'];assert len(old)==8 and len(ff)==1
    meanold.append(mean([float(r['loss_change']) for r in old]));focal.append(float(ff[0]['loss_change']));oldflips+=sum(int(r['correct_to_broken']) for r in old);oldfix+=sum(int(r['broken_to_repaired']) for r in old)
  change_summary.append({'method':arm,'branch':br,'mean_old_loss_change':mean(meanold),'contexts_old_loss_decreases':sum(x<0 for x in meanold),'contexts':len(meanold),'mean_focal_loss_change':mean(focal),'old_classes_repaired':oldfix,'old_classes_broken':oldflips})
 summary[arm]=summ
write('TRAJECTORY_MEANS.csv',trajectory);write('TIMING_CONTRAST_BY_BASE.csv',contrast);write('FINAL_CONTEXT_COMPARISON.csv',context);write('BATCH_MAGNITUDES.csv',batches);write('BEFORE_AFTER_REHEARSAL.csv',change_summary)
summary['query_rows']=len(q);summary['negative_query_rows']=sum(int(r['correct'])==0 for r in q);summary['negative_by_phase']={phase:sum(r['incorrect'] for r in neg if r['phase']==phase) for phase in phases}
summary['new_model_calls']=0;summary['new_optimizer_updates']=0
(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2,allow_nan=False));print(json.dumps(summary,indent=2))
