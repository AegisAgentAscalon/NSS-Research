"""Read a typed maintenance world and emit proposed dispositions; never act on them."""
from __future__ import annotations
import argparse
from support import *
from nss_hsa import *

CLASSES=['DEFER','COMPLETE','READY','BLOCKED']
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--world',type=Path,default=ROOT/'examples/world.json');ap.add_argument('--output',type=Path,default=ROOT/'examples/output.json');a=ap.parse_args()
    setup()
    try:
        raw=a.world.read_bytes();w=json.loads(raw);x,specs=prepare_worlds([w]);plan=compile_plan(specs)
        cp=torch.load(ROOT/'checkpoints/8801_hsa_inference.pt',weights_only=True,map_location='cpu');m=MaintenanceReader();m.load_state_dict(cp['model']);m.eval()
        if model_sha(m)!=cp['model_hash']:raise HierarchyError('MODEL_DIGEST_MISMATCH')
        with torch.no_grad():out=m(x,plan,checked=True)[0].softmax(-1).numpy()
        save(a.output,{'schema':'nss.hsa.typed_output.v1','world_sha256':hashlib.sha256(raw).hexdigest(),'model_sha256':model_sha(m),'topology_sha256':plan.identity,
            'decisions':[{'task':i,'status':CLASSES[int(row.argmax())],'assigned_score':float(row.max())} for i,row in enumerate(out)],
            'limits':['not a language reader','scores are not calibrated','advisory only; no actions executed']})
        (ROOT/'examples/plan.json').write_bytes(plan.to_bytes());print(a.output.read_text())
    except (OSError,ValueError,KeyError) as e:
        print(json.dumps({'status':'ERROR','type':type(e).__name__,'detail':str(e)}),file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
