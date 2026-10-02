"""Experiment 001B: durable recovery-attempt staging and atomic checkpoint publication."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from .artifacts import Bundle
from .experiment001a import FIXTURE, action
from .ledger import Ledger
from .publication import RecoveryStore, durable_recover
from .recovery import checkpoint, execute
from .serialization import read_json


def run(directory):
    directory = Path(directory)
    bundle = Bundle(FIXTURE / "manifest.json")
    inputs = read_json(FIXTURE / "input_ref.json")
    ledger = Ledger(directory / "actions")

    source = checkpoint(bundle, "AB", "001B", inputs)
    store = RecoveryStore(directory / "recovery")
    source_hash = store.publish_initial(source)

    # Use a task-local committed action for 001B so the attempt binds it explicitly.
    a = action()
    a["key"] = "001B:marker"
    a["task_id"] = "001B"
    ledger.perform(a)

    result = durable_recover(bundle, store, ledger, task_id="001B", destination="A",
                             attempt_id="001B:AB-A", authorized=True)
    clean = execute(bundle, "A", bundle.artifact(inputs, "inputs.schema.json"))
    # Re-submitting the committed action must not create another effect.
    ledger.perform(a)
    report = dict(
        status=result["status"],
        source_hash=source_hash,
        source_AB=source["cache"],
        recovered_A=result["state"]["cache"],
        clean_A=clean,
        exact_match=result["state"]["cache"] == clean,
        current_profile=store.current("001B")["profile"],
        attempt_status=store.inspect_attempt("001B:AB-A")["status"],
        effect_count=ledger.effect_count(),
        action_keys=store.inspect_attempt("001B:AB-A")["action_keys"],
        scope="Durable local integer recovery publication and local mock effects only; no neural execution",
    )
    if (report["status"] != "SUCCESS" or not report["exact_match"] or
            report["current_profile"] != "A" or report["attempt_status"] != "PUBLISHED" or
            report["effect_count"] != 1):
        raise RuntimeError("Experiment 001B failed")
    return report


if __name__ == "__main__":
    with TemporaryDirectory(prefix="nss-001b-") as directory:
        print(json.dumps(run(directory), indent=2))
