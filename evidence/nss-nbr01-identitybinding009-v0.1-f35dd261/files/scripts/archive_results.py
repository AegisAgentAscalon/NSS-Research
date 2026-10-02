"""Lossless archival only: unchanged NPY entries, uncompressed ZIP then XZ.
Avoid nested DEFLATE obscuring long duplicate array sequences. NOT quantization.
"""
from pathlib import Path
import sys,json,zipfile,lzma,tempfile,hashlib,shutil,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr009.common import ROOT,sha,dump,utc

def entries_digest(path):
 h=hashlib.sha256()
 with zipfile.ZipFile(path) as z:
  for n in z.namelist():
   h.update(n.encode());h.update(hashlib.sha256(z.read(n)).digest())
 return h.hexdigest()

rows=[]
for path in sorted((ROOT/'evidence/results').glob('*.npz')):
 start=time.perf_counter();archive=Path(str(path)+'.xz');original_sha=sha(path)
 with tempfile.TemporaryDirectory(prefix='nbr009_archive_') as td:
  stored=Path(td)/path.name
  with zipfile.ZipFile(path) as zin,zipfile.ZipFile(stored,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as zout:
   for name in zin.namelist():zout.writestr(name,zin.read(name))
  digest=entries_digest(path)
  if entries_digest(stored)!=digest:raise AssertionError('Repacking changed a numerical array')
  with open(stored,'rb') as src,lzma.open(archive,'wb',filters=[{'id':lzma.FILTER_LZMA2,'preset':1,'dict_size':16*1024*1024}]) as out:shutil.copyfileobj(src,out,1024*1024)
  decoded=Path(td)/'decoded.npz'
  with lzma.open(archive,'rb') as src,open(decoded,'wb') as out:shutil.copyfileobj(src,out,1024*1024)
  if sha(decoded)!=sha(stored):raise AssertionError('Archive did not decode exactly')
  rec={'schema':'nbr009-evidence-archive-v1','format':'Unchanged NPY entries in ZIP_STORED NPZ, losslessly XZ-compressed','source':path.name,'original_container_sha256':original_sha,'decoded_container_sha256':sha(stored),'entries_digest':digest,'archive_sha256':sha(archive),'original_bytes':path.stat().st_size,'decoded_bytes':stored.stat().st_size,'archive_bytes':archive.stat().st_size,'seconds':time.perf_counter()-start,'utc':utc()}
  dump(path.with_suffix('.archive.json'),rec);rows.append(rec)
 # Original model/result arrays preserved exactly, but the storage container changed.
 path.unlink();print(path.name,rec['original_bytes'],rec['archive_bytes'],flush=True)
dump(ROOT/'evidence/ARCHIVAL.json',{'status':'LOSSLESS_ARRAYS_VERIFIED','model_or_learning_state_quantized':False,'files':rows,'utc':utc()})
