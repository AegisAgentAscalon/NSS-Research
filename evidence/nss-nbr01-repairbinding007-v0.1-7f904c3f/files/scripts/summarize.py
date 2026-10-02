from pathlib import Path
import json,collections,statistics
ROOT=Path(__file__).resolve().parents[1]

def summarize():
    pairs=[json.loads(p.read_text()) for p in sorted((ROOT/'results').glob('pair_*.json'))]
    assert len(pairs)==5
    groups=collections.defaultdict(list)
    for pair in pairs:
        for row in pair['rows']:groups[(row['case'],row['method'],row['reader'],row['depth'])].append(row)
    ag=[]
    fields=('accuracy','known_accuracy','unknown_accuracy','unsupported_room_rate','unresolved_rate','key_identity_accuracy','value_identity_accuracy','key_cosine','value_cosine')
    for key,rs in sorted(groups.items()):
        d=dict(zip(('case','method','reader','depth'),key));d['seeds']=[r['seed'] for r in rs]
        for f in fields:
            vs=[r[f] for r in rs if r.get(f) is not None]
            if vs:d[f]={'mean':statistics.mean(vs),'sd':statistics.stdev(vs) if len(vs)>1 else 0,'min':min(vs),'max':max(vs),'values':vs}
        ag.append(d)
    gates=[]
    nominal=['isolation/clean4','isolation/keys02_t64','isolation/values02_t64','isolation/both02_t64','isolation/both02_t1024_h8']+[f'stream/{x}' for x in ('initial','correction','clear','rewrite','reset','new_scope')]
    for pair in pairs:
        for method in ('none','normalize','intrinsic_mlp','learned_dictionary','nearest'):
            for reader in ('record_hop','gated_hop'):
                selected=[r for r in pair['rows'] if r['case'] in nominal and r['method']==method and r['reader']==reader and r['depth']==(8 if 'h8' in r['case'] else 4)]
                assert len(selected)==len(nominal)
                failed=[{'case':r['case'],'metric':f,'value':r[f]} for r in selected for f in ('known_accuracy','unknown_accuracy') if r[f] is not None and r[f]<.95]
                gates.append({'seed':pair['seed'],'reader':reader,'method':method,'pass':not failed,'failed':failed})
    fits=[json.loads(p.read_text()) for p in (ROOT/'checkpoints').glob('*.json')]
    for i in range(901,906):
        a,b=[json.loads((ROOT/'checkpoints'/f'{k}_{i}.json').read_text()) for k in ('intrinsic_mlp','learned_dictionary')]
        assert a['batch_fingerprints']==b['batch_fingerprints']
    result={'status':'RUN_NBR01_OPEN','aggregates':ag,'gates':gates,'main_pairs':5,'new_fits':len(fits),'optimizer_steps':sum(f['steps'] for f in fits),'sequence_presentations':sum(f['sequence_presentations'] for f in fits),'supervised_updates':sum(f['sequence_presentations']*4 for f in fits),'summed_training_loop_seconds':sum(f['seconds'] for f in fits),'summed_eval_loop_seconds':sum(p['seconds'] for p in pairs),'result_rows':sum(len(p['rows']) for p in pairs),'answer_evaluations':sum(p['answer_evaluations'] for p in pairs),'state_configurations':sum(p['state_count'] for p in pairs),'new_parameters':{f['kind']:f['parameters'] for f in fits}}
    (ROOT/'SUMMARY.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('aggregates','gates')},indent=2))
    for method in ('none','normalize','intrinsic_mlp','learned_dictionary','nearest'):
        print(method,{reader:sum(g['pass'] for g in gates if g['method']==method and g['reader']==reader) for reader in ('record_hop','gated_hop')})
if __name__=='__main__':summarize()
