"""Durable single-runner recovery-attempt and checkpoint publication for Experiment 001B.

This module models a local process-crash-safe publication boundary. It does not claim
multi-runner safety, power-loss guarantees beyond SQLite's local durability settings,
or real external-action exactly-once semantics.
"""
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
import json
import os
import sqlite3

from .recovery import accept_cache, recover
from .runtime import ContractError, digest, fail
from .serialization import decode, validate
from .task_records import (validate_checkpoint, validate_handoff_binding,
    validate_target_record, validate_sealed_revision, prepare_handoff)


@contextmanager
def database(path, *, create=False):
    path = Path(path).resolve()
    if not create and not path.is_file():
        fail("RECOVERY_REQUIRED", "Durable recovery store is missing")
    db = sqlite3.connect(path if create else path.as_uri() + "?mode=rw",
                         timeout=5, uri=not create)
    try:
        db.execute("PRAGMA synchronous=FULL")
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        fail("INTERNAL_FAILURE", f"Durable recovery storage failure: {e}")
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def checkpoint_hash(state):
    validate_checkpoint(state)
    return digest(state)


def attempt_record(value):
    validate(value, "recovery_attempt.schema.json")
    if (value['schema_version'] == 2) != ('task_handoff' in value):
        fail('VALIDATION_FAILED', 'Attempt version and task handoff disagree')
    if 'task_handoff' in value:
        binding=value['task_handoff']
        if binding['request']['source_checkpoint_hash'] != value['source_checkpoint_hash'] or binding['target_record']['task_id'] != value['task_id']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Attempt handoff scope differs')
    status = value["status"]
    staged = value["staged_checkpoint_hash"]
    published = value["published_checkpoint_hash"]
    failure = value["failure_code"]
    if status == "PREPARED" and (staged is not None or published is not None or failure is not None):
        fail("VALIDATION_FAILED", "PREPARED attempt cannot carry staged/published/failure state")
    if status == "STAGED" and (staged is None or published is not None or failure is not None):
        fail("VALIDATION_FAILED", "STAGED attempt requires only a staged checkpoint")
    if status == "PUBLISHED" and (staged is None or published != staged or failure is not None):
        fail("VALIDATION_FAILED", "PUBLISHED attempt requires matching staged/published checkpoint")
    if status == "FAILED" and (failure is None or published is not None):
        fail("VALIDATION_FAILED", "FAILED attempt requires a failure code and no published checkpoint")
    return value


def _get_body(db, table, key):
    row = db.execute(f"SELECT body FROM {table} WHERE key=?", (key,)).fetchone()
    return None if row is None else decode(row[0])


def crash(hook, stage):
    if hook == stage:
        os._exit(73)


