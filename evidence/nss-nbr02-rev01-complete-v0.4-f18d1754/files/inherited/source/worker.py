"""Streaming worker: receives no seed recipes, score ledger, or future receipt outcomes."""
import sys,os,json,traceback,random
from pathlib import Path
import numpy as np
import torch
from runtime import Recorder,Learner

def main():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    random.seed(0);np.random.seed(0);torch.manual_seed(0)
    out=Path(sys.argv[1]).resolve();rec=Recorder(out);model=Learner(rec)
    denied=('private/','protocol/','generator.py','driver.py','auditor.py')
    def guard(event,args):
        if event=='open' and isinstance(args[0],(str,bytes)):
            p=os.fsdecode(args[0])
            if any(s in p for s in denied):raise PermissionError('WORKER_ISOLATION:'+p)
    sys.addaudithook(guard)
    print(json.dumps({'ready':True,'torch':torch.__version__,'numpy':np.__version__}),flush=True)
    for line in sys.stdin:
        try:
            msg=json.loads(line);op=msg.pop('op')
            if op=='LOAD':model.load(**msg);ans={'loaded':True}
            elif op=='CUE':ans=model.start_cue(**msg)
            elif op=='FILLERS':ans=model.fillers(**msg)
            elif op=='RECEIPT':ans=model.receipt(**msg)
            elif op=='QUERY':ans=model.query(**msg)
            elif op=='DERIVATIVE':ans=model.derivative(**msg)
            elif op=='CHECKPOINT':ans=model.checkpoint(**msg)
            elif op=='ISOLATION_CHECK':
                caught=[]
                for rel in ('protocol/SEED_RECIPE.json','raw/primary/private/PLAN.json','source/auditor.py'):
                    try:
                        open(out.parent.parent.parent/rel,'rb')
                    except PermissionError:caught.append(rel)
                assert len(caught)==3
                rec.emit('ISOLATION_GUARD_TEST',{'denied':caught});ans={'isolated':True}
            elif op=='CLOSE':rec.close();print(json.dumps({'closed':True,'counts':rec.counts}),flush=True);return
            else:raise ValueError('UNKNOWN_OPERATION')
            print(json.dumps(ans,allow_nan=False),flush=True)
        except BaseException as ex:
            detail={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc(),'counts':rec.counts}
            try:rec.emit('WORKER_FATAL',detail)
            finally:
                print(json.dumps({'fatal':detail}),flush=True)
            raise
if __name__=='__main__':main()
