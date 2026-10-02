"""Engineering checks. No optimizer is constructed and no gradient is applied."""
from __future__ import annotations
import sys,json,copy,traceback,math,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from support import *
from nss_hsa import *
from nss_hsa.attention import graph_mask
from nss_hsa.hierarchy import canonical
import sh01_common as old

RESULTS=[];COMPARE=[]
def check(name,fn):
    try:detail=fn();row={'name':name,'pass':True,'detail':detail}
    except Exception as e:
        row={'name':name,'pass':False,'type':type(e).__name__,'detail':str(e),'traceback':traceback.format_exc()}
    RESULTS.append(row)
    save(ROOT/'results/validation_progress.json',{'checks':RESULTS,'comparisons':COMPARE})
    return row['pass']

def cmp(name,a,b):
    row={'name':name,**comparison(a,b)};COMPARE.append(row)
    if row['violations']:raise AssertionError(str(row))

def expected(code,fn):
    try:fn()
    except HierarchyError as e:
        assert e.code==code,(e.code,code);return {'caught':code}
    raise AssertionError('Fault not detected: '+code)

def graph_features(seed,n):
    ws=old.worlds(seed,3,n);x,ix,v,y=old.batch(ws)
    xx,specs=prepare_worlds(ws);assert torch.equal(x,xx)
    p=compile_plan(specs);mask=graph_mask(p)
    for bi,s in enumerate(specs):
        for qi,keys in enumerate(s.rows()):
            assert list(keys)==ix[bi,qi][v[bi,qi]].tolist()
            assert int(mask[bi,qi].sum())==len(keys)
    raw=p.to_bytes();restored=AttentionPlan.from_bytes(raw)
    assert restored.to_bytes()==raw and restored.identity==p.identity
    # Different evidence with identical topology does not change the plan.
    changed=copy.deepcopy(ws);changed[0]['progress'][0]^=1
    _,ss=prepare_worlds(changed);assert ss==specs
    return {'tasks':n,'worlds':len(ws),'rows_checked':p.positions*3,'exact_features':True}

def numerical(seed,n,dtype):
    torch.manual_seed(seed);ws=old.worlds(seed,2,n);_,ix,va,_=old.batch(ws)
    p=compile_plan([Hierarchy.from_dependencies(w['deps']) for w in ws])
    q,k,v=[torch.randn(2,2,p.positions,16,dtype=dtype,requires_grad=True) for _ in range(3)]
    a=packed_attention(q,k,v,p);b=masked_reference(q,k,v,p);c=old.sparse_attention(q,k,v,ix,va)
    cmp('attention_packed_dense',a,b);cmp('attention_packed_old',a,c)
    upstream=torch.randn_like(a)
    ga=torch.autograd.grad((a*upstream).sum(),(q,k,v),retain_graph=True)
    gb=torch.autograd.grad((b*upstream).sum(),(q,k,v),retain_graph=True)
    for kind,x,y in zip('qkv',ga,gb):cmp('gradient_'+kind,x,y)
    if dtype==torch.float64:
        out=np.zeros(a.shape,np.float64);qq,kk,vv=[t.detach().numpy() for t in (q,k,v)]
        for bi,s in enumerate(p.specs):
            for qi,keys in enumerate(s.rows()):
                for head in range(2):
                    ss=qq[bi,head,qi]@kk[bi,head,list(keys)].T/math.sqrt(16);pp=np.exp(ss-ss.max());pp/=pp.sum()
                    out[bi,head,qi]=pp@vv[bi,head,list(keys)]
        cmp('independent_numpy',a,out)
    return {'tasks':n,'dtype':str(dtype)}

