"""Exact fresh-process replay comparison; wall time excluded, no numeric tolerance."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from io_utils import load,dump,lines,canonical,sha,check_lock

def main():
    p=argparse.ArgumentParser();p.add_argument('--a',type=Path,required=True);p.add_argument('--b',type=Path,required=True);p.add_argument('--output',type=Path,required=True);arg=p.parse_args();check_lock()
    ac,bc=load(arg.a/'capture/CAPTURE.json'),load(arg.b/'capture/CAPTURE.json');narr=0;nels=0;raw_identical=0;semanticfiles=0
    ai,bi=load(arg.a/'input/INPUT_LOCK.json'),load(arg.b/'input/INPUT_LOCK.json')
    if ai!=bi:raise AssertionError('regenerated input lock differs')
    for file in ai['files']:
        if (arg.a/'input'/file).read_bytes()!=(arg.b/'input'/file).read_bytes():raise AssertionError('regenerated input bytes differ: '+file)
        semanticfiles+=1
    ad={x['output_id']:x for x in ac['outputs']};bd={x['output_id']:x for x in bc['outputs']}
    if set(ad)!=set(bd):raise AssertionError('replay output keys differ')
    for oid,a in ad.items():
        b=bd[oid]
        if {k:v for k,v in a.items() if k!='sha256'}!={k:v for k,v in b.items() if k!='sha256'}:raise AssertionError('output provenance differs')
        ap,bp=arg.a/'capture'/a['file'],arg.b/'capture'/b['file'];raw_identical+=int(sha(ap)==sha(bp))
        with np.load(ap,allow_pickle=False) as x,np.load(bp,allow_pickle=False) as y:
            if set(x.files)!=set(y.files):raise AssertionError('array key mismatch')
            for name in x.files:
                v,w=x[name],y[name]
                if v.dtype!=w.dtype or v.shape!=w.shape or v.tobytes()!=w.tobytes():raise AssertionError('not exact: '+oid+'/'+name)
                narr+=1;nels+=v.size
    for name in ['events.jsonl','queries.jsonl','LOADER_AUDIT.json','ATTEMPTS.json']:
        if (arg.a/'capture'/name).read_bytes()!=(arg.b/'capture'/name).read_bytes():raise AssertionError('deterministic capture file differs: '+name)
        semanticfiles+=1
    aca={k:v for k,v in ac.items() if k!='outputs'};bca={k:v for k,v in bc.items() if k!='outputs'}
    if aca!=bca:raise AssertionError('capture summary differs')
    scorefiles=0
    if (arg.a/'scores').is_dir() and (arg.b/'scores').is_dir():
        for x in (arg.a/'scores').iterdir():
            if x.is_file():
                y=arg.b/'scores'/x.name
                if x.read_bytes()!=y.read_bytes():raise AssertionError('independent score replay differs: '+x.name)
                scorefiles+=1
    dump(arg.output,dict(status='PASS_EXACT_FRESH_PROCESS_REPLAY',arrays=narr,elements=nels,distinct_outputs=len(ad),byte_identical_npz_containers=raw_identical,
       deterministic_metadata_files=semanticfiles,byte_identical_independently_scored_files=scorefiles,
       excluded=['timing.jsonl','worker stderr logs','external supervisor elapsed/RSS/cgroup receipts'],
       no_new_scientific_samples=True))
    print(load(arg.output))
if __name__=='__main__':main()
