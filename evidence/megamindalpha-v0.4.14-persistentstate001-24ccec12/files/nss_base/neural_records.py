"""Local numerical experiment journal, separate from integer EvaluationRun001.

Content hashes detect accidental modification, not a malicious author rewriting
all records. No qualification, signed authority, automatic promotion or runtime
configuration pointer lives here. Failed preparation never creates a valid result.
"""
from contextlib import contextmanager
from copy import deepcopy
import os
from pathlib import Path
import re
import sqlite3

from .neural_contracts import (FORMAT, encoded, fields, fingerprint, protocol,
    required_updates, trial_verdict)
from .runtime import fail
from .serialization import decode


def validate_plan(p):
    fields(p,('schema_version','protocol','data_binding','environment','code_sha256','authority'))
    protocol(p['protocol']);encoded(p)
    if type(p['schema_version']) is not int or p['schema_version'] not in (1,2) or p['authority']!='NONE':
        fail('VALIDATION_FAILED','Invalid plan version or authority')
    if type(p['code_sha256']) is not str or not re.fullmatch('[0-9a-f]{64}',p['code_sha256']):
        fail('VALIDATION_FAILED','Invalid code identity')
    fields(p['data_binding'],('snapshot_id','snapshot_sha256','codec_sha256','test_sha256','source_hashes'))
    fields(p['data_binding']['source_hashes'],('train','validation'))
    for h in [p['data_binding'][k] for k in ('snapshot_sha256','codec_sha256','test_sha256')]+list(p['data_binding']['source_hashes'].values()):
        if type(h) is not str or not re.fullmatch('[0-9a-f]{64}',h):fail('VALIDATION_FAILED','Invalid data hash')
    fields(p['environment'],('python','torch','platform','machine','device','dtype','threads','deterministic_algorithms','cuda_used','packed_ternary','energy_measured') + (('numerics',) if p['schema_version']==2 else ()))
    if p['schema_version']==2:
        n=p['environment']['numerics']
        fields(n,('schema_version','torch_build_sha256','cpu_identity_sha256','cpu_capability','backend_environment','float32_matmul_precision','cpu_autocast','score_path','mse_rule'))
        if type(n['schema_version']) is not int or n['schema_version']!=1 or n['float32_matmul_precision']!='highest' or n['cpu_autocast'] is not False or n['score_path']!='reloaded_checkpoints_no_grad_v2' or n['mse_rule']!='torch_fp32_mean_exact':
            fail('INCOMPATIBLE_CONFIGURATION','Unsupported numerical execution contract')
        for key in ('torch_build_sha256','cpu_identity_sha256'):
            if type(n[key]) is not str or not re.fullmatch('[0-9a-f]{64}',n[key]):fail('VALIDATION_FAILED','Invalid numerical identity hash')
        if type(n['cpu_capability']) is not str or not 1<=len(n['cpu_capability'])<=64:fail('VALIDATION_FAILED','Invalid CPU capability')
        fields(n['backend_environment'],('MKL_CBWR','MKL_ENABLE_INSTRUCTIONS','MKL_NUM_THREADS','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','ATEN_CPU_CAPABILITY','ONEDNN_MAX_CPU_ISA'))
        if any(v is not None and (type(v) is not str or len(v)>128) for v in n['backend_environment'].values()):fail('VALIDATION_FAILED','Invalid numerical backend environment')
    e=p['environment']
    if e['device']!='cpu' or e['dtype']!='float32' or type(e['threads']) is not int or e['threads']!=1 or e['deterministic_algorithms'] is not True or any(e[k] is not False for k in ('cuda_used','packed_ternary','energy_measured')):
        fail('INCOMPATIBLE_CONFIGURATION','Unsupported runtime environment')
    return deepcopy(p)


