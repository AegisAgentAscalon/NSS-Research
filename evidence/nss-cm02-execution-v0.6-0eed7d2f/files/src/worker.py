"""Streaming fixed-weight worker. It can see only the public message currently on stdin."""
from __future__ import annotations
import argparse,copy,json,sys,time
from pathlib import Path
import numpy as np
from io_utils import ROOT,paths,configure,canonical,array_digest,dump
from controller import Controller,scan_control,deep_size,cache_key,zero_work,merge_work,public_projection

ALLOWED_ATTEMPT_FILE=None
def guard(event,args):
    if event=='open' and args and isinstance(args[0],(str,bytes)):
        path=Path(str(args[0])).resolve()
        if path==ALLOWED_ATTEMPT_FILE:return
        if path.is_relative_to(ROOT/'raw') or path.is_relative_to(ROOT/'protocol') or 'protected' in path.name or path.name in ('generate.py','score.py'):
            raise PermissionError('CM02 worker cannot open stimuli/future/protected/protocol files')

def claim_global_forward(seed,query_id):
    import fcntl
    counter=ROOT/'audit/GLOBAL_FORWARD_LEDGER.json'
    with counter.open('r+') as f:
        fcntl.flock(f,fcntl.LOCK_EX);v=json.load(f)
        if v['attempted']>=6000:raise RuntimeError('Global 6000-forward hard stop')
        v['attempted']+=1;v['last_seed']=seed;v['last_query_id']=query_id
        f.seek(0);json.dump(v,f,sort_keys=True);f.truncate();f.flush();fcntl.flock(f,fcntl.LOCK_UN)

