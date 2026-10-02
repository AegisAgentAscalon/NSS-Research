"""Generate chronological stimuli. Only this process and the scorer see intent/seed data."""
from __future__ import annotations
import argparse,copy,hashlib
from pathlib import Path
import numpy as np
from io_utils import ROOT,paths,check_lock,load,dump,write_lines,canonical,array_digest,digest

def ident(seed,domain,i):
    b=hashlib.sha256(f'CM02-ID-v0.2|{seed:016x}|{domain}|{i:04d}'.encode()).digest()
    return int.from_bytes(b[:4 if domain=='scope' else 8],'big')
def event_id(seed,i):return int.from_bytes(hashlib.sha256(f'CM02-EVT-v0.2|{seed:016x}|{i:04d}'.encode()).digest()[:8],'big')
def make_sequence(family,template,seeds,spec):
    from q010r.data import make_case
    stem=f'{family}/{template}';sd={c:seeds['numeric_seeds'][f'{stem}/{c}'] for c in seeds['components_per_sequence']}
    split='fixture' if 'FIX' in family else 'development' if 'DEV' in family else 'heldout'
    c=make_case(case_id=stem,pair_id=stem,paired_seed=seeds['numeric_seeds'][f'{family}/root']%(2**31-1),
       graph_seed=sd['graph'],treatment_seed=sd['treatment'],arm='CM02-new-source',split='development' if split=='fixture' else split,
       phase='CM02-chronological',path_length=1,allowed_depth=1,missing=False,near_treatment=False)
    book=c.book.copy();edges=dict(c.truth_edges);owners=c.owner.copy();A=int(c.query_slot);Ad=int(c.displaced_decoy_id)
    free=[i for i in range(16) if i not in (A,Ad)];C,Cd,D,Dd,B=free[:5];back=free[5:]
    role=dict(A=A,A_decoy=Ad,C=C,C_decoy=Cd,D=D,D_decoy=Dd,B=B)
    for lab in ('A','C','D'):
        slot,dc=role[lab],role[lab+'_decoy'];g=np.random.Generator(np.random.PCG64(sd['close_'+lab]))
        v=book[slot,:16].astype(np.float64)+g.normal(0.,.01,16);book[dc,:16]=(v/np.linalg.norm(v)).astype(np.float32)
    if not np.isfinite(book).all() or len({r.tobytes() for r in book})!=16:raise ValueError('nonfinite/colliding code; no resampling')
    scope=[ident(sd['identifiers'],'scope',i) for i in range(2)];task=[ident(sd['identifiers'],'task',i) for i in range(2)]
    order=sorted(range(16),key=lambda i:hashlib.sha256(f'CM02-ORDER-v0.2|{sd["identifiers"]:016x}|{i:04d}'.encode()).digest())
    handle={slot:ident(sd['identifiers'],'handle',j) for j,slot in enumerate(order)}
    eids=[event_id(sd['event_ids'],i) for i in range(82)]
    allids=scope+task+list(handle.values())+eids
    if any(x==0 for x in allids) or len(set(allids))!=len(allids):raise ValueError('identifier collision; no retry')
    slot_scope={i:scope[0 if i in (A,Ad,C,Cd,D,Dd) else 1] for i in range(16)}
    physical={int(slot):row for row,slot in enumerate(owners)};revision={i:1 for i in range(16)};live=set(range(16));events=[]
    def registration(slot,ordinal):return dict(type='register',event=eids[ordinal],scope=slot_scope[slot],handle=handle[slot],revision=1,row=physical[slot],
                key=book[slot].tolist(),payload_code=book[edges[slot]].tolist(),payload_symbol=edges[slot])
    for j,slot in enumerate(order):events.append(registration(slot,j))
    events.append(dict(type='activate',event=eids[16],task=task[0],scope=scope[0],task_contexts=[{'task':task[i],'scope':scope[i]} for i in range(2)]))
    episode=digest({'handles':list(handle.values()),'event':eids[0]})[:32]
    qs={q['after_event']:q for q in spec['templates'][template]['query_specifications']};gold=[];frames=[];last_binding={};current=0
    for e0 in spec['templates'][template]['events']:
        p=e0['event_position'];typ=e0['type'];e=dict(type=typ,event=eids[17+p])
        if typ=='revise':
            sl=role[e0['target']] if 'target' in e0 else back[int(e0['target_rule'].split('[')[1][:-1])]
            revision[sl]+=1;edges[sl]=(edges[sl]+1)%16;e.update(scope=slot_scope[sl],handle=handle[sl],revision=revision[sl],key=book[sl].tolist(),payload_code=book[edges[sl]].tolist(),payload_symbol=edges[sl])
        elif typ=='delete':
            sl=role[e0['target']];revision[sl]+=1;live.remove(sl);e.update(scope=slot_scope[sl],handle=handle[sl],revision=revision[sl])
        elif typ=='switch':
            current=0 if e0['task']=='A' else 1;e.update(task=task[current],scope=scope[current])
        else:
            ti=0 if e0['task']=='A' else 1;e.update(task=task[ti],scope=scope[ti])
            if typ=='conflict':e['handles']=[handle[role[x]] for x in e0['targets']]
            else:
                sl=role[e0['target']];e.update(handle=handle[sl],revision=revision[sl])
                if typ=='correct':
                    e['supersedes']=last_binding[ti]
                    if 'resolves' in e0:e['resolves']=last_binding[ti]
            last_binding[ti]=e['event']
        events.append(e)
        if p not in qs:continue
        qspec=qs[p];ci=spec['query_after_event_positions'].index(p);sigma=.01 if (spec['family_index'][family]+spec['template_order'].index(template)+ci)%2==0 else .2
        anchor=role[qspec['protected_query_anchor']];g=np.random.Generator(np.random.PCG64(sd[f'query_{p:02d}']))
        v=book[anchor,:16].astype(np.float64)+g.normal(0.,sigma,16);q=np.zeros(17,np.float32);q[:16]=(v/np.linalg.norm(v)).astype(np.float32)
        # Build the shared numerical store from observable events and their public keys/rows.
        keys=np.zeros((16,17),np.float32);values=keys.copy();valid=np.zeros(16,bool);row_map={};recs={}
        for ev in events:
            if ev['type']=='register':row_map[np.asarray(ev['key'],np.float32).tobytes()]=ev['row'];recs[(ev['scope'],ev['handle'])]=ev
            if ev['type'] in ('register','revise'):
                row=row_map[np.asarray(ev['key'],np.float32).tobytes()];keys[row]=ev['key'];values[row]=ev['payload_code'];valid[row]=True;recs[(ev['scope'],ev['handle'])]=ev
            if ev['type']=='delete':
                rr=recs[(ev['scope'],ev['handle'])];row=row_map[np.asarray(rr['key'],np.float32).tobytes()];keys[row]=0;values[row]=0;valid[row]=False
        arr={'keys':keys,'values':values,'valid':valid,'book':book,'active':c.active,'symbols':c.symbols,'query':q}
        qid=f'{episode}-{p:02d}';frame={'query_id':qid,'event_count':len(events),'current':{'task':task[current],'scope':scope[current]},'arrays':{k:v.tolist() for k,v in arr.items()}}
        assert current==(0 if qspec['active_task']=='A' else 1)
        expected=edges[anchor] if anchor in live else -1
        alt=edges[role[qspec['diagnostic_alternate_intent']]] if qspec['diagnostic_alternate_intent'] else None
        if alt is not None and expected==alt:raise ValueError('no-cue labels collide')
        gold.append(dict(query_id=qid,episode_id=episode,family=family,split=split,template=template,checkpoint=p,checkpoint_index=ci,sigma=sigma,
            expected=expected,alternate_expected=alt,intended_handle=handle[anchor],intended_slot=anchor,active_task=task[current],active_scope=scope[current],
            intended_revision=revision[anchor],expected_route=qspec['W_I_route_expected'],input_digest=array_digest(arr),prefix_digest=digest(events),whole_map_expected=True))
        frames.append(frame)
    public={'episode_id':episode,'catalogue':{'book':book.tolist(),'active':c.active.tolist(),'symbols':c.symbols.tolist()},'events':events,'queries':frames}
    meta={'episode_id':episode,'family':family,'split':split,'template':template,'seeds':sd,'role_slots':role,'physical_owners':owners.tolist(),
          'initial_edges':[list(x) for x in c.truth_edges],'book_digest':array_digest({'book':book}),'stream_digest':digest(events),'base_book_digest':array_digest({'book':c.book})}
    return public,gold,meta

