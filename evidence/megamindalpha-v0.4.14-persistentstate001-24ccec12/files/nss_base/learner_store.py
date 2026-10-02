"""Small coordinator journal: plans, training attestations, phase refs, proposals.

No dataset/checkpoint/task/current-generation replica. Existing owners retain bytes.
Only one cooperative worker dispatches numerical work; journal writes are atomic.
"""
from copy import deepcopy
from .learner_contracts import (FORMAT, PHASES, learning_plan, manifest, numerical_input,
    operation_id, run_receipt, snapshot_ref)
from .local_journal import EventJournal, epoch, fault
from .neural_contracts import encoded, fields, fingerprint
from .qualification_contracts import identifier, text
from .runtime import fail


def proposal_for(p, receipts, verdict):
    return {'schema_version':1, 'format':FORMAT, 'cycle_id':p['cycle_id'],
        'learning_plan_sha256':fingerprint(p), 'parent':p['parent'],
        'snapshot':receipts['SNAPSHOT'], 'training':receipts['TRAIN'], 'evaluation':receipts['EVALUATE'],
        'numerical_verdict':verdict,
        'recommendation':'INDEPENDENT_REVIEW_REQUIRED' if verdict=='PASS' else 'NOT_RECOMMENDED',
        'qualification_status':'INSUFFICIENT_EVIDENCE',
        'missing_claims':['PROFILE:A2','PROFILE:A2B','DIRECTED_TRANSITIONS_FOR_NEW_CANDIDATE'],
        'authority':'NONE','deployment_authorized':False,'runtime_execution_permit':False,
        'scope':'Fixed A2 overlay recipe; no self-qualification or successor-Core authority'}


def _reduce(m, events):
    cycles={}
    for event in events:
        b=event['body'];kind=event['kind'];at=event['at']
        if kind=='PLAN':
            p=learning_plan(b)
            if p['cycle_id'] in cycles or p['producer_id'] not in m['producer_ids'] or at<p['at']:
                fail('VALIDATION_FAILED','Invalid/duplicate learning plan or producer')
            cycles[p['cycle_id']]={'plan':p, 'approval':None, 'withdrawn':False,
                'started':[], 'receipts':{}, 'proposal':None, 'cancel':None}
            continue
        if type(b) is not dict: fail('VALIDATION_FAILED','Expected typed learner event')
        identifier(b.get('cycle_id'))
        if b['cycle_id'] not in cycles: fail('VALIDATION_FAILED','Event refers to unknown learning cycle')
        c=cycles[b['cycle_id']];p=c['plan']
        if kind=='APPROVE':
            fields(b,('cycle_id','plan_sha256','approver_id','expires_at'))
            epoch(b['expires_at'])
            if (c['approval'] is not None or c['cancel'] or c['proposal'] or b['plan_sha256']!=fingerprint(p)
                or b['approver_id'] not in m['approver_ids'] or b['approver_id']==p['producer_id']
                or not at<b['expires_at']<=at+86400):
                fail('AUTHORIZATION_DENIED','Invalid local plan approval')
            c['approval']=deepcopy(b)
        elif kind=='WITHDRAW':
            fields(b,('cycle_id','actor_id','reason'));text(b['reason'])
            if b['actor_id'] not in m['approver_ids'] or c['approval'] is None:
                fail('AUTHORIZATION_DENIED','Only a declared operator can withdraw an approval')
            if c['withdrawn']:fail('VALIDATION_FAILED','Duplicate withdrawal event')
            c['withdrawn']=True
        elif kind=='CANCEL':
            fields(b,('cycle_id','actor_id','reason'));text(b['reason'])
            if b['actor_id'] not in m['approver_ids']+[p['producer_id']]:
                fail('AUTHORIZATION_DENIED','Cancellation caller not permitted')
            if c['proposal'] or c['cancel']:fail('CONSTRAINT_CONFLICT','Cycle already terminal')
            c['cancel']=deepcopy(b)
        elif kind in ('START','DONE','PROPOSE'):
            if c['cancel'] or c['proposal']:fail('VALIDATION_FAILED','Terminal cycle cannot advance')
            if kind=='START':
                fields(b,('cycle_id','phase'));phase=b['phase']
                if type(phase) is not str:fail('VALIDATION_FAILED','Phase must be text')
                if (not c['approval'] or c['withdrawn'] or at>=c['approval']['expires_at']):
                    fail('AUTHORIZATION_DENIED','New dispatch requires unexpired local approval')
                if (phase not in PHASES or phase in c['started']
                    or list(c['receipts'])!=list(PHASES[:PHASES.index(phase)])):
                    fail('VALIDATION_FAILED','Phase dispatch order/identity invalid')
                if p['budget']['optimizer_updates']<p['recipe']['steps'] or p['budget']['evaluation_passes']<p['criteria']['repeats']:
                    fail('BUDGET_EXHAUSTED','Planned work exceeds its approved budget')
                c['started'].append(phase)
            elif kind=='DONE':
                fields(b,('cycle_id','phase','reference'));phase=b['phase']
                if type(phase) is not str:fail('VALIDATION_FAILED','Phase must be text')
                if phase not in c['started'] or phase in c['receipts']:
                    fail('VALIDATION_FAILED','Receipt has no exact pending phase')
                if phase=='SNAPSHOT':
                    s=snapshot_ref(b['reference'])
                    if s['snapshot_id']!=p['snapshot_request']['snapshot_id']:
                        fail('VALIDATION_FAILED','Snapshot receipt substitution')
                else:
                    r=run_receipt(b['reference'])
                    expected=numerical_input(p,c['receipts']['SNAPSHOT'],c['receipts'].get('TRAIN') if phase=='EVALUATE' else None)
                    if r['id']!=operation_id(p,phase) or r['plan_sha256']!=fingerprint(expected):
                        fail('VALIDATION_FAILED','Wrong numerical-owner receipt')
                c['receipts'][phase]=deepcopy(b['reference'])
            else:
                fields(b,('cycle_id','proposal'))
                if (c['withdrawn'] or not c['approval'] or at>=c['approval']['expires_at']):
                    fail('AUTHORIZATION_DENIED','Proposal creation blocked by withdrawn/expired local approval')
                if list(c['receipts'])!=list(PHASES):fail('INSUFFICIENT_EVIDENCE','Missing owner receipts')
                expected=proposal_for(p,c['receipts'],c['receipts']['EVALUATE']['verdict'])
                if encoded(b['proposal'])!=encoded(expected):fail('VALIDATION_FAILED','Proposal differs from bound owner evidence')
                c['proposal']=deepcopy(expected)
        else: fail('VALIDATION_FAILED','Unknown learner event')
    return cycles


