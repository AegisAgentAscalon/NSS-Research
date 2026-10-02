"""Installed CandidateRuns/CandidateEvaluations evidence adapter, read-only.

Evidence does not become a release grant. The Qualifications owner validates the
separate parent certificate through upstream(); no cross-store private SQL here.
Only the fixed A2 recipe and its developer-visible tests are supported.
"""
from copy import deepcopy
from .candidate_records import (CandidateRuns, CandidateEvaluations, training_report,
    evaluation_report)
from .dataset_contracts import references
from .dataset_store import DatasetSnapshots
from .experience_store import ExperienceArchive
from .learner_contracts import learning_plan, numerical_input, operation_id
from .learner_store import LearningCycles
from .neural_contracts import CODEC, encoded, fields, fingerprint, pairs, validate_pairs
from .qualification_contracts import (CANDIDATE_FORMAT, POLICY, POLICY_HASH, binding,
    request, verification)
from .qualification_neural import NeuralEvidence, LIMITS
from .runtime import fail
from .serialization import decode


def _success(result):
    if result['status'] != 'SUCCESS': fail(result['status'], result['detail'])
    return result['data']


class CandidateEvidence(NeuralEvidence):
    """Reuse request/guard mechanics, not the legacy probe's evidence interpretation."""
    def __init__(self, cycles, *, training, evaluations, archive, snapshots,
                 tokenizer_path, parent_source):
        owners=((cycles,LearningCycles),(training,CandidateRuns),(evaluations,CandidateEvaluations),
            (archive,ExperienceArchive),(snapshots,DatasetSnapshots),(parent_source,NeuralEvidence))
        if any(type(v) is not cls for v,cls in owners):
            fail('VALIDATION_FAILED', 'Only installed public candidate/source owners are supported')
        self.cycles=cycles;self.training=training;self.evaluations=evaluations
        self.archive=archive;self.snapshots=snapshots;self.tokenizer_path=tokenizer_path
        self.parent_source=parent_source

    def view(self, run_id, seed, precision, *, current=True):
        from .neural_execution import CandidateSession
        from .neural_backend import environment
        from .neuralprobe001 import implementation
        import torch
        c=self.cycles.inspect(run_id)
        if c['status']!='PROPOSED': fail('INSUFFICIENT_EVIDENCE', 'No sealed learning proposal')
        if current and c['withdrawn']: fail('AUTHORIZATION_DENIED', 'Candidate proposal was withdrawn')
        p=learning_plan(c['plan']);s=c['receipts']['SNAPSHOT'];parent=p['parent']
        if (type(seed) is not int or seed!=p['recipe']['seed'] or precision!=parent['precision']):
            fail('INCOMPATIBLE_CONFIGURATION', 'Exact candidate seed/precision required')
        if current and (p['code_sha256']!=implementation()['sha256'] or
                p['environment_sha256']!=fingerprint(environment())):
            fail('INCOMPATIBLE_CONFIGURATION', 'Candidate code/numerical environment changed')
        # Parent evidence is checked through its own adapter, not relabeled as new evidence.
        pv=self.parent_source.view(parent['run_id'],parent['trial_seed'],parent['precision'],current=current)
        if pv[4]!=parent or pv[0]['report']['verdict']!='PASS':
            fail('INCOMPATIBLE_CONFIGURATION', 'Candidate parent evidence differs')
        if current:
            batch=_success(self.archive.read_batch_for_use(references(p['snapshot_request']),purpose='training'))
            if batch['archive_binding']['sha256']!=p['archive_sha256']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Candidate archive substituted')
            for split in ('train','validation'):
                view=_success(self.snapshots.read_for_use(s['snapshot_id'],expected_manifest_hash=s['sha256'],
                    purpose='training',split=split,archive=self.archive,tokenizer_path=self.tokenizer_path))
                if len(view['examples'])!=1:fail('VALIDATION_FAILED','Candidate recipe expects one record per split')
                value=decode(view['examples'][0]['text']);fields(value,('codec','pairs'))
                if value['codec']!=CODEC['id']:fail('INCOMPATIBLE_CONFIGURATION','Wrong candidate codec')
                validate_pairs(value['pairs'],split)
        tr=self.training.inspect(operation_id(p,'TRAIN'));ev=self.evaluations.inspect(operation_id(p,'EVALUATE'))
        if (tr['status']!='FINALIZED' or ev['status']!='FINALIZED' or
                tr['receipt']!=c['receipts']['TRAIN'] or ev['receipt']!=c['receipts']['EVALUATE'] or
                tr['plan']!=numerical_input(p,s) or ev['plan']!=numerical_input(p,s,tr['receipt'])):
            fail('VALIDATION_FAILED', 'Candidate owner plans/receipts differ from the sealed proposal')
        t=training_report(tr['plan'],tr['report']);r=evaluation_report(ev['plan'],ev['report'])
        if t['checkpoint_hashes']!=r['checkpoint_hashes']:
            fail('VALIDATION_FAILED','Candidate evaluation did not bind the trained artifacts')
        if any(t['artifacts'][k]!=pv[1]['artifacts'][k] for k in ('core','A','B')):
            fail('INCOMPATIBLE_CONFIGURATION','Candidate changed a parent artifact')
        # Same execution ABI; candidate names and artifact hashes produce distinct profile ECIDs.
        identity=parent['runtime_sha256'];session=CandidateSession(t['artifacts'],identity)
        lineage={'cycle_sha256':fingerprint(p),'proposal_sha256':fingerprint(c['proposal']),
            'producer_id':p['producer_id'],'training_receipt':tr['receipt'],'evaluation_receipt':ev['receipt'],
            'snapshot':s,'parent_binding_sha256':fingerprint(parent),
            'parent_core_certificate':p['parent_core_certificate'],'criteria_sha256':fingerprint(p['criteria']),
            'retention_pairs_sha256':fingerprint([v for v in pairs('test') if all(i not in (5,6) for i in v)])}
        b=binding({**{k:deepcopy(parent[k]) for k in ('core_generation','tokenizer','context_abi','overlay_abi',
                'runtime_sha256','code_sha256','environment_sha256','test_pairs_sha256','transition_pairs_sha256')},
            'run_id':run_id,'trial_seed':seed,'precision':precision,'plan_sha256':fingerprint(ev['plan']),
            'report_sha256':fingerprint(r),'checkpoint_hashes':t['checkpoint_hashes'],
            'profile_ecids':{key:session.catalog.ecid(key) for key in ('CORE','A2','A2B')},
            'data_binding_sha256':fingerprint({'archive':p['archive_sha256'],'snapshot':s,'selection':p['snapshot_request']}),
            'protocol_sha256':fingerprint({'criteria':p['criteria'],'recipe':p['recipe'],'policy':POLICY_HASH}),
            'checker':'candidate_A2_profile_and_recovery_v1','source_format':CANDIDATE_FORMAT,'candidate_lineage':lineage})
        checker={'name':'qualification_candidate_v1','code_sha256':p['code_sha256'],
            'numerical_backend_sha256':fingerprint({'torch':str(torch.__version__),'build':torch.__config__.show(),
                                                  'cpu_capability':torch.backends.cpu.get_cpu_capability()})}
        return ev, t, c, session, b, checker

    def upstream(self, req):
        """Separate parent approval dependency checked by the qualification owner."""
        p=self.cycles.inspect(request(req)['binding']['run_id'])['plan']
        return {**p['parent_core_certificate'],'binding':p['parent'],
                'claim':{'kind':'PROFILE','profile':'CORE'},'source':self.parent_source}

    def verify(self, req):
        from .learner_recipe import verify_candidate
        from .neural_execution import CandidateSession
        from .neural_checks import replay_observations
        req=request(req);ev,t,c,_,b,checker=self.guard(req);p=c['plan'];scope=req['claim']
        tr=self.training.inspect(operation_id(p,'TRAIN'))
        out={'schema_version':1,'request_sha256':fingerprint(req),'binding_sha256':fingerprint(b),
            'claim':scope,'policy_sha256':POLICY_HASH,'verdict':'INCONCLUSIVE','checks':[],'repeats':[],
            'checker_identity':checker,'limits':list(LIMITS)+[
                'Exact CandidateRuns/CandidateEvaluations lineage; A2 is never relabeled as A.',
                'Retention excludes intentionally changed symbols 5 and 6; no universal preservation claim.'],
            'deployment_authorized':False}
        # Uses freshly loaded checkpoint scoring and exact comparisons against both sealed repeats.
        verify_candidate(ev,tr,gate=lambda:self.guard(req))
        if ev['report']['verdict']!='PASS':
            out['verdict']='FAIL';out['checks']=[{'id':'candidate_pass','passed':False,
                'observed':ev['report']['verdict'],'requirement':'Frozen candidate acceptance criteria must pass'}]
            return verification(out)
        m=ev['report']['repeats'][0]
        for _ in range(POLICY['verification_repeats']):
            self.guard(req)
            row={'core_accuracy':m['core']['pair_accuracy'],'retained_accuracy':m['retained_AB']['pair_accuracy'],
                 'updated_gain':m['A2B']['pair_accuracy']-m['parent_on_updated']['pair_accuracy']}
            if scope['kind']=='PROFILE':
                row['profile_accuracy']=m['core' if scope['profile']=='CORE' else scope['profile']]['pair_accuracy']
            else:
                row.update(replay_observations(CandidateSession,t['artifacts'],b,scope,atol=1e-6,rtol=1e-6))
            out['repeats'].append(row)
        o=out['repeats'][0];checks=out['checks']
        def check(key, ok, observed, required):
            checks.append({'id':key,'passed':bool(ok),'observed':observed,'requirement':required})
        check('core_only',o['core_accuracy']>=POLICY['minimum_accuracy'],o['core_accuracy'],'Core baseline >= 0.95')
        check('retention',o['retained_accuracy']>=p['criteria']['minimum_retained_accuracy'],o['retained_accuracy'],
              'Declared unchanged-symbol pairs meet frozen retention threshold')
        check('updated_gain',o['updated_gain']>=p['criteria']['minimum_gain'],o['updated_gain'],
              'Updated task improves over the accepted parent under frozen criteria')
        if scope['kind']=='PROFILE':
            check('profile_accuracy',o['profile_accuracy']>=p['criteria']['minimum_accuracy'],o['profile_accuracy'],
                  'Exact named profile meets frozen candidate accuracy threshold')
        else:
            for k in ('stale_rejected','source_unchanged','exact_match','tolerance_match','draft_cleared','denial_preserved','reverse_rejected'):
                check(k,o[k] is True,o[k],'True on the four qualified directed-transition inputs')
            check('one_checker_effect',o['checker_mock_effect_count']==1,o['checker_mock_effect_count'],
                  'One isolated checker effect; no live action is executed')
        check('repeatability',out['repeats'][0]==out['repeats'][1],out['repeats'][0]==out['repeats'][1],
              'Exact repeated checkpoint/recovery observations')
        out['verdict']='PASS' if all(r['passed'] for r in checks) else 'FAIL'
        self.guard(req);return verification(out)


def from_config(config):
    """Open existing owners only; no implicit journal creation or approval."""
    from .learner_contracts import owner_paths
    p=owner_paths(config)
    return CandidateEvidence(LearningCycles(p['cycles']),training=CandidateRuns(p['candidates']),
        evaluations=CandidateEvaluations(p['evaluations']),archive=ExperienceArchive(p['archive']),
        snapshots=DatasetSnapshots(p['snapshots']),tokenizer_path=p['tokenizer'],
        parent_source=NeuralEvidence(p['parent_journal'],p['parent_data']))
