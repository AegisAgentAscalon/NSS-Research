"""Durable single-runner action protocol and separate idempotent mock effect store.

Crash hooks terminate the process, not just an exception handler. The local mock
has authoritative receipts; this is not a guarantee for arbitrary external APIs.
"""
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
import json
import os
import sqlite3

from .runtime import digest, fail
from .serialization import decode, validate


@contextmanager
def database(path, *, create=False):
    path = Path(path).resolve()
    if not create and not path.is_file():
        fail("RECOVERY_REQUIRED", "Local action evidence store is missing")
    db = sqlite3.connect(path if create else path.as_uri() + "?mode=rw",
                         timeout=5, uri=not create)
    try:
        db.execute("PRAGMA synchronous=FULL")
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        fail("INTERNAL_FAILURE", f"Local action storage failure: {e}")
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def record(value):
    validate(value, "action.schema.json")
    committed = value["status"] == "COMMITTED"
    if committed != isinstance(value["receipt"], str) or (committed and not value["receipt"]):
        fail("VALIDATION_FAILED", "Only COMMITTED records have nonempty receipts")
    return value


def get(db, key):
    row = db.execute("SELECT body FROM records WHERE key=?", (key,)).fetchone()
    if row is None:
        return None
    value = record(decode(row[0]))
    if value["key"] != key:
        fail("VALIDATION_FAILED", "Stored key and action key disagree")
    return value


def put(db, value):
    record(value)
    db.execute("INSERT OR REPLACE INTO records(key,body) VALUES (?,?)",
               (value["key"], json.dumps(value, sort_keys=True)))


def same_request(a, b):
    if any(a[k] != b[k] for k in ("key", "task_id", "payload")):
        fail("CONSTRAINT_CONFLICT", "Idempotency key reused with different task/payload")


def receipt_for(action):
    return digest({k: action[k] for k in ("key", "task_id", "payload")})


def crash(hook, stage):
    if hook == stage:
        os._exit(73)


class Ledger:
    """One runner owns this directory; restart must occur after the old runner exits."""
    def __init__(self, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / "ledger.sqlite3"
        self.world = directory / "mock_world.sqlite3"
        if self.path.exists() != self.world.exists():
            fail("RECOVERY_REQUIRED", "Ledger/effect store pair incomplete; do not recreate lost evidence")
        for path in (self.path, self.world):
            with database(path, create=not path.exists()) as db:
                db.execute("CREATE TABLE IF NOT EXISTS records(key TEXT PRIMARY KEY, body TEXT NOT NULL)")
        # An abandoned PENDING operation is never automatically assumed unexecuted.
        with database(self.path) as db:
            for (key,) in db.execute("SELECT key FROM records").fetchall():
                value = get(db, key)
                if value["status"] == "PENDING":
                    value["status"] = "UNCERTAIN"
                    put(db, value)

    def inspect(self, key):
        with database(self.path) as db:
            return get(db, key)

    def ensure_replay_safe(self, task_id):
        """Require all task actions to be confirmed COMMITTED with matching mock receipts."""
        with database(self.path) as db:
            values = []
            for (key,) in db.execute("SELECT key FROM records").fetchall():
                value = get(db, key)
                if value["task_id"] != task_id:
                    continue
                if value["status"] != "COMMITTED":
                    fail("RECOVERY_REQUIRED", "Pending/uncertain task action requires reconciliation")
                if value["receipt"] != receipt_for(value):
                    fail("VALIDATION_FAILED", "Committed ledger action has invalid receipt")
                values.append(value)
        with database(self.world) as world:
            for value in values:
                receipt = get(world, value["key"])
                if receipt is None:
                    fail("RECOVERY_REQUIRED", "Committed action has no authoritative mock receipt")
                same_request(value, receipt)
                if receipt["status"] != "COMMITTED" or receipt["receipt"] != value["receipt"]:
                    fail("VALIDATION_FAILED", "Ledger and mock effect receipts disagree")

    def action_keys(self, task_id):
        """Return sorted verified committed action keys for a replay-safe task."""
        self.ensure_replay_safe(task_id)
        keys = []
        with database(self.path) as db:
            for (key,) in db.execute("SELECT key FROM records").fetchall():
                value = get(db, key)
                if value["task_id"] == task_id:
                    keys.append(value["key"])
        return sorted(keys)

    def _apply_mock(self, action):
        with database(self.world) as db:
            previous = get(db, action["key"])
            if previous is not None:
                same_request(previous, action)
                if previous["status"] != "COMMITTED" or previous["receipt"] != receipt_for(action):
                    fail("VALIDATION_FAILED", "Invalid mock receipt")
                return previous["receipt"]
            completed = deepcopy(action)
            completed.update(status="COMMITTED", receipt=receipt_for(action))
            put(db, completed)  # This inserted row IS the mock external effect.
            return completed["receipt"]

    def perform(self, action, crash_at=None):
        action = deepcopy(record(action))
        if action["status"] != "PENDING":
            fail("VALIDATION_FAILED", "New action requests must be PENDING")
        with database(self.path) as db:
            old = get(db, action["key"])
            if old is not None:
                same_request(old, action)
                if old["status"] == "COMMITTED":
                    if old["receipt"] != receipt_for(action):
                        fail("VALIDATION_FAILED", "Invalid ledger receipt")
                    return old["receipt"]  # Executor is not called.
                if old["status"] == "UNCERTAIN":
                    fail("RECOVERY_REQUIRED", "Explicit reconciliation required")
            else:
                put(db, action)
        crash(crash_at, "after_pending")
        with database(self.path) as db:
            current = get(db, action["key"])
            if current["status"] != "PENDING":
                fail("RECOVERY_REQUIRED", "Action no longer pending")
            current["status"] = "UNCERTAIN"
            put(db, current)
        crash(crash_at, "before_effect")
        receipt = self._apply_mock(action)
        crash(crash_at, "after_effect")
        with database(self.path) as db:
            current = get(db, action["key"])
            current.update(status="COMMITTED", receipt=receipt)
            put(db, current)
        crash(crash_at, "after_commit")
        return receipt

    def reconcile(self, key):
        """Explicitly consult mock receipts. Proven absence permits a later retry."""
        with database(self.path) as db:
            action = get(db, key)
            if action is None:
                fail("VALIDATION_FAILED", "Unknown action")
            with database(self.world) as world:
                receipt = get(world, key)
            if receipt is not None:
                same_request(action, receipt)
                if receipt["status"] != "COMMITTED" or receipt["receipt"] != receipt_for(action):
                    fail("VALIDATION_FAILED", "Corrupted mock receipt")
                action.update(status="COMMITTED", receipt=receipt["receipt"])
            elif action["status"] == "COMMITTED":
                fail("VALIDATION_FAILED", "Committed action has no mock effect receipt")
            else:
                action.update(status="PENDING", receipt=None)
            put(db, action)
            return action["status"]

    def effect_count(self):
        with database(self.world) as db:
            return db.execute("SELECT count(*) FROM records").fetchone()[0]