def validate_report(plan,r):
    validate_plan(plan)
    fields(r,('schema_version','format','plan_sha256','checker','authority','scope',
        'verdict','stop_reason','completed_trials','required_optimizer_updates','trials','data_permission_scope'))
    encoded(r);p=plan['protocol']
    if (type(r['schema_version']) is not int or r['schema_version']!=1 or r['format']!=FORMAT
        or r['plan_sha256']!=fingerprint(plan) or r['checker']!='symbol_pair_accuracy_and_recovery_v1'
        or r['authority']!='NONE' or r['scope']!='DEVELOPMENT_NEURAL_LINEAR_SMOKE_TEST'):
        fail('VALIDATION_FAILED','Report header differs from its plan/contract')
    expected=required_updates(p)
    if type(r['required_optimizer_updates']) is not int or r['required_optimizer_updates']!=expected:
        fail('VALIDATION_FAILED','Optimizer budget accounting differs')
    if type(r['trials']) is not list or type(r['completed_trials']) is not int or len(r['trials'])!=r['completed_trials']:
        fail('VALIDATION_FAILED','Invalid trial count')
    if p['max_optimizer_steps']<expected:
        if r['trials'] or r['verdict']!='INCONCLUSIVE' or r['stop_reason']!='BUDGET_EXHAUSTED':
            fail('VALIDATION_FAILED','Insufficient budget cannot produce a complete verdict')
        return deepcopy(r)
    scope=[(s,m) for m in p['precisions'] for s in p['seeds']]
    if len(r['trials'])!=len(scope):fail('VALIDATION_FAILED','Incomplete seed/precision matrix')
    verdicts=[]
    for row,(s,m) in zip(r['trials'],scope):
        fields(row,('result','artifacts','recovery'))
        result=row['result']
        fields(result,('seed','precision','metrics','training','invariants','parameters','effective_core_values','core_storage','overlay_precision','checkpoint_hashes'))
        fields(result['metrics'],('core','A','B','AB','joint','gen2','gen2_retained','ablation_A','ablation_B','ablation_core'))
        fields(result['invariants'],('core_trained','core_unchanged_after_freeze','previous_overlays_unchanged','gen2_reuses_exact_B','blank_overlays_noop'))
        fields(result['checkpoint_hashes'],('core','A','B','joint','A2'))
        if result['seed']!=s or result['precision']!=m:fail('VALIDATION_FAILED','Trial identity/order differs')
        if set(row['artifacts'])!= {'core','A','B','joint','A2'}:fail('VALIDATION_FAILED','Missing checkpoint')
        if result['checkpoint_hashes']!={k:fingerprint(v) for k,v in row['artifacts'].items()}:
            fail('VALIDATION_FAILED','Checkpoint hashes differ')
        if result['parameters']!= {'core':512,'A':128,'B':128,'modular_total':256,'joint':256,'A2':128}:
            fail('VALIDATION_FAILED','Parameter comparison differs')
        log=result['training']
        if set(log)!= {'core','A','B','joint','A2'}:fail('VALIDATION_FAILED','Incomplete training log')
        for name,item in log.items():
            base=['updates','first_loss','last_loss','seconds']
            fields(item,base if name=='core' else base+['blank_noop','weights_changed','train_input_tokens'])
            for key in ('first_loss','last_loss','seconds'):
                if type(item[key]) not in (int,float) or item[key]<0:fail('VALIDATION_FAILED','Invalid training measurement')
            if type(item['updates']) is not int:fail('VALIDATION_FAILED','Invalid update count')
            if name!='core' and (item['blank_noop'] is not True or item['weights_changed'] is not True or type(item['train_input_tokens']) is not int or item['train_input_tokens']!=item['updates']*128*2):
                fail('VALIDATION_FAILED','Invalid overlay/update accounting')
        if log['core']['updates']!=p['core_steps'] or any(log[k]['updates']!=p['overlay_steps'] for k in ('A','B','A2')) or log['joint']['updates']!=2*p['overlay_steps']:
            fail('VALIDATION_FAILED','Training budgets differ from the protocol')
        if log['joint']['train_input_tokens']!=log['A']['train_input_tokens']+log['B']['train_input_tokens']:
            fail('VALIDATION_FAILED','Input-token comparison differs')
        if any(v is not True for v in result['invariants'].values()):fail('VALIDATION_FAILED','Structural invariant not satisfied')
        q=row['recovery']
        fields(q,('stale_cache_rejected','source_cache_unchanged','recovered_equals_clean_exact','recovered_within_tolerance','max_absolute_error','draft_cleared','denied_status','reverse_status','core_only_return','committed_mock_effects','ecids','state_kind','approval_kind'))
        if type(q['max_absolute_error']) not in (int,float) or q['max_absolute_error']<0:
            fail('VALIDATION_FAILED','Invalid recovery numerical error')
        if (q['stale_cache_rejected'] is not True or q['source_cache_unchanged'] is not True
            or q['recovered_within_tolerance'] is not True or q['committed_mock_effects']!=1
            or q['denied_status']!='AUTHORIZATION_DENIED' or q['core_only_return']!='SUCCESS'):
            fail('VALIDATION_FAILED','Invalid recovery evidence')
        verdicts.append(trial_verdict(p,result['metrics']))
    if r['verdict']!=('PASS' if all(v=='PASS' for v in verdicts) else 'FAIL') or r['stop_reason']!='COMPLETE':
        fail('VALIDATION_FAILED','Reported verdict differs from frozen numerical criteria')
    return deepcopy(r)


