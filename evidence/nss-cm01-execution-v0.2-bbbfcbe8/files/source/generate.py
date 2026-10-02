"""CM-01 stimulus producer. Writes visible evidence and an isolated truth ledger."""
from __future__ import annotations
import copy,sys
from dataclasses import asdict
from pathlib import Path
import numpy as np
from common import ROOT,paths,configure,check_lock,load,dump,write_lines,canonical,digest_arrays
from manager import Workspace,encode,compile_public

COMPONENTS=('graph','treatment','close','query','identifiers')

def generate_one(family,stratum,j,seedmap):
    from q010r.data import make_case
    unit=3 if stratum==4 else stratum
    stem=f'{family}/s{unit}/j{j}'
    seeds={k:seedmap[f'{stem}/{k}'] for k in COMPONENTS}
    split='development' if family.startswith(('CMDEV','CMFIX')) else 'heldout'
    c=make_case(case_id=stem,pair_id=stem,paired_seed=seedmap[f'{family}/root']%(2**31-1),
                graph_seed=seeds['graph'],treatment_seed=seeds['treatment'],arm='CM01-visible-case',
                split=split,phase='CM01-new-interface',path_length=1,allowed_depth=1)
    book=c.book.copy();symbols=c.symbols.copy();owner=c.owner.copy();edges=dict(c.truth_edges)
    src=int(c.query_symbol_id);decoy=int(c.displaced_decoy_id)
    no_cue=(stratum==7 and j>=4)
    close=(stratum==2 or no_cue)
    if close:
        g=np.random.Generator(np.random.PCG64(seeds['close']))
        v=book[src,:16].astype(np.float64)+g.normal(0.,.01,16)
        book[decoy,:16]=(v/np.linalg.norm(v)).astype(np.float32)
    keys=np.zeros_like(c.keys);values=np.zeros_like(c.values);valid=c.present.copy()
    for row,slot in enumerate(owner):
        if valid[row]:keys[row]=book[slot];values[row]=book[edges[int(symbols[slot])]]
    initial_edges=edges.copy()
    sigma=.01 if j%4<2 else .2
    g=np.random.Generator(np.random.PCG64(seeds['query']))
    v=book[src,:16].astype(np.float64)+g.normal(0.,sigma,16)
    q=np.r_[(v/np.linalg.norm(v)).astype(np.float32),np.float32(0)].astype(np.float32)
    ids=np.random.Generator(np.random.PCG64(seeds['identifiers']));seen=set()
    def opaque():
        while True:
            x=int(ids.bit_generator.random_raw())
            if x and x not in seen:seen.add(x);return x
    scope=int(ids.integers(1,2**32-1));task=opaque();handles=[opaque() for _ in range(16)]
    journal=[]
    def event(typ,**kw):
        e=dict(type=typ,event=opaque(),**kw);journal.append(e);return e
    for slot in ids.permutation(16):
        slot=int(slot)
        event('register',scope=scope,handle=handles[slot],revision=1,key=book[slot].tolist(),
              payload_code=book[edges[slot]].tolist(),payload_symbol=edges[slot])
    selected=None;foreign_selection=None;mutations=[];subtype='standard';fault=None
    if stratum not in (3,4):
        chosen=decoy if no_cue or stratum==8 else src
        selected=event('select',scope=scope,task=task,handle=handles[chosen],revision=1)
    if stratum==5:
        row=int(np.flatnonzero(owner==src)[0])
        if j<4:
            subtype='revision';newdst=next(x for x in range(16) if x not in (src,edges[src],decoy))
            edges[src]=newdst;values[row]=book[newdst]
            e=event('revise',scope=scope,handle=handles[src],revision=2,key=book[src].tolist(),payload_code=book[newdst].tolist(),payload_symbol=newdst)
            mutations.append({'type':'update','source':src,'destination':newdst,'event':e['event']})
        else:
            subtype='deletion';edges.pop(src);valid[row]=False;keys[row]=0;values[row]=0
            e=event('delete',scope=scope,handle=handles[src],revision=2)
            mutations.append({'type':'delete','source':src,'event':e['event']})
    if stratum==6:
        foreign_scope=scope^0x80000000
        if foreign_scope==0:foreign_scope=scope^0x40000000
        foreign_task=opaque();fh=opaque()
        event('register',scope=foreign_scope,handle=fh,revision=1,key=book[decoy].tolist(),payload_code=book[edges[decoy]].tolist(),payload_symbol=edges[decoy])
        foreign_selection=event('select',scope=foreign_scope,task=foreign_task,handle=fh,revision=1)
        subtype='foreign_scope_checkpoint';fault='restore_observed_foreign_workspace'
    if stratum==7:
        subtype='no_cue' if no_cue else 'detectable'
        if not no_cue:fault='replace_handle_keep_binding_event'
    if stratum==8:
        if j<4:
            subtype='correction';event('correct',scope=scope,task=task,handle=handles[src],revision=1,supersedes=selected['event'])
        else:
            subtype='unresolved_conflict';event('conflict',scope=scope,task=task,handles=[handles[src],handles[decoy]])
    current={'scope':scope,'task':task};view=compile_public(journal,current);ws=Workspace(**view['workspace'])
    before_fault=encode(ws)
    if fault=='replace_handle_keep_binding_event':ws=Workspace(ws.scope,handles[decoy],ws.revision,ws.binding_event,ws.operation)
    elif fault=='restore_observed_foreign_workspace':
        e=foreign_selection;ws=Workspace(e['scope'],e['handle'],e['revision'],e['event'],'R')
    public={'current':current,'journal':journal,'workspace':asdict(ws),'serialized':encode(ws)}
    case_id=f'{family}-s{stratum}-j{j}'
    expected_action='original' if stratum in (3,4) or (stratum==8 and j>=4) else 'abstain' if stratum in (5,6) or (stratum==7 and j<4) else 'canonical'
    gold={'case_id':case_id,'family':family,'split':split,'stratum':stratum,'within_stratum':j,'sigma':sigma,'subtype':subtype,
          'query_source':-1 if stratum==4 else src,'initial_truth_edges':sorted([list(x) for x in initial_edges.items()]),'truth_mutations':mutations,
          'physical_owners':owner.tolist(),'intended_handle':None if stratum==4 else handles[src],
          'expected_management_action':expected_action,'observable_invalid':expected_action=='abstain',
          'information_limit':stratum in (3,4) or no_cue,'decoy_source':decoy,'decoy_handle':handles[decoy],
          'generation':{'unit':stem,'seeds':seeds,'close_decoy':close,'close_sigma':.01 if close else None},
          'workspace_fault':fault,'workspace_before_fault':before_fault,'workspace_after_fault':encode(ws)}
    raw={'keys':keys,'values':values,'valid':valid,'query':q,'book':book,'active':c.active.copy(),'symbols':symbols}
    return raw,public,gold

