"""Summaries include every registered seed, not best-seed selection."""
import sys,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.models import MODES
from nbr01_exist.util import write_json

def stat(xs):
    xs=[float(x) for x in xs if x is not None]
    return dict(mean=statistics.mean(xs),sample_sd=statistics.stdev(xs) if len(xs)>1 else 0.,n=len(xs),values=xs)
def main():
    by={}
    for mode in MODES:
        docs=[json.loads((ROOT/'evidence/results'/f'{mode}_rep{s}.json').read_text()) for s in range(301,306)]
        out={};out['seeds']=[d['seed'] for d in docs];out['raw_state_bytes_per_stream']=docs[0]['raw_state_bytes_per_stream']
        out['lifecycle']={}
        for sigma in [0.,.15,.30]:
            endpoints=[];passes=[];minimum=[]
            for d in docs:
                rs=[r for r in d['rows'] if r['case']=='lifecycle' and r['sigma']==sigma]
                final=next(r for r in rs if r['phase']=='rewritten' and r['round']==1024);endpoints.append(final)
                passed=all(r[k]>=.95 for r in rs if r['round']==1024 for k in ['known_accuracy','unknown_accuracy'])
                passed=passed and all(r['focus_accuracy']>=.95 for r in rs if r['round']==0 and r['phase'] in ('first_write','correction','rewritten')) and final['all_read_stream_success']>=.95
                passes.append(bool(passed));minimum.append(min(r[k] for r in rs if r['round']==1024 for k in ['known_accuracy','unknown_accuracy']))
            out['lifecycle'][str(sigma)]={k:stat([r[k] for r in endpoints]) for k in ['known_accuracy','unknown_accuracy','existence_accuracy','all_read_stream_success']}
            out['lifecycle'][str(sigma)].update(passes=passes,passed_seeds=sum(passes),min_phase_endpoint=stat(minimum))
        ext=[];xp=[]
        for d in docs:
            empty=next(r for r in d['rows'] if r['case']=='extended_empty' and r['round']==4096)
            wr=[r for r in d['rows'] if r['case']=='extended_write']
            ep=next(r for r in wr if r['round']==256);ext.append(ep)
            xp.append(all(r[k]>=.95 for r in [empty,*wr] for k in ['known_accuracy','unknown_accuracy','existence_accuracy']) and empty['all_read_stream_success']>=.95)
        out['extended']={k:stat([r[k] for r in ext]) for k in ['known_accuracy','unknown_accuracy','existence_accuracy','focus_accuracy']};out['extended'].update(passes=xp,passed_seeds=sum(xp))
        out['presence_chronic']=[]
        for sigma,common in [(.15,False),(.30,False),(.45,False),(.30,True),(.45,True)]:
            rows=[r for d in docs for r in d['rows'] if r['case']=='presence_chronic' and r['sigma']==sigma and r['common']==common and r['round']==2048]
            if rows:out['presence_chronic'].append(dict(sigma=sigma,common=common,**{k:stat([r[k] for r in rows]) for k in ['known_accuracy','unknown_accuracy','existence_accuracy','all_read_stream_success']}))
        out['faults']=[]
        for fault in ['one_sign','all_signs','erase_presence','erase_content']:
            rows=[r for d in docs for r in d['rows'] if r['case']=='state_fault' and r['fault']==fault and r['round']==128]
            if rows:out['faults'].append(dict(fault=fault,**{k:stat([r[k] for r in rows]) for k in ['known_accuracy','unknown_accuracy','existence_accuracy','present_unreadable_fraction']}))
        out['write_delivery']=[]
        for old in ['empty','populated']:
            for delivery in ['content_only','whole_state']:
                for alpha in [.25,.5,.75,1.]:
                    rows=[r for d in docs for r in d['rows'] if r['case']=='write_delivery' and r['round']==16 and r['old_kind']==old and r['delivery']==delivery and r['alpha']==alpha]
                    out['write_delivery'].append(dict(old_kind=old,delivery=delivery,alpha=alpha,focus_accuracy=stat([r['focus_accuracy'] for r in rows]),existence_accuracy=stat([r['existence_accuracy'] for r in rows])))
        out['local_dynamics']=[d['local_dynamics'] for d in docs if d['local_dynamics']]
        by[mode]=out
    train=[json.loads(p.read_text()) for p in (ROOT/'evidence/main').glob('*.json') if '.prerun.' not in p.name]
    results=[json.loads(p.read_text()) for p in (ROOT/'evidence/results').glob('*.json')]
    answer=dict(study='ExistenceContent005',modes=by,completed_fits=len(train),optimizer_steps=sum(t['steps'] for t in train),
        sequence_presentations=sum(t['sequence_presentations'] for t in train),supervised_event_presentations=sum(t['supervised_event_presentations'] for t in train),
        training_wall_seconds_sum=sum(t['train_wall_seconds'] for t in train),training_cpu_seconds_sum=sum(t['train_cpu_seconds'] for t in train),
        metric_rows=sum(d['metric_rows'] for d in results),saved_answer_evaluations=sum(d['saved_answer_evaluations'] for d in results),evaluation_configurations=len(results),
        caution='Five paired learned representations, not metric cells, are replication units. Source representations and content repairs are reused and not free.')
    write_json(ROOT/'SUMMARY.json',answer)
    for mode,out in by.items():
        d=out['lifecycle']['0.15'];print(mode,*(round(d[k]['mean']*100,4) for k in ['known_accuracy','unknown_accuracy','existence_accuracy','all_read_stream_success']),'passes',d['passed_seeds'])
if __name__=='__main__':main()
