from pathlib import Path
import sys,json,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_empty.train import train
from nbr01_empty.util import write_json
old=json.loads((ROOT/'evidence/main/contract_rep303_seed603.json').read_text())
with tempfile.TemporaryDirectory(prefix='nbr004-training-replay-') as d:
 new=train(ROOT,Path(d),'contract',303,603)
 keys=['training_data_digest','initial_digest','final_digest','checkpoint_sha256','changed_parameter_elements','steps','supervised_event_presentations']
 checks={k:old[k]==new[k] for k in keys}
 if not all(checks.values()):raise RuntimeError(checks)
 write_json(ROOT/'evidence/TRAINING_REPRODUCTION.json',{'status':'PASS','fresh_interpreter':True,'main_run':'contract_rep303_seed603','checks':checks,'new_run':new,'not_an_additional_seed':True})
print('TRAINING REPRODUCED')
