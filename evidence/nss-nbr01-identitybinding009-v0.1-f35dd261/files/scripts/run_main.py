from pathlib import Path
import sys,argparse,time,json,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import *
from nbr009 import stage_a,stage_b,context
from nbr009.score import score_a,score_b,score_cue

def verify_lock():
    lock=json.loads((ROOT/'spec/EXECUTION_LOCK.json').read_text())
    for p,d in lock['hashes'].items():
        if sha(ROOT/p)!=d:raise RuntimeError('Changed locked input: '+p)
    return sha(ROOT/'spec/EXECUTION_LOCK.json')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pair',type=int,required=True);ap.add_argument('--out',type=Path);ap.add_argument('--stages',default='A,B,CUE');a=ap.parse_args()
    setup();lock=verify_lock();out=a.out or ROOT/'evidence/results';out.mkdir(parents=True,exist_ok=True);t=time.perf_counter();timing={}
    for tag in a.stages.split(','):
        fn={'A':stage_a.run,'B':stage_b.run,'CUE':context.run}[tag];score={'A':score_a,'B':score_b,'CUE':score_cue}[tag];path=out/f'{tag}_pair{a.pair}.npz'
        ts=time.perf_counter();fn(a.pair,path);rows=score(path);dump(path.with_name(path.stem+'_scores.json'),rows);timing[tag]=time.perf_counter()-ts
        print('COMPLETE',a.pair,tag,'seconds',timing[tag],'rows',len(rows),flush=True)
    dump(out/f'RUN_pair{a.pair}.json',{'pair':a.pair,'lock_sha':lock,'timing':timing,'wall_seconds':time.perf_counter()-t,'rss_max_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'env':env()})
if __name__=='__main__':main()
