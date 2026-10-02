"""Verify this documentation package. No scientific model or experiment is imported."""
from pathlib import Path
import hashlib,json

def main():
    root=Path(__file__).resolve().parent
    m=json.loads((root/'MANIFEST.json').read_text())
    for r in m['files']:
        p=root/r['path']
        if not p.is_file(): raise SystemExit('Missing '+r['path'])
        b=p.read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
            raise SystemExit('Mismatch '+r['path'])
    s=json.loads((root/'STATUS.json').read_text())
    assert not s['execution_authorized'] and s['training_updates']==0 and s['inference_calls']==0
    seeds=json.loads((root/'SEEDS.json').read_text())
    nums=[r['uint64'] for r in seeds['allocations']]
    assert len(nums)==27==len(set(nums)) and min(nums)>0
    for r in seeds['allocations']:
        assert r['uint64']==int.from_bytes(hashlib.sha256((seeds['namespace']+'|'+r['label']).encode('ascii')).digest()[:8],'big')
    c=json.loads((root/'CALL_AND_STORAGE_LEDGER.json').read_text())
    for k in c['per_pass_totals']:
        assert c['per_pass_totals'][k]==sum(x[k] for x in c['one_pass_stages'])
        assert 2*c['per_pass_totals'][k]==c['capture_plus_fresh_adaptive_replay'][k]
        assert c['capture_plus_fresh_adaptive_replay'][k]<=c['hard_all_attempt_caps'][k]
    assert c['capture_plus_fresh_adaptive_replay']['updates']==3856
    assert c['capture_plus_fresh_adaptive_replay']['cell_examples']==112032
    assert c['capture_plus_fresh_adaptive_replay']['head_vectors']==36544
    assert c['planned_schema_slot_bytes']<c['raw_hard_cap_bytes']
    print(json.dumps({'status':'DOCUMENT_PACKAGE_VERIFIED','files':len(m['files']),'experiment_run':False}))

if __name__=='__main__':main()
