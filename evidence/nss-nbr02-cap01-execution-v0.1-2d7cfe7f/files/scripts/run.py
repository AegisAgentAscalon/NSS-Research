from pathlib import Path
import sys,json,time,traceback,shutil,resource,itertools
import numpy as np
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from cap01 import *
from fixtures import grid,exact_targets

def get_model(seed,mode):
    m=Reader();d=torch.load(ROOT/f'checkpoints/{seed}_{mode}.pt',weights_only=True,map_location='cpu')
    m.load_state_dict(d['model']);m.eval();return m

def prepare():
    cases=[]
    for item in grid():
        e=item['episode'];fid=item['stratum']+'_'+e['id'];write_json(ROOT/'fixtures'/f'{fid}.json',item)
        for rev,seed,mode,policy,cap in itertools.product(range(2),item['models'],['dense','hsa'],['ordinary','segmented'],item['caps']):
            ident=f'{fid}_r{rev}_m{seed}_{mode}_{policy}_c{cap}'
            cases.append({'id':ident,'fixture':fid,'stratum':item['stratum'],'rev':rev,'seed':seed,'mode':mode,'policy':policy,'cap':cap})
    write_json(ROOT/'CASES.json',cases)
    files={str(p.relative_to(ROOT)):file_sha(p) for d in ['source','tests','scripts','checkpoints','fixtures'] for p in (ROOT/d).rglob('*') if p.is_file() and '__pycache__' not in str(p)}
    files.update({k:file_sha(ROOT/k) for k in ['PROTOCOL.md','CASES.json']})
    write_json(ROOT/'SOURCE_FIXTURE_LOCK.json',{'utc':time.time(),'files':files,'cases':len(cases),
             'runtime':{'torch':torch.__version__,'numpy':np.__version__,'python':sys.version}})
    print('Locked',len(cases),'cases;',len(files),'files')

