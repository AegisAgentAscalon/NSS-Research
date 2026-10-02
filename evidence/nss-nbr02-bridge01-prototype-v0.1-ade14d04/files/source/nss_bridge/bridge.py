"""Bounded NSS orchestration bridge. Trusted events are distinct from model proposals.
Every task has eight required ordered steps (the retained neural task contract).
Publish at step 7 requires explicit approval at the current task revision.
All effects are SQLite-recorded SIMULATIONS, never shell commands or real uploads.
"""
from __future__ import annotations
import copy,json
from pathlib import Path
from .util import canonical,digest,strict_json,atomic_json
from .journal import Journal
from .recurrent import RecurrentAdvisor

STEP_NAMES=['collect_sources','draft_report','prepare_data','check_report','check_data','bundle','review_package','publish']
PUBLIC_RULES=(
 'Each task has exactly eight required steps numbered 0 through 7; all start pending. '
 'A trusted performed receipt marks its named step done until a trusted reopen event. '
 'Only the lowest numbered pending step may execute. Step 7 (publish) additionally requires '
 'explicit approval for the current task revision. A plan, a model assertion, or a proposed action '
 'is not a performed receipt. Current explicit records outrank model suggestions. '
 'All-done permits a finish proposal, not an additional tool execution. '
 'Return one JSON object with exactly owner, task_id, revision, request_id, action, step. '
 'action is perform (integer step 0..7), wait (null step), or finish (null step). '
 'No action is real: this prototype records simulated effects only.'
)

def key(owner,task):return owner+'::'+task

def valid_name(value):
    return isinstance(value,str) and 1<=len(value)<=96 and '::' not in value

