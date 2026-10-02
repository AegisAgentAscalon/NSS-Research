"""Independent score-table contrasts at a common, explicitly reused observation grid.
No learner/controller/generator imports; only retained decoded score rows.
"""
import numpy as np
BOUNDARIES=((3,'PRE_EXTRA'),(3,'POST_EXTRA'),(4,'PRE_EXTRA'),(4,'POST_EXTRA'),(5,'POST_REAL'),(6,'POST_REAL'))
BRANCHES=('B1','U','E','LATE')
def assess(qrows,calibration,plan):
    data=[r for r in qrows if r['phase']=='heldout']
    if not data:return {},[],[],[],[]
    idx={(r['arm'],r['fit'],r['base'],r['branch'],r['trial'],r['kind'],r['cue'],r['stage']):r for r in data}
    def actual(arm,fit,base,branch,tr,kind,c,stage='post_real'):
        return idx[(arm,fit,base,branch,tr,kind,c,stage)]
    def at(arm,fit,base,br,boundary,kind,c):
        tr,where=boundary
        has_extra=(br=='E' and tr==3) or (br=='LATE' and tr==4)
        stage='post_extra' if where=='POST_EXTRA' and has_extra else 'post_real'
        return actual(arm,fit,base,br,tr,kind,c,stage)
    decisions={};first=[];cells_all=[];individual=[];changes=[]
    for arm in ('G','L'):
        tau=calibration[arm];arm_first=[]
        for base in range(4,12):
            for fit in range(4):
                f=base+8;row={'arm':arm,'base':base,'fit':fit}
                for br in BRANCHES:
                    r=at(arm,fit,base,br,(3,'POST_EXTRA'),'focal',f)
                    for metric in ('correct','loss','logit_margin','probability_margin'):row[br+'_'+metric]=r[metric]
                first.append(row);arm_first.append(row)
                for br,tr in (('E',3),('LATE',4)):
                    for c in [f,*range(8)]:
                        kind='focal' if c==f else 'old';p=actual(arm,fit,base,br,tr,kind,c);q=actual(arm,fit,base,br,tr,kind,c,'post_extra')
                        changes.append({'arm':arm,'base':base,'fit':fit,'branch':br,'trial':tr,'cue':c,'kind':kind,'before_frame':p['frame'],'after_frame':q['frame'],'before_correct':p['correct'],'after_correct':q['correct'],'broken_to_repaired':int(not p['correct'] and q['correct']),'correct_to_broken':int(p['correct'] and not q['correct']),'loss_change':q['loss']-p['loss'],'probability_margin_change':q['probability_margin']-p['probability_margin']})
        branch_results={};arm_ind={};arm_cells={}
        for br in BRANCHES:
            rr=[];cells=[]
            for base in range(4,12):
                for fit in range(4):
                    f=base+8
                    for tr,where in BOUNDARIES:
                        focal=at(arm,fit,base,br,(tr,where),'focal',f)
                        fu=at(arm,fit,base,'U',(tr,where),'focal',f)
                        for c in range(8):
                            pre=actual(arm,fit,base,'COMMON',2,'old',c);r=at(arm,fit,base,br,(tr,where),'old',c);b=at(arm,fit,base,'B1',(tr,where),'old',c)
                            rr.append({'arm':arm,'branch':br,'base':base,'fit':fit,'trial':tr,'boundary':where,'source_stage':r['stage'],'source_frame':r['frame'],'time_aligned_reuse':bool(where=='POST_EXTRA' and r['stage']=='post_real'),'cue':c,'target':r['target'],'pre_correct':pre['correct'],'B1_correct':b['correct'],'candidate_correct':r['correct'],'lost_prefork_label':int(pre['correct'] and not r['correct']),'additional_error':int(b['correct'] and not r['correct']),'loss':r['loss'],'loss_delta':r['loss']-b['loss'],'margin_decrease':b['probability_margin']-r['probability_margin'],'probability_margin':r['probability_margin'],'logit_margin':r['logit_margin'],'focal_correct':focal['correct'],'focal_loss':focal['loss'],'focal_U_regression':int(fu['correct'] and not focal['correct'])})
                for tr,where in BOUNDARIES:
                    z=[r for r in rr if r['base']==base and r['trial']==tr and r['boundary']==where];assert len(z)==32
                    dl=float(np.mean([r['loss_delta'] for r in z]));dm=float(np.mean([r['margin_decrease'] for r in z]))
                    cells.append({'arm':arm,'branch':br,'base':base,'trial':tr,'boundary':where,'n_old_readouts':len(z),'old_correct':sum(r['candidate_correct'] for r in z),'mean_old_loss':float(np.mean([r['loss'] for r in z])),'mean_loss_delta_B1':dl,'mean_margin_decrease_B1':dm,'tau_loss':tau['tau_loss'],'tau_margin':tau['tau_margin'],'confidence_pass':bool(dl<=tau['tau_loss'] and dm<=tau['tau_margin'])})
            pooled=[]
            for tr,where in BOUNDARIES:
                z=[r for r in rr if r['trial']==tr and r['boundary']==where];assert len(z)==256
                dl=float(np.mean([r['loss_delta'] for r in z]));dm=float(np.mean([r['margin_decrease'] for r in z]))
                pooled.append({'trial':tr,'boundary':where,'correct_old':sum(r['candidate_correct'] for r in z),'old_total':len(z),'mean_old_loss':float(np.mean([r['loss'] for r in z])),'min_correct_probability':float(min((r['probability_margin']+1)/2 for r in z)),'mean_loss_delta_B1':dl,'mean_margin_decrease_B1':dm,'focal_correct':sum(r['focal_correct'] for r in z if r['cue']==0),'focal_total':32,'confidence_pass':bool(dl<=tau['tau_loss'] and dm<=tau['tau_margin'])})
            gf=[sum(r[br+'_correct']-r['B1_correct'] for r in arm_first if r['fit']==fit) for fit in range(4)]
            gb=[sum(r[br+'_correct']-r['B1_correct'] for r in arm_first if r['base']==base) for base in range(4,12)]
            eff=sum(g>=1 for g in gf)>=3 and sum(g>0 for g in gb)>=6 and np.mean([r[br+'_loss']-r['B1_loss'] for r in arm_first])<=0
            no_first_loss=all(r[br+'_correct']>=r['U_correct'] for r in arm_first)
            labels=not any(r['lost_prefork_label'] or r['additional_error'] for r in rr)
            confid=all(c['confidence_pass'] for c in cells+pooled)
            focal=not any(r['focal_U_regression'] for r in rr)
            branch_results[br]={'first_correct':sum(r[br+'_correct'] for r in arm_first),'first_total':32,'first_loss':float(np.mean([r[br+'_loss'] for r in arm_first])),'gain_by_fit':gf,'gain_by_base':gb,'efficacy_pass':bool(eff),'no_U_first_regression':no_first_loss,'all_boundary_old_labels_pass':labels,'all_boundary_old_confidence_pass':confid,'all_boundary_focal_no_U_regression':focal,'lost_prefork_observations':sum(r['lost_prefork_label'] for r in rr),'extra_errors_vs_B1':sum(r['additional_error'] for r in rr),'confidence_failing_base_boundaries':sum(not c['confidence_pass'] for c in cells),'full_trajectory_screen_pass':bool(eff and no_first_loss and labels and confid and focal),'pooled':pooled}
            individual+=rr;cells_all+=cells;arm_ind[br]=rr;arm_cells[br]=cells
        contrasts=[]
        for base in range(4,12):
            for tr,where in BOUNDARIES:
                early=next(c for c in arm_cells['E'] if (c['base'],c['trial'],c['boundary'])==(base,tr,where));late=next(c for c in arm_cells['LATE'] if (c['base'],c['trial'],c['boundary'])==(base,tr,where))
                contrasts.append({'base':base,'trial':tr,'boundary':where,'late_minus_early_mean_old_loss':late['mean_old_loss']-early['mean_old_loss'],'late_minus_early_correct_old':late['old_correct']-early['old_correct']})
        # Explicitly exploratory timing contrast; no post-hoc significance or newly tuned success threshold.
        finals=[c for c in contrasts if c['trial']==6]
        decisions[arm]={'calibration':tau,'branches':branch_results,'timing_contrasts':contrasts,'late_final_loss_lower_bases':sum(c['late_minus_early_mean_old_loss']<0 for c in finals),'late_minus_early_final_mean_loss':float(np.mean([c['late_minus_early_mean_old_loss'] for c in finals])),'interpretation':'Paired timing contrasts are descriptive/exploratory. A final benefit cannot erase earlier harm; strict trajectory screen uses every common boundary.'}
    return decisions,first,cells_all,individual,changes