class LearningCycles(EventJournal):
    filename='learning_cycles.sqlite3'
    validate_manifest=staticmethod(manifest)

    @classmethod
    def create(cls,directory,operators):
        return cls.create_document(directory,operators)

    def inspect(self,cycle_id=None):
        with self.transaction() as db:
            m,cycles,meta,_=self.read(db,_reduce)
        if cycle_id is None:return {'operators':m,'cycles':sorted(cycles),'events':meta['count'],'authority':'NONE'}
        identifier(cycle_id)
        if cycle_id not in cycles:fail('INSUFFICIENT_EVIDENCE','Unknown learning cycle')
        c=deepcopy(cycles[cycle_id]);c['status']='PROPOSED' if c['proposal'] else 'CANCELLED' if c['cancel'] else 'PENDING'
        c['authority']='NONE';c['historical']=c['status']!='PENDING'
        return c

    def prepare(self,plan,*,at):
        p=learning_plan(plan)
        with self.transaction() as db:
            _,cycles,meta,_=self.read(db,_reduce)
            if p['cycle_id'] in cycles:
                if cycles[p['cycle_id']]['plan']!=p:fail('CONSTRAINT_CONFLICT','Cycle ID already binds another plan')
            else:self.append(db,_reduce,meta,'PLAN',at,p)
        return self.inspect(p['cycle_id'])

    def approve(self,cycle_id,*,approver_id,expires_at,at):
        c=self.inspect(cycle_id)
        b={'cycle_id':cycle_id,'plan_sha256':fingerprint(c['plan']),'approver_id':approver_id,'expires_at':expires_at}
        return self._event('APPROVE',b,at)

    def withdraw(self,cycle_id,*,actor_id,reason,at):
        return self._event('WITHDRAW',{'cycle_id':cycle_id,'actor_id':actor_id,'reason':reason},at)

    def cancel(self,cycle_id,*,actor_id,reason,at):
        return self._event('CANCEL',{'cycle_id':cycle_id,'actor_id':actor_id,'reason':reason},at)

    def _event(self,kind,body,at,crash_at=None):
        with self.transaction() as db:
            _,cycles,meta,events=self.read(db,_reduce)
            # Exact retry returns historical state, not renewed approval or dispatch.
            if not any(e['kind']==kind and e['body']==body for e in events):
                self.append(db,_reduce,meta,kind,at,body)
                fault(crash_at,'before_'+kind.lower()+'_commit')
        fault(crash_at,'after_'+kind.lower()+'_commit')
        return self.inspect(body['cycle_id'])

    def begin(self,cycle_id,phase,*,at):
        c=self.inspect(cycle_id)
        if phase in c['started']:return False
        self._event('START',{'cycle_id':cycle_id,'phase':phase},at)
        return True

    def complete(self,cycle_id,phase,reference,*,at):
        return self._event('DONE',{'cycle_id':cycle_id,'phase':phase,'reference':reference},at)

    def propose(self,cycle_id,*,at,crash_at=None):
        c=self.inspect(cycle_id)
        if list(c['receipts'])!=list(PHASES):fail('INSUFFICIENT_EVIDENCE','Incomplete numerical work')
        p=proposal_for(c['plan'],c['receipts'],c['receipts']['EVALUATE']['verdict'])
        return self._event('PROPOSE',{'cycle_id':cycle_id,'proposal':p},at,crash_at)

    def gate(self,cycle_id,caller_id,*,at):
        identifier(cycle_id);identifier(caller_id);at=epoch(at)
        with self.transaction() as db:
            _,cycles,meta,_=self.read(db,_reduce)
            if cycle_id not in cycles:fail('INSUFFICIENT_EVIDENCE','Unknown learning cycle')
            c=cycles[cycle_id];p=c['plan']
            if caller_id!=p['producer_id'] or not c['approval'] or c['withdrawn'] or c['cancel']:
                fail('AUTHORIZATION_DENIED','Cycle is not approved for this caller')
            if at<meta['last_at'] or at>=c['approval']['expires_at']:
                fail('AUTHORIZATION_DENIED','Local training approval expired or clock moved backward')
            if p['budget']['optimizer_updates']<p['recipe']['steps'] or p['budget']['evaluation_passes']<p['criteria']['repeats']:
                fail('BUDGET_EXHAUSTED','No dispatch: insufficient optimizer/evaluation budget')
        return True
