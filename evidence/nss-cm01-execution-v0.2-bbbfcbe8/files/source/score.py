"""Independent CM01 scorer: no producer, model, generator, or manager imports."""
from __future__ import annotations
import argparse,csv,json,re,sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from common import ROOT,paths,configure,check_lock,load,dump,read_lines,arrays,sha,canonical

STRATA={1:'bound_known',2:'bound_close',3:'unbound_known',4:'unbound_absent',5:'stale_revision',6:'cross_scope',7:'wrong_reference',8:'correction_conflict'}

def reconstruct(case):
    """Separately implemented path-1 source, perturbation, and live-truth replay."""
    rec=case['generation'];seed=rec['seeds'];g=np.random.Generator(np.random.PCG64(seed['graph']))
    path=g.permutation(16)[:2];source=int(path[0]);target=int(path[1]);outside=[i for i in range(16) if i not in path]
    decoy=outside[-1];dest=outside[0]
    edges={i:i for i in outside};edges[decoy]=dest;edges[source]=target;edges[target]=target
    if edges!=dict(case['initial_truth_edges']):raise AssertionError('independent initial truth mismatch')
    z=g.standard_normal((16,16));book=np.zeros((16,17),np.float32);book[:,:16]=(z/np.linalg.norm(z,axis=1,keepdims=True)).astype(np.float32)
    owners=g.permutation(16)
    if owners.tolist()!=case['physical_owners']:raise AssertionError('independent physical layout mismatch')
    if rec['close_decoy']:
        n=np.random.Generator(np.random.PCG64(seed['close'])).normal(0.,.01,16)
        x=book[source,:16].astype(np.float64)+n;book[decoy,:16]=(x/np.linalg.norm(x)).astype(np.float32)
    qn=np.random.Generator(np.random.PCG64(seed['query'])).normal(0.,case['sigma'],16)
    q16=book[source,:16].astype(np.float64)+qn;q=np.zeros(17,np.float32);q[:16]=(q16/np.linalg.norm(q16)).astype(np.float32)
    for e in case['truth_mutations']:
        if e['type']=='delete':edges.pop(e['source'])
        elif e['type']=='update':edges[e['source']]=e['destination']
        else:raise AssertionError('undeclared gold event')
    keys=np.zeros((16,17),np.float32);values=keys.copy();valid=np.zeros(16,bool)
    for row,owner in enumerate(owners):
        if int(owner) in edges:valid[row]=True;keys[row]=book[owner];values[row]=book[edges[int(owner)]]
    return {'keys':keys,'values':values,'valid':valid,'query':q,'book':book,'active':np.ones(16,bool),'symbols':np.arange(16,dtype=np.int64)},edges,source,decoy

