import json,torch
from q010c.protocol import ROOT,sha,build_criteria
from q010c.train import zero_start_check
from q010c.evaluate import write_json

torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
p=ROOT/'protocol/REPAIR_SCOPE.md'
r=zero_start_check(sha(p));write_json(ROOT/'results/ZERO_START_RUNTIME.json',r)
c=build_criteria();write_json(ROOT/'results/CRITERIA_SERIALIZATION_DRAFT.json',{'status':'DEVELOPMENT_SERIALIZATION_CHECK_ONLY_NOT_PREMAIN_FREEZE','criteria':c})
print(json.dumps({'status':r['status'],'factories':len(r['rows']),'updates':sum(x['actual_updates'] for x in r['rows']),'criteria_cells':len(c['conditions'])}))
