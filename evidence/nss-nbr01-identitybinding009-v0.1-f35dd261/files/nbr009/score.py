"""Independent NumPy outcome scorer. No neural predictions are regenerated here.
Graph truth derives from supplied source graph/events, never the candidate state.
Stored logical relations are decoded separately to detect hidden cross-owner damage.
"""
import json
from pathlib import Path
import numpy as np
N=16

def follow(parent,start):
    out=np.full(len(start),N,np.int64)
    for i,s in enumerate(start):
        seen=set();cur=int(s)
        for _ in range(N+1):
            if cur==N or cur in seen:break
            seen.add(cur);nxt=int(parent[i,cur])
            if nxt==cur:out[i]=cur;break
            cur=nxt
    return out

def decode_store(own,v,present,kr,vr,book,active,owner_epoch,epoch):
    b,cap=own.shape;rel=np.full((b,N+1),N,np.int64);counts=np.zeros((b,N),np.int64)
    for i in range(b):
        for j in range(cap):
            o=int(own[i,j])
            if not present[i,j] or not (0<=o<N):continue
            counts[i,o]+=1
            if not kr[i,j] or not vr[i,j] or owner_epoch[i,j]!=epoch[i] or not active[i,o]:continue
            value=v[i,j]
            if np.dot(value,value)<1e-12:continue
            candidates=[int(k) for k in np.flatnonzero(active[i])]
            if not candidates:continue
            ds=[float(np.dot(value-book[i,k],value-book[i,k])) for k in candidates]
            ud=float(np.dot(value[:-1],value[:-1])+(value[-1]-1)**2)
            z=int(np.argmin(ds))
            if ds[z]<ud:rel[i,o]=candidates[z]
        rel[i,:N][counts[i]>1]=N
    return rel,counts

def stats(x):return {'n':int(np.size(x)),'correct':int(np.sum(x)),'rate':float(np.mean(x))}

def score_a(path):
    meta=json.loads(Path(path).with_suffix('.json').read_text());rows=[]
    with np.load(path,allow_pickle=False) as a:
        for c in meta['configs']:
            pre=c['prefix'];get=lambda k:a[pre+'__'+k]
            ids=get('ids');b=len(ids);r=np.arange(b);expected=get('input_parent').copy();codes=get('codes');old,new,nb=ids[:,0],ids[:,1],ids[:,7]
            previous=None;ever_joint=np.ones(b,bool)
            for t,phase in enumerate(c['phases']):
                src=get('event_src')[t];dst=get('event_dst')[t];op=int(get('event_op')[t]);ok=get('event_allowed')[t]
                if phase=='reset':expected[:]=N
                elif phase=='fresh_scope':expected[:]=N;expected[:,0]=0;expected[:,1]=0
                elif op:
                    expected[r[ok],src[ok]]=dst[ok] if op==1 else N
                if not np.array_equal(expected,get('gold')[t]):raise AssertionError('Saved truth differs from events')
                book=get('state_book')[t];active=get('state_active')[t]
                owner=get('state_owner')[t];vals=get('state_vals')[t];present=get('state_present')[t]
                graph,counts=decode_store(owner,vals,present,get('state_kr')[t],get('state_vr')[t],book,active,get('state_owner_epoch')[t],get('state_epoch')[t])
                allrel=(graph[:,:N]==expected[:,:N]).all(-1)
                roles=np.stack([old,new,nb],1);qidx=np.full((b,3),N,np.int64)
                for j in range(3):
                    same=(book==codes[r,roles[:,j]][:,None,:]).all(-1)&active;known=same.sum(-1)==1
                    qidx[known,j]=same[known].argmax(-1)
                truth=np.stack([follow(expected,qidx[:,j]) for j in range(3)],-1)
                for reader in ('record_hop','gated_hop','exact_owner'):
                    pred=get('pred_'+reader)[t,:,:,-1];cor=pred==truth
                    base={'stage':'A','pair':meta['pair'],'variant':c['variant'],'track':c['track'],'family':c['family'],'phase':phase,'reader':reader}
                    rows.append(base|{'metric':'answers_joint',**stats(cor.all(-1))})
                    for j,label in enumerate(('old','new','unaffected')):rows.append(base|{'metric':label,**stats(cor[:,j])})
                base={'stage':'A','pair':meta['pair'],'variant':c['variant'],'track':c['track'],'family':c['family'],'phase':phase,'reader':'store'}
                rows.append(base|{'metric':'all_relations_correct',**stats(allrel)})
                rows.append(base|{'metric':'duplicate_owner',**stats((counts>1).any(-1))})
                if phase in ('write_new','correct_new','clear_new','rewrite_new'):
                    prop=get('receipt_wrong_owner_proposal')[t];comm=get('receipt_wrong_owner_commit')[t]
                    written=get('receipt_written')[t];cleared=get('receipt_cleared')[t]
                    rows.extend([base|{'metric':'wrong_owner_proposal',**stats(prop)},base|{'metric':'wrong_owner_commit',**stats(comm)},base|{'metric':'event_accepted',**stats(written|cleared)},base|{'metric':'veto',**stats(get('receipt_veto')[t])}])
                    if previous is not None:
                        changed=graph[:,:N]!=previous[:,:N];changed[r,new]=False
                        rows.append(base|{'metric':'untargeted_relation_change',**stats(changed.any(-1))})
                previous=graph.copy()
    return rows

