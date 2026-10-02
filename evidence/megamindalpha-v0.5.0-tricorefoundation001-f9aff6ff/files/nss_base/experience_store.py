"""Single-operator local experience archive; no training or execution authority.

One SQLite transaction publishes evidence, immutable event/revision and archive
head. This head is NOT the runtime checkpoint pointer. Public reads verify bounded
lineage by replaying the pure reducer. Hashing detects accidental inconsistency;
an attacker controlling the DB can forge an entire history. Not an audit PKI.
"""
from contextlib import contextmanager
from copy import deepcopy
from functools import wraps
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3

from .experience_contracts import (MAX_REVISIONS, MAX_SOURCE_BYTES, bounded_copy,
    check_use, hash_id, human, identifier, initial_revision, next_revision,
    normalize, purpose as validate_purpose, validate_revision)
from .runtime import ContractError, digest, fail
from .serialization import decode, validate

FORMAT = 'MegaMindAlpha.ExperienceArchive001'


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def _success(data, *, replayed=False, historical=False):
    return {'status':'SUCCESS','data':deepcopy(data),'detail':'',
            'replayed':replayed,'historical':historical}


def _public(method):
    @wraps(method)
    def call(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ContractError as exc:
            return {'status':exc.code,'data':None,'detail':str(exc),'replayed':False,'historical':False}
        except (OSError, sqlite3.Error, UnicodeError, RecursionError) as exc:
            return {'status':'INTERNAL_FAILURE','data':None,
                'detail':'Archive operation failed; inspect storage and retry the exact operation ID. '
                         + type(exc).__name__, 'replayed':False,'historical':False}
    return call


def _fault(selected, point):
    """Explicit test harness hook; never accepted from a JSON request."""
    if selected == point: os._exit(74)


def _fault_arg(value):
    if value not in (None,'after_blobs','after_revision','after_head','before_commit','after_commit'):
        fail('VALIDATION_FAILED','Unknown archive test fault point')


class ExperienceArchive:
    """Use create() once, then open with ExperienceArchive(directory).

    HUMAN metadata is an operator attestation, not an authentication credential.
    Full inspect/history/source methods are administrative inspection only.
    Downstream consumers MUST use read_for_use with an exact current revision.
    """
    def __init__(self, directory):
        self.path = Path(directory).resolve() / 'archive.sqlite3'
        try:
            with self._db(): pass
        except (OSError, sqlite3.Error):
            fail('RECOVERY_REQUIRED','Archive cannot be opened; no automatic repair or recreation')

    @classmethod
    def create(cls, directory):
        directory = Path(directory).resolve()
        try:
            if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
                fail('CONSTRAINT_CONFLICT','Archive initialization requires an empty/new directory')
            directory.mkdir(parents=True, exist_ok=True)
            path = directory / 'archive.sqlite3'
            db = sqlite3.connect(path, timeout=5)
            try:
                db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
                for sql in (
                    'CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)',
                    'CREATE TABLE evidence(sha256 TEXT PRIMARY KEY,content BLOB NOT NULL)',
                    'CREATE TABLE records(id TEXT PRIMARY KEY,capture_hash TEXT NOT NULL,capture_body TEXT NOT NULL,origin_key TEXT UNIQUE NOT NULL,head_sha256 TEXT NOT NULL)',
                    'CREATE TABLE revisions(experience_id TEXT NOT NULL,revision INTEGER NOT NULL,sha256 TEXT NOT NULL,body TEXT NOT NULL,operation_id TEXT NOT NULL UNIQUE,PRIMARY KEY(experience_id,revision),UNIQUE(experience_id,sha256))',
                    'CREATE TABLE operations(id TEXT PRIMARY KEY,kind TEXT NOT NULL,request_hash TEXT NOT NULL,body TEXT NOT NULL,result_sha256 TEXT NOT NULL)',
                    'CREATE TABLE revocations(source_sha256 TEXT NOT NULL,purpose TEXT NOT NULL,operation_id TEXT NOT NULL UNIQUE,PRIMARY KEY(source_sha256,purpose))',
                ): db.execute(sql)
                db.executemany('INSERT INTO metadata VALUES (?,?)',[('format',FORMAT),('schema_version','1')])
                db.commit()
            except BaseException:
                db.rollback(); raise
            finally: db.close()
            return cls(directory)
        except (OSError, sqlite3.Error):
            fail('INTERNAL_FAILURE','Could not initialize local archive; partial files are not automatically erased')

    @contextmanager
    def _db(self):
        if not self.path.is_file(): fail('RECOVERY_REQUIRED','Archive database missing; open never recreates it')
        db = sqlite3.connect(self.path.as_uri()+'?mode=rw',uri=True,timeout=5)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
            try: metadata = dict(db.execute('SELECT key,value FROM metadata').fetchall())
            except sqlite3.Error: fail('RECOVERY_REQUIRED','Existing file is not an initialized archive')
            if metadata != {'format':FORMAT,'schema_version':'1'}:
                fail('INCOMPATIBLE_CONFIGURATION','Unsupported archive format/schema; explicit migration required')
            yield db
            db.commit()
        except BaseException:
            db.rollback(); raise
        finally: db.close()

    def _blob(self, db, sha):
        hash_id(sha)
        row=db.execute('SELECT content FROM evidence WHERE sha256=?',(sha,)).fetchone()
        if row is None: fail('INSUFFICIENT_EVIDENCE','Referenced evidence bytes are missing')
        raw=row[0]
        if type(raw) is not bytes or len(raw)>MAX_SOURCE_BYTES or sha256(raw).hexdigest()!=sha:
            fail('VALIDATION_FAILED','Stored evidence bytes/digest disagree')
        try: raw.decode('utf-8')
        except UnicodeError: fail('VALIDATION_FAILED','Stored evidence is not valid UTF-8')
        return raw

    def _put_blobs(self, db, blobs):
        for key,raw in blobs.items():
            db.execute('INSERT OR IGNORE INTO evidence VALUES (?,?)',(key,raw))
            if self._blob(db,key)!=raw: fail('VALIDATION_FAILED','Evidence digest collision/body mismatch')

    def _hydrate(self, db, command):
        command=bounded_copy(command)
        if type(command) is not dict: fail('VALIDATION_FAILED','Stored command is not an object')
        location=command if 'evidence' in command else command.get('payload',{})
        if type(location) is not dict: fail('VALIDATION_FAILED','Stored payload is malformed')
        if 'evidence' in location:
            if type(location['evidence']) is not list or len(location['evidence'])>32:
                fail('VALIDATION_FAILED','Stored source list is malformed')
            for s in location['evidence']:
                validate(s,'experience_source.schema.json')
                s['content']=self._blob(db,s['sha256']).decode('utf-8')
        return command

    def _operation(self, db, op_id):
        row=db.execute('SELECT * FROM operations WHERE id=?',(op_id,)).fetchone()
        if row is None: return None
        body=decode(row['body'])
        normalized,_=normalize(self._hydrate(db,body),row['kind'])
        expected=digest({'kind':row['kind'],'request':normalized})
        if normalized!=body or body['operation_id']!=op_id or expected!=row['request_hash']:
            fail('VALIDATION_FAILED','Stored operation binding or digest is invalid')
        hash_id(row['result_sha256'])
        return dict(row),body

    def _lineage(self, db, id):
        identifier(id)
        capture=db.execute('SELECT * FROM records WHERE id=?',(id,)).fetchone()
        if capture is None: fail('INSUFFICIENT_EVIDENCE','Unknown experience record')
        rows=db.execute('SELECT * FROM revisions WHERE experience_id=? ORDER BY revision',(id,)).fetchall()
        if not rows or len(rows)>MAX_REVISIONS: fail('VALIDATION_FAILED','Missing/oversized revision history')
        states=[];first_command=None
        for index,row in enumerate(rows):
            op=self._operation(db,row['operation_id'])
            if op is None: fail('VALIDATION_FAILED','Revision has no operation evidence')
            op_row,command=op
            if command.get('experience_id')!=id: fail('VALIDATION_FAILED','Operation belongs to a different record')
            if index==0:
                if op_row['kind']!='CAPTURE': fail('VALIDATION_FAILED','Initial revision is not a capture')
                expected=initial_revision(command); first_command=command
            else:
                if op_row['kind']!='CHANGE': fail('VALIDATION_FAILED','Later revision lacks mutation evidence')
                expected=next_revision(states[-1],command)
            actual=validate_revision(bounded_copy(decode(row['body'])))
            h=digest(actual)
            if (row['revision']!=index or actual['revision']!=index or actual!=expected
                    or h!=row['sha256'] or op_row['result_sha256']!=h):
                fail('VALIDATION_FAILED','Revision differs from its event/reducer/lineage')
            states.append(actual)
        if (digest(first_command)!=capture['capture_hash'] or decode(capture['capture_body'])!=first_command
                or capture['head_sha256']!=digest(states[-1])):
            fail('VALIDATION_FAILED','Capture or current archive pointer disagrees with history')
        expected_origin=self._origin(first_command)
        if capture['origin_key']!=expected_origin: fail('VALIDATION_FAILED','Capture origin identity mismatch')
        return first_command,states

    @staticmethod
    def _origin(command):
        execution=command['observation']['execution']
        return digest({'task_id':execution['task_id'],'checkpoint':execution['checkpoint_sha256']}) if execution else 'external:'+command['experience_id']

    @staticmethod
    def _view(capture,state):
        return {'reference':{'experience_id':state['experience_id'],'revision':state['revision'],'sha256':digest(state)},
                'record':state,'capture':capture}

    def _verified_revocations(self, db, source_hashes=None, requested_purpose=None):
        # Validate the complete local revocation ledger before filtering. A lost
        # or repointed index row must not silently turn a withdrawal into ALLOWED.
        # This deliberately favors integrity over an unproved authority cache.
        rows=db.execute('SELECT * FROM revocations').fetchall()
        event_ids={r[0] for r in db.execute("SELECT id FROM operations WHERE kind='REVOKE_SOURCE'")}
        if event_ids!={r['operation_id'] for r in rows}:
            fail('VALIDATION_FAILED','Revocation events and index disagree; explicit repair required')
        revoked=set()
        for row in rows:
            op=self._operation(db,row['operation_id'])
            if op is None: fail('VALIDATION_FAILED','Revocation lacks operation evidence')
            op_row,command=op
            if (op_row['kind']!='REVOKE_SOURCE' or command['source_sha256']!=row['source_sha256']
                    or command['purpose']!=row['purpose'] or op_row['result_sha256']!=digest(command)):
                fail('VALIDATION_FAILED','Source revocation binding is invalid')
            human(command['actor']); self._blob(db,command['source_sha256'])
            revoked.add((row['source_sha256'],row['purpose']))
        if source_hashes is not None:
            hashes=set(source_hashes)
            return {(h,p) for h,p in revoked if h in hashes and p==requested_purpose}
        return revoked

    def _any_revoked(self, db, state, p):
        revoked=self._verified_revocations(db,[s['sha256'] for s in state['sources']],p)
        return any((s['sha256'],p) in revoked for s in state['sources'])

    def _retry(self, db, kind, command):
        found=self._operation(db,command['operation_id'])
        if found is None: return None
        row,old=found
        if row['kind']!=kind or old!=command:
            fail('CONSTRAINT_CONFLICT','Operation ID already binds a different exact request')
        if kind=='REVOKE_SOURCE':
            self._verified_revocations(db,[command['source_sha256']],command['purpose'])
            linked=db.execute('SELECT 1 FROM revocations WHERE operation_id=?',(command['operation_id'],)).fetchone()
            if linked is None: fail('VALIDATION_FAILED','Revocation result is missing')
            return _success({'source_sha256':command['source_sha256'],'purpose':command['purpose'],
                             'revocation_hash':digest(command)},replayed=True)
        capture,states=self._lineage(db,command['experience_id'])
        state=next((s for s in states if digest(s)==row['result_sha256']),None)
        if state is None: fail('VALIDATION_FAILED','Historical operation result is missing')
        return _success(self._view(capture,state),replayed=True,historical=state!=states[-1])

    @staticmethod
    def _save_operation(db,kind,command,result_hash):
        db.execute('INSERT INTO operations VALUES (?,?,?,?,?)',(command['operation_id'],kind,
            digest({'kind':kind,'request':command}),_json(command),result_hash))

    @_public
    def capture(self, request, *, fault_at=None):
        _fault_arg(fault_at);command,blobs=normalize(request,'CAPTURE')
        state=initial_revision(command);key=digest(state);id=command['experience_id']
        with self._db() as db:
            retry=self._retry(db,'CAPTURE',command)
            if retry is not None: return retry
            if db.execute('SELECT 1 FROM records WHERE id=? OR origin_key=?',(id,self._origin(command))).fetchone():
                fail('CONSTRAINT_CONFLICT','Experience ID or exact task checkpoint already captured')
            self._put_blobs(db,blobs);_fault(fault_at,'after_blobs')
            self._save_operation(db,'CAPTURE',command,key)
            db.execute('INSERT INTO revisions VALUES (?,?,?,?,?)',(id,0,key,_json(state),command['operation_id']))
            _fault(fault_at,'after_revision')
            db.execute('INSERT INTO records VALUES (?,?,?,?,?)',(id,digest(command),_json(command),self._origin(command),key))
            _fault(fault_at,'after_head');_fault(fault_at,'before_commit')
        _fault(fault_at,'after_commit')
        return _success(self._view(command,state))

    @_public
    def change(self, request, *, fault_at=None):
        _fault_arg(fault_at);command,blobs=normalize(request,'CHANGE')
        with self._db() as db:
            retry=self._retry(db,'CHANGE',command)
            if retry is not None: return retry
            capture,states=self._lineage(db,command['experience_id']);prior=states[-1]
            state=next_revision(prior,command)
            if command['action']=='PERMISSION' and command['payload']['decision']=='ALLOWED':
                if self._any_revoked(db,state,command['payload']['purpose']):
                    fail('TRAINING_RESTRICTED','Source-purpose revocation cannot be overridden by a record grant')
            self._put_blobs(db,blobs);_fault(fault_at,'after_blobs')
            key=digest(state);self._save_operation(db,'CHANGE',command,key)
            db.execute('INSERT INTO revisions VALUES (?,?,?,?,?)',(state['experience_id'],state['revision'],key,_json(state),command['operation_id']))
            _fault(fault_at,'after_revision')
            changed=db.execute('UPDATE records SET head_sha256=? WHERE id=? AND head_sha256=?',
                (key,state['experience_id'],command['expected_revision_hash'])).rowcount
            if changed!=1: fail('CONSTRAINT_CONFLICT','Archive head changed before publication')
            _fault(fault_at,'after_head');_fault(fault_at,'before_commit')
        _fault(fault_at,'after_commit')
        return _success(self._view(capture,state))

    @_public
    def revoke_source(self, request, *, fault_at=None):
        _fault_arg(fault_at);command,_=normalize(request,'REVOKE_SOURCE');human(command['actor'])
        with self._db() as db:
            retry=self._retry(db,'REVOKE_SOURCE',command)
            if retry is not None: return retry
            self._blob(db,command['source_sha256'])
            if db.execute('SELECT 1 FROM revocations WHERE source_sha256=? AND purpose=?',
                    (command['source_sha256'],command['purpose'])).fetchone():
                fail('CONSTRAINT_CONFLICT','Exact source-purpose pair already revoked; use its original operation ID')
            self._save_operation(db,'REVOKE_SOURCE',command,digest(command))
            db.execute('INSERT INTO revocations VALUES (?,?,?)',(command['source_sha256'],command['purpose'],command['operation_id']))
            _fault(fault_at,'after_revision');_fault(fault_at,'before_commit')
        _fault(fault_at,'after_commit')
        return _success({'source_sha256':command['source_sha256'],'purpose':command['purpose'],'revocation_hash':digest(command)})

    @_public
    def operation_receipt(self, operation_id):
        """Administrative exact-operation lookup; no execution or permission grant."""
        identifier(operation_id)
        with self._db() as db:
            found=self._operation(db,operation_id)
            if found is None: return _success(None)
            row,command=found
            # Verify the operation still owns a valid published result.
            self._retry(db,row['kind'],command)
            return _success({'kind':row['kind'],'request':command,
                'request_hash':row['request_hash'],'result_sha256':row['result_sha256']})

    @_public
    def inspect(self, experience_id, *, revision_hash=None):
        """Administrative historical read; does NOT grant retrieval/training use."""
        if revision_hash is not None: hash_id(revision_hash)
        with self._db() as db:
            capture,states=self._lineage(db,experience_id)
            selected=states[-1] if revision_hash is None else next((s for s in states if digest(s)==revision_hash),None)
            if selected is None: fail('INSUFFICIENT_EVIDENCE','Revision is not in this record history')
            return _success(self._view(capture,selected),historical=selected!=states[-1])

    @_public
    def inspect_source(self, source_sha256):
        with self._db() as db:
            raw=self._blob(db,source_sha256)
            return _success({'sha256':source_sha256,'content':raw.decode('utf-8'),'bytes':len(raw)})

    @_public
    def history(self, experience_id):
        with self._db() as db:
            _,states=self._lineage(db,experience_id)
            return _success([{'experience_id':s['experience_id'],'revision':s['revision'],
                'sha256':digest(s),'parent_hash':s['parent_hash'],'review_status':s['review']['status'],
                'updated_at':s['updated_at']} for s in states])

    @_public
    def list_records(self, *, limit=100, after=None):
        if type(limit) is not int or not 1<=limit<=1000: fail('VALIDATION_FAILED','List limit must be 1..1000')
        if after is not None: identifier(after)
        with self._db() as db:
            ids=[r[0] for r in db.execute('SELECT id FROM records WHERE id>? ORDER BY id LIMIT ?',(after or '',limit))]
            out=[]
            for id in ids:
                capture,states=self._lineage(db,id);s=states[-1]
                out.append({'experience_id':id,'revision':s['revision'],'sha256':digest(s),
                    'review_status':s['review']['status'],'family_id':capture['family_id'],
                    'sensitivity':capture['sensitivity']})
            return _success(out)

    @_public
    def read_for_use(self, experience_id, *, purpose: str, expected_revision_hash: str):
        """Point-in-time, exact-current-revision curated view; not a durable grant.

        A future snapshot/training consumer must recheck source permissions before
        consumption. Previously exported bytes cannot be remotely recalled here.
        """
        hash_id(expected_revision_hash);validate_purpose(purpose)
        with self._db() as db:
            capture,states=self._lineage(db,experience_id);state=states[-1]
            if digest(state)!=expected_revision_hash: fail('CONSTRAINT_CONFLICT','Use request is not for the current revision')
            check_use(state,purpose,self._any_revoked(db,state,purpose))
            return _success({'reference':self._view(capture,state)['reference'],
                'purpose':purpose,'statement':state['statement'],'sources':state['sources'],
                'observation':capture['observation'],'family_id':capture['family_id'],
                'sensitivity':capture['sensitivity'],'scope':'Point-in-time local review attestation; not authenticated permission or release authority.'})

    def _binding(self):
        # Location binding is deliberately local, not a signed portable identity.
        descriptor={'format':FORMAT,'schema_version':1,'locator':self.path.as_uri()}
        return {**descriptor,'sha256':digest(descriptor)}

    @_public
    def binding(self):
        """Public local location/format binding. Does not authenticate disk history."""
        with self._db():
            return _success(self._binding())

    def _checked_use(self, db, reference, requested_purpose, revoked):
        capture, states = self._lineage(db, reference['experience_id'])
        state = states[-1]; actual = self._view(capture, state)['reference']
        if actual != reference:
            fail('CONSTRAINT_CONFLICT', 'Use requires the exact current experience revision')
        check_use(state, requested_purpose, any((s['sha256'], requested_purpose) in revoked for s in state['sources']))
        return capture, state, actual

    @_public
    def read_evidence_for_use(self, reference, *, source_id, max_bytes=MAX_SOURCE_BYTES):
        """Exact source bytes under the SAME retrieval-permission check and lock.

        Never use inspect_source for a downstream consumer. This is a bounded
        point-in-time read, not an authentication grant or a revocation lease.
        """
        validate(bounded_copy({'references': [reference], 'purpose': 'retrieval'}),
                 'experience_use_batch.schema.json')
        identifier(source_id)
        if type(max_bytes) is not int or not 0 <= max_bytes <= MAX_SOURCE_BYTES:
            fail('VALIDATION_FAILED', 'Invalid bounded source-read limit')
        with self._db() as db:
            _, state, actual = self._checked_use(db, reference, 'retrieval', self._verified_revocations(db))
            item = next((s for s in state['sources'] if s['id'] == source_id), None)
            if item is None: fail('INSUFFICIENT_EVIDENCE', 'Unknown source in the permitted experience')
            raw = self._blob(db, item['sha256'])
            if len(raw) > max_bytes: fail('BUDGET_EXHAUSTED', 'Exact evidence exceeds the remaining byte budget')
            return _success({'reference': actual, 'source': item, 'content': raw.decode('utf-8'),
                'bytes': len(raw), 'purpose': 'retrieval', 'archive_binding': self._binding()})

    @_public
    def read_batch_for_use(self, references, *, purpose):
        """Exact-current, all-or-nothing permission check under ONE archive lock.

        This is a point-in-time observation, not a cross-store publication lease.
        Future consumption must call it again. No administrative history bypass.
        """
        command=bounded_copy({'references':references,'purpose':purpose})
        validate(command,'experience_use_batch.schema.json')
        ids=[r['experience_id'] for r in command['references']]
        if len(ids)!=len(set(ids)):
            fail('VALIDATION_FAILED','Duplicate experience in use batch')
        with self._db() as db:
            views=[]
            revoked=self._verified_revocations(db)
            for reference in command['references']:
                capture, state, actual = self._checked_use(db, reference, purpose, revoked)
                views.append({'reference':actual,'purpose':purpose,'statement':state['statement'],
                    'sources':state['sources'],'observation':capture['observation'],
                    'family_id':capture['family_id'],'sensitivity':capture['sensitivity'],
                    'updated_at':state['updated_at'],'review':state['review'],
                    'permission':state['permissions'][purpose],'source_revocation_status':'CLEAR',
                    'scope':'local-attestation-v1'})
            return _success({'archive_binding':self._binding(),'views':views})

    @_public
    def audit(self):
        with self._db() as db:
            integrity=[row[0] for row in db.execute('PRAGMA integrity_check')]
            if integrity!=['ok']: fail('VALIDATION_FAILED','SQLite integrity check failed')
            ids=[r[0] for r in db.execute('SELECT id FROM records')]
            for id in ids: self._lineage(db,id)
            self._verified_revocations(db)
            for row in db.execute('SELECT sha256 FROM evidence'): self._blob(db,row[0])
            for row in db.execute('SELECT id,kind FROM operations'):
                self._operation(db,row['id'])
                count=db.execute('SELECT COUNT(*) FROM '+('revocations' if row['kind']=='REVOKE_SOURCE' else 'revisions')+' WHERE operation_id=?',(row['id'],)).fetchone()[0]
                if count!=1: fail('VALIDATION_FAILED','Orphan or multiply referenced operation')
            if db.execute('SELECT COUNT(*) FROM revisions WHERE experience_id NOT IN (SELECT id FROM records)').fetchone()[0]:
                fail('VALIDATION_FAILED','Orphan revision')
            return _success({'records':len(ids),'revisions':db.execute('SELECT COUNT(*) FROM revisions').fetchone()[0],
                'operations':db.execute('SELECT COUNT(*) FROM operations').fetchone()[0],
                'evidence_blobs':db.execute('SELECT COUNT(*) FROM evidence').fetchone()[0],
                'source_revocations':db.execute('SELECT COUNT(*) FROM revocations').fetchone()[0],
                'scope':'Local structural/hash/lineage checks; not semantic correctness, authenticity, or hostile-tamper resistance.'})
