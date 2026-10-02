"""Fixed full-panel assessment; never imported by learner or schedule.
Every probability is a model score, not a calibrated downstream risk estimate.
"""
import collections
import numpy as np
BRANCHES=('B1','U','D','B4','F4')
PROFILES={'cautious':.01,'primary':.03,'permissive':.05}

def assess(rows,calibration,plan):
    groups=collections.defaultdict(list)
    for r in rows:
        if r['phase'] in ('development','heldout') and r['arm'] in ('G','L') and r['kind'] in ('focal','old'):
            groups[(r['session'],r['method'],r['fit'],r['base'],r['phase'])].append(r)
    cycles=[];stages=[];individual=[];ops=[]
    def prob(r):return (1.+r['probability_margin'])/2.
    for (sid,method,fit,base,phase),rr in sorted(groups.items()):
        meta={'session':sid,'method':method,'fit':fit,'base':base,'phase':phase}
        anchor={r['cue']:r for r in rr if r['branch']=='COMMON' and r['trial']==2 and r['stage']=='post_real'}
        f=plan['sessions'][sid]['focal'];assert len(anchor)==9
        old_anchor=np.array([prob(anchor[c]) for c in range(8)])
        # The pre-correction focal readout was scored under its OLD label. Re-evaluate it under the released correction.
        new_target=plan['sessions'][sid]['transactions'][2]['target'];ar=anchor[f]
        zz=np.array([ar['logit0'],ar['logit1']]);pp=np.exp(zz-zz.max());pp/=pp.sum();focal_anchor=float(pp[new_target])
        for branch in BRANCHES:
            br=[r for r in rr if r['branch']==branch];by=collections.defaultdict(dict)
            for r in br:
                k=(r['trial'],r['stage']);assert r['cue'] not in by[k];by[k][r['cue']]=r
            assert all(len(x)==9 for x in by.values())
            states={}
            for (tr,stage),rs in sorted(by.items()):
                old=np.array([prob(rs[c]) for c in range(8)]);drop=old_anchor-old;fo=rs[f]
                v={**meta,'branch':branch,'trial':tr,'stage':stage,'mean_old_probability':float(old.mean()),'mean_old_loss':float(np.mean([rs[c]['loss'] for c in range(8)])),'old_correct':sum(rs[c]['correct'] for c in range(8)),'old_mean_drop':float(drop.mean()),'old_worst_drop':float(drop.max()),'old_min_probability':float(old.min()),'focal_correct':fo['correct'],'focal_probability':prob(fo),'focal_loss':fo['loss'],'focal_gain':prob(fo)-focal_anchor,'joint_probability_gain':float((np.sum(old-old_anchor)+prob(fo)-focal_anchor)/9.),'focal_parent_probability_under_new_target':focal_anchor}
                states[(tr,stage)]=v;ops.append(v)
                for c in range(8):individual.append({**meta,'branch':branch,'trial':tr,'stage':stage,'cue':c,'target':rs[c]['target'],'anchor_probability':float(old_anchor[c]),'probability':float(old[c]),'probability_drop':float(drop[c]),'correct':rs[c]['correct'],'loss':rs[c]['loss'],'source_frame':rs[c]['frame']})
            ends=[]
            for tr in range(3,9):
                st='post_batch_1' if branch in ('D','F4') and tr<=6 else ('post_batch_4' if branch=='B4' and tr==6 else 'post_real')
                v=states[(tr,st)];ends.append(v);stages.append(v)
            vv=list(states.values())
            transient=all(v['old_mean_drop']<=.10 and v['old_worst_drop']<=.35 and v['old_correct']>=7 for v in vv)
            new_ok=all(v['focal_correct'] for v in ends)
            for profile,tol in PROFILES.items():
                def opok(v):return v['old_mean_drop']<=tol and v['old_worst_drop']<=.20 and v['old_correct']>=7
                restored=all(opok(v) for v in ends if v['trial']>=6)
                gain=all(v['joint_probability_gain']>0 for v in ends if v['trial']>=6)
                sustained=next((v['trial'] for j,v in enumerate(ends) if all(opok(w) for w in ends[j:])),None)
                failures=[]
                if not transient:failures.append('TRANSIENT_ENVELOPE')
                if not new_ok:failures.append('FOCAL_ACQUISITION_OR_SURVIVAL')
                if not restored:failures.append('OPERATING_RECOVERY_OR_PERSISTENCE')
                if not gain:failures.append('NONPOSITIVE_RETAINED_JOINT_GAIN')
                cycles.append({**meta,'branch':branch,'profile':profile,'recovery_mean_drop_allowance':tol,'transient_ok':int(transient),'focal_ok':int(new_ok),'recovery_ok':int(restored),'retained_gain_ok':int(gain),'cycle_pass':int(not failures),'failure_reasons':'|'.join(failures),'first_correction_correct':ends[0]['focal_correct'],'consolidation_old_loss':ends[3]['mean_old_loss'],'final_old_loss':ends[-1]['mean_old_loss'],'final_old_mean_drop':ends[-1]['old_mean_drop'],'final_focal_loss':ends[-1]['focal_loss'],'final_joint_probability_gain':ends[-1]['joint_probability_gain'],'peak_actual_old_mean_drop':max(v['old_mean_drop'] for v in vv),'peak_actual_old_loss':max(v['mean_old_loss'] for v in vv),'stage_mean_old_loss':float(np.mean([v['mean_old_loss'] for v in ends])),'old_outside_operating_stages':sum(not opok(v) for v in ends),'sustained_recovery_from_stage':sustained,'actual_observed_boundaries':len(vv),'maintenance_applications':4 if branch in ('D','B4','F4') else 0,'maintenance_examples':32 if branch in ('D','B4','F4') else 0})
    decision={'primary_profile':'primary','thresholds_are_provisional_lab_contract_not_production_risk':True,'claim':'bounded full-cycle feasibility; no serving, cumulative plasticity, unseen-skill or efficiency guarantee','results':[]}
    for phase in ('development','heldout'):
        for method in ('G','L'):
            for branch in BRANCHES:
                for profile in PROFILES:
                    q=[r for r in cycles if r['phase']==phase and r['method']==method and r['branch']==branch and r['profile']==profile]
                    if not q:continue
                    n=len(q);minimum=29 if phase=='heldout' else 15
                    fits={str(f):sum(r['cycle_pass'] for r in q if r['fit']==f) for f in range(4)}
                    count=sum(r['cycle_pass'] for r in q)
                    qualified=count>=minimum and min(fits.values())>=(6 if phase=='heldout' else 3)
                    decision['results'].append({'phase':phase,'method':method,'branch':branch,'profile':profile,'contexts':n,'qualified_cycles':count,'by_fit':fits,'first_correction_correct':sum(r['first_correction_correct'] for r in q),'new_behavior_cycles':sum(r['focal_ok'] for r in q),'transient_ok_cycles':sum(r['transient_ok'] for r in q),'recovery_ok_cycles':sum(r['recovery_ok'] for r in q),'positive_retained_gain_cycles':sum(r['retained_gain_ok'] for r in q),'mean_final_old_loss':float(np.mean([r['final_old_loss'] for r in q])),'mean_final_focal_loss':float(np.mean([r['final_focal_loss'] for r in q])),'mean_final_joint_gain':float(np.mean([r['final_joint_probability_gain'] for r in q])),'screen':('PASS' if qualified else 'FAIL') if phase=='heldout' else 'DEVELOPMENT_DIAGNOSTIC_ONLY'})
    decision['heldout_assessed']=any(r['phase']=='heldout' for r in cycles)
    return decision,cycles,stages,individual,ops
