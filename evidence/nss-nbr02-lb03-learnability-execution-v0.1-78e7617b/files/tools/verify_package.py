"""Read-only archive/file integrity check. Does not load a neural model."""
from pathlib import Path,PurePosixPath
import hashlib,json,sys,zipfile

def sha_file(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def verify(path):
 path=Path(path)
 if path.is_file():
  with zipfile.ZipFile(path)as z:
   if z.testzip() is not None:raise ValueError('ZIP_CRC')
   names=z.namelist()
   if len(names)!=len(set(names)):raise ValueError('DUPLICATE_MEMBER')
   mf=[n for n in names if n.endswith('/MANIFEST.json') and n.count('/')==1]
   if len(mf)!=1:raise ValueError('TOP_MANIFEST')
   prefix=mf[0].rsplit('/',1)[0]+'/';raw=z.read(mf[0]);d=json.loads(raw)
   expected={prefix+x['path']for x in d['files']}|{mf[0],prefix+'MANIFEST.sha256'}
   if {x for x in names if not x.endswith('/')}!=expected:raise ValueError('MEMBERSHIP')
   if z.read(prefix+'MANIFEST.sha256').decode().split()[0]!=hashlib.sha256(raw).hexdigest():raise ValueError('MANIFEST_SHA')
   for r in d['files']:
    if PurePosixPath(r['path']).is_absolute() or '..'in PurePosixPath(r['path']).parts:raise ValueError('UNSAFE_PATH')
    h=hashlib.sha256();size=0
    with z.open(prefix+r['path'])as f:
     for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk);size+=len(chunk)
    if h.hexdigest()!=r['sha256']or size!=r['bytes']:raise ValueError(r['path'])
 else:
  raw=(path/'MANIFEST.json').read_bytes();d=json.loads(raw)
  if (path/'MANIFEST.sha256').read_text().split()[0]!=hashlib.sha256(raw).hexdigest():raise ValueError('MANIFEST_SHA')
  for r in d['files']:
   p=path/r['path']
   if not p.is_file()or p.stat().st_size!=r['bytes']or sha_file(p)!=r['sha256']:raise ValueError(r['path'])
 print(json.dumps({'status':'PASS','payloads':len(d['files']),'scope':'Bytes/membership against supplied manifest, not external authentication or scientific replication.'}))
if __name__=='__main__':verify(sys.argv[1]if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