def full_gradient(seed,dtype):
    torch.manual_seed(seed);ws=old.worlds(seed,2,8);x,ix,va,y=old.batch(ws);x=x.to(dtype)
    p=compile_plan([Hierarchy.from_dependencies(w['deps']) for w in ws])
    a=MaintenanceReader().to(dtype);b=old.Reader().to(dtype);b.load_state_dict(a.state_dict())
    before=model_sha(a);xx=x.clone().requires_grad_();yy=x.clone().requires_grad_()
    oa=a(xx,p);ob=b(yy,ix,va,8,'hsa');cmp('full_logits',oa,ob)
    up=torch.randn_like(oa)
    (oa*up).sum().backward();(ob*up).sum().backward()
    cmp('full_input_gradient',xx.grad,yy.grad)
    for name,param in a.named_parameters():cmp('full_parameter_gradient:'+name,param.grad,dict(b.named_parameters())[name].grad)
    assert model_sha(a)==before
    return {'parameters_checked':sum(1 for _ in a.parameters()),'dtype':str(dtype),'weights_unchanged':True}

def cache_test():
    ws=old.worlds(190,3,8);cache=PlanCache(2);ss=[(Hierarchy.from_dependencies(w['deps']),) for w in ws]
    p=cache.get(ss[0]);assert cache.get(ss[0]) is p
    cache.get(ss[1]);cache.get(ss[2]);assert len(cache)==2 and cache.evictions==1
    p2=cache.get(ss[0]);assert p2 is not p and p2.identity==p.identity
    return {'hits':cache.hits,'misses':cache.misses,'evictions':cache.evictions}

def degenerate_graph():
    for deps,width in [([[]],1),([[],[]],1),([[1],[0]],2),([[],[0],[1,0]],10)]:
        s=Hierarchy.from_dependencies(deps,region_width=width);p=compile_plan([s]);p.validate_tensors()
        q,k,v=[torch.randn(1,2,p.positions,4,dtype=torch.float64) for _ in range(3)]
        cmp('tiny_variable_dependency_graph',packed_attention(q,k,v,p),masked_reference(q,k,v,p))
    return {'layouts':4,'feature_adapter_scope':'separate; SH01 feature adapter still requires two dependencies'}

def noninterference():
    s=Hierarchy.from_dependencies(old.worlds(803,1,16)[0]['deps']);p=compile_plan([s]);q,k,v=[torch.randn(1,2,p.positions,16,dtype=torch.float64) for _ in range(3)]
    y=packed_attention(q,k,v,p);allowed=set(s.rows()[0]);off=next(j for j in range(p.positions) if j not in allowed)
    kk=k.clone();vv=v.clone();kk[:,:,off]+=100;vv[:,:,off]-=100
    z=packed_attention(q,kk,vv,p);assert torch.equal(y[:,:,0],z[:,:,0])
    return {'query':0,'forbidden_key':off,'scope':'one attention layer, not all indirect multihop model paths'}

def shape_trace():
    from torch.utils._python_dispatch import TorchDispatchMode
    s=Hierarchy.from_dependencies(old.worlds(806,1,32)[0]['deps']);p=compile_plan([s]);T=p.positions;shapes=[]
    class Trace(TorchDispatchMode):
        def __torch_dispatch__(self,func,types,args=(),kwargs=None):
            out=func(*args,**(kwargs or {}))
            def visit(z):
                if isinstance(z,torch.Tensor):shapes.append({'op':str(func),'shape':list(z.shape)})
                elif isinstance(z,(list,tuple)):
                    for a in z:visit(a)
            visit(out);return out
    q,k,v=[torch.randn(1,2,T,16) for _ in range(3)]
    with Trace():packed_attention(q,k,v,p)
    bad=[z for z in shapes if any(z['shape'][i:i+2]==[T,T] for i in range(len(z['shape'])-1))]
    assert not bad
    save(ROOT/'results/native_shape_trace.json',{'positions':T,'operations':shapes,'full_TT_observed':False,'limitation':'dispatcher-visible tensors; not all allocations internal to native kernels'})
    return {'tensor_outputs':len(shapes),'full_TT_observed':False}

