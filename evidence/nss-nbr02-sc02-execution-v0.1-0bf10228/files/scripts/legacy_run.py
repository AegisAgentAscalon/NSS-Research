"""Locked main correctness/cost observations; no training or source changes."""
from support import *
import argparse,traceback,copy,gc
from sc01 import Store,Workspace,digest
from sh01_common import oracle
from nss_hsa import prepare_worlds,PlanCache

POLICIES=['index','cache','segment']

def execute(ep,model,mid,policy,*,audit=True,snap_dir=None):
    t0=time.perf_counter();store=Store(ep['world']);ws=Workspace(store,mid,policy,ep['record_cap'],ep['result_cap'])
    core=time.perf_counter()-t0;measures=[];checks=[];snapshots=[];account_max={}
    full_cache={};full_calls=0
    for ei,event in enumerate(ep['events']):
        t=time.perf_counter();out=None
        if event['op']=='change':store.mutate(event['change'])
        elif event['op']=='checkpoint':
            raw=ws.snapshot();store_bytes=canonical(store.to_dict())
            if snap_dir:
                p=snap_dir/f"{ep['id']}_{policy}_{ei}.json";p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
                p.with_suffix('.store.json').write_bytes(store_bytes)
            store=Store.from_dict(json.loads(store_bytes));ws=Workspace.restore(raw,store,mid)
            snapshots.append({'event':ei,'workspace_bytes':len(raw),'store_bytes':len(store_bytes),'sha256':hashlib.sha256(raw).hexdigest()})
        elif event['op']=='job':out=ws.job(event['id'],event['tasks'],model,limit_tasks=event.get('limit_tasks'))
        else:raise ValueError('Unknown event')
        core+=time.perf_counter()-t
        ac=ws.accounting()
        for k,v in ac.items():account_max[k]=max(account_max.get(k,0),v)
        if out is not None and audit:
            key=digest(store.world)
            if key not in full_cache:
                x,s=prepare_worlds([store.world]);p=PlanCache().get(s)
                with torch.no_grad():full_cache[key]=model(x,p).numpy()[0]
                full_calls+=1
            full=full_cache[key];truth=oracle(store.world)
            for task,rec in out.items():
                if rec is None:
                    measures.append({'event':ei,'job':event['id'],'task':task,'status':'UNFINISHED_OR_DEFERRED','epoch':store.epoch})
                    continue
                arr=np.array(rec['logits'],dtype=np.float32);cmp=compare(arr,full[task]);checks.append(cmp)
                measures.append({'event':ei,'job':event['id'],'task':task,'status':'ANSWER','epoch':store.epoch,
                                 'target':int(truth[task]),'pred':rec['label'],'full_pred':int(full[task].argmax()),
                                 'logits':rec['logits'],'full_logits':full[task].tolist(),'signature':rec['signature'],
                                 'numerical':cmp,'origin':rec['origin']})
    answered=[m for m in measures if m['status']=='ANSWER'];unresolved=[m for m in measures if m['status']!='ANSWER']
    groups={}
    for m in answered:groups.setdefault((m['event'],m['job']),[]).append(m)
    stats=dict(ws.stats)
    out={'episode':ep['id'],'n':ep['n'],'family':ep['family'],'fixture_seed':ep['seed'],'policy':policy,'model_hash':mid,
         'record_cap':ep['record_cap'],'core_seconds':core,'observed_total_seconds':time.perf_counter()-t0,
         'ingest_seconds':store.ingest_seconds,'ingest_encoded_bytes':store.ingest_bytes,'stats':stats,
         'accounting_peak_payload':account_max,'snapshots':snapshots,'reference_forward_calls':full_calls,
         'answers':len(answered),'correct':sum(m['pred']==m['target']for m in answered),
         'full_correct':sum(m['full_pred']==m['target']for m in answered),
         'changed_classes':sum(m['pred']!=m['full_pred']for m in answered),
         'false_complete':sum(m['pred']==1 and m['target']!=1 for m in answered),
         'unresolved_positions':len(unresolved),
         'answered_job_occasions':len(groups),'whole_answered_job_occasions_correct':sum(all(m['pred']==m['target']for m in ms)for ms in groups.values()),
         'numeric_scalars':sum(c['scalars']for c in checks),'numeric_violations':sum(c['violations']for c in checks),
         'max_abs':max((c['max_abs']for c in checks),default=0.),'max_normalized':max((c['max_normalized']for c in checks),default=0.),
         'final_receipt_count':len(ws.receipts),'historical_receipt_count':len(ws.history),
         'observations':measures,'trace':ws.trace,'final_model_hash':model_hash(model),'optimizer_applications':0}
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--n',type=int,required=True);a.add_argument('--seed',type=int,required=True);args=a.parse_args()
    setup();start=time.perf_counter();done=[]
    for model_seed in [8801,8802,8804]:
        m,mid=load(model_seed)
        for p in sorted((ROOT/'fixtures').glob(f'n{args.n}_s{args.seed}_*.json')):
            ep=json.loads(p.read_text())
            for policy in POLICIES:
                dest=ROOT/'results'/'episodes'/f'{ep["id"]}_m{model_seed}_{policy}.json'
                if dest.exists():raise RuntimeError('Refusing to overwrite executed condition '+str(dest))
                try:
                    out=execute(ep,m,mid,policy,audit=True,
                                snap_dir=(ROOT/'results'/'snapshots')if model_seed==8801 and ep['family']=='resume'else None)
                    out['model_seed']=model_seed;out['runtime']=runtime();save(dest,out)
                    done.append({'file':dest.name,'answers':out['answers'],'changed':out['changed_classes'],'numfail':out['numeric_violations'],
                                 'seconds':out['core_seconds']})
                except Exception:
                    save(ROOT/'failures'/f'run_{ep["id"]}_m{model_seed}_{policy}.json',{'traceback':traceback.format_exc(),'elapsed':time.perf_counter()-start,'runtime':runtime()})
                    raise
                if runtime()['peak_rss_bytes']>2*1024**3 or time.perf_counter()-start>600:raise RuntimeError('RESOURCE_GUARD')
                save(ROOT/'results'/f'progress_n{args.n}_s{args.seed}.json',{'completed':done,'elapsed':time.perf_counter()-start,'runtime':runtime()})
        print('completed',args.n,args.seed,model_seed,flush=True)
    save(ROOT/'results'/f'run_n{args.n}_s{args.seed}.json',{'status':'COMPLETE','conditions':done,'elapsed':time.perf_counter()-start,'runtime':runtime()})
    print(json.dumps({'conditions':len(done),'elapsed':time.perf_counter()-start,'answers':sum(d['answers']for d in done),'changed':sum(d['changed']for d in done),'numeric_violations':sum(d['numfail']for d in done)}),flush=True)
if __name__=='__main__':main()
