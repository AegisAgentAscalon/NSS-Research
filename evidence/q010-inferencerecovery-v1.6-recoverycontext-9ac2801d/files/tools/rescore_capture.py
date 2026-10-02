import argparse,torch
from pathlib import Path
from q010v.verify import verify_capture
p=argparse.ArgumentParser();p.add_argument('capture',type=Path);p.add_argument('output',type=Path);a=p.parse_args();torch.set_num_threads(1);torch.set_num_interop_threads(1);verify_capture(a.capture,a.output)
