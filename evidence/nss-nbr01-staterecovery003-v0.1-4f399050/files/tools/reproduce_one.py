from pathlib import Path
import argparse,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
cmd=[sys.executable,str(root/'run.py'),'train','--kind','recurrent','--rep-seed','303','--seed','503','--steps','1800','--output',str(a.output)]
subprocess.run(cmd,cwd=root,check=True)
original=json.loads((root/'evidence/main/recurrent_rep303_seed503.json').read_text())
new=json.loads((a.output/'recurrent_rep303_seed503.json').read_text())
for k in ['training_data_digest','initial_digest','final_digest','checkpoint_sha256']:
    if original[k]!=new[k]:raise SystemExit(f'Reproduction mismatch: {k}')
print('PASS: full training data and final checkpoint match.')
