"""One deterministic capture or genuine adaptive replay of the frozen bridge study."""
from __future__ import annotations
import argparse,json,random,sys,time
from pathlib import Path
import numpy as np,torch
from common import CFG,ROOT,Journal,arrhash,canon,json_write,npz,seed,sha,source_check
from data import training,a_truth,labels,b_prefix,evaluation,suffix,cue_order
from model import setup,init,load,a_loss,b_loss,sgd,NAMES
from pinning import PinnedStates


def checkpoint(folder,step,m,opt,gen,data_state):
    p=folder/f'checkpoint_{step:04d}.pt'
    torch.save({'model':m.state_dict(),'optimizer':opt.state_dict(),'torch_rng':torch.get_rng_state(),
     'python_rng':random.getstate(),'numpy_rng':np.random.get_state(),'init_generator':gen.get_state(),
     'data_generation_final_rng':data_state,'next_update':step,'source_lock':source_check()},p)


def train_fit(folder,name,j,steps=2000,batch=16):
    folder.mkdir(parents=True,exist_ok=False)
    m,gen=init(name);opt=torch.optim.Adam(m.parameters(),lr=CFG['initial_lr'],foreach=False,fused=False)
    ev,lens,st=training(name,steps,batch);y=labels();bseq=b_prefix(range(4))
    # Actual complete initial training inputs retained. State targets are separately reproducible.
    npz(folder/'INPUTS.npz',events=ev,lengths=lens,b_labels=y,b_events=bseq)
    npz(folder/'initial.npz',**m.weights());checkpoint(folder,0,m,opt,gen,st)
    logfile=open(folder/'TRAINING.jsonl','x')
    for u in range(steps):
        n=int(lens[u]);e=ev[u,:,:n].copy();bits,nxt,packed=a_truth(e)
        ref=j.intent(f'{name}/fit/{u}',updates=1,backwards=1,cells=batch*n+12,heads=batch*n+12,
                     inputs=arrhash({'A':e,'packed':packed,'B':bseq,'target_B':y}),pre=m.ident())
        opt.zero_grad(set_to_none=True);_,oa=m.roll(e);_,ob=m.roll(bseq)
        la=a_loss(oa,bits,nxt);lb=b_loss(ob,y);loss=la+lb
        loss.backward();grad=torch.nn.utils.clip_grad_norm_(m.parameters(),1.,error_if_nonfinite=True)
        grad_hash=arrhash({k:p.grad.detach().numpy() for k,p in m.named_parameters()})
        opt.step()
        if any(not torch.isfinite(p).all() for p in m.parameters()):raise RuntimeError('NONFINITE_TRAINED_PARAMETER')
        out={'update':u+1,'length':n,'loss':float(loss.detach()),'A_loss':float(la.detach()),'B_loss':float(lb.detach()),
             'unclipped_norm':float(grad),'clipped_gradient_hash':grad_hash,'post':m.ident()}
        logfile.write(canon(out).decode()+'\n');logfile.flush()
        # Post-weight identity and finite losses acknowledged durably, full checkpoints every 250.
        j.commit(ref,**out)
        if (u+1)%250==0 or u+1==steps:
            checkpoint(folder,u+1,m,opt,gen,st)
            print(json.dumps({'phase':'initial_fit','fit':name,'step':u+1,'loss':out['loss']}),flush=True)
    logfile.close();npz(folder/'terminal.npz',**m.weights())
    # 32 literal previously observed length-17 examples; replay targets use their recorded semantics.
    pool=np.concatenate([ev[0,:,:17],ev[2,:,:17]],axis=0) if steps>=3 else np.tile(ev[0,:,:17],(2,1))
    npz(folder/'REPAIR_POOL.npz',events=pool)
    return m,pool


def forward_b(m,j,op):
    es=b_prefix(range(4));ref=j.intent(op,cells=12,heads=12,weights=m.ident())
    with torch.no_grad():hs,ls=m.roll(es)
    out={'events':es,'states':hs.numpy(),'logits':ls[:,-1].numpy()}
    j.commit(ref,result=arrhash(out));return out


def online_step(m,c,y,folder,k,j,lr):
    e=b_prefix([c]);ref=j.intent(f'{folder.name}/online{k}',updates=1,backwards=1,cells=3,heads=3,
                                cue=int(c),pre=m.ident())
    hs,ls=m.roll(e)
    # Prediction exists before the receipt target is supplied to the loss.
    observed=ls.detach().numpy().copy();loss=b_loss(ls,np.array([y]))
    pre,g,post,sc,prod=sgd(m,loss,lr)
    arrays={'pre':pre,'gradient':g,'post':post,'stats':sc,'product':prod,'B_events':e,
            'B_labels':np.array([y],np.int64),'B_logits':observed,'B_states':hs.detach().numpy()}
    npz(folder/f'update_{k:02d}.npz',**arrays)
    j.commit(ref,evidence=f'update_{k:02d}.npz',evidence_hash=arrhash(arrays),post=m.ident(),receipt=f'{folder.name}/receipt/{k}')


