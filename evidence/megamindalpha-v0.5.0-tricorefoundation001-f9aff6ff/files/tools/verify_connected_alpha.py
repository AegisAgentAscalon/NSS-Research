#!/usr/bin/env python3
"""Check recorded connected-demo acceptance, NOT independent neural qualification.

Historical reports may be inspected after withdrawal. This does not execute them or
renew data permission. The demo itself checks before/after current owner states.
"""
import argparse
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.candidate_records import training_report, evaluation_report
from nss_base.learner_contracts import learning_plan
from nss_base.learner_store import proposal_for
from nss_base.neural_contracts import fingerprint, read_document


def verify_proposal(path):
    path=Path(path);s=read_document(path);root=path.parent;issues=[]
    exact={'status':'SUCCESS','scope':'CONNECTED_HUMAN_ASSISTED_DEMO_THROUGH_REVIEW_ONLY_PROPOSAL',
        'profile_sequence':['AB','A','CORE'],'unapproved_dispatch':'AUTHORIZATION_DENIED',
        'numerical_verdict':'PASS','proposal_current_use_status':'INSUFFICIENT_EVIDENCE',
        'missing_qualification':['PROFILE:A2','PROFILE:A2B','DIRECTED_TRANSITIONS_FOR_NEW_CANDIDATE'],
        'proposal_after_revocation':'TRAINING_RESTRICTED','mock_external_effect_count':1,
        'candidate_deployed':False,'runtime_execution_permit':False}
    for k,v in exact.items():
        if type(s.get(k)) is not type(v) or s[k]!=v:issues.append('Unexpected summary field: '+k)
    for k in ('exact_repeats','historical_retry_unchanged','no_retraining_on_retry',
              'production_generation_unchanged','task_unchanged_by_learning','original_neural_report_unchanged'):
        if s.get(k) is not True:issues.append('Missing demonstrated invariant: '+k)
    p=learning_plan(read_document(root/'learning-plan.json'))
    t=read_document(root/'candidate-report.json');e=read_document(root/'evaluation-report.json')
    proposal=read_document(root/'release-proposal.json')
    tr=training_report(t['plan'],t['report']);ev=evaluation_report(e['plan'],e['report'])
    if t['status']!='FINALIZED' or e['status']!='FINALIZED':issues.append('Incomplete numerical owner')
    for record in (t,e):
        receipt=record['receipt']
        if receipt['plan_sha256']!=fingerprint(record['plan']) or receipt['report_sha256']!=fingerprint(record['report']):
            issues.append('Numerical receipt does not match historical bytes')
    if t['plan']['learning_plan']!=p or e['plan']['learning_plan']!=p or e['plan']['training_receipt']!=t['receipt']:
        issues.append('Candidate/evaluation plan lineage mismatch')
    expected=proposal_for(p,{'SNAPSHOT':t['plan']['snapshot'],'TRAIN':t['receipt'],'EVALUATE':e['receipt']},ev['verdict'])
    if proposal!=expected:issues.append('Proposal differs from recorded owners')
    if (s['plan_sha256']!=fingerprint(p) or s['candidate_sha256']!=tr['checkpoint_hashes']['A2']
            or s['parent_core_sha256']!=tr['checkpoint_hashes']['core']
            or s['snapshot_sha256']!=t['plan']['snapshot']['sha256']
            or s['optimizer_updates']!=tr['training']['updates'] or s['metrics']!=ev['repeats'][0]
            or s['core_and_parent_overlays_unchanged']!=tr['invariants']
            or ev['repeats'][0]!=ev['repeats'][1]):
        issues.append('Summary substituted a numerical or lineage result')
    return issues