def run(start=0,end=None):
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    origin=time.perf_counter();cases=json.loads((ROOT/'CASES.json').read_text());models={};refcache={}
    lock=json.loads((ROOT/'SOURCE_FIXTURE_LOCK.json').read_text())
    assert all(file_sha(ROOT/k)==v for k,v in lock['files'].items()),'SOURCE_LOCK_CHANGED'
    work=ROOT/'_working';work.mkdir(exist_ok=True);journal=ROOT/'results/ATTEMPTS.jsonl';done=0
    for ix,c in enumerate(cases):
        if ix<start or (end is not None and ix>=end):continue
        path=ROOT/'results/cases'/f"{c['id']}.json"
        if path.exists():continue
        if time.perf_counter()-origin>900:raise RuntimeError('RUNNER_TIME_GUARD')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024>2*1024**3:raise RuntimeError('RSS_GUARD')
        if ix%20==0 and sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())>240*1024**2:raise RuntimeError('EVIDENCE_GUARD')
        with journal.open('a') as f:f.write(json.dumps({'case':c['id'],'index':ix,'event':'START','utc':time.time()})+'\n')
        rec={'case':c,'index':ix};temp=work/f'{ix:04}'
        try:
            item=json.loads((ROOT/'fixtures'/f"{c['fixture']}.json").read_text());e=item['episode'];w=e['worlds'][c['rev']];ts=e['targets']
            key=(c['seed'],c['mode'])
            if key not in models:models[key]=get_model(*key)
            m=models[key];before=model_hash(m);spec,graph,cl=graph_and_closure(w,ts,c['mode'])
            closures=[len(graph_and_closure(w,[t],c['mode'])[2][0]) for t in ts]
            rec.update({'n':e['n'],'family':e['family'],'targets':ts,'world_sha256':digest(w),'positions':spec.positions,
                        'resident_target_closures':closures,'resident_admitted':sum(n<=c['cap'] for n in closures),
                        'joint_initial_closure':len(cl[0]),'first_layer_rows':len(cl[1]),'final_rows':len(cl[2])})
            rk=(c['fixture'],c['rev'],c['seed'],c['mode'])
            if rk not in refcache:
                rt=time.perf_counter();ref=full_reference(m,w,c['mode'],ts);ref['reference_seconds']=time.perf_counter()-rt
                if len(refcache)>=4:refcache.clear()
                refcache[rk]=ref
            ref=refcache[rk];t=time.perf_counter();eng=StreamExecutor(m,w,ts,c['mode'],c['policy'],c['cap'],temp)
            rec['paused']=False;rec['stale_resume_rejected']=None
            keep=e['family']=='resume' and c['rev']==0 and c['seed']==8801 and c['policy']=='segmented'
            if e['family']=='resume':
                if eng.advance(7):raise RuntimeError('PAUSE_POINT_NOT_REACHED')
                snap=temp/'resume.json';eng.snapshot(snap);rec['paused']=True;rec['checkpoint_bytes']=snap.stat().st_size
                if c['rev']==0:
                    try:StreamExecutor.restore(snap,m,e['worlds'][1],ts,c['mode'],c['policy'],c['cap'])
                    except CapError as err:rec['stale_resume_rejected']=err.code
                    else:raise RuntimeError('STALE_RESUME_ACCEPTED')
                if keep:
                    pd=ROOT/'results/paused'/c['id'];shutil.copytree(temp,pd);write_json(pd/'CASE.json',c)
                eng=StreamExecutor.restore(snap,m,w,ts,c['mode'],c['policy'],c['cap'])
            eng.advance()
            if eng.stats['tiles']>500000:raise RuntimeError('TILE_GUARD')
            logits=eng.logits();elapsed=time.perf_counter()-t
            a=np.load(eng.h1_file,mmap_mode='r');b=np.load(eng.h2_file,mmap_mode='r')
            cmp={'block1':compare(a[list(cl[1])],ref['stage1'][list(cl[1])]),
                 'block2':compare(b[list(cl[2])],ref['stage2'][list(cl[2])]),'logits':compare(logits,ref['logits'])}
            y=exact_targets(w,ts);pred=logits.argmax(-1);rp=ref['logits'].argmax(-1)
            nok=all(v['violations']==0 for v in cmp.values());cok=bool(np.array_equal(pred,rp))
            rec.update({'status':'COMPLETE' if nok and cok else 'NUMERICAL_DIAGNOSTIC','comparisons':cmp,'class_parity':cok,
                        'logits':logits.tolist(),'reference_logits':ref['logits'].tolist(),'targets_y':y.tolist(),'predictions':pred.tolist(),
                        'correct':int((y==pred).sum()),'whole_correct':bool((y==pred).all()),
                        'false_complete':int(((pred==1)&(y!=1)).sum()),'false_ready':int(((pred==2)&(y!=2)).sum()),
                        'stats':dict(eng.stats),'core_seconds':elapsed,'reference_seconds':ref['reference_seconds'],
                        'model_unchanged':model_hash(m)==before,'freeze':w['freeze'],
                        'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024})
            if not nok or not cok:
                f=ROOT/'failures/numerical';f.mkdir(exist_ok=True)
                if len(list(f.glob('*.npz')))<8:
                    np.savez_compressed(f/f"{c['id']}.npz",block1=np.asarray(a[list(cl[1])]),block1_ref=ref['stage1'][list(cl[1])],
                                        block2=np.asarray(b[list(cl[2])]),block2_ref=ref['stage2'][list(cl[2])],logits=logits,reference=ref['logits'])
            assert rec['model_unchanged'];assert eng.stats['peak_selected_positions']<=c['cap'];del a,b,eng
        except Exception:
            rec.update({'status':'TECHNICAL_FAILURE','traceback':traceback.format_exc()});write_json(ROOT/'failures'/f"{c['id']}.json",rec)
        write_json(path,rec)
        with journal.open('a') as f:f.write(json.dumps({'case':c['id'],'event':rec['status'],'utc':time.time()})+'\n')
        shutil.rmtree(temp,ignore_errors=True);done+=1
        if done%12==0:print(json.dumps({'completed':done,'index':ix,'status':rec['status'],'elapsed_s':round(time.perf_counter()-origin,2)}),flush=True)
    write_json(ROOT/'results'/f'RUN_RECEIPT_{start}_{end}.json',{'completed_this_call':done,'seconds':time.perf_counter()-origin,
               'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'optimizer_applications':0})
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='prepare':prepare()
    else:run(int(sys.argv[1]) if len(sys.argv)>1 else 0,int(sys.argv[2]) if len(sys.argv)>2 else None)