def repair_step(m,events,current,folder,k,j):
    B,T=events.shape;bits,nxt,packed=a_truth(events);be=b_prefix(range(4))
    ref=j.intent(f'{folder.name}/repair{k}',updates=1,backwards=1,cells=B*T+12,heads=B*T+12,
       evidence=arrhash({'A':events,'B':be,'labels':current}),pre=m.ident())
    hs,la=m.roll(events);hb,lb=m.roll(be);loss=a_loss(la,bits,nxt)+b_loss(lb,current)
    pre,g,post,sc,prod=sgd(m,loss,CFG['repair_lr'])
    a={'pre':pre,'gradient':g,'post':post,'stats':sc,'product':prod,'A_events':events,'A_logits':la.detach().numpy(),
       'A_states':hs.detach().numpy(),'B_events':be,'B_labels':current.copy(),'B_logits':lb.detach().numpy(),'B_states':hb.detach().numpy()}
    npz(folder/f'update_{k:02d}.npz',**a)
    j.commit(ref,evidence=f'update_{k:02d}.npz',evidence_hash=arrhash(a),post=m.ident(),kind_record='REHEARSAL_NOT_NEW_RECEIPT')


def reconstruct(m,d,j,op):
    ev,ls=d['events'],d['lengths'];h=np.zeros((len(ev),64),np.float32)
    # Grouping by public length is identical before/after; bytes can be compared at unchanged weights.
    states=np.zeros((len(ev),ev.shape[1],64),np.float32);logits=np.zeros((len(ev),ev.shape[1],9),np.float32)
    ref=j.intent(op,cells=int(ls.sum()),heads=int(ls.sum()),weights=m.ident(),prefix=arrhash(d))
    with torch.no_grad():
        for n in sorted(set(map(int,ls))):
            ii=np.flatnonzero(ls==n);hh,ll=m.roll(ev[ii,:n]);states[ii,:n]=hh.numpy();logits[ii,:n]=ll.numpy();h[ii]=hh[:,-1].numpy()
    j.commit(ref,states=arrhash({'h':h,'prefix_states':states,'prefix_logits':logits}))
    return h,states,logits


def resume(m,h,s,j,op):
    es=np.tile(s,(len(h),1));ref=j.intent(op,cells=len(h)*len(s),heads=len(h)*(len(s)+1),weights=m.ident(),state=arrhash({'h':h}))
    with torch.no_grad():
        ht=torch.from_numpy(h.copy());first=m.head(ht);hs,ls=m.roll(es,ht)
        states=torch.cat([ht[:,None,:],hs],dim=1).numpy();out=torch.cat([first[:,None,:],ls],dim=1).numpy()
    j.commit(ref,result=arrhash({'states':states,'logits':out}));return states,out


