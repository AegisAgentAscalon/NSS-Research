"""Inference producer: public files only. Protected truth-file access is blocked."""
from __future__ import annotations
import argparse,copy,json,sys,time
from dataclasses import asdict
from pathlib import Path
import numpy as np
from common import ROOT,paths,configure,check_lock,load,dump,read_lines,write_lines,arrays,canonical,sha,digest_arrays
from manager import Workspace,encode,decode,compile_public,route,deep_size,key

def guard(event,args):
    if event=='open' and args and isinstance(args[0],(str,bytes)):
        name=str(args[0])
        if 'protected.jsonl' in name:raise PermissionError('Producer is forbidden from opening scorer truth')

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--fixture',action='store_true');a=p.parse_args()
    sys.addaudithook(guard);r,s=paths(True);configure();lock=check_lock()
    import torch
    from inference_loader import load_readers,inspect_exports
    from q010r.models import PublicInput,compose_read,resolve_code,model_state_hash
    audit_before=inspect_exports();raw=arrays(a.input/'inputs.npz');pub=read_lines(a.input/'public.jsonl');n=len(pub)
    routes=[];public_controls=[];costs=[];isolation=0
    for i,v in enumerate(pub):
        view=compile_public(v['journal'],v['current']);w=Workspace(**v['workspace']);t=time.perf_counter_ns()
        b=route(w,view,v['current']);c=route(decode(v['serialized']),view,v['current']);latency=time.perf_counter_ns()-t
        if canonical(b)!=canonical(c) or encode(w)!=v['serialized']:raise AssertionError('B/C disagreement')
        # Counterfactual envelope labels cannot enter this public-only function.
        def envelope_call(envelope):
            vv=envelope['public'];return route(Workspace(**vv['workspace']),compile_public(vv['journal'],vv['current']),vv['current'])
        for private in ({'expected':-1,'owner':[],'query_source':'UNKNOWN'},{'expected':999,'owner':list(range(16)),'query_source':5}):
            if envelope_call({'public':v,'private':private})!=b:raise AssertionError('protected-label interference')
        isolation+=1
        if b['lookup_count']>2:raise AssertionError('lookup budget')
        routes.append({'index':i,'structured':b,'serialized':c,'transition_log':view['transitions'],
                       'workspace_after_events':view['workspace'],'retained_workspace':asdict(w)})
        pred=-1
        if b['action']=='canonical':pred=view['records'][key(w.scope,w.handle)]['payload_symbol']
        public_controls.append({'index':i,'control':'public_exact_lookup','predicted':pred,'action':b['action']})
        costs.append({'index':i,'serialized_bytes':len(v['serialized'].encode()),'byte_control_symbols':56,
                      'packed_fields_bytes':26,'python_workspace_bytes':deep_size(w),'python_string_bytes':deep_size(v['serialized']),
                      'python_parsed_fields_bytes':deep_size(asdict(w)),'journal_canonical_bytes':len(canonical(v['journal'])),
                      'python_journal_bytes':deep_size(v['journal']),'directory_canonical_bytes':len(canonical(view['records'])),
                      'binding_index_canonical_bytes':len(canonical(view['bindings'])),'python_directory_and_binding_bytes':deep_size({'r':view['records'],'b':view['bindings']}),
                      'workspace_changes':view['writes'],'workspace_rewritten_bytes':view['writes']*56,
                      'workspace_field_reads_symbols_BC':112,'journal_events_processed':len(v['journal']),
                      'lookup_count_per_interface':b['lookup_count'],'lookup_returned_bytes_per_interface':sum(x['returned_bytes'] for x in b['lookups']),
                      'route_pair_nanoseconds':latency,'canonical_query_bytes':68 if b['action']=='canonical' else 0,
                      'public_state_arrays_bytes':sum(raw[k][i].nbytes for k in ('keys','values','valid')),
                      'resolver_catalogue_bytes':sum(raw[k][i].nbytes for k in ('book','active','symbols')),
                      'active_query_bytes':68,'payload_vectors_in_journal_bytes':sum(68 for e in v['journal'] if 'payload_code' in e),
                      'canonical_key_vectors_in_journal_bytes':sum(68 for e in v['journal'] if 'key' in e)})
    a.output.mkdir(parents=True,exist_ok=False)
    write_lines(a.output/'routing.jsonl',routes);write_lines(a.output/'public_control.jsonl',public_controls);write_lines(a.output/'costs.jsonl',costs)
    chunks=[];attempted=0;successful=0;batches_attempted=0;identities=[]
    seeds=[1201] if a.fixture else range(1201,1206)
    family_size=8 if a.fixture else 64
    for seed in seeds:
        models,model_ids=load_readers(seed)
        for role in ('ordinary','near','attention'):
            model=models[role];identities.append(model_ids[role]);before=model_state_hash(model)
            for start in range(0,n,family_size):
                for variant in ('original','canonical'):
                    inds=np.array([i for i in range(start,start+family_size) if variant=='original' or routes[i]['structured']['action']=='canonical'],dtype=np.int64)
                    if len(inds)==0:continue
                    q=raw['query'][inds].copy() if variant=='original' else np.array([routes[int(i)]['structured']['canonical_key'] for i in inds],np.float32)
                    inputs={k:raw[k][inds].copy() for k in ('keys','values','valid')};pre=digest_arrays(inputs|{'query':q})
                    public=PublicInput.sanitized(*(torch.from_numpy(inputs[k]) for k in ('keys','values','valid')),torch.from_numpy(q))
                    public_before=digest_arrays({k:getattr(public,k).numpy().copy() for k in ('keys','values','valid','query')})
                    attempted+=len(inds);batches_attempted+=1
                    dump(a.output/'ATTEMPTS.json',{'logical_calls_attempted':attempted,'logical_calls_completed':successful,'physical_forward_batches_attempted':batches_attempted})
                    if attempted>(48 if a.fixture else 15360):raise AssertionError('forward cap exceeded')
                    with torch.inference_mode():
                        returned=model.forward_step(public,0);composed=compose_read(returned.selection_logits,public.values)
                        if not torch.equal(returned.read_code,composed.read_code):raise AssertionError('pointer arithmetic mismatch')
                        index,status,clean=resolve_code(returned.read_code,torch.from_numpy(raw['book'][inds]),torch.from_numpy(raw['active'][inds]))
                    result={'indices':inds,'query':q,'logits':returned.selection_logits.numpy().copy(),'weights':composed.weights.numpy().copy(),
                            'weighted_code':composed.weighted_code.numpy().copy(),'read_code':returned.read_code.numpy().copy(),
                            'clean_code':clean.numpy().copy(),'resolved_ids':np.where(status.numpy()>0,np.take_along_axis(raw['symbols'][inds],index.numpy().clip(0,15)[:,None],axis=1)[:,0],-1).astype(np.int64),
                            'selected_rows':returned.selection_logits.argmax(-1).numpy().copy()}
                    if digest_arrays(inputs|{'query':q})!=pre:raise AssertionError('mutated public arrays')
                    if digest_arrays({k:getattr(public,k).numpy() for k in ('keys','values','valid','query')})!=public_before:raise AssertionError('mutated sanitized public input')
                    name=f'{role}_{seed}_family{start//family_size}_{variant}.npz';np.savez_compressed(a.output/name,**result)
                    chunks.append({'file':name,'seed':seed,'role':role,'variant':variant,'rows':len(inds),'sha256':sha(a.output/name)})
                    successful+=len(inds)
            if model_state_hash(model)!=before:raise AssertionError('model mutation')
        print(f'CAPTURED seed {seed}: {successful} logical forward calls',flush=True)
    audit_after=inspect_exports()
    if audit_before!=audit_after:raise AssertionError('saved export drift')
    dump(a.output/'ATTEMPTS.json',{'logical_calls_attempted':attempted,'logical_calls_completed':successful,'physical_forward_batches_attempted':batches_attempted})
    dump(a.output/'CAPTURE.json',{'kind':'fixture' if a.fixture else 'main','records':n,'chunks':chunks,'source_lock_sha256':lock,
                                'logical_forward_calls':successful,'physical_forward_batches':batches_attempted,'model_identities':identities,
                                'weights_before':audit_before,'weights_after':audit_after,'training_updates':0,'protected_file_guard_enabled':True,
                                'protected_label_mutation_checks':isolation,'structured_serialized_equal':True,
                                'input_hashes':{x:sha(a.input/x) for x in ('inputs.npz','public.jsonl','GENERATION.json')}})
if __name__=='__main__':main()
