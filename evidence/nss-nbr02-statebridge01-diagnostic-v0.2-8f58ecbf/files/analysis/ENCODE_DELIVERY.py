"""Lossless storage-only NPZ envelope coding. Checks exact NPZ byte reconstruction."""
from pathlib import Path
import numpy as np,hashlib,io,json,lzma,struct,time
root=Path(__file__).resolve().parents[1];target=root/'delivery/arrays.xz';entries=[];start=time.time()
# 32MiB LZMA dictionary; no lossy numeric conversion. Original/replay aliases separate.
with lzma.open(target,'wb',format=lzma.FORMAT_XZ,filters=[{'id':lzma.FILTER_LZMA2,'preset':6,'dict_size':32*1024*1024}]) as out:
 out.write(b'NSS_NPZ_ENVELOPE_V1\n')
 for p in sorted((root/'primary').rglob('*.npz')):
  raw=p.read_bytes()
  with np.load(io.BytesIO(raw),allow_pickle=False) as z:a={k:z[k] for k in z.files}
  buf=io.BytesIO();np.savez_compressed(buf,**a)
  if buf.getvalue()!=raw:raise RuntimeError('NPZ_RECONSTRUCTION_NOT_IDENTICAL '+str(p))
  descriptors=[]
  for k,v in a.items():
   if v.dtype.hasobject:raise RuntimeError('OBJECT_ARRAY')
   order='F' if np.isfortran(v) else 'C';b=v.tobytes(order=order)
   descriptors.append({'name':k,'dtype':v.dtype.str,'shape':list(v.shape),'order':order,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
  h={'path':str(p.relative_to(root)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'arrays':descriptors}
  hb=json.dumps(h,sort_keys=True,separators=(',',':')).encode();out.write(struct.pack('<Q',len(hb)));out.write(hb)
  for d,v in zip(descriptors,a.values()):out.write(v.tobytes(order=d['order']))
  entries.append({k:h[k] for k in ['path','bytes','sha256']})
 out.write(struct.pack('<Q',0))
info={'format':'NSS_NPZ_ENVELOPE_V1','payload':'delivery/arrays.xz','payload_bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'entries':entries,'numpy_version':np.__version__,'compression':'lossless XZ of headers and exact numeric bytes; original NPZ bytes rebuilt with np.savez_compressed, verified for every source file',
 'seconds':time.time()-start}
(root/'DELIVERY_ENCODING.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps({k:v for k,v in info.items() if k!='entries'}),flush=True)
