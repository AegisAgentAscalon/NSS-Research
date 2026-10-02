"""Runs only after all four parents pass admission; no automatic rescue."""
from common import *
from study import check_lock, record_failure
import traceback

@torch.no_grad()
def evaluate_surface(model,parent,panel,baseline,tag,path):
    N=len(panel['prefixes']); result={}; checks=[]
    canonical_state_hash=sha_arr(baseline['hidden'][:,0])
    for mode in ('CARRY','REBUILD'):
        outputs={key:np.empty((N,129,9),np.float32) for key in ('SHARED','COPIED')}
        all_hidden=np.empty((N,129,64),np.float32)
        for p in (8,24):
            rows=np.where(panel['prefixes']==p)[0]; prefix=panel['tokens'][rows,:p]; suffix=panel['tokens'][rows,p:p+128]
            if mode=='CARRY':
                h0=baseline['hidden'][rows,0].copy()
            else:
                ph,pl=model.rollout(prefix)
                pcheck=check_trajectory(model,prefix,ph.numpy(),pl.numpy(),tag=tag+'/REBUILD_PREFIX')
                checks.append(pcheck); h0=ph[:,-1].numpy().copy()
            hs,ls=model.rollout(suffix,torch.from_numpy(h0.copy()))
            hh=hs.numpy(); ll=ls.numpy()
            copied=torch.stack([parent.head(hs[:,t]) for t in range(128)],1).numpy()
            checks.append(check_trajectory(model,suffix,hh,ll,h0=h0,tag=tag+'/'+mode+'/shared'))
            checks.append(check_trajectory(model,suffix,hh,copied,h0=h0,tag=tag+'/'+mode+'/copied',head=parent.head))
            boundary_h=torch.from_numpy(h0)
            outputs['SHARED'][rows]=np.concatenate([model.head(boundary_h).numpy()[:,None],ll],1)
            outputs['COPIED'][rows]=np.concatenate([parent.head(boundary_h).numpy()[:,None],copied],1)
            all_hidden[rows]=np.concatenate([h0[:,None],hh],1)
        assert_ok(sha_arr(baseline['hidden'][:,0])==canonical_state_hash,'CANONICAL_SAVED_STATE_MUTATED')
        for head in ('SHARED','COPIED'):
            metrics=metrics_by_family(outputs[head],baseline['targets'],panel['families'],reference=baseline['logits'])
            result[mode+'_'+head]={'metrics':metrics}
        if path=='F':
            assert_ok(np.array_equal(outputs['COPIED'],baseline['logits']),'FULLY_PROTECTED_NOT_EXACT',tag+'/'+mode)
        np.savez_compressed(ROOT/'evidence'/f'{tag}_{mode}.npz',shared_logits=outputs['SHARED'],copied_logits=outputs['COPIED'])
        # First observed class-failure reproducer per seed/path/mode/head/family, not all redundant trajectories.
        for head in ('SHARED','COPIED'):
            for f,name in enumerate(FAMILIES):
                seed=tag.split('_')[1]; key=f'main_{seed}_{path}_{mode}_{head}_{name}'
                target=ROOT/'failures'/f'{key}.npz'
                if target.exists(): continue
                for row in np.where(panel['families']==f)[0]:
                    bad=outputs[head][row,1:33].argmax(-1)!=baseline['targets'][row,1:33]
                    if bad.any():
                        p=int(panel['prefixes'][row]); np.savez_compressed(target,tokens=panel['tokens'][row,:p+128],
                            starting_state=all_hidden[row,0],hidden=all_hidden[row],logits=outputs[head][row],targets=baseline['targets'][row])
                        write_json(ROOT/'failures'/f'{key}.json',{'tag':tag,'mode':mode,'head':head,'family':name,'row':int(row),'prefix_length':p,
                                   'first_error_suffix':int(np.flatnonzero(bad)[0])+1,'weights':tag+'.pt','model_hash':hash_sd(model.state_dict()),
                                   'parent_hash':hash_sd(parent.state_dict()),'panel_tokens_hash':sha_arr(panel['tokens']),
                                   'disposition':'Observed symptom; update-surface contrast, not a proven cell-level cause.'})
                        break
        if not all(c['pass'] for c in checks):
            np.savez_compressed(ROOT/'failures'/f'{tag}_{mode}_numerical_full.npz',tokens=panel['tokens'],prefixes=panel['prefixes'],
                                hidden=all_hidden,shared_logits=outputs['SHARED'],copied_logits=outputs['COPIED'])
    write_json(ROOT/'evidence'/f'{tag}_numerical.json',checks)
    assert_ok(all(c['pass'] for c in checks),'NUMERICAL_GATE_FAILED',tag)
    return result


