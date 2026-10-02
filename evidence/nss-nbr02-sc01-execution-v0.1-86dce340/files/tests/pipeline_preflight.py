from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from support import *
from fixtures import episode
from run import execute

def main():
    setup();m,mid=load(8801);out=[]
    for n,family in [(8,'resume'),(32,'churn'),(128,'sweep'),(32,'oversize')]:
        ep=episode(n,991777,family);rows=[]
        for pol in ['index','cache','segment']:
            z=execute(ep,m,mid,pol);rows.append(z)
            assert z['numeric_violations']==0 and z['changed_classes']==0
            assert z['stats'].get('peak_active_rows',0)<=ep['record_cap']
            assert z['final_model_hash']==mid
        for a in rows[1:]:
            assert [(m['event'],m['job'],m['task'],m['status'],m.get('pred'))for m in a['observations']]==[(m['event'],m['job'],m['task'],m['status'],m.get('pred'))for m in rows[0]['observations']]
        out.extend(rows)
    save(ROOT/'results'/'pipeline_preflight.json',{'status':'PASS','conditions':out,'runtime':runtime()})
    print('pipeline preflight',len(out),'conditions PASS',sum(z['numeric_scalars']for z in out),'scalars',flush=True)
if __name__=='__main__':main()
