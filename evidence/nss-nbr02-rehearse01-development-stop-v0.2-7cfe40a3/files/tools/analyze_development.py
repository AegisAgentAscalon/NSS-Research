"""Post-result descriptive analysis of exposed development only. No model operations."""
from pathlib import Path
import json,sys
import pandas as pd
root=Path(sys.argv[1]);out=root/'analysis';out.mkdir(exist_ok=True)
q=pd.read_csv(root/'raw/primary/final_audit/QUERY_ROWS.csv');d=q[(q.phase=='development')&q.arm.isin(['G','L'])].copy()
cal=json.loads((root/'raw/primary/A0_AND_GUARDS_LOCK.json').read_text())['calibration']
summary=d[(d.trial>=3)&d.kind.isin(['focal','old'])].groupby(['arm','branch','trial','stage','kind'],as_index=False).agg(correct=('correct','sum'),total=('correct','count'),mean_loss=('loss','mean'),mean_logit_margin=('logit_margin','mean'),mean_probability_margin=('probability_margin','mean'))
summary.to_csv(out/'DEVELOPMENT_SUMMARY.csv',index=False)
ix={(r.arm,int(r.fit),int(r.base),r.branch,int(r.trial),r.kind,int(r.cue),r.stage):r for r in d.itertuples()}
def get(a,fit,b,br,tr,k,c,st=None):
 if st is None:st='post_extra' if tr==3 and br in ('F','R') else 'post_real'
 return ix[a,fit,b,br,tr,k,c,st]
trans=[];ret=[];first=[];details=[]
for arm in ('G','L'):
 for base in range(4):
  for fit in range(4):
   f=base+8;r={'arm':arm,'base':base,'fit':fit}
   for br in ('B1','U','F','R'):
    z=get(arm,fit,base,br,3,'focal',f);r[br+'_correct']=int(z.correct);r[br+'_loss']=z.loss
   first.append(r)
   for br in ('F','R'):
    for c in [f,*range(8)]:
     kind='focal' if c==f else 'old';pre=get(arm,fit,base,br,3,kind,c,'pre_extra');post=get(arm,fit,base,br,3,kind,c)
     trans.append({'arm':arm,'base':base,'fit':fit,'branch':br,'cue':c,'kind':kind,'pre_correct':int(pre.correct),'post_correct':int(post.correct),'repaired':int(not pre.correct and post.correct),'broken':int(pre.correct and not post.correct),'loss_change':post.loss-pre.loss,'probability_margin_change':post.probability_margin-pre.probability_margin})
   for br in ('U','F','R'):
    for tr in (3,4,5,6):
     for c in range(8):
      r=get(arm,fit,base,br,tr,'old',c);b1=get(arm,fit,base,'B1',tr,'old',c);pre=get(arm,fit,base,'COMMON',2,'old',c)
      details.append({'arm':arm,'base':base,'fit':fit,'branch':br,'trial':tr,'cue':c,'correct':int(r.correct),'B1_correct':int(b1.correct),'pre_correct':int(pre.correct),'loss_delta':r.loss-b1.loss,'margin_decrease':b1.probability_margin-r.probability_margin,'actual_loss':r.loss})
D=pd.DataFrame(details)
for keys,g in D.groupby(['arm','branch','base','trial']):
 a,br,b,tr=keys;dl=float(g.loss_delta.mean());dm=float(g.margin_decrease.mean());t=cal[a]
 ret.append({'arm':a,'branch':br,'base':int(b),'trial':int(tr),'mean_loss_delta_vs_B1':dl,'mean_probability_margin_decrease_vs_B1':dm,'tau_loss':t['tau_loss'],'tau_margin':t['tau_margin'],'within_calibrated_envelope':dl<=t['tau_loss'] and dm<=t['tau_margin'],'interpretation':'descriptive development check; not held-out qualification'})
for name,rows in [('DEVELOPMENT_FIRST_CORRECTION',first),('DEVELOPMENT_REHEARSAL_TRANSITIONS',trans),('DEVELOPMENT_RETENTION_INDIVIDUAL',details),('DEVELOPMENT_CONFIDENCE_DIAGNOSTIC',ret)]:pd.DataFrame(rows).to_csv(out/(name+'.csv'),index=False)
batch=pd.read_csv(root/'raw/primary/final_audit/BATCH_UPDATES.csv');batch=batch[batch.phase=='development'];batch.groupby(['arm','branch']).agg(batches=('frame','count'),mean_raw_norm=('gradient_norm','mean'),min_raw_norm=('gradient_norm','min'),max_raw_norm=('gradient_norm','max'),mean_step_norm=('actual_step_norm','mean'),mean_cancellation_ratio=('cancellation_ratio','mean')).to_csv(out/'DEVELOPMENT_BATCH_MAGNITUDES.csv')
neg=q[q.correct==0];neg.to_csv(out/'ALL_PHASE_NEGATIVES.csv',index=False)
result={'status':'DEVELOPMENT_ONLY_NOT_QUALIFICATION','query_rows':len(q),'negative_rows':len(neg),'phase_rows':q.groupby('phase').size().to_dict(),'phase_negatives':neg.groupby('phase').size().to_dict(),'first_correct':pd.DataFrame(first).groupby('arm')[[b+'_correct' for b in ('B1','U','F','R')]].sum().to_dict('index'),'old_tail_correct':D.groupby(['arm','branch']).correct.agg(['sum','count']).reset_index().to_dict('records'),'confidence_exceeding_cells':pd.DataFrame(ret).assign(fail=lambda x:~x.within_calibrated_envelope).groupby(['arm','branch']).fail.sum().reset_index().to_dict('records'),'rehearsal_old_repairs_breaks':pd.DataFrame(trans).query('kind=="old"').groupby(['arm','branch'])[['repaired','broken']].sum().reset_index().to_dict('records')}
(out/'SUMMARY.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
