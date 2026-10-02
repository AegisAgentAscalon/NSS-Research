"""Pre-generation source and protocol lock, with immutable export and seed checks."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,time
from io_utils import ROOT,baseline,load,dump,sha

def main():
    if (ROOT/'protocol/SOURCE_LOCK.json').exists():raise FileExistsError('Never overwrite an execution lock')
    seeds=load(ROOT/'protocol/SEEDS.json');ss=seeds['numeric_seeds']
    assert len(ss)==477 and len(set(ss.values()))==477 and all(ss.values())
    for label,n in ss.items():assert n==int.from_bytes(hashlib.sha256((seeds['namespace']+'/'+label).encode()).digest()[:8],'big')
    b=baseline();models=load(ROOT/'protocol/FROZEN_EXPORT_IDENTITIES.json')['all_15_exports']
    for r in models:
        assert sha(b/'provenance/saved_main_exports'/r['file'])==r['sha256']
    deps={str(p.relative_to(b)):sha(p) for p in b.rglob('*.py') if '__pycache__' not in p.parts and 'failures' not in p.parts}
    for p in [*sorted((b/'protocol').glob('*.json')),*sorted((b/'provenance/saved_main_exports').glob('*'))]:
        if p.is_file():deps[str(p.relative_to(b))]=sha(p)
    scientific={str(p.relative_to(ROOT)):sha(p) for folder in ('src','protocol') for p in sorted((ROOT/folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    audit=load(ROOT/'audit/INPUT_INTEGRITY.json');expected=load(ROOT/'protocol/SOURCE_IDENTITIES.json')
    am={x['archive']:x['sha256'] for x in audit}
    for r in expected['inputs']:
        if r['id'] in ('cm01','q010'):assert am[r['local_archive']]==r['sha256']
    dump(ROOT/'audit/SEED_REVALIDATION.json',{'status':'PASS_477_REDERIVED_AND_UNIQUE','allocations':len(ss),'existing_review_collision_audit_sha256':sha(ROOT/'protocol/SEED_AUDIT.json'),
       'prior_audit_dependencies_match_current_archives':True,'new_seed_namespace_introduced':False,'missing_historical_rng_histories_auditable':False})
    dump(ROOT/'protocol/SOURCE_LOCK.json',{'id':'CM02_EXECUTION_SOURCE_LOCK_v0.6','locked_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        'study_files':scientific,'baseline_files':deps,'main_cases_generated_before_lock':0,'fixture_cases_generated_before_lock':0,'experimental_model_forwards_before_lock':0,
        'non_neural_contract_test_methods_before_lock':19,'failed_previous_version_model_forwards':2395,'failed_previous_version':'v0.3 failed fixture; v0.4/v0.5 interrupted main; successful v0.5 fixture carried with exact scientific-source identity','no_post_lock_changes_permitted':True})
    assert load(ROOT/'audit/GLOBAL_FORWARD_LEDGER.json')['attempted']==2395  # Preserve all previous failed/interrupted calls in the hard budget.
    print('LOCKED',len(scientific),'study files;',len(deps),'dependency source/protocol/export files;',sha(ROOT/'protocol/SOURCE_LOCK.json'))
if __name__=='__main__':main()
