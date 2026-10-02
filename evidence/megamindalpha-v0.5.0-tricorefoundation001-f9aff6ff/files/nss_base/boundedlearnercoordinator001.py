"""Opt-in integrated local learning demo. Human approvals here are SCRIPTED.

Completes through a release PROPOSAL. Current qualifier cannot accept A2/A2B;
there is deliberately no candidate-to-production shortcut or generic Runtime work.
"""
import argparse
from copy import deepcopy
from pathlib import Path
import sys
import time
from tempfile import TemporaryDirectory
from .context_contracts import make_request
from .context_service import ContextService
from .learner_cli import initialize, open_learner
from .learner_contracts import CRITERIA, FORMAT, RECIPE_ID, learning_plan, operation_id
from .learner_coordinator import unwrap
from .neural_contracts import encoded, fingerprint, pairs, read_document
from .neural_data import ProbeData
from .neural_records import ProbeRuns
from .overlaycatalogcontroller001 import prepare_catalog, FIXTURE
from .runtime import ContractError, fail

OPERATORS={'schema_version':1,'format':FORMAT,'producer_ids':['learner-worker'],'approver_ids':['human-operator']}


def local_config(root):
    root=Path(root).resolve()
    return {k:str(root/v) for k,v in {'cycles':'learner/cycles','archive':'learning-data/experience',
        'snapshots':'learning-data/snapshots','tokenizer':'learning-data/codec.json',
        'qualifications':'qualification','parent_journal':'probe/journal','parent_data':'probe/data',
        'candidates':'learner/candidates','evaluations':'learner/evaluations'}.items()}


def plan_from_reviewed_data(co, *, cycle_id='learn-001', seed=31, steps=350, origin=None):
    """Explicit fixture authoring helper, not a learned planning/curation mechanism."""
    core=co.qualifications.inspect('core');request=deepcopy(unwrap(co.snapshots.inspect('neural-pairs-v1'))['manifest']['request'])
    request.update(operation_id='snapshot:'+cycle_id,snapshot_id='dataset:'+cycle_id,at='2026-09-11T12:00:00Z')
    request['members']=[{**unwrap(co.archive.inspect('neural-'+split))['reference'],'split':split} for split in ('train','validation')]
    request['members'].sort(key=lambda x:x['experience_id'])
    return learning_plan({'schema_version':1,'format':FORMAT,'cycle_id':cycle_id,'producer_id':'learner-worker',
        'at':co.now(),'reason':'Human-selected missing swap 5/6 capability in an installed synthetic recipe.',
        'parent':core['request']['binding'],
        'parent_core_certificate':{'request_id':'core','certificate_sha256':fingerprint(core['certificate'])},
        'archive_sha256':unwrap(co.archive.binding())['sha256'],'snapshot_request':request,
        'recipe':{'id':RECIPE_ID,'seed':seed,'steps':steps,'learning_rate':.03},
        'budget':{'optimizer_updates':steps,'evaluation_passes':2,'training_attempts':1},'criteria':deepcopy(CRITERIA),
        'code_sha256':core['request']['binding']['code_sha256'],
        'environment_sha256':core['request']['binding']['environment_sha256'], 'origin':origin,'authority':'NONE'})


