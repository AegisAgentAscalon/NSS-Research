"""Bounded orchestration through public data/numerical owners; never a deployer."""
from copy import deepcopy
import time
from .dataset_contracts import references
from .learner_contracts import (PHASES, learning_plan, numerical_input, operation_id)
from .local_journal import epoch, fault
from .neural_contracts import CODEC, fields, fingerprint, validate_pairs
from .runtime import ContractError, fail
from .serialization import decode

FAULTS = ('after_plan_commit', 'after_snapshot_dispatch', 'after_snapshot_sealed',
    'after_train_dispatch', 'after_training_prepared', 'after_training_computed',
    'after_training_sealed', 'after_train_receipt', 'after_evaluate_dispatch',
    'after_evaluation_prepared', 'after_evaluation_computed', 'after_evaluation_sealed',
    'after_evaluate_receipt', 'before_propose_commit', 'after_propose_commit')


def unwrap(result):
    if result['status'] != 'SUCCESS': fail(result['status'], result['detail'])
    return result['data']


class LearnerCoordinator:
    """One cooperating local worker; collaborators supplied by installed application.

    clock is a trusted Python injection for deterministic tests, never JSON code.
    Neither context content nor local review attestations is a Runtime execution permit.
    """
    def __init__(self, cycles, *, archive, snapshots, tokenizer_path, source, qualifications,
                 training, evaluations, clock=None):
        from .candidate_records import CandidateRuns, CandidateEvaluations
        from .dataset_store import DatasetSnapshots
        from .experience_store import ExperienceArchive
        from .learner_store import LearningCycles
        from .qualification_neural import NeuralEvidence
        from .qualification_store import Qualifications
        expected=((cycles,LearningCycles),(archive,ExperienceArchive),(snapshots,DatasetSnapshots),
            (source,NeuralEvidence),(qualifications,Qualifications),(training,CandidateRuns),(evaluations,CandidateEvaluations))
        if any(type(value) is not cls for value,cls in expected):
            fail('VALIDATION_FAILED','Only installed public owner adapters are supported')
        if clock is not None and not callable(clock):fail('VALIDATION_FAILED','Clock injection must be trusted installed code')
        self.cycles=cycles; self.archive=archive; self.snapshots=snapshots
        self.tokenizer_path=tokenizer_path; self.source=source; self.qualifications=qualifications
        self.training=training; self.evaluations=evaluations
        self.clock=clock or time.time

    def now(self):
        value=self.clock()
        if type(value) not in (int,float) or not 0<=value<=253402300799:
            fail('VALIDATION_FAILED','Invalid observed clock')
        return epoch(int(value))

    def guard_sources(self, p):
        """Current checks, not cached authorization or administrative inspection."""
        p=learning_plan(p)
        try:
            from .neural_backend import environment
            from .neuralprobe001 import implementation
        except ImportError:
            fail('CAPABILITY_UNAVAILABLE','Candidate recipe requires optional installed CPU PyTorch')
        if p['code_sha256']!=implementation()['sha256'] or p['environment_sha256']!=fingerprint(environment()):
            fail('INCOMPATIBLE_CONFIGURATION','Code or numerical environment changed; create a new plan')
        ref=p['parent']; stored,row,_,_,actual,_=self.source.view(ref['run_id'],ref['trial_seed'],ref['precision'])
        if actual!=ref or stored['report']['verdict']!='PASS':
            fail('INCOMPATIBLE_CONFIGURATION','Exact successful parent evidence required')
        cert=p['parent_core_certificate']
        self.qualifications.check_use(cert['request_id'],certificate_sha256=cert['certificate_sha256'],
            expected_claim={'kind':'PROFILE','profile':'CORE'},expected_binding=ref,source=self.source)
        batch=unwrap(self.archive.read_batch_for_use(references(p['snapshot_request']),purpose='training'))
        if batch['archive_binding']['sha256']!=p['archive_sha256']:
            fail('INCOMPATIBLE_CONFIGURATION','Selected archive was substituted')
        return {k:deepcopy(row['artifacts'][k]) for k in ('core','A','B')}

    def dataset_pairs(self,p,snapshot):
        """Read exact approved text through the snapshot's consumption boundary."""
        out={}
        for split in ('train','validation'):
            view=unwrap(self.snapshots.read_for_use(snapshot['snapshot_id'],expected_manifest_hash=snapshot['sha256'],
                purpose='training',split=split,archive=self.archive,tokenizer_path=self.tokenizer_path))
            if len(view['examples'])!=1:fail('VALIDATION_FAILED','Recipe expects one curated pair record per split')
            obj=decode(view['examples'][0]['text']);fields(obj,('codec','pairs'))
            if obj['codec']!=CODEC['id']:fail('INCOMPATIBLE_CONFIGURATION','Wrong synthetic corpus codec')
            out[split]=validate_pairs(obj['pairs'],split)
        return out

    def prepare(self,plan,*,crash_at=None):
        self._fault_name(crash_at);p=learning_plan(plan)
        # An identical historical prepare is inspectable even after withdrawal.
        try:old=self.cycles.inspect(p['cycle_id'])
        except ContractError as e:
            if e.code!='INSUFFICIENT_EVIDENCE':raise
            old=None
        if old is None:self.guard_sources(p)
        out=self.cycles.prepare(p,at=self.now());fault(crash_at,'after_plan_commit');return out

    def _fault_name(self,name):
        if name is not None and (type(name) is not str or name not in FAULTS):
            fail('VALIDATION_FAILED','Unknown explicit learning fault hook')

    def _gate(self,p,caller,snapshot=None):
        self.cycles.gate(p['cycle_id'],caller,at=self.now());artifacts=self.guard_sources(p)
        if snapshot is not None:self.dataset_pairs(p,snapshot)
        return artifacts

    def advance(self,cycle_id,*,caller_id,crash_at=None):
        """Advance to a proposal or typed stop. A proposal is not a release grant."""
        self._fault_name(crash_at);c=self.cycles.inspect(cycle_id);p=c['plan']
        if caller_id!=p['producer_id']:fail('AUTHORIZATION_DENIED','Wrong learning producer')
        if c['status'] in ('PROPOSED','CANCELLED'):return c  # historical, no new dispatch
        self._gate(p,caller_id)
        if 'SNAPSHOT' not in c['receipts']:
            self.cycles.begin(cycle_id,'SNAPSHOT',at=self.now());fault(crash_at,'after_snapshot_dispatch')
            s=unwrap(self.snapshots.build(p['snapshot_request'],archive=self.archive,tokenizer_path=self.tokenizer_path))
            fault(crash_at,'after_snapshot_sealed')
            self.cycles.complete(cycle_id,'SNAPSHOT',s,at=self.now())
        c=self.cycles.inspect(cycle_id);s=c['receipts']['SNAPSHOT']
        from .learner_recipe import existing, train_candidate, evaluate_candidate, verify_candidate
        for phase,owner,executor in [('TRAIN',self.training,train_candidate),('EVALUATE',self.evaluations,evaluate_candidate)]:
            c=self.cycles.inspect(cycle_id)
            np=numerical_input(p,s,c['receipts'].get('TRAIN') if phase=='EVALUATE' else None)
            rid=operation_id(p,phase);old=existing(owner,rid,np)
            if phase in c['receipts']:
                if old is None or old['status']!='FINALIZED' or old['receipt']!=c['receipts'][phase]:
                    fail('VALIDATION_FAILED','Coordinator references missing/changed numerical evidence')
                continue
            artifacts=self._gate(p,caller_id,s)
            fresh=self.cycles.begin(cycle_id,phase,at=self.now());fault(crash_at,'after_'+phase.lower()+'_dispatch')
            if old is not None and old['status']=='FINALIZED':
                out=old  # adopt exact committed owner receipt; never train again
            elif not fresh:
                fail('RECOVERY_REQUIRED','Numerical dispatch is unresolved; cancel/abandon and explicitly approve a new attempt')
            else:
                gate=lambda:self._gate(p,caller_id,s)
                if phase=='TRAIN':
                    out=executor(owner,rid,np,artifacts=artifacts,train_pairs=self.dataset_pairs(p,s)['train'],gate=gate,crash_at=crash_at)
                else:
                    training=self.training.inspect(operation_id(p,'TRAIN'))
                    out=executor(owner,rid,np,training=training,gate=gate,crash_at=crash_at)
            fault(crash_at,'after_'+phase.lower()+'_receipt')
            self.cycles.complete(cycle_id,phase,out['receipt'],at=self.now())
        c=self.cycles.inspect(cycle_id)
        train=self.training.inspect(operation_id(p,'TRAIN'));ev=self.evaluations.inspect(operation_id(p,'EVALUATE'))
        verify_candidate(ev,train,gate=lambda:self._gate(p,caller_id,s))
        return self.cycles.propose(cycle_id,at=self.now(),crash_at=crash_at)

    def check_proposal(self,cycle_id):
        """Check current lineage/metrics; unsupported qualification remains explicit."""
        c=self.cycles.inspect(cycle_id)
        if c['status']!='PROPOSED':fail('INSUFFICIENT_EVIDENCE','No completed release proposal')
        if c['withdrawn']:fail('AUTHORIZATION_DENIED','Operator withdrew this proposal from current use')
        p=c['plan'];s=c['receipts']['SNAPSHOT']
        def current():self.guard_sources(p);self.dataset_pairs(p,s)
        current()
        train=self.training.inspect(operation_id(p,'TRAIN'));ev=self.evaluations.inspect(operation_id(p,'EVALUATE'))
        if train['receipt']!=c['receipts']['TRAIN'] or ev['receipt']!=c['receipts']['EVALUATE']:
            fail('VALIDATION_FAILED','Proposal owner references changed')
        from .learner_recipe import verify_candidate
        observed=verify_candidate(ev,train,gate=current)
        return {'status':'INSUFFICIENT_EVIDENCE','current_numerical_verification':observed,
            'proposal_sha256':fingerprint(c['proposal']), 'missing_claims':c['proposal']['missing_claims'],
            'authority':'NONE','deployment_authorized':False}
