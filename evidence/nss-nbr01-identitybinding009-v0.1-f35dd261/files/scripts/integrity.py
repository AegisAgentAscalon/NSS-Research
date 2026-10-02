"""Read-only SHA256 verification for the immutable release; standard library only."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def verify() -> dict:
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
    failed = []
    for relative, expected in manifest['files'].items():
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            failed.append(relative)
    if failed:
        raise RuntimeError('Release file mismatch: ' + ', '.join(failed))
    result = {'status': 'PASS', 'manifest_files': len(manifest['files']),
              'manifest_sha256': digest(ROOT / 'MANIFEST.json')}
    return result

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