def faults():
    check('fault_duplicate_dependency',lambda:expected('DUPLICATE_DEPENDENCY',lambda:Hierarchy.from_dependencies([[1,1],[0]])))
    check('fault_self_dependency',lambda:expected('INVALID_DEPENDENCY',lambda:Hierarchy.from_dependencies([[0]])))
    check('fault_out_of_range',lambda:expected('INVALID_DEPENDENCY',lambda:Hierarchy.from_dependencies([[5],[]])))
    check('fault_empty_graph',lambda:expected('INVALID_LAYOUT',lambda:Hierarchy.from_dependencies([])))
    check('fault_region_width',lambda:expected('INVALID_LAYOUT',lambda:Hierarchy.from_dependencies([[]],region_width=0)))
    a=Hierarchy.from_dependencies([[],[]],scope='a');b=Hierarchy.from_dependencies([[],[]],scope='b')
    check('fault_mixed_scope',lambda:expected('MIXED_BATCH_LAYOUT_OR_SCOPE',lambda:compile_plan([a,b])))
    p=compile_plan([a]);raw=p.to_bytes();env=json.loads(raw);env['payload']['specs'][0]['scope']='tamper'
    check('fault_corrupt_plan',lambda:expected('CORRUPT_PLAN',lambda:AttentionPlan.from_bytes(canonical(env))))
    check('fault_stale_plan',lambda:expected('STALE_TOPOLOGY_PLAN',lambda:p.assert_matches([Hierarchy.from_dependencies([[1],[]],scope='a')])))
    pp=AttentionPlan.from_bytes(raw);pp.buckets[0].indices[0,0,0]=pp.positions-1
    check('fault_mutated_tensor',lambda:expected('MUTATED_PLAN_TENSORS',pp.validate_tensors))
    w=old.worlds(400,1,8)[0];xx,ss=prepare_worlds([w]);p=compile_plan(ss);m=MaintenanceReader()
    check('fault_wrong_feature_width',lambda:expected('INVALID_FEATURE_SHAPE',lambda:m(xx[:,:,:36],p)))
    xx=xx.clone();xx[0,0,0]=float('nan')
    check('fault_nonfinite_features',lambda:expected('NONFINITE_FEATURE',lambda:m(xx,p,checked=True)))
    def mut():
        mm=MaintenanceReader();before=model_sha(mm)
        with torch.no_grad():mm.head.bias[0]+=1
        assert before!=model_sha(mm)
        return {'hash_mismatch_detected':True}
    check('fault_model_mutation',mut)

if __name__=='__main__':
    setup();started=time.perf_counter()
    for seed in range(12):
        for n in [3,8,16,32]:check(f'graph_features_{seed}_{n}',lambda seed=seed,n=n:graph_features(920000+seed,n))
    for dtype in [torch.float32,torch.float64]:
        for seed in range(3):
            for n in [3,8,16,32]:check(f'numerical_{dtype}_{seed}_{n}',lambda seed=seed,n=n,dtype=dtype:numerical(930000+seed,n,dtype))
        for seed in [940001,940002]:check(f'full_grad_{dtype}_{seed}',lambda seed=seed,dtype=dtype:full_gradient(seed,dtype))
    check('bounded_cache',cache_test);check('degenerate_topology',degenerate_graph);check('forbidden_connection',noninterference);check('native_tensor_shapes',shape_trace);faults()
    summary={'runtime':runtime(),'checks':RESULTS,'comparisons':COMPARE,'passed':sum(r['pass'] for r in RESULTS),'total':len(RESULTS),'scalar_comparisons':sum(r['scalars'] for r in COMPARE),'violations':sum(r['violations'] for r in COMPARE),'optimizer_applications':0,'elapsed_seconds':time.perf_counter()-started}
    save(ROOT/'results/validation.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['checks','comparisons','runtime']},indent=2),flush=True)
    if summary['passed']!=summary['total']:print(json.dumps([r for r in RESULTS if not r['pass']],indent=2));sys.exit(1)
