from pathlib import Path
import sys,copy,json,time,traceback
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from support import *
from sc01 import *
from sh01_common import worlds,oracle
from nss_hsa import prepare_worlds,PlanCache
from nss_hsa.records import compile_features

def main():
    setup();start=time.perf_counter();checks=[];comparisons=[]
    def check(name,fn):
        try:detail=fn();checks.append({'name':name,'passed':True,'detail':detail})
        except Exception:
            checks.append({'name':name,'passed':False,'traceback':traceback.format_exc()})
        save(ROOT/'results'/'preflight_progress.json',{'checks':checks,'comparisons':comparisons})
    def requires_fault(code,fn):
        try:fn()
        except SCError as e:assert e.code==code,(e.code,code);return e.code
        raise AssertionError('Fault escaped '+code)
    m,mid=load(8801)
    ws={n:worlds(991001+n,4,n)for n in [8,32,128]}
    for n in [8,32,128]:
        for wi,w in enumerate(ws[n]):
            def fn(w=w,n=n,wi=wi):
                x,specs=prepare_worlds([w]);p=PlanCache().get(specs)
                with torch.no_grad():full=m(x,p).numpy()[0]
                targets=[0,n//2,n-1];sp=make_plan(specs[0],targets)
                with torch.no_grad():y=slice_forward(m,x[0,list(sp.input_ids)],sp).numpy()
                c=compare(y,full[sp.targets,:]);comparisons.append(c);assert c['violations']==0
                assert np.array_equal(y.argmax(-1),full[list(sp.targets)].argmax(-1))
                graph=specs[0].rows()
                for st in sp.stages:
                    assert all(set(graph[q]).issubset(st.inputs)for q in st.outputs)
                return {'records':sp.record_count,'full':p.positions,'targets':list(sp.targets),**c}
            check(f'float32_exact_closure_{n}_{wi}',fn)
    m64=copy.deepcopy(m).double()
    for wi,w in enumerate(ws[8]):
        def fn(w=w):
            x,specs=prepare_worlds([w]);p=PlanCache().get(specs);x=x.double();sp=make_plan(specs[0],[0,3])
            with torch.no_grad():f=m64(x,p,backend='masked_reference').numpy()[0];y=slice_forward(m64,x[0,list(sp.input_ids)],sp).numpy()
            c=compare(y,f[list(sp.targets)]);comparisons.append(c);assert c['violations']==0;return c
        check(f'float64_reference_{wi}',fn)
    for policy in ['index','cache','segment']:
        def lifecycle(policy=policy):
            st=Store(ws[8][0]);a=Workspace(st,mid,policy,40);a.job('J',list(range(8)),m,limit_tasks=2)
            raw=a.snapshot();b=Workspace.restore(raw,st,mid)
            st.mutate({'field':'progress','task':int(st.world['deps'][2][0])})
            b.job('J',list(range(8)),m)
            x,s=prepare_worlds([st.world]);p=PlanCache().get(s)
            with torch.no_grad():f=m(x,p).numpy()[0]
            ys=np.array([b.receipts[f'J:{i}']['logits']for i in range(8)])
            c=compare(ys,f);comparisons.append(c);assert c['violations']==0
            before=b.stats['emitted_receipts'];b.job('J',list(range(8)),m);assert b.stats['emitted_receipts']==before
            assert b.stats['peak_active_rows']<=40
            return {'receipts':len(b.receipts),'emitted':b.stats['emitted_receipts'],**c}
        check('lifecycle_'+policy,lifecycle)
        def pressure(policy=policy):
            a=Workspace(Store(ws[8][0]),mid,policy,16);a.job('small',[0,1],m)
            assert len(a.receipts)==0 and a.stats['budget_deferrals']==2
            return {'explicit_deferrals':2}
        check('bounded_deferral_'+policy,pressure)
    st=Store(ws[8][1]);base=Workspace(st,mid,'segment',40);base.job('J',[0,1],m);raw=base.snapshot()
    def corrupt():
        d=json.loads(raw);d['payload']['cursor']+=1
        return requires_fault('CORRUPT_CHECKPOINT',lambda:Workspace.restore(canonical(d),st,mid))
    check('fault_corrupt_checksum',corrupt)
    check('fault_model_revision',lambda:requires_fault('WRONG_MODEL_REVISION',lambda:Workspace.restore(raw,st,'bad-model')))
    check('fault_scope',lambda:requires_fault('WRONG_STORE_OR_SCOPE',lambda:Workspace.restore(raw,Store(ws[8][1],'other-scope'),mid)))
    check('fault_malformed',lambda:requires_fault('MALFORMED_CHECKPOINT',lambda:Workspace.restore(b'{',st,mid)))
    check('fault_job_identity',lambda:requires_fault('JOB_ID_COLLISION',lambda:base.job('J',[2,3],m)))
    check('fault_duplicate_task',lambda:requires_fault('DUPLICATE_JOB_TASK',lambda:base.job('other',[1,1],m)))
    check('fault_bad_target',lambda:requires_fault('INVALID_TARGETS',lambda:base.job('bad',[100],m)))
    def event_gap():
        a=Workspace(Store(ws[8][1]),mid,'segment',40);a.job('a',[0],m);a.store.mutate({'field':'freeze'});a.store.events=[]
        return requires_fault('MISSING_REVISION_EVENT',lambda:a.job('b',[0],m))
    check('fault_missing_revision_event',event_gap)
    def missing_edge():
        spec=st.spec;graph=spec.rows();return requires_fault('MISSING_GRAPH_DEPENDENCY',lambda:build_stage(graph,(0,),(0,)))
    check('fault_missing_dependency',missing_edge)
    def nonfinite():
        p=make_plan(st.spec,[0]);x=compile_features(st.world,st.spec)[list(p.input_ids)];x[0,0]=float('nan')
        return requires_fault('NONFINITE_INPUT',lambda:slice_forward(m,x,p))
    check('fault_nonfinite',nonfinite)
    def isolation():
        other=Workspace.restore(raw,st,mid);other.jobs['J']['tasks'][0]=7
        assert base.jobs['J']['tasks'][0]==0
        clone=Store.from_dict(st.to_dict());clone.mutate({'field':'freeze'});assert st.world['freeze']!=clone.world['freeze']
        return 'isolated'
    check('snapshot_isolation',isolation)
    def deps_revision():
        a=Workspace(Store(ws[8][2]),mid,'segment',40);a.job('j',[0,1],m)
        a.store.mutate({'field':'dependency','task':0,'value':[6,7]});a.job('k',[0,1],m)
        x,s=prepare_worlds([a.store.world]);p=PlanCache().get(s)
        with torch.no_grad():f=m(x,p).numpy()[0]
        yy=np.array([a.receipts[f'k:{i}']['logits']for i in [0,1]])
        c=compare(yy,f[:2]);comparisons.append(c);assert c['violations']==0;return c
    check('topology_revision_invalidation',deps_revision)
    out={'status':'PASS'if all(c['passed']for c in checks)else'FAIL','checks':checks,'comparisons':comparisons,
         'seconds':time.perf_counter()-start,'runtime':runtime(),'optimizer_applications':0}
    save(ROOT/'results'/'preflight.json',out)
    print(json.dumps({'status':out['status'],'checks':len(checks),'failed':[c['name']for c in checks if not c['passed']],'seconds':out['seconds']},indent=2))
    return 0 if out['status']=='PASS'else 1
if __name__=='__main__':raise SystemExit(main())
