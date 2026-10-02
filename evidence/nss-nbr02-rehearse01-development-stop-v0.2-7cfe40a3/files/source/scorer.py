"""Independent REHEARSE01 score/certificate audit. No controller, generator,
Torch model, production QP solver, or update function is imported.
"""
import json,csv,sys,math,hashlib,collections
from pathlib import Path
import numpy as np
from reference_numeric import records,math_reference,check,split,log_check,write_csv,canonical,digest

ROOT=Path(__file__).resolve().parent.parent

def scope(c):return 0 if c in [0,1,2,3,8,9,12,13,14,15] else 1

def tech():return {**dict(enumerate([0,1,0,1,1,0,1,0])),8:0,10:1}

def expected_entry(c,s,y,r,pre,post,seq,origin='validated_receipt'):
    xx=np.zeros((3,23),dtype='f4');xx[0,22]=1;xx[1,20+s]=1;xx[2,c]=1
    return {'schema':1,'scope':s,'cue':c,'codes':[22,20+s,c],'feature_hash':digest(xx.tobytes()),'label':int(y),'receipt':r,'pre_version':pre,'post_version':post,'receipt_sequence':int(seq),'validity':'VALID','origin':origin}

def independently_verify_plan(plan):
    alloc=json.loads((ROOT/'protocol/SEEDS.json').read_text());seeds={x['label']:x['seed_uint64'] for x in alloc['allocations']}
    for k,v in seeds.items():assert int.from_bytes(hashlib.sha256(('NSS-NBR02-REHEARSE01-REVIEW-v0.1/'+k).encode()).digest()[:8],'big')==v
    targets={};rngchecks=0
    for name,ranges in [('old',[range(4),range(4,8)]),('development',[range(8,10),range(10,12)]),('heldout',[range(12,16),range(16,20)])]:
        if name not in plan['generated_groups']:continue
        for sc,ids in enumerate(ranges):
            k=f'labels/{name}/scope{sc}';g=np.random.Generator(np.random.PCG64(seeds[k]));v=g.permutation(list(ids));targets.update({int(c):int(j<len(v)//2) for j,c in enumerate(v)})
            assert g.bit_generator.state==plan['rng'][k]['final'];rngchecks+=1
    assert targets=={int(k):v for k,v in plan['targets'].items()}
    ids={};n=0
    for sid,sm in plan['sessions'].items():
        ph=sm['phase'];tx=sm['transactions']
        if ph in ('initial','probe_warm'):
            k=f'order/main/{sm["fit"]}' if ph=='initial' else 'order/probe';g=np.random.Generator(np.random.PCG64(seeds[k]));v=[];length=100 if ph=='initial' else 10
            while len(v)<length:v+=list(map(int,g.permutation(8)))
            cues=v[:length];assert plan['rng'][k]['final']==g.bit_generator.state
        elif ph in ('development','heldout','fixture','probe'):
            f,p=sm['focal'],sm['protected'];cues=[f,p,f,f,p,f]
            if ph in ('development','heldout'):assert f==sm['base']+8 and p==[4,5,0,1,4,5,6,7,0,1,2,3][sm['base']]
            else:assert (f,p)==[(8,4),(10,0)][sm['base']]
        else:cues=[t['cue'] for t in tx]
        assert len(tx)==len(cues)
        for i,(c,t) in enumerate(zip(cues,tx),1):
            assert c==t['cue'] and scope(c)==t['scope']
            if ph in ('initial','development','heldout'):yy=targets[c]
            elif ph in ('probe_warm','probe','fixture'):yy=tech()[c]
            else:yy=t['target']
            if ph in ('development','heldout','probe','fixture') and c==sm['focal'] and i>=3:yy^=1
            assert yy==t['target'],'PUBLIC_LABEL_RECIPE'
            if ph=='fixture':
                key=f'fixture/filler/case{sm["base"]}/trial{i}';g=np.random.Generator(np.random.PCG64(seeds[key]));v=[int(g.integers(0,4))+4*((1-scope(c)) if j%2==0 else scope(c)) for j in range(32)];assert t['fillers']==v[:sm['delay']]
            else:assert not t['fillers']
            rr=hashlib.sha256(f"REHEARSE01-v0.1|{seeds[t['wire_key']]:016x}|{t['wire_phase']}|{t['wire_base']}|{i}|receipt".encode()).digest()[:8].hex()
            ident=(t['wire_phase'],t['wire_base'],i);assert rr!='0'*16 and rr==t['receipt']
            if rr in ids:assert ids[rr]==ident
            ids[rr]=ident;n+=1
    return targets,seeds,{'transactions':n,'distinct_public_receipts':len(ids),'label_rng_checks':rngchecks}

def initial_expected(sm,seeds):
    if sm['phase'] in ('derivative','margin_derivative'):
        W=np.zeros((16,23));U=np.zeros((16,16));b=np.zeros(16);V=np.zeros((2,16));a=np.zeros(2);U[0,0]=U[1,1]=.5;V[1,1]=1
        if sm['coupled']:U[1,0]=.5
        if sm['nonlinear']:W[0,22]=.4
    else:
        k=f'init/main/{sm["fit"]}' if sm['phase']=='initial' else ('init/probe' if sm['phase']=='probe_warm' else 'init/fixture');g=np.random.Generator(np.random.PCG64(seeds[k]))
        W=g.uniform(-np.sqrt(6/39),np.sqrt(6/39),(16,23));U=g.uniform(-.05,.05,(16,16))+np.eye(16)*.25;b=np.zeros(16);V=g.uniform(-.02,.02,(2,16));a=np.zeros(2)
    return np.concatenate([x.astype('f4').ravel() for x in (W,U,b,V,a)])

def audit(run,out,full=False):
    run=Path(run);out=Path(out);out.mkdir(parents=True,exist_ok=True);plan=json.loads((run/'private/PLAN.json').read_text());targets,seeds,inp=independently_verify_plan(plan)
    stats={'scalar_checks':0,'max_tolerance_ratio':0.,'frames':0,'updates':0,'queries':0,'forks':0,'expected_faults':0,'checkpoints':0,'filler_steps':0,'batch_examples':0,'batches':0,'post_strong_checks':0}
    log,events=log_check(run/'worker/events.jsonl');assert not log['unknown_attempts'],'UNKNOWN_COMPLETION'
    event_by_seq={e['sequence']:e for e in events};evidence={e['frame']['index']:e for e in events if e['event']=='EVIDENCE_DURABLE'}
    releases=collections.defaultdict(list)
    for e in events:
        if e['event']=='FEEDBACK_RELEASED':releases[(e['context']['session'],e['context']['branch'],e['receipt'])].append(e)
    weights={};tables={};used={};pending={};cues={};forks={};inits={};init_tables={};probes={};probe_tables={};protect={};batchlist={};batchrows=[];batched=set();qrows=[];updates=[];drows=[];prows=[];delay_groups={};dupcomparisons=dupelements=0
    def contextrow(m):
        sm=plan['sessions'][m['context']['session']]
        return {'session':m['context']['session'],'phase':sm['phase'],'method':sm['method'],'arm':m['arm'],'fit':sm['fit'],'base':sm.get('base',-1),'delay':sm.get('delay',0),'branch':m['context']['branch'],'trial':m['context'].get('trial',0)}
    def addrow(m,z,y,cue,kind,k):
        z=np.asarray(z,dtype=float);p=np.exp(z-z.max());p/=p.sum()
        qrows.append({**contextrow(m),'frame':k,'kind':kind,'stage':m.get('query',{}).get('stage','pre_feedback' if kind=='raw_pre' else 'post_real'),'cue':cue,'scope':scope(cue),'target':y,'predicted':int(z.argmax()),'correct':int(z.argmax()==y),'loss':float(np.logaddexp.reduce(z)-z[y]),'logit_margin':float(z[y]-z[1-y]),'probability_margin':float(p[y]-p[1-y]),'logit0':float(z[0]),'logit1':float(z[1])})
    for k,m,a in records(run/'worker/records.bin'):
        stats['frames']+=1;kind=m['kind'];assert k in evidence
        ctx=m['context'];sid=ctx['session'];branch=ctx['branch'];key=(sid,branch);sm=plan['sessions'][sid];arm=m['arm'];tr=ctx.get('trial',0)
        if kind=='load':
            assert key not in weights;weights[key]=a['params']
            if branch in ('U','F','R'):assert np.array_equal(weights[key],forks[sid]['params'])
            elif sm['phase'] in ('initial','probe_warm','fixture','sandbox','derivative','margin_derivative'):assert np.array_equal(weights[key],initial_expected(sm,seeds))
            elif sm['phase']=='probe':assert np.array_equal(weights[key],probes[sm['method']])
            else:assert np.array_equal(weights[key],inits[(sm['fit'],sm['method'])])
        elif kind=='management_load':
            tables[key]=m['table'];used[key]=m['used'];assert not used[key]
            if branch in ('U','F','R'):assert tables[key]==forks[sid]['table']
            elif sm['phase'] in ('initial','probe_warm','fixture','sandbox','derivative','margin_derivative'):assert tables[key]=={}
            elif sm['phase']=='probe':assert tables[key]==probe_tables[sm['method']]
            else:assert tables[key]==init_tables[(sm['fit'],sm['method'])]
        elif kind=='buffer_import':
            assert sm['phase'] in ('fixture','sandbox') and tables[key]=={};expected={}
            for rr in m['observations']:
                c=rr['cue'];sc=scope(c);rid=digest(f"REHEARSE01-v0.1|{seeds['wire/fixture']:016x}|historical|{c}|receipt".encode())[:16]
                assert rr=={'cue':c,'scope':sc,'target':tech()[c],'receipt':rid,'sequence':c+1}
                expected[f'{sc}:{c}']=expected_entry(c,sc,rr['target'],rid,'OBSERVED_FIXTURE_HISTORY','OBSERVED_FIXTURE_HISTORY',c+1,'fixture_prior_receipt')
            assert len(expected)==8 and expected==m['table'];tables[key]=expected
        elif kind=='cue':
            assert key not in pending and np.array_equal(a['params'],weights[key]);assert m['version']==digest(a['params'].tobytes())
            tx=sm['transactions'][tr-1];assert m['cue']==tx['cue'] and m['receipt']==tx['receipt'] and m['scope']==tx['scope']
            assert m['codes']==[22,20+scope(m['cue']),m['cue']] and m['table']==tables[key] and m['used']==used[key]
            ref=math_reference(a['params'],m['codes'],tx['target'])
            for n in ('h','logits','probabilities'):check(a[n],ref[n],'cue/'+n,stats)
            if arm=='L':check(a['elig_steps'],ref['elig_steps'],'local_elig',stats)
            else:assert a['elig_steps'].shape==(0,640)
            cues[k]=(m,a,ref);pending[key]=k
            if m['reconstructed']:
                orig=cues[m['original_cue_ref']['index']]
                for n in ('params','h','elig_steps','logits','probabilities'):assert np.array_equal(a[n],orig[1][n]),'FORK_FORWARD'
            else:addrow(m,a['logits'],tx['target'],tx['cue'],'raw_pre',k)
        elif kind=='fillers':
            cm,ca,ref=cues[pending[key]];tx=sm['transactions'][tr-1];assert m['codes']==tx['fillers'] and m['pending_unchanged']
            W,U,b,V,aa=split(ca['params'].astype(float));h=ca['h'][-1].astype(float);hs=[h.copy()]
            for c in m['codes']:h=np.tanh(W[:,c]+U@h+b);hs.append(h.copy())
            check(a['h'],np.array(hs),'filler_h',stats);stats['filler_steps']+=len(m['codes'])
        elif kind=='fork':
            assert branch=='COMMON' and pending[key]==m['cue_ref']['index'];tx=sm['transactions'][tr-1];old=tables[key].get(f'{tx["scope"]}:{tx["cue"]}')
            assert old is not None and old['label']!=tx['target'] and not used[key];assert np.array_equal(a['params'],weights[key]) and m['table']==tables[key]
            forks[sid]={'params':a['params'],'table':tables[key].copy(),'frame':k,'ref':pending.pop(key),'trial':tr};weights[(sid,'B1')]=weights[key].copy();tables[(sid,'B1')]=tables[key].copy();used[(sid,'B1')]=False;pending[(sid,'B1')]=forks[sid]['ref'];stats['forks']+=1
        elif kind=='fork_match':
            assert m['bitwise_forward_gradient'] and m['distinct_mutable_storage'];forks[sid]['gradient']=a['raw_gradient']
        elif kind=='post_strong_match':
            assert m['semantic_authority_equal'] and m['branches']==['U','F','R']
            assert all(np.array_equal(weights[(sid,b)],weights[(sid,'U')]) for b in ('F','R'))
            stats['post_strong_checks']+=1
        elif kind=='batch_example':
            op=m['application_id'];assert key not in pending and key not in batched
            assert np.array_equal(a['params'],weights[key]) and m['pre_digest']==digest(weights[key].tobytes())
            rr=m['source'];assert rr==tables[key][f'{rr["scope"]}:{rr["cue"]}'] and rr['validity']=='VALID'
            assert rr['feature_hash']==digest(np.eye(23,dtype='f4')[rr['codes']].tobytes()) and rr['receipt_sequence']<evidence[k]['sequence']
            assert m['source_hash']==digest(canonical(rr));role=m['role'];i=m['ordinal']
            if role=='R':assert rr['cue']==i and rr['cue']<8
            else:assert rr['cue']==(sm['transactions'][0]['cue'] if sm['phase']=='sandbox' else sm['focal'])
            qq=batchlist.setdefault(op,[]);assert i==len(qq) and i<8
            ref=math_reference(weights[key],rr['codes'],rr['label'])
            for n in ('h','logits','probabilities'):check(a[n],ref[n],'batch/'+n,stats)
            if arm=='L':check(a['elig_steps'],ref['elig_steps'],'batch/local',stats)
            else:assert a['elig_steps'].shape==(0,640)
            check(a['raw_gradient'],ref[arm],'batch/raw_'+arm,stats)
            qq.append((k,m,a));stats['batch_examples']+=1
        elif kind=='batch_apply':
            op=m['application_id'];qq=batchlist.pop(op);assert len(qq)==8 and key not in batched and key not in pending
            assert np.array_equal(a['pre'],weights[key]) and m['pre_digest']==digest(a['pre'].tobytes())
            src=[q[1]['source'] for q in qq];assert src==m['sources'] and [q[0] for q in qq]==[r['index'] for r in m['examples']]
            expected_op=digest(canonical({'schema':'REHEARSAL_v1','learner_namespace':sid,'branch':branch,'parent_online_application':m['parent_online_attempt'] if sm['phase']!='sandbox' else 'SYNTHETIC_PRIOR_RECEIPT','batch_ordinal':0,'sources':[r['receipt'] for r in src]}));assert op==expected_op
            gg=np.stack([q[2]['raw_gradient'] for q in qq]);assert gg.tobytes()==a['example_gradients'].tobytes()
            acc=np.zeros(674,'f8')
            for g in gg:acc=np.add(acc,g.astype('f8'))
            mean64=np.divide(acc,8.);mean32=mean64.astype('f4')
            for n,x in [('accumulator64',acc),('mean64',mean64),('mean32',mean32)]:assert x.tobytes()==a[n].tobytes(),'BATCH_REDUCTION:'+n
            if m['role']=='F':assert all(np.array_equal(x,gg[0]) for x in gg) and np.array_equal(mean32,gg[0])
            norm=float(np.linalg.norm(mean32.astype('f8')));fac=min(1.,1/norm) if norm else 1.;check(a['norm_factor'],np.array([norm,fac]),'batch/norm_factor',stats)
            nf=a['norm_factor'];fac32=np.minimum(np.float32(1),np.float32(1)/nf[0]) if nf[0]>0 else np.float32(1);assert fac32.tobytes()==nf[1].tobytes()
            product=np.multiply(mean32,nf[1],dtype='f4');assert product.tobytes()==a['clip_product'].tobytes()
            expect_product=product.copy();defect=m['defect']
            if defect=='sign':expect_product=-expect_product
            elif defect=='double':expect_product=expect_product*np.float32(2)
            assert expect_product.tobytes()==a['applied_product'].tobytes()
            expected=np.subtract(a['pre'],expect_product,dtype='f4');assert expected.tobytes()==a['post'].tobytes(),'BATCH_APPLIED_BYTES'
            if defect:
                assert sm['phase']=='sandbox' and defect==sm['defect'] and np.linalg.norm(product)>0
                assert not np.allclose(a['post'],np.subtract(a['pre'],product,dtype='f4'),atol=2e-6,rtol=2e-5);stats['expected_faults']+=1
            else:assert branch in ('F','R') and m['role']==branch and tr==3
            assert m['table_unchanged'] and m['consumed_unchanged'] and m['ephemeral_reset'] and m['post_digest']==digest(a['post'].tobytes())
            weights[key]=a['post'];batched.add(key);stats['updates']+=1;stats['batches']+=1
            individual_norms=np.linalg.norm(gg.astype('f8'),axis=1)
            batchrows.append({**contextrow(m),'frame':k,'application_id':op,'role':m['role'],'gradient_norm':float(nf[0]),'clip_factor':float(nf[1]),'actual_step_norm':float(np.linalg.norm(a['post'].astype('f8')-a['pre'].astype('f8'))),'mean_example_norm':float(individual_norms.mean()),'cancellation_ratio':norm/float(individual_norms.mean()) if individual_norms.mean()>0 else None,'defect':defect})
        elif kind in ('update','frozen_receipt','derivative'):
            ci=pending.pop(key);cm,ca,ref=cues[ci];tx=sm['transactions'][tr-1];assert tx['target']==m['target'] and ci==m['cue_ref']['index']
            if kind=='derivative':
                check(a['raw_gradient'],ref[arm],'derivative_'+arm,stats);eg=ref['G'][:640];el=ref['L'][:640];gn=float(np.linalg.norm(eg));df=float(np.linalg.norm(eg-el))
                if not sm['coupled']:check(ref['G'],ref['L'],'diagonal',stats)
                if sm['coupled'] and not sm['nonlinear']:assert abs(gn*gn-47/32)<1e-12 and abs(df*df-3/8)<1e-12
                drows.append({**contextrow(m),'relative_difference':None if gn<1e-12 else df/gn});continue
            assert m['table_before']==tables[key];old=tables[key].get(f'{tx["scope"]}:{tx["cue"]}');change=old is not None and old['label']!=tx['target'] and not used[key]
            assert m['changed']==change and m['used']==(used[key] or change)
            expected_clip=2. if branch in ('U','F','R') and change else 1.;assert m['clip']==expected_clip
            rr=releases[(sid,branch,m['receipt'])];assert len(rr)==1 and rr[0]['outcome']==tx['target'] and rr[0]['prediction_sequence']==m['prediction_sequence']
            pred=event_by_seq[m['prediction_sequence']];assert pred['event']=='PREDICTION_BEFORE_FEEDBACK' and pred['sequence']<rr[0]['sequence']<evidence[k]['sequence']
            if kind=='update':
                g=a['raw_gradient'];check(g,ref[arm],'gradient_'+arm,stats);norm=float(np.linalg.norm(g.astype('f8')));fac=min(1.,expected_clip/norm) if norm else 1.;check(a['norm_factor'],np.array([norm,fac]),'norm_factor',stats)
                fac32=np.minimum(np.float32(1),np.float32(expected_clip)/a['norm_factor'][0]) if a['norm_factor'][0]>0 else np.float32(1);assert fac32.tobytes()==a['norm_factor'][1].tobytes();product=np.multiply(g,a['norm_factor'][1],dtype='f4');assert product.tobytes()==a['proposed_clip_product'].tobytes(),'CLIP_PRODUCT_BYTES'
                if branch in ('B1','U','F','R') and change:assert np.array_equal(g,forks[sid]['gradient'])
                pp=product.copy()
                if m['defect']=='sign':pp=-pp
                if m['defect']=='double':pp=pp*np.float32(2)
                expected=(ca['params']-pp).astype('f4')
                assert np.array_equal(expected,a['post']),'APPLIED_PARAMETER_BYTES'
                if m['defect']:
                    assert sm['phase']=='sandbox' and not np.allclose(a['post'],ca['params'].astype('f8')-g.astype('f8')*fac,atol=2e-6,rtol=2e-5);stats['expected_faults']+=1
                eg=ref['G'][:640];el=ref['L'][:640];normg=float(np.linalg.norm(eg));norml=float(np.linalg.norm(el));df=float(np.linalg.norm(eg-el))
                updates.append({**contextrow(m),'frame':k,'cue_frame':ci,'receipt':m['receipt'],'raw_norm':float(a['norm_factor'][0]),'factor':float(a['norm_factor'][1]),'actual_step_norm':float(np.linalg.norm(a['post'].astype('f8')-ca['params'].astype('f8'))),'relative_local_difference':df/normg if normg>1e-12 else None,'gradient_cosine':float(np.dot(eg,el)/(normg*norml)) if normg*norml>1e-12 else None,'defect':m['defect']});stats['updates']+=1
            else:assert np.array_equal(a['post'],weights[key])
            assert m['post_digest']==digest(a['post'].tobytes());tnew=tables[key].copy();tnew[f'{tx["scope"]}:{tx["cue"]}']=expected_entry(tx['cue'],tx['scope'],tx['target'],m['receipt'],m['pre_digest'],m['post_digest'],evidence[k]['sequence']-1)
            assert tnew==m['table_after'],'TABLE_AFTER_AUTHORITY';tables[key]=tnew;used[key]=m['used'];weights[key]=a['post']
        elif kind=='query':
            assert key not in pending and m['readonly'] and m['parameter_version']==digest(weights[key].tobytes());assert m['codes']==[22,20+scope(m['cue']),m['cue']]
            ref=math_reference(weights[key],m['codes'])
            for n in ('h','logits','probabilities'):check(a[n],ref[n],'query/'+n,stats)
            c=m['cue'];y=(tech()[c] if sm['phase'] in ('fixture','probe','probe_warm') else targets[c]) if sm['phase']!='sandbox' else sm['transactions'][0]['target']
            if sm['phase'] in ('fixture','probe','development','heldout') and c==sm.get('focal') and tr>=3:y^=1
            addrow(m,a['logits'],y,c,m['query']['kind'],k);stats['queries']+=1
        elif kind=='checkpoint':
            assert key not in pending and m['ephemeral_empty'] and np.array_equal(a['params'],weights[key]) and m['cursor']['table']==tables[key] and m['cursor']['used']==used[key]
            if sm['phase']=='initial' and m['cursor']['completed']==100:inits[(sm['fit'],arm)]=a['params'].copy();init_tables[(sm['fit'],arm)]=tables[key].copy()
            if sm['phase']=='probe_warm' and m['cursor']['completed']==10:probes[arm]=a['params'].copy();probe_tables[arm]=tables[key].copy()
            stats['checkpoints']+=1
        else:raise ValueError('UNKNOWN_KIND:'+kind)
        if sm['phase']=='fixture' and kind in ('cue','update','frozen_receipt','query','fork_match','batch_example','batch_apply'):
            dk=(sm['base'],arm,branch,tr,kind,m.get('cue'),m.get('query',{}).get('kind'),m.get('reconstructed',False),m.get('ordinal'),m.get('query',{}).get('stage'))
            if dk not in delay_groups:delay_groups[dk]=(sm['delay'],{n:v.copy() for n,v in a.items()})
            else:
                od,aa=delay_groups[dk];assert od!=sm['delay'] and aa.keys()==a.keys()
                for n in a:assert np.array_equal(aa[n],a[n]),'DELAY_CHANGED:'+str(dk);dupcomparisons+=1;dupelements+=a[n].size
    assert not pending and not batchlist,'UNFINISHED_PENDING';assert log['intents']==stats['updates']==log['commits']
    exact=json.loads((run/'EXACT.json').read_text()) if (run/'EXACT.json').exists() else [];groups=collections.defaultdict(list)
    for row in exact:groups[(row['phase'],row['base'],row.get('delay',0))].append(row)
    for (phase,base,delay),rr in groups.items():
        labels=tech() if phase in ('fixture','probe') else targets;table={c:labels[c] for c in range(8)};f=[8,10][base] if phase in ('fixture','probe') else base+8
        for row in rr:
            c=row['cue'];y=labels[c]^int(c==f and row['trial']>=3);assert y==row['target'] and row['predicted']==table.get(c) and row['correct']==int(table.get(c)==y)
            if row['kind']=='raw_pre':table[c]=y
    gates=[];calibration={}
    for arm in ('G','L'):
        delta_losses=[];delta_margins=[]
        for fit in range(4):
            rr=[r for r in qrows if r['arm']==arm and r['fit']==fit];warm=[r for r in rr if r['phase']=='warm' and r['kind']=='initial_inventory']
            ds=[r for r in rr if r['phase']=='development'];ns=[r for r in qrows if r['arm']=='N_'+arm and r['fit']==fit and r['phase']=='development']
            def primary(r):
                if r['trial']<2:return False
                sm=plan['sessions'][r['session']];q=sm['transactions'][r['trial']-1]['cue']
                return r['kind'] in ('focal','old') and r['cue']==q
            dd=[r for r in ds if r['branch'] in ('COMMON','B1') and primary(r)];nn=[r for r in ns if primary(r)]
            if len(warm)==8 and len(dd)==20 and len(nn)==20:
                w=sum(r['correct'] for r in warm);d=sum(r['correct'] for r in dd);n=sum(r['correct'] for r in nn)
                dk=[r for r in dd if r['kind']=='focal' and r['trial'] in (3,4,6)];nk=[r for r in nn if r['kind']=='focal' and r['trial'] in (3,4,6)]
                assert len(dk)==len(nk)==12
                bkc=sum(r['correct'] for r in dk);nkc=sum(r['correct'] for r in nk);hh=12-nkc;gain=bkc-nkc;ab=w==8 and d>=16
                gates.append({'arm':arm,'fit':fit,'initial_correct':w,'development_correct':d,'frozen_correct':n,'overall_gain':d-n,'B1_K':bkc,'N_K':nkc,'K':12,'H':hh,'net_gain':gain,'normalized_gain':gain/hh if hh else None,'absolute_pass':bool(ab),'informative':bool(hh>0),'pass':int(ab and hh>0 and 2*gain>=hh)})
            for base in range(4):
                pre=[r for r in ds if r['base']==base and r['branch']=='COMMON' and r['trial']==2 and r['kind']=='old']
                if len(pre)!=8:continue
                for trial in (3,4):
                    post=[r for r in ds if r['base']==base and r['branch']=='B1' and r['trial']==trial and r['kind']=='old']
                    assert len(post)==8
                    delta_losses.append(abs(np.mean([r['loss'] for r in post])-np.mean([r['loss'] for r in pre])))
                    delta_margins.append(abs(np.mean([r['probability_margin'] for r in post])-np.mean([r['probability_margin'] for r in pre])))
        if len(delta_losses)==32:
            ml=float(np.median(delta_losses));mm=float(np.median(delta_margins));calibration[arm]={'median_loss':ml,'median_margin':mm,'tau_loss':min(.01,max(.002,ml)),'tau_margin':min(.02,max(.005,mm)),'observations':32}
    result={'status':'PASS','stats':stats,'log':log,'input_verification':inp,'gate':gates,'calibration':calibration,'heldout_generated':plan['heldout_generated'],'delay_arrays':dupcomparisons,'delay_elements':dupelements}
    if full:
        for name,rr in [('QUERY_ROWS',qrows),('NEGATIVE_QUERY_ROWS',[r for r in qrows if not r['correct']]),('UPDATES',updates),('DERIVATIVES',drows),('EXACT_ROWS',exact),('A0',gates),('BATCH_UPDATES',batchrows)]:write_csv(out/(name+'.csv'),rr)
        decision,pairs,ret,ind,transitions=assess(qrows,calibration,plan)
        for name,rr in [('FIRST_CORRECTION_PAIRS',pairs),('RETENTION_BASE_CHECKPOINT',ret),('RETENTION_INDIVIDUAL',ind),('RECOVERY_TRANSITIONS',transitions)]:write_csv(out/(name+'.csv'),rr)
        (out/'DECISIONS.json').write_text(json.dumps(decision,indent=2,allow_nan=False));result['decisions']=decision
    (out/'AUDIT.json').write_text(json.dumps(result,indent=2,allow_nan=False));return result

def assess(qrows,calibration,plan):
    out={};pairs=[];ret=[];ind=[];transitions=[]
    idx={(r['arm'],r['fit'],r['base'],r['branch'],r['trial'],r['kind'],r['cue'],r['stage']):r for r in qrows if r['phase']=='heldout'}
    def get(arm,fit,base,br,tr,kind,c,stage=None):
        if stage is None:stage='post_extra' if tr==3 and br in ('F','R') else 'post_real'
        return idx[(arm,fit,base,br,tr,kind,c,stage)]
    for arm in ('G','L'):
        if not idx or arm not in calibration:continue
        results={};first=[];tau=calibration[arm]
        for base in range(4,12):
            f=base+8
            for fit in range(4):
                vals={br:get(arm,fit,base,br,3,'focal',f) for br in ('B1','U','F','R')}
                row={'arm':arm,'base':base,'fit':fit}
                for br,v in vals.items():row.update({br+'_correct':v['correct'],br+'_loss':v['loss'],br+'_margin':v['logit_margin']})
                row['R_minus_F_correct']=vals['R']['correct']-vals['F']['correct'];row['R_minus_F_loss']=vals['R']['loss']-vals['F']['loss'];first.append(row);pairs.append(row)
                for br in ('F','R'):
                    for c in [f,*range(8)]:
                        kind='focal' if c==f else 'old';before=get(arm,fit,base,br,3,kind,c,'pre_extra');after=get(arm,fit,base,br,3,kind,c)
                        transitions.append({'arm':arm,'base':base,'fit':fit,'branch':br,'cue':c,'kind':kind,'pre_correct':before['correct'],'post_correct':after['correct'],'broken_to_repaired':int(not before['correct'] and after['correct']),'correct_to_broken':int(before['correct'] and not after['correct']),'loss_change':after['loss']-before['loss'],'margin_change':after['probability_margin']-before['probability_margin']})
        for br in ('U','F','R'):
            rr=[];cells=[]
            endpoints=[(3,'post_extra' if br in ('F','R') else 'post_real'),(4,'post_real'),(5,'post_real'),(6,'post_real')]
            allend=endpoints+([(3,'pre_extra')] if br in ('F','R') else [])
            for base in range(4,12):
                for fit in range(4):
                    for tr,stage in allend:
                        for c in range(8):
                            pre=get(arm,fit,base,'COMMON',2,'old',c);b1=get(arm,fit,base,'B1',tr,'old',c);b=get(arm,fit,base,br,tr,'old',c,stage)
                            rr.append({'arm':arm,'branch':br,'base':base,'fit':fit,'trial':tr,'stage':stage,'cue':c,'pre_correct':pre['correct'],'B1_correct':b1['correct'],'candidate_correct':b['correct'],'lost_prefork_label':int(pre['correct'] and not b['correct']),'additional_error':int(b1['correct'] and not b['correct']),'loss_delta':b['loss']-b1['loss'],'margin_decrease':b1['probability_margin']-b['probability_margin'],'loss':b['loss'],'logit_margin':b['logit_margin'],'probability_margin':b['probability_margin']})
                for tr,stage in allend:
                    zz=[r for r in rr if r['base']==base and r['trial']==tr and r['stage']==stage];assert len(zz)==32
                    dl=float(np.mean([r['loss_delta'] for r in zz]));dm=float(np.mean([r['margin_decrease'] for r in zz]));cells.append({'arm':arm,'branch':br,'base':base,'trial':tr,'stage':stage,'loss_delta':dl,'margin_decrease':dm,'tau_loss':tau['tau_loss'],'tau_margin':tau['tau_margin'],'pass':bool(dl<=tau['tau_loss'] and dm<=tau['tau_margin'])})
            pooled=[]
            for tr,stage in allend:
                zz=[r for r in rr if r['trial']==tr and r['stage']==stage];assert len(zz)==256
                dl=float(np.mean([r['loss_delta'] for r in zz]));dm=float(np.mean([r['margin_decrease'] for r in zz]));pooled.append({'trial':tr,'stage':stage,'correct_old':sum(r['candidate_correct'] for r in zz),'old_total':len(zz),'old_mean_loss':float(np.mean([r['loss'] for r in zz])),'loss_delta':dl,'margin_decrease':dm,'pass':bool(dl<=tau['tau_loss'] and dm<=tau['tau_margin'])})
            recovery=[r for r in rr if (r['trial'],r['stage']) in endpoints];rcells=[r for r in cells+pooled if (r['trial'],r['stage']) in endpoints]
            gainsfit=[sum(r[br+'_correct']-r['B1_correct'] for r in first if r['fit']==i) for i in range(4)];gainsbase=[sum(r[br+'_correct']-r['B1_correct'] for r in first if r['base']==i) for i in range(4,12)]
            efficacy=sum(x>=1 for x in gainsfit)>=3 and sum(x>0 for x in gainsbase)>=6 and float(np.mean([r[br+'_loss']-r['B1_loss'] for r in first]))<=0
            noreg=all(r[br+'_correct']>=r['U_correct'] for r in first);labels=not any(r['lost_prefork_label'] or r['additional_error'] for r in recovery);confidence=all(r['pass'] for r in rcells)
            strictlabels=not any(r['lost_prefork_label'] or r['additional_error'] for r in rr);strictconfidence=all(r['pass'] for r in cells+pooled)
            results[br]={'first_correct':sum(r[br+'_correct'] for r in first),'B1_correct':sum(r['B1_correct'] for r in first),'out_of':32,'efficacy_pass':bool(efficacy),'no_U_first_regressions':bool(noreg),'gain_by_fit':gainsfit,'gain_by_base':gainsbase,'mean_loss':float(np.mean([r[br+'_loss'] for r in first])),'old_label_recovery_pass':labels,'confidence_recovery_pass':confidence,'lost_pre_count':sum(r['lost_prefork_label'] for r in recovery),'extra_errors_vs_B1':sum(r['additional_error'] for r in recovery),'confidence_failing_cells':sum(not r['pass'] for r in cells if (r['trial'],r['stage']) in endpoints),'pooled':pooled,'combined_recovery':bool(efficacy and noreg and labels and confidence),'strict_no_transient_harm':bool(strictlabels and strictconfidence),'strict_labels':strictlabels,'strict_confidence':strictconfidence};ret+=cells;ind+=rr
        out[arm]={'calibration':tau,'branches':results,'R_minus_F_correct':sum(r['R_minus_F_correct'] for r in first),'R_minus_F_loss':float(np.mean([r['R_minus_F_loss'] for r in first])),'selection_inference':'exploratory matched extra-work contrast; B1/U cheaper'}
    return out,pairs,ret,ind,transitions

if __name__=='__main__':print(json.dumps(audit(sys.argv[1],sys.argv[2],full='--full' in sys.argv),indent=2,allow_nan=False))
