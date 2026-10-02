from pathlib import Path
import json,statistics,collections,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr01_recovery.util import write_json
ROOT=Path(__file__).resolve().parents[1]

def summarize(root=ROOT):
    files=sorted((root/'evidence/results').glob('rep*.json'))
    if len(files)!=5:raise RuntimeError('Expected all five pairs')
    runs=[json.loads(p.read_text()) for p in files]
    allrows=[x for r in runs for x in r['rows']]
    grouped=collections.defaultdict(list)
    for x in allrows:grouped[(x['group'],x['condition'],x['level'],x['rounds'],x['mode'])].append(x)
    summary=[]
    for key,rows in sorted(grouped.items()):
        a=dict(zip(('group','condition','level','rounds','mode'),key));a['pairs']=len(rows)
        for category in ('all','known','unknown'):
            values=[x[category]['accuracy'] for x in rows if x[category]['accuracy'] is not None]
            a[category]=dict(mean=statistics.mean(values) if values else None,
                sd=statistics.stdev(values) if len(values)>1 else None,values=values)
        for name in ('latent_mse','stored_fast_mse','max_state_abs','executed_autonomous_updates','stable_wrong_count'):
            values=[x[name] for x in rows]
            a[name]=dict(mean=statistics.mean(values),sd=statistics.stdev(values),values=values)
        if 'changed_address_n' in rows[0]:
            v=[x['changed_address_correct']/x['changed_address_n'] for x in rows]
            a['changed_address_accuracy']=dict(mean=statistics.mean(v),sd=statistics.stdev(v),values=v)
        summary.append(a)
    screens=[]
    for run in runs:
        rows=run['rows']
        for mode in sorted(set(x['mode'] for x in rows)):
            def row(group,condition,level,rounds):
                return next(x for x in rows if (x['group'],x['condition'],x['level'],x['rounds'],x['mode'])==(group,condition,level,rounds,mode))
            clean=row('shock','clean',0.,4);overwrite=row('overwrite','clean',0.,4);reset=row('reset','explicit_clear',0.,4096)
            long=row('long_clean','no_new_observation',0.,4096);short=row('long_clean','no_new_observation',0.,16)
            baseline=(clean['known']['accuracy']>=.95 and clean['unknown']['accuracy']>=.95 and overwrite['changed_address_correct']/overwrite['changed_address_n']>=.95 and reset['unknown']['accuracy']>=.95)
            longpass=(long['known']['accuracy']>=.95 and long['unknown']['accuracy']>=.95 and long['known']['accuracy']>=short['known']['accuracy']-.01 and long['unknown']['accuracy']>=short['unknown']['accuracy']-.01)
            screens.append(dict(rep_seed=run['rep_seed'],mode=mode,competence=baseline,long_stability=longpass))
    training=[json.loads(p.read_text()) for p in (root/'evidence/main').glob('*.json') if not p.name.endswith('.prerun.json')]
    if len(training)!=15:raise RuntimeError('Expected15 trained checkpoints')
    for seed in range(301,306):
        if len({x['training_data_digest'] for x in training if x['rep_seed']==seed})!=1:raise RuntimeError('Training data unmatched')
    result=dict(study='StateRecovery003',main_pairs=len(runs),main_checkpoints=len(training),cells=len(allrows),
        total_answer_evaluations=sum(x['all']['n'] for x in allrows),
        total_main_optimizer_steps=sum(x['steps'] for x in training),
        example_presentations=sum(x['examples'] for x in training),
        training_loop_seconds=sum(x['train_wall_seconds'] for x in training),
        evaluation_seconds=sum(x['eval_wall_seconds'] for x in runs),
        matched_training_data_digest_verified=True,screens=screens,summary=summary,
        frozen_parameters_during_evaluation=True,
        uncertainties='Mean and sample SD across five paired reused representation/new training-data seeds; no best-run selection or claim of new full pretraining')
    write_json(root/'SUMMARY.json',result)
    return result

if __name__=='__main__':
    r=summarize();print({k:v for k,v in r.items() if k not in ('screens','summary')})