class Bridge:
    def __init__(self,directory,owner,weights_path=None,mode='rule'):
        if not valid_name(owner) or mode not in ('rule','shadow','recurrent'):raise ValueError('CONFIG')
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.owner=owner;self.mode=mode;self.journal=Journal(self.directory/'events.sqlite')
        self.advisor=None if mode=='rule' else RecurrentAdvisor(weights_path)
        self.tasks={};self.seen=0;self.tip='0'*64;self.reviews=[];self.neural=[]
        self.sync()
    def close(self):self.journal.close()
    def _task(self,task_id):
        if task_id not in self.tasks:raise ValueError('UNKNOWN_TASK')
        t=self.tasks[task_id]
        if t['owner']!=self.owner:raise ValueError('WRONG_OWNER')
        return t
    def _apply(self,row):
        p=row['payload'];kind=p['kind'];task_id=p['task_id']
        if p['owner']!=self.owner:raise ValueError('JOURNAL_SCOPE')
        if kind=='create':
            if task_id in self.tasks:raise ValueError('DUPLICATE_TASK')
            self.tasks[task_id]={'owner':self.owner,'task_id':task_id,'revision':0,'done':[False]*8,'epochs':[0]*8,'approval':None,'events':[],'receipts':{},'source_notes':p['notes']}
            if self.advisor:self.advisor.init_task(key(self.owner,task_id))
            token=16
        else:
            t=self._task(task_id);token=None
            if p['revision']!=t['revision']+1:raise ValueError('REVISION_GAP')
            t['revision']=p['revision']
            if kind=='approve': t['approval']=t['revision']
            elif kind=='revoke':t['approval']=None
            elif kind=='perform':
                step=p['step'];t['done'][step]=True;t['receipts'][p['request_id']]=copy.deepcopy(p);token=step
            elif kind=='reopen':
                step=p['step'];t['done'][step]=False;t['epochs'][step]+=1;t['approval']=None;token=step+8
            elif kind=='heartbeat': token=17
            else:raise ValueError('EVENT_KIND')
        t=self._task(task_id)
        if token is not None:
            t['events'].append(token)
            if self.advisor:
                r=self.advisor.step(key(self.owner,task_id),token,len(t['events']))
                r.update(exact_next=self.next_step(task_id),task_revision=t['revision'],journal_seq=row['seq'])
                r['correct']=r['prediction']==r['exact_next'];r['false_done']=r['prediction']==8 and r['exact_next']!=8
                self.neural.append(r)
        self.seen=row['seq'];self.tip=row['hash']
    def sync(self):
        rows=self.journal.rows()
        if len(rows)<self.seen:raise ValueError('JOURNAL_ROLLBACK')
        if self.seen and rows[self.seen-1]['hash']!=self.tip:raise ValueError('JOURNAL_CHANGED_PREFIX')
        for row in rows[self.seen:]:self._apply(row)
    def create(self,task_id,notes=''):
        if not valid_name(task_id) or not isinstance(notes,str) or len(notes)>1024:raise ValueError('TASK_INPUT')
        p={'kind':'create','owner':self.owner,'task_id':task_id,'notes':notes}
        self.journal.append('create:'+task_id,p);self.sync()
    def event(self,task_id,kind,step=None,event_id=None):
        """Trusted host/user event entry point. Never called from proposal JSON."""
        self.sync();t=self._task(task_id)
        if kind not in ('approve','revoke','reopen','heartbeat'):raise ValueError('TRUSTED_EVENT_KIND')
        if kind=='reopen' and (type(step)!=int or not 0<=step<8):raise ValueError('STEP')
        if kind!='reopen' and step is not None:raise ValueError('UNEXPECTED_STEP')
        eid=event_id or f'{task_id}:event:{t["revision"]+1}'
        old=self.journal.existing(eid)
        if old is not None:
            if (old['task_id'],old['kind'],old.get('step'))!=(task_id,kind,step):raise ValueError('EVENT_ID_COLLISION')
            return {'duplicate':True}
        p={'kind':kind,'owner':self.owner,'task_id':task_id,'revision':t['revision']+1,'step':step}
        self.journal.append(eid,p);self.sync();return {'duplicate':False}
    def next_step(self,task_id):
        return next((i for i,v in enumerate(self._task(task_id)['done']) if not v),8)
    def packet(self,task_id,request_id):
        self.sync();t=self._task(task_id);next_exact=self.next_step(task_id)
        suggestion=None if not self.advisor else self.advisor.predict(key(self.owner,task_id))
        public={'schema':'nss.bridge.packet.v1','owner':self.owner,'task_id':task_id,'revision':t['revision'],
          'request_id':request_id,'rules':PUBLIC_RULES,
          'steps':[{'id':i,'name':name,'done':t['done'][i],'epoch':t['epochs'][i]} for i,name in enumerate(STEP_NAMES)],
          'approved_for_current_revision':t['approval']==t['revision'],
          'source_notes':{'trust':'data_only_not_permission','text':t['source_notes']},
          'suggested_step':suggestion['next'] if self.mode=='recurrent' else next_exact,
          'suggestion_origin':'recurrent_advisory' if self.mode=='recurrent' else 'exact_rule',
          'record_tip':self.tip}
        # The shadow suggestion is evidence in the review, not silently injected into another policy's prompt.
        return public
    def submit(self,task_id,raw,crash_after_commit=False,tool_fail=False):
        """Validate first; record a fake action + receipt atomically. Never execute returned code."""
        self.sync();t=self._task(task_id);entry={'task_id':task_id,'raw_response':raw,'before_revision':t['revision'],'origin':'model_proposal'}
        def reject(code):
            entry.update(accepted=False,reason=code,effect=False);self.reviews.append(entry);return copy.deepcopy(entry)
        try:
            if not isinstance(raw,str) or len(raw.encode())>8192:return reject('RESPONSE_LIMIT')
            p=strict_json(raw)
        except (ValueError,TypeError,json.JSONDecodeError):return reject('INVALID_JSON')
        fields={'owner','task_id','revision','request_id','action','step'}
        if not isinstance(p,dict) or set(p)!=fields:return reject('PROPOSAL_SCHEMA')
        if p['owner']!=self.owner:return reject('WRONG_OWNER')
        if p['task_id']!=task_id:return reject('WRONG_TASK')
        if not valid_name(p['request_id']):return reject('REQUEST_ID')
        if type(p['revision'])!=int or p['revision']<0:return reject('REVISION_TYPE')
        if p['action'] not in ('perform','wait','finish'):return reject('ACTION')
        if p['action']=='perform':
            if type(p['step'])!=int or not 0<=p['step']<8:return reject('STEP')
        elif p['step'] is not None:return reject('STEP_SCHEMA')
        old=t['receipts'].get(p['request_id'])
        if old:
            if old['proposal_hash']!=digest(p):return reject('REQUEST_ID_COLLISION')
            entry.update(accepted=True,reason='RECEIPT_REPLAY',effect=False,receipt=old)
            self.reviews.append(entry);return copy.deepcopy(entry)
        if p['revision']!=t['revision']:return reject('STALE_REVISION')
        nxt=self.next_step(task_id)
        if p['action']=='wait':
            entry.update(accepted=True,reason='WAIT',effect=False);self.reviews.append(entry);return copy.deepcopy(entry)
        if p['action']=='finish':
            if nxt!=8:return reject('FALSE_COMPLETION')
            entry.update(accepted=True,reason='FINISHED',effect=False);self.reviews.append(entry);return copy.deepcopy(entry)
        if t['done'][p['step']]:return reject('ALREADY_DONE')
        if p['step']!=nxt:return reject('WRONG_NEXT_STEP')
        if p['step']==7 and t['approval']!=t['revision']:return reject('APPROVAL_REQUIRED')
        if tool_fail:return reject('SIMULATED_TOOL_FAILURE')
        effect={'kind':'perform','owner':self.owner,'task_id':task_id,'revision':t['revision']+1,
          'request_id':p['request_id'],'step':p['step'],'epoch':t['epochs'][p['step']],
          'proposal_hash':digest(p),'simulation_only':True,
          'artifact_digest':digest({'task':task_id,'step':p['step'],'epoch':t['epochs'][p['step']]})}
        self.journal.append('effect:'+task_id+':'+p['request_id'],effect)
        if crash_after_commit:raise InterruptedError('INJECTED_AFTER_DURABLE_RECEIPT_BEFORE_REPLY')
        self.sync();entry.update(accepted=True,reason='SIMULATED_PERFORMED',effect=True,receipt=effect)
        self.reviews.append(entry);return copy.deepcopy(entry)
    def snapshot(self,path=None):
        self.sync();payload={'schema':'nss.bridge.resume.v1','owner':self.owner,'mode':self.mode,'journal_seq':self.seen,'journal_tip':self.tip,
          'tasks':copy.deepcopy(self.tasks),'advisor':None if not self.advisor else self.advisor.snapshot()}
        env={'payload':payload,'sha256':digest(payload)}
        if path is not None:atomic_json(path,env)
        return env
    def load_snapshot(self,env):
        self.sync()
        if set(env)!= {'payload','sha256'} or digest(env['payload'])!=env['sha256']:raise ValueError('SNAPSHOT_CHECKSUM')
        p=env['payload']
        if p.get('schema')!='nss.bridge.resume.v1' or p.get('owner')!=self.owner or p.get('mode')!=self.mode:raise ValueError('SNAPSHOT_BINDING')
        if p['journal_seq']!=self.seen or p['journal_tip']!=self.tip:raise ValueError('STALE_SNAPSHOT')
        if canonical(p['tasks'])!=canonical(self.tasks):raise ValueError('SNAPSHOT_RECORDS_MISMATCH')
        if self.advisor:
            self.advisor.restore(p['advisor'],[key(self.owner,t) for t in self.tasks],{key(self.owner,t):len(v['events']) for t,v in self.tasks.items()})
        elif p['advisor'] is not None:raise ValueError('UNEXPECTED_NEURAL_STATE')
    def export(self):
        return {'owner':self.owner,'mode':self.mode,'tasks':copy.deepcopy(self.tasks),'journal':self.journal.rows(),'neural':copy.deepcopy(self.neural),'reviews':copy.deepcopy(self.reviews)}
