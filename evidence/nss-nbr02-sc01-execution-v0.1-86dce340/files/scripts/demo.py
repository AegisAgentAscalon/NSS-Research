"""Advisory demonstration on an already-retained synthetic input."""
from support import *
from sc01 import Store,Workspace
import argparse

def main():
    p=argparse.ArgumentParser();p.add_argument('--policy',choices=['index','cache','segment'],default='segment');args=p.parse_args()
    setup();m,mid=load(8801);w=json.loads((ROOT/'examples/world.json').read_text());store=Store(w)
    ws=Workspace(store,mid,args.policy,128)
    out=ws.job('demo',[0,1,2,3],m)
    labels=['DEFER','COMPLETE','READY','BLOCKED']
    d={'schema':'nss.sc01.demo.v1','policy':args.policy,'advisory_only':True,
       'tasks':[{'task':t,'status':'DEFER_BUDGET'if r is None else labels[r['label']],
                 'evidence_fingerprint':None if r is None else r['signature']}for t,r in out.items()],
       'stats':dict(ws.stats),'accounting':ws.accounting(),'optimizer_applications':0}
    print(json.dumps(d,indent=2));save(ROOT/'examples/output.json',d)
if __name__=='__main__':main()
