from pathlib import Path
import json,sys,numpy as np,hashlib

def run(a,b,out):
 a,b,out=Path(a),Path(b),Path(out);ca=json.loads((a/'CAPTURE.json').read_text());cb=json.loads((b/'CAPTURE.json').read_text());assert len(ca['chunks'])==len(cb['chunks']);count=0;elements=0
 for x,y in zip(ca['chunks'],cb['chunks'],strict=True):
  assert x['condition']==y['condition'] and x['file']==y['file']
  with np.load(a/x['file'],allow_pickle=False) as za,np.load(b/y['file'],allow_pickle=False) as zb:
   assert za.files==zb.files
   for k in za.files:
    u,v=za[k],zb[k];assert u.dtype==v.dtype and u.shape==v.shape and u.tobytes()==v.tobytes(),(x['file'],k);count+=1;elements+=u.size
  # Metadata contains generated cases/recipes/event histories, not wall timers.
  assert json.loads((a/x['meta']).read_text())==json.loads((b/y['meta']).read_text()),x['meta']
 out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps({'status':'PASS','left':str(a),'right':str(b),'chunks':len(ca['chunks']),'arrays_exact':count,'elements_exact':elements,'metadata_exact':True,'scope':'Same development cases replayed in a fresh interpreter; not independent samples or main qualification'},indent=2));print(out.read_text())
if __name__=='__main__':run(*sys.argv[1:])
