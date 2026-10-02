"""Run with python -m nss_base.experiment001a; temporary mock storage by default."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from .artifacts import Bundle
from .ledger import Ledger
from .recovery import checkpoint, recover, execute
from .serialization import read_json

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "recovery001a"


def action():
    return dict(schema_version=1, key="001A:marker", task_id="001A",
        payload=dict(operation="append_marker", value="one committed effect"),
        status="PENDING", receipt=None)


def run(directory):
    bundle = Bundle(FIXTURE / "manifest.json")
    inputs = read_json(FIXTURE / "input_ref.json")
    ledger = Ledger(directory)
    ledger.perform(action())
    source = checkpoint(bundle, "AB", "001A", inputs)
    ledger = Ledger(directory)  # Real close/reopen of durable SQLite records.
    result = recover(bundle, source, "A", ledger, authorized=True)
    ledger.perform(action())  # A replayed request must skip the committed effect.
    clean = execute(bundle, "A", bundle.artifact(inputs, "inputs.schema.json"))
    report = dict(status=result.status, source_AB=source["cache"], recovered_A=result.state["cache"],
        clean_A=clean, exact_match=result.state["cache"] == clean,
        replayed=result.replayed, effect_count=ledger.effect_count(),
        scope="Integer simulator and local mock effects only; no neural execution")
    if result.status != "SUCCESS" or not report["exact_match"] or report["effect_count"] != 1:
        raise RuntimeError("Experiment failed")
    return report


if __name__ == "__main__":
    with TemporaryDirectory(prefix="nss-001a-") as directory:
        print(json.dumps(run(directory), indent=2))
