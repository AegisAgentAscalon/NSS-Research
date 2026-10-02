"""Real subprocess termination at a declared local evaluation crash boundary."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.dataset_store import DatasetSnapshots
from nss_base.evaluation_store import EvaluationRuns
from nss_base.experience_store import ExperienceArchive
from nss_base.serialization import read_json
root=Path(sys.argv[1]);kw={'root':root/'inputs'}
if (root/'archive').exists():
    kw.update(snapshots=DatasetSnapshots(root/'snapshots'),archive=ExperienceArchive(root/'archive'),tokenizer_path=root/'tokenizer.json')
result=EvaluationRuns(root/'evaluations').execute(read_json(root/'plan.json'),fault_at=sys.argv[2],**kw)
print(result);raise SystemExit(3)
