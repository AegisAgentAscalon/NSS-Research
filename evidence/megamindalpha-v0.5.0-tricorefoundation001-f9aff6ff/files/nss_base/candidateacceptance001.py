"""Connected candidate acceptance demonstration, using scripted local reviewers.

Exercises actual A2 training -> separate qualification -> fresh release grant ->
atomic local adoption -> managed A2B/A2/CORE stages -> separately approved rollback.
No learned judge, production identity, native serving or Runtime permit is claimed.
"""
import argparse
from copy import deepcopy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from .boundedlearnercoordinator001 import prepare_learning_fixture
from .catalog_contracts import require_state_identity
from .catalog_controller import CatalogController, fixture_descriptor
from .context_contracts import make_request
from .context_service import ContextService
from .generation_evidence import from_evidence
from .neural_contracts import encoded, fingerprint, pairs
from .qualification_candidate import CandidateEvidence
from .qualificationevidence002 import AT, review_for
from .runtime import ContractError, fail


def candidate_source(co):
    """Application wiring only: the learner does not own qualification/adoption."""
    return CandidateEvidence(co.cycles,training=co.training,evaluations=co.evaluations,
        archive=co.archive,snapshots=co.snapshots,tokenizer_path=co.tokenizer_path,parent_source=co.source)


def proposed_claims(source, plan):
    scopes=[('candidate-core',{'kind':'PROFILE','profile':'CORE'},[]),
        ('candidate-a2',{'kind':'PROFILE','profile':'A2'},['candidate-core']),
        ('candidate-a2b',{'kind':'PROFILE','profile':'A2B'},['candidate-core']),
        ('candidate-to-a2',{'kind':'TRANSITION','source':'A2B','destination':'A2','mode':'replay'},
            ['candidate-core','candidate-a2','candidate-a2b']),
        ('candidate-to-core',{'kind':'TRANSITION','source':'A2','destination':'CORE','mode':'replay'},
            ['candidate-core','candidate-a2'])]
    return [source.propose(run_id=plan['cycle_id'],seed=plan['recipe']['seed'],precision=plan['parent']['precision'],
        scope=scope,producer_id='fixture-builder',request_id=key,at=AT,prerequisites=deps)
        for key,scope,deps in scopes]


def publish_request(manager, req, evidence):
    issued=manager.issue(req,issuer_id='release-owner',ttl_seconds=900,**evidence)
    opts={'caller_id':'local-runner','grant_sha256':fingerprint(issued['grant']),**evidence}
    for fn in (manager.prepare,manager.stage,manager.publish):result=fn(req['release_id'],**opts)
    return result,opts