class RecoveryStore:
    """One runner owns this store directory at a time.

    Content-addressed checkpoints may be staged durably without becoming active. The
    active task pointer changes only in the same SQLite transaction that marks an
    attempt PUBLISHED.
    """
    def __init__(self, directory):
        directory = Path(directory)
        existed = directory.exists()
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / "recovery.sqlite3"
        # If a non-empty recovery directory survives but the DB is absent, fail closed.
        if not self.path.exists() and existed and any(directory.iterdir()):
            fail("RECOVERY_REQUIRED", "Recovery directory exists but durable database is missing")
        with database(self.path, create=not self.path.exists()) as db:
            db.execute("CREATE TABLE IF NOT EXISTS attempts(key TEXT PRIMARY KEY, body TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS checkpoints(key TEXT PRIMARY KEY, body TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS current(task_id TEXT PRIMARY KEY, checkpoint_hash TEXT NOT NULL)")

    def _checkpoint(self, db, key):
        value = _get_body(db, "checkpoints", key)
        if value is None:
            fail("RECOVERY_REQUIRED", "Referenced checkpoint is missing")
        validate_checkpoint(value)
        if checkpoint_hash(value) != key:
            fail("VALIDATION_FAILED", "Stored checkpoint hash/body mismatch")
        return value

    def _attempt(self, db, attempt_id):
        value = _get_body(db, "attempts", attempt_id)
        if value is None:
            return None
        attempt_record(value)
        if value["attempt_id"] != attempt_id:
            fail("VALIDATION_FAILED", "Stored attempt ID and key disagree")
        if 'task_handoff' in value:
            validate_handoff_binding(self._checkpoint(db, value['source_checkpoint_hash']), value['task_handoff'])
        return value

    def inspect_attempt(self, attempt_id):
        with database(self.path) as db:
            value = self._attempt(db, attempt_id)
            return deepcopy(value) if value is not None else None

    def current(self, task_id):
        with database(self.path) as db:
            row = db.execute("SELECT checkpoint_hash FROM current WHERE task_id=?", (task_id,)).fetchone()
            if row is None:
                fail("RECOVERY_REQUIRED", "No published checkpoint for task")
            state = self._checkpoint(db, row[0])
            if state["task_id"] != task_id:
                fail("VALIDATION_FAILED", "Current pointer references another task")
            return deepcopy(state)

    def current_hash(self, task_id):
        with database(self.path) as db:
            row = db.execute("SELECT checkpoint_hash FROM current WHERE task_id=?", (task_id,)).fetchone()
            if row is None:
                fail("RECOVERY_REQUIRED", "No published checkpoint for task")
            state = self._checkpoint(db, row[0])
            if state["task_id"] != task_id:
                fail("VALIDATION_FAILED", "Current pointer references another task")
            return row[0]

    def publish_initial(self, state):
        validate_checkpoint(state)
        key = checkpoint_hash(state)
        with database(self.path) as db:
            row = db.execute("SELECT checkpoint_hash FROM current WHERE task_id=?", (state["task_id"],)).fetchone()
            if row is not None:
                current = self._checkpoint(db, row[0])
                if row[0] != key or current != state:
                    fail("INCOMPATIBLE_CONFIGURATION", "Task already has a different published checkpoint")
                return key
            db.execute("INSERT OR IGNORE INTO checkpoints(key,body) VALUES (?,?)",
                       (key, json.dumps(state, sort_keys=True)))
            # Verify an existing content-addressed row cannot disagree.
            if self._checkpoint(db, key) != state:
                fail("VALIDATION_FAILED", "Checkpoint hash collision/body mismatch")
            db.execute("INSERT INTO current(task_id,checkpoint_hash) VALUES (?,?)", (state["task_id"], key))
        return key

    def prepare(self, *, attempt_id, source, target_profile, target_ecid, input_artifact, action_keys, task_handoff=None):
        validate_checkpoint(source)
        validate(input_artifact, "artifact.schema.json")
        if input_artifact != source["input_artifact"]:
            fail("INCOMPATIBLE_CONFIGURATION", "Attempt inputs differ from source")
        if source['schema_version'] == 2:
            validate_handoff_binding(source, task_handoff)
        elif task_handoff is not None:
            fail('VALIDATION_FAILED', 'Legacy source has no TaskRecord')
        action_keys = sorted(action_keys)
        value = dict(
            schema_version=1,
            attempt_id=attempt_id,
            task_id=source["task_id"],
            source_checkpoint_hash=checkpoint_hash(source),
            source_profile=source["profile"],
            source_ecid=source["ecid"],
            target_profile=target_profile,
            target_ecid=target_ecid,
            input_artifact=deepcopy(input_artifact),
            action_keys=action_keys,
            status="PREPARED",
            staged_checkpoint_hash=None,
            published_checkpoint_hash=None,
            failure_code=None,
            detail="",
        )
        if task_handoff is not None:
            value.update(schema_version=2, task_handoff=deepcopy(task_handoff))
        attempt_record(value)
        with database(self.path) as db:
            existing = self._attempt(db, attempt_id)
            if existing is not None:
                if existing != value:
                    fail("CONSTRAINT_CONFLICT", "Attempt ID reused for different recovery request")
                return deepcopy(existing)
            row = db.execute("SELECT checkpoint_hash FROM current WHERE task_id=?", (source["task_id"],)).fetchone()
            if row is None or row[0] != value["source_checkpoint_hash"]:
                fail("INCOMPATIBLE_CONFIGURATION", "Source is not the currently published checkpoint")
            if self._checkpoint(db, row[0]) != source:
                fail("VALIDATION_FAILED", "Published source checkpoint differs from supplied source")
            db.execute("INSERT INTO attempts(key,body) VALUES (?,?)",
                       (attempt_id, json.dumps(value, sort_keys=True)))
        return deepcopy(value)

    def stage(self, attempt_id, state):
        validate_checkpoint(state)
        key = checkpoint_hash(state)
        with database(self.path) as db:
            attempt = self._attempt(db, attempt_id)
            if attempt is None:
                fail("VALIDATION_FAILED", "Unknown recovery attempt")
            if attempt["status"] != "PREPARED":
                fail("CONSTRAINT_CONFLICT", "Only PREPARED attempts may stage a result")
            if state["task_id"] != attempt["task_id"] or state["profile"] != attempt["target_profile"] or state["ecid"] != attempt["target_ecid"]:
                fail("INCOMPATIBLE_CONFIGURATION", "Staged checkpoint does not match attempt target")
            if state["input_artifact"] != attempt["input_artifact"]:
                fail("INCOMPATIBLE_CONFIGURATION", "Staged checkpoint portable inputs differ from attempt")
            source=self._checkpoint(db, attempt['source_checkpoint_hash'])
            if 'task_handoff' in attempt:
                validate_target_record(source, attempt['task_handoff'], state)
            elif state['schema_version'] != 1:
                fail('VALIDATION_FAILED', 'Legacy attempt cannot stage a TaskRecord')
            db.execute("INSERT OR IGNORE INTO checkpoints(key,body) VALUES (?,?)",
                       (key, json.dumps(state, sort_keys=True)))
            if self._checkpoint(db, key) != state:
                fail("VALIDATION_FAILED", "Checkpoint hash collision/body mismatch")
            attempt.update(status="STAGED", staged_checkpoint_hash=key)
            attempt_record(attempt)
            db.execute("UPDATE attempts SET body=? WHERE key=?",
                       (json.dumps(attempt, sort_keys=True), attempt_id))
        return key

    def mark_failed(self, attempt_id, code, detail):
        with database(self.path) as db:
            attempt = self._attempt(db, attempt_id)
            if attempt is None:
                fail("VALIDATION_FAILED", "Unknown recovery attempt")
            if attempt["status"] == "PUBLISHED":
                fail("CONSTRAINT_CONFLICT", "Published attempt cannot be marked failed")
            attempt.update(status="FAILED", published_checkpoint_hash=None,
                           failure_code=code, detail=detail)
            attempt_record(attempt)
            db.execute("UPDATE attempts SET body=? WHERE key=?",
                       (json.dumps(attempt, sort_keys=True), attempt_id))
        return deepcopy(attempt)

    def staged(self, attempt_id):
        with database(self.path) as db:
            attempt = self._attempt(db, attempt_id)
            if attempt is None or attempt["status"] not in ("STAGED", "PUBLISHED"):
                fail("RECOVERY_REQUIRED", "No durable staged checkpoint for attempt")
            return deepcopy(self._checkpoint(db, attempt["staged_checkpoint_hash"]))

    def publish(self, attempt_id):
        """Atomically change the active pointer and mark the attempt PUBLISHED."""
        with database(self.path) as db:
            attempt = self._attempt(db, attempt_id)
            if attempt is None:
                fail("VALIDATION_FAILED", "Unknown recovery attempt")
            if attempt["status"] == "PUBLISHED":
                state = self._checkpoint(db, attempt["published_checkpoint_hash"])
                # Historical publication is a read, but still verify the exact
                # target and TaskRecord binding rather than trust a repointed row.
                if (state['task_id'], state['profile'], state['ecid'], state['input_artifact']) != (attempt['task_id'], attempt['target_profile'], attempt['target_ecid'], attempt['input_artifact']):
                    fail('INCOMPATIBLE_CONFIGURATION', 'Historical checkpoint differs from recorded target')
                if 'task_handoff' in attempt:
                    validate_target_record(self._checkpoint(db, attempt['source_checkpoint_hash']), attempt['task_handoff'], state)
                elif state['schema_version'] != 1:
                    fail('VALIDATION_FAILED', 'Legacy history cannot introduce a TaskRecord')
                return deepcopy(state)
            if attempt["status"] != "STAGED":
                fail("CONSTRAINT_CONFLICT", "Only STAGED attempts may be published")
            staged = self._checkpoint(db, attempt["staged_checkpoint_hash"])
            if (staged["task_id"], staged["profile"], staged["ecid"], staged["input_artifact"]) != (attempt["task_id"], attempt["target_profile"], attempt["target_ecid"], attempt["input_artifact"]):
                fail("INCOMPATIBLE_CONFIGURATION", "Staged target no longer matches attempt")
            source = self._checkpoint(db, attempt['source_checkpoint_hash'])
            if 'task_handoff' in attempt:
                validate_target_record(source, attempt['task_handoff'], staged)
            elif staged['schema_version'] != 1:
                fail('VALIDATION_FAILED', 'Legacy publication cannot introduce a TaskRecord')
            row = db.execute("SELECT checkpoint_hash FROM current WHERE task_id=?", (attempt["task_id"],)).fetchone()
            if row is None or row[0] != attempt["source_checkpoint_hash"]:
                fail("INCOMPATIBLE_CONFIGURATION", "Current checkpoint changed before publication")
            # One transaction: readers never see target current without PUBLISHED attempt state.
            db.execute("UPDATE current SET checkpoint_hash=? WHERE task_id=?",
                       (attempt["staged_checkpoint_hash"], attempt["task_id"]))
            attempt.update(status="PUBLISHED",
                           published_checkpoint_hash=attempt["staged_checkpoint_hash"])
            attempt_record(attempt)
            db.execute("UPDATE attempts SET body=? WHERE key=?",
                       (json.dumps(attempt, sort_keys=True), attempt_id))
            return deepcopy(staged)


    def publish_task_revision(self, *, task_id, expected_checkpoint_hash, task_record):
        """CAS a sealed record revision; no profile change or second current pointer.

        This is a storage primitive, not authorization. The public stage coordinator
        validates simulated authority, current computation and action evidence.
        """
        with database(self.path) as db:
            row=db.execute('SELECT checkpoint_hash FROM current WHERE task_id=?',(task_id,)).fetchone()
            if row is None:
                fail('RECOVERY_REQUIRED', 'No current task checkpoint')
            if row[0] != expected_checkpoint_hash:
                fail('INCOMPATIBLE_CONFIGURATION', 'Stale stage-finish request')
            state=self._checkpoint(db,row[0])
            if state['task_id'] != task_id:
                fail('VALIDATION_FAILED', 'Cross-task checkpoint pointer')
            for (key,) in db.execute('SELECT key FROM attempts').fetchall():
                attempt=self._attempt(db,key)
                if attempt['task_id']==task_id and attempt['status'] in ('PREPARED','STAGED'):
                    fail('RECOVERY_REQUIRED', 'Finish blocked while handoff is in flight')
            validate_sealed_revision(state,task_record)
            updated=deepcopy(state);updated.update(task_record=deepcopy(task_record),draft='')
            key=checkpoint_hash(updated)
            db.execute('INSERT OR IGNORE INTO checkpoints(key,body) VALUES (?,?)',(key,json.dumps(updated,sort_keys=True)))
            if self._checkpoint(db,key)!=updated:
                fail('VALIDATION_FAILED','Checkpoint hash collision/body mismatch')
            db.execute('UPDATE current SET checkpoint_hash=? WHERE task_id=?',(key,task_id))
            return deepcopy(updated)


