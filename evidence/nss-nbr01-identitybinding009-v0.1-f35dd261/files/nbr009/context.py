"""Conditional Stage CUE: additional independent observations, not a new model.

This numerical membership diagnostic does not retrofit 32D features into the old
reader. Reference views are established before queries. No target room, identity
index or membership bit is an input to matching. Equal-size single and duplicate
controls are separate information comparisons, not equal-information claims.
"""
from .common import *
from nbr008.resolver import features

METHODS=('single16','duplicate32','independent32','single32')
FAMILIES=('known_clean','known_q05','known_q20','novel','near_novel','second_missing','second_conflicting','second_shuffled','both_common_noise','novel_both_near','identical_known','identical_novel')

def sample(seed,b,family):
    rng=np.random.default_rng(seed);n=16;r=np.arange(b)
    a=data.normalize(rng.normal(size=(b,n,16))).astype(np.float32)
    z=data.normalize(rng.normal(size=(b,n,16))).astype(np.float32)
    big=(np.sqrt(2)*data.normalize(rng.normal(size=(b,n,32)))).astype(np.float32)
    idx=rng.integers(0,n,b);other=(idx+1+rng.integers(0,n-1,b))%n
    x=a[r,idx].copy();y=z[r,idx].copy();w=big[r,idx].copy()
    primary_noise=.2 if family in ('known_q20','second_missing','second_conflicting','second_shuffled','both_common_noise') else .05 if family=='known_q05' else 0.
    nx=rng.normal(size=x.shape).astype(np.float32);ny=rng.normal(size=y.shape).astype(np.float32);nw=rng.normal(size=w.shape).astype(np.float32)
    if primary_noise:
        x=data.normalize(x+primary_noise*nx).astype(np.float32)
        # Added independent cue stays mildly disturbed, explicitly better information.
        y=data.normalize(y+.05*ny).astype(np.float32)
        w=(np.sqrt(2)*data.normalize(w+primary_noise*nw)).astype(np.float32)
    known=family not in ('novel','near_novel','novel_both_near','identical_novel')
    if family=='novel':
        x=data.normalize(rng.normal(size=x.shape)).astype(np.float32);y=data.normalize(rng.normal(size=y.shape)).astype(np.float32);w=(np.sqrt(2)*data.normalize(rng.normal(size=w.shape))).astype(np.float32)
    if family in ('near_novel','novel_both_near'):
        x=data.normalize(a[r,idx]+.01*nx).astype(np.float32)
        y=data.normalize(z[r,idx]+.01*ny).astype(np.float32) if family=='novel_both_near' else data.normalize(rng.normal(size=y.shape)).astype(np.float32)
        # Entire equal-size single observation is close in this stress; dual has
        # independent origin information only in its additional observed channel.
        w=(np.sqrt(2)*data.normalize(big[r,idx]+.01*nw)).astype(np.float32)
    if family=='second_missing':y[:]=0
    if family=='second_conflicting':y=z[r,other].copy()
    if family=='second_shuffled':y=np.roll(y,1,axis=0)
    if family=='both_common_noise':
        x=data.normalize(a[r,idx]+.2*nx).astype(np.float32);y=data.normalize(z[r,idx]+.2*nx).astype(np.float32)
    # Identical known/novel family calls must use SAME seed, hence same observables.
    return {'a':a,'z':z,'big':big,'x':x,'y':y,'w':w,'target':np.where(known,idx,16).astype(np.int64),'origin_known':np.full(b,known,bool)}

def evidence(p,method):
    if method=='single16':return p['x'],p['a']
    if method=='duplicate32':return np.concatenate([p['x'],p['x']],-1),np.concatenate([p['a'],p['a']],-1)
    if method=='independent32':return np.concatenate([p['x'],p['y']],-1),np.concatenate([p['a'],p['z']],-1)
    return p['w'],p['big']

def decide(p,method,cfg):
    x,book=evidence(p,method);scale=x.shape[-1]/16
    ds=((x[:,None,:]-book)**2).sum(-1)/scale
    order=np.argsort(ds,axis=-1);r=np.arange(len(x));best=order[:,0]
    dist=ds[r,best];margin=ds[r,order[:,1]]-dist
    accept=(dist<=cfg['distance'])&(margin>=cfg['margin'])
    return np.where(accept,best,16),dist,margin

def calibrate(pair,path,b=1024):
    rows={};cut={};arrays={}
    for mi,m in enumerate(METHODS):
        blocks=[]
        for j,f in enumerate(('known_clean','known_q05','known_q20','novel')):
            p=sample(71950000+pair*1000+j,b,f);pred,d,margin=decide(p,m,{'distance':100,'margin':-1})
            blocks.append((p['target'],d,margin,pred));arrays[m+'_'+f+'_target']=p['target'];arrays[m+'_'+f+'_dist']=d;arrays[m+'_'+f+'_margin']=margin;arrays[m+'_'+f+'_nearest']=pred
        y,d,mg,idx=[np.concatenate([t[k] for t in blocks]) for k in range(4)]
        candidates=[]
        for tau in np.linspace(.1,1.4,66):
            for gap in (0.,.01,.04,.08,.16):
                ac=(d<=tau)&(mg>=gap);false=np.mean(ac[y==16]);correct=np.mean((idx[y!=16]==y[y!=16])&ac[y!=16])
                if false<=.005:candidates.append((correct,-false,-tau,-gap,tau,gap))
        best=max(candidates);cut[m]={'distance':float(best[-2]),'margin':float(best[-1])};rows[m]={'known_correct':best[0],'false_accept':-best[1]}
    info={'pair':pair,'labelled_examples_unique':b*4,'feature_evaluations':b*4*4,'grid':{'distance':'linspace .1..1.4,66','margin':[0,.01,.04,.08,.16]},'cuts':cut,'development_results':rows,'disjoint_from_main':True}
    save_arrays(path,arrays,info);return cut

def run(pair,path,b=1024):
    cfg=json.loads((ROOT/'checkpoints'/f'cue_calibration_{pair}.json').read_text())['cuts']
    arrays={};entries=[]
    for j,f in enumerate(FAMILIES):
        seed=72950000+pair*1000+(100 if f.startswith('identical_') else j)
        p=sample(seed,b,f)
        for k,v in p.items():arrays[f+'__'+k]=v
        for m in METHODS:
            pred,d,g=decide(p,m,cfg[m]);arrays[f+'__pred_'+m]=pred;arrays[f+'__dist_'+m]=d;arrays[f+'__margin_'+m]=g
        entries.append({'family':f,'seed':seed,'batch':b})
    save_arrays(path,arrays,{'stage':'CUE','pair':pair,'configs':entries,'cuts':cfg,'status':'conditional diagnostic locked before main; extra information not equal evidence','timestamp':utc()})
