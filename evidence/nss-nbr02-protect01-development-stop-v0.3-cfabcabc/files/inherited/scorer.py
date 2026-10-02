"""Independent REV01 semantic/numeric scorer: no producer/model/controller imports.
Boolean/dictionary replay of public receipt history; float64 NumPy independent derivative.
"""
import json,csv,sys,math,hashlib,collections
from pathlib import Path
import numpy as np
from reference_numeric import records,math_reference,check,split,log_check,write_csv,canonical,digest
ROOT=Path(__file__).resolve().parent.parent

def scope(c):return 0 if c in [0,1,2,3,8,9,12,13,14,15] else 1

def independently_verify_plan(plan):
    allocations=json.loads((ROOT/'protocol/SEEDS.json').read_text());seeds={x['label']:x['uint64'] for x in allocations['allocations']}
    for key,v in seeds.items():assert int.from_bytes(hashlib.sha256((allocations['namespace']+'|'+key).encode('ascii')).digest()[:8],'big')==v
    targets={};rngchecks=0
    for group,ranges in [('old',[range(0,4),range(4,8)]),('development',[range(8,10),range(10,12)]),('heldout',[range(12,16),range(16,20)])]:
        if group not in plan['generated_groups']:continue
        for sc,ids in enumerate(ranges):
            g=np.random.Generator(np.random.PCG64(seeds[f'labels/{group}/scope{sc}']));vv=g.permutation(list(ids))
            targets.update({int(c):int(j<len(vv)//2) for j,c in enumerate(vv)})
            assert plan['rng'][f'labels/{group}/scope{sc}']['final']==g.bit_generator.state;rngchecks+=1
    assert targets=={int(k):v for k,v in plan['targets'].items()}
    checked=0;ids={}
    for sid,sm in plan['sessions'].items():
        phase=sm['phase'];tx=sm['transactions']
        if phase in ('initial','probe'):
            key='order/probe' if phase=='probe' else f'order/main/{sm["fit"]}';g=np.random.Generator(np.random.PCG64(seeds[key]));v=[];n=50 if phase=='probe' else 100
            while len(v)<n:v.extend(map(int,g.permutation(8)))
            exp=v[:n];assert plan['rng'][key]['final']==g.bit_generator.state
        elif phase in ('development','heldout','fixture'):
            f,p=sm['focal'],sm['protected'];exp=[f,p,f,f,p,f]
        else:exp=[t['cue'] for t in tx]
        assert len(exp)==len(tx)
        for i,(c,t) in enumerate(zip(exp,tx),1):
            assert c==t['cue'] and scope(c)==t['scope']
            if phase in ('initial','probe','development','heldout'):
                y=targets[c]
                if phase in ('development','heldout') and c==sm['focal'] and i>=3:y^=1
                assert t['target']==y
            if phase=='fixture':
                assert t['target']==(0 if i==1 else 1)
                g=np.random.Generator(np.random.PCG64(seeds[f'fixture/filler/trial{i}']))
                fillers=[int(g.integers(0,4))+4*((1-scope(c)) if j%2==0 else scope(c)) for j in range(32)]
                assert t['fillers']==fillers[:sm['delay']]
            else:assert t['fillers']==[]
            wireseed=seeds[t['wire_key']]
            s=f"REV01-v0.2|{wireseed:016x}|{t['wire_phase']}|{t['wire_base']}|{i}|receipt"
            rid=hashlib.sha256(s.encode('ascii')).digest()[:8].hex();assert rid!='0000000000000000' and t['receipt']==rid
            identity=(t['wire_phase'],t['wire_base'],i)
            if rid in ids:assert ids[rid]==identity
            ids[rid]=identity;checked+=1
    return targets,seeds,{'transactions':checked,'unique_wire_receipts':len(ids),'rng_groups':rngchecks}

def initial_expected(sm,seeds):
    if sm['phase']=='derivative':
        W=np.zeros((16,23));U=np.zeros((16,16));b=np.zeros(16);V=np.zeros((2,16));a=np.zeros(2)
        U[0,0]=U[1,1]=.5;V[1,1]=1
        if sm['coupled']:U[1,0]=.5
        if sm['nonlinear']:W[0,22]=.4
    else:
        key='init/main/'+str(sm['fit']) if sm['phase']=='initial' else ('init/probe' if sm['phase']=='probe' else 'init/fixture')
        g=np.random.Generator(np.random.PCG64(seeds[key]));W=g.uniform(-np.sqrt(6/39),np.sqrt(6/39),(16,23));U=g.uniform(-.05,.05,(16,16))+np.eye(16)*.25;b=np.zeros(16);V=g.uniform(-.02,.02,(2,16));a=np.zeros(2)
    return np.concatenate([v.astype('f4').ravel() for v in (W,U,b,V,a)])

def audit(run,out,full=False):
    run=Path(run);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((run/'private/PLAN.json').read_text());targets,seeds,inp=independently_verify_plan(plan)
    stats={'scalar_checks':0,'max_tolerance_ratio':0.,'frames':0,'updates':0,'queries':0,'forks':0,'expected_faults':0,'checkpoints':0,'filler_steps':0}
    log,events=log_check(run/'worker/events.jsonl')
    if log['unknown_attempts']:raise ValueError('UNKNOWN_COMPLETION')
    event_by_seq={e['sequence']:e for e in events};intent_count=0
    evidence={e['frame']['index']:e for e in events if e['event']=='EVIDENCE_DURABLE'}
    releases=collections.defaultdict(list)
    for e in events:
        if e['event']=='FEEDBACK_RELEASED':releases[(e['context']['session'],e['context']['branch'],e['receipt'])].append(e)
    weights={};tables={};used={};pending={};cues={};forks={};inits={};init_tables={};qrows=[];updates=[];drows=[];fork_rows=[];delay_groups={};dupcomparisons=0;dupelements=0
    def contextrow(m):
        sm=plan['sessions'][m['context']['session']]
        return {'session':m['context']['session'],'phase':sm['phase'],'method':sm['method'],'arm':m['arm'],'fit':sm['fit'],'base':sm.get('base',-1),'delay':sm.get('delay',0),'branch':m['context']['branch'],'trial':m['context'].get('trial',0)}
    def addrow(m,z,y,cue,kind,k):
        z=np.asarray(z,dtype=float);p=np.exp(z-z.max());p/=p.sum()
        qrows.append({**contextrow(m),'frame':k,'kind':kind,'cue':cue,'scope':scope(cue),'target':y,'predicted':int(z.argmax()),'correct':int(z.argmax()==y),'loss':float(np.logaddexp.reduce(z)-z[y]),'logit_margin':float(z[y]-z[1-y]),'probability_margin':float(p[y]-p[1-y]),'logit0':float(z[0]),'logit1':float(z[1])})
    for k,m,a in records(run/'worker/records.bin'):
        stats['frames']+=1;kind=m['kind'];ctx=m['context'];sid=ctx['session'];branch=ctx['branch'];key=(sid,branch);sm=plan['sessions'][sid];arm=m['arm'];tr=ctx.get('trial',0)
        assert k in evidence
        if kind=='load':
            assert key not in weights;weights[key]=a['params']
            if branch=='B2':assert np.array_equal(weights[key],forks[sid]['params'])
            elif sm['phase'] in ('initial','probe','fixture','sandbox','derivative'):assert np.array_equal(weights[key],initial_expected(sm,seeds))
            else:assert np.array_equal(weights[key],inits[(sm['fit'],sm['method'])]),'INITIAL_CHECKPOINT'
        elif kind=='management_load':
            tables[key]=m['table'];used[key]=m['used']
            if branch=='B2':assert tables[key]==forks[sid]['table'] and not used[key]
            elif sm['phase'] in ('initial','probe','fixture','sandbox','derivative'):assert tables[key]=={} and not used[key]
            else:assert tables[key]==init_tables[(sm['fit'],sm['method'])] and not used[key]
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
            assert old is not None and old['label']!=tx['target'] and not used[key]
            assert np.array_equal(a['params'],weights[key]) and m['table']==tables[key]
            forks[sid]={'params':a['params'],'table':tables[key].copy(),'frame':k,'ref':pending.pop(key),'trial':tr}
            weights[(sid,'B1')]=weights[key].copy();tables[(sid,'B1')]=tables[key].copy();used[(sid,'B1')]=False;pending[(sid,'B1')]=forks[sid]['ref'];stats['forks']+=1
        elif kind=='fork_match':
            assert m['bitwise_forward_gradient'] and m['distinct_mutable_storage'];forks[sid]['gradient']=a['raw_gradient']
        elif kind in ('update','frozen_receipt','derivative'):
            ci=pending.pop(key);cm,ca,ref=cues[ci];tx=sm['transactions'][tr-1];assert tx['target']==m['target'] and ci==m['cue_ref']['index']
            if kind=='derivative':
                check(a['raw_gradient'],ref[arm],'derivative_'+arm,stats)
                eg=ref['G'][:640];el=ref['L'][:640];gn=float(np.linalg.norm(eg));diff=float(np.linalg.norm(eg-el))
                if not sm['coupled']:check(ref['G'],ref['L'],'diagonal',stats)
                if sm['coupled'] and not sm['nonlinear']:assert abs(gn*gn-47/32)<1e-12 and abs(diff*diff-3/8)<1e-12
                drows.append({**contextrow(m),'relative_difference':None if gn<1e-12 else diff/gn});continue
            assert m['table_before']==tables[key]
            old=tables[key].get(f'{tx["scope"]}:{tx["cue"]}');change=(old is not None and old['label']!=tx['target'] and not used[key]);assert m['changed']==change
            assert m['used']==(used[key] or change)
            expected_clip=2. if branch=='B2' and tr==forks[sid]['trial'] else 1.;assert m['clip']==expected_clip
            pe=event_by_seq[m['prediction_sequence']];assert pe['event']=='PREDICTION_BEFORE_FEEDBACK' and pe['receipt']==m['receipt']
            rel=releases[(sid,branch,m['receipt'])];assert any(pe['sequence']<e['sequence']<evidence[k]['sequence'] for e in rel)
            if kind=='update':
                g=a['raw_gradient'];check(g,ref[arm],'raw_'+arm,stats);norm=float(np.linalg.norm(g.astype(float)));fac=min(1.,expected_clip/norm) if norm else 1.;check(a['norm_factor'],[norm,fac],'norm_factor',stats)
                expected=ca['params'].astype(float)-g.astype(float)*fac;defect=m['defect']
                if defect:
                    assert sm['phase']=='sandbox';assert not np.allclose(a['post'],expected,atol=2e-6,rtol=2e-5)
                    scale=-1 if defect=='sign' else 2;check(a['post'],ca['params'].astype(float)-g.astype(float)*fac*scale,'injected_step',stats);stats['expected_faults']+=1
                else:check(a['post'],expected,'SGD_application',stats)
                if branch in ('B1','B2') and change:assert np.array_equal(g,forks[sid]['gradient']),'FORK_RAW_GRADIENT'
                eg=ref['G'][:640];el=ref['L'][:640];gn=float(np.linalg.norm(eg));ln=float(np.linalg.norm(el));difference=float(np.linalg.norm(eg-el))
                updates.append({**contextrow(m),'frame':k,'cue_frame':ci,'receipt':m['receipt'],'cue':tx['cue'],'target':tx['target'],'clip':expected_clip,'raw_norm':norm,'clip_factor':fac,'step_norm':float(np.linalg.norm(a['post'].astype(float)-ca['params'])),'changed':int(change),'loss_before':float(np.logaddexp.reduce(ca['logits'].astype(float))-ca['logits'][tx['target']]),'encoder_gradient_relative_difference':None if gn<1e-12 else difference/gn,'encoder_cosine':None if gn*ln<1e-24 else float(eg@el/(gn*ln)),'defect':defect or ''})
                stats['updates']+=1
            else:assert np.array_equal(a['post'],ca['params']),'FROZEN_MUTATION'
            assert m['post_digest']==digest(a['post'].tobytes())
            tnew=tables[key].copy();tnew[f'{tx["scope"]}:{tx["cue"]}']={'label':tx['target'],'receipt':m['receipt'],'pre_version':m['pre_digest'],'post_version':m['post_digest']};assert tnew==m['table_after']
            tables[key]=tnew;used[key]=m['used'];weights[key]=a['post']
        elif kind=='query':
            assert key not in pending and m['readonly'] and m['parameter_version']==digest(weights[key].tobytes())
            assert m['codes']==[22,20+scope(m['cue']),m['cue']]
            ref=math_reference(weights[key],m['codes'])
            for n in ('h','logits','probabilities'):check(a[n],ref[n],'query/'+n,stats)
            c=m['cue']
            if sm['phase']=='fixture':y={0:0,1:1,2:0,3:1,4:1,5:0,6:1,7:0}[c]
            else:y=targets[c]
            if sm['phase'] in ('fixture','development','heldout') and c==sm.get('focal') and tr>=3:y^=1
            addrow(m,a['logits'],y,c,m['query']['kind'],k);stats['queries']+=1
        elif kind=='checkpoint':
            assert key not in pending and m['ephemeral_empty'] and np.array_equal(a['params'],weights[key]) and m['cursor']['table']==tables[key] and m['cursor']['used']==used[key]
            if sm['phase']=='initial' and m['cursor']['completed']==100:
                inits[(sm['fit'],arm)]=a['params'].copy();init_tables[(sm['fit'],arm)]=tables[key].copy()
            stats['checkpoints']+=1
        else:raise ValueError('UNKNOWN_KIND:'+kind)
        if sm['phase']=='fixture' and kind in ('cue','update','frozen_receipt','query','fork_match'):
            dkey=(arm,branch,tr,kind,m.get('cue'),m.get('query',{}).get('kind'),m.get('reconstructed',False))
            if dkey not in delay_groups:delay_groups[dkey]=(sm['delay'],{n:v.copy() for n,v in a.items()})
            else:
                od,aa=delay_groups[dkey];assert od!=sm['delay']
                assert aa.keys()==a.keys()
                for n in a:assert np.array_equal(aa[n],a[n]),'DELAY_CHANGED:'+str(dkey);dupcomparisons+=1;dupelements+=a[n].size
    assert not pending,'UNFINISHED_PENDING'
    assert log['intents']==stats['updates']==log['commits']
    # Independently verify public exact controls by rebuilding last-observed tables.
    exact=json.loads((run/'EXACT.json').read_text()) if (run/'EXACT.json').exists() else []
    groups=collections.defaultdict(list)
    for r in exact:groups[(r['phase'],r['base'])].append(r)
    for (phase,base),rr in groups.items():
        table={} if phase=='fixture' else {c:targets[c] for c in range(8)}
        f=0 if phase=='fixture' else next(sm['focal'] for sm in plan['sessions'].values() if sm['phase']==phase and sm.get('base')==base)
        for r in rr:
            c=r['cue'];y=({0:0,1:1,2:0,3:1,4:1,5:0,6:1,7:0}[c] if phase=='fixture' else targets[c]) ^ int(c==f and r['trial']>=3)
            assert y==r['target'];assert r['predicted']==table.get(c) and r['correct']==int(table.get(c)==y)
            if r['kind']=='raw_pre':table[c]=y
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
                gates.append({'arm':arm,'fit':fit,'initial_correct':w,'development_correct':d,'frozen_correct':n,'gain':d-n,'pass':int(w==8 and d>=16 and d-n>=4)})
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
        write_csv(out/'QUERY_ROWS.csv',qrows);write_csv(out/'NEGATIVE_QUERY_ROWS.csv',[r for r in qrows if not r['correct']]);write_csv(out/'UPDATES.csv',updates);write_csv(out/'DERIVATIVES.csv',drows);write_csv(out/'EXACT_ROWS.csv',exact);write_csv(out/'A0.csv',gates)
        decision,paired,retention,violations=assess(qrows,updates,calibration)
        write_csv(out/'FIRST_CORRECTION_PAIRS.csv',paired);write_csv(out/'RETENTION_BASE_CHECKPOINT.csv',retention);write_csv(out/'RETENTION_INDIVIDUAL.csv',violations)
        (out/'DECISIONS.json').write_text(json.dumps(decision,indent=2,allow_nan=False));result['decisions']=decision
    (out/'AUDIT.json').write_text(json.dumps(result,indent=2,allow_nan=False));return result

def assess(qrows,updates,calibration):
    out={};paired=[];retention=[];violations=[]
    idx={(r['arm'],r['fit'],r['base'],r['branch'],r['trial'],r['kind'],r['cue']):r for r in qrows if r['phase']=='heldout'}
    ud={(r['arm'],r['fit'],r['base'],r['branch'],r['trial']):r for r in updates if r['phase']=='heldout'}
    for arm in ('G','L'):
        if arm not in calibration or not idx:continue
        tau=calibration[arm];pairs=[];rp=[];bad=[]
        for base in range(4,12):
            f=base+8
            for fit in range(4):
                one=idx[(arm,fit,base,'B1',3,'focal',f)];two=idx[(arm,fit,base,'B2',3,'focal',f)]
                r={'arm':arm,'base':base,'fit':fit,'target':one['target'],'B1_correct':one['correct'],'B2_correct':two['correct'],'gain':two['correct']-one['correct'],'B1_loss':one['loss'],'B2_loss':two['loss'],'B1_margin':one['probability_margin'],'B2_margin':two['probability_margin'],'raw_norm':ud[(arm,fit,base,'B1',3)]['raw_norm'],'B1_update_frame':ud[(arm,fit,base,'B1',3)]['frame'],'B2_update_frame':ud[(arm,fit,base,'B2',3)]['frame']};pairs.append(r)
                for tr in (3,4,5,6):
                    for c in range(8):
                        pre=idx[(arm,fit,base,'COMMON',2,'old',c)];a=idx[(arm,fit,base,'B1',tr,'old',c)];b=idx[(arm,fit,base,'B2',tr,'old',c)]
                        bad.append({'arm':arm,'base':base,'fit':fit,'trial':tr,'cue':c,'pre_correct':pre['correct'],'B1_correct':a['correct'],'B2_correct':b['correct'],'lost_prefork_label':int(pre['correct'] and not b['correct']),'additional_B2_error':int(a['correct'] and not b['correct']),'loss_delta':b['loss']-a['loss'],'margin_decrease':a['probability_margin']-b['probability_margin'],'B1_loss':a['loss'],'B2_loss':b['loss'],'B1_margin':a['probability_margin'],'B2_margin':b['probability_margin']})
            for tr in (3,4,5,6):
                bb=[r for r in bad if r['base']==base and r['trial']==tr];dl=float(np.mean([r['loss_delta'] for r in bb]));dm=float(np.mean([r['margin_decrease'] for r in bb]))
                rp.append({'arm':arm,'base':base,'trial':tr,'count':len(bb),'loss_delta':dl,'margin_decrease':dm,'tau_loss':tau['tau_loss'],'tau_margin':tau['tau_margin'],'loss_pass':int(dl<=tau['tau_loss']+1e-12),'margin_pass':int(dm<=tau['tau_margin']+1e-12)})
        gainsfit=[sum(r['gain'] for r in pairs if r['fit']==i) for i in range(4)];gainsbase=[sum(r['gain'] for r in pairs if r['base']==i) for i in range(4,12)]
        effic=(sum(x>=1 for x in gainsfit)>=3 and sum(x>0 for x in gainsbase)>=6 and np.mean([r['B2_loss']-r['B1_loss'] for r in pairs])<=1e-12)
        labelpass=not any(r['lost_prefork_label'] or r['additional_B2_error'] for r in bad)
        confpass=all(r['loss_pass'] and r['margin_pass'] for r in rp)
        pooled=[]
        for tr in (3,4,5,6):
            bb=[r for r in bad if r['trial']==tr];dl=float(np.mean([r['loss_delta'] for r in bb]));dm=float(np.mean([r['margin_decrease'] for r in bb]));pp=dl<=tau['tau_loss']+1e-12 and dm<=tau['tau_margin']+1e-12;confpass=confpass and pp;pooled.append({'trial':tr,'loss_delta':dl,'margin_decrease':dm,'pass':bool(pp)})
        out[arm]={'B1_correct':sum(r['B1_correct'] for r in pairs),'B2_correct':sum(r['B2_correct'] for r in pairs),'total':32,'gain_by_fit':gainsfit,'gain_by_base':gainsbase,'mean_B1_loss':float(np.mean([r['B1_loss'] for r in pairs])),'mean_B2_loss':float(np.mean([r['B2_loss'] for r in pairs])),'efficacy_pass':bool(effic),'old_label_pass':bool(labelpass),'old_confidence_pass':bool(confpass),'overall_pass':bool(effic and labelpass and confpass),'lost_prefork_label_count':sum(r['lost_prefork_label'] for r in bad),'additional_label_error_count':sum(r['additional_B2_error'] for r in bad),'confidence_failing_base_checkpoints':sum(not(r['loss_pass'] and r['margin_pass']) for r in rp),'pooled_confidence':pooled,'calibrated_limits':tau}
        paired+=pairs;retention+=rp;violations+=bad
    return out,paired,retention,violations
if __name__=='__main__':
    print(json.dumps(audit(sys.argv[1],sys.argv[2],full='--full' in sys.argv),indent=2,allow_nan=False))