def verify_candidate_history(path):
    """Inspect owner-backed history after revocation; no permission or numerical work."""
    from nss_base.generation_contracts import generation
    from nss_base.generation_store import Generations
    from nss_base.learner_cli import open_learner
    from nss_base.learner_contracts import operation_id
    from nss_base.qualification_contracts import request, CANDIDATE_FORMAT
    path=Path(path);root=path.parent;s=read_document(path);issues=[]
    exact={'status':'SUCCESS','scope':'CONNECTED_HUMAN_ASSISTED_LOCAL_CANDIDATE_ADOPTION_AND_ROLLBACK',
        'candidate_source_format':CANDIDATE_FORMAT,'managed_profile_sequence':['A2B','A2','CORE'],
        'numerical_verdict':'PASS','busy_publication':'RECOVERY_REQUIRED','old_ticket_rejected':'INCOMPATIBLE_CONFIGURATION',
        'prerequisite_withdrawal':'AUTHORIZATION_DENIED','dataset_withdrawal':'TRAINING_RESTRICTED',
        'mock_external_effect_count':1,'runtime_execution_permit':False,'production_deployment_authorized':False,
        'autonomous_review':False,'candidate_locally_adopted_then_rolled_back':True}
    for k,v in exact.items():
        if type(s.get(k)) is not type(v) or s[k]!=v:issues.append('Unexpected acceptance field: '+k)
    for k in ('parent_core_unchanged','no_adoption_from_evaluation_or_qualification','source_current_until_publish',
        'staged_artifacts_match_numerical_execution','stale_neural_state_rejected','recovered_matches_clean',
        'source_state_unchanged','parent_archived_on_adoption','rollback_exact_parent',
        'historical_adoption_does_not_republish','learning_proposal_unchanged','one_training_attempt'):
        if s.get(k) is not True:issues.append('Missing invariant: '+k)
    config=read_document(root/'learner_owners.json');co=open_learner(config)
    c=co.cycles.inspect(s['learning_cycle_id']);p=learning_plan(c['plan'])
    tr=co.training.inspect(operation_id(p,'TRAIN'));ev=co.evaluations.inspect(operation_id(p,'EVALUATE'))
    training_report(tr['plan'],tr['report']);evaluation_report(ev['plan'],ev['report'])
    if c['receipts']['TRAIN']!=tr['receipt'] or c['receipts']['EVALUATE']!=ev['receipt']:
        issues.append('Proposal lost exact numerical-owner lineage')
    g=generation(read_document(root/'candidate-family.json'));b=g['binding'];lineage=b['candidate_lineage']
    if (b['source_format']!=CANDIDATE_FORMAT or b['checkpoint_hashes']!=tr['report']['checkpoint_hashes'] or
        b['checkpoint_hashes']['A2']!=s['candidate_sha256'] or b['report_sha256']!=fingerprint(ev['report']) or
        lineage['cycle_sha256']!=fingerprint(p) or lineage['proposal_sha256']!=fingerprint(c['proposal']) or
        lineage['training_receipt']!=tr['receipt'] or lineage['evaluation_receipt']!=ev['receipt']):
        issues.append('Candidate family/report binding mismatch')
    reqs=[request(r) for r in read_document(root/'candidate-requests.json')]
    if len(reqs)!=5 or [r['claim'] for r in reqs]!=s['exact_qualified_claims']:
        issues.append('Incomplete exact profile/transition claims')
    for r in reqs:
        q=co.qualifications.inspect(r['request_id'])
        if q['request']!=r or r['binding']!=b or q['status']!='QUALIFIED' or q['certificate'] is None:
            issues.append('Missing exact historically accepted claim: '+r['request_id'])
    manager=Generations(root/'generations');adopt=manager.inspect_release('candidate-adoption')
    back=manager.inspect_release('candidate-rollback')
    if (adopt['status']!='PUBLISHED' or back['status']!='PUBLISHED' or
        adopt['receipt']!=s['adoption_receipt'] or back['receipt']!=s['rollback_receipt'] or
        adopt['receipt']['current']['generation_sha256']!=fingerprint(g) or
        back['receipt']['previous']!=adopt['receipt']['current'] or
        back['receipt']['current']['generation_sha256']!=adopt['receipt']['previous']['generation_sha256'] or
        manager.inspect()['current']!=back['receipt']['current']):issues.append('Publication/rollback history mismatch')
    task=manager.inspect_task('candidate-task')
    if not task['closed'] or task['ticket']['profile']!='CORE':issues.append('Candidate task was not finished in Core-only state')
    co.qualifications.audit();manager.audit();co.training.audit();co.evaluations.audit()
    from nss_base.ledger import Ledger
    if Ledger(root/'probe/mock_actions').effect_count()!=1:issues.append('Mock effect count changed')
    return issues


def verify(path):
    s=read_document(path)
    if s.get('scope')=='CONNECTED_HUMAN_ASSISTED_LOCAL_CANDIDATE_ADOPTION_AND_ROLLBACK':
        return verify_candidate_history(path)
    return verify_proposal(path)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--summary',required=True);a=p.parse_args()
    try:issues=verify(a.summary)
    except Exception as e:
        print(type(e).__name__+': '+str(e));return 1
    print('\n'.join(issues) if issues else 'PASS: recorded connected-demo history matches exact owner artifacts and declared scope. This inspection gives no new permission or Runtime execution authority.')
    return bool(issues)

if __name__=='__main__':raise SystemExit(main())
