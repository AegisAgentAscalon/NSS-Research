"""Explicit opt-in CPU neural probe, standalone CLI and public lab coordinator."""
import argparse
from copy import deepcopy
from pathlib import Path
import os
import sys
from tempfile import TemporaryDirectory
import time

from .ledger import Ledger
from .neural_backend import (deterministic_cpu, encode_pairs, environment, load_checkpoint,
    metric, train_trial, evaluate_checkpoints)
from .neural_contracts import (CHECKER, FORMAT, encoded, fingerprint, pairs, protocol,
    read_document, required_updates, trial_verdict)
from .neural_data import ProbeData
from .neural_execution import recovery_check
from .neural_records import ProbeRuns, validate_plan, validate_report
from .runtime import ContractError, fail

ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/'fixtures/neuralprobe001/protocol.json'


def implementation():
    # Binds installed source, not a signed Python/PyTorch binary or security claim.
    from hashlib import sha256
    files={str(f.relative_to(ROOT)):sha256(f.read_bytes()).hexdigest()
           for f in sorted((ROOT/'nss_base').glob('*.py'))}
    return {'files':files,'sha256':fingerprint(files)}


def plan_for(p,data):
    return {'schema_version':2,'protocol':protocol(p),'data_binding':deepcopy(data.binding),
            'environment':environment(),'code_sha256':implementation()['sha256'],'authority':'NONE'}


def check_current(plan,data):
    validate_plan(plan)
    if plan['schema_version']!=2:
        fail('INCOMPATIBLE_CONFIGURATION','Legacy evidence lacks the numerical execution contract; historical inspection only')
    if (plan['environment']!=environment() or plan['code_sha256']!=implementation()['sha256']
            or plan['data_binding']!=data.binding):
        fail('INCOMPATIBLE_CONFIGURATION','Code, environment or data binding changed')
    data.gate()


def execute(store,id,plan,data,ledger,*,crash_at=None):
    """No caller scores/callbacks/backend code accepted. Terminal retry is history."""
    plan=validate_plan(plan)
    if crash_at not in (None,'after_prepared','after_training','before_commit','after_commit'):
        fail('VALIDATION_FAILED','Unknown fault hook')
    # Query history before current-use gate: inspectable history is NOT permission.
    try:old=store.inspect(id)
    except ContractError as exc:
        if exc.code!='INSUFFICIENT_EVIDENCE':raise
        old=None
    if old is not None:
        if old['plan']!=plan:fail('CONSTRAINT_CONFLICT','Retry plan differs')
        if old['status']=='FINALIZED':return old
    check_current(plan,data);store.prepare(id,plan)
    if crash_at=='after_prepared':os._exit(79)
    p=plan['protocol'];need=required_updates(p)
    report={'schema_version':1,'format':FORMAT,'plan_sha256':fingerprint(plan),
        'checker':CHECKER,'authority':'NONE','scope':'DEVELOPMENT_NEURAL_LINEAR_SMOKE_TEST',
        'verdict':'INCONCLUSIVE','stop_reason':'BUDGET_EXHAUSTED','completed_trials':0,
        'required_optimizer_updates':need,'trials':[],
        'data_permission_scope':'Point-in-time training-purpose gates; no lease, export recall or trained-weight unlearning.'}
    if p['max_optimizer_steps']>=need:
        task='neural-probe-replay'
        ledger.perform({'schema_version':1,'key':'neural-probe:one-mock-action','task_id':task,
                        'payload':{'operation':'append_marker','value':'synthetic probe side effect'},'status':'PENDING','receipt':None})
        for mode in p['precisions']:
            for seed in p['seeds']:
                check_current(plan,data)
                train=data.read('train');test=data.read('test')
                result,artifacts=train_trial(p,seed,mode,train,test,data.gate)
                with deterministic_cpu(seed):
                    recovery=recovery_check(artifacts,test[:4],fingerprint({'environment':plan['environment'],
                        'implementation':plan['code_sha256']}),ledger,task,p['recovery_atol'],p['recovery_rtol'])
                report['trials'].append({'result':result,'artifacts':artifacts,'recovery':recovery})
        report['completed_trials']=len(report['trials']);report['stop_reason']='COMPLETE'
        report['verdict']='PASS' if all(trial_verdict(p,row['result']['metrics'])=='PASS' for row in report['trials']) else 'FAIL'
    if crash_at=='after_training':os._exit(79)
    check_current(plan,data)
    return store.finalize(id,report,crash_at=crash_at if crash_at in ('before_commit','after_commit') else None)


