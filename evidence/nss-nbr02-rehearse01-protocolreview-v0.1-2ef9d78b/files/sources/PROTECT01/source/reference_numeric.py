"""Independent scalar/NumPy checker. Never imports learner, generator, driver or runtime."""
import json,struct,zlib,hashlib,math,csv,sys,os
from pathlib import Path
import numpy as np

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def records(path):
    with open(path,'rb') as f:
        k=0;cache={}
        while True:
            off=f.tell();q=f.read(40)
            if not q:break
            if len(q)!=40:raise ValueError('TRUNCATED_FRAME_HEADER')
            size=struct.unpack('<Q',q[:8])[0];blob=f.read(size)
            if len(blob)!=size or hashlib.sha256(blob).digest()!=q[8:]:raise ValueError('FRAME_DIGEST')
            raw=zlib.decompress(blob);n=struct.unpack('<I',raw[:4])[0];head=json.loads(raw[4:4+n]);buf=raw[4+n:];arrays={}
            for name,d in head['arrays'].items():
                if 'alias' in d:
                    if d['alias'] not in cache:raise ValueError('MISSING_ARRAY_ALIAS')
                    b=cache[d['alias']]
                else:
                    b=buf[d['offset']:d['offset']+d['bytes']];cache[d['identity']]=b
                if digest(b)!=d['sha256']:raise ValueError('ARRAY_DIGEST')
                a=np.frombuffer(b,dtype=np.dtype(d['dtype'])).reshape(d['shape']).copy();arrays[name]=a
            k+=1;yield k,head['metadata'],arrays

def split(v):
    return (v[:368].reshape(16,23),v[368:624].reshape(16,16),v[624:640],v[640:672].reshape(2,16),v[672:674])
def math_reference(v,codes,y=None):
    W,U,b,V,a=split(np.asarray(v,dtype=np.float64));h=np.zeros(16);hs=[h.copy()];xx=[];es=[]
    ew=np.zeros((16,23));eu=np.zeros((16,16));eb=np.zeros(16)
    for i in codes:
        x=np.eye(23)[i];xx.append(x);old=h.copy();h=np.tanh(W.dot(x)+U.dot(old)+b);hs.append(h.copy());d=1-h*h
        # Independent loops implement each local row, using a full old trace copy.
        neww=np.empty_like(ew);newu=np.empty_like(eu);newb=np.empty_like(eb)
        for r in range(16):
            neww[r]=d[r]*(x+U[r,r]*ew[r]);newu[r]=d[r]*(old+U[r,r]*eu[r]);newb[r]=d[r]*(1+U[r,r]*eb[r])
        ew,eu,eb=neww,newu,newb;es.append(np.r_[ew.ravel(),eu.ravel(),eb])
    z=V.dot(h)+a;e=np.exp(z-max(z));p=e/e.sum()
    result={'h':np.array(hs),'logits':z,'probabilities':p,'elig_steps':np.array(es)}
    if y is not None:
        q=p.copy();q[y]-=1;delta=V.T.dot(q)
        gW=np.zeros_like(W);gU=np.zeros_like(U);gb=np.zeros_like(b);adj=delta.copy()
        for t in range(len(codes)-1,-1,-1):
            adjz=adj*(1-hs[t+1]**2);gW+=np.outer(adjz,xx[t]);gU+=np.outer(adjz,hs[t]);gb+=adjz;adj=U.T.dot(adjz)
        result['G']=np.r_[gW.ravel(),gU.ravel(),gb,np.outer(q,h).ravel(),q]
        result['L']=np.r_[(delta[:,None]*ew).ravel(),(delta[:,None]*eu).ravel(),delta*eb,np.outer(q,h).ravel(),q]
    return result

def expected_step(pre,gradient,defect=None):
    g=np.asarray(gradient,dtype=np.float64);factor=min(1.,1/np.linalg.norm(g)) if np.linalg.norm(g)>0 else 1.
    mul=-1 if defect=='sign' else (2 if defect=='double' else 1)
    return np.asarray(pre,dtype=np.float64)-mul*factor*g

