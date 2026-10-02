"""One durable owner of prepared evaluation runs and immutable result receipts.

Only PURE synthetic computation is replayed. FINALIZED means the attempt ended,
not that it passed. Historical evidence never conveys deployment or data authority.
"""
from contextlib import contextmanager
from copy import deepcopy
from functools import wraps
import json
import os
import sqlite3

from .evaluation_contracts import (FORMAT, comparison_scope, evaluate_repeat,
    make_report, normalize_plan, validate_material, validate_report)
from .evaluation_inputs import capture_inputs, local_path
from .experience_contracts import hash_id, identifier
from .runtime import ContractError, digest, fail
from .serialization import decode

MAX_STORED_BYTES=4*1024*1024
FAULTS=(None,'after_prepare','after_compute','after_report_write','before_commit','after_commit')


def _json(value):
    text=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
    if len(text.encode('utf-8'))>MAX_STORED_BYTES:fail('BUDGET_EXHAUSTED','Evaluation record exceeds storage budget')
    return text


def _body(text):
    if type(text) is not str or len(text.encode('utf-8'))>MAX_STORED_BYTES:
        fail('VALIDATION_FAILED','Invalid stored evaluation JSON')
    return decode(text)


def _result(data, *, historical=False, replayed=False):
    return {'status':'SUCCESS','data':deepcopy(data),'detail':'',
        'historical':historical,'replayed':replayed,'authorizes_deployment':False}


def _public(method):
    @wraps(method)
    def wrapped(*a,**kw):
        try:return method(*a,**kw)
        except ContractError as exc:
            return {'status':exc.code,'data':None,'detail':str(exc),'historical':False,
                    'replayed':False,'authorizes_deployment':False}
        except (sqlite3.Error,OSError,UnicodeError,RecursionError) as exc:
            return {'status':'INTERNAL_FAILURE','data':None,
                'detail':'Evaluation operation failed without publication authority: '+type(exc).__name__,
                'historical':False,'replayed':False,'authorizes_deployment':False}
    return wrapped


def _fault(point,selected):
    if point==selected:os._exit(77)


def _receipt(plan,material,report):
    return {'run_id':plan['run_id'],'plan_sha256':digest(plan),'material_sha256':digest(material),
        'state':'FINALIZED' if report else 'PREPARED','report_sha256':digest(report) if report else None,
        'verdict':report['verdict'] if report else None,'authority':'NONE'}