def prepare_learning_fixture(directory):
    root=Path(directory);ctl,ch,_,original=prepare_catalog(root)
    data=ProbeData.create(root/'learning-data');config=local_config(root);initialize(config,OPERATORS)
    co=open_learner(config);manager=ctl.generations;ledger=ctl.inputs['ledger'];task='neural-probe-replay'
    # The real catalogue/task/context owners are exercised before learning begins.
    req={'schema_version':1,'catalog_sha256':ch,'expected_current':manager.inspect()['current'],
        'task_id':task,'stage':{'id':'learning-request','mode':'WORK','sealed':False,
            'objective':'Record the explicitly requested synthetic swap-5/6 improvement',
            'required_facts':[],'requested_output':'Portable requirements, not training or release authority'},
        'capabilities':['interpret'],'pairs':pairs('test')[:4],
        'budget':{'max_document_bytes':1000000,'max_cost_units':1000}}
    record=read_document(FIXTURE/'task_record.json');record.update(task_id=task,stage=req['stage'])
    record['receipts']=[{'key':k,'kind':'mock_action','receipt':ledger.inspect(k)['receipt']} for k in ledger.action_keys(task)]
    ctl.apply({'schema_version':1,'operation_id':'learning-start','caller_id':'local-runner','action':'START',
        'request':req,'ticket_id':'learning-stage','record':record})
    def act(kind,**extra):
        v=ctl.inspect(task)
        return ctl.apply({'schema_version':1,'operation_id':kind+':'+v['ticket']['ticket_id'],
            'caller_id':'local-runner','action':kind,'source_ticket':v['ticket'],
            'expected_record_sha256':fingerprint(v['work']['record']),**extra})
    def view():
        v=ctl.inspect(task)
        return ctl.read(v['ticket'],caller_id='local-runner',expected_record_sha256=fingerprint(v['work']['record']))
    sequence=['AB']
    for cap,stage,mode in [('solve','learning-solve','WORK'),('control','learning-control','CONTROL')]:
        act('FINISH',results=[],receipts=[]);r=deepcopy(req)
        r['capabilities']=[cap];r['stage'].update(id=stage,mode=mode)
        act('MOVE',request=r,ticket_id=stage);sequence.append(view()['ticket']['profile'])
    task_view=view();service=ContextService(ctl,archive=data.archive)
    packet=unwrap(service.build(make_request(task_view,'local-runner')))
    unwrap(service.consume(packet,caller_id='local-runner',expected_packet_sha256=fingerprint(packet)))
    act('FINISH',results=[],receipts=[])
    completed_record=ctl.inspect(task)['work']['record']
    origin={'task_id':task,'record_sha256':fingerprint(completed_record),'context_packet_sha256':fingerprint(packet)}
    act('CLOSE');before_generation=manager.inspect();before_task=ctl.inspect(task)
    # Persist the exact completed-task context as evidence, not automatic train text.
    actor={'id':'scripted-reviewer','kind':'HUMAN','version':'fixture-not-authenticated'};at='2026-09-11T12:00:00Z'
    ref=unwrap(data.archive.inspect('neural-train'))['reference'];content=encoded({'record':completed_record,'packet':packet}).decode()
    from hashlib import sha256
    evidence={'id':'completed-work','kind':'TASK_SNAPSHOT','author':actor,'recorded_at':at,
        'media_type':'application/json','content':content,'sha256':sha256(content.encode()).hexdigest(),
        'generator':None,'parent_source_ids':['pairs'],'rights_note':'Synthetic task snapshot; scripted operator approval only.'}
    def change(action,payload):
        ref=unwrap(data.archive.inspect('neural-train'))['reference']
        return unwrap(data.archive.change({'schema_version':1,'operation_id':'learning:'+action,'experience_id':'neural-train',
            'expected_revision_hash':ref['sha256'],'actor':actor,'at':at,'reason':'Explicit fixture curation, not autonomous judgment.',
            'action':action,'payload':payload}))
    text=unwrap(data.archive.inspect('neural-train'))['record']['statement']['text']
    change('CORRECT',{'statement':{'text':text,'uncertainty':'LOW','support_ids':['pairs','completed-work']},'evidence':[evidence]})
    change('REVIEW',{'decision':'APPROVED'})
    change('PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'fixture:learning-approved'})
    plan=plan_from_reviewed_data(co,origin=origin)
    (root/'learner_owners.json').write_bytes(encoded(config));(root/'learning-plan.json').write_bytes(encoded(plan))
    (root/'learner-operators.json').write_bytes(encoded(OPERATORS))
    co.prepare(plan)
    try:co.advance(plan['cycle_id'],caller_id=plan['producer_id'])
    except ContractError as e:unapproved=e.code
    else:unapproved='NOT_BLOCKED'
    co.cycles.approve(plan['cycle_id'],approver_id='human-operator',expires_at=co.now()+3600,at=co.now())
    final=co.advance(plan['cycle_id'],caller_id='learner-worker')
    return dict(root=root, ctl=ctl, data=data, config=config, co=co, manager=manager,
        ledger=ledger, task=task, plan=plan, final=final, sequence=sequence, original=original,
        before_generation=before_generation, before_task=before_task, unapproved=unapproved)


def run(directory):
    f=prepare_learning_fixture(directory)
    root=f['root'];ctl=f['ctl'];data=f['data'];config=f['config'];co=f['co'];manager=f['manager']
    ledger=f['ledger'];task=f['task'];plan=f['plan'];final=f['final'];sequence=f['sequence'];original=f['original']
    before_generation=f['before_generation'];before_task=f['before_task'];unapproved=f['unapproved']
    current=co.check_proposal(plan['cycle_id'])
    tr=co.training.inspect(operation_id(plan,'TRAIN'));ev=co.evaluations.inspect(operation_id(plan,'EVALUATE'))
    reopened=open_learner(config);history=reopened.advance(plan['cycle_id'],caller_id='learner-worker')
    count_before=co.training.audit()['attempts']
    data.revoke_for_test()
    try:co.check_proposal(plan['cycle_id'])
    except ContractError as e:withdrawn=e.code
    else:withdrawn='NOT_BLOCKED'
    unchanged=co.advance(plan['cycle_id'],caller_id='learner-worker')==final
    summary={'status':'SUCCESS','scope':'CONNECTED_HUMAN_ASSISTED_DEMO_THROUGH_REVIEW_ONLY_PROPOSAL',
        'profile_sequence':sequence,'unapproved_dispatch':unapproved,'plan_sha256':fingerprint(plan),
        'snapshot_sha256':final['receipts']['SNAPSHOT']['sha256'],
        'candidate_sha256':tr['report']['checkpoint_hashes']['A2'],'parent_core_sha256':tr['report']['checkpoint_hashes']['core'],
        'core_and_parent_overlays_unchanged':tr['report']['invariants'],
        'optimizer_updates':tr['report']['training']['updates'],'numerical_verdict':ev['report']['verdict'],
        'metrics':ev['report']['repeats'][0],'exact_repeats':ev['report']['repeats'][0]==ev['report']['repeats'][1],
        'proposal_current_use_status':current['status'],'missing_qualification':current['missing_claims'],
        'proposal_after_revocation':withdrawn,'historical_retry_unchanged':history==final and unchanged,
        'no_retraining_on_retry':co.training.audit()['attempts']==count_before==1,
        'production_generation_unchanged':manager.inspect()==before_generation,
        'task_unchanged_by_learning':ctl.inspect(task)==before_task,
        'original_neural_report_unchanged':ProbeRuns(root/'probe/journal').inspect('probe-001')==original,
        'mock_external_effect_count':ledger.effect_count(),'candidate_deployed':False,'runtime_execution_permit':False}
    required=['exact_repeats','historical_retry_unchanged','no_retraining_on_retry','production_generation_unchanged',
        'task_unchanged_by_learning','original_neural_report_unchanged']
    if (not all(summary[k] for k in required) or unapproved!='AUTHORIZATION_DENIED'
            or withdrawn!='TRAINING_RESTRICTED' or current['status']!='INSUFFICIENT_EVIDENCE'
            or ledger.effect_count()!=1 or sequence!=['AB','A','CORE'] or ev['report']['verdict']!='PASS'):
        fail('VALIDATION_FAILED','Connected learner demonstration invariant failed')
    (root/'candidate-report.json').write_bytes(encoded(tr));(root/'evaluation-report.json').write_bytes(encoded(ev))
    (root/'release-proposal.json').write_bytes(encoded(final['proposal']));(root/'summary.json').write_bytes(encoded(summary))
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory');a=p.parse_args()
    try:
        if a.directory:r=run(a.directory)
        else:
            with TemporaryDirectory(prefix='megamind-learner-') as d:r=run(d)
        print(encoded(r).decode());return 0
    except ContractError as e:
        print(encoded({'status':e.code,'detail':str(e),'authority':'NONE'}).decode(),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
