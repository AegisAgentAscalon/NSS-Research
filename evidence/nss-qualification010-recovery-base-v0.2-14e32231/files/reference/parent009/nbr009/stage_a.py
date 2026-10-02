"""Stage A: clean distinct ownership and register/write/read interference."""
from .common import *
from .state import N
from .episodes import paired,build_state
from .readout import neural_read,exact_owner_read

FAMILIES=('ordinary','source01','source10','room01','middle01','both01')
# Candidate preparation is separately controlled from information-rich exact ownership.
VARIANTS=(('identity','identity','parent','resolved','nearest'),
          ('parent','learned','parent','resolved','nearest'),
          ('ordinary','learned','ordinary','resolved','nearest'),
          ('near','learned','near','resolved','nearest'),
          ('guard_parent','guarded','parent','resolved','nearest'),
          ('guard_near','guarded','near','resolved','nearest'),
          ('reject','identity','parent','resolved','nearest'),
          ('obs_A_identity','identity','parent','observed','A_nearest'),
          ('obs_B_identity','identity','parent','observed','B_nearest'),
          ('obs_B_parent','learned','parent','observed','B_nearest'),
          ('obs_B_near','learned','near','observed','B_nearest'))

@torch.no_grad()
def run(pair,path,b=64,development=False,variants=None,families=None):
    setup();ms,head,cfg=load_pair(pair);before=model_hashes(ms);arrays={};config=[]
    for fi,family in enumerate(families or FAMILIES):
        seed=(71900000 if development else 72900000)+pair*1000+fi*31
        p=paired(seed,b,family);r=np.arange(b);ids=p['ids'];old,new,room0,room1,room2,mid0,mid1,nb=[ids[:,j] for j in range(8)]
        for name,mode,kind,track,method in (variants or VARIANTS):
            binder=load_binder(pair,kind)
            resolver=make_resolver(method,ms,head,cfg);s=build_state(p,binder,mode,track,resolver)
            expected=p['parent'].copy();phases=[];snaps=[];queries=[];receipts=[];actions=[]
            reads={k:[] for k in ('record_hop','gated_hop','exact_owner')}
            def capture(phase,receipt=None,event=None):
                phases.append(phase);snaps.append(s.arrays());queries.append(p['codes'][r,old].copy())
                actions.append({'op':0,'src':new.copy(),'dst':np.full(b,N),'allowed':np.zeros(b,bool)} if event is None else event)
                rr={k:np.zeros(b,dtype=bool) for k in ('written','cleared','wrong_owner_proposal','wrong_owner_commit','veto','stale','qualified')}
                rr.update(selected=np.full(b,N,np.int64),target=np.full(b,-1,np.int64),src=new.copy())
                if receipt:
                    for k in rr:
                        if k in receipt:rr[k]=receipt[k].numpy().copy()
                receipts.append(rr)
                # Old/new/unaffected; values and intermediate nodes are additionally
                # audited directly from stored owners/payloads, no scorer intervention.
                qids=np.stack([old,new,nb],1);outs={k:[] for k in reads}
                for j in range(3):
                    q=torch.from_numpy(p['codes'][r,qids[:,j]])
                    for rd in ('record_hop','gated_hop'):
                        outs[rd].append(neural_read(s,ms[rd],resolver,q,8)['pred'].numpy())
                    outs['exact_owner'].append(exact_owner_read(s,q,resolver,8).numpy())
                for k in reads:reads[k].append(np.stack(outs[k],1))
            gold=[]
            def mark(phase,receipt=None,event=None):capture(phase,receipt,event);gold.append(expected.copy())
            mark('before_registration')
            reg=s.register(torch.from_numpy(p['codes'][r,new]));assert torch.equal(reg['handle'],torch.from_numpy(new));mark('register_only')
            def event(label,op,dst,allowed=True,scope='study',update_gold=True):
                ok=np.full(b,allowed,dtype=bool);val=torch.from_numpy(p['codes'][r,dst]);q=torch.from_numpy(p['codes'][r,new]);ok_model=ok&(name!='reject')
                sig=s.signature()
                rec=s.event(reg['handle'],val,op,ok_model,scope,reg['epoch']) if track=='resolved' else s.observed_event(q,val,resolver,op,ok_model,scope)
                if (not allowed or scope!='study') and s.signature()!=sig:raise RuntimeError('Denied event mutated state')
                if update_gold and allowed and scope=='study':expected[r,new]=dst if op==1 else N
                mark(label,rec,{'op':op,'src':new.copy(),'dst':dst.copy(),'allowed':ok&(scope=='study')})
            event('denied_write',1,mid1,False);event('wrong_scope',1,mid1,True,'other')
            event('write_new',1,mid1);event('correct_new',1,room2);event('clear_new',-1,room2);event('rewrite_new',1,room1)
            s.clear_scope();expected[:]=N;mark('reset')
            # Fresh scope via registration receipt, including a room self-record.
            rg_room=s.register(torch.from_numpy(p['codes'][r,room0]));rg_src=s.register(torch.from_numpy(p['codes'][r,new]));expected[:]=N
            # Gold graph now maps registry rows 0 and 1; decode outputs use new registry.
            va=torch.from_numpy(p['codes'][r,room0]);s.event(rg_room['handle'],va,1,True,epoch=rg_room['epoch'])
            if track=='resolved':rec=s.event(rg_src['handle'],va,1,name!='reject',epoch=rg_src['epoch'])
            else:rec=s.observed_event(torch.from_numpy(p['codes'][r,new]),va,resolver,1,name!='reject')
            expected[:,0]=0;expected[:,1]=0
            # Fresh query data differs: only new identity's result used in fresh screen.
            mark('fresh_scope',rec)
            prefix=f'{family}__{name}'
            for key in snaps[0]:arrays[prefix+'__state_'+key]=np.stack([x[key] for x in snaps])
            for key in receipts[0]:arrays[prefix+'__receipt_'+key]=np.stack([x[key] for x in receipts])
            arrays[prefix+'__gold']=np.stack(gold);arrays[prefix+'__input_parent']=p['parent'];arrays[prefix+'__ids']=ids;arrays[prefix+'__codes']=p['codes']
            for k,v in reads.items():arrays[prefix+'__pred_'+k]=np.stack(v)
            for k in ('src','dst','allowed'):arrays[prefix+'__event_'+k]=np.stack([a[k] for a in actions])
            arrays[prefix+'__event_op']=np.array([a['op'] for a in actions],np.int64)
            config.append({'prefix':prefix,'family':family,'variant':name,'mode':mode,'kind':kind,'track':track,'resolver':method,'phases':phases,'batch':b,'seed':seed,'binder_hash':weights_hash(binder)})
    if before!=model_hashes(ms):raise RuntimeError('Evaluation modified weights')
    save_arrays(path,arrays,{'stage':'A','pair':pair,'development':development,'configs':config,'fixed_weights':before,'timestamp':utc()})
    return arrays,config