def emit(x):print(canonical(x).decode(),flush=True)
def main():
    a=argparse.ArgumentParser();a.add_argument('--seeds',required=True);a.add_argument('--attempt-log',type=Path,required=True);args=a.parse_args()
    global ALLOWED_ATTEMPT_FILE
    ALLOWED_ATTEMPT_FILE=args.attempt_log.resolve()
    sys.addaudithook(guard);base,stage=paths(True);configure()
    import torch
    from inference_loader import load_readers,inspect_exports
    from q010r.models import PublicInput,compose_read,resolve_code,model_state_hash
    seeds=[int(x) for x in args.seeds.split(',')]
    audit_before=inspect_exports();models={};identities={};model_before={}
    for seed in seeds:
        ms,ids=load_readers(seed);models[seed]=ms['near'];identities[seed]=ids['near'];model_before[seed]=model_state_hash(ms['near']);del ms
    cache={};attempts=0;completed=0;query_ordinal=0;logical=0;hits=0;controllers=None;episode=None;event_count=0
    emit({'status':'ready','export_audit':audit_before,'participating_models':identities,'models_have_native_recurrent_state':False,
          'model_tensor_bytes':{str(s):sum(x.numel()*x.element_size() for x in models[s].state_dict().values()) for s in seeds}})
    for line in sys.stdin:
        envelope=json.loads(line);msg=public_projection(envelope);typ=msg['type']
        if typ=='begin':
            if set(msg)!=set(('type','episode_id','catalogue')):raise ValueError('begin message fields')
            episode=msg['episode_id'];cat=msg['catalogue'];controllers={k:Controller(k,cat['book'],cat['active'],cat['symbols']) for k in ('W','I','L')}
            event_count=0;cumulative={k:zero_work() for k in controllers};emit({'type':'begun','episode_id':episode});continue
        if typ=='event':
            if set(msg)!=set(('type','event')):raise ValueError('event message fields')
            if controllers is None:raise ValueError('event without begin')
            updates={};times={}
            for k,c in controllers.items():
                t=time.perf_counter_ns();w=c.apply(msg['event']);times[k]=time.perf_counter_ns()-t;merge_work(cumulative[k],w)
                updates[k]={'work':w,'controller_unique_graph_bytes':deep_size(c), 'entry_state':[[task,value] for task,value in sorted(c.state['entries'].items())]}
            event_count+=1
            emit({'type':'event_committed','episode_id':episode,'event_count':event_count,'event_id':msg['event']['event'],'updates':updates,'timing_ns':times});continue
        if typ=='query':
            if set(msg)!=set(('type','query_id','event_count','current','arrays')):raise ValueError('query message fields')
            if event_count!=msg['event_count']:raise ValueError('event prefix mismatch')
            arrays={k:np.asarray(v,np.bool_ if k in ('valid','active') else np.int64 if k=='symbols' else np.float32) for k,v in msg['arrays'].items()}
            if set(arrays)!=set(('keys','values','valid','query','book','active','symbols')):raise ValueError('numerical schema')
            for k,c in controllers.items():
                if c.state['current']!=msg['current']:raise ValueError('context mismatch')
                for f in ('keys','values','valid','book','active','symbols'):
                    if c.state[f].dtype!=arrays[f].dtype or c.state[f].tobytes()!=arrays[f].tobytes():raise ValueError('store reconstruction mismatch '+f)
            order=('W','I','O');order=order[query_ordinal%3:]+order[:query_ordinal%3];query_ordinal+=1
            routes={};work={};timing={}
            for k in order:
                t=time.perf_counter_ns()
                if k=='O':r={'action':'original','reason':'no_retained_selection','fields':None,'canonical_key':None};w=zero_work();w['query_visits']=1
                else:r,w=controllers[k].route()
                timing[k]=time.perf_counter_ns()-t;routes[k]=r;work[k]=w
            if routes['W']!=routes['I']:raise AssertionError('W/I route mismatch')
            exact={};exact_work={};exact_memory={}
            for k in ('W','I'):exact['X_'+k],exact_work['X_'+k]=controllers[k].exact(routes[k])
            t=time.perf_counter_ns();sr,sp,sw,sm=scan_control(controllers['W'].state['journal'],arrays['book'],arrays['active'],arrays['symbols'],arrays['query']);timing['X_S']=time.perf_counter_ns()-t
            if sr!=routes['I']:raise AssertionError('prefix scan disagrees')
            exact['X_S']=sp;exact_work['X_S']=sw;exact_memory['X_S']=sm
            lr,lw=controllers['L'].route();lp,lx=controllers['L'].exact(lr);merge_work(lw,lx)
            exact['X_latest']=lp;exact_work['X_latest']=lw;exact_memory['X_latest']=controllers['L'].memory(arrays['query'])
            if exact['X_W']!=exact['X_I'] or sp!=exact['X_W']:raise AssertionError('pinned exact control mismatch')
            # Model/controller API receives a projection: hidden/future suffixes are not inputs.
            for altered in ({'private':{'intent':-1},'future':[{'type':'delete'}]}, {'private':{'intent':777},'future':[{'type':'correct'}]}):
                if canonical(public_projection(dict(public=msg,**altered)))!=canonical(msg):raise AssertionError('private/future projection leak')
            decoded=[];new=[];memory={};nulls=0
            for seed in seeds:
                model=models[seed];memory[str(seed)]={k:controllers[k].memory(arrays['query'],model) for k in ('W','I')}
                memory[str(seed)]['O']={'whole_unique_python_graph_bytes':deep_size({'arrays':arrays,'current':msg['current'],'model':model}),
                     'state_array_bytes':sum(v.nbytes for k,v in arrays.items() if k!='query'),'query_bytes':arrays['query'].nbytes,'selection_semantic_field_bytes':0,'selection_ascii_bytes':0,'entries':0,'journal_events':0}
                for k in order:
                    route=routes[k];logical+=1
                    if route['action']=='abstain':
                        nulls+=1;decoded.append({'seed':seed,'arm':k,'output_id':None,'predicted':-1,'model_work_required':0,'cache_hit':False});continue
                    q=arrays['query'] if route['action']=='original' else np.asarray(route['canonical_key'],np.float32)
                    a=dict(arrays,query=q);ck=cache_key(model_before[seed],a)
                    hit=ck in cache
                    if not hit:
                        attempted_digest=array_digest(a);public=PublicInput.sanitized(*(torch.from_numpy(a[f][None].copy()) for f in ('keys','values','valid')),torch.from_numpy(q[None].copy()))
                        before_public=array_digest({f:getattr(public,f).numpy().copy() for f in ('keys','values','valid','query')})
                        claim_global_forward(seed,msg['query_id'])
                        attempts+=1;dump(args.attempt_log,{'attempted':attempts,'completed':completed,'physical_forward_batches':attempts,'seed':seed,'query_id':msg['query_id']})
                        if attempts>3000:raise RuntimeError('per-pass conservative forward cap')
                        with torch.inference_mode():
                            out=model.forward_step(public,0);comp=compose_read(out.selection_logits,public.values)
                            if not torch.equal(out.read_code,comp.read_code):raise AssertionError('pointer recomposition mismatch')
                            idx,status,clean=resolve_code(out.read_code,torch.from_numpy(a['book'][None]),torch.from_numpy(a['active'][None]))
                        if array_digest(a)!=attempted_digest or array_digest({f:getattr(public,f).numpy() for f in ('keys','values','valid','query')})!=before_public:raise AssertionError('numerical input mutated')
                        pred=int(a['symbols'][int(idx[0])]) if int(status[0])>0 else -1
                        oid=__import__('hashlib').sha256(ck.encode()).hexdigest()
                        result={'query':q[None].tolist(),'logits':out.selection_logits.numpy().tolist(),'weights':comp.weights.numpy().tolist(),
                           'weighted_code':comp.weighted_code.numpy().tolist(),'read_code':out.read_code.numpy().tolist(),'clean_code':clean.numpy().tolist(),
                           'resolved_ids':[pred],'selected_rows':out.selection_logits.argmax(-1).numpy().tolist()}
                        info={'output_id':oid,'model_seed':seed,'model_hash':model_before[seed],'query_id':msg['query_id'],'input_digest':attempted_digest,'arrays':result}
                        cache[ck]=info;new.append(info);completed+=1
                    else:hits+=1
                    info=cache[ck];decoded.append({'seed':seed,'arm':k,'output_id':info['output_id'],'predicted':info['arrays']['resolved_ids'][0],'model_work_required':1,'cache_hit':hit})
            emit({'type':'query_result','episode_id':episode,'query_id':msg['query_id'],'event_count':event_count,'routes':routes,
                  'latest_route':lr,'scan_route':sr,'exact_controls':exact,'query_work':work,'exact_work':exact_work,'exact_memory':exact_memory,
                  'cumulative_event_work':cumulative,'memory_by_seed':memory,'decision_rows':decoded,'new_outputs':new,'query_order':list(order),
                  'timing_ns':timing,'experimental_cache_unique_graph_bytes':deep_size(cache),'projection_checks':2})
            continue
        if typ=='finish':
            after=inspect_exports()
            if audit_before!=after:raise AssertionError('export drift')
            for s in seeds:
                if model_state_hash(models[s])!=model_before[s]:raise AssertionError('runtime model changed')
            dump(args.attempt_log,{'attempted':attempts,'completed':completed,'physical_forward_batches':attempts})
            emit({'type':'finished','attempted_forwards':attempts,'completed_forwards':completed,'physical_forward_batches':attempts,
                  'logical_interface_decisions':logical,'cache_hits':hits,'participating_model_seeds':seeds,'export_audit_after':after,
                  'new_optimizer_updates':0,'new_training':False,'runtime_weights_unchanged':True,'experimental_cache_unique_graph_bytes':deep_size(cache),
                  'worker_guard':'current public messages on stdin; raw/protocol/producer/scorer-file reads denied','source_modules_imported':[x for x in sys.modules if x in ('generate','score')]})
            break
        raise ValueError('unknown public message type')
if __name__=='__main__':
    try:main()
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr);emit({'type':'fatal','error':type(e).__name__,'message':str(e)});sys.exit(1)
