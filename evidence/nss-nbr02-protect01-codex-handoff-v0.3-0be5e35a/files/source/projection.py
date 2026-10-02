"""Frozen PROTECT01 eight-row Euclidean projection and single-cast update.
Never consumes a task score. Rank thresholds and KKT tolerance are protocol v0.2.
"""
import itertools
import numpy as np

class ProjectionError(RuntimeError):pass

def normalize(A):
    A=np.asarray(A,dtype=np.float64)
    if A.shape!=(8,674) or not np.isfinite(A).all():raise ProjectionError('BAD_OLD_JACOBIAN')
    r=np.linalg.norm(A,axis=1);C=np.zeros_like(A);nz=r!=0;C[nz]=A[nz]/r[nz,None]
    return C,r

def certificate(C,d2,d,lam):
    b=max(1.,float(np.linalg.norm(d2)));cd=C@d
    v=np.array([max(0.,float((-cd).max())),max(0.,float((-lam).max())),
                float(np.max(np.abs(d-d2-C.T@lam))),float(np.max(np.abs(lam*cd))),
                float(np.linalg.norm(d))],dtype='f8')
    ok=bool(v[0]<=1e-9*b and v[1]<=1e-9*b and v[2]<=1e-9*b and v[3]<=1e-9*b*b and v[4]<=np.linalg.norm(d2)+1e-8*b)
    return v,cd,ok

def solve(A,d2,charge=lambda *x:None):
    charge('qp');d2=np.asarray(d2,dtype='f8')
    if d2.shape!=(674,) or not np.isfinite(d2).all():raise ProjectionError('BAD_QP_TARGET')
    C,r=normalize(A);b=max(1.,float(np.linalg.norm(d2)))
    charge('svd');fulls=np.linalg.svd(C,compute_uv=False)
    rows=[];best=None
    if np.array_equal(d2,np.zeros(674)):
        return {'C':C,'scales':r,'d':d2.copy(),'lambda':np.zeros(8),'residual':np.zeros(8),'full_singular_values':fulls,
                'supports':np.zeros((0,16)),'selected':np.array([0,0,0,0,0,0,0],dtype='f8')}
    for size in range(9):
        for ids in itertools.combinations(range(8),size):
            charge('support');mask=sum(1<<i for i in ids);lam=np.zeros(8);ss=np.zeros(8);rank=0
            if size:
                charge('svd');U,s,Vh=np.linalg.svd(C[list(ids)],full_matrices=False);ss[:size]=s
                rank=int(np.sum(s>1e-12*max(1.,float(s[0]))))
                if rank<size:
                    rows.append([mask,rank,-1,0,0,0,0,0,*ss]);continue
                t=Vh@d2;d=d2-Vh.T@t;lam[list(ids)]=-U@(t/s)
            else:d=d2.copy()
            v,cd,ok=certificate(C,d2,d,lam);obj=.5*float(np.dot(d-d2,d-d2))
            rows.append([mask,rank,int(ok),obj,v[0],v[1],v[2],v[3],*ss])
            if ok and (best is None or obj<best[0]-1e-12*b*b):best=(obj,mask,d.copy(),lam.copy(),v.copy(),cd.copy())
    if best is None:
        # Carry candidate table with the raised exception for durable failure diagnostics.
        e=ProjectionError('QP_NO_CERTIFIED_SOLUTION');e.evidence={'A':np.asarray(A),'C':C,'scales':r,'d2':d2,'supports':np.asarray(rows),'full_singular_values':fulls};raise e
    obj,mask,d,lam,v,cd=best
    return {'C':C,'scales':r,'d':d,'lambda':lam,'residual':cd,'full_singular_values':fulls,
            'supports':np.asarray(rows,dtype='f8'),'selected':np.r_[mask,obj,v]}

def apply_pair(pre,d2,clipped_step,solution):
    """B2 uses inherited float32 subtract; P/S each use one float64-add/float32 cast."""
    pre=np.asarray(pre,dtype='f4');th0=pre.astype('f8');C=solution['C'];dp=solution['d'];b=max(1.,float(np.linalg.norm(d2)))
    b2=np.subtract(pre,np.asarray(clipped_step,dtype='f4'),dtype=np.float32);delta2=b2.astype('f8')-th0
    pp=(th0+dp).astype('f4');deltaP=pp.astype('f8')-th0;ep=deltaP-dp
    bound=2e-6*max(1.,float(np.linalg.norm(th0)),float(np.linalg.norm(dp)))
    if np.linalg.norm(ep)>bound:raise ProjectionError('P_CAST_ENVELOPE')
    linear=C@deltaP;allowance=1e-9*b+np.abs(C)@np.abs(ep)
    if np.any(linear < -allowance):raise ProjectionError('P_ACTUAL_PRIMAL')
    np_=float(np.linalg.norm(deltaP));n2=float(np.linalg.norm(delta2))
    if n2==0 and np_>1e-8*b:raise ProjectionError('B2_ZERO_NONZERO_P')
    sv=np.zeros(674) if np_==0 or n2==0 else delta2*(np_/n2)
    sp=(th0+sv).astype('f4');deltaS=sp.astype('f8')-th0;es=deltaS-sv;ns=float(np.linalg.norm(deltaS));mismatch=ns-np_
    if np.linalg.norm(es)>2e-6*max(1.,float(np.linalg.norm(th0)),float(np.linalg.norm(sv))):raise ProjectionError('S_CAST_ENVELOPE')
    if abs(mismatch)>np.linalg.norm(es)+1e-10*max(1.,np_):raise ProjectionError('S_TRIANGLE_NORM')
    rel=abs(mismatch)/np_ if np_ else 0.
    if np_ and rel>1e-4:raise ProjectionError('S_NORM_COMPARABILITY')
    return {'thetaP':pp,'thetaS':sp,'thetaB2':b2,'deltaP':deltaP,'deltaS':deltaS,'delta2':delta2,'eP':ep,'eS':es,'s64':sv,
            'linear_actual':linear,'linear_allowance':allowance,'norm_metrics':np.array([np_,n2,ns,mismatch,rel,float(np.linalg.norm(ep)),float(np.linalg.norm(es))],dtype='f8')}
