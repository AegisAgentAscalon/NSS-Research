from pathlib import Path
from contextlib import contextmanager
import tempfile,lzma,shutil,json,hashlib,zipfile

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

@contextmanager
def materialize(path):
 """Yield an NPZ path for either direct or verified lossless archived evidence."""
 path=Path(path)
 if path.exists() and path.suffix=='.npz':yield path;return
 archive=path if path.name.endswith('.npz.xz') else Path(str(path)+'.xz')
 base=Path(str(archive)[:-3]);receipt=json.loads(base.with_suffix('.archive.json').read_text())
 if sha(archive)!=receipt['archive_sha256']:raise ValueError('Damaged archive '+str(archive))
 with tempfile.TemporaryDirectory(prefix='nbr009_evidence_') as td:
  out=Path(td)/base.name
  with lzma.open(archive,'rb') as src,open(out,'wb') as dst:shutil.copyfileobj(src,dst,1024*1024)
  if sha(out)!=receipt['decoded_container_sha256']:raise ValueError('Decoded evidence hash mismatch')
  shutil.copy2(base.with_suffix('.json'),out.with_suffix('.json'))
  yield out
