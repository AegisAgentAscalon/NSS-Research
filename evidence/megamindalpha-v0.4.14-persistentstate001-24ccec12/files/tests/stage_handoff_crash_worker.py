"""Fresh-process fault injector for a single already-initialized stage task."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nss_base.artifacts import Bundle
from nss_base.ledger import Ledger
from nss_base.publication import RecoveryStore
from nss_base.serialization import read_json
from nss_base.stage_handoff import handoff_stage
root=Path(sys.argv[1])
r=handoff_stage(Bundle(root/'fixture/manifest.json'),RecoveryStore(root/'recovery'),
    Ledger(root/'actions'),task_id='stage-001',destination='A',attempt_id='h1',
    request=read_json(root/'request.json'),authorized=True,crash_at=sys.argv[2])
print(r)
raise SystemExit(1)