def _ledger_action_keys(ledger, task_id):
    ledger.ensure_replay_safe(task_id)
    return ledger.action_keys(task_id)


def _durable_recover(bundle, store, ledger, *, task_id, destination, attempt_id,
                    authorized=False, load_ok=True, crash_at=None, task_handoff=None):
    """Resume or execute a durable recovery attempt.

    Crash hooks are process-exit boundaries used only by tests:
    after_prepare, after_compute, after_stage, after_publish.
    """
    attempt = store.inspect_attempt(attempt_id)
    if attempt is None:
        source = store.current(task_id)
        try:
            accept_cache(bundle, source, source["profile"])
            bundle.edge(source["profile"], destination)
            if not authorized:
                fail("AUTHORIZATION_DENIED", "Simulated authorization not supplied")
            action_keys = _ledger_action_keys(ledger, task_id)
            if source['schema_version'] == 2:
                validate_handoff_binding(source, task_handoff)
                if prepare_handoff(bundle, source, destination, task_handoff['request'], ledger) != task_handoff:
                    fail('INCOMPATIBLE_CONFIGURATION', 'Handoff record is not the validated source-derived plan')
            elif task_handoff is not None:
                fail('VALIDATION_FAILED', 'Legacy source has no portable TaskRecord')
            attempt = store.prepare(
                attempt_id=attempt_id,
                source=source,
                target_profile=destination,
                target_ecid=bundle.ecid(destination),
                input_artifact=source["input_artifact"],
                action_keys=action_keys,
                task_handoff=task_handoff,
            )
        except ContractError as e:
            return dict(status=e.code, state=source, attempt=None, replayed=False, detail=str(e))
        crash(crash_at, "after_prepare")
    else:
        if attempt["task_id"] != task_id or attempt["target_profile"] != destination:
            return dict(status="CONSTRAINT_CONFLICT", state=store.current(task_id), attempt=attempt,
                        replayed=False, detail="Attempt does not match requested task/destination")
        if attempt.get('task_handoff') != task_handoff:
            return dict(status='CONSTRAINT_CONFLICT', state=store.current(task_id), attempt=attempt,
                        replayed=False, detail='Retry substituted handoff request or target record')
        if attempt["status"] == "FAILED":
            return dict(status=attempt["failure_code"], state=store.current(task_id), attempt=attempt,
                        replayed=False, detail=attempt["detail"])
        if attempt["status"] == "PUBLISHED":
            state = store.publish(attempt_id)
            return dict(status="SUCCESS", state=state, attempt=store.inspect_attempt(attempt_id),
                        replayed=False, detail="Already published historical result; current pointer unchanged")
        if not authorized:
            return dict(status="AUTHORIZATION_DENIED", state=store.current(task_id), attempt=attempt,
                        replayed=False, detail="Simulated authorization required to resume unpublished attempt")

    # Re-check the exact source and committed-action set before recompute or publication.
    current = store.current(task_id)
    try:
        if checkpoint_hash(current) != attempt["source_checkpoint_hash"]:
            fail("INCOMPATIBLE_CONFIGURATION", "Current checkpoint changed during recovery attempt")
        if current["ecid"] != attempt["source_ecid"] or current["profile"] != attempt["source_profile"]:
            fail("INCOMPATIBLE_CONFIGURATION", "Current source identity differs from prepared attempt")
        if current["input_artifact"] != attempt["input_artifact"]:
            fail("INCOMPATIBLE_CONFIGURATION", "Portable inputs changed during recovery attempt")
        action_keys = _ledger_action_keys(ledger, task_id)
        if action_keys != attempt["action_keys"]:
            fail("RECOVERY_REQUIRED", "Task action set changed during recovery attempt")
        if current['schema_version'] == 2:
            validate_handoff_binding(current, task_handoff)
            if prepare_handoff(bundle, current, destination, task_handoff['request'], ledger) != task_handoff:
                fail('INCOMPATIBLE_CONFIGURATION', 'Resumed handoff evidence changed')
        edge = bundle.edge(current["profile"], destination)
        if attempt["source_ecid"] != bundle.ecid(current["profile"]):
            fail("INCOMPATIBLE_CONFIGURATION", "Source ECID differs from current bundle")
        if attempt["target_ecid"] != bundle.ecid(destination):
            fail("INCOMPATIBLE_CONFIGURATION", "Target ECID changed during recovery attempt")

        if attempt["status"] == "PREPARED":
            result = recover(bundle, current, destination, ledger, authorized=authorized, load_ok=load_ok, task_handoff=task_handoff)
            if result.status != "SUCCESS":
                failed = store.mark_failed(attempt_id, result.status, result.detail)
                return dict(status=result.status, state=current, attempt=failed,
                            replayed=result.replayed, detail=result.detail)
            target = result.state
            crash(crash_at, "after_compute")
            store.stage(attempt_id, target)
            attempt = store.inspect_attempt(attempt_id)
            crash(crash_at, "after_stage")
        elif attempt["status"] == "STAGED":
            # Validate resumed target load and state before publication.
            if not load_ok:
                fail("INTERNAL_FAILURE", "Target load unavailable on STAGED resume")
            target = store.staged(attempt_id)
            accept_cache(bundle, target, destination)
        else:
            fail("VALIDATION_FAILED", "Unexpected recovery attempt state")

        state = store.publish(attempt_id)
        crash(crash_at, "after_publish")
        return dict(status="SUCCESS", state=state, attempt=store.inspect_attempt(attempt_id),
                    replayed=edge["replay_required"], detail="")
    except ContractError as e:
        # If the attempt is still mutable, make the failure durable. Source current pointer stays unchanged.
        latest = store.inspect_attempt(attempt_id)
        if latest is not None and latest["status"] not in ("PUBLISHED", "FAILED"):
            try:
                latest = store.mark_failed(attempt_id, e.code, str(e))
            except ContractError:
                latest = store.inspect_attempt(attempt_id)
        return dict(status=e.code, state=store.current(task_id), attempt=latest,
                    replayed=False, detail=str(e))


def durable_recover(bundle, store, ledger, *, task_id, destination, attempt_id,
                    authorized=False, load_ok=True, crash_at=None, task_handoff=None):
    """Typed public boundary, including missing/corrupt durable-store failures.

    RecoveryStore methods are storage primitives, not authorization endpoints.
    A failure reports the readable current checkpoint or None if it is unavailable.
    """
    try:
        return _durable_recover(bundle, store, ledger, task_id=task_id,
            destination=destination, attempt_id=attempt_id, authorized=authorized,
            load_ok=load_ok, crash_at=crash_at, task_handoff=task_handoff)
    except ContractError as e:
        try:
            current = store.current(task_id)
        except ContractError:
            current = None
        return dict(status=e.code, state=current, attempt=None, replayed=False, detail=str(e))
