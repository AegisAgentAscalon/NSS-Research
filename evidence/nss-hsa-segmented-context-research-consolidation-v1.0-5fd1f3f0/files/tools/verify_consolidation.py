#!/usr/bin/env python3
"""Verify bytes only. Never deserialize models, import study code, or run experiments.

Run from anywhere: python tools/verify_consolidation.py [--root PATH] [--deep]
Exit 0: requested checks pass. Exit 1: error/mismatch. Exit 2: compact edition
passes its payload checks but --deep cannot run because originals are omitted.
Hashes detect changes relative to the included manifest, not publisher identity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe_relative(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    if not name or '\\' in name or p.is_absolute() or '..' in p.parts or ':' in name:
        raise ValueError(f'Unsafe relative name: {name!r}')
    return p


def verify_original(path: Path, expected: dict) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f'Original archive unavailable: {path.name}')
    if path.stat().st_size != expected['bytes'] or sha256_file(path) != expected['sha256']:
        raise ValueError(f'Original archive bytes/hash mismatch: {path.name}')
    root = path.stem + '/'
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)):
            raise ValueError(f'Duplicate ZIP names: {path.name}')
        for info in infos:
            safe_relative(info.filename)
            if not info.filename.startswith(root):
                raise ValueError(f'Member outside original root: {info.filename}')
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError(f'Symlink member: {info.filename}')
        bad = z.testzip()
        if bad is not None:
            raise ValueError(f'CRC failure: {bad}')
        manifest = json.loads(z.read(root + 'MANIFEST.json'))
        entries = manifest['files']
        actual = {i.filename[len(root):] for i in infos if not i.is_dir()}
        if actual != set(entries) | {'MANIFEST.json'}:
            raise ValueError(f'Original manifest membership mismatch: {path.name}')
        for name, record in entries.items():
            safe_relative(name)
            data = z.read(root + name)
            if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError(f'Original payload mismatch: {path.name}::{name}')
    return {'study': expected['study'], 'archive': path.name,
            'payloads_verified': len(entries), 'crc_pass': True,
            'archive_sha256': expected['sha256']}


def verify_outer(root: Path) -> dict:
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    entries = manifest['files']
    actual = set()
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Unexpected symbolic link: {path}')
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    declared = set(entries) | {'MANIFEST.json'}
    if actual != declared:
        raise ValueError(f'Outer file-set mismatch; missing={sorted(declared-actual)}, extra={sorted(actual-declared)}')
    for name, record in entries.items():
        relative = safe_relative(name)
        path = root.joinpath(*relative.parts)
        if path.stat().st_size != record['bytes'] or sha256_file(path) != record['sha256']:
            raise ValueError(f'Consolidation payload mismatch: {name}')
    catalog = json.loads((root / 'indexes/SOURCE_CATALOG.json').read_text(encoding='utf-8'))
    for item in catalog:
        name = item['path']
        relative = safe_relative(name)
        path = root.joinpath(*relative.parts)
        if (not path.is_file() or path.stat().st_size != item['bytes']
                or sha256_file(path) != item['sha256']):
            raise ValueError(f'Source catalog target unavailable or mismatched: {name}')
    return {'edition': manifest['edition'], 'outer_payloads_verified': len(entries),
            'source_catalog_entries_verified': len(catalog),
            'outer_byte_integrity_pass': True, 'scientific_execution': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--deep', action='store_true', help='Also check original ZIP CRCs and every inner manifest entry.')
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        result = verify_outer(root)
        if args.deep:
            audit = json.loads((root / 'verification/INPUT_AUDIT.json').read_text(encoding='utf-8'))
            missing = [r['study'] for r in audit['studies'] if not (root / r['archive']).is_file()]
            if missing:
                result['deep_status'] = 'ORIGINAL_ARCHIVES_NOT_INCLUDED'
                result['unavailable_studies'] = missing
                print(json.dumps(result, indent=2))
                return 2
            result['original_archives'] = [verify_original(root / r['archive'], r) for r in audit['studies']]
            result['original_payloads_verified'] = sum(r['payloads_verified'] for r in result['original_archives'])
            result['deep_status'] = 'PASS'
        else:
            result['deep_status'] = 'NOT_REQUESTED'
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'FAILED', 'error_type': type(exc).__name__, 'error': str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