def main():
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['fixture','main'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    paths(True);lock=check_lock();seeds=load(ROOT/'protocol/SEEDS.json');spec=load(ROOT/'protocol/EVENT_TEMPLATES.json');families=seeds['families'][:1] if a.kind=='fixture' else seeds['families'][1:]
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'public').mkdir();truth=[];metas=[]
    for f in families:
        for t in spec['template_order']:
            pub,g,m=make_sequence(f,t,seeds,spec);dump(a.output/'public'/f'{pub["episode_id"]}.json',pub);truth+=g;metas.append(m)
    write_lines(a.output/'protected_queries.jsonl',truth);write_lines(a.output/'protected_sequences.jsonl',metas)
    # Public ordering gives opaque IDs only; controllers never see family/template names.
    dump(a.output/'PUBLIC_ORDER.json',[m['episode_id'] for m in metas])
    dump(a.output/'INPUT_LOCK.json',{'source_lock_sha256':lock,'kind':a.kind,'sequences':len(metas),'query_occasions':len(truth),
       'files':{str(p.relative_to(a.output)):__import__('io_utils').sha(p) for p in sorted(a.output.rglob('*')) if p.is_file()},'catalogue_and_stream_identities':metas})
    print(f'GENERATED {a.kind}: {len(metas)} sequences, {len(truth)} query occasions',flush=True)
if __name__=='__main__':main()
