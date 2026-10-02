"""Process-crash injector for Recovery Experiment 001B."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nss_base.artifacts import Bundle
from nss_base.experiment001a import FIXTURE, action
from nss_base.ledger import Ledger
from nss_base.publication import RecoveryStore, durable_recover
from nss_base.recovery import checkpoint
from nss_base.serialization import read_json

root = Path(sys.argv[1])
stage = sys.argv[2]
bundle = Bundle(FIXTURE / "manifest.json")
inputs = read_json(FIXTURE / "input_ref.json")
ledger = Ledger(root / "actions")
a = action()
a["key"] = "001B:marker"
a["task_id"] = "001B"
ledger.perform(a)
source = checkpoint(bundle, "AB", "001B", inputs)
store = RecoveryStore(root / "recovery")
store.publish_initial(source)
durable_recover(bundle, store, ledger, task_id="001B", destination="A",
                attempt_id="001B:AB-A", authorized=True, crash_at=stage)
raise SystemExit("crash hook did not terminate process")
