#!/usr/bin/env python3
"""Verify release bytes; this is integrity checking, NOT signature authentication."""
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    issues=[];seen=set()
    for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
        digest,rel=line.split('  ',1)
        p=(ROOT/rel).resolve()
        if not p.is_relative_to(ROOT) or rel in seen:
            issues.append('Unsafe/duplicate manifest path: '+rel);continue
        seen.add(rel)
        if not p.is_file() or sha256(p.read_bytes()).hexdigest()!=digest:
            issues.append('Missing/mismatched: '+rel)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and '.git' not in p.parts
            and p.suffix!='.pyc' and p.name!='MANIFEST.sha256'}
    # A retained historical manifest is intentionally covered like any other file.
    actual.update(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('MANIFEST.sha256') if p!=ROOT/'MANIFEST.sha256')
    for extra in sorted(actual-seen):issues.append('Unlisted file: '+extra)
    print('\n'.join(issues) if issues else f'PASS: {len(seen)} release files match SHA-256 manifest.')
    return bool(issues)

if __name__=='__main__':raise SystemExit(main())
