#!/usr/bin/env python3
"""Convenience runner. No installation, download, existing-directory overwrite or network."""
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import uuid
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=('checks','demo','preflight'))
    args=p.parse_args()
    if args.mode=='checks':
        return subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_foundation*.py','-v'],cwd=ROOT).returncode
    if args.mode=='preflight':
        return subprocess.run([sys.executable,'-m','nss_base','research','--preflight'],cwd=ROOT).returncode
    # Keep generated data outside the release tree so its checksum manifest remains meaningful.
    output=ROOT.parent/'NSS_Run_Output'/('foundation-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6])
    result=subprocess.run([sys.executable,'-m','nss_base','demo','--output',str(output)],cwd=ROOT)
    if result.returncode==0:print('Saved local test output:',output)
    return result.returncode


if __name__=='__main__':raise SystemExit(main())