def check(a,b,where,stats):
    a=np.asarray(a);b=np.asarray(b)
    if a.shape!=b.shape:raise ValueError('SHAPE:'+where+str((a.shape,b.shape)))
    if not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('NONFINITE:'+where)
    diff=np.abs(a-b);tol=2e-6+2e-5*np.abs(b);ratio=float(np.max(diff/tol)) if a.size else 0
    stats['scalar_checks']+=a.size;stats['max_tolerance_ratio']=max(stats['max_tolerance_ratio'],ratio)
    if ratio>1:raise ValueError('NUMERIC:'+where+':'+str(ratio))
    return ratio

def log_check(path):
    prev='0'*64;seq=0;intents={};commits={};events=[]
    for l in Path(path).read_text().splitlines():
        w=json.loads(l);o=w['record'];seq+=1
        assert o['sequence']==seq and o['previous']==prev and digest(canonical(o))==w['sha256'],'LOG_CHAIN'
        prev=w['sha256'];events.append(o)
        if o['event']=='UPDATE_INTENT':assert o['attempt'] not in intents;intents[o['attempt']]=o
        if o['event']=='UPDATE_COMMIT':assert o['attempt'] in intents and o['attempt'] not in commits;commits[o['attempt']]=o
    unknown=sorted(set(intents)-set(commits))
    return {'events':len(events),'intents':len(intents),'commits':len(commits),'unknown_attempts':unknown,'chain':prev},events

