"""Continue a worker after infrastructure interruption, never select by score."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_empty.train import train
from nbr01_empty.util import sha
for seed in range(301,306):
 for kind in ('replay','contract','local_empty'):
  stem=f'{kind}_rep{seed}_seed{seed+300}'
  record=ROOT/'evidence/main'/f'{stem}.json';checkpoint=record.with_suffix('.safetensors')
  if record.exists():
   x=json.loads(record.read_text());assert sha(checkpoint)==x['checkpoint_sha256'];print('PRESERVED',stem,flush=True)
  else:train(ROOT,ROOT/'evidence/main',kind,seed,seed+300)
print('ALL_TRAINING_COMPLETE',flush=True)
