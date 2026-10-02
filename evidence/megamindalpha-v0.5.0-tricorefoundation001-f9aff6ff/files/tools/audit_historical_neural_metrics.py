#!/usr/bin/env python3
"""Post-hoc portability diagnostic. Does NOT relax live verifier or issue evidence.

The inherited strict verifier remains unchanged. This audit preserves exact
accuracy/count checks and separately reports small floating MSE discrepancies.
Its tolerances are NOT a retrospectively altered experimental acceptance threshold.
"""
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nss_base.neural_backend import deterministic_cpu, encode_pairs, environment, load_checkpoint, metric
from nss_base.neural_contracts import fingerprint, pairs, read_document
from nss_base.neural_records import validate_report


def main():
    path = ROOT/'docs/audits/neuralprobe001/confirmation_report.json'
    stored = read_document(path); r = validate_report(stored['plan'], stored['report'])
    mismatches = []; exact = True; within = True; count = 0
    for row in r['trials']:
        result = row['result']
        with deterministic_cpu(result['seed']):
            mods = {k:load_checkpoint(v,result['checkpoint_hashes'][k]) for k,v in row['artifacts'].items()}
            c = mods['core']; t = pairs('test'); x = encode_pairs(t)
            pred = {'core':(c(x),'CORE'),'A':(c(x,a=mods['A']),'A'),'B':(c(x,b=mods['B']),'B'),
                'AB':(c(x,a=mods['A'],b=mods['B']),'AB'),'joint':(c(x,b=mods['joint']),'AB'),
                'gen2':(c(x,a=mods['A2'],b=mods['B']),'A2B'),'ablation_A':(c(x,b=mods['B']),'AB'),
                'ablation_B':(c(x,a=mods['A']),'AB'),'ablation_core':(c(x),'AB')}
            actual={k:metric(y,t,target) for k,(y,target) in pred.items()}
            retained=[v for v in t if all(i not in (5,6) for i in v)]
            actual['gen2_retained']=metric(c(encode_pairs(retained),a=mods['A2'],b=mods['B']),retained,'AB')
            for k,new in actual.items():
                old=result['metrics'][k];count+=1
                for field in ('pair_accuracy','token_accuracy','pairs'):
                    exact = exact and old[field] == new[field]
                ok=math.isclose(new['mse'],old['mse'],rel_tol=1e-5,abs_tol=1e-8)
                within = within and ok
                if old['mse']!=new['mse']:
                    mismatches.append({'seed':result['seed'],'precision':result['precision'],'metric':k,
                        'stored_mse':old['mse'],'recomputed_mse':new['mse'],
                        'absolute_difference':abs(old['mse']-new['mse']),'within_diagnostic_tolerance':ok})
    result={'status':'DIAGNOSTIC_COMPLETE','stored_report_sha256':fingerprint(r),
        'metric_groups':count,'accuracies_and_counts_exact':exact,'mse_bit_exact':not mismatches,
        'mse_within_posthoc_diagnostic_tolerance':within,'mse_atol':1e-8,'mse_rtol':1e-5,
        'nominal_environment_equal':stored['plan']['environment']==environment(),
        'maximum_mse_difference':max([m['absolute_difference'] for m in mismatches],default=0),
        'differences':mismatches,'authority':'NONE','deployment_authorized':False,
        'qualification_eligible':False,
        'limitation':'Historical-only diagnostic. Strict current verifier unchanged. Lower-level cause of drift not established.'}
    print(json.dumps(result,indent=2));return 0 if exact and within else 1


if __name__=='__main__':raise SystemExit(main())
