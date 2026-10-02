"""Post-result retained-data recount and repeatability audit, no new fixtures."""
from support import *
from run import execute
from sc01 import Store,Workspace,closure
from nss_hsa.hierarchy import Hierarchy
import copy,traceback

def main():
    setup();start=time.perf_counter();rows=[];recounts=[];policy_pairs=[];models={}
    for seed in [8801,8802,8804]:models[seed]=load(seed)
    for p in sorted((ROOT/'results/episodes').glob('*.json')):
        d=json.loads(p.read_text());rows.append(d)
        ep=json.loads((ROOT/'fixtures'/f"{d['episode']}.json").read_text());w=copy.deepcopy(ep['world'])
        byevent={}
        for obs in d['observations']:byevent.setdefault(obs['event'],[]).append(obs)
        nans=correct=fc=changes=violations=scalars=badtargets=wrongargs=0
        for ei,event in enumerate(ep['events']):
            if event['op']=='change':
                c=event['change'];f=c['field']
                if f=='freeze':w['freeze']=1-w['freeze']
                elif f=='dependency':w['deps'][c['task']]=c['value']
                else:w[f][c['task']]=1-w[f][c['task']]
            for o in byevent.get(ei,[]):
                if o['status']!='ANSWER':continue
                t=o['task'];truth=3
                if w['progress'][t]!=0:truth=1
                elif sum(w['progress'][j] for j in w['deps'][t])==len(w['deps'][t]):truth=2
                if w['freeze']:truth=0
                a=np.array(o['logits'],np.float32);b=np.array(o['full_logits'],np.float32)
                pred=int(a.argmax());fullpred=int(b.argmax());badtargets+=int(o['target']!=truth);wrongargs+=int(pred!=o['pred']or fullpred!=o['full_pred'])
                nans+=1;correct+=int(pred==truth);fc+=int(pred==1 and truth!=1);changes+=int(pred!=fullpred)
                err=np.abs(a-b);violations+=int(((err>2e-5+2e-5*np.abs(b))|~np.isfinite(a)|~np.isfinite(b)).sum());scalars+=4
        valid=all([nans==d['answers'],correct==d['correct'],fc==d['false_complete'],changes==d['changed_classes'],violations==d['numeric_violations'],scalars==d['numeric_scalars'],badtargets==0,wrongargs==0,d['model_hash']==d['final_model_hash']==models[d['model_seed']][1],d['stats'].get('peak_active_rows',0)<=d['record_cap']])
        recounts.append({'file':p.name,'pass':valid,'answers':nans,'label_discrepancies':badtargets,'argmax_discrepancies':wrongargs})
    for d in rows:
        if d['policy']=='index':continue
        r=next(x for x in rows if x['episode']==d['episode']and x['model_seed']==d['model_seed']and x['policy']=='index')
        fields=lambda x:[(a['event'],a['job'],a['task'],a['status'],a.get('pred'))for a in x['observations']]
        policy_pairs.append({'episode':d['episode'],'model':d['model_seed'],'policy':d['policy'],'exact_status_label_parity':fields(d)==fields(r)})
    repeats=[]
    for d in rows:
        if d['fixture_seed']!=932101 or d['family']not in['resume','sweep']:continue
        ep=json.loads((ROOT/'fixtures'/f"{d['episode']}.json").read_text());m,mid=models[d['model_seed']]
        z=execute(ep,m,mid,d['policy']);identical=z['observations']==d['observations']and z['trace']==d['trace']
        repeats.append({'episode':d['episode'],'model':d['model_seed'],'policy':d['policy'],'bit_exact_records':identical})
        save(ROOT/'results/audit_progress.json',{'recounts':recounts,'policy_pairs':policy_pairs,'replays':repeats})
    restores=[]
    for p in sorted((ROOT/'results/snapshots').glob('*.json')):
        if p.name.endswith('.store.json'):continue
        raw=p.read_bytes();payload=json.loads(raw)['payload'];store=Store.from_dict(json.loads(p.with_suffix('.store.json').read_text()))
        m,mid=models[8801];ws=Workspace.restore(raw,store,mid)
        parts=p.stem.split('_');ei=int(parts[-1]);epid='_'.join(parts[:3]);policy=parts[3]
        ep=json.loads((ROOT/'fixtures'/f'{epid}.json').read_text())
        for event in ep['events'][ei+1:]:
            if event['op']=='change':store.mutate(event['change'])
            elif event['op']=='checkpoint':
                rb=ws.snapshot();store=Store.from_dict(json.loads(canonical(store.to_dict())));ws=Workspace.restore(rb,store,mid)
            else:ws.job(event['id'],event['tasks'],m,limit_tasks=event.get('limit_tasks'))
        expected=next(d for d in rows if d['episode']==epid and d['model_seed']==8801 and d['policy']==policy)
        restores.append({'snapshot':p.name,'bit_exact_final_trace':ws.trace==expected['trace']})
    topology=[]
    for p in sorted((ROOT/'fixtures').glob('*.json')):
        ep=json.loads(p.read_text());spec=Hierarchy.from_dependencies(ep['world']['deps']);qs=set(4*i for i in range(spec.tasks))
        sizes=[];coverage=[]
        for t in range(spec.tasks):
            ids=closure(spec,[t])[0];sizes.append(len(ids));coverage.append(qs.issubset(ids))
        topology.append({'episode':ep['id'],'n':spec.tasks,'positions':spec.positions,'all_global_task_queries_in_every_single_task_closure':all(coverage),
                         'min_single_rows':min(sizes),'max_single_rows':max(sizes),'mean_single_rows':float(np.mean(sizes)),'record_cap':ep['record_cap']})
    good=all(a['pass']for a in recounts)and all(a['exact_status_label_parity']for a in policy_pairs)and all(a['bit_exact_records']for a in repeats)and all(a['bit_exact_final_trace']for a in restores)
    out={'status':'PASS'if good else'FAIL','recounts':recounts,'policy_pairs':policy_pairs,'replays':repeats,'restores':restores,'topology_audit':topology,
         'runtime':runtime(),'seconds':time.perf_counter()-start,'optimizer_applications':0,'new_main_conditions':0}
    save(ROOT/'results/audit.json',out)
    print(json.dumps({'status':out['status'],'recounts':len(recounts),'policy_pairs':len(policy_pairs),'fresh_process_replays':len(repeats),'snapshot_restores':len(restores),'seconds':out['seconds']},indent=2))
if __name__=='__main__':main()
