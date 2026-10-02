#!/usr/bin/env python3
"""Verify documentary package identities only; does not execute research code."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def safe_path(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'Unsafe manifest path: {name!r}')
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError(f'Unexpected file target: {name!r}')
    return path

def main() -> int:
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    failures: list[str] = []
    entries = manifest['files']
    if len({item['path'] for item in entries}) != len(entries):
        failures.append('Duplicate manifest paths')
    for item in entries:
        path = safe_path(root, item['path'])
        if not path.is_file():
            failures.append(f"Missing: {item['path']}")
        elif path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
            failures.append(f"Identity mismatch: {item['path']}")
    sources = json.loads((root / 'SOURCE_INDEX.json').read_text(encoding='utf-8'))['sources']
    for item in sources:
        path = safe_path(root, item['package_path'])
        if not path.is_file() or digest(path) != item['sha256'] or path.stat().st_size != item['bytes']:
            failures.append(f"Source-snapshot mismatch: {item['id']}")
    result = {
        'status': 'PASS' if not failures else 'FAIL',
        'kind': 'DOCUMENT_BYTES_ONLY',
        'manifest_payloads': len(entries),
        'source_snapshots': len(sources),
        'failures': failures,
        'scientific_results_reproduced': False,
        'historical_source_code_executed': False,
    }
    print(json.dumps(result, indent=2))
    return 1 if failures else 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Document verification failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