def run(directory):
    f=prepare_learning_fixture(directory);root=f['root'];co=f['co'];manager=f['manager'];ledger=f['ledger']
    plan=f['plan'];source=candidate_source(co);evidence={'source':source,'qualifications':co.qualifications}
    proposal_before=co.cycles.inspect(plan['cycle_id']);parent_before=manager.inspect()['current']
    requests=proposed_claims(source,plan);reviews=[]
    for req in requests:
        co.qualifications.prepare(req,source=source)
        receipt=co.qualifications.decide(review_for(req),source=source);reviews.append(receipt)
        if receipt['verdict']!='QUALIFIED':fail('VALIDATION_FAILED','Candidate failed explicit claim qualification')
    family=from_evidence('candidate-family-1','fixture-builder',
        [r['request_id'] for r in requests[:3]],[r['request_id'] for r in requests[3:]],qualifications=co.qualifications)
    target=fingerprint(family);manager.propose(family,**evidence)
    manager.qualify(target,reviewer_id='generation-reviewer',**evidence)
    # No capability adoption before a distinct release approval.
    not_auto=manager.inspect()['current']==parent_before
    release=manager.make_request(target,release_id='candidate-adoption',caller_id='local-runner',
        mode='UPDATE',reason='Scripted separate local approval of exact new A2 family')
    issue=manager.issue(release,issuer_id='release-owner',ttl_seconds=900,**evidence)
    opts={'caller_id':'local-runner','grant_sha256':fingerprint(issue['grant']),**evidence}
    manager.prepare('candidate-adoption',**opts);manager.stage('candidate-adoption',**opts)
    source_until_publish=manager.inspect()['current']==parent_before
    # Existing stages really block the new family, then become stale after publication.
    oldticket=manager.pin_stage('parent-barrier',profile='CORE',caller_id='local-runner',
        qualifications=co.qualifications,source=co.source)
    try:manager.publish('candidate-adoption',**opts)
    except ContractError as e:barrier=e.code
    else:barrier='NOT_BLOCKED'
    manager.close_stage(oldticket,caller_id='local-runner')
    adoption=manager.publish('candidate-adoption',**opts)
    archived_at_adoption=manager.inspect()['generations'][parent_before['generation_sha256']]=='ARCHIVED'
    try:manager.read_stage(oldticket,caller_id='local-runner',**evidence)
    except ContractError as e:stale=e.code
    else:stale='NOT_BLOCKED'
    # Register capabilities with exact new names; routing remains a declared fixture.
    v=source.view(plan['cycle_id'],plan['recipe']['seed'],plan['parent']['precision'])
    decl={'CORE':{'capabilities':['control'],'load_units':0,'step_units':1,'max_pairs':4},
          'A2':{'capabilities':['updated_first'],'load_units':1,'step_units':1,'max_pairs':4},
          'A2B':{'capabilities':['updated_both'],'load_units':2,'step_units':2,'max_pairs':4}}
    descriptor=fixture_descriptor(family,v[1]['artifacts'],catalog_id='candidate-catalog-1',
        author_id='fixture-builder',declarations=decl)
    ctl=CatalogController(manager,**evidence,ledger=ledger,evidence_root=f['ctl'].inputs['evidence_root'])
    ch=ctl.register(descriptor,reviewer_id='generation-reviewer')['catalog_sha256']
    current=manager.inspect()['current'];task='candidate-task'
    record=deepcopy(f['before_task']['work']['record']);record.update(task_id=task,revision=0,parent_hash=None,receipts=[],checked_results=[])
    stage={'id':'candidate-both','mode':'WORK','sealed':False,'objective':'Apply updated synthetic symbol transformations',
           'required_facts':[],'requested_output':'Exact fixed-fixture result'}
    record['stage']=deepcopy(stage)
    req={'schema_version':1,'catalog_sha256':ch,'expected_current':current,'task_id':task,'stage':stage,
        'capabilities':['updated_both'],'pairs':pairs('test')[:4],
        'budget':{'max_document_bytes':1000000,'max_cost_units':1000}}
    ctl.apply({'schema_version':1,'operation_id':'candidate-start','caller_id':'local-runner','action':'START',
        'request':req,'ticket_id':'candidate-both','record':record})
    def read():
        x=ctl.inspect(task)
        return ctl.read(x['ticket'],caller_id='local-runner',expected_record_sha256=fingerprint(x['work']['record']))
    def act(kind,**extras):
        x=ctl.inspect(task)
        return ctl.apply({'schema_version':1,'operation_id':'candidate:'+kind+':'+x['ticket']['ticket_id'],
            'caller_id':'local-runner','action':kind,'source_ticket':x['ticket'],
            'expected_record_sha256':fingerprint(x['work']['record']),**extras})
    from .neural_execution import CandidateSession
    from .neural_backend import deterministic_cpu, load_checkpoint, encode_pairs
    import torch
    session=v[3];old=read()
    with deterministic_cpu(plan['recipe']['seed']):state=session.state('A2B',req['pairs'],task)
    source_cache=state['cache'].clone()
    def forward_stage(view):
        # Consume the manager's actually staged bytes, not a separately selected candidate.
        mods={k:load_checkpoint(a,fingerprint(a)) for k,a in view['artifacts'].items()}
        with torch.no_grad():return mods['core'](encode_pairs(view['pairs']),a=mods.get('A2'),b=mods.get('B'))
    with deterministic_cpu(plan['recipe']['seed']):
        staged_matches=torch.equal(forward_stage(old),session.predict('A2B',req['pairs']))
    context=ContextService(ctl,archive=co.archive)
    packet=context.build(make_request(old,'local-runner'))
    if packet['status']!='SUCCESS':fail(packet['status'],packet['detail'])
    # Fixed fixture evidence is a development claim only; checks do not broaden it.
    profiles=['A2B'];cache_rejected=False;clean_match=False
    for cap,name,mode in [('updated_first','candidate-a2','WORK'),('control','candidate-core','EVALUATION')]:
        act('FINISH',results=[],receipts=[]);r=deepcopy(req);r['capabilities']=[cap]
        r['stage'].update(id=name,mode=mode)
        act('MOVE',request=r,ticket_id=name);new=read();profiles.append(new['ticket']['profile'])
        try:require_state_identity(old['task_state_identity'],new)
        except ContractError as e:cache_rejected=e.code=='INCOMPATIBLE_CONFIGURATION'
        else:cache_rejected=False
        with deterministic_cpu(plan['recipe']['seed']):
            recovered=session.recover(state,new['ticket']['profile'],task,ledger,authorized=True)
            clean=CandidateSession(v[1]['artifacts'],v[4]['runtime_sha256']).predict(new['ticket']['profile'],req['pairs'])
            clean_match=recovered['status']=='SUCCESS' and torch.equal(recovered['state']['cache'],clean)
            staged_matches=staged_matches and torch.equal(forward_stage(new),clean)
        if not cache_rejected or not clean_match:fail('VALIDATION_FAILED','Candidate recovery mismatch')
        state=recovered['state'];old=new
    act('FINISH',results=[],receipts=[]);act('CLOSE')
    before_rollback=manager.inspect()['current']
    back=manager.make_request(parent_before['generation_sha256'],release_id='candidate-rollback',
        caller_id='local-runner',mode='ROLLBACK',reason='Fresh explicit rollback to preserved parent family')
    rollback,_=publish_request(manager,back,{'qualifications':co.qualifications,'source':co.source})
    current_after=manager.inspect()['current']
    history=manager.publish('candidate-adoption',**opts)
    no_republish=manager.inspect()['current']==current_after
    # Revocation has no retroactive deletion or implied re-execution. Check new use fails.
    c=co.qualifications.inspect('candidate-a2')['certificate']
    co.qualifications.revoke({'schema_version':1,'operation_id':'withdraw-candidate-a2',
        'request_id':'candidate-a2','certificate_sha256':fingerprint(c),'reviewer_id':'fixture-reviewer',
        'at':AT,'reason':'Scripted acceptance-prerequisite withdrawal'})
    def use(key):
        q=co.qualifications.inspect(key)
        return co.qualifications.check_use(key,certificate_sha256=fingerprint(q['certificate']),
            expected_claim=q['request']['claim'],expected_binding=q['request']['binding'],source=source)
    try:use('candidate-to-a2')
    except ContractError as e:revoked=e.code
    else:revoked='NOT_BLOCKED'
    f['data'].revoke_for_test()
    try:use('candidate-core')
    except ContractError as e:withdrawn=e.code
    else:withdrawn='NOT_BLOCKED'
    parent_ticket=manager.pin_stage('rollback-parent',profile='CORE',caller_id='local-runner',
        qualifications=co.qualifications,source=co.source)
    manager.read_stage(parent_ticket,caller_id='local-runner',qualifications=co.qualifications,source=co.source)
    manager.close_stage(parent_ticket,caller_id='local-runner')
    with deterministic_cpu(plan['recipe']['seed']):source_unchanged=torch.equal(source_cache,session.predict('A2B',req['pairs']))
    summary={'status':'SUCCESS','scope':'CONNECTED_HUMAN_ASSISTED_LOCAL_CANDIDATE_ADOPTION_AND_ROLLBACK',
        'learning_cycle_id':plan['cycle_id'],'candidate_sha256':v[4]['checkpoint_hashes']['A2'],
        'parent_core_unchanged':v[4]['checkpoint_hashes']['core']==plan['parent']['checkpoint_hashes']['core'],
        'numerical_verdict':v[0]['report']['verdict'],'candidate_source_format':v[4]['source_format'],
        'exact_qualified_claims':[r['claim'] for r in requests],
        'no_adoption_from_evaluation_or_qualification':not_auto,'source_current_until_publish':source_until_publish,
        'busy_publication':barrier,'old_ticket_rejected':stale,'managed_profile_sequence':profiles,
        'staged_artifacts_match_numerical_execution':staged_matches,'stale_neural_state_rejected':cache_rejected,
        'recovered_matches_clean':clean_match,'source_state_unchanged':source_unchanged,
        'parent_archived_on_adoption':archived_at_adoption,
        'adoption_receipt':adoption['receipt'],'rollback_receipt':rollback['receipt'],
        'rollback_exact_parent':current_after['generation_sha256']==parent_before['generation_sha256'],
        'historical_adoption_does_not_republish':history['historical'] and no_republish,
        'prerequisite_withdrawal':revoked,'dataset_withdrawal':withdrawn,
        'learning_proposal_unchanged':co.cycles.inspect(plan['cycle_id'])==proposal_before,
        'one_training_attempt':co.training.audit()['attempts']==1,
        'mock_external_effect_count':ledger.effect_count(),
        'candidate_locally_adopted_then_rolled_back':True,'runtime_execution_permit':False,
        'production_deployment_authorized':False,'autonomous_review':False}
    required=('parent_core_unchanged','no_adoption_from_evaluation_or_qualification','source_current_until_publish',
        'staged_artifacts_match_numerical_execution','stale_neural_state_rejected','recovered_matches_clean',
        'source_state_unchanged','parent_archived_on_adoption','rollback_exact_parent','historical_adoption_does_not_republish',
        'learning_proposal_unchanged','one_training_attempt')
    if (not all(summary[k] for k in required) or profiles!=['A2B','A2','CORE'] or barrier!='RECOVERY_REQUIRED'
        or stale!='INCOMPATIBLE_CONFIGURATION' or revoked!='AUTHORIZATION_DENIED' or withdrawn!='TRAINING_RESTRICTED'
        or ledger.effect_count()!=1):fail('VALIDATION_FAILED','Connected candidate-acceptance invariant failed')
    (root/'candidate-family.json').write_bytes(encoded(family));(root/'candidate-requests.json').write_bytes(encoded(requests))
    (root/'summary.json').write_bytes(encoded(summary));return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory');a=p.parse_args()
    try:
        if a.directory:r=run(a.directory)
        else:
            with TemporaryDirectory(prefix='candidate-acceptance-') as d:r=run(d)
        print(encoded(r).decode());return 0
    except ContractError as e:
        print(encoded({'status':e.code,'detail':str(e),'runtime_execution_permit':False}).decode(),file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