class EvaluationRuns:
    """Local trusted-operator evidence store, not a release or authorization service."""
    def __init__(self,directory):
        self.path=local_path(directory)/'evaluations.sqlite3'
        try:
            with self._db():pass
        except (sqlite3.Error,OSError):fail('RECOVERY_REQUIRED','Evaluation store cannot be opened; no implicit repair')

    @classmethod
    def create(cls,directory):
        directory=local_path(directory)
        try:
            if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
                fail('CONSTRAINT_CONFLICT','Initialize evaluations only in a new/empty directory')
            directory.mkdir(parents=True,exist_ok=True)
            db=sqlite3.connect(directory/'evaluations.sqlite3',timeout=5)
            try:
                db.execute('PRAGMA synchronous=FULL');db.execute('BEGIN IMMEDIATE')
                db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
                db.execute('''CREATE TABLE runs(id TEXT PRIMARY KEY, plan_sha256 TEXT NOT NULL,
                    plan TEXT NOT NULL, material_sha256 TEXT NOT NULL, material TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN ('PREPARED','FINALIZED')),
                    report_sha256 TEXT, report TEXT,
                    CHECK((state='PREPARED' AND report IS NULL AND report_sha256 IS NULL) OR
                          (state='FINALIZED' AND report IS NOT NULL AND report_sha256 IS NOT NULL)))''')
                db.execute('CREATE TABLE receipts(run_id TEXT PRIMARY KEY, body TEXT NOT NULL)')
                db.executemany('INSERT INTO metadata VALUES (?,?)',[('format',FORMAT),('schema_version','1')]);db.commit()
            except BaseException:db.rollback();raise
            finally:db.close()
            return cls(directory)
        except (sqlite3.Error,OSError):fail('INTERNAL_FAILURE','Evaluation initialization failed; no destructive cleanup')

    @contextmanager
    def _db(self):
        if not self.path.is_file():fail('RECOVERY_REQUIRED','Evaluation database missing; open never recreates it')
        db=sqlite3.connect(self.path.as_uri()+'?mode=rw',uri=True,timeout=5);db.row_factory=sqlite3.Row
        try:
            db.execute('PRAGMA synchronous=FULL');db.execute('BEGIN IMMEDIATE')
            try:meta=dict(db.execute('SELECT key,value FROM metadata'))
            except sqlite3.Error:fail('RECOVERY_REQUIRED','Not an initialized evaluation store')
            if meta!={'format':FORMAT,'schema_version':'1'}:
                fail('INCOMPATIBLE_CONFIGURATION','Unknown evaluation format/schema; migration required')
            yield db;db.commit()
        except BaseException:db.rollback();raise
        finally:db.close()

    def _stored(self,db,run_id):
        identifier(run_id);row=db.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone()
        if row is None:fail('INSUFFICIENT_EVIDENCE','Unknown evaluation run')
        plan=normalize_plan(_body(row['plan']));material=validate_material(plan,_body(row['material']))[0]
        if plan['run_id']!=run_id or digest(plan)!=row['plan_sha256'] or digest(material)!=row['material_sha256']:
            fail('VALIDATION_FAILED','Evaluation identity/hash mismatch')
        record=db.execute('SELECT body FROM receipts WHERE run_id=?',(run_id,)).fetchone();report=None
        if row['state']=='PREPARED':
            if row['report'] is not None or row['report_sha256'] is not None or record is not None:
                fail('VALIDATION_FAILED','Incomplete run must not have a result/receipt')
        elif row['state']=='FINALIZED':
            report=validate_report(plan,material,_body(row['report']))
            if digest(report)!=row['report_sha256'] or record is None or _body(record[0])!=_receipt(plan,material,report):
                fail('VALIDATION_FAILED','Finalized report lacks its exact completion receipt')
        else:fail('VALIDATION_FAILED','Unknown evaluation state')
        return plan,material,report

    @_public
    def prepare(self,plan,*,root,snapshots=None,archive=None,tokenizer_path=None):
        plan=normalize_plan(plan)
        with self._db() as db:
            if db.execute('SELECT 1 FROM runs WHERE id=?',(plan['run_id'],)).fetchone():
                old,material,report=self._stored(db,plan['run_id'])
                if old!=plan:fail('CONSTRAINT_CONFLICT','Run ID already binds another immutable plan')
                return _result(_receipt(old,material,report),historical=True,replayed=True)
        material=capture_inputs(plan,root,snapshots=snapshots,archive=archive,tokenizer_path=tokenizer_path)
        with self._db() as db:
            if db.execute('SELECT 1 FROM runs WHERE id=?',(plan['run_id'],)).fetchone():
                old,old_material,report=self._stored(db,plan['run_id'])
                if old!=plan or old_material!=material:fail('CONSTRAINT_CONFLICT','Run ID changed during preparation')
                return _result(_receipt(old,old_material,report),historical=True,replayed=True)
            db.execute('INSERT INTO runs VALUES (?,?,?,?,?,?,?,?)',(plan['run_id'],digest(plan),_json(plan),
                digest(material),_json(material),'PREPARED',None,None))
        return _result(_receipt(plan,material,None))

    @_public
    def execute(self,plan,*,root,snapshots=None,archive=None,tokenizer_path=None,fault_at=None):
        if fault_at not in FAULTS:fail('VALIDATION_FAILED','Unknown explicit process-crash test point')
        plan=normalize_plan(plan)
        prepared=self.prepare(plan,root=root,snapshots=snapshots,archive=archive,tokenizer_path=tokenizer_path)
        if prepared['status']!='SUCCESS':return prepared
        if prepared['data']['state']=='FINALIZED':return prepared
        _fault('after_prepare',fault_at)
        with self._db() as db:old,material,report=self._stored(db,plan['run_id'])
        def check_current():
            current=capture_inputs(plan,root,snapshots=snapshots,archive=archive,tokenizer_path=tokenizer_path)
            if current!=material:fail('INCOMPATIBLE_CONFIGURATION','Inputs changed since PREPARED; use a new plan')
        rows=[];remaining=plan['max_evaluations']
        for repeat in range(1,plan['repeats']+1):
            check_current()
            new=evaluate_repeat(plan,material,repeat,remaining);rows.extend(new);remaining-=len(new)
            if remaining==0:break
        report=make_report(plan,material,rows);_fault('after_compute',fault_at)
        check_current()  # Point-in-time recheck; NOT a cross-store permission lease.
        with self._db() as db:
            saved,saved_material,prior=self._stored(db,plan['run_id'])
            if saved!=plan or saved_material!=material:fail('CONSTRAINT_CONFLICT','Prepared run changed')
            if prior is not None:
                if prior!=report:fail('VALIDATION_FAILED','Finalized run disagrees with deterministic repeat')
                return _result(_receipt(saved,saved_material,prior),historical=True,replayed=True)
            db.execute("UPDATE runs SET state='FINALIZED',report_sha256=?,report=? WHERE id=? AND state='PREPARED'",
                       (digest(report),_json(report),plan['run_id']))
            _fault('after_report_write',fault_at)
            db.execute('INSERT INTO receipts VALUES (?,?)',(plan['run_id'],_json(_receipt(plan,material,report))))
            _fault('before_commit',fault_at)
        _fault('after_commit',fault_at)
        return _result(_receipt(plan,material,report))

    @_public
    def inspect(self,run_id):
        """Administrative HISTORY, including retained synthetic fixtures; not data authority."""
        with self._db() as db:p,m,r=self._stored(db,run_id)
        return _result({'receipt':_receipt(p,m,r),'plan':p,'material':m,'report':r},historical=True)

    @_public
    def verify_current(self,run_id,*,expected_report_sha256,root,snapshots=None,archive=None,tokenizer_path=None):
        """Recheck current inputs/permissions; does not rerun or grant release authority."""
        hash_id(expected_report_sha256)
        with self._db() as db:p,m,r=self._stored(db,run_id)
        if r is None:fail('INSUFFICIENT_EVIDENCE','Run remains incomplete with no evaluation verdict')
        if digest(r)!=expected_report_sha256:fail('CONSTRAINT_CONFLICT','Expected report identity differs')
        now=capture_inputs(p,root,snapshots=snapshots,archive=archive,tokenizer_path=tokenizer_path)
        if now!=m:fail('INCOMPATIBLE_CONFIGURATION','Current observation differs from evaluated material')
        return _result({'receipt':_receipt(p,m,r),'scope':'Point-in-time current-input check only; no permission lease or deployment authority.'})

    @_public
    def compare(self,left_id,right_id):
        """Historical comparable evidence only; no automatic winner or release selection."""
        with self._db() as db:
            lp,lm,lr=self._stored(db,left_id);rp,rm,rr=self._stored(db,right_id)
        if lr is None or rr is None:fail('INSUFFICIENT_EVIDENCE','Cannot compare unfinished runs')
        if comparison_scope(lp,lm)!=comparison_scope(rp,rm):
            fail('INCOMPATIBLE_CONFIGURATION','Runs do not share exact tests, fixtures, code and budgets')
        def score(p,m,r):return {'receipt':_receipt(p,m,r),'passed_checks':sum(x['passed'] for x in r['trials'])}
        return _result({'left':score(lp,lm,lr),'right':score(rp,rm,rr),
            'fully_observed':lr['stop_reason']==rr['stop_reason']=='COMPLETE',
            'scope':'Historical synthetic case comparison; not model quality, current permission or release approval.'},historical=True)

    @_public
    def list_runs(self,*,limit=100,after=None):
        if type(limit) is not int or not 1<=limit<=1000:fail('VALIDATION_FAILED','Limit must be 1..1000')
        if after is not None:identifier(after)
        with self._db() as db:
            ids=[row[0] for row in db.execute('SELECT id FROM runs WHERE id>? ORDER BY id LIMIT ?',(after or '',limit))]
            rows=[_receipt(*self._stored(db,id)) for id in ids]
        return _result(rows,historical=True)

    @_public
    def audit(self):
        with self._db() as db:
            if [r[0] for r in db.execute('PRAGMA integrity_check')]!=['ok']:fail('VALIDATION_FAILED','SQLite integrity failed')
            ids=[row[0] for row in db.execute('SELECT id FROM runs')];completed=0
            for id in ids:
                if self._stored(db,id)[2] is not None:completed+=1
            if db.execute('SELECT count(*) FROM receipts').fetchone()[0]!=completed:
                fail('VALIDATION_FAILED','Orphan or missing evaluation completion receipt')
            if db.execute('SELECT count(*) FROM receipts WHERE run_id NOT IN (SELECT id FROM runs)').fetchone()[0]:
                fail('VALIDATION_FAILED','Orphan completion receipt')
        return _result({'runs':len(ids),'finalized':completed,'prepared':len(ids)-completed,
            'scope':'Stored byte/semantic consistency only, not current data permissions, external authentication or an independent evaluator.'},historical=True)
