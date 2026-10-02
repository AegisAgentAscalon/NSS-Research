from pathlib import Path
import sys,argparse,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import *
from nbr009.train import fit
from nbr009.context import calibrate
p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True);a=p.parse_args();a.folder.mkdir(parents=True,exist_ok=True);setup()
ref=ROOT/'checkpoints/binder_near_1101.safetensors';out=a.folder/ref.name
rec=fit(1,'near',1101,1200,out);orig=json.loads(ref.with_suffix('.json').read_text())
assert sha(out)==sha(ref)
assert rec['data_checks']==orig['data_checks']
assert [v['loss'] for v in rec['history']]==[v['loss'] for v in orig['history']]
cut=calibrate(1,a.folder/'cue_calibration_1.npz')
assert cut==json.loads((ROOT/'checkpoints/cue_calibration_1.json').read_text())['cuts']
with np.load(ROOT/'checkpoints/cue_calibration_1.npz',allow_pickle=False) as x,np.load(a.folder/'cue_calibration_1.npz',allow_pickle=False) as y:
    assert x.files==y.files
    for k in x.files:assert np.array_equal(x[k],y[k])
dump(a.folder/'REPRODUCTION.json',{'status':'PASS','fresh_interpreter':True,'pair':1,'kind':'near','steps':1200,'checkpoint_sha256':sha(out),'identical_checkpoint_bytes':True,'calibration_arrays_identical':True,'utc':utc()});print('Training and calibration reproduction PASS')
