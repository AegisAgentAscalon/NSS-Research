"""Fresh visible-catalogue/stream identity audit, not a claim of statistical independence."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from io_utils import ROOT,load,dump,lines,digest,array_digest,baseline,sha,check_lock

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--previous',type=Path);p.add_argument('--cm01',type=Path,default=Path('/mnt/data/_cm02_deps/NSS_CM01_Execution_v0.2'));a=p.parse_args();check_lock()
    oldbooks=set();oldstreams=set();fileaudit=[];books=0;streams=0
    for root in [baseline(),a.cm01]:
        for f in sorted(root.rglob('*.npz')):
            with np.load(f,allow_pickle=False) as z:
                hits=[]
                for name in z.files:
                    if not any(term in name.lower() for term in ('book','catalog')):continue
                    x=z[name]
                    if x.shape[-2:]!=(16,17):continue
                    for book in x.reshape(-1,16,17):oldbooks.add(array_digest({'book':book}));books+=1
                    hits.append({'array':name,'catalogues':int(x.reshape(-1,16,17).shape[0])})
            if hits:fileaudit.append({'dependency':root.name,'file':str(f.relative_to(root)),'sha256':sha(f),'arrays':hits})
        for f in sorted(root.rglob('public.jsonl')):
            for row in lines(f):
                if 'journal' in row:oldstreams.add(digest(row['journal']));streams+=1
            fileaudit.append({'dependency':root.name,'file':str(f.relative_to(root)),'sha256':sha(f),'public_journals':True})
    if a.previous:
        for m in lines(a.previous/'protected_sequences.jsonl'):oldbooks.add(m['book_digest']);oldbooks.add(m['base_book_digest']);oldstreams.add(m['stream_digest'])
    new=lines(a.input/'protected_sequences.jsonl');seen=set();collision=[]
    for m in new:
        if m['book_digest'] in oldbooks or m['base_book_digest'] in oldbooks or m['stream_digest'] in oldstreams:collision.append(m['episode_id'])
        if m['book_digest'] in seen:collision.append(m['episode_id'])
        seen.add(m['book_digest'])
    dump(a.output,dict(status='PASS_AVAILABLE_INPUT_IDENTITY_AUDIT' if not collision else 'FAIL_STOP',new_sequences=len(new),
        historical_catalogue_observations=books,unique_historical_catalogue_hashes=len(oldbooks),historical_public_journals=streams,unique_historical_journal_hashes=len(oldstreams),
        compared_files=fileaudit,collisions=collision,
        limitations=['Only retained book/catalogue arrays and named public journal files can be inspected. Missing historical raw main captures and RNG histories remain unavailable.',
                     'Exact nonidentity is not a proof of statistical independence or semantic non-overlap. Revisions/checkpoints within an episode intentionally share one catalogue.']))
    if collision:raise AssertionError('input identity collision; no resampling')
    print('INPUT IDENTITY AUDIT PASS',len(new),'new sequences;',books,'historical catalogue observations;',streams,'journals')
if __name__=='__main__':main()