def write_csv(path,rows,fields=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:fields=list(rows[0]) if rows else ['empty']
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

def verify_plan(plan,seeds,targets):
    count=0
    for sid,sm in plan['sessions'].items():
        phase=sm['phase'];txs=sm['transactions'];fit=sm['fit']
        if phase in ('initial','cost'):
            key=f'order/main/{fit}' if phase=='initial' else 'order/cost';n=100 if phase=='initial' else 50
            g=np.random.Generator(np.random.PCG64(seeds[key]));order=[]
            while len(order)<n:order.extend(int(x) for x in g.permutation(8))
            expected=order[:n];assert len(txs)==n
        elif phase=='receipt_diagnostic':expected=[4,0,5,1,6,2]
        elif phase in ('development','heldout'):
            f,p=sm['focal'],sm['protected'];expected=[f,p,f,f,p,f]
            assert (phase=='development' and f in range(8,12)) or (phase=='heldout' and f in range(12,20))
        else:expected=[t['cue'] for t in txs]
        for tr,(t,c) in enumerate(zip(txs,expected),1):
            assert t['cue']==c
            if phase not in ('fixture','sandbox','derivative'):
                expected_target=targets[c]^int(phase in ('development','heldout') and sm.get('reversal')==1 and tr>=3 and c==sm['focal'])
                assert t['target']==expected_target,'RECEIPT_LABEL'
            if phase in ('development','heldout'):key=f"filler/base/{sm['base']:02}/trial/{tr}";d=sm['delay']
            elif phase=='receipt_diagnostic':key=f'filler/receipt_diagnostic/fit/{fit}/trial/{tr}';d=8
            elif phase=='fixture':key=f"filler/fixture/{sm['case']}";d=sm['delay']
            else:key=None;d=0
            if key:
                sc=0 if c in (0,1,2,3,8,9,12,13,14,15) else 1;g=np.random.Generator(np.random.PCG64(seeds[key]));v=[int(g.integers(0,4))+4*((1-sc) if j%2==0 else sc) for j in range(32)]
                assert t['fillers']==v[:d],'FILLER_RECIPE'
            else:assert t['fillers']==[]
            count+=1
    return count

def audit_run(run,out):
    run=Path(run);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((run/'private/PLAN.json').read_text());seeds=json.loads((run.parent.parent/'protocol/SEED_RECIPE.json').read_text())['seeds']
    # Rebuild targets independently from seeds, but never instantiate held-out mappings if absent.
    targets={}
    groups=[('old',[(0,1,2,3),(4,5,6,7)]),('dev',[(8,9),(10,11)])]
    if plan.get('heldout_generated'):groups.append(('heldout',[(12,13,14,15),(16,17,18,19)]))
    for group,scopes in groups:
        for sc,cues in enumerate(scopes):
            order=np.random.Generator(np.random.PCG64(seeds[f'environment/{group}/scope{sc}'])).permutation(cues)
            targets.update({int(x):int(i<len(cues)//2) for i,x in enumerate(order)})
    assert targets=={int(k):v for k,v in plan['targets'].items()},'TARGET_RECIPE'
    input_count=verify_plan(plan,seeds,targets)
    stats={'scalar_checks':0,'max_tolerance_ratio':0.,'frames':0,'updates':0,'queries':0,'filler_steps':0,'expected_fault_updates':0,'ordinary_update_errors':0}
    traces=[];rows=[];derivs=[];versions={};cue_rec={};session_weights={};seen_sessions=set();pending={};lastfill={};initials={}
    log,events=log_check(run/'worker/events.jsonl')
    prior_prediction={o['receipt']:o['sequence'] for o in events if o['event']=='PREDICTION_BEFORE_FEEDBACK'}
    releases={o['receipt']:o['sequence'] for o in events if o['event']=='FEEDBACK_RELEASED'}
    if log['unknown_attempts']:raise ValueError('UNKNOWN_COMPLETION')
    def row(logits,y,m,kind,cue):
        z=np.asarray(logits,dtype=float);loss=float(np.logaddexp.reduce(z)-z[y]);meta=plan['sessions'][m['context']['session']]
        return {'session':m['context']['session'],'phase':meta['phase'],'arm':m['arm'],'fit':meta.get('fit',-1),'base':meta.get('base',-1),'delay':meta.get('delay',0),'reversal':meta.get('reversal',0),'trial':m['context'].get('trial',0),'kind':kind,'cue':cue,'target':y,'predicted':int(np.argmax(z)),'correct':int(np.argmax(z)==y),'loss':loss,'logit0':float(z[0]),'logit1':float(z[1])}
    for k,m,a in records(run/'worker/records.bin'):
        stats['frames']+=1;kind=m['kind'];sid=m['context']['session'];sm=plan['sessions'][sid];arm=m['arm']
        if kind=='load':
            assert sid not in seen_sessions;seen_sessions.add(sid);v=a['params'];session_weights[sid]=v;versions[digest(v.tobytes())]=v
            if sm['phase'] in ('initial','cost','fixture','sandbox','derivative'):
                if sm['phase']=='derivative':
                    W=np.zeros((16,23));U=np.zeros((16,16));b=np.zeros(16);V=np.zeros((2,16));aa=np.zeros(2)
                    U[0,0]=.5;U[1,1]=.5;V[1,1]=1
                    if sm['coupled']:U[1,0]=.5
                    if sm['nonlinear']:W[0,22]=.4
                else:
                    key=f"initialization/main/{sm['fit']}" if sm['phase']=='initial' else 'initialization/'+('cost' if sm['phase']=='cost' else 'fixture')
                    gen=np.random.Generator(np.random.PCG64(seeds[key]));W=gen.uniform(-np.sqrt(6/39),np.sqrt(6/39),(16,23));U=gen.uniform(-.05,.05,(16,16))+np.eye(16)*.25;b=np.zeros(16);V=gen.uniform(-.02,.02,(2,16));aa=np.zeros(2)
                vv=np.concatenate([x.astype(np.float32).ravel() for x in (W,U,b,V,aa)])
                assert np.array_equal(v,vv),'INITIAL_BYTES'
            else:
                key=(sm['fit'],arm[-1] if arm.startswith('N') else arm)
                assert np.array_equal(v,initials[key]),'CONDITION_START_CHECKPOINT'
        elif kind=='cue':
            assert sid not in pending;assert np.array_equal(a['params'],session_weights[sid]);assert digest(a['params'].tobytes())==m['version']
            tr=m['context']['trial'];target=sm['transactions'][tr-1]['target'];cue=sm['transactions'][tr-1]['cue'];assert cue==m['cue'];assert m['codes']==[22,20+m['scope'],cue]
            ref=math_reference(a['params'],m['codes'],target)
            for key in ('h','logits','probabilities'):check(a[key],ref[key],kind+key,stats)
            if arm=='L':check(a['elig_steps'],ref['elig_steps'],'elig_steps',stats)
            elif a['elig_steps'].shape!=(0,640):raise ValueError('UNEXPECTED_TRACE')
            pending[sid]=(m,a,ref);cue_rec[k]=(m,a,ref);lastfill[sid]=a['h'][-1];rows.append(row(a['logits'],target,m,'raw_pre',cue))
        elif kind=='fillers':
            cm,ca,ref=pending[sid];codes=sm['transactions'][m['context']['trial']-1]['fillers'];assert m['codes']==codes
            W,U,b,V,aa=split(ca['params'].astype(float));h=ca['h'][-1].astype(float);hh=[h.copy()]
            for code in codes:
                h=np.tanh(W[:,code]+U@h+b);hh.append(h.copy())
            check(a['h'],np.array(hh),'filler',stats);assert m['pending_unchanged'];stats['filler_steps']+=len(codes)
        elif kind in ('update','frozen_receipt','derivative'):
            cm,ca,ref=pending.pop(sid);y=m['target'];assert y==sm['transactions'][m['context']['trial']-1]['target']
            if kind!='derivative':assert prior_prediction[m['receipt']]<releases[m['receipt']],'POST_AS_PRE'
            if kind in ('update','derivative'):
                check(a['raw_gradient'],ref[arm],'raw_'+arm,stats)
                g=ref['G'];l=ref['L'];encg=g[:640];encl=l[:640];gn=float(np.linalg.norm(encg));ln=float(np.linalg.norm(encl));diff=float(np.linalg.norm(encg-encl));cos=None if gn*ln<1e-24 else float(np.dot(encg,encl)/(gn*ln))
                ds={'session':sid,'phase':sm['phase'],'arm':arm,'fit':sm.get('fit',-1),'base':sm.get('base',-1),'trial':m['context']['trial'],'exact_encoder_norm':gn,'local_encoder_norm':ln,'encoder_difference':diff,'relative_difference':None if gn<1e-12 else diff/gn,'cosine':cos,'U_offdiag_norm':float(np.linalg.norm(split(ca['params'])[1]-np.diag(np.diag(split(ca['params'])[1]))))}
                derivs.append(ds)
                if kind=='derivative':
                    if not sm['coupled']:check(ref['G'],ref['L'],'diagonal_exact',stats)
                    if sm['coupled'] and not sm['nonlinear']:
                        assert abs(gn*gn-47/32)<1e-12 and abs(diff*diff-3/8)<1e-12 and diff/gn>=.05,'ANALYTIC_WITNESS'
                    continue
                gobs=a['raw_gradient'].astype(float);norm=float(np.linalg.norm(gobs));fac=min(1.,1/norm) if norm else 1.;check(a['norm_factor'],np.array([norm,fac]),'norm_clip',stats)
                exp=expected_step(ca['params'],gobs);defect=m['defect']
                if defect:
                    assert sm['phase']=='sandbox';assert not np.allclose(a['post'],exp,atol=2e-6,rtol=2e-5),'UNDETECTED_INJECTED_STEP'
                    check(a['post'],expected_step(ca['params'],gobs,defect),'specified_fault',stats);stats['expected_fault_updates']+=1
                else:check(a['post'],exp,'committed_update',stats)
                stats['updates']+=1
                traces.append({**ds,'loss_before':float(np.logaddexp.reduce(ca['logits'].astype(float))-ca['logits'][y]),'raw_gradient_norm':norm,'clip_factor':fac,'update_norm':float(np.linalg.norm(a['post']-ca['params'])),'expected_injection':int(bool(defect))})
            else:assert np.array_equal(a['post'],ca['params']),'FROZEN_CHANGED'
            session_weights[sid]=a['post'];versions[digest(a['post'].tobytes())]=a['post']
        elif kind=='query':
            assert sid not in pending;assert m['readonly'];v=session_weights[sid];assert digest(v.tobytes())==m['parameter_version'];ref=math_reference(v,m['codes'])
            for key in ('h','logits','probabilities'):check(a[key],ref[key],'query_'+key,stats)
            cue=m['cue'];y=targets[cue]
            if sm.get('reversal',0) and cue==sm.get('focal') and m['context'].get('trial',0)>=3:y=1-y
            if sm['phase']=='fixture':y=sm['transactions'][0]['target']
            rows.append(row(a['logits'],y,m,m['query']['kind'],cue));stats['queries']+=1
        elif kind=='checkpoint':
            assert sid not in pending and m['ephemeral_empty'];assert np.array_equal(a['params'],session_weights[sid])
            if sm['phase']=='initial' and m['cursor'].get('completed')==100:initials[(sm['fit'],arm)]=a['params']
        else:raise ValueError('UNKNOWN_RECORD:'+kind)
    assert not pending,'LEFT_PENDING'
    # Natural per-arm equality under delay: raw gradients, states and updates from same start, tested separately in replay checker.
    gate=[]
    for arm in ('G','L'):
        for fit in range(4):
            rr=[r for r in rows if r['arm']==arm and r['fit']==fit]
            warm=[r for r in rr if r['phase']=='warm' and r['kind']=='warm_inventory']
            dev=[r for r in rr if r['phase']=='development' and r['delay']==0 and r['kind']=='primary']
            nn=[r for r in rows if r['arm']=='N_'+arm and r['fit']==fit and r['phase']=='development' and r['delay']==0 and r['kind']=='primary']
            if len(warm)==8 and len(dev)==40 and len(nn)==40:
                w=sum(r['correct'] for r in warm);d=sum(r['correct'] for r in dev);n=sum(r['correct'] for r in nn)
                gate.append({'arm':arm,'fit':fit,'initial_correct':w,'initial_total':8,'development_correct':d,'development_total':40,'frozen_correct':n,'gain':d-n,'pass':int(w==8 and d>=32 and d-n>=8)})
    exact_path=run/'EXACT_CONTROL.json'
    if exact_path.exists():
        exact=json.loads(exact_path.read_text());current={};group=None
        for xr in exact:
            key=(xr['phase'],xr['base'],xr['delay'],xr['reversal'])
            if key!=group:current={c:targets[c] for c in range(8)};group=key
            c=xr['cue'];y=targets[c]^int(xr['reversal'] and c>=8 and xr['trial']>=3)
            assert y==xr['target']
            if xr['kind']=='raw_pre':
                assert xr['predicted']==current.get(c);current[c]=y
            else:assert xr['predicted']==current.get(c)
            assert xr['correct']==int(xr['predicted']==y)
        write_csv(out/'EXACT_ROWS.csv',exact)
    stats['independently_verified_input_transactions']=input_count
    write_csv(out/'QUERY_ROWS.csv',rows);write_csv(out/'NEGATIVE_QUERY_ROWS.csv',[r for r in rows if not r['correct']]);write_csv(out/'UPDATE_DIAGNOSTICS.csv',traces);write_csv(out/'GRADIENT_COMPARISON.csv',derivs);write_csv(out/'A0_FIT_GATE.csv',gate)
    result={'status':'PASS','stats':stats,'log':log,'gate':gate,'heldout_generated':plan.get('heldout_generated',False)}
    (out/'AUDIT.json').write_text(json.dumps(result,indent=2,allow_nan=False));return result
if __name__=='__main__':
    result=audit_run(sys.argv[1],sys.argv[2]);print(json.dumps(result,indent=2))
