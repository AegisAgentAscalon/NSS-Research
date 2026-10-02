from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/"reference"/"parent008"
for p in (PARENT,PARENT/"reference"):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
