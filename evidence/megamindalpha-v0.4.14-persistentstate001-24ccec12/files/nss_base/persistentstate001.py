"""Opt-in scoped symbolic persistence demo; proposer and reviewers are scripted.

Uses existing neural-probe artifacts solely to exercise the admitted runtime
boundary. State updates themselves neither train weights nor execute effects.
"""
import argparse
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
from .catalog_controller import CatalogController
from .context_contracts import make_request
from .context_plan import unwrap
from .context_service import ContextService
from .contextretrieval001 import reviewed_fixture, ACTOR, AT
from .experience_store import ExperienceArchive
from .generation_store import Generations, now_seconds
from .neural_contracts import encoded, fingerprint, pairs, read_document
from .neural_records import ProbeRuns
from .overlaycatalogcontroller001 import prepare_catalog, FIXTURE
from .runtime import ContractError, fail
from .state_contracts import prepare, attest, POLICY

SCOPE={'agent_id':'fixture-cerys','project_id':'fixture-nss','session_id':'state-session-1'}
ROOT_INSTRUCTIONS='Keep facts separate from interpretations. Do not grant authority to saved state.'
SOURCE={'kind':'TASK','source_id':'source-1','field_id':'speed'}
CALLER='local-runner'


def rejected(operation):
    try:operation()
    except ContractError as e:return e.code
    fail('VALIDATION_FAILED','Expected operation to be rejected')


