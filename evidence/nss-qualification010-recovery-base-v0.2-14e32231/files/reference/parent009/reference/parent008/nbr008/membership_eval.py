"""Fresh main identity boundary tests; no training or calibration imports."""
import argparse,time
from pathlib import Path
import numpy as np
import torch
from .common import *
from .config import *
from .samples import sample,FAMILIES

@torch.no_grad()
def evaluate(pair,out,dev=False,n=1024):
    seed=1000 if dev else 1000+pair;setup(seed);models=parents(pair);head,cfg=load_gate(seed,dev)
    methods=METHODS+('distance_nearest','margin_nearest')
    cases=[(f,16) for f in FAMILIES]+[(f,c) for c in (8,12) for f in ('known_q20','novel')]
    arrays={};rows=[];cases_meta=[];start=time.perf_counter()
    for j,(family,count) in enumerate(cases):
        rs=(410000000 if not dev else 400000000)+pair*1000+j
        a=sample(np.random.default_rng(rs),n,family,count)
        x=torch.from_numpy(a['x']);book=torch.from_numpy(a['book']);active=torch.from_numpy(a['active'])
        key=f'm{j:03d}';arrays[key+'_target']=a['target'].astype(np.int16);arrays[key+'_raw_x']=a['x'];
        cases_meta.append({'key':key,'family':family,'active_count':count,'seed':rs,'n':n})
        for m in methods:
            r=resolver(m,models,head,cfg);d=r(x,book,active)
            pred=d.index[:,0].numpy();ac=d.accept[:,0].numpy()
            vals=d.value[:,0]
            outsim=torch.einsum('bd,bnd->bn',torch.nn.functional.normalize(vals,dim=-1),book).masked_fill(~active,-1e6)
            selected=outsim.argmax(-1).numpy();selected=np.where(ac,selected,-1)
            row={'key':key,'family':family,'count':count,'method':m,'pair':pair,'n':n,'accept_n':int(ac.sum()),'accepted':float(ac.mean()),'correct_identity':float((selected==a['target']).mean()),'wrong_known':float(((selected>=0)&(selected!=a['target'])).mean()) if a['known'].any() else None,'false_accept':float(ac.mean()) if not a['known'].any() else None}
            rows.append(row);prefix=key+'_'+m
            arrays[prefix+'_index']=selected.astype(np.int16);arrays[prefix+'_accept']=ac;arrays[prefix+'_features']=d.feat[:,0].numpy();arrays[prefix+'_score']=d.score[:,0].numpy()
        # Permutation intervention must preserve accepted symbol (not row number).
        if family in ('known_q20','novel') and count==16:
            perm=torch.arange(15,-1,-1)
            for m in ('A_nearest','B_nearest','A_learned','B_learned'):
                r=resolver(m,models,head,cfg);d=r(x,book[:,perm],active[:,perm]);base=arrays[key+'_'+m+'_index']
                sim=torch.einsum('bd,bnd->bn',torch.nn.functional.normalize(d.value[:,0],dim=-1),book)
                pred=sim.argmax(-1).numpy();pred=np.where(d.accept[:,0].numpy(),pred,-1)
                arrays[key+'_'+m+'_permuted']=pred.astype(np.int16)
                if not np.array_equal(pred,base):raise RuntimeError('Permutation changed selected identities')
    # Same-observable pair deliberately gives conflicting hidden origin labels.
    a=sample(np.random.default_rng(420000000+pair),n,'novel_near030')
    f=torch.from_numpy(a['x']);b=torch.from_numpy(a['book']);act=torch.from_numpy(a['active'])
    ambiguity={}
    for m in ('A_nearest','B_nearest'):
        d=resolver(m,models,head,cfg)(f,b,act)
        ambiguity[m]={'n_identical_pairs':n,'same_decision_required':True,'accept_both_rate':float(d.accept.float().mean()),'reject_both_rate':float((~d.accept).float().mean()),'two_origin_binary_accuracy':.5}
        arrays['ambiguous_'+m]=d.accept[:,0].numpy()
    path=Path(out)/f'membership_pair{pair}.npz';path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise FileExistsError(path)
    np.savez_compressed(path,**arrays);info={'pair':pair,'seed':seed,'rows':rows,'cases':cases_meta,'ambiguity':ambiguity,'seconds':time.perf_counter()-start,'array_sha256':sha(path),'head_hash':weights_hash(head),'parent_hashes':model_hashes(models),'environment':env()}
    dump(path.with_suffix('.json'),info);return info
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--pair',type=int,required=True);a.add_argument('--out',required=True);a.add_argument('--dev',action='store_true');a.add_argument('--n',type=int,default=1024);p=a.parse_args();evaluate(p.pair,p.out,p.dev,p.n)
