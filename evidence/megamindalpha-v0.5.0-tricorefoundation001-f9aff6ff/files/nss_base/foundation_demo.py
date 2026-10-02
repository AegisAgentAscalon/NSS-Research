"""Executable overlay-independent lifecycle demo with deterministic test adapters."""
from copy import deepcopy
from pathlib import Path
import argparse
import json
from .generation_store import Generations
from .foundation_adapters import test_configuration
from .foundation_context import FoundationContextSource
from .foundation_runner import CycleRunner
from .foundation_store import prepare_admission, prepare_state, current_time
from .state_contracts import attest
from .context_service import ContextService
from .context_contracts import make_request
from .context_plan import unwrap
from .neural_contracts import fingerprint, encoded
from .runtime import ContractError, fail

OPERATORS = [{'id':'builder','roles':['PRODUCER','OPERATOR']},
             {'id':'reviewer','roles':['REVIEWER']}, {'id':'issuer','roles':['ISSUER']}]
SCOPE = {'agent_id':'test-companion','project_id':'nss-foundation','session_id':'test-session'}


def approved(proposal):
    now=current_time()
    return attest(proposal,reviewer_id='reviewer',reviewed_at=now,expires_at=now+1800,
                  reason='Explicit local structural test attestation; not actual user/model qualification')


def fixture_record(root, task_id='task-001'):
    from .qualification_contracts import identifier
    identifier(task_id)
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    source={'schema_version':1,'fields':[
        {'id':'request','value':'Retain the exact test value and label all imagined events.','unit':None},
        {'id':'value','value':'京都 / Kyoto','unit':None}]}
    name=task_id+'.json';(root/name).write_bytes(encoded(source))
    return {'schema_version':1,'task_id':task_id,'revision':0,'parent_hash':None,
        'goal':'Exercise the current-role contracts, not neural competence.',
        'original_request':{'text':source['fields'][0]['value'],'source_id':'fixture'},
        'sources':[{'id':'fixture','kind':'synthetic','artifact':{'path':name,'sha256':fingerprint(source)}}],
        'facts':[{'id':'exact-value','value':'京都 / Kyoto','unit':None,'source_id':'fixture','source_field':'value'}],
        'assumptions':[],'unresolved_questions':[],'clarifications':[],'checked_results':[],
        'constraints':[],'receipts':[],
        'stage':{'id':'foundation-task','mode':'WORK','sealed':False,'objective':'Test scoped state.',
                 'required_facts':[{'fact_id':'exact-value','fields':['value']}],'requested_output':'Exact test value.'}}


def setup(root, *, primary_only=False, wrong_validator=True):
    root=Path(root)
    if root.exists() and any(root.iterdir()): raise ValueError('Refusing to overwrite a nonempty demo directory')
    root.mkdir(parents=True,exist_ok=True)
    cfg,adapters=test_configuration(primary_only=primary_only,wrong_validator=wrong_validator)
    store=Generations.create_foundation(root/'generations',OPERATORS,cfg)
    record=fixture_record(root/'evidence')
    proposal=prepare_admission(store.foundation_snapshot(),record,caller_id='builder',owner_scope=SCOPE,
        operation_id='admit-001',proposer_id='fixture-author',proposer_version='v1')
    view=store.foundation_admit(record,approved(proposal),evidence_root=root/'evidence')
    service=ContextService(FoundationContextSource(store,evidence_root=root/'evidence'))
    runner=CycleRunner(store,service,adapters)
    return store,service,runner,adapters,view


def live_view(store,root,task_id='task-001'):
    return store.foundation_read(task_id,caller_id='builder',owner_scope=SCOPE,evidence_root=Path(root)/'evidence')


def context_for(store,service,root,task_id='task-001'):
    return unwrap(service.build(make_request(live_view(store,root,task_id),'builder')))


def run_demo(root):
    store,service,runner,adapters,view=setup(root)
    root=Path(root);before_cfg=store.foundation_snapshot()['configuration']
    c=prepare_state(view,operation_id='note-001',proposer_id='test-tertiary',proposer_version='test-r1',deltas=[{
        'op':'ADD_NOTE','source_refs':[{'kind':'TASK','source_id':'fixture','field_id':'request'}],
        'note':{'id':'pending-reflection','text':'A test hypothesis is not an observed event.',
                'kind':'CLAIM','status':'HYPOTHESIS','confidence':None,'mandatory':True,
                'identity_sensitive':False,'expires_at':None}}])
    denied=None
    try: store.foundation_update(c,evidence_root=root/'evidence')
    except ContractError as e: denied=e.code
    if not (denied=='NEEDS_CLARIFICATION'): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    store.foundation_update(approved(c),evidence_root=root/'evidence')
    phases=['PRIMARY_ONLY','TASK','LEARN','REFLECT','VERIFY'];results=[];stale=None
    for i,phase in enumerate(phases,1):
        p=context_for(store,service,root)
        result=runner.run_tick(p,operation_id='tick-'+str(i),phase=phase,experience_cutoff=i)
        results.append(result)
        if i==1:
            stale=service.consume(p,caller_id='builder',expected_packet_sha256=fingerprint(p))['status']
            retry=runner.run_tick(p,operation_id='tick-1',phase=phase,experience_cutoff=1)
            if not (retry['status']=='ALREADY_COMMITTED' and retry['model_calls']==0): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    before=live_view(store,root)
    resumed=Generations(root/'generations')
    after=live_view(resumed,root)
    if not (before==after): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (before_cfg==resumed.foundation_snapshot()['configuration']): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (results[-1]['messages'][-1]['payload']['relation']=='contradicted'): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (results[-1]['output']['payload']['exact_value']=='京都 / Kyoto'): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (results[-2]['messages'][-1]['record_kind']=='hypothetical'): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (not before['record']['facts'][0]['value'].startswith('An untested')): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (before['candidate_states']['SECONDARY']['payload']['calls']==1): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (before['states']['SECONDARY']['payload']['calls']==1): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    if not (stale=='INCOMPATIBLE_CONFIGURATION'): fail('VALIDATION_FAILED', 'Foundation demo invariant failed')
    report={'status':'PASS','release':'TriCoreFoundation001','scope':'DETERMINISTIC_TEST_ADAPTERS_NOT_NEURAL_MODELS',
        'configuration_sha256':fingerprint(before_cfg),'phases':phases,
        'calls_by_role':{r:a.calls for r,a in adapters.items()},'committed_ticks':before['ticks'],
        'symbolic_revisions':len(before['history']),'restart_exact':before==after,
        'unreviewed_state_result':denied,'stale_context_result':stale,
        'wrong_validator_did_not_veto_exact_result':True,'tertiary_remained_hypothetical':True,
        'candidate_state_separate_from_serving_state':True,'serving_parameters_unchanged':True,
        'new_parameter_updates':0,'external_effects':0,'forge_connected':False,'runtime_connected':False,
        'NBR01_status':'NOT_RUN','production_qualified':False,
        'receipts':[{'phase':r['phase'],'calls':r['receipts']} for r in results]}
    (root/'DEMO_RESULT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path,help='New or empty local directory; never overwritten')
    args=parser.parse_args()
    try: print(json.dumps(run_demo(args.output),indent=2,ensure_ascii=False))
    except (ContractError,ValueError,OSError) as e:
        print(json.dumps({'status':getattr(e,'code','ERROR'),'detail':str(e)}));return 1
    return 0


if __name__=='__main__': raise SystemExit(main())
