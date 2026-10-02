"""Post-result descriptive development analysis only. No parameter updates.
These tables cannot qualify a held-out screen or change its admission rule.
"""
from pathlib import Path
import json,csv,sys,collections,math
import numpy as np
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R/'source'))
from reference_numeric import records,write_csv
from independent_projection import margin_reference
r=R/'raw/primary';out=R/'analysis';out.mkdir(exist_ok=True)
plan=json.loads((r/'private/PLAN.json').read_text());qq=list(csv.DictReader(open(r/'final_audit/QUERY_ROWS.csv')))
for x in qq:
 for k in ('fit','base','trial','cue','target','correct','predicted','frame','delay'):x[k]=int(x[k])
 for k in ('loss','probability_margin','logit_margin'):x[k]=float(x[k])
dev=[q for q in qq if q['phase']=='development'];idx={(x['arm'],x['fit'],x['base'],x['branch'],x['trial'],x['kind'],x['cue']):x for x in dev}
summary=[];old=[];pairs=[];resid=[];norms=[];predonly=[]
for arm in ('G','L'):
 for br in ('B1','B2','P','S'):
  for tr in (3,4,5,6):
   f=[x for x in dev if x['arm']==arm and x['branch']==br and x['trial']==tr and x['kind']=='focal']
   oo=[x for x in dev if x['arm']==arm and x['branch']==br and x['trial']==tr and x['kind']=='old']
   summary.append({'arm':arm,'branch':br,'trial':tr,'focal_correct':sum(x['correct'] for x in f),'focal_n':len(f),'focal_loss':float(np.mean([x['loss'] for x in f])),'old_correct':sum(x['correct'] for x in oo),'old_n':len(oo),'old_loss':float(np.mean([x['loss'] for x in oo])),'old_probability_margin':float(np.mean([x['probability_margin'] for x in oo]))})
  for x in [v for v in dev if v['arm']==arm and v['branch']==br and v['kind']=='old']:
   pre=idx[(arm,x['fit'],x['base'],'COMMON',2,'old',x['cue'])];b1=idx[(arm,x['fit'],x['base'],'B1',x['trial'],'old',x['cue'])]
   old.append({'arm':arm,'branch':br,'fit':x['fit'],'base':x['base'],'trial':x['trial'],'cue':x['cue'],'pre_correct':pre['correct'],'post_correct':x['correct'],'lost_prefork':int(pre['correct'] and not x['correct']),'extra_vs_B1':int(b1['correct'] and not x['correct']),'loss_delta_B1':x['loss']-b1['loss'],'probability_margin_decrease_B1':b1['probability_margin']-x['probability_margin']})
 for fit in range(4):
  for base in range(4):
   v={b:idx[(arm,fit,base,b,3,'focal',base+8)] for b in ('B1','B2','P','S')};row={'arm':arm,'fit':fit,'base':base}
   for b,x in v.items():row[b+'_correct']=x['correct'];row[b+'_loss']=x['loss']
   row['P_lost_B1']=int(v['B1']['correct'] and not v['P']['correct']);row['P_lost_B2']=int(v['B2']['correct'] and not v['P']['correct']);row['P_minus_S']=v['P']['correct']-v['S']['correct'];pairs.append(row)