def assess_context(m0,pool,d,split,fit,case,cue,order,folder,j):
    folder.mkdir(parents=True,exist_ok=False);m=load(m0.weights());y0=labels();cur=y0.copy();cur[cue]=1-cur[cue]
    stream=cue_order(cue,order);s=suffix(cue)
    h0,ph,pl=reconstruct(m0,d,j,f'{folder.name}/prepare_A')
    hbytes=h0.tobytes();h0.setflags(write=False);parent=m0.ident();registry=PinnedStates(parent,h0,arrhash(d))
    meta={'fit':fit,'split':split,'case':case,'focal_cue':cue,'order':order,'public_order':stream.tolist(),
          'old_B_labels':y0.tolist(),'parameter_parent':parent,'A_prefix_hash':arrhash(d),
          'state_producer':parent,'A_state_hash':sha(hbytes),'slots_are_supplied_metadata':True}
    json_write(folder/'CONTEXT.json',meta);npz(folder/'PUBLIC.npz',**d,suffix=s,initial_h=h0,initial_prefix_states=ph,initial_prefix_logits=pl)
    npz(folder/'weights_0.npz',**m.weights())
    versions=[]
    for stage in range(3):
        if stage==1:
            for k,c in enumerate(stream):
                # For other cues, old lawful targets persist. Focal changed label is first released here.
                online_step(m,int(c),int(cur[c]),folder,k,j,CFG['online_lr'])
                b=forward_b(m,j,f'{folder.name}/post_online{k}');npz(folder/f'B_post_update_{k:02d}.npz',**b)
            npz(folder/'weights_1.npz',**m.weights())
        elif stage==2:
            for q in range(4):
                k=8+q;repair_step(m,pool[q*8:(q+1)*8],cur,folder,k,j)
                b=forward_b(m,j,f'{folder.name}/post_repair{k}');npz(folder/f'B_post_update_{k:02d}.npz',**b)
            npz(folder/'weights_2.npz',**m.weights())
        if h0.tobytes()!=hbytes or m0.ident()!=parent:raise RuntimeError('PINNED_STATE_OR_WEIGHTS_CHANGED')
        hr,rh,rl=reconstruct(m,d,j,f'{folder.name}/stage{stage}/REBUILD')
        result={'rebuilt_h':hr,'prefix_states':rh,'prefix_logits':rl}
        for mode,h in [('CARRY',h0),('REBUILD',hr),('RESET',np.zeros_like(h0))]:
            st,out=resume(m,h,s,j,f'{folder.name}/stage{stage}/{mode}')
            result[mode+'_states']=st;result[mode+'_logits']=out
        # A real parameter-version route back to the frozen task revision, not a gold-answer replacement.
        st,out=resume(m0,registry.read(m0.ident()),s,j,f'{folder.name}/stage{stage}/PINNED')
        result['PINNED_states']=st;result['PINNED_logits']=out
        if stage==0 and (not np.array_equal(result['CARRY_logits'],result['REBUILD_logits']) or not np.array_equal(hr,h0)):
            raise RuntimeError('UNCHANGED_REBUILD_MISMATCH')
        npz(folder/f'A_stage_{stage}.npz',**result)
        b=forward_b(m,j,f'{folder.name}/stage{stage}/B');npz(folder/f'B_stage_{stage}.npz',**b)
        frozen=forward_b(m0,j,f'{folder.name}/stage{stage}/B_PINNED');npz(folder/f'B_PINNED_stage_{stage}.npz',**frozen)
        versions.append(m.ident())
    json_write(folder/'COMPLETE.json',{'parent':parent,'versions':versions,'saved_state_unchanged':True,'receipts':8,'repair_updates':4,
        'pending_feedback_at_boundary':False,'no_heldout_A_labels_used_for_learning':True,'one_shared_pinned_weight_copy':True,
        'task_states':32,'state_bytes':h0.nbytes,'pinned_parameter_bytes':sum(v.nbytes for v in m0.weights().values()),
        'B_new_label':int(cur[cue]),'concurrency_note':'Separate logical task states, serial execution. Not concurrent-thread or service publication testing.'})


def competence(m,d,j,fit,folder):
    folder.mkdir(parents=True,exist_ok=False);h,ps,pl=reconstruct(m,d,j,f'gate/{fit}/prefix')
    s=suffix(0);carry,co=resume(m,h,s,j,f'gate/{fit}/CARRY');zero,zo=resume(m,np.zeros_like(h),s,j,f'gate/{fit}/RESET')
    hr,_,_=reconstruct(m,d,j,f'gate/{fit}/REBUILD');rb,ro=resume(m,hr,s,j,f'gate/{fit}/REBUILD_READ')
    b=forward_b(m,j,f'gate/{fit}/B')
    if not np.array_equal(co,ro) or not np.array_equal(h,hr):raise RuntimeError('A0_REPLAY_ERROR')
    truth=[]
    for e,n in zip(d['events'],d['lengths']):
        bits,nxt,_=a_truth(np.r_[e[:n],s]);ix=[int(n)-1]+[int(n)+i-1 for i in range(1,9)]
        truth.append(np.column_stack([bits[0,ix],nxt[0,ix]]))
    truth=np.stack(truth);pos=CFG['read_positions']
    def score(o):
        return np.mean(np.all((o[:,pos,:4]>0)==truth[:,pos,:4],axis=-1)&(np.argmax(o[:,pos,4:],axis=-1)==truth[:,pos,4]))
    ac,az=float(score(co)),float(score(zo));bc=int(((b['logits'][:,0]>0)==labels()).sum())
    passed=ac>=CFG['a0_joint_min'] and bc==4 and ac-az>=CFG['a0_state_advantage']
    npz(folder/'EVIDENCE.npz',**d,suffix=s,h=h,prefix_states=ps,prefix_logits=pl,carry=co,reset=zo,rebuild=ro,truth=truth,**{'B_'+k:v for k,v in b.items()})
    rec={'fit':fit,'A_joint':ac,'RESET_joint':az,'A_B_advantage':ac-az,'B_correct':bc,'pass':bool(passed),'old_weight_identity':m.ident()}
    json_write(folder/'DECISION.json',rec);return rec


