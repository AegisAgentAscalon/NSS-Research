from __future__ import annotations
import copy,json,time,traceback
from pathlib import Path
import numpy as np
import torch
from torch.utils._python_dispatch import TorchDispatchMode
from common import *
from store import *
ROOT=Path(__file__).resolve().parents[1]

def main():
    setup();start=time.perf_counter();tests=[];numeric=[]
    def check(name,condition,details=None):
        tests.append({'name':name,'pass':bool(condition),'details':details})
        if not condition: print('FAIL',name,details,flush=True)
    def throws(name,fn,code):
        try:fn();check(name,False,'no exception')
        except ContextError as e:check(name,str(e)==code,str(e))
    for seed in range(772000,772064):
        w=worlds(seed,1,8)[0];s=store_from_world(w);a=Manager(s,False);b=Manager(s,True)
        roots=list(range(8));oldclock=s.clock
        p=a.packet(roots,freeze=w['freeze']);q=b.packet(roots,freeze=w['freeze'])
        check(f'{seed}:equal_initial',p==q)
        check(f'{seed}:roundtrip',world_from_packet(p)['progress']==w['progress'])
        for _ in range(3):check(f'{seed}:warm_equal',a.packet(roots,freeze=w['freeze'])==b.packet(roots,freeze=w['freeze']))
        snap=b.snapshot();s2=VersionedStore.restore(s.dump());b2=Manager.restore(s2,snap)
        check(f'{seed}:restart',b2.packet(roots,freeze=w['freeze'])==q)
        r=s.get(3,'P');r['revision']+=1;r['progress']=1-r['progress'];r['source']+=':revision';r.pop('issued',None);s.publish(r)
        p2=a.packet(roots,freeze=w['freeze']);q2=b.packet(roots,freeze=w['freeze'])
        check(f'{seed}:invalidation',p2==q2 and q2!=q and b.invalidations==1)
        check(f'{seed}:historical_cutoff',world_from_packet(a.packet(roots,cutoff=oldclock,freeze=w['freeze']))['progress']==w['progress'])
        check(f'{seed}:nonerasure',len(s.history[3])==2)
        s.act_once('action:1',{'file':'A','operation':'write'})
        r2=VersionedStore.restore(s.dump());r2.act_once('action:1',{'file':'A','operation':'write'})
        check(f'{seed}:idempotent_restart',r2.effect_count==1)
    w=worlds(773000,1,8)[0];s=store_from_world(w);m=Manager(s,True);roots=list(range(8));m.packet(roots)
    throws('fault:wrong_scope',lambda:m.packet(roots,scope='OTHER'),'WRONG_SCOPE')
    throws('fault:future_not_visible',lambda:m.packet(roots,cutoff=0),'NOT_VISIBLE_AT_CUTOFF')
    throws('fault:budget',lambda:Manager(s,True,budget=32).packet(roots),'MANDATORY_CONTEXT_OVER_BUDGET')
    ss=VersionedStore.restore(s.dump());del ss.history[1]
    throws('fault:missing_dependency',lambda:Manager(ss,False).packet(roots),'MISSING_RECORD')
    ss=VersionedStore.restore(s.dump());ss.history[1][-1]['blob']+=' '
    throws('fault:source_corruption',lambda:Manager(ss,False).packet(roots),'SOURCE_DIGEST_MISMATCH')
    snap=m.snapshot();broken=copy.deepcopy(snap);broken['data']['budget']+=1
    throws('fault:checkpoint_corruption',lambda:Manager.restore(s,broken),'CHECKPOINT_DIGEST_MISMATCH')
    mm=Manager.restore(s,m.snapshot());next(iter(mm.cache.values()))['body']+=' '
    throws('fault:cache_corruption',lambda:mm.packet(roots),'CACHE_DIGEST_MISMATCH')
    rr=s.get(0,'P');throws('fault:duplicate_revision',lambda:s.publish(rr),'NON_MONOTONIC_REVISION')
    s.act_once('X',{'a':1});throws('fault:receipt_conflict',lambda:s.act_once('X',{'a':2}),'RECEIPT_PAYLOAD_CONFLICT')
    # Counterfactual stale cache and omitted evidence must change/destroy the paired contract.
    rr=s.get(0,'P');rr['revision']+=1;rr['progress']=1-rr['progress'];s.publish(rr)
    before=next(iter(m.cache.values()))['body'].encode();after=m.packet(roots)
    check('fault:stale_packet_detected',before!=after)
    bad=json.loads(after);bad['records']=[r for r in bad['records'] if r['id']!=1]
    throws('fault:omitted_dependency_at_reader',lambda:world_from_packet(canonical(bad)),'UNRESOLVED_READER_DEPENDENCY')
    # Numerical reference: fixed random q/k/v, all rows/gradients.
    for n in [3,8,16,32]:
        x,idx,valid,y=batch(worlds(774000+n,2,n));b,ts,kmax=idx.shape
        for dtype in [torch.float64,torch.float32]:
            torch.manual_seed(774100+n)
            vals=[torch.randn(2,2,ts,16,dtype=dtype,requires_grad=True) for _ in range(3)]
            q,k,v=vals
            out=sparse_attention(q,k,v,idx,valid);ref=masked_attention(q,k,v,idx,valid)
            atol,rtol=(1e-10,1e-9) if dtype==torch.float64 else (2e-5,2e-5)
            err=(out-ref).abs();tol=atol+rtol*ref.abs()
            row={'n':n,'dtype':str(dtype),'elements':out.numel(),'max_abs':err.max().item(),'outside':int((err>tol).sum())}
            loss=(out.square()).sum();gr=torch.autograd.grad(loss,vals,retain_graph=True)
            gr2=torch.autograd.grad(ref.square().sum(),vals)
            row['gradient_elements']=sum(z.numel() for z in gr)
            row['gradient_outside']=sum(int(((z-r).abs()>(atol+rtol*r.abs())).sum()) for z,r in zip(gr,gr2))
            row['gradient_max_abs']=max((z-r).abs().max().item() for z,r in zip(gr,gr2))
            # Independently indexed NumPy float64 softmax reference.
            if dtype==torch.float64:
                qa,ka,va=[z.detach().numpy() for z in vals];nr=np.zeros_like(qa)
                for bi in range(2):
                    for hi in range(2):
                        for ti in range(ts):
                            ids=idx[bi,ti][valid[bi,ti]].numpy()
                            score=ka[bi,hi,ids]@qa[bi,hi,ti]/4
                            prob=np.exp(score-score.max());prob/=prob.sum()
                            nr[bi,hi,ti]=prob@va[bi,hi,ids]
                e=np.abs(nr-out.detach().numpy());row['numpy_max_abs']=float(e.max());row['numpy_outside']=int((e>(atol+rtol*np.abs(nr))).sum())
            numeric.append(row);check(f'numerical:{n}:{dtype}',row['outside']==0 and row['gradient_outside']==0 and row.get('numpy_outside',0)==0,row)
    # Native sparsity: inspect every produced tensor shape, no dense pairwise square permitted.
    class Shapes(TorchDispatchMode):
        def __init__(self):super().__init__();self.shapes=[]
        def __torch_dispatch__(self,func,types,args=(),kwargs=None):
            z=func(*args,**(kwargs or {}))
            def walk(y):
                if isinstance(y,torch.Tensor):self.shapes.append(list(y.shape))
                elif isinstance(y,(list,tuple)):
                    for a in y:walk(a)
            walk(z);return z
    x,idx,valid,y=batch(worlds(774200,1,32));ts=x.shape[1]
    q,k,v=[torch.randn(1,2,ts,16) for _ in range(3)]
    shapes=Shapes()
    with shapes: sparse_attention(q,k,v,idx,valid)
    squares=[z for z in shapes.shapes if sum(a==ts for a in z)>=2]
    check('native:no_dense_square',len(squares)==0,{'T':ts,'shapes':shapes.shapes,'square_shapes':squares})
    # Actual differentiability/optimizer smoke; no behavioral tuning.
    steps=0
    for mode in ['dense','hsa']:
        torch.manual_seed(775000);model=Reader();opt=torch.optim.AdamW(model.parameters(),lr=.002)
        x,idx,valid,y=batch(worlds(775001,16,8))
        for j in range(2):
            opt.zero_grad(set_to_none=True);o=model(x,idx,valid,8,mode);loss=F.cross_entropy(o.reshape(-1,4),y.reshape(-1));loss.backward();opt.step();steps+=1
        check(f'smoke:{mode}',bool(torch.isfinite(loss)),{'loss':loss.item()})
    receipt={'pass':all(t['pass'] for t in tests),'checks':len(tests),'passed':sum(t['pass'] for t in tests),
             'optimizer_applications':steps,'seconds':time.perf_counter()-start,'tests':tests,'numerical':numeric}
    write_json(ROOT/'results/preflight.json',receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('tests','numerical')}),flush=True)
    return 0 if receipt['pass'] else 2
if __name__=='__main__':raise SystemExit(main())
