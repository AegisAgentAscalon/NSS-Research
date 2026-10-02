from support import *
import collections,statistics

def main():
    root=ROOT;rows=[json.loads(p.read_text())for p in sorted((root/'results/episodes').glob('*.json'))]
    audit=json.loads((root/'results/audit.json').read_text());pre=json.loads((root/'results/preflight.json').read_text())
    groups=[]
    for n in [8,32,128]:
        for pol in ['index','cache','segment']:
            ds=[d for d in rows if d['n']==n and d['policy']==pol]
            groups.append({'n':n,'policy':pol,'conditions':len(ds),'answers':sum(d['answers']for d in ds),'correct':sum(d['correct']for d in ds),
                           'false_complete':sum(d['false_complete']for d in ds),'reader_calls':sum(d['stats'].get('reader_calls',0)for d in ds),
                           'reader_rows':sum(d['stats'].get('reader_input_rows',0)for d in ds),'archive_rows':sum(d['stats'].get('archive_rows_read',0)for d in ds),
                           'memo_hits':sum(d['stats'].get('result_hits',0)for d in ds),'peak_active_rows':max(d['stats'].get('peak_active_rows',0)for d in ds)})
    model_quality=[]
    for n in [8,32,128]:
        for ms in [8801,8802,8804]:
            obs=[o for d in rows if d['n']==n and d['model_seed']==ms and d['policy']=='index'for o in d['observations']if o['status']=='ANSWER']
            cm=np.zeros((4,4),int)
            for o in obs:cm[o['target'],o['pred']]+=1
            model_quality.append({'n':n,'model_seed':ms,'answers':len(obs),'correct':int(cm.trace()),'class_counts':cm.sum(1).tolist(),'confusion':cm.tolist()})
    benchmarks=[]
    for n in[8,32,128]:benchmarks+=json.loads((root/f'results/benchmark_n{n}.json').read_text())['rows']
    contrasts=[]
    for n in[8,32,128]:
        for fam in['reuse','sweep','churn','resume']:
            d={x['policy']:x for x in benchmarks if x['n']==n and x['family']==fam}
            contrasts.append({'n':n,'family':fam,'index_ms':d['index']['median_ms'],'cache_ms':d['cache']['median_ms'],'segment_ms':d['segment']['median_ms'],
                              'segment_vs_cache_saving_percent':100*(1-d['segment']['median_ms']/d['cache']['median_ms'])})
    closure_rows=[]
    for n in[8,32,128]:
        ds=[a for a in audit['topology_audit']if a['n']==n and a['episode'].endswith('_reuse')]
        closure_rows.append({'n':n,'full_positions':ds[0]['positions'],'min_single':min(a['min_single_rows']for a in ds),
                             'max_single':max(a['max_single_rows']for a in ds),'all_task_query_metadata_required':all(a['all_global_task_queries_in_every_single_task_closure']for a in ds)})
    unique_receipt_violations=0;completed_occasions=0;deferred_occasions=0;partial_occasions=0
    for d in rows:
        keys=[(t['job'],t['task'],t['signature'])for t in d['trace']if'signature'in t]
        unique_receipt_violations+=len(keys)-len(set(keys))
        ep=json.loads((root/'fixtures'/f"{d['episode']}.json").read_text())
        for ei,e in enumerate(ep['events']):
            if e['op']!='job':continue
            obs=[o for o in d['observations']if o['event']==ei]
            ans=sum(o['status']=='ANSWER'for o in obs)
            if e.get('limit_tasks')is not None:partial_occasions+=1
            elif ans==len(e['tasks']):completed_occasions+=1
            else:deferred_occasions+=1
    out={'status':'COMPLETE_BOUNDED_COMPONENT','conditions':len(rows),'episodes':36,'models':[8801,8802,8804],
         'answers':sum(d['answers']for d in rows),'numeric_scalars':sum(d['numeric_scalars']for d in rows),
         'numeric_violations':sum(d['numeric_violations']for d in rows),'changed_classes':sum(d['changed_classes']for d in rows),
         'max_abs':max(d['max_abs']for d in rows),'max_normalized':max(d['max_normalized']for d in rows),
         'budget_deferrals':sum(d['stats'].get('budget_deferrals',0)for d in rows),'completed_request_occasions':completed_occasions,
         'deferred_request_occasions':deferred_occasions,'partial_request_occasions':partial_occasions,'duplicate_receipts':unique_receipt_violations,
         'main_sliced_reader_calls':sum(d['stats'].get('reader_calls',0)for d in rows),'main_reference_reader_calls':sum(d['reference_forward_calls']for d in rows),
         'main_core_seconds':sum(d['core_seconds']for d in rows),'peak_main_process_rss_bytes':max(d['runtime']['peak_rss_bytes']for d in rows),
         'optimizer_applications':0,'new_fits':0,'groups':groups,'model_quality':model_quality,'timing_contrasts':contrasts,'closure':closure_rows,
         'audit_status':audit['status'],'preflight_checks':len(pre['checks']),'post_lock_driver_names':['complete_timing.py','complete_timing_128.py','audit.py','summarize.py'],
         'caveats':['Repeated model/policy/job observations are not independent trials.','The full archive is RAM-backed and outside the active input-row cap.','Timing is prototype CPU/in-memory and not a system-wide energy/storage benchmark.','Two timing runner interruptions preserved completed families and separately completed only missing resume families.']}
    save(root/'results/SUMMARY.json',out);print(json.dumps({k:v for k,v in out.items()if k not in['groups','model_quality','timing_contrasts']},indent=2))
if __name__=='__main__':main()