def fixtures(folder,j):
    folder.mkdir();m,_=init('fixture');g=np.random.Generator(np.random.PCG64(seed('fixture/A')))
    e=g.integers(0,9,(32,17),dtype=np.uint8);cur=labels()
    for k in range(4):online_step(m,k,int(cur[k]),folder,k,j,CFG['online_lr'])
    for q in range(4):repair_step(m,e[q*8:(q+1)*8],cur,folder,4+q,j)
    # These are ordinary numeric-array update defects, not extra learner fits.
    controls=[]
    for k in range(4):
        pre=np.array([1.,-2.,.125],np.float32);grad=np.array([.5,-.25,.1],np.float32)
        expected=pre-np.float32(.1)*grad
        wrong=pre+np.float32(.1)*grad if k%2==0 else pre-np.float32(.2)*grad
        ref=j.intent('sandbox/update'+str(k),updates=1)
        a={'pre':pre,'gradient':grad,'expected':expected,'actual':wrong};npz(folder/f'BAD_{k}.npz',**a)
        detected=not np.array_equal(expected,wrong);assert detected
        j.commit(ref,deliberate_fault=True,detected=detected);controls.append({'fault':k,'detected':detected})
    # Version key and task-buffer identity must not silently follow mutable "latest".
    state=np.array([[.2,.3]],np.float32);old=state.copy();registry=PinnedStates('a'*64,state,'fixture-prefix')
    candidate=registry.read('a'*64);candidate+=1
    checks={'independent_scratch':np.array_equal(registry.read('a'*64),old)}
    for name,key in [('foreign_version','b'*64),('missing_version',None)]:
        try:registry.read(key)
        except ValueError:checks[name]=True
        else:checks[name]=False
    assert all(checks.values());json_write(folder/'CONTRACTS.json',{'numeric_faults':controls,'actual_registry_checks':checks,
      'scope':'Local version/state routing only. No credentials, serving-atomicity, or full receipt-security claim.'})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=False);source_check();setup();j=Journal(out/'audit')
    json_write(out/'START.json',{'source_lock':source_check(),'config':CFG,'all_seeds':{n:seed(n) for n in ['initial/B_labels','eval/dev','eval/test']}})
    status='INCOMPLETE'
    try:
        fixtures(out/'fixtures',j)
        from preflight import check as independent_fixture_check
        independent_fixture_check(out/'fixtures')
        # Source/schema cap proof is a conservative format bound, not an accuracy-oriented probe.
        probe,_=train_fit(out/'probe','cost_probe',j,CFG['probe_updates'],16)
        del probe
        models=[];pools=[];dev,_=evaluation('dev');npz(out/'DEV_INPUTS.npz',**dev)
        for f in range(4):
            m,p=train_fit(out/f'train/fit{f}',str(f),j);models.append(m);pools.append(p)
        json_write(out/'INITIAL_LOCK.json',{'weights':[m.ident() for m in models],'test_generated':False})
        gates=[competence(m,dev,j,f,out/f'gate/fit{f}') for f,m in enumerate(models)]
        json_write(out/'A0.json',{'fits':gates,'pass':sum(x['pass'] for x in gates)>=3,'test_generated':False})
        if sum(x['pass'] for x in gates)<3:
            status='STOPPED_AT_A0';return
        for f,m in enumerate(models):
            for c,(cue,o) in enumerate(CFG['dev_scenarios']):
                assess_context(m,pools[f],dev,'dev',f,c,cue,o,out/f'contexts/dev_f{f}_c{c}',j)
        # No development-outcome thresholds or source changes. All fits retained after group admission.
        json_write(out/'PRE_TEST_LOCK.json',{'A0':True,'weights':[m.ident() for m in models],'source':source_check(),'dev_did_not_select_anything':True})
        test,st=evaluation('test');npz(out/'TEST_INPUTS.npz',**test)
        json_write(out/'TEST_GENERATOR.json',{'seed':seed('eval/test'),'final_state':st})
        for f,m in enumerate(models):
            for c,(cue,o) in enumerate(CFG['test_scenarios']):
                assess_context(m,pools[f],test,'test',f,c,cue,o,out/f'contexts/test_f{f}_c{c}',j)
            print(json.dumps({'phase':'contexts_complete','fit':f,'counts':j.count}),flush=True)
        status='COMPLETE'
    finally:
        j.close();json_write(out/'STATUS.json',{'status':status,'counts':j.count,'source_unchanged':source_check(),'test_generated':(out/'TEST_INPUTS.npz').exists()})
if __name__=='__main__':main()