for k,m,a in records(r/'worker/records.bin'):
 if m['kind']!='protection':continue
 sm=plan['sessions'][m['context']['session']]
 if sm['phase']!='development':continue
 arm=m['arm'];br=m['context']['branch'];fit=sm['fit'];base=sm['base'];delta=a['deltaP' if br=='P' else 'deltaS']
 norms.append({'arm':arm,'branch':br,'fit':fit,'base':base,'norm_P':float(a['norm_metrics'][0]),'norm_B2':float(a['norm_metrics'][1]),'norm_S':float(a['norm_metrics'][2]),'relative_norm_mismatch':float(a['norm_metrics'][4]),'P_S_cosine':float(np.dot(a['deltaP'],a['deltaS'])/(np.linalg.norm(a['deltaP'])*np.linalg.norm(a['deltaS']))),'support_mask':int(a['selected'][0]),'minimum_actual_linear':float(a['linear_actual'].min()),'zero_rows':int(np.sum(a['scales']==0))})
 for i in range(8):
  pre=idx[(arm,fit,base,'COMMON',2,'old',i)];post=idx[(arm,fit,base,br,3,'old',i)];prediction=float(a['A'][i].astype('f8')@delta);ref,_=margin_reference(a['params'],[22,20+(i>=4),i],pre['target']);predref=float(ref@delta);actual=post['logit_margin']-pre['logit_margin']
  resid.append({'arm':arm,'branch':br,'fit':fit,'base':base,'cue':i,'frame':k,'linear_prediction':prediction,'independent_gradient_prediction':predref,'actual_margin_change':actual,'nonlinear_residual':actual-prediction,'pre_margin':pre['logit_margin'],'post_margin':post['logit_margin'],'pre_correct':pre['correct'],'post_correct':post['correct']})
for n,rows in [('DEVELOPMENT_SUMMARY',summary),('DEVELOPMENT_FIRST_CORRECTION',pairs),('DEVELOPMENT_OLD_INDIVIDUAL',old),('DEVELOPMENT_NONLINEAR_RESIDUALS',resid),('DEVELOPMENT_NORM_MATCH',norms)]:write_csv(out/(n+'.csv'),rows)
gate=json.loads((r/'A0_AND_GUARDS_LOCK.json').read_text());floors=[]
for g in gate['fits']:floors.append({**g,'maximum_possible_gain':20-g['frozen_correct'],'relative_gain_criterion_attainable':20-g['frozen_correct']>=4,'absolute_accuracy_pass':g['development_correct']>=16,'initial_inventory_pass':g['initial_correct']==8})
write_csv(out/'ADMISSION_COMPONENTS.csv',floors)
results={'status':'EXPLORATORY_DEVELOPMENT_ONLY','admission':gate['status'],'heldout_not_generated':not plan['heldout_generated'],'all_neural_query_rows':len(qq),'incorrect_rows':sum(not x['correct'] for x in qq),'initial_fits':8,'all_absolute_floors_pass':all(x['absolute_accuracy_pass'] and x['initial_inventory_pass'] for x in floors),'impossible_relative_gate_fit_cases':[{'arm':x['arm'],'fit':x['fit'],'frozen_correct':x['frozen_correct'],'maximum_possible_gain':x['maximum_possible_gain']} for x in floors if not x['relative_gain_criterion_attainable']],'by_method':{}}
for arm in ('G','L'):
 pp=[x for x in pairs if x['arm']==arm];rr=[x for x in resid if x['arm']==arm and x['branch']=='P'];nn=[x for x in norms if x['arm']==arm and x['branch']=='P']
 results['by_method'][arm]={'first_correct':{br:sum(x[br+'_correct'] for x in pp) for br in ('B1','B2','P','S')},'out_of':16,'P_lost_B1':sum(x['P_lost_B1'] for x in pp),'P_lost_B2':sum(x['P_lost_B2'] for x in pp),'P_minus_S':sum(x['P_minus_S'] for x in pp),'P_mean_norm':float(np.mean([x['norm_P'] for x in nn])),'P_norm_min':min(x['norm_P'] for x in nn),'P_norm_max':max(x['norm_P'] for x in nn),'P_S_mean_cosine':float(np.mean([x['P_S_cosine'] for x in nn])),'max_relative_norm_mismatch':max(x['relative_norm_mismatch'] for x in nn),'P_negative_real_margin_count':sum(x['actual_margin_change']<0 for x in rr),'P_real_margin_count':len(rr),'P_negative_beyond_1e_6':sum(x['actual_margin_change']< -1e-6 for x in rr),'P_min_actual_margin_change':min(x['actual_margin_change'] for x in rr),'P_max_actual_margin_change':max(x['actual_margin_change'] for x in rr),'P_linear_prediction_min':min(x['linear_prediction'] for x in rr),'P_lost_old_label_in_any_tail':sum(x['lost_prefork'] for x in old if x['arm']==arm and x['branch']=='P')}
(out/'EXPLORATORY_SUMMARY.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
