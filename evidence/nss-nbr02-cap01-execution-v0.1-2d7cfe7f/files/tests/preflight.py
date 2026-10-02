from pathlib import Path
import sys,tempfile,json,copy,traceback,time,shutil
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from cap01 import *
from fixtures import make_episode,exact_targets
from retained_common import oracle

def run():
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    results=[];start=time.perf_counter();numerical=[]
    model=Reader();model.load_state_dict(torch.load(ROOT/'checkpoints/8801_hsa.pt',weights_only=True)['model']);model.eval()
    with tempfile.TemporaryDirectory(prefix='cap01_preflight_',dir='/mnt/data') as temp:
        temp=Path(temp)
        for n in [8,32]:
            for mode in ['dense','hsa']:
                for policy in ['ordinary','segmented']:
                    for cap in [16,32]:
                        e=make_episode(n,991101+n,'resume');w=e['worlds'][0];ts=e['targets']
                        case=f'{n}_{mode}_{policy}_{cap}'
                        ref=full_reference(model,w,mode,ts)
                        a=StreamExecutor(model,w,ts,mode,policy,cap,temp/case)
                        a.advance(limit_tiles=7);path=temp/case/'resume.json';a.snapshot(path)
                        # Preserve paused state for exactly matched continuation comparison.
                        cp=temp/(case+'_clone');shutil.copytree(temp/case,cp)
                        a.advance();y=a.logits()
                        b=StreamExecutor.restore(cp/'resume.json',model,w,ts,mode,policy,cap);b.advance();z=b.logits()
                        assert np.array_equal(y,z),'resume mismatch'
                        stats=compare(y,ref['logits']);assert stats['violations']==0,stats
                        assert np.array_equal(y.argmax(-1),ref['logits'].argmax(-1))
                        h1=np.load(a.h1_file,mmap_mode='r')[list(a.closure[1])]
                        st=compare(h1,ref['stage1'][list(a.closure[1])]);assert st['violations']==0,st
                        numerical.extend([stats,st]);assert a.stats['peak_selected_positions']<=cap
                        assert np.array_equal(exact_targets(w,ts),oracle(w)[ts])
                        results.append({'case':case,'pass':True})
        # Isolated fault injections: restore only, not scientific execution.
        e=make_episode(8,991999,'resume');w=e['worlds'][0];ts=e['targets'];base=temp/'fault'
        x=StreamExecutor(model,w,ts,'hsa','segmented',16,base);x.advance(1);x.snapshot(base/'resume.json')
        def fails(name,fn,expected=None):
            try:fn()
            except CapError as err:
                assert expected is None or err.code==expected,(name,err.code,expected)
                results.append({'case':name,'pass':True,'detected':err.code});return
            raise AssertionError('undetected '+name)
        args=[model,w,ts,'hsa','segmented',16]
        fails('changed_evidence',lambda:StreamExecutor.restore(base/'resume.json',model,e['worlds'][1],ts,'hsa','segmented',16),'STALE_OR_MISBOUND_SNAPSHOT')
        fails('wrong_budget',lambda:StreamExecutor.restore(base/'resume.json',model,w,ts,'hsa','segmented',32),'STALE_OR_MISBOUND_SNAPSHOT')
        fails('wrong_scope',lambda:StreamExecutor.restore(base/'resume.json',*args,scope='other'),'STALE_OR_MISBOUND_SNAPSHOT')
        fails('wrong_reader',lambda:StreamExecutor.restore(base/'resume.json',model,w,ts,'dense','segmented',16),'STALE_OR_MISBOUND_SNAPSHOT')
        altered=copy.deepcopy(model)
        with torch.no_grad():next(altered.parameters()).add_(.001)
        fails('changed_weights',lambda:StreamExecutor.restore(base/'resume.json',altered,w,ts,'hsa','segmented',16),'STALE_OR_MISBOUND_SNAPSHOT')
        failcopy=temp/'bad';shutil.copytree(base,failcopy)
        p=failcopy/'embedding.npy';raw=bytearray(p.read_bytes());raw[-2]^=1;p.write_bytes(raw)
        fails('corrupt_spool',lambda:StreamExecutor.restore(failcopy/'resume.json',*args),'CORRUPT_SPOOL')
        p=base/'resume.json';original=p.read_bytes();env=json.loads(original);env['payload']['key_offset']+=1;p.write_text(json.dumps(env))
        fails('corrupt_checkpoint',lambda:StreamExecutor.restore(p,*args),'CORRUPT_SNAPSHOT');p.write_bytes(original)
        env=json.loads(original);env['payload']['key_offset']=100000;env['sha256']=digest(env['payload']);p.write_text(json.dumps(env))
        fails('invalid_cursor',lambda:StreamExecutor.restore(p,*args),'INVALID_CURSOR');p.write_bytes(original)
        env=json.loads(original);d=env['payload']['weighted_values'];d['bytes_b64']='AAAA';env['sha256']=digest(env['payload']);p.write_text(json.dumps(env))
        fails('corrupt_accumulator',lambda:StreamExecutor.restore(p,*args),'CORRUPT_ACCUMULATOR');p.write_bytes(original)
        fails('bad_target',lambda:StreamExecutor(model,w,[99],'hsa','ordinary',16,temp/'t'),'INVALID_TARGETS')
        fails('inadequate_tile',lambda:StreamExecutor(model,w,ts,'hsa','ordinary',4,temp/'u'),'INSUFFICIENT_TILE_BUDGET')
        bad=copy.deepcopy(w);bad['nuisance'][0][0]=float('nan')
        # The canonical source binding also rejects nonfinite JSON before ingestion.
        try:StreamExecutor(model,bad,ts,'hsa','ordinary',16,temp/'nf')
        except (ValueError,CapError):results.append({'case':'nonfinite_source','pass':True})
        else:raise AssertionError('nonfinite accepted')
        fails('unfinished_output',lambda:x.logits(),'INCOMPLETE_COMPUTATION')
    out={'passed':len(results),'cases':results,'numerical':numerical,'elapsed_seconds':time.perf_counter()-start,'optimizer_applications':0}
    write_json(ROOT/'results/PREFLIGHT.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ['cases','numerical']},indent=2))

if __name__=='__main__':
    try:run()
    except Exception:
        write_json(ROOT/'failures/prelock_preflight_failure.json',{'traceback':traceback.format_exc()});raise
