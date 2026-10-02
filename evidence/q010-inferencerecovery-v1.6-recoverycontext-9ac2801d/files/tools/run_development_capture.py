import argparse,json,torch,traceback
from q010c.protocol import ROOT
from q010c.development import development_readers
from q010c.evaluate import capture_seed,write_json
from q010v.verify import verify_capture
p=argparse.ArgumentParser();p.add_argument('--attempt',required=True);p.add_argument('--seed',type=int,default=91401);a=p.parse_args()
torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
root=ROOT/'results'/a.attempt;root.mkdir(exist_ok=False)
write_json(root/'SCOPE.json',{'purpose':'infrastructure repair development validation','main':False,'new_optimizer_updates':0,'seed':a.seed,'conditions':64,'cases_per_nonlifecycle_cell':4,'case_indices':[0,1,64,65],'complete_durability_horizon':1024,'reader_roster':'two inherited controls, three exact retained40-update development weights, exact owner','not_a_main_fit_or_scientific_qualification':True})
try:
 m,ids=development_readers();capture_seed(a.seed,m,ids,root/'capture',split='development',development_count=4)
 verify_capture(root/'capture',root/'independent_score')
except BaseException as e:
 write_json(root/'FAILURE.json',{'error':repr(e),'traceback':traceback.format_exc()});raise
