"""Post-result independent recount and fresh-process replay; zero updates."""
from pathlib import Path
import sys,json,shutil,tempfile,collections,time
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from cap01 import *

def model(seed,mode):
    m=Reader();m.load_state_dict(torch.load(ROOT/f'checkpoints/{seed}_{mode}.pt',weights_only=True,map_location='cpu')['model']);m.eval();return m

def recount():
    cases=json.loads((ROOT/'CASES.json').read_text());rows=[];errors=[]
    for c in cases:
        p=ROOT/'results/cases'/f"{c['id']}.json"
        if not p.exists():errors.append(('missing',c['id']));continue
        r=json.loads(p.read_text());e=json.loads((ROOT/'fixtures'/f"{c['fixture']}.json").read_text())['episode'];w=e['worlds'][c['rev']]
        if r['status']=='TECHNICAL_FAILURE':errors.append(('technical',c['id']));continue
        ys=[]
        for tid in sorted(e['targets']):
            # Independently derive labels without importing either study scorer.
            label=3
            if all(w['progress'][d]==1 for d in w['deps'][tid]):label=2
            if w['progress'][tid]==1:label=1
            if w['freeze']==1:label=0
            ys.append(label)
        a=np.asarray(r['logits']);pred=a.argmax(-1);truth=np.asarray(ys)
        if ys!=r['targets_y'] or pred.tolist()!=r['predictions'] or int((truth==pred).sum())!=r['correct'] or bool((truth==pred).all())!=r['whole_correct']:
            errors.append(('recount',c['id']))
        if r['stats']['peak_selected_positions']>c['cap']:errors.append(('budget',c['id']))
        if not np.array_equal(pred,np.argmax(r['reference_logits'],axis=-1)):errors.append(('class_reference',c['id']))
        rows.append(r)
    paired={};paircheck=[]
    for r in rows:
        c=r['case'];key=(c['fixture'],c['rev'],c['seed'],c['mode'],c['cap']);paired.setdefault(key,{})[c['policy']]=r
    for k,v in paired.items():
        a,b=v['ordinary'],v['segmented'];c=compare(a['logits'],b['logits'])
        same=a['predictions']==b['predictions'];paircheck.append({'key':k,'class_same':same,'numeric':c})
        if not same or c['violations']:errors.append(('policy_disagreement',k))
    locked=json.loads((ROOT/'SOURCE_FIXTURE_LOCK.json').read_text());locks=[k for k,v in locked['files'].items() if file_sha(ROOT/k)!=v]
    # Pick fixed representative replays, not only correct cases.
    picks=[]
    for n in [8,32,128,512]:
        for seed in ([8801,8802,8804] if n<512 else [8801]):
            for mode in ['dense','hsa']:
                for policy in ['ordinary','segmented']:
                    candidates=sorted([r for r in rows if r['n']==n and r['case']['seed']==seed and r['case']['mode']==mode and r['case']['policy']==policy and r['family']=='dispersed' and r['case']['rev']==0 and r['case']['cap']==32],key=lambda r:r['case']['id'])
                    picks.append(candidates[0]['case'])
    write_json(ROOT/'results/AUDIT_REPLAY_PLAN.json',picks)
    out={'case_recounts':len(rows),'policy_pairs':len(paircheck),'errors':errors,'lock_mismatches':locks,'policy_checks':paircheck,'selected_replay_cases':len(picks)}
    write_json(ROOT/'results/RECOUNT.json',out)
    print({k:v for k,v in out.items() if k!='policy_checks'})

def replay(start,end):
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    picks=json.loads((ROOT/'results/AUDIT_REPLAY_PLAN.json').read_text());res=[];t0=time.perf_counter()
    for c in picks[start:end]:
        rec=json.loads((ROOT/'results/cases'/f"{c['id']}.json").read_text());e=json.loads((ROOT/'fixtures'/f"{c['fixture']}.json").read_text())['episode'];w=e['worlds'][c['rev']]
        m=model(c['seed'],c['mode'])
        with tempfile.TemporaryDirectory(prefix='cap01_audit_',dir='/mnt/data') as temp:
            eng=StreamExecutor(m,w,e['targets'],c['mode'],c['policy'],c['cap'],temp);eng.advance();got=eng.logits()
            eq=bool(np.array_equal(got,np.asarray(rec['logits'],dtype=np.float32)))
            res.append({'case':c['id'],'bit_exact':eq,'numeric':compare(got,rec['logits'])})
    write_json(ROOT/'results'/f'REPLAY_{start}_{end}.json',{'results':res,'seconds':time.perf_counter()-t0,'optimizer_applications':0})
    print('fresh replay',start,end,'bitexact',sum(x['bit_exact'] for x in res),'/',len(res))

def resume(start,end):
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    dirs=sorted((ROOT/'results/paused').iterdir());results=[];t0=time.perf_counter()
    for d in dirs[start:end]:
        c=json.loads((d/'CASE.json').read_text());r=json.loads((ROOT/'results/cases'/f"{c['id']}.json").read_text())
        e=json.loads((ROOT/'fixtures'/f"{c['fixture']}.json").read_text())['episode'];w=e['worlds'][0];m=model(c['seed'],c['mode'])
        snap=json.loads((d/'resume.json').read_text())['payload'];partial=snap['key_offset']
        with tempfile.TemporaryDirectory(prefix='cap01_resume_audit_',dir='/mnt/data') as temp:
            cp=Path(temp)/'paused';shutil.copytree(d,cp)
            eng=StreamExecutor.restore(cp/'resume.json',m,w,e['targets'],c['mode'],c['policy'],c['cap']);eng.advance();a=eng.logits()
            results.append({'case':c['id'],'bit_exact':bool(np.array_equal(a,np.asarray(r['logits'],dtype=np.float32))),
                            'saved_stage':snap['stage'],'saved_group':snap['group'],'saved_key_offset':partial})
    write_json(ROOT/'results'/f'RESUME_AUDIT_{start}_{end}.json',{'results':results,'seconds':time.perf_counter()-t0,'optimizer_applications':0})
    print('paused resume',start,end,'bitexact',sum(x['bit_exact'] for x in results),'/',len(results))
if __name__=='__main__':
    if sys.argv[1]=='recount':recount()
    elif sys.argv[1]=='replay':replay(int(sys.argv[2]),int(sys.argv[3]))
    elif sys.argv[1]=='resume':resume(int(sys.argv[2]),int(sys.argv[3]))
