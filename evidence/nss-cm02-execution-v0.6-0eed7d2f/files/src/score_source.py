"""Independent source reconstruction from reviewed seeds/events; no producer imports."""
from __future__ import annotations
import hashlib
import numpy as np
from io_utils import digest,array_digest

def restore(meta,seeds,spec):
    family,t=meta['family'],meta['template'];stem=family+'/'+t
    sd={k:seeds['numeric_seeds'][stem+'/'+k] for k in seeds['components_per_sequence']}
    if sd!=meta['seeds']:raise AssertionError('component seed drift')
    rng=np.random.Generator(np.random.PCG64(sd['graph']));path=rng.permutation(np.arange(16,dtype=np.int64))[:2]
    a,end=map(int,path);outside=[x for x in range(16) if x not in (a,end)];ad=outside[-1]
    edges={x:x for x in outside};edges[ad]=outside[0];edges[a]=end;edges[end]=end
    initial=[[k,v] for k,v in sorted(edges.items())]
    if initial!=meta['initial_edges']:raise AssertionError('initial truth drift')
    base=rng.standard_normal((16,16));book=np.zeros((16,17),np.float32);book[:,:16]=(base/np.linalg.norm(base,axis=-1,keepdims=True)).astype(np.float32)
    base_hash=array_digest({'book':book});owners=rng.permutation(16)
    free=iter(x for x in range(16) if x not in (a,ad));c,cd,d,dd,b=[next(free) for _ in range(5)];bg=list(free)
    roles={'A':a,'A_decoy':ad,'B':b,'C':c,'C_decoy':cd,'D':d,'D_decoy':dd}
    if roles!=meta['role_slots'] or owners.tolist()!=meta['physical_owners']:raise AssertionError('independent roles/physical order')
    for label in ('A','C','D'):
        r=np.random.Generator(np.random.PCG64(sd['close_'+label]));x=book[roles[label],:16].astype(np.float64)+r.normal(0.,.01,size=16)
        book[roles[label+'_decoy'],:16]=np.asarray(x/np.linalg.norm(x),np.float32)
    assert len({x.tobytes() for x in book})==16 and np.isfinite(book).all()
    def identifier(domain,ordinal):
        text='CM02-ID-v0.2|%016x|%s|%04d'%(sd['identifiers'],domain,ordinal)
        return int.from_bytes(hashlib.sha256(text.encode('ascii')).digest()[:4 if domain=='scope' else 8],byteorder='big')
    scopes=[identifier('scope',j) for j in (0,1)];tasks=[identifier('task',j) for j in (0,1)]
    order=sorted(range(16),key=lambda i:hashlib.sha256(('CM02-ORDER-v0.2|%016x|%04d'%(sd['identifiers'],i)).encode('ascii')).digest())
    handles={s:identifier('handle',ordinal) for ordinal,s in enumerate(order)}
    eids=[int.from_bytes(hashlib.sha256(('CM02-EVT-v0.2|%016x|%04d'%(sd['event_ids'],i)).encode('ascii')).digest()[:8],'big') for i in range(82)]
    allids=scopes+tasks+list(handles.values())+eids
    assert all(allids) and len(set(allids))==len(allids)
    space={i:scopes[0 if i in (a,ad,c,cd,d,dd) else 1] for i in range(16)}
    row={int(x):i for i,x in enumerate(owners)};revs={i:1 for i in range(16)};live=set(revs)
    events=[]
    for i,s in enumerate(order):
        events.append({'type':'register','event':eids[i],'scope':space[s],'handle':handles[s],'revision':1,'row':row[s],
                       'key':book[s].tolist(),'payload_code':book[edges[s]].tolist(),'payload_symbol':edges[s]})
    events.append({'type':'activate','event':eids[16],'task':tasks[0],'scope':scopes[0],
                   'task_contexts':[{'task':tasks[i],'scope':scopes[i]} for i in (0,1)]})
    eid=digest({'handles':list(handles.values()),'event':eids[0]})[:32]
    assert eid==meta['episode_id'];active=0;prior={};qframes=[];gold=[];qspecs={x['after_event']:x for x in spec['templates'][t]['query_specifications']}
    for symbolic in spec['templates'][t]['events']:
        pos,typ=symbolic['event_position'],symbolic['type'];ev={'type':typ,'event':eids[17+pos]}
        if typ in ('revise','delete'):
            s=roles[symbolic['target']] if 'target' in symbolic else bg[int(symbolic['target_rule'].removeprefix('background_pool[').removesuffix(']'))]
            revs[s]+=1;ev.update(scope=space[s],handle=handles[s],revision=revs[s])
            if typ=='delete':live.remove(s)
            else:
                edges[s]=(edges[s]+1)%16;ev.update(key=book[s].tolist(),payload_code=book[edges[s]].tolist(),payload_symbol=edges[s])
        elif typ=='switch':
            active=int(symbolic['task']=='B');ev.update(task=tasks[active],scope=scopes[active])
        else:
            ti=int(symbolic['task']=='B');ev.update(task=tasks[ti],scope=scopes[ti])
            if typ=='conflict':ev['handles']=[handles[roles[x]] for x in symbolic['targets']]
            else:
                sl=roles[symbolic['target']];ev.update(handle=handles[sl],revision=revs[sl])
                if typ=='correct':
                    ev['supersedes']=prior[ti]
                    if symbolic.get('resolves'):ev['resolves']=prior[ti]
            prior[ti]=ev['event']
        events.append(ev)
        if pos not in qspecs:continue
        qs=qspecs[pos];ci=spec['query_after_event_positions'].index(pos);sig=(.01,.2)[(spec['family_index'][family]+spec['template_order'].index(t)+ci)%2]
        target=roles[qs['protected_query_anchor']];noise=np.random.Generator(np.random.PCG64(sd['query_%02d'%pos])).normal(0,sig,16)
        v=book[target,:16].astype(np.float64)+noise;q=np.zeros(17,np.float32);q[:16]=np.asarray(v/np.linalg.norm(v),np.float32)
        keys=np.zeros((16,17),np.float32);vals=keys.copy();valid=np.zeros(16,bool)
        for pr,s in enumerate(owners):
            if int(s) in live:keys[pr]=book[s];vals[pr]=book[edges[int(s)]];valid[pr]=True
        arr={'keys':keys,'values':vals,'valid':valid,'query':q,'book':book,'active':np.ones(16,bool),'symbols':np.arange(16,dtype=np.int64)}
        qid=eid+'-%02d'%pos;cur={'task':tasks[active],'scope':scopes[active]}
        qframes.append({'query_id':qid,'event_count':len(events),'current':cur,'arrays':{k:v.tolist() for k,v in arr.items()}})
        assert active==int(qs['active_task']=='B')
        expected=edges[target] if target in live else -1;alt=edges[roles[qs['diagnostic_alternate_intent']]] if qs['diagnostic_alternate_intent'] else None
        if alt is not None:assert alt!=expected
        gold.append({'query_id':qid,'episode_id':eid,'family':family,'split':meta['split'],'template':t,'checkpoint':pos,'checkpoint_index':ci,'sigma':sig,
             'expected':expected,'alternate_expected':alt,'intended_handle':handles[target],'intended_slot':target,'active_task':tasks[active],'active_scope':scopes[active],
             'intended_revision':revs[target],'expected_route':qs['W_I_route_expected'],'input_digest':array_digest(arr),'prefix_digest':digest(events),'whole_map_expected':True})
    assert base_hash==meta['base_book_digest'] and array_digest({'book':book})==meta['book_digest'] and digest(events)==meta['stream_digest']
    return {'episode_id':eid,'catalogue':{'book':book.tolist(),'active':np.ones(16,bool).tolist(),'symbols':np.arange(16).tolist()},'events':events,'queries':qframes},gold