def run(directory):
    root=Path(directory);base,ch,_,original=prepare_catalog(root)
    archive=ExperienceArchive.create(root/'state-archive');manager=base.generations
    ctl=CatalogController(manager,archive=archive,**base.inputs,**base.evidence)
    ledger=ctl.inputs['ledger'];task='neural-probe-replay';service=ContextService(ctl,archive=archive)
    policy={'policy_id':POLICY,'instruction_policy_sha256':fingerprint({'instructions':ROOT_INSTRUCTIONS}),'max_record_bytes':65536}
    def stage(label,id,mode='WORK'):
        return {'schema_version':1,'catalog_sha256':ch,'expected_current':manager.inspect()['current'],
            'task_id':task,'stage':{'id':id,'mode':mode,'sealed':False,'objective':'Keep source-backed state',
                'required_facts':[],'requested_output':'Preserve exact work and unresolved questions'},
            'capabilities':[label],'pairs':pairs('test')[:4],
            'budget':{'max_document_bytes':1000000,'max_cost_units':1000}}
    req=stage('interpret','observe');record=read_document(FIXTURE/'task_record.json')
    record.update(task_id=task,stage=req['stage'])
    record['receipts']=[{'key':k,'kind':'mock_action','receipt':ledger.inspect(k)['receipt']} for k in ledger.action_keys(task)]
    ctl.apply({'schema_version':1,'operation_id':'state-start','caller_id':CALLER,'action':'START',
        'request':req,'ticket_id':'state-observe','record':record})
    legacy=ctl.inspect(task);initial=ctl.read(legacy['ticket'],caller_id=CALLER,expected_record_sha256=fingerprint(legacy['work']['record']))
    weights_before=fingerprint(initial['artifacts']);current_before=manager.inspect()['current']
    def approved(c):
        at=now_seconds()
        return attest(c,reviewer_id='generation-reviewer',reviewed_at=at,expires_at=at+600,
            reason='Scripted review declaration for synthetic fixtures, not an authenticated human')
    bind=approved(prepare(initial,operation_id='state-bind',state_scope=SCOPE,policy=policy,
        archive_binding=unwrap(archive.binding()),proposer_id='deterministic-proposer',proposer_version='v1'))
    ctl.apply(bind)
    def history():return ctl.inspect(task,caller_id=CALLER,scope=SCOPE)
    def view():
        h=history();return ctl.read(h['ticket'],caller_id=CALLER,scope=SCOPE,expected_record_sha256=fingerprint(h['work']['record']))
    def propose(ops,event):
        h=history()
        return prepare({'ticket':h['ticket'],'record':h['work']['record']},operation_id=event,state_scope=SCOPE,
            proposer_id='deterministic-proposer',proposer_version='v1',deltas=ops)
    delta=propose([{'op':'SET_GOAL','text':'Retain and verify the observed speed across a restart','source_refs':[SOURCE]},
        {'op':'ADD_QUESTION','id':'speed-question','text':'What is the exact recorded speed value?',
         'blocking':True,'source_refs':[SOURCE]}], 'state-event-1')
    missing_review=rejected(lambda:ctl.apply(delta));reviewed=approved(delta);ctl.apply(reviewed)
    duplicate=ctl.apply(reviewed);before=view()
    # Reopen durable owner, not an in-memory substitute.
    manager=Generations(root/'generations');ctl=CatalogController(manager,archive=archive,**base.inputs,**base.evidence)
    service=ContextService(ctl,archive=archive);restored=view();restart_equal=restored==before
    packet=unwrap(service.build(make_request(restored,CALLER)))
    wrong_scope=rejected(lambda:ctl.read(restored['ticket'],caller_id=CALLER,scope={**SCOPE,'agent_id':'other'},
        expected_record_sha256=fingerprint(restored['record'])))
    small=make_request(restored,CALLER,max_context_bytes=1);overflow=service.build(small)
    ctl.apply(approved(propose([{'op':'RESOLVE_QUESTION','id':'speed-question','answer':'10','source_refs':[SOURCE]}], 'state-event-2')))
    stale_packet=service.consume(packet,caller_id=CALLER,expected_packet_sha256=fingerprint(packet))
    identity,src=reviewed_fixture(archive,'identity-example','A fictional fixture values careful source attribution.',
                                  sensitivity='IDENTITY_SENSITIVE')
    note={'id':'identity-note','text':'This fixture values source attribution.','kind':'CLAIM','status':'HYPOTHESIS',
          'confidence':None,'mandatory':True,'identity_sensitive':True,'expires_at':None}
    identity_command=approved(propose([{'op':'ADD_NOTE','note':note,
        'source_refs':[{'kind':'EXPERIENCE','reference':identity}]}], 'state-event-3'))
    ctl.apply(identity_command);approved_identity_state=view()
    unwrap(archive.change({'schema_version':1,'operation_id':'challenge-state-identity','experience_id':'identity-example',
        'expected_revision_hash':identity['sha256'],'actor':ACTOR,'at':AT,'reason':'Synthetic challenge',
        'action':'DISPUTE','payload':{'conflict_id':'identity-challenge','support_ids':[src['id']],'evidence':[]}}))
    disputed=rejected(view);historical_identity=history()['work']['record']==approved_identity_state['record']
    duplicate_after_dispute=ctl.apply(identity_command)
    ctl.apply(approved(propose([{'op':'RETIRE_NOTE','id':'identity-note','reason':'Disputed interpretation withheld from current use',
                               'source_refs':[]}], 'state-event-4')))
    live_after_retirement=view()
    def life(action,event,**extra):
        h=history()
        return ctl.apply({'schema_version':2,'operation_id':event,'caller_id':CALLER,'scope':SCOPE,'action':action,
            'source_ticket':h['ticket'],'expected_record_sha256':fingerprint(h['work']['record']),**extra})
    state_before_moves=live_after_retirement['record']['persistent_state'];sequence=['AB']
    life('FINISH','finish-observe',results=[],receipts=[])
    next_stage=stage('solve','solve');next_stage['stage']['required_facts']=[{'fact_id':'speed','fields':['value','unit']}]
    life('MOVE','move-solve',request=next_stage,ticket_id='state-solve');v=view();sequence.append(v['ticket']['profile'])
    solve_packet=unwrap(service.build(make_request(v,CALLER)))
    life('FINISH','finish-solve',results=[],receipts=[])
    life('MOVE','move-control',request=stage('control','control','CONTROL'),ticket_id='state-control')
    final=view();sequence.append(final['ticket']['profile'])
    state_preserved=final['record']['persistent_state']==state_before_moves
    life('FINISH','finish-control',results=[],receipts=[]);life('CLOSE','close-task')
    state_history=ctl.state_history(task,caller_id=CALLER,scope=SCOPE)
    old_retry=ctl.apply(reviewed)
    # Compare original sealed bundle; no new model training or release happened during state work.
    weights_after=fingerprint(manager.inspect_release('adopt')['artifacts'])
    summary={'status':'SUCCESS','scope':'SCOPED_SYMBOLIC_STATE_NOT_LEARNED_TEMPORAL_MEMORY',
        'manual_review_required':missing_review,'reviewed_restart_exact':restart_equal,
        'goal':restored['record']['goal'],'open_question':restored['record']['unresolved_questions'][-1]['text'],
        'duplicate_is_history':duplicate['historical'],'wrong_scope_rejected':wrong_scope,
        'mandatory_overflow':overflow['status'],'stale_packet_rejected':stale_packet['status'],
        'disputed_identity_blocks_current_use':disputed,'disputed_revision_preserved':historical_identity,
        'duplicate_after_dispute_is_history':duplicate_after_dispute['historical'],
        'source_unit':solve_packet['payload']['facts'][0]['unit'],'profile_sequence':sequence,
        'scope_and_provenance_survive_moves':state_preserved,'task_closed':history()['closed'],
        'historical_retry_did_not_reopen':old_retry['historical'] and history()['closed'],
        'history_revisions':len(state_history['history']),
        'core_and_overlay_artifacts_unchanged':weights_before==weights_after,
        'current_generation_unchanged':current_before==manager.inspect()['current'],
        'root_instruction_reference_unchanged':final['record']['persistent_state']['policy']==policy,
        'original_neural_report_unchanged':original==ProbeRuns(root/'probe/journal').inspect('probe-001'),
        'mock_external_effect_count':ledger.effect_count(),'learned_proposer':False,
        'authenticated_review':False,'new_training_or_runtime_authority':False,
        'state_byte_budget':policy['max_record_bytes'],'final_record_bytes':len(encoded(final['record']))}
    checks=('reviewed_restart_exact','duplicate_is_history','disputed_revision_preserved',
        'duplicate_after_dispute_is_history','scope_and_provenance_survive_moves','task_closed','historical_retry_did_not_reopen',
        'core_and_overlay_artifacts_unchanged','current_generation_unchanged','root_instruction_reference_unchanged','original_neural_report_unchanged')
    if not (all(summary[k] for k in checks) and sequence==['AB','A','CORE'] and summary['source_unit']=='m/s'
        and summary['mock_external_effect_count']==1 and missing_review=='NEEDS_CLARIFICATION'
        and wrong_scope=='AUTHORIZATION_DENIED' and overflow['status']=='BUDGET_EXHAUSTED'
        and stale_packet['status']!='SUCCESS' and disputed!='SUCCESS'):
        fail('VALIDATION_FAILED','Persistent-state demonstration failed its scoped invariants')
    for name,value in [('scope',SCOPE),('bind-operation',bind),('unreviewed-proposal',delta),('reviewed-operation',reviewed),
                       ('historical-context',packet),('state-history',state_history),('summary',summary)]:
        (root/(name+'.json')).write_bytes(encoded(value))
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory');a=p.parse_args()
    try:
        if a.directory:r=run(a.directory)
        else:
            with TemporaryDirectory(prefix='megamind-state-') as d:r=run(d)
        print(encoded(r).decode());return 0
    except ContractError as e:
        print(encoded({'status':e.code,'detail':str(e)}).decode(),file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