def score_b(path):
    meta=json.loads(Path(path).with_suffix('.json').read_text());rows=[]
    with np.load(path,allow_pickle=False) as a:
        for c in meta['configs']:
            pre=c['label'];get=lambda k:a[pre+'__'+k]
            truth=follow(get('parent'),get('query'));known=truth!=N
            graph,count=decode_store(get('state_owner'),get('state_vals'),get('state_present'),get('state_kr'),get('state_vr'),get('state_book'),get('state_active'),get('state_owner_epoch'),get('state_epoch'))
            base={'stage':'B','pair':meta['pair'],'condition':pre,'policy':c['policy'],'hops':c['hops'],'horizon':c['horizon'],'cadence':c['cadence'],'fields':c['fields'],'fault':c['fault']}
            rows.append(base|{'reader':'store','depth':0,'metric':'logical_relations_joint',**stats((graph==get('parent')).all(-1))})
            for rd in ('record_hop','gated_hop','exact_owner'):
                pred=get('pred_'+rd)
                for depth in (1,2,4,8):
                    cor=pred[:,depth-1]==truth
                    for label,mask in (('all',np.ones_like(known)),('supported',known),('missing',~known)):
                        rows.append(base|{'reader':rd,'depth':depth,'metric':label,**stats(cor[mask])})
                    wrongroom=(pred[:,depth-1,None]==get('rooms')).any(-1)&~cor
                    rows.append(base|{'reader':rd,'depth':depth,'metric':'unsupported_terminal',**stats(wrongroom)})
    return rows

def score_cue(path):
    meta=json.loads(Path(path).with_suffix('.json').read_text());rows=[]
    with np.load(path,allow_pickle=False) as a:
        for c in meta['configs']:
            f=c['family'];y=a[f+'__target'];known=y!=N
            for m in ('single16','duplicate32','independent32','single32'):
                pred=a[f+'__pred_'+m];base={'stage':'CUE','pair':meta['pair'],'family':f,'method':m}
                rows.append(base|{'metric':'correct',**stats(pred==y)})
                rows.append(base|{'metric':'accepted',**stats(pred!=N)})
                if (~known).any():rows.append(base|{'metric':'false_accept',**stats(pred[~known]!=N)})
        for m in ('single16','duplicate32','independent32','single32'):
            if not np.array_equal(a['identical_known__pred_'+m],a['identical_novel__pred_'+m]):raise AssertionError('Same evidence produced different decisions')
    return rows