def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['fixture','main'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    paths(True);configure();lock=check_lock();seedmap=load(ROOT/'protocol/SEEDS.json')['seeds']
    families=['CMFIX-00'] if a.kind=='fixture' else ['CMDEV-01','CMDEV-02','CMDEV-03']+[f'CMEVAL-{i:02d}' for i in range(1,6)]
    allraw=[];pub=[];gold=[]
    for f in families:
        for s in range(1,9):
            for j in ([0] if a.kind=='fixture' else range(8)):
                r,v,g=generate_one(f,s,j,seedmap);allraw.append(r);pub.append(v);gold.append(g)
    data={k:np.stack([r[k] for r in allraw]) for k in allraw[0]}
    a.output.mkdir(parents=True,exist_ok=False);np.savez_compressed(a.output/'inputs.npz',**data)
    write_lines(a.output/'public.jsonl',pub);write_lines(a.output/'protected.jsonl',gold)
    pairs=[]
    for f in families:
        for j in ([0] if a.kind=='fixture' else range(8)):
            inds=[i for i,g in enumerate(gold) if g['family']==f and g['within_stratum']==j and g['stratum'] in (3,4)]
            u,v=inds
            assert canonical(pub[u])==canonical(pub[v])
            assert all(np.array_equal(data[k][u],data[k][v]) for k in data)
            pairs.append({'known_index':u,'absent_index':v,'visible_sha256':__import__('hashlib').sha256(canonical(pub[u])).hexdigest()})
    dump(a.output/'GENERATION.json',{'kind':a.kind,'records':len(pub),'families':families,'source_lock_sha256':lock,'input_array_digest':digest_arrays(data),'identical_public_opposite_truth_pairs':pairs,'training_updates':0})
    print(f'GENERATED {a.kind} {len(pub)} records',flush=True)
if __name__=='__main__':main()