class ProbeRuns:
    """Single local runner. Pure restart from seed, not optimizer checkpoint resume."""
    filename = 'neural_runs.sqlite3'
    format = FORMAT
    validate_plan = staticmethod(validate_plan)
    validate_report = staticmethod(validate_report)

    def __init__(self,directory):
        self.path=Path(directory).resolve()/self.filename
        with self._db():pass

    @classmethod
    def create(cls,directory):
        d=Path(directory)
        if d.exists() and any(d.iterdir()):fail('CONSTRAINT_CONFLICT','New journal needs an empty directory')
        d.mkdir(parents=True,exist_ok=True)
        db=sqlite3.connect(d/cls.filename)
        try:
            db.execute('PRAGMA synchronous=FULL')
            db.execute('CREATE TABLE metadata(format TEXT NOT NULL)');db.execute('INSERT INTO metadata VALUES (?)',(cls.format,))
            db.execute('CREATE TABLE attempts(id TEXT PRIMARY KEY, plan TEXT NOT NULL, plan_hash TEXT NOT NULL, status TEXT NOT NULL, report TEXT, report_hash TEXT, receipt TEXT)')
            db.commit()
        finally:db.close()
        return cls(d)

    @contextmanager
    def _db(self):
        if not self.path.is_file():fail('RECOVERY_REQUIRED','Numerical journal missing; no implicit repair')
        db=sqlite3.connect(self.path.as_uri()+'?mode=rw',uri=True,timeout=5)
        db.row_factory=sqlite3.Row
        try:
            db.execute('PRAGMA synchronous=FULL');db.execute('BEGIN IMMEDIATE')
            rows=db.execute('SELECT format FROM metadata').fetchall()
            if len(rows)!=1 or rows[0][0]!=self.format:fail('INCOMPATIBLE_CONFIGURATION','Wrong numerical journal format')
            yield db
            db.commit()
        except sqlite3.Error:
            db.rollback();fail('RECOVERY_REQUIRED','Corrupt or unavailable numerical journal')
        except BaseException:
            db.rollback();raise
        finally:db.close()

    def _read(self,db,id):
        if type(id) is not str or not re.fullmatch('[A-Za-z0-9_.:-]{1,96}',id):
            fail('VALIDATION_FAILED','Invalid numerical attempt ID')
        row=db.execute('SELECT * FROM attempts WHERE id=?',(id,)).fetchone()
        if row is None:return None
        p=self.validate_plan(decode(row['plan']))
        if fingerprint(p)!=row['plan_hash']:fail('VALIDATION_FAILED','Plan digest mismatch')
        report=receipt=None
        if row['status']=='PREPARED':
            if any(row[k] is not None for k in ('report','report_hash','receipt')):
                fail('VALIDATION_FAILED','Partial numerical publication')
        elif row['status']=='FINALIZED':
            if any(row[k] is None for k in ('report','report_hash','receipt')):
                fail('VALIDATION_FAILED','Incomplete report/receipt')
            report=self.validate_report(p,decode(row['report']));receipt=decode(row['receipt'])
            expected={'id':id,'plan_sha256':fingerprint(p),'report_sha256':fingerprint(report),
                      'verdict':report['verdict'],'authority':'NONE'}
            if row['report_hash']!=fingerprint(report) or receipt!=expected:
                fail('VALIDATION_FAILED','Numerical receipt identity mismatch')
        else:fail('VALIDATION_FAILED','Unknown attempt state')
        return {'id':id,'status':row['status'],'plan':p,'report':report,'receipt':receipt,
                'historical':row['status']=='FINALIZED','authority':'NONE'}

    def inspect(self,id):
        with self._db() as db:
            result=self._read(db,id)
            if result is None:fail('INSUFFICIENT_EVIDENCE','Unknown numerical attempt')
            return result

    def prepare(self,id,plan):
        p=self.validate_plan(plan)
        with self._db() as db:
            previous=self._read(db,id)
            if previous:
                if previous['plan']!=p:fail('CONSTRAINT_CONFLICT','Attempt ID already binds another plan')
                return previous
            db.execute('INSERT INTO attempts VALUES (?,?,?,\'PREPARED\',NULL,NULL,NULL)',
                       (id,encoded(p).decode(),fingerprint(p)))
        return self.inspect(id)

    def finalize(self,id,report,*,crash_at=None):
        if crash_at not in (None,'before_commit','after_commit'):fail('VALIDATION_FAILED','Invalid publication fault hook')
        with self._db() as db:
            previous=self._read(db,id)
            if previous is None:fail('INSUFFICIENT_EVIDENCE','No prepared plan')
            r=self.validate_report(previous['plan'],report)
            if previous['status']=='FINALIZED':
                if previous['report']!=r:fail('CONSTRAINT_CONFLICT','Finalized evidence is immutable')
                return previous
            receipt={'id':id,'plan_sha256':fingerprint(previous['plan']),
                     'report_sha256':fingerprint(r),'verdict':r['verdict'],'authority':'NONE'}
            db.execute('UPDATE attempts SET status=\'FINALIZED\',report=?,report_hash=?,receipt=? WHERE id=?',
                (encoded(r).decode(),fingerprint(r),encoded(receipt).decode(),id))
            if crash_at=='before_commit':os._exit(79)
        if crash_at=='after_commit':os._exit(79)
        return self.inspect(id)

    def audit(self):
        with self._db() as db:
            if [r[0] for r in db.execute('PRAGMA integrity_check')]!=['ok']:
                fail('VALIDATION_FAILED','Numerical SQLite integrity check failed')
            ids=[r[0] for r in db.execute('SELECT id FROM attempts ORDER BY id')]
            for id in ids:self._read(db,id)
            return {'attempts':len(ids),'authority':'NONE','kind':'local structural/hash integrity, not independent model evaluation'}