def run():
    check_lock(); initial=json.loads((ROOT/'evidence'/'outcome.json').read_text())
    assert_ok(initial['status']=='PARENTS_ADMITTED','BASELINE_GATE_NOT_PASSED')
    assert_ok(not (ROOT/'evidence'/'adaptation_started.json').exists(),'ADAPTATION_ALREADY_STARTED')
    write_json(ROOT/'evidence'/'adaptation_started.json',{'time_utc':utc(),'parent_status':initial['status']})
    started=time.perf_counter(); cases=[]; evaluations=[]; baselines={}
    for seed in SEEDS:
        parent,_=load_checkpoint(ROOT/'checkpoints'/f'parent_{seed}_2000.pt'); parent_hash=hash_sd(parent.state_dict())
        data=np.load(ROOT/'fixtures'/f'training_{seed}.npz'); panel=make_panel(seed,'confirmation',data['tokens'])
        np.savez_compressed(ROOT/'fixtures'/f'confirmation_{seed}.npz',**panel)
        baseline=score_panel(parent,panel,f'confirmation_parent_{seed}')
        assert_ok(all(c['pass'] for c in baseline['checks']),'NUMERICAL_BASELINE_CONFIRMATION',seed)
        b_original=b_score(parent); basepass=competence(baseline['metrics'],b_original)
        baselines[str(seed)]={'metrics':baseline['metrics'],'original_B':b_original,'parent_confirmation_competence':basepass}
        for cue in (0,3,4,7):
            for path in ('F','U'):
                model,_=load_checkpoint(ROOT/'checkpoints'/f'parent_{seed}_2000.pt'); opt=opt_for(model,frozen=path=='F')
                assert_ok(model.head.weight.data_ptr()!=parent.head.weight.data_ptr(),'READOUT_ALIAS_MAIN')
                cell0=hash_sd(model.cell.state_dict()); bzero=b_score(model,cue)
                base_tag=f'adapt_{seed}_c{cue}_{path}'
                write_json(ROOT/'checkpoints'/f'{base_tag}_0000.json',{'weights_ref':f'parent_{seed}_2000.pt','weights_sha256':sha_file(ROOT/'checkpoints'/f'parent_{seed}_2000.pt'),
                           'optimizer':'fresh empty Adam state, hyperparameters in protocol','stage':0,'frozen_transition':path=='F'})
                log=ROOT/'logs'/f'{base_tag}_updates.jsonl'
                for stage in range(1,65):
                    rec=update(model,opt,correction=cue); b=b_score(model,cue)
                    assert_ok(b['numerical']['pass'],'NUMERICAL_B_ADAPTATION',base_tag+'/'+str(stage))
                    if path=='F': assert_ok(hash_sd(model.cell.state_dict())==cell0,'FROZEN_TRANSITION_CHANGED',base_tag)
                    append_json(log,{'seed':seed,'cue':cue,'path':path,'stage':stage,'update':rec,'B':b})
                    if stage in STAGES:
                        tag=f'{base_tag}_{stage:04d}'
                        save_checkpoint(ROOT/'checkpoints'/f'{tag}.pt',model,opt,stage,{'seed':seed,'cue':cue,'path':path})
                        scores=evaluate_surface(model,parent,panel,baseline,tag,path)
                        write_json(ROOT/'evidence'/f'{tag}_summary.json',scores)
                        evaluations.append({'seed':seed,'cue':cue,'path':path,'stage':stage,'scores':scores,'B':b})
                        if stage==64:
                            for head in ('SHARED','COPIED'):
                                r=scores['CARRY_'+head]['metrics']['32']
                                carry=all(x['event_accuracy']>=.99 and x['whole_rate']>=.95 and x['accuracy_drop_pp']<=1.+1e-10 and x['new_false_done']==0 for x in r.values())
                                rr=scores['REBUILD_'+head]['metrics']['32']
                                rebuilt=all(x['event_accuracy']>=.99 and x['whole_rate']>=.95 and x['accuracy_drop_pp']<=1.+1e-10 and x['new_false_done']==0 for x in rr.values())
                                joint=carry and b['pass'] and basepass
                                cases.append({'seed':seed,'cue':cue,'condition':path+'-'+head,'joint_pass':joint,'B_acquired':b['pass'],
                                              'carry_pass':carry,'rebuild_pass':rebuilt,'parent_confirmation_pass':basepass,'B_min_probability':b['min_true_probability']})
                                if not joint: record_failure('JOINT_SCREEN_FAIL','adaptation_final',cases[-1],{'seed':seed,'cue':cue,'condition':path+'-'+head},'RETAIN_FIXED_OTHER_CONTEXTS')
                    if time.perf_counter()-started+initial['elapsed_main_seconds']>1680: raise RuntimeError('STOP_RUNTIME')
                print('CORRECTION',seed,cue,path,'B minimum',round(b['min_true_probability'],5),'final CARRY',[(x['condition'],x['carry_pass']) for x in cases[-2:]],flush=True)
        assert_ok(hash_sd(parent.state_dict())==parent_hash,'PARENT_MUTATED')
    conditions={c:{'contexts_pass':sum(x['joint_pass'] for x in cases if x['condition']==c),'contexts_total':16,
                   'parents_all_four_pass':sum(all(x['joint_pass'] for x in cases if x['condition']==c and x['seed']==s) for s in SEEDS)} for c in ['F-SHARED','F-COPIED','U-SHARED','U-COPIED']}
    initial.update(status='COMPLETED_BOUNDED_COMPARISON',confirmation_generated=True,conditions=conditions,cases=cases,baselines=baselines,
                   B_main_adaptation_updates=COUNTERS['optimizer_applications'],optimizer_applications_total=8048+COUNTERS['optimizer_applications'],
                   adaptation_counters=COUNTERS,adaptation_elapsed_seconds=time.perf_counter()-started,adaptation_peak_rss=rss())
    write_json(ROOT/'evidence'/'outcome.json',initial)
    write_json(ROOT/'evidence'/'all_stage_metrics.json',evaluations)
    print('COMPLETE',conditions,flush=True)

if __name__=='__main__':
    try: run()
    except Exception as exc:
        record_failure('ADAPTATION_EXECUTION_STOP','adaptation',{'error':str(exc),'traceback':traceback.format_exc(),'counters':COUNTERS})
        write_json(ROOT/'evidence'/'adaptation_stop.json',{'status':'STOP_ADAPTATION','error':str(exc),'counters':COUNTERS,'peak_rss':rss()})
        raise
