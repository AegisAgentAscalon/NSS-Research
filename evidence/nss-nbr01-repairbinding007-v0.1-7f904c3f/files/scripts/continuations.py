"""Fresh-interpreter full-state maintenance and mid-query continuation checks."""
from pathlib import Path
import sys,json,copy
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr007 import ROOT,snapshot
from nbr007.evaluate import problem,load_models,exposure,statehash
from nbr006 import common as c,data,models
PATH=ROOT/'evidence/continuations'
@torch.no_grad()
def prepare():
    PATH.mkdir(parents=True,exist_ok=True);index=[]
    for seed in range(901,906):
        c.setup(seed);readers,binder,fitted=load_models(seed)
        for kind in ('none','learned_dictionary','nearest'):
            p=problem(91000000+seed,h=8,b=16);k,v,e,q,book=data.tensors(p);rng=np.random.default_rng(7123+seed)
            k,v=exposure(k,v,e,book,kind,fitted,rng,23,.02,'both')
            ids={'reader':c.weights_hash(readers['record_hop']),'binder':c.weights_hash(binder),'repair':c.weights_hash(fitted[kind]) if kind in fitted else kind,'dictionary_schema':'identity17-v1'}
            stem=f'{kind}_{seed}'
            snapshot.save(PATH/(stem+'.npz'),k,v,e,book,q,rng,ids,'research',0)
            kk,vv=exposure(k,v,e,book,kind,fitted,rng,41,.02,'both')
            expected={'keys':kk.numpy(),'values':vv.numpy(),'present':e.numpy(),'book':book.numpy(),'query':q.numpy()}
            for name,m in readers.items():expected[name]=m(kk,vv,e,q,8).numpy()
            np.savez_compressed(PATH/(stem+'_expected.npz'),**expected)
            index.append({'type':'state','seed':seed,'kind':kind,'stem':stem,'identities':ids})
        for name,reader in readers.items():
            p=problem(91100000+seed,h=8,b=16);k,v,e,q,book=data.tensors(p);rng=np.random.default_rng(seed)
            h=reader(k,v,e,q,3)[:,-1]
            ids={'reader':c.weights_hash(reader),'binder':c.weights_hash(binder),'repair':'none','dictionary_schema':'identity17-v1'}
            stem=f'query_{name}_{seed}';snapshot.save(PATH/(stem+'.npz'),k,v,e,book,h,rng,ids,'research',3)
            np.savez_compressed(PATH/(stem+'_expected.npz'),output=reader(k,v,e,q,8)[:,3:].numpy())
            index.append({'type':'query','seed':seed,'reader':name,'stem':stem,'identities':ids})
    c.dump(PATH/'INDEX.json',index);print('prepared',len(index))
@torch.no_grad()
def verify():
    index=json.loads((PATH/'INDEX.json').read_text());cases=[]
    for x in index:
        c.setup(x['seed']);readers,binder,fitted=load_models(x['seed'])
        a,rng,cut=snapshot.load(PATH/(x['stem']+'.npz'),x['identities'],'research');k,v,e,book,q=a
        expected=np.load(PATH/(x['stem']+'_expected.npz'),allow_pickle=False)
        if x['type']=='state':
            kk,vv=exposure(k,v,e,book,x['kind'],fitted,rng,41,.02,'both')
            got={'keys':kk.numpy(),'values':vv.numpy(),'present':e.numpy(),'book':book.numpy(),'query':q.numpy()}
            for name,m in readers.items():got[name]=m(kk,vv,e,q,8).numpy()
        else:got={'output':readers[x['reader']](k,v,e,q,8-cut).numpy()}
        for key,a in got.items():assert np.array_equal(a,expected[key]),(x,key)
        cases.append({'stem':x['stem'],'type':x['type'],'exact':True})
    c.dump(PATH/'VERIFIED.json',{'status':'PASS','cases':cases,'count':len(cases),'scope':'Complete saved states in fresh interpreter; not crash-safe deployment/optimizer resume.'});print('verified',len(cases))
if __name__=='__main__':prepare() if sys.argv[-1]=='prepare' else verify()