def independent_route(public):
    """Independent grammar and journal replay; no call to producer management code."""
    text=public['serialized'];parts=text.split('|')
    if len(parts)!=6 or parts[0]!='01' or parts[-1] not in ('R','U','H'):raise AssertionError('codec')
    if [len(x) for x in parts[1:5]]!=[8,16,8,16] or any(re.fullmatch('[0-9a-f]+',x) is None for x in parts[1:5]):raise AssertionError('codec widths')
    nums=[int(x,16) for x in parts[1:5]];w=dict(zip(('scope','handle','revision','binding_event'),nums));w['operation']=parts[-1]
    if w!=public['workspace'] or len(text.encode())!=56:raise AssertionError('serialized fields differ')
    if w['operation']=='R' and not all(nums):raise AssertionError('R zeros')
    if w['operation']=='U' and any(nums):raise AssertionError('U nonzero')
    records={};bindings={}
    for e in public['journal']:
        kind=e['type']
        if kind in ('register','revise'):records[(e['scope'],e['handle'])]=dict(e,active=True)
        elif kind=='delete':records[(e['scope'],e['handle'])].update(active=False,revision=e['revision'],event=e['event'])
        elif kind in ('select','correct'):bindings[e['event']]=dict(e,conflict=False)
        elif kind=='conflict':
            for x in bindings.values():
                if x['task']==e['task']:x['conflict']=True
        else:raise AssertionError('public event kind')
    current=public['current'];record=None;nlookup=0
    if w['operation']!='R':action,reason='original','conflict' if w['operation']=='H' else 'unresolved'
    elif w['scope']!=current['scope']:action,reason='abstain','cross_scope'
    else:
        binding=bindings.get(w['binding_event']);nlookup=1
        if binding is None:action,reason='original','missing_binding'
        elif binding['conflict']:action,reason='original','conflict'
        elif (binding['task'],binding['scope'],binding['handle'],binding['revision'])!=(current['task'],w['scope'],w['handle'],w['revision']):action,reason='abstain','binding_mismatch'
        else:
            record=records.get((w['scope'],w['handle']));nlookup=2
            if record is None:action,reason='original','missing_record'
            elif not record['active']:action,reason='abstain','deleted'
            elif record['revision']!=w['revision']:action,reason='abstain','stale_revision'
            else:action,reason='canonical','validated_public_binding'
    return dict(action=action,reason=reason,lookup_count=nlookup,record=record if action=='canonical' else None,workspace=w,records=records,bindings=bindings)

