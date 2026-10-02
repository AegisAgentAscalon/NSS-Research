from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import ROOT,sha,dump
from nbr008.prepare import fit,calibrate
out=ROOT/'evidence/reproduction/training';out.mkdir(parents=True,exist_ok=True)
m,fitinfo=fit(1001,1200,out);cal=calibrate(1001,m,out,4096)
old=json.loads((ROOT/'checkpoints/match_head_1001.json').read_text());oldcal=json.loads((ROOT/'checkpoints/calibration_1001.json').read_text())
assert sha(out/'match_head_1001.safetensors')==sha(ROOT/'checkpoints/match_head_1001.safetensors')
assert old['batch_fingerprints']==fitinfo['batch_fingerprints'];assert old['history']==fitinfo['history'];assert oldcal==cal
res={'status':'PASS','seed':1001,'optimizer_steps':1200,'checkpoint_identical':True,'history_and_batch_fingerprints_identical':True,'calibration_identical':True,'seconds':fitinfo['seconds'],'sha256':sha(out/'match_head_1001.safetensors')}
dump(ROOT/'evidence/TRAINING_REPRODUCTION.json',res);print(res)