def public_state(prefix):
    records={};history={};selections={};current={};context={};bindings={}
    for e in prefix:
        typ=e['type']
        if typ=='activate':
            context={x['task']:x['scope'] for x in e['task_contexts']};selections={k:None for k in context};current={'task':e['task'],'scope':e['scope']}
        elif typ=='switch':current={'task':e['task'],'scope':e['scope']}
        elif typ in ('select','correct','conflict'):
            old=selections.get(e['task'])
            if typ=='correct' and old is not None:assert e['supersedes']==old['event']
            if 'resolves' in e:assert old is not None and old['type']=='conflict' and e['resolves']==old['event']
            assert context[e['task']]==e['scope'];selections[e['task']]=e;bindings[e['event']]=e
        elif typ in ('register','revise','delete'):
            k=e['scope'],e['handle'];history.setdefault(k,[]).append(e)
            if typ=='register':assert k not in records and e['revision']==1;records[k]=dict(e,active=True)
            else:
                old=records[k];assert old['active'] and e['revision']==old['revision']+1
                if typ=='revise':assert old['key']==e['key'];records[k]=dict(e,active=True)
                else:records[k]=dict(old,active=False,event=e['event'],revision=e['revision'])
        else:raise AssertionError('unexpected event')
    return records,history,selections,current

def route_prefix(prefix,latest=False):
    recs,hist,sel,cur=public_state(prefix);e=sel[cur['task']];r=None
    if e is None:f=[1,0,0,0,0,'U'];action,reason='original','unselected'
    elif e['type']=='conflict':f=[1,e['scope'],0,0,e['event'],'H'];action,reason='original','conflict'
    else:
        f=[1,e['scope'],e['handle'],e['revision'],e['event'],'R'];r=recs[(e['scope'],e['handle'])]
        if e['scope']!=cur['scope']:action,reason='abstain','cross_scope'
        elif not r['active']:action,reason='abstain','deleted'
        elif e['revision']!=r['revision']:
            if latest:
                chain=[x for x in hist[(e['scope'],e['handle'])] if x['revision']>=e['revision']]
                assert [x['revision'] for x in chain]==list(range(e['revision'],r['revision']+1)) and all(x['type']!='delete' and x['key']==r['key'] for x in chain)
                action,reason='canonical','observed_latest_revision'
            else:action,reason='abstain','stale_revision'
        else:action,reason='canonical','validated_pinned_revision'
    return {'action':action,'reason':reason,'fields':f,'canonical_key':r['key'] if action=='canonical' else None},int(r['payload_symbol']) if action=='canonical' else -1,cur

def packet(fields):return '01|%08x|%016x|%08x|%016x|%s'%tuple(fields[1:])
def expected_entries(prefix):
    _,_,sel,_=public_state(prefix);out={}
    for task,e in sel.items():
        if e is None:v=[1,0,0,0,0,'U']
        elif e['type']=='conflict':v=[1,e['scope'],0,0,e['event'],'H']
        else:v=[1,e['scope'],e['handle'],e['revision'],e['event'],'R']
        out[task]=v
    return out
