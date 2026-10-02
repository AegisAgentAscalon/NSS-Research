"""Independent chronological/source/math scorer. Never imports generator/worker/controller."""
from __future__ import annotations
import argparse,collections,json,sys
from pathlib import Path
import numpy as np
from io_utils import ROOT,paths,configure,load,dump,lines,canonical,array_digest,check_lock,sha,csv_write,read_arrays
from score_source import restore,route_prefix,expected_entries,packet

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    base,_=paths(False);configure();lock=check_lock()
    from reader_math import decode_code
    from q010v.pointer_math import verify_captured_pointer_arrays,replay_and_audit_pointer_read
    from q010v.pointer_math_frozen import replay_and_audit_pointer_read as frozen,ReaderMathAuditError
    a.output.mkdir(parents=True,exist_ok=False)
    def stop(msg):dump(a.output/'FAILURE.json',{'status':'FAIL_STOP','reason':msg});raise AssertionError(msg)
    cap=load(a.capture/'CAPTURE.json');spec=load(ROOT/'protocol/EVENT_TEMPLATES.json');seeds=load(ROOT/'protocol/SEEDS.json')
    metas=lines(a.input/'protected_sequences.jsonl');original_gold=lines(a.input/'protected_queries.jsonl');gold={};frames={};prefixes={};episodes={};map_checks=0
    for m in metas:
        rebuilt,gg=restore(m,seeds,spec);actual=load(a.input/'public'/f'{m["episode_id"]}.json')
        if canonical(actual)!=canonical(rebuilt):stop('independent source/public stream reconstruction mismatch')
        episodes[m['episode_id']]=actual
        for g,q in zip(gg,rebuilt['queries']):
            gold[g['query_id']]=g;frames[g['query_id']]=q;prefixes[g['query_id']]=rebuilt['events'][:q['event_count']];map_checks+=1
    if canonical(list(gold.values()))!=canonical(original_gold):stop('isolated truth ledger differs from independently derived truth')
    public_order=load(a.input/'PUBLIC_ORDER.json')
    if public_order!=[x['episode_id'] for x in metas]:stop('order drift')
    evt=lines(a.capture/'events.jsonl');events_expected=sum(len(p['events']) for p in episodes.values())
    if len(evt)!=events_expected:stop('event-count incompleteness')
    state_transitions=0
    for er in evt:
        pub=episodes[er['episode_id']];cnt=er['event_count'];event=pub['events'][cnt-1]
        if event['event']!=er['event_id']:stop('event audit identity')
        entries=expected_entries(pub['events'][:cnt])
        w=[[task,packet(v)] for task,v in sorted(entries.items())];i=[[task,v] for task,v in sorted(entries.items())]
        if er['updates']['W']['entry_state']!=w or er['updates']['I']['entry_state']!=i or er['updates']['L']['entry_state']!=i:stop('workspace/index transition disagreement')
        for k in ('W','I','L'):
            work=er['updates'][k]['work'];expected_writes=2 if event['type']=='activate' else 1 if event['type'] in ('select','correct','conflict') else 0
            if work['event_updates']!=1 or work['task_field_semantic_bytes_rewritten']!=26*expected_writes:stop('event work ledger mismatch')
            if work['workspace_ascii_bytes_rewritten']!=(56*expected_writes if k=='W' else 0):stop('packet write budget mismatch')
        state_transitions+=1
    outputs={};audited=0;elements=0
    for desc in cap['outputs']:
        path=a.capture/desc['file']
        if sha(path)!=desc['sha256']:stop('captured output hash mismatch')
        with np.load(path,allow_pickle=False) as z:raw={k:z[k] for k in z.files}
        q=frames[desc['query_id']];data=read_arrays(q['arrays']);full=dict(data,query=raw['query'][0])
        if array_digest(full)!=desc['input_digest']:stop('cache input digest mismatch')
        expected_oid=__import__('hashlib').sha256((desc['model_hash']+':stage0:'+array_digest(full)).encode()).hexdigest()
        if desc['output_id']!=expected_oid:stop('cache key mismatch')
        verify_captured_pointer_arrays(raw['logits'],data['values'][None],data['valid'][None],captured_read_code=raw['read_code'],captured_weights=raw['weights'],captured_pre_norm=raw['weighted_code'])
        d=decode_code(raw['read_code'][0],data['book'],data['active'],data['symbols']);pred=-1 if d.symbol_id=='UNKNOWN' else int(d.symbol_id)
        if pred!=int(raw['resolved_ids'][0]) or not np.array_equal(d.clean_code,raw['clean_code'][0]):stop('independent decoder mismatch')
        if not np.array_equal(np.argmax(raw['logits'],axis=-1),raw['selected_rows']):stop('row selection mismatch')
        outputs[desc['output_id']]={'desc':desc,'raw':raw,'pred':pred};audited+=1;elements+=sum(x.size for x in raw.values())
    if audited!=cap['summary']['completed_forwards'] or len(outputs)!=audited:stop('forward ledger mismatch')
    queries=lines(a.capture/'queries.jsonl');rows=[];ctrl=[];cost=[];altrows=[];rchecks=0;no_cue=0
    for qr in queries:
        qid=qr['query_id'];g=gold[qid];public=frames[qid];prefix=prefixes[qid];data=read_arrays(public['arrays'])
        pr,pred_exact,cur=route_prefix(prefix);lr,pred_latest,_=route_prefix(prefix,latest=True)
        if cur!=public['current'] or qr['event_count']!=len(prefix):stop('causal prefix mismatch')
        if qr['routes']['W']!=pr or qr['routes']['I']!=pr or qr['scan_route']!=pr or qr['latest_route']!=lr:stop('independent management policy disagreement')
        if qr['routes']['O']!={'action':'original','reason':'no_retained_selection','fields':None,'canonical_key':None}:stop('O altered')
        if qr['exact_controls']!={'X_W':pred_exact,'X_I':pred_exact,'X_S':pred_exact,'X_latest':pred_latest}:stop('independent exact-control disagreement')
        if qr['projection_checks']!=2:stop('isolation check missing')
        if len(qr['decision_rows'])!=(3 if cap['kind']=='fixture' else 15):stop('per-query decision count')
        expected_semantics={'canonical':('canonical','validated_pinned_revision'),'abstain_stale':('abstain','stale_revision'),
            'abstain_deleted':('abstain','deleted'),'original_conflict':('original','conflict')}
        if (pr['action'],pr['reason'])!=expected_semantics[g['expected_route']]:stop('template policy does not match independent public policy')
        rchecks+=1
        for dr in qr['decision_rows']:
            k,seed=dr['arm'],dr['seed'];route=qr['routes'][k];known=int(g['expected']!=-1);neural_row=None
            if route['action']=='abstain':
                if dr['output_id'] is not None or dr['model_work_required']!=0:stop('abstention invoked model')
                pred=-1
            else:
                if dr['output_id'] not in outputs:stop('missing neural output')
                out=outputs[dr['output_id']];q_use=data['query'] if route['action']=='original' else np.asarray(route['canonical_key'],np.float32)
                if out['desc']['model_seed']!=seed or out['desc']['input_digest']!=array_digest(dict(data,query=q_use)):stop('wrong model/input cache reuse')
                pred=out['pred'];neural_row=int(out['raw']['selected_rows'][0])
            if pred!=dr['predicted']:stop('logged prediction disagrees')
            accepted=int(route['action']=='canonical');wrong=accepted*int(route['fields'][2]!=g['intended_handle'])
            row=dict(query_id=qid,episode_id=g['episode_id'],family=g['family'],split=g['split'],template=g['template'],checkpoint=g['checkpoint'],sigma=g['sigma'],model_seed=seed,arm=k,
                     known=known,expected=g['expected'],predicted=pred,correct=int(pred==g['expected']),route=route['action'],reason=route['reason'],accepted_reference=accepted,
                     observable_invalid_acceptance=0,hidden_intent_wrong_binding=wrong,management_abstention=int(route['action']=='abstain'),
                     safe_but_lost_recall=int(route['action']=='abstain' and known),correct_unknown=int(not known and pred==-1),covered=int(pred!=-1),
                     intended_revision=g['intended_revision'],bound_revision=route['fields'][3] if accepted else None,
                     neural_selected_row=neural_row,output_id=dr['output_id'],whole_map_integrity=1)
            rows.append(row)
            if g['alternate_expected'] is not None:
                altrows.append(dict(query_id=qid,family=g['family'],split=g['split'],checkpoint=g['checkpoint'],system=k,model_seed=seed,predicted=pred,
                    main_expected=g['expected'],alternate_expected=g['alternate_expected'],main_correct=int(pred==g['expected']),alternate_correct=int(pred==g['alternate_expected']),
                    paired_label_accuracy=(int(pred==g['expected'])+int(pred==g['alternate_expected']))/2,new_forwards=0))
        for name,pp in qr['exact_controls'].items():
            route=lr if name=='X_latest' else pr;accepted=route['action']=='canonical';known=g['expected']!=-1
            ctrl.append(dict(query_id=qid,episode_id=g['episode_id'],family=g['family'],split=g['split'],template=g['template'],checkpoint=g['checkpoint'],sigma=g['sigma'],control=name,
                  policy='current_entity' if name=='X_latest' else 'pinned_revision',expected=g['expected'],predicted=pp,correct=int(pp==g['expected']),known=int(known),
                  accepted_reference=int(accepted),hidden_intent_wrong_binding=int(accepted and route['fields'][2]!=g['intended_handle']),
                  known_refusal=int(known and pp==-1),correct_unknown=int(not known and pp==-1),reason=route['reason']))
            if g['alternate_expected'] is not None:altrows.append(dict(query_id=qid,family=g['family'],split=g['split'],checkpoint=g['checkpoint'],system=name,model_seed='none',predicted=pp,
                    main_expected=g['expected'],alternate_expected=g['alternate_expected'],main_correct=int(pp==g['expected']),alternate_correct=int(pp==g['alternate_expected']),
                    paired_label_accuracy=(int(pp==g['expected'])+int(pp==g['alternate_expected']))/2,new_forwards=0))
        if g['alternate_expected'] is not None:no_cue+=1
        # Compare actual whole-object inventory, not sums of overlapping component inventories.
        for seed,arms in qr['memory_by_seed'].items():
            for arm,inventory in arms.items():
                cost.append(dict(query_id=qid,family=g['family'],split=g['split'],template=g['template'],checkpoint=g['checkpoint'],model_seed=int(seed),arm=arm,
                      **{x:inventory[x] for x in ('whole_unique_python_graph_bytes','state_array_bytes','query_bytes','selection_semantic_field_bytes','selection_ascii_bytes','entries','journal_events')},
                      canonical_state_metadata_bytes=inventory.get('canonical_state_metadata_bytes',None),
                      query_index_reads=qr['query_work'][arm]['index_reads'],query_packet_decodes=qr['query_work'][arm]['packet_decodes'],
                      query_returned_bytes=qr['query_work'][arm]['lookup_returned_bytes'],
                      query_peak_transient_controller_graph_bytes=qr['query_work'][arm]['peak_transient_unique_graph_bytes']))
    if len(queries)!=len(gold) or len(rows)!=(72 if cap['kind']=='fixture' else 2880) or len(ctrl)!=len(gold)*4:stop('incomplete scientific coverage')
    # All per-query rows retained; no failure-conditioned filtering.
    csv_write(a.output/'DECISIONS.csv',rows);csv_write(a.output/'EXACT_CONTROLS.csv',ctrl);csv_write(a.output/'NEGATIVE_OUTCOMES.csv',[r for r in rows if not r['correct']],fields=list(rows[0]))
    csv_write(a.output/'CONTROL_NEGATIVES.csv',[r for r in ctrl if not r['correct']],fields=list(ctrl[0]));csv_write(a.output/'MEMORY_AND_READ_WORK.csv',cost)
    csv_write(a.output/'NO_CUE_ALTERNATE_LABELS.csv',altrows)
    def summarize(items,fields):
        groups=collections.defaultdict(list)
        for r in items:groups[tuple(r[k] for k in fields)].append(r)
        ans=[]
        for key,rs in sorted(groups.items()):
            d=dict(zip(fields,key));d.update(n=len(rs),correct=sum(r['correct'] for r in rs),accuracy=sum(r['correct'] for r in rs)/len(rs),known=sum(r['known'] for r in rs),
               known_correct=sum(r['correct']*r['known'] for r in rs),known_accuracy=sum(r['correct']*r['known'] for r in rs)/sum(r['known'] for r in rs) if sum(r['known'] for r in rs) else None,
               correct_unknown=sum(r['correct_unknown'] for r in rs),hidden_intent_wrong_bindings=sum(r['hidden_intent_wrong_binding'] for r in rs))
            if 'safe_but_lost_recall' in rs[0]:d['safe_but_lost_recall']=sum(r['safe_but_lost_recall'] for r in rs)
            ans.append(d)
        return ans
    for name,fields in [('POOLED',['split','arm']),('CHECKPOINT_GRID',['split','template','checkpoint','arm']),('NOISE_GRID',['split','template','checkpoint','sigma','arm']),
                        ('SEQUENCE_GRID',['split','family','template','model_seed','arm']),('FAMILY_GRID',['split','family','arm'])]:csv_write(a.output/(name+'.csv'),summarize(rows,fields))
    csv_write(a.output/'CONTROL_GRID.csv',summarize(ctrl,['split','template','checkpoint','control']))
    pairs=[]
    for f in sorted({r['family'] for r in rows}):
        aa={k:[r for r in rows if r['family']==f and r['arm']==k] for k in ('W','I','O')}
        ns=len(aa['W']);acc={k:sum(r['correct'] for r in rr)/len(rr) for k,rr in aa.items()}
        pairs.append(dict(family=f,split=aa['W'][0]['split'],unique_query_occasions=ns/(1 if cap['kind']=='fixture' else 5),reader_measurements_per_arm=ns,
                          W=acc['W'],I=acc['I'],O=acc['O'],W_minus_I_pp=100*(acc['W']-acc['I']),W_minus_O_pp=100*(acc['W']-acc['O'])))
    csv_write(a.output/'FAMILY_PAIRED.csv',pairs)
    # Event work is per stream and independent of how many saved readout seeds are measured.
    evwork=[]
    byid={m['episode_id']:m for m in metas}
    for er in evt:
        m=byid[er['episode_id']]
        for arm,x in er['updates'].items():evwork.append(dict(episode_id=m['episode_id'],family=m['family'],split=m['split'],template=m['template'],event_count=er['event_count'],arm=arm,controller_unique_graph_bytes=x['controller_unique_graph_bytes'],**x['work']))
    csv_write(a.output/'EVENT_WORK.csv',evwork)
    cm=[]
    for fam in sorted({g['family'] for g in gold.values()}):
        for arm in ('W','I'):
            cs=[r for r in cost if r['family']==fam and r['arm']==arm and r['model_seed']==1201]
            es=[r for r in evwork if r['family']==fam and r['arm']==arm]
            cm.append(dict(family=fam,split=cs[0]['split'],arm=arm,query_occasions=len(cs),events=len(es),
                  sum_resident_graph_observations_bytes=sum(x['whole_unique_python_graph_bytes'] for x in cs),peak_resident_graph_bytes=max(x['whole_unique_python_graph_bytes'] for x in cs),
                  sum_canonical_metadata_bytes=sum(x['canonical_state_metadata_bytes'] for x in cs),
                  task_semantic_bytes_rewritten=sum(x['task_field_semantic_bytes_rewritten'] for x in es),packet_ascii_bytes_rewritten=sum(x['workspace_ascii_bytes_rewritten'] for x in es),
                  selection_object_bytes_reallocated=sum(x['selection_object_bytes_reallocated'] for x in es),
                  packet_encodes=sum(x['packet_encodes'] for x in es),packet_decodes=sum(x['packet_decodes'] for x in es)+sum(x['query_packet_decodes'] for x in cs),
                  index_reads=sum(x['index_reads'] for x in es)+sum(x['query_index_reads'] for x in cs),
                  lookup_returned_bytes=sum(x['lookup_returned_bytes'] for x in es)+sum(x['query_returned_bytes'] for x in cs),
                  event_record_bytes_rewritten=sum(x['record_rewritten_bytes'] for x in es),event_binding_bytes_rewritten=sum(x['binding_rewritten_bytes'] for x in es)))
    csv_write(a.output/'COST_FAMILY_GRID.csv',cm)
    underflow=None
    if cap['kind']=='fixture':
        with np.load(base/'audit/FRESH_MAIN_UNDERFLOW_REJECTION.npz',allow_pickle=False) as z:uf={k:z[k] for k in z.files}
        kw={k:uf[k] for k in ('captured_read_code','captured_weights','captured_pre_norm')}
        try:frozen(uf['logits'],uf['values'],uf['valid'],**kw)
        except ReaderMathAuditError as e:message=str(e)
        else:stop('historical fresh-reproduction underflow rejection disappeared')
        replay_and_audit_pointer_read(uf['logits'],uf['values'],uf['valid'],**kw)
        underflow={'preserved':True,'frozen_rejection':message,'amendment':2**-126,'fixture_sha256':sha(base/'audit/FRESH_MAIN_UNDERFLOW_REJECTION.npz'),
           'scope':'v1.6 retained regenerated rejection; original historical rejected row and original v2 source still unavailable'}
    prohibited=[m for m in sys.modules if m in ('controller','generate','worker','capture') or m.startswith(('q010r','q010c'))]
    if prohibited:stop('independent scorer imported producer modules: '+str(prohibited))
    receipt=dict(status='PASS_INTERNAL_INDEPENDENT_SCORING',kind=cap['kind'],source_lock_sha256=lock,independently_reconstructed_sequences=len(metas),
      independently_reconstructed_query_occasions=len(gold),whole_map_checks=map_checks,independent_event_transition_checks=state_transitions,
      W_I_and_scan_route_checks=rchecks,observable_invalid_acceptances=0,protected_projection_checks=sum(q['projection_checks'] for q in queries),
      audited_distinct_forwards=audited,captured_output_numeric_elements=elements,learned_interface_decisions=len(rows),non_neural_control_decisions=len(ctrl),
      incorrect_learned_outcomes=sum(not r['correct'] for r in rows),incorrect_control_outcomes=sum(not r['correct'] for r in ctrl),
      no_cue_query_occasions=no_cue,alternate_label_decisions=len(altrows),underflow_amendment=underflow,prohibited_imports=prohibited,
      statistical_scope='families/chronological sequences; saved model seeds repeat readouts; exploratory descriptive results',training_updates=0)
    dump(a.output/'SCORE_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2),flush=True)
if __name__=='__main__':main()
