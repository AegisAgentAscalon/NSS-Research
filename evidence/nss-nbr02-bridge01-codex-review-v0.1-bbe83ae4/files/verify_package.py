"""Verify tracked BRIDGE01 files without loading models or executing experiments.

Run before using an extracted package. After a demo, extra generated files are
reported but permitted unless --strict is requested. Hashes detect corruption,
not an attacker who can replace the manifest and its checksum together.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def verify(root: Path, strict: bool = False) -> dict:
    root = root.resolve()
    manifest_bytes = (root / 'MANIFEST.json').read_bytes()
    expected = (root / 'MANIFEST.sha256').read_text().split()[0]
    if hashlib.sha256(manifest_bytes).hexdigest() != expected:
        raise ValueError('Manifest checksum mismatch')
    manifest = json.loads(manifest_bytes)
    tracked = set()
    checked_bytes = 0
    for item in manifest['files']:
        rel = PurePosixPath(item['path'])
        if rel.is_absolute() or '..' in rel.parts or str(rel) in tracked:
            raise ValueError('Unsafe or duplicate manifest member')
        tracked.add(str(rel))
        path = root.joinpath(*rel.parts)
        if not path.resolve().is_relative_to(root):
            raise ValueError('Member escapes root')
        data = path.read_bytes()
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f'Payload mismatch: {rel}')
        checked_bytes += len(data)
    extras = sorted(str(p.relative_to(root)).replace('\\','/') for p in root.rglob('*')
                    if p.is_file() and str(p.relative_to(root)).replace('\\','/') not in
                    tracked | {'MANIFEST.json', 'MANIFEST.sha256'}
                    and '__pycache__' not in p.parts and p.suffix != '.pyc')
    if strict and extras:
        raise ValueError(f'Unlisted files: {extras[:8]}')
    return {'status':'PASS', 'payloads':len(tracked), 'payload_bytes':checked_bytes,
            'extra_files':extras, 'models_loaded':0, 'optimizer_applications':0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.root, args.strict), indent=2))
