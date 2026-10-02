#!/usr/bin/env python3
"""Verify the complete CM-01 delivery without loading models or running experiments."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def verify(root:Path)->dict:
    root=root.resolve(strict=True);manifest=json.loads((root/'MANIFEST.json').read_text())
    for item in manifest['files']:
        rel=Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe manifest path')
        p=root/rel
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):raise ValueError('Missing/unsafe member '+str(rel))
        if p.stat().st_size!=item['bytes']:raise ValueError('Size mismatch '+str(rel))
        with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
        if h!=item['sha256']:raise ValueError('Hash mismatch '+str(rel))
    c=json.loads((root/'audit/COMPLETENESS.json').read_text())
    if not all(c['checks'].values()) or c['total_model_forward_calls_including_replay']>30816:raise ValueError('Study completeness/cap receipt failed')
    return {'status':'PASS_COMPLETE_NEW_CM01_PACKAGE','files_verified':len(manifest['files']),'old_baseline_models_included':False,'new_model_calls':0}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args()
    print(json.dumps(verify(a.root),indent=2))
