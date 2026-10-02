import copy
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from nss_base.artifacts import Bundle
from nss_base.experiment001a import FIXTURE, action, run
from nss_base.ledger import Ledger, record, database
from nss_base.recovery import checkpoint, accept_cache, execute, recover
from nss_base.runtime import ContractError
from nss_base.serialization import decode, read_json, validate


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fixture = self.root / "fixture"
        shutil.copytree(FIXTURE, self.fixture)
        self.path = self.fixture / "manifest.json"
        self.bundle = Bundle(self.path)
        self.inputs = read_json(self.fixture / "input_ref.json")
        self.source = checkpoint(self.bundle, "AB", "001A", self.inputs)
        self.ledger = Ledger(self.root / "actions")

    def assert_code(self, code, function, *args):
        with self.assertRaises(ContractError) as caught:
            function(*args)
        self.assertEqual(caught.exception.code, code)

    def mutate_manifest(self, change):
        value = read_json(self.path)
        change(value)
        self.path.write_text(json.dumps(value), encoding="utf-8")

    def test_success_and_exact_clean_equivalence(self):
        self.assertEqual(self.source["cache"], [-4, 14, 26, 80])
        original = copy.deepcopy(self.source)
        out = recover(self.bundle, self.source, "A", self.ledger, authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        self.assertTrue(out.replayed)
        self.assertEqual(out.state["cache"], [-11, 7, 19, 73])
        clean = checkpoint(self.bundle, "A", "001A", self.inputs)
        clean["draft"] = ""
        self.assertEqual(out.state, clean)
        self.assertEqual(self.source, original)
        self.assert_code("INCOMPATIBLE_CONFIGURATION", accept_cache, self.bundle, self.source, "A")

    def test_checkpoint_json_roundtrip(self):
        saved = self.root / "checkpoint.json"
        saved.write_text(json.dumps(self.source), encoding="utf-8")
        loaded = read_json(saved)
        out = recover(Bundle(self.path), loaded, "A", self.ledger, authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        self.assertEqual(loaded, self.source)

    def test_corrupt_cache_not_accepted(self):
        self.source["cache"][0] += 1
        out = recover(self.bundle, self.source, "A", self.ledger, authorized=True)
        self.assertEqual(out.status, "VALIDATION_FAILED")
        self.assertIs(out.state, self.source)

    def test_stale_ecid_rejected(self):
        self.source["ecid"] = "0" * 64
        out = recover(self.bundle, self.source, "A", self.ledger, authorized=True)
        self.assertEqual(out.status, "INCOMPATIBLE_CONFIGURATION")
        self.assertIs(out.state, self.source)

    def test_failure_retention_and_authorization(self):
        for kwargs, status in [({}, "AUTHORIZATION_DENIED"),
                               ({"authorized": True, "load_ok": False}, "INTERNAL_FAILURE")]:
            with self.subTest(status=status):
                out = recover(self.bundle, self.source, "A", self.ledger, **kwargs)
                self.assertEqual(out.status, status)
                self.assertIs(out.state, self.source)
                self.assertEqual(out.state["profile"], "AB")

    def test_directed_transition_and_no_implicit_fallback(self):
        for src, dest in [("A", "AB"), ("AB", "core")]:
            with self.subTest(src=src, dest=dest):
                state = checkpoint(self.bundle, src, "001A", self.inputs)
                out = recover(self.bundle, state, dest, self.ledger, authorized=True)
                self.assertEqual(out.status, "INCOMPATIBLE_CONFIGURATION")
                self.assertIs(out.state, state)

    def test_core_only_execution_and_qualified_fallback(self):
        state = checkpoint(self.bundle, "A", "001A", self.inputs)
        out = recover(self.bundle, state, "core", self.ledger, authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        self.assertEqual(out.state["cache"], [-5, 1, 5, 23])

    def test_explicit_same_profile_reuse(self):
        state = checkpoint(self.bundle, "A", "001A", self.inputs)
        out = recover(self.bundle, state, "A", self.ledger, authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        self.assertFalse(out.replayed)
        self.assertEqual(out.state, state)

    def test_actual_hashes(self):
        d = self.bundle.document
        for ref in [d["core"]] + [o["artifact"] for o in d["overlays"]]:
            self.assertEqual(ref["sha256"], sha256((self.fixture / ref["path"]).read_bytes()).hexdigest())

    def test_artifact_tamper_and_updated_ecid(self):
        for name in ["core", "A", "B"]:
            with self.subTest(name=name):
                path = self.fixture / "artifacts" / (name + ".json")
                original = path.read_bytes()
                old_manifest = self.path.read_bytes()
                old_ecid = self.bundle.ecid("AB")
                data = read_json(path)
                data["add"] += 1
                path.write_text(json.dumps(data), encoding="utf-8")
                self.assert_code("INCOMPATIBLE_CONFIGURATION", Bundle, self.path)
                # Rehashing declares a new configuration; it is not a silent repair.
                def update(d):
                    ref = d["core"] if name == "core" else next(o["artifact"] for o in d["overlays"] if o["id"] == name)
                    ref["sha256"] = sha256(path.read_bytes()).hexdigest()
                self.mutate_manifest(update)
                new = Bundle(self.path)
                self.assertNotEqual(new.ecid("AB"), old_ecid)
                self.assert_code("INCOMPATIBLE_CONFIGURATION", accept_cache, new, self.source, "AB")
                path.write_bytes(original)
                self.path.write_bytes(old_manifest)

    def test_loaded_bundle_detects_later_tamper(self):
        (self.fixture / "artifacts/A.json").write_text("{}", encoding="utf-8")
        out = recover(self.bundle, self.source, "A", self.ledger, authorized=True)
        self.assertEqual(out.status, "INCOMPATIBLE_CONFIGURATION")
        self.assertIs(out.state, self.source)

    def test_missing_and_changed_portable_inputs(self):
        p = self.fixture / self.inputs["path"]
        original = p.read_bytes()
        p.unlink()
        self.assert_code("VALIDATION_FAILED", checkpoint, self.bundle, "A", "001A", self.inputs)
        p.write_bytes(original + b" ")
        self.assert_code("INCOMPATIBLE_CONFIGURATION", checkpoint, self.bundle, "A", "001A", self.inputs)

    def test_corrupt_schema_cases(self):
        original = self.path.read_bytes()
        changes = [
            lambda d: d.update(unknown=True),
            lambda d: d.update(schema_version=True),
            lambda d: d.pop("generation"),
            lambda d: d["profiles"][1].update(overlays="A"),
            lambda d: d["overlays"][0]["artifact"].update(sha256="bad"),
            lambda d: d["transitions"][0].update(replay_required="yes"),
            lambda d: d["profiles"][0].update(evidence_ref=""),
            lambda d: d["profiles"].append(copy.deepcopy(d["profiles"][0])),
            lambda d: d["overlays"].append(copy.deepcopy(d["overlays"][0])),
            lambda d: d["profiles"][1].update(overlays=["A", "A"]),
            lambda d: d["profiles"][1].update(overlays=["missing"]),
        ]
        for i, change in enumerate(changes):
            with self.subTest(case=i):
                self.path.write_bytes(original)
                self.mutate_manifest(change)
                with self.assertRaises(ContractError):
                    Bundle(self.path)

    def test_strict_json_duplicate_nan_truncated(self):
        for value in ['{"x":1,"x":2}', '{"x":NaN}', '{']:
            with self.subTest(value=value):
                self.assert_code("VALIDATION_FAILED", decode, value)

    def test_invalid_profile_and_transition_semantics(self):
        original = self.path.read_bytes()
        changes = [
            lambda d: d["profiles"].pop(0),
            lambda d: d["profiles"][2].update(overlays=["B"]),
            lambda d: d["profiles"][2].update(overlays=["B", "A"]),
            lambda d: d["overlays"][0].update(excludes=["B"]),
            lambda d: d["overlays"][0].update(requires=["B"]),
            lambda d: d["transitions"][0].update(failure_destination="core"),
            lambda d: d["transitions"][0].update(invalidate=[]),
            lambda d: d["transitions"][0].update(state_reuse_policy="reuse"),
            lambda d: d["transitions"].append(copy.deepcopy(d["transitions"][0])),
        ]
        for i, change in enumerate(changes):
            with self.subTest(case=i):
                self.path.write_bytes(original)
                self.mutate_manifest(change)
                with self.assertRaises(ContractError):
                    Bundle(self.path)

    def test_path_escape_rejected(self):
        self.mutate_manifest(lambda d: d["core"].update(path="../outside.json"))
        self.assert_code("VALIDATION_FAILED", Bundle, self.path)

    def test_deterministic_ecid_across_serialization(self):
        d = read_json(self.path)
        self.path.write_text(json.dumps(d, sort_keys=True), encoding="utf-8")
        self.assertEqual(Bundle(self.path).ecid("AB"), self.bundle.ecid("AB"))

    def test_committed_action_skip_after_restart_and_replay(self):
        first = self.ledger.perform(action())
        restarted = Ledger(self.root / "actions")
        out = recover(self.bundle, self.source, "A", restarted, authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        with patch.object(restarted, "_apply_mock", side_effect=AssertionError("Executor called twice")):
            self.assertEqual(restarted.perform(action()), first)
        self.assertEqual(restarted.effect_count(), 1)

    def test_idempotency_key_conflict(self):
        self.ledger.perform(action())
        for field in ["payload", "task_id"]:
            bad = action()
            bad[field] = {"operation": "append_marker", "value": "different"} if field == "payload" else "other-task"
            self.assert_code("CONSTRAINT_CONFLICT", self.ledger.perform, bad)
        self.assertEqual(self.ledger.effect_count(), 1)

    def test_action_record_schema_and_status_consistency(self):
        bads = []
        for change in [dict(status="DONE"), dict(status="COMMITTED"), dict(receipt="unexpected"),
                       dict(key=""), dict(extra=True), dict(schema_version=True)]:
            a = action(); a.update(change); bads.append(a)
        for a in bads:
            with self.subTest(record=a):
                self.assert_code("VALIDATION_FAILED", record, a)
        a = action()
        a["payload"]["operation"] = "real_tool"
        self.assert_code("VALIDATION_FAILED", record, a)

    def test_corrupt_durable_record_is_not_trusted(self):
        self.ledger.perform(action())
        with database(self.ledger.path) as db:
            db.execute("UPDATE records SET body=?", ('{"status":"COMMITTED"}',))
        self.assert_code("VALIDATION_FAILED", Ledger, self.root / "actions")

    def test_corrupt_receipt_reconciliation(self):
        self.ledger.perform(action())
        bad = self.ledger.inspect(action()["key"])
        bad["receipt"] = "corrupt"
        with database(self.ledger.world) as db:
            db.execute("UPDATE records SET body=?", (json.dumps(bad),))
        self.assert_code("VALIDATION_FAILED", self.ledger.reconcile, action()["key"])

    def test_real_process_crash_windows(self):
        worker = Path(__file__).with_name("crash_worker.py")
        for stage in ["after_pending", "before_effect", "after_effect", "after_commit"]:
            with self.subTest(stage=stage):
                directory = self.root / stage
                result = subprocess.run([sys.executable, str(worker), str(directory), stage],
                                        capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 73, result.stderr)
                # Inspect durable PENDING before restart recovery converts it.
                if stage == "after_pending":
                    with database(directory / "ledger.sqlite3") as db:
                        self.assertEqual(decode(db.execute("SELECT body FROM records").fetchone()[0])["status"], "PENDING")
                ledger = Ledger(directory)
                status = ledger.inspect(action()["key"])["status"]
                if stage != "after_commit":
                    self.assertEqual(status, "UNCERTAIN")
                    out = recover(self.bundle, self.source, "A", ledger, authorized=True)
                    self.assertEqual(out.status, "RECOVERY_REQUIRED")
                    self.assertIs(out.state, self.source)
                    self.assert_code("RECOVERY_REQUIRED", ledger.perform, action())
                    self.assertEqual(ledger.reconcile(action()["key"]), "COMMITTED" if stage == "after_effect" else "PENDING")
                else:
                    self.assertEqual(status, "COMMITTED")
                ledger.perform(action())
                ledger = Ledger(directory)
                self.assertEqual(ledger.inspect(action()["key"])["status"], "COMMITTED")
                self.assertEqual(ledger.effect_count(), 1)
                out = recover(self.bundle, self.source, "A", ledger, authorized=True)
                self.assertEqual(out.status, "SUCCESS")
                self.assertEqual(out.state["cache"], [-11, 7, 19, 73])

    def test_missing_mock_store_never_means_no_effect(self):
        self.ledger.perform(action())
        self.ledger.world.unlink()
        self.assert_code("RECOVERY_REQUIRED", Ledger, self.root / "actions")
        self.assert_code("RECOVERY_REQUIRED", self.ledger.reconcile, action()["key"])
        self.assertFalse(self.ledger.world.exists())

    def test_uncertain_scope_and_explicit_retry(self):
        a = action()
        a["task_id"] = "other-task"
        a["status"] = "UNCERTAIN"
        with database(self.ledger.path) as db:
            db.execute("INSERT INTO records VALUES (?,?)", (a["key"], json.dumps(a)))
        self.ledger.ensure_replay_safe("001A")
        self.assert_code("RECOVERY_REQUIRED", self.ledger.ensure_replay_safe, "other-task")
        self.assertEqual(self.ledger.reconcile(a["key"]), "PENDING")
        # Reconciliation proving absence alone is not an execution or completion.
        self.assertEqual(self.ledger.effect_count(), 0)
        self.assert_code("RECOVERY_REQUIRED", self.ledger.ensure_replay_safe, "other-task")
        a["status"] = "PENDING"
        self.ledger.perform(a)
        self.ledger.ensure_replay_safe("other-task")

    def test_sqlite_corruption_fails_closed(self):
        self.ledger.path.write_bytes(b"not sqlite")
        self.assert_code("INTERNAL_FAILURE", Ledger, self.root / "actions")

    def test_action_and_schema_json_roundtrip(self):
        a = decode(json.dumps(action()))
        self.assertEqual(validate(a, "action.schema.json"), action())
        self.ledger.perform(a)
        saved = decode(json.dumps(self.ledger.inspect(a["key"])))
        self.assertEqual(record(saved)["status"], "COMMITTED")

    def test_mock_store_itself_is_idempotent(self):
        a = action()
        self.assertEqual(self.ledger._apply_mock(a), self.ledger._apply_mock(a))
        self.assertEqual(self.ledger.effect_count(), 1)

    def test_end_to_end_demo(self):
        report = run(self.root / "demo")
        self.assertTrue(report["exact_match"])
        self.assertEqual(report["effect_count"], 1)


if __name__ == "__main__":
    unittest.main()