def verify_numerics(stored,data,*,current=True):
    """Recompute scores from pinned data-only checkpoints, not caller-provided scores.

Historical verification may read retained evidence; current=False explicitly gives
NO permission for training/redeployment. Default goes through current-use gates.
"""
    plan=stored['plan'];r=validate_report(plan,stored['report'])
    if current:check_current(plan,data)
    p=plan['protocol'];checked=0
    for row in r['trials']:
        result=row['result'];ck=row['artifacts']
        with deterministic_cpu(result['seed']):
            if plan['schema_version']==2:
                metrics=evaluate_checkpoints(ck,result['checkpoint_hashes'],pairs('test'))
                if metrics!=result['metrics']:fail('VALIDATION_FAILED','Recorded scores differ from checkpoint inference')
                checked+=1
                continue
            mods={k:load_checkpoint(v,result['checkpoint_hashes'][k]) for k,v in ck.items()}
            core=mods['core'];test=pairs('test');x=encode_pairs(test)
            preds={'core':(core(x),'CORE'),'A':(core(x,a=mods['A']),'A'),
                   'B':(core(x,b=mods['B']),'B'),'AB':(core(x,a=mods['A'],b=mods['B']),'AB'),
                   'joint':(core(x,b=mods['joint']),'AB'),'gen2':(core(x,a=mods['A2'],b=mods['B']),'A2B'),
                   'ablation_A':(core(x,b=mods['B']),'AB'),'ablation_B':(core(x,a=mods['A']),'AB'),
                   'ablation_core':(core(x),'AB')}
            metrics={k:metric(y,test,n) for k,(y,n) in preds.items()}
            retained=[r for r in test if all(v not in (5,6) for v in r)]
            metrics['gen2_retained']=metric(core(encode_pairs(retained),a=mods['A2'],b=mods['B']),retained,'AB')
            if metrics!=result['metrics']:fail('VALIDATION_FAILED','Recorded scores differ from checkpoint inference')
            checked+=1
    return {'status':'SUCCESS','numerical_trials_recomputed':checked,'current_data_checked':current,
            'authority':'NONE','scope':'Same local implementation re-executed; not independent evaluator'}


def run(directory,p=None,*,withdraw=True):
    root=Path(directory)
    if root.exists() and any(root.iterdir()):fail('CONSTRAINT_CONFLICT','Probe requires an empty/new directory')
    root.mkdir(parents=True,exist_ok=True)
    p=protocol(read_document(DEFAULT) if p is None else p)
    (root/'protocol.json').write_bytes(encoded(p))
    data=ProbeData.create(root/'data');store=ProbeRuns.create(root/'journal');ledger=Ledger(root/'mock_actions')
    plan=plan_for(p,data);(root/'plan.json').write_bytes(encoded(plan))
    start=time.perf_counter();final=execute(store,'probe-001',plan,data,ledger)
    verification=verify_numerics(final,data)
    historical=store.inspect('probe-001');blocked=None;retry_historical=None
    if withdraw:
        data.revoke_for_test()
        try:check_current(plan,data)
        except ContractError as exc:blocked=exc.code
        else:fail('VALIDATION_FAILED','Revoked training data was still usable')
        retry=execute(store,'probe-001',plan,data,ledger)
        retry_historical=retry==historical
        if blocked!='TRAINING_RESTRICTED' or not retry_historical:
            fail('VALIDATION_FAILED','Revocation/history boundary failed')
    summary={'status':'SUCCESS','verdict':final['report']['verdict'],'scope':final['report']['scope'],
        'authority':'NONE','completed_trials':final['report']['completed_trials'],
        'required_optimizer_updates':required_updates(p),'total_seconds':time.perf_counter()-start,
        'numerical_verification':verification,'revoked_use_status':blocked,
        'retry_is_unchanged_history':retry_historical,'mock_external_effects':ledger.effect_count(),
        'journal_audit':store.audit(),'report_sha256':final['receipt']['report_sha256'],
        'trial_metrics':[{'seed':r['result']['seed'],'precision':r['result']['precision'],
                         'metrics':r['result']['metrics'],'recovery':r['recovery']} for r in final['report']['trials']]}
    (root/'report.json').write_bytes(encoded(final));(root/'summary.json').write_bytes(encoded(summary))
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory');parser.add_argument('--protocol');parser.add_argument('--keep-permission',action='store_true')
    args=parser.parse_args()
    try:
        p=read_document(args.protocol) if args.protocol else None
        if args.directory:result=run(args.directory,p,withdraw=not args.keep_permission)
        else:
            with TemporaryDirectory(prefix='megamind-neuralprobe001-') as d:result=run(d,p,withdraw=not args.keep_permission)
        print(encoded(result).decode())
        return 0 if result['verdict']=='PASS' else 2
    except ContractError as exc:
        print(encoded({'status':exc.code,'detail':str(exc),'authority':'NONE'}).decode(),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
