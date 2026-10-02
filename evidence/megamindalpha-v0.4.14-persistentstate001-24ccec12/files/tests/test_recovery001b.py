import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from nss_base.artifacts import Bundle
from nss_base.experiment001a import FIXTURE, action
from nss_base.experiment001b import run
from nss_base.ledger import Ledger, database as action_database
from nss_base.publication import RecoveryStore, checkpoint_hash, database as recovery_database, durable_recover
from nss_base.recovery import checkpoint, execute
from nss_base.runtime import ContractError, Catalog, Overlay, Profile, Transition, State, transition
from nss_base.serialization import decode, read_json, validate


class DurablePublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fixture = self.root / "fixture"
        shutil.copytree(FIXTURE, self.fixture)
        self.bundle = Bundle(self.fixture / "manifest.json")
        self.inputs = read_json(self.fixture / "input_ref.json")
        self.source = checkpoint(self.bundle, "AB", "001B", self.inputs)
        self.ledger = Ledger(self.root / "actions")
        self.a = action()
        self.a["key"] = "001B:marker"
        self.a["task_id"] = "001B"
        self.ledger.perform(self.a)
        self.store = RecoveryStore(self.root / "recovery")
        self.source_hash = self.store.publish_initial(self.source)

    def assert_code(self, code, function, *args, **kwargs):
        with self.assertRaises(ContractError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def run_recovery(self, **kwargs):
        params = dict(bundle=self.bundle, store=self.store, ledger=self.ledger,
                      task_id="001B", destination="A", attempt_id="001B:AB-A",
                      authorized=True)
        params.update(kwargs)
        return durable_recover(**params)

    def test_durable_attempt_links_source_inputs_target_and_actions(self):
        out = self.run_recovery()
        self.assertEqual(out["status"], "SUCCESS")
        record = self.store.inspect_attempt("001B:AB-A")
        self.assertEqual(record["status"], "PUBLISHED")
        self.assertEqual(record["source_checkpoint_hash"], self.source_hash)
        self.assertEqual(record["source_ecid"], self.source["ecid"])
        self.assertEqual(record["target_ecid"], self.bundle.ecid("A"))
        self.assertEqual(record["input_artifact"], self.source["input_artifact"])
        self.assertEqual(record["action_keys"], ["001B:marker"])
        self.assertEqual(record["staged_checkpoint_hash"], record["published_checkpoint_hash"])

    def test_atomic_publication_exact_clean_equivalence(self):
        out = self.run_recovery()
        clean = checkpoint(self.bundle, "A", "001B", self.inputs)
        clean["draft"] = ""
        self.assertEqual(out["state"], clean)
        self.assertEqual(self.store.current("001B"), clean)
        self.assertEqual(self.source["profile"], "AB")
        self.assertEqual(self.ledger.effect_count(), 1)
        self.ledger.perform(self.a)
        self.assertEqual(self.ledger.effect_count(), 1)

    def test_failure_retains_published_source_and_attempt_is_durable(self):
        original = copy.deepcopy(self.store.current("001B"))
        out = self.run_recovery(load_ok=False)
        self.assertEqual(out["status"], "INTERNAL_FAILURE")
        self.assertEqual(self.store.current("001B"), original)
        record = self.store.inspect_attempt("001B:AB-A")
        self.assertEqual(record["status"], "FAILED")
        self.assertEqual(record["failure_code"], "INTERNAL_FAILURE")
        again = self.run_recovery()
        self.assertEqual(again["status"], "INTERNAL_FAILURE")
        self.assertEqual(self.store.current("001B"), original)

    def test_unresolved_action_blocks_attempt_creation(self):
        other = action()
        other.update(key="001B:uncertain", task_id="001B", status="UNCERTAIN")
        with action_database(self.ledger.path) as db:
            db.execute("INSERT INTO records VALUES (?,?)", (other["key"], json.dumps(other)))
        out = durable_recover(self.bundle, self.store, self.ledger, task_id="001B",
                              destination="A", attempt_id="001B:blocked", authorized=True)
        self.assertEqual(out["status"], "RECOVERY_REQUIRED")
        self.assertIsNone(self.store.inspect_attempt("001B:blocked"))
        self.assertEqual(self.store.current("001B")["profile"], "AB")

    def test_action_set_change_blocks_resume_and_retains_source(self):
        # Create only the PREPARED record using the same public primitives.
        self.store.prepare(attempt_id="001B:AB-A", source=self.source, target_profile="A",
                           target_ecid=self.bundle.ecid("A"), input_artifact=self.source["input_artifact"],
                           action_keys=self.ledger.action_keys("001B"))
        extra = action()
        extra.update(key="001B:extra", task_id="001B")
        self.ledger.perform(extra)
        out = self.run_recovery()
        self.assertEqual(out["status"], "RECOVERY_REQUIRED")
        self.assertEqual(self.store.current("001B")["profile"], "AB")
        self.assertEqual(self.store.inspect_attempt("001B:AB-A")["status"], "FAILED")

    def test_current_pointer_compare_and_swap_prevents_stale_publish(self):
        self.store.prepare(attempt_id="001B:AB-A", source=self.source, target_profile="A",
                           target_ecid=self.bundle.ecid("A"), input_artifact=self.source["input_artifact"],
                           action_keys=self.ledger.action_keys("001B"))
        target = checkpoint(self.bundle, "A", "001B", self.inputs)
        target["draft"] = ""
        self.store.stage("001B:AB-A", target)
        # Simulate an independently published source replacement without adding concurrency claims.
        alternate = copy.deepcopy(self.source)
        alternate["draft"] = "different-but-valid-source-state"
        alt_hash = checkpoint_hash(alternate)
        with recovery_database(self.store.path) as db:
            db.execute("INSERT INTO checkpoints(key,body) VALUES (?,?)", (alt_hash, json.dumps(alternate, sort_keys=True)))
            db.execute("UPDATE current SET checkpoint_hash=? WHERE task_id=?", (alt_hash, "001B"))
        self.assert_code("INCOMPATIBLE_CONFIGURATION", self.store.publish, "001B:AB-A")
        self.assertEqual(self.store.current("001B"), alternate)

    def test_staged_checkpoint_corruption_fails_closed(self):
        self.store.prepare(attempt_id="001B:AB-A", source=self.source, target_profile="A",
                           target_ecid=self.bundle.ecid("A"), input_artifact=self.source["input_artifact"],
                           action_keys=self.ledger.action_keys("001B"))
        target = checkpoint(self.bundle, "A", "001B", self.inputs)
        target["draft"] = ""
        key = self.store.stage("001B:AB-A", target)
        with recovery_database(self.store.path) as db:
            db.execute("UPDATE checkpoints SET body=? WHERE key=?", (json.dumps({"corrupt": True}), key))
        self.assert_code("VALIDATION_FAILED", self.store.staged, "001B:AB-A")
        self.assertEqual(self.store.current("001B")["profile"], "AB")

    def test_attempt_schema_semantics(self):
        out = self.run_recovery()
        r = self.store.inspect_attempt("001B:AB-A")
        self.assertEqual(validate(r, "recovery_attempt.schema.json"), r)
        broken = copy.deepcopy(r)
        broken["published_checkpoint_hash"] = None
        from nss_base.publication import attempt_record
        self.assert_code("VALIDATION_FAILED", attempt_record, broken)

    def test_process_crash_windows_preserve_or_publish_atomically(self):
        worker = Path(__file__).with_name("recovery_publication_crash_worker.py")
        for stage in ["after_prepare", "after_compute", "after_stage", "after_publish"]:
            with self.subTest(stage=stage):
                directory = self.root / stage
                result = subprocess.run([sys.executable, str(worker), str(directory), stage],
                                        capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 73, result.stderr)
                ledger = Ledger(directory / "actions")
                store = RecoveryStore(directory / "recovery")
                record = store.inspect_attempt("001B:AB-A")
                if stage in ("after_prepare", "after_compute"):
                    self.assertEqual(record["status"], "PREPARED")
                    self.assertEqual(store.current("001B")["profile"], "AB")
                elif stage == "after_stage":
                    self.assertEqual(record["status"], "STAGED")
                    self.assertEqual(store.current("001B")["profile"], "AB")
                else:
                    self.assertEqual(record["status"], "PUBLISHED")
                    self.assertEqual(store.current("001B")["profile"], "A")
                resumed = durable_recover(self.bundle, store, ledger, task_id="001B", destination="A",
                                           attempt_id="001B:AB-A", authorized=True)
                self.assertEqual(resumed["status"], "SUCCESS")
                self.assertEqual(store.current("001B")["profile"], "A")
                clean = execute(self.bundle, "A", self.bundle.artifact(self.inputs, "inputs.schema.json"))
                self.assertEqual(store.current("001B")["cache"], clean)
                # Recovery never re-executes the already committed action.
                before = ledger.effect_count()
                a = action(); a.update(key="001B:marker", task_id="001B")
                ledger.perform(a)
                self.assertEqual(ledger.effect_count(), before)

    def test_missing_recovery_database_fails_closed_when_directory_survives(self):
        self.store.path.unlink()
        marker = self.root / "recovery" / "evidence.marker"
        marker.write_text("survived", encoding="utf-8")
        self.assert_code("RECOVERY_REQUIRED", RecoveryStore, self.root / "recovery")

    def test_historical_runtime_order_is_part_of_reuse_and_identity(self):
        overlays = (Overlay("A", "a"), Overlay("B", "b"))
        profiles = (Profile("core", (), "e0"), Profile("AB", ("A", "B"), "e1"),
                    Profile("BA", ("B", "A"), "e2"))
        with self.assertRaises(ContractError) as caught:
            Catalog("c", "G", "tok", "ctx", "ov", "rt", overlays, profiles,
                    (Transition("AB", "BA", "reuse", "t"),))
        self.assertEqual(caught.exception.code, "INCOMPATIBLE_CONFIGURATION")
        c1 = Catalog("c", "G", "tok", "ctx", "ov", "rt", overlays, profiles,
                     (Transition("AB", "AB", "reuse", "t"),))
        self.assertNotEqual(c1.ecid("AB"), c1.ecid("BA"))


    def test_resume_requires_authorization_until_published(self):
        self.store.prepare(attempt_id="001B:AB-A", source=self.source, target_profile="A",
                           target_ecid=self.bundle.ecid("A"), input_artifact=self.source["input_artifact"],
                           action_keys=self.ledger.action_keys("001B"))
        out = durable_recover(self.bundle, self.store, self.ledger, task_id="001B", destination="A",
                              attempt_id="001B:AB-A", authorized=False)
        self.assertEqual(out["status"], "AUTHORIZATION_DENIED")
        self.assertEqual(self.store.inspect_attempt("001B:AB-A")["status"], "PREPARED")
        self.assertEqual(self.store.current("001B")["profile"], "AB")
        ok = self.run_recovery()
        self.assertEqual(ok["status"], "SUCCESS")

    def test_corrupt_committed_receipt_blocks_recovery(self):
        with action_database(self.ledger.path) as db:
            row = db.execute("SELECT body FROM records WHERE key=?", (self.a["key"],)).fetchone()
            value = decode(row[0])
            value["receipt"] = "0" * 64
            db.execute("UPDATE records SET body=? WHERE key=?", (json.dumps(value), self.a["key"]))
        out = durable_recover(self.bundle, self.store, self.ledger, task_id="001B", destination="A",
                              attempt_id="001B:bad-receipt", authorized=True)
        self.assertEqual(out["status"], "VALIDATION_FAILED")
        self.assertIsNone(self.store.inspect_attempt("001B:bad-receipt"))
        self.assertEqual(self.store.current("001B")["profile"], "AB")

    def test_end_to_end_001b_demo(self):
        report = run(self.root / "demo001b")
        self.assertTrue(report["exact_match"])
        self.assertEqual(report["current_profile"], "A")
        self.assertEqual(report["attempt_status"], "PUBLISHED")

    def prepare_staged(self):
        self.store.prepare(attempt_id="001B:AB-A", source=self.source, target_profile="A",
            target_ecid=self.bundle.ecid("A"), input_artifact=self.source["input_artifact"],
            action_keys=self.ledger.action_keys("001B"))
        target = checkpoint(self.bundle, "A", "001B", self.inputs); target["draft"] = ""
        self.store.stage("001B:AB-A", target)

    def test_staged_resume_load_failure_preserves_source(self):
        self.prepare_staged()
        out = self.run_recovery(load_ok=False)
        self.assertEqual(out["status"], "INTERNAL_FAILURE")
        self.assertEqual(self.store.current("001B"), self.source)
        self.assertEqual(self.store.inspect_attempt("001B:AB-A")["status"], "FAILED")

    def test_same_profile_publication_reports_no_replay(self):
        self.run_recovery()
        out = self.run_recovery(attempt_id="001B:A-A")
        self.assertEqual(out["status"], "SUCCESS")
        self.assertFalse(out["replayed"])

    def test_old_published_attempt_remains_readable_after_next_publication(self):
        first = self.run_recovery()
        next_result = self.run_recovery(attempt_id="001B:A-core", destination="core")
        self.assertEqual(next_result["status"], "SUCCESS")
        old = self.run_recovery(authorized=False)
        self.assertEqual(old["status"], "SUCCESS")
        self.assertEqual(old["state"], first["state"])
        self.assertFalse(old["replayed"])
        self.assertEqual(self.store.current("001B")["profile"], "core")

    def test_missing_store_returns_typed_failure_without_fabricated_state(self):
        self.store.path.unlink()
        out = self.run_recovery()
        self.assertEqual(out["status"], "RECOVERY_REQUIRED")
        self.assertIsNone(out["state"])

    def test_current_pointer_cannot_reference_another_task(self):
        other = dict(self.source, task_id="other")
        key = self.store.publish_initial(other)
        with recovery_database(self.store.path) as db:
            db.execute("UPDATE current SET checkpoint_hash=? WHERE task_id=?", (key,"001B"))
        self.assert_code("VALIDATION_FAILED", self.store.current, "001B")
        self.assert_code("VALIDATION_FAILED", self.store.current_hash, "001B")

    def test_prepare_cannot_substitute_portable_inputs(self):
        bad = dict(self.inputs, sha256="0"*64)
        self.assert_code("INCOMPATIBLE_CONFIGURATION", self.store.prepare,
            attempt_id="bad", source=self.source, target_profile="A",
            target_ecid=self.bundle.ecid("A"), input_artifact=bad, action_keys=[])


if __name__ == "__main__":
    unittest.main()