def save_csv(p,rows):
    if not rows:raise ValueError('refuse empty results')
    with Path(p).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r,s=paths(False);configure();lock=check_lock()
    from reader_math import decode_code
    from q010v.pointer_math import verify_captured_pointer_arrays,replay_and_audit_pointer_read
    from q010v.pointer_math_frozen import replay_and_audit_pointer_read as frozen,ReaderMathAuditError
    data=arrays(a.input/'inputs.npz');pub=read_lines(a.input/'public.jsonl');gold=read_lines(a.input/'protected.jsonl');routes=read_lines(a.capture/'routing.jsonl')
    public_control=read_lines(a.capture/'public_control.jsonl');cap=load(a.capture/'CAPTURE.json');n=len(pub)
    true=[];management=[];metadata=[]
    for i,g in enumerate(gold):
        reconstructed,edges,source,decoy=reconstruct(g)
        for k,x in reconstructed.items():
            if x.dtype!=data[k][i].dtype or x.shape!=data[k][i].shape or x.tobytes()!=data[k][i].tobytes():raise AssertionError(f'independent source array differs: {i}/{k}')
        # Check journal payloads against source truth at their actual event time.
        before=dict(g['initial_truth_edges']);slot_by_code={data['book'][i,j].tobytes():j for j in range(16)}
        handles={}
        for e in pub[i]['journal']:
            if e['type']=='register':
                slot=slot_by_code[np.asarray(e['key'],np.float32).tobytes()]
                if e['payload_symbol']!=before[slot] or not np.array_equal(e['payload_code'],data['book'][i,before[slot]]):raise AssertionError('journal registration fabrication')
                handles[(e['scope'],e['handle'])]=slot
            elif e['type']=='revise':
                mutation=next(x for x in g['truth_mutations'] if x['event']==e['event'])
                if e['payload_symbol']!=mutation['destination']:raise AssertionError('revision payload differs from event truth')
            elif e['type']=='delete':
                if not any(x['event']==e['event'] and x['type']=='delete' for x in g['truth_mutations']):raise AssertionError('unbound deletion')
        expected=edges.get(g['query_source'],-1)
        true.append(expected);metadata.append((edges,source,decoy))
        rt=independent_route(pub[i]);management.append(rt)
        for name in ('structured','serialized'):
            c=routes[i][name]
            for field in ('action','reason','lookup_count'):
                if c[field]!=rt[field]:raise AssertionError('independent route mismatch')
            if c['action']=='canonical':
                if c['canonical_key']!=rt['record']['key'] or c['record_event']!=rt['record']['event']:raise AssertionError('canonical query provenance mismatch')
            elif c['canonical_key'] is not None:raise AssertionError('undeclared query replacement')
        if rt['action']!=g['expected_management_action']:raise AssertionError('frozen management expectation mismatch')
        expected_lookup=rt['record']['payload_symbol'] if rt['record'] else -1
        if expected_lookup!=public_control[i]['predicted']:raise AssertionError('public exact control mismatch')
    traces={};audited=0;array_elements=0
    for chunk in cap['chunks']:
        path=a.capture/chunk['file']
        if sha(path)!=chunk['sha256']:raise AssertionError('capture file drift')
        raw=arrays(path);inds=raw['indices'];seed=chunk['seed'];role=chunk['role'];variant=chunk['variant']
        verify_captured_pointer_arrays(raw['logits'],data['values'][inds],data['valid'][inds],captured_read_code=raw['read_code'],captured_weights=raw['weights'],captured_pre_norm=raw['weighted_code'])
        audited+=len(inds);array_elements+=sum(x.size for x in raw.values())
        if not np.array_equal(raw['selected_rows'],np.argmax(raw['logits'],axis=-1)):raise AssertionError('selected row mismatch')
        for local,idx in enumerate(inds):
            i=int(idx);expected_q=data['query'][i] if variant=='original' else np.array(management[i]['record']['key'],np.float32)
            if not np.array_equal(raw['query'][local],expected_q):raise AssertionError('query variant drift')
            dd=decode_code(raw['read_code'][local],data['book'][i],data['active'][i],data['symbols'][i]);pred=-1 if dd.symbol_id=='UNKNOWN' else int(dd.symbol_id)
            if pred!=int(raw['resolved_ids'][local]) or not np.array_equal(dd.clean_code,raw['clean_code'][local]):raise AssertionError('independent output decoder mismatch')
            tracekey=(seed,role,variant,i)
            if tracekey in traces:raise AssertionError('duplicate neural observation')
            traces[tracekey]={'predicted':pred,'selected_row':int(raw['selected_rows'][local])}
    if audited!=cap['logical_forward_calls']:raise AssertionError('forward ledger')
    model_grid=sorted({(c['seed'],c['role']) for c in cap['chunks']});rows=[]
    for seed,role in model_grid:
        for i,g in enumerate(gold):
            for arm in ('A','B','C'):
                action='original' if arm=='A' else management[i]['action']
                if action=='abstain':pred=-1;selected=None
                else:
                    trace=traces[(seed,role,'canonical' if action=='canonical' else 'original',i)];pred=trace['predicted'];selected=trace['selected_row']
                is_known=true[i]!=-1;bound_handle=management[i]['workspace']['handle'] if action=='canonical' else None
                false_binding=(bound_handle is not None and bound_handle!=g['intended_handle'])
                row=dict(case_id=g['case_id'],family=g['family'],split=g['split'],model_seed=seed,role=role,arm=arm,stratum=STRATA[g['stratum']],subtype=g['subtype'],sigma=g['sigma'],
                         expected=true[i],predicted=pred,correct=int(pred==true[i]),known=int(is_known),covered=int(pred!=-1),management_action=action,
                         management_abstention=int(action=='abstain'),returned_unknown=int(pred==-1),false_binding=int(false_binding),
                         observable_invalid=int(g['observable_invalid']),invalid_reference_accepted=int(g['observable_invalid'] and action=='canonical'),
                         invalid_query_nonabstention=int(g['observable_invalid'] and action!='abstain'),information_limit=int(g['information_limit']),
                         selected_row='' if selected is None else selected,accepted_handle='' if bound_handle is None else bound_handle)
                rows.append(row)
    controls=[]
    for i,g in enumerate(gold):
        rows_owner=np.flatnonzero(np.array(g['physical_owners'])==g['query_source']) if g['query_source']>=0 else []
        oracle=-1
        if len(rows_owner) and data['valid'][i,rows_owner[0]]:
            dd=decode_code(data['values'][i,rows_owner[0]],data['book'][i],data['active'][i],data['symbols'][i]);oracle=-1 if dd.symbol_id=='UNKNOWN' else int(dd.symbol_id)
        for name,pred in [('public_exact_lookup',public_control[i]['predicted']),('privileged_exact_owner',oracle)]:
            controls.append(dict(case_id=g['case_id'],family=g['family'],split=g['split'],stratum=STRATA[g['stratum']],subtype=g['subtype'],sigma=g['sigma'],control=name,expected=true[i],predicted=pred,correct=int(pred==true[i]),known=int(true[i]!=-1)))
    pair_checks=[]
    for i,g in enumerate(gold):
        if g['stratum']!=3:continue
        j=next(j for j,h in enumerate(gold) if (h['family'],h['within_stratum'],h['stratum'])==(g['family'],g['within_stratum'],4))
        assert canonical(pub[i])==canonical(pub[j]) and all(np.array_equal(v[i],v[j]) for v in data.values())
        for seed,role in model_grid:
            for variant in ('original',):
                if traces[(seed,role,variant,i)]!=traces[(seed,role,variant,j)]:raise AssertionError('identical input divergent output')
        pair_checks.append({'known':g['case_id'],'absent':gold[j]['case_id'],'known_expected':true[i],'absent_expected':true[j],'identical_inputs':True})
    no_cue=[]
    for i,g in enumerate(gold):
        if g['subtype']!='no_cue':continue
        alt=metadata[i][0][g['decoy_source']]
        no_cue.append({'case_id':g['case_id'],'expected_intended':true[i],'counterfactual_expected_if_observed_binding_were_intended':alt,
                       'public_exact_predicted':public_control[i]['predicted'],'identical_public_input_by_construction':True,'new_neural_calls':0})
    def summaries(fields):
        groups=defaultdict(list)
        for x in rows:groups[tuple(x[k] for k in fields)].append(x)
        result=[]
        for key,rs in sorted(groups.items()):
            d=dict(zip(fields,key));d.update(records=len(rs),correct=sum(x['correct'] for x in rs),accuracy=sum(x['correct'] for x in rs)/len(rs),
                  known=sum(x['known'] for x in rs),known_correct=sum(x['correct']*x['known'] for x in rs),
                  unknown_cases=sum(not x['known'] for x in rs),unknown_correct=sum(x['correct']*(not x['known']) for x in rs),
                  management_abstentions=sum(x['management_abstention'] for x in rs),covered=sum(x['covered'] for x in rs),
                  false_bindings=sum(x['false_binding'] for x in rs),invalid_reference_accepted=sum(x['invalid_reference_accepted'] for x in rs));result.append(d)
        return result
    a.output.mkdir(parents=True,exist_ok=False)
    save_csv(a.output/'DECISIONS.csv',rows);save_csv(a.output/'CONTROLS.csv',controls)
    save_csv(a.output/'NEGATIVE_OUTCOMES.csv',[x for x in rows if not x['correct']])
    grid=summaries(['split','family','model_seed','role','arm','stratum','subtype','sigma']);save_csv(a.output/'FULL_GRID.csv',grid)
    save_csv(a.output/'POOLED.csv',summaries(['split','role','arm','stratum','subtype']))
    paired=[]
    families=sorted({g['family'] for g in gold if g['split']=='heldout'})
    for family in families:
        for role in ('near','ordinary','attention'):
            def accuracy(arm,stratum):
                z=[x for x in rows if x['family']==family and x['role']==role and x['arm']==arm and x['stratum']==stratum];return sum(x['correct'] for x in z)/len(z)
            ca,cb=accuracy('A','bound_close'),accuracy('B','bound_close');ka,kb=accuracy('A','bound_known'),accuracy('B','bound_known')
            inv=[x for x in rows if x['family']==family and x['role']==role and x['arm']=='B' and x['observable_invalid']]
            invalid_rate=sum(x['invalid_reference_accepted'] for x in inv)/len(inv)
            paired.append(dict(family=family,role=role,bound_close_A=ca,bound_close_B=cb,gain_pp=100*(cb-ca),bound_known_A=ka,bound_known_B=kb,known_loss_pp=100*(ka-kb),invalid_false_acceptance=invalid_rate,
                               meets_gain_and_control=bool(cb-ca>=.1-1e-12 and ka-kb<=.01+1e-12),invalid_rule_pass=invalid_rate<=.05))
    if paired:save_csv(a.output/'HELDOUT_PAIRED.csv',paired)
    source_modules=[x for x in sys.modules if x.startswith(('q010r','q010c')) or x in ('manager','generate','capture')]
    if source_modules:raise AssertionError('scorer imported producer modules: '+str(source_modules))
    underflow=None
    if cap['kind']=='fixture':
        uf=arrays(r/'audit/FRESH_MAIN_UNDERFLOW_REJECTION.npz')
        kw={k:uf[k] for k in ('captured_read_code','captured_weights','captured_pre_norm')}
        try:frozen(uf['logits'],uf['values'],uf['valid'],**kw)
        except ReaderMathAuditError as e:old=str(e)
        else:raise AssertionError('retained frozen underflow rejection disappeared')
        replay_and_audit_pointer_read(uf['logits'],uf['values'],uf['valid'],**kw)
        underflow={'status':'PASS_FROZEN_REJECTION_AND_EXISTING_AMENDMENT','fixture_source':'v1.6 retained fresh-main rejection, not the lost historical raw row','sha256':sha(r/'audit/FRESH_MAIN_UNDERFLOW_REJECTION.npz'),'frozen_message':old,'amendment_absolute_probability_allowance':2**-126}
    b=[x for x in rows if x['arm']=='B'];c=[x for x in rows if x['arm']=='C']
    if [{k:v for k,v in x.items() if k!='arm'} for x in b]!=[{k:v for k,v in x.items() if k!='arm'} for x in c]:raise AssertionError('scored B/C disagreement')
    near=[x for x in paired if x['role']=='near'];signal=sum(x['meets_gain_and_control'] for x in near)>=4 if near else None
    bound_agreement={}
    for role in ('ordinary','near','attention'):
        rs=[x for x in b if x['role']==role and x['split']=='heldout' and x['stratum'] in ('bound_known','bound_close')]
        lookup={x['case_id']:x['predicted'] for x in controls if x['control']=='public_exact_lookup'}
        bound_agreement[role]={'comparisons':len(rs),'identical_predictions':sum(x['predicted']==lookup[x['case_id']] for x in rs)}
    receipt={'status':'PASS_INDEPENDENT_SCORING','kind':cap['kind'],'records':n,'decision_rows':len(rows),'control_rows':len(controls),'incorrect_decision_rows':sum(not x['correct'] for x in rows),
             'neural_calls_audited':audited,'array_elements_audited':array_elements,'independently_reconstructed_cases':n,'independent_management_replays':n,'B_C_comparisons_equal':len(b),
             'producer_modules_imported':source_modules,'source_lock_sha256':lock,'matched_opposite_truth_pairs':len(pair_checks),'no_cue_counterfactuals':len(no_cue),
             'primary_near_heldout_families_meeting_gain_control':sum(x['meets_gain_and_control'] for x in near),'primary_useful_reference_signal':signal,
             'all_heldout_invalid_reference_rules_pass':all(x['invalid_rule_pass'] for x in paired) if paired else None,
             'bound_public_exact_prediction_agreement':bound_agreement,'underflow_check':underflow,'training_updates':0}
    dump(a.output/'INFORMATION_LIMITS.json',{'matched_pairs':pair_checks,'no_cue_counterfactuals':no_cue,'nonidentifiable_strata_gate_fitting':'not_performed'})
    dump(a.output/'SCORE_RECEIPT.json',receipt)
    print(json.dumps(receipt,indent=2),flush=True)
if __name__=='__main__':main()
