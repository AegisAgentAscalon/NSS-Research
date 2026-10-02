#!/usr/bin/env python3
"""Verify and extract one original study into a NEW directory; execute nothing.
Example: python tools/extract_study.py SH02 --destination /path/to/new-folder
The complete original study root is retained beneath that directory. The compact
review edition has no original ZIPs; use the full consolidation for extraction.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys
import zipfile
sys.dont_write_bytecode = True
from verify_consolidation import safe_relative, verify_original


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study', choices=['SH01', 'SH02', 'SC01', 'SC02', 'CAP01', 'CAP02'])
    parser.add_argument('--destination', required=True, type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        audit = json.loads((root / 'verification/INPUT_AUDIT.json').read_text(encoding='utf-8'))
        expected = next(r for r in audit['studies'] if r['study'] == args.study)
        archive = root / expected['archive']
        verification = verify_original(archive, expected)
        dest = args.destination.expanduser().absolute()
        if dest.exists() or dest.is_symlink():
            raise FileExistsError(f'Refusing to overwrite an existing destination: {dest}')
        dest.mkdir(parents=True, exist_ok=False)
        base = dest.resolve()
        count = 0
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                rel = safe_relative(info.filename)
                target = base.joinpath(*rel.parts)
                if not target.resolve().is_relative_to(base):
                    raise ValueError(f'Unsafe extraction path: {info.filename}')
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(info) as source, target.open('xb') as out:
                        shutil.copyfileobj(source, out, length=1024 * 1024)
                    count += 1
        print(json.dumps({'status': 'EXTRACTED_NO_EXECUTION', 'study': args.study,
                          'destination': str(base), 'files': count, 'verification': verification}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, StopIteration, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'FAILED', 'error_type': type(exc).__name__, 'error': str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
