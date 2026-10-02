"""Retained-result analysis only. No optimizer updates and no additional neural scoring."""
from __future__ import annotations
import gzip,json,time
from pathlib import Path
import numpy as np
from common import canonical,sha,write_json
ROOT=Path(__file__).resolve().parents[1]

def main():
    summaries=json.loads((ROOT/'results/summary.json').read_text());failures=[]
    with gzip.open(ROOT/'fixtures/confirmation.jsonl.gz','rt') as f:ws=[json.loads(s) for s in f]
    # Independent explicit rule, not the original oracle function or an NN.
    independent=np.zeros((len(ws),8),np.int64)
    for a,w in enumerate(ws):
        completed={i for i,v in enumerate(w['progress']) if v==1}
        for task in range(8):
            if w['freeze']==1:decision=0
            elif task in completed:decision=1
            elif set(w['deps'][task]).issubset(completed):decision=2
            else:decision=3
            independent[a,task]=decision
    reference=np.load(ROOT/'results/pred_8801_dense_confirmation.npz')['target']
    write_json(ROOT/'results/exact_rule_control.json',{'decisions':int(reference.size),
         'correct':int((independent==reference).sum()),'scope':'Independent deterministic evaluation of the supplied rule; not learned inference or a scientific novelty.'})
    for row in summaries:
        if row['split']!='confirmation':continue
        a=np.load(ROOT/f"results/pred_{row['seed']}_{row['mode']}_confirmation.npz")
        pred=a['logits'].argmax(-1);tar=a['target'];bad=np.argwhere(pred!=tar)
        for wi,task in bad[:8]:
            w=ws[int(wi)];deps=w['deps'][int(task)]
            rec={'seed':row['seed'],'reader':row['mode'],'world_index':int(wi),'task':int(task),
                'target':int(tar[wi,task]),'predicted':int(pred[wi,task]),'logits':a['logits'][wi,task].tolist(),
                'own_progress':w['progress'][int(task)],'dependency_ids':deps,
                'dependency_progress':[w['progress'][d] for d in deps],'global_freeze':w['freeze'],
                'source_world_sha':sha(canonical(w)),
                'classification':'learned_decision_error; available evidence and packet/compiler are not missing; exact internal cause unlocalized'}
            failures.append(rec)
    write_json(ROOT/'failures/learned_decision_examples.json',failures)
    # Verify source lock is unchanged. Added operational/post-result drivers are separately listed.
    lock=json.loads((ROOT/'SOURCE_LOCK.json').read_text());checks=[]
    for rel,entry in lock['files'].items():checks.append({'file':rel,'match':sha((ROOT/rel).read_bytes())==entry['sha256']})
    additional={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'source').glob('*.py') if str(p.relative_to(ROOT)) not in lock['files']}
    write_json(ROOT/'results/source_integrity_audit.json',{'locked_files':checks,'additional_drivers':additional,
        'note':'complete_retained is operational continuation within original cap; post_retained filters unavailable finals; demo/diagnostics are post-result utilities. No locked source altered.'})
    print('diagnostics retained',len(failures),'exact control',int((independent==reference).sum()),flush=True)
if __name__=='__main__':main()
