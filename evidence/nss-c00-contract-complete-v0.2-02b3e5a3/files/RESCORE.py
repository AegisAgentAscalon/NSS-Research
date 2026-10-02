from pathlib import Path
import argparse,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parent
if a.out.exists():raise SystemExit('Please supply a new output directory.')
subprocess.run([sys.executable,str(root/'source/check.py'),str(root/'inputs/primary'),str(root/'raw/primary'),str(a.out)],check=True)
for source in (root/'results/primary').iterdir():
    if source.read_bytes()!=(a.out/source.name).read_bytes():raise SystemExit('Rescore mismatch: '+source.name)
print('All retained independent result files reproduced exactly. No neural calls or updates.')
