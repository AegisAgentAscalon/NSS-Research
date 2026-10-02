"""Aggregate every completed seed without selecting successful runs."""
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parents[1]


def build():
    runs=[json.loads(p.read_text()) for p in sorted((ROOT/'evidence/pilot').glob('*_seed*.json'))
          if not p.name.endswith('_prerun.json')]
    if len(runs)!=20:raise ValueError('Expected all20 completed training runs')
    rows=[x for r in runs for x in r['evaluation']]
    diagnostic=json.loads((ROOT/'evidence/GATE_DIAGNOSTIC.json').read_text())
    rows += [x for r in diagnostic['results'] for x in r['evaluation']]
    cells=[]
    for kind in sorted({x['kind'] for x in rows}):
        for condition in ('early_cue','overwrite','no_cue'):
            for delay in (0,4,16,64,128):
                for keep in (False,True):
                    for depth in (1,2,4,8):
                        values=[x['accuracy'] for x in rows if x['kind']==kind and x['condition']==condition
                                and x['delay']==delay and x['keep']==keep and x['depth']==depth]
                        if len(values)!=5:raise ValueError('Missing seed')
                        cells.append({'kind':kind,'condition':condition,'delay':delay,'keep':keep,'depth':depth,
                                      'seed_count':5,'mean':statistics.mean(values),'sample_sd':statistics.stdev(values),
                                      'min':min(values),'max':max(values),'seed_order':[201,202,203,204,205],
                                      'values':values,'instances_per_seed':256})
    screens=[]
    for result in runs:
        kind=result['training']['kind']
        selected=[x for x in result['evaluation'] if x['kind']==kind and x['keep'] and x['delay'] in (0,4,16)
                  and x['depth'] in (1,2,4)]
        known=[x for x in selected if x['condition']!='no_cue'];unknown=[x for x in selected if x['condition']=='no_cue']
        recall=sum(x['correct'] for x in known)/sum(x['n'] for x in known)
        empty=sum(x['correct'] for x in unknown)/sum(x['n'] for x in unknown)
        screens.append({'kind':kind,'seed':result['training']['seed'],'known_recall':recall,
                        'unknown_accuracy':empty,'passes_pilot_screen':recall>=.95 and empty>=.95})
    resources=[]
    for kind in ('gru','gated','hard_gated','transformer'):
        same=[r for r in runs if r['training']['kind']==kind];t=same[0]['training']
        resources.append({'kind':kind,'parameters':t['parameter_count'],'weight_bytes':t['parameter_bytes'],
                          'optimizer_tensor_bytes':t['optimizer_tensor_bytes'],'gradient_bytes':t['gradient_bytes_when_allocated'],
                          'five_seed_training_seconds':sum(r['training']['train_wall_seconds'] for r in same),
                          'min_sampled_training_RSS':min(r['memory']['train_sampled_peak_bytes'] for r in same),
                          'max_sampled_training_RSS':max(r['memory']['train_sampled_peak_bytes'] for r in same)})
    summary={'study':'NBR-01/Pilot001','status':'PILOT_AND_POSTHOC_DIAGNOSTICS_RUN_FULL_NBR01_OPEN',
             'completed_pilot_training_runs':20,'optimizer_steps_in_completed_pilot':12000,
             'training_example_presentations_in_completed_pilot':768000,
             'development_training_runs':3,'development_optimizer_steps':900,
             'full_training_reproduction_runs':1,'reproduction_optimizer_steps':600,
             'interrupted_attempts_excluded_from_completed_totals':2,
             'pilot_metric_cells':sum(len(r['evaluation']) for r in runs),
             'posthoc_hard_admission_metric_cells':sum(len(r['evaluation']) for r in diagnostic['results']),
             'baseline_screens':screens,'resources':resources,'aggregate_cells':cells,
             'uncertainty':'SD describes variability across five training/data seeds; not a confidence interval or significance claim.',
             'label_scope':'Eight known symbols plus UNKNOWN, explicit write/distractor tokens, short training horizons. Not language or full companion cognition.',
             'NBR02_to_07':'NOT_RUN','architecture_acceptance':False}
    return summary

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    with args.output.open('x') as f:json.dump(build(),f,indent=2,allow_nan=False);f.write('\n')
