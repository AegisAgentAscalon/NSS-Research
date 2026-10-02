#!/usr/bin/env python3
"""Recompute historical self-authored toy metrics; never grant current data use."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.neural_contracts import read_document
from nss_base.neuralprobe001 import verify_numerics

def main():
    path=ROOT/'docs/audits/neuralprobe001/confirmation_report.json'
    result=verify_numerics(read_document(path),None,current=False)
    print(result)
    return 0
if __name__=='__main__':raise SystemExit(main())
