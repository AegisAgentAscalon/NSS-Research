"""Explicit os._exit fault injector, test-only; requests cannot set fault points."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from nss_base.dataset_store import DatasetSnapshots
from nss_base.experience_store import ExperienceArchive
from nss_base.serialization import read_json
root=Path(sys.argv[1]);point=sys.argv[2]
result=DatasetSnapshots(root/'snapshots').build(read_json(root/'request.json'),
    archive=ExperienceArchive(root/'archive'),tokenizer_path=root/'tokenizer.json',fault_at=point)
print(json.dumps(result))
raise SystemExit(3)  # A requested crash must terminate with the explicit fault code.
