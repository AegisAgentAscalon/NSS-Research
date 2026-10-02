"""Post-result fresh-process replay and archive-bit mismatch diagnosis. No updates."""
from __future__ import annotations
import gzip,time,resource
from support import *
from nss_hsa import *
import sh01_common as old

def main():
    setup();start=time.perf_counter();rows=[]
    for seed in [8801,8802,8804]:
        c=torch.load(ROOT/f'checkpoints/{seed}_hsa_inference.pt',weights_only=True,map_location='cpu')
        a=MaintenanceReader();a.load_state_dict(c['model']);a.eval();b=old.Reader();b.load_state_dict(c['model']);b.eval()
        for split in ['development','confirmation','stress']:
            with gzip.open(ROOT/f'fixtures/{split}.jsonl.gz','rt') as f:ws=[json.loads(line) for line in f]
            saved=np.load(ROOT/f'results/clean_{seed}_{split}.npz');up=np.load(ROOT/f'reference/pred_{seed}_hsa_{split}.npz')
            out=[];legacy=[]
            # Reconstruct full upstream feature batch before slicing, as SH01 audit did.
            parts=old.batch(ws)
            with torch.no_grad():
                for i in range(0,len(ws),16):
                    x,ix,va,y=[p[i:i+16] for p in parts]
                    xx,ss=prepare_worlds(ws[i:i+16]);p=compile_plan(ss)
                    out.append(a(xx,p).numpy());legacy.append(b(x,ix,va,p.tasks,'hsa').numpy())
            new=np.concatenate(out);ll=np.concatenate(legacy)
            row={'seed':seed,'split':split,'fresh_clean_bit_exact':bool(np.array_equal(new,saved['logits'])),
                 'legacy_fullbatch_vs_archive_bit_exact':bool(np.array_equal(ll,up['logits'])),
                 'legacy_vs_archive_numerical':comparison(ll,up['logits']),
                 'legacy_vs_archive_class_changes':int((ll.argmax(-1)!=up['logits'].argmax(-1)).sum()),
                 'recount_match':old.metrics(saved['target'],new.argmax(-1))==old.metrics(up['target'],up['logits'].argmax(-1))}
            rows.append(row)
            if not row['legacy_fullbatch_vs_archive_bit_exact']:
                np.savez_compressed(ROOT/f'failures/legacy_bit_mismatch_{seed}_{split}.npz',legacy_current=ll,archive=up['logits'])
    lock=json.loads((ROOT/'SOURCE_LOCK.json').read_text());integrity=[]
    for name,info in lock['files'].items():integrity.append({'file':name,'match':sha(ROOT/name)==info['sha256']})
    result={'rows':rows,'locked_source_checks':integrity,'runtime':runtime(),'optimizer_updates':0,'elapsed_seconds':time.perf_counter()-start,
        'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        'scope':'Post-result engineering replay. Old-source original-archive bitwise failures retained; tolerance never changed.'}
    save(ROOT/'results/post_audit.json',result)
    print(json.dumps({'rows':rows,'locked_files_match':all(c['match'] for c in integrity)},indent=2))
if __name__=='__main__':main()
