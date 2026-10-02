"""Post-main paired diagnostics. No new fitting, thresholds or main replacement."""
import json,sys,time
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr007 import ROOT
from nbr007.evaluate import problem,load_models,exposure,scores,statehash
from nbr006 import common as c,data,models
from nbr006.eval import install

@torch.no_grad()
def run(outdir):
    rows=[];arrays={};i=0;t=time.perf_counter()
    for seed in range(901,906):
        c.setup(seed);readers,binder,fitted=load_models(seed)
        def record(case,kind,p,k,v,e):
            nonlocal i
            key=f'd{i:04d}';i+=1
            arrays[key+'_parent']=p['parent'].astype(np.int16);arrays[key+'_query']=p['query'].astype(np.int16);arrays[key+'_rooms']=p['rooms'].astype(np.int16)
            for name,m in readers.items():
                pred=models.logits(m(k,v,e,torch.from_numpy(p['q']),8),torch.from_numpy(p['codes'])).argmax(-1).numpy()[:,[0,1,3,7]]
                arrays[key+'_'+name]=pred.astype(np.int16)
                for j,d in enumerate((1,2,4,8)):
                    rows.append({'key':key,'seed':seed,'case':case,'method':kind,'reader':name,'depth':d,'state_hash':statehash(k,v,e),**scores(pred[:,j],p)})
        # Main long periodic was h8; main long late-only was h4. Supply the
        # missing matched h4 periodic arm, same graph and exact noise schedule.
        p=problem(81000000+seed*100+4,4,64);k0,v0,e,q,book=data.tensors(p)
        for kind in ('learned_dictionary','nearest'):
            k,v=exposure(k0,v0,e,book,kind,fitted,np.random.default_rng(620000+seed),1024,.02,'both')
            record('matched_periodic_h4_t1024',kind,p,k,v,e)
        # Clean repeated-maintenance stability (rather than main's t=0 clean).
        for kind in ('intrinsic_mlp','learned_dictionary','nearest'):
            k,v=exposure(k0,v0,e,book,kind,fitted,np.random.default_rng(620000+seed),1024,0.,'both')
            record('clean_maintenance_h4_t1024',kind,p,k,v,e)
        # Are final new-scope errors already present at the original write?
        p=problem(84500000+seed,4,64);st=install(p,binder)
        record('new_scope_install_no_noise','none',p,*st.snapshot())
    d=Path(outdir);d.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(d/'arrays.npz',**arrays)
    c.dump(d/'RESULTS.json',{'label':'POST_MAIN_EXPLORATORY','reason':'Matched h4 long timing comparison; clean maintenance and initial-binding separation. No main scores/weights changed.','rows':rows,'state_configurations':i,'seconds':time.perf_counter()-t,'array_hash':c.sha(d/'arrays.npz')});print('diagnostics',i,len(rows))
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else ROOT/'evidence/diagnostics')
