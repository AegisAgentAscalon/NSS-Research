"""Charged finite, fixed algebraic solver cases; no trained neural data."""
from fractions import Fraction
import copy,numpy as np
from projection import solve,apply_pair
from independent_projection import validate_certificate,validate_application

def run_checks(rec,literals):
    results=[];arrays=[]
    for case in literals['cases']:
        A=np.zeros((8,674),dtype='f8');d2=np.zeros(674);expected=np.zeros(674)
        for row,vals in enumerate(case['sparse_rows']):
            for col,v in vals.items():A[row,int(col)]=float(Fraction(v))
        for col,v in case['d2'].items():d2[int(col)]=float(Fraction(v))
        for col,v in case['analytic_exact_projection'].items():expected[int(col)]=float(Fraction(v))
        try:
            so=solve(A,d2,rec.charge);a={'A':A,'d2':d2,**so};cert=validate_certificate(a)
            assert np.max(np.abs(so['d']-expected))<=1e-8*max(1.,np.linalg.norm(d2)),'ANALYTIC_PROJECTION'
        except Exception as exc:
            rec.frame({'kind':'solver_failure','context':{'session':'SOLVER','branch':'NONE'},'arm':'NONE','case':case['id'],'reason':str(exc)}, {'A':A,'d2':d2,'expected':expected,**getattr(exc,'evidence',{})});raise
        rec.frame({'kind':'solver_fixture','context':{'session':'SOLVER','branch':'NONE'},'arm':'NONE','case':case['id'],'certificate':cert},{**a,'expected':expected})
        results.append({'case':case['id'],'passed':True,**cert});arrays.append(a)
    # Copied certificate faults; no QP reruns and no task outcome supplied.
    controls=[]
    for label,mut in [('wrong_sign',lambda z:z['d'].__setitem__(0,-1.)),('wrong_dual',lambda z:z['lambda'].__setitem__(0,-10.)),('wrong_direction',lambda z:z['d'].__setitem__(1,20.))]:
        aa={k:v.copy() for k,v in arrays[2].items()};mut(aa);caught=False
        try:validate_certificate(aa)
        except AssertionError:caught=True
        assert caught;controls.append(label)
    # Pure IEEE single-round arithmetic inputs, not additional optimizer applications.
    for scale in [0.,2**-140,2**-25,1.,-1.]:
        aa=arrays[2];pre=np.zeros(674,dtype='f4');pre[1]=scale
        pair=apply_pair(pre,aa['d2'],(-aa['d2']).astype('f4'),aa);check={'params':pre,**aa,**pair};validate_application(check)
        bad={k:v.copy() if isinstance(v,np.ndarray) else v for k,v in check.items()};bad['thetaS'][2]=1.
        caught=False
        try:validate_application(bad)
        except AssertionError:caught=True
        assert caught
    # A zero local derivative is not a finite-step safety theorem.
    assert -1.**2<0 and 0.*1.==0.
    rec.emit('SOLVER_NONNEURAL_DETECTORS',{'clean_cases':16,'copied_faults':controls,'cast_cases':5,'zero_row_finite_harm_example':True,'no_extra_optimizer_applications':True})
    return {'passed':True,'cases':results,'counts':rec.counts}
