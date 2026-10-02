"""Coordinator streams committed public events; worker receives neither future nor truth."""
from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
from io_utils import ROOT,canonical,load,dump,lines,sha,check_lock

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--kind',choices=['fixture','main'],required=True);a=p.parse_args()
    lock=check_lock();a.output.mkdir(parents=True,exist_ok=False);(a.output/'outputs').mkdir();seeds=[1201] if a.kind=='fixture' else list(range(1201,1206))
    err=(a.output/'worker.stderr.log').open('w');proc=subprocess.Popen([sys.executable,str(ROOT/'src/worker.py'),'--seeds',','.join(map(str,seeds)),'--attempt-log',str(a.output/'ATTEMPTS.json')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True,bufsize=1)
    def receive():
        line=proc.stdout.readline()
        if not line:raise RuntimeError('worker closed stdout: '+(a.output/'worker.stderr.log').read_text())
        msg=json.loads(line)
        if msg.get('type')=='fatal':raise RuntimeError('worker failure '+str(msg))
        return msg
    def request(msg):proc.stdin.write(canonical({'public':msg}).decode()+'\n');proc.stdin.flush();return receive()
    ready=receive();dump(a.output/'LOADER_AUDIT.json',ready);outputs=[];querycount=0
    try:
        with (a.output/'events.jsonl').open('wb') as ef,(a.output/'queries.jsonl').open('wb') as qf,(a.output/'timing.jsonl').open('wb') as tf:
            for eid in load(a.input/'PUBLIC_ORDER.json'):
                pub=load(a.input/'public'/f'{eid}.json');request({'type':'begin','episode_id':eid,'catalogue':pub['catalogue']})
                bycount={x['event_count']:x for x in pub['queries']}
                for ei,event in enumerate(pub['events'],1):
                    result=request({'type':'event','event':event});tf.write(canonical({'kind':'event','episode_id':eid,'event_count':ei,'timing_ns':result.pop('timing_ns')})+b'\n');ef.write(canonical(result)+b'\n')
                    if ei not in bycount:continue
                    q=bycount[ei];result=request(dict(type='query',**q));tf.write(canonical({'kind':'query','query_id':q['query_id'],'timing_ns':result.pop('timing_ns')})+b'\n')
                    for out in result.pop('new_outputs'):
                        arr=out.pop('arrays');data={k:np.asarray(v,np.int64 if k in ('resolved_ids','selected_rows') else np.float32) for k,v in arr.items()}
                        name='outputs/'+out['output_id']+'.npz';np.savez_compressed(a.output/name,**data);out.update(file=name,sha256=sha(a.output/name));outputs.append(out)
                    qf.write(canonical(result)+b'\n');qf.flush();querycount+=1
            finished=request({'type':'finish'});proc.stdin.close();code=proc.wait(timeout=30)
            if code!=0:raise RuntimeError('worker exit '+str(code))
        dump(a.output/'CAPTURE.json',dict(kind=a.kind,source_lock_sha256=lock,queries=querycount,outputs=outputs,summary=finished,original_input_lock_sha256=sha(a.input/'INPUT_LOCK.json')))
        print(f'CAPTURE {a.kind}: {querycount} queries, {len(outputs)} distinct forwards',flush=True)
    except BaseException:
        proc.kill();proc.wait();raise
    finally:err.close()
if __name__=='__main__':main()
