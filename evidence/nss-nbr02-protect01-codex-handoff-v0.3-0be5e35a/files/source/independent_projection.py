"""Independent NumPy scalar certificate and margin-derivative checker.
Imports neither producer, controller, autograd nor production projection solver.
"""
import numpy as np

def margin_reference(v,codes,y):
    from reference_numeric import split,math_reference
    W,U,b,V,a=split(np.asarray(v,dtype='f8'));ref=math_reference(v,codes)
    hs=ref['h'];q=np.array([1.,-1.]) if y==0 else np.array([-1.,1.]);adj=V.T.dot(q)
    dw=np.zeros_like(W);du=np.zeros_like(U);db=np.zeros(16)
    for t in range(len(codes)-1,-1,-1):
        dz=adj*(1-hs[t+1]**2);dw[:,codes[t]]+=dz;du+=np.outer(dz,hs[t]);db+=dz;adj=U.T.dot(dz)
    return np.concatenate((dw.ravel(),du.ravel(),db,np.outer(q,hs[-1]).ravel(),q)),ref

def validate_certificate(a):
    A=np.asarray(a['A'],dtype='f8');r=np.sqrt(np.sum(A*A,axis=1));C=np.zeros_like(A)
    for j in range(8):
        if r[j]!=0:C[j]=A[j]/r[j]
    assert np.allclose(C,a['C'],atol=1e-15,rtol=1e-15),'QP_ROW_NORMALIZATION'
    assert np.allclose(r,a['scales'],atol=1e-15,rtol=1e-15),'QP_ROW_SCALE'
    target=np.asarray(a['d2'],dtype='f8');d=np.asarray(a['d'],dtype='f8');lam=np.asarray(a['lambda'],dtype='f8');b=max(1.,np.linalg.norm(target));row=C.dot(d)
    assert np.isfinite(d).all() and np.isfinite(lam).all(),'QP_NONFINITE'
    assert np.min(row)>=-1e-9*b,'QP_PRIMAL'
    assert np.min(lam)>=-1e-9*b,'QP_DUAL'
    assert np.max(np.abs(d-target-C.T.dot(lam)))<=1e-9*b,'QP_STATIONARITY'
    assert np.max(np.abs(lam*row))<=1e-9*b*b,'QP_COMPLEMENTARITY'
    assert np.linalg.norm(d)<=np.linalg.norm(target)+1e-8*b,'QP_NORM'
    assert np.allclose(row,a['residual'],rtol=1e-12,atol=1e-12),'QP_STORED_RESIDUAL'
    if a['supports'].shape[0]:
        assert a['supports'].shape==(256,16),'QP_SUPPORT_COUNT'
        expected=[]
        for n in range(9):
            # Independent mask enumeration then cardinality/lexicographic ordering.
            masks=[m for m in range(256) if m.bit_count()==n]
            masks.sort(key=lambda m:tuple(i for i in range(8) if m&(1<<i)));expected.extend(masks)
        assert list(a['supports'][:,0].astype(int))==expected,'QP_SUPPORT_ORDER'
        feasible=a['supports'][a['supports'][:,2]==1]
        assert len(feasible)>0
        chosen=None
        for rr in feasible:
            if chosen is None or rr[3]<chosen[3]-1e-12*b*b:chosen=rr
        assert int(a['selected'][0])==int(chosen[0]),'QP_OBJECTIVE_SELECTION'
        obj=.5*np.sum((d-target)**2)
        assert abs(obj-a['selected'][1])<=1e-12*b*b,'QP_OBJECTIVE'
    else:assert not np.any(target) and not np.any(d),'QP_ZERO_SPECIAL_CASE'
    return {'min_linear':float(row.min()),'stationarity':float(np.max(np.abs(d-target-C.T@lam))),'objective':float(.5*np.sum((d-target)**2))}

def validate_application(a):
    pre=np.asarray(a['params'],dtype='f4');th=pre.astype('f8');dp=a['d'];C=a['C'];d2=a['d2']
    p=(th+dp).astype('f4');b2=(pre-(-d2).astype('f4')).astype('f4');dd2=b2.astype('f8')-th;ddp=p.astype('f8')-th
    for key,ref in [('thetaP',p),('thetaB2',b2),('deltaP',ddp),('delta2',dd2)]:assert a[key].tobytes()==ref.tobytes(),'APPLIED_BYTES:'+key
    e=ddp-dp;bound=2e-6*max(1.,np.linalg.norm(th),np.linalg.norm(dp));assert np.linalg.norm(e)<=bound
    assert np.all(C@ddp>=-1e-9*max(1.,np.linalg.norm(d2))-np.abs(C)@np.abs(e)),'CAST_PRIMAL'
    n=np.linalg.norm(ddp);n2=np.linalg.norm(dd2);s=np.zeros(674) if not n or not n2 else dd2*(n/n2);sp=(th+s).astype('f4');dds=sp.astype('f8')-th;es=dds-s
    for key,ref in [('thetaS',sp),('deltaS',dds),('s64',s),('eP',e),('eS',es)]:assert a[key].tobytes()==ref.tobytes(),'APPLIED_BYTES:'+key
    miss=abs(np.linalg.norm(dds)-n);assert miss<=np.linalg.norm(es)+1e-10*max(1.,n),'ACTUAL_NORM_TRIANGLE'
    assert n==0 or miss/n<=1e-4,'ACTUAL_NORM_COMPARABILITY'
    return {'normP':float(n),'normS':float(np.linalg.norm(dds)),'relative_mismatch':float(miss/n if n else 0.),'cast_norm':float(np.linalg.norm(e))}
