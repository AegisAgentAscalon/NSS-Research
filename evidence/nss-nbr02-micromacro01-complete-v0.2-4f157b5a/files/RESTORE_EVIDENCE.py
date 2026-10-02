#!/usr/bin/env python3
"""Restore retained bytes; never instantiate a model or produce new scientific observations."""
import sys,json,hashlib,gzip,lzma,shutil,zlib,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'source'))
from envelope_codec import decode_envelopes
import struct

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def safe(rel):
 p=(ROOT/rel).resolve()
 if not p.is_relative_to(ROOT):raise ValueError('OUTSIDE_PACKAGE')
 return p

def restore():
 spec=json.loads((ROOT/'delivery/RESTORATION.json').read_text())
 if zlib.ZLIB_RUNTIME_VERSION!=spec['zlib_runtime']:
  raise RuntimeError(f'Exact framed-byte restoration requires zlib {spec["zlib_runtime"]}; got {zlib.ZLIB_RUNTIME_VERSION}')
 pending=spec['items'].copy();restored=0
 while pending:
  progress=False
  for item in pending.copy():
   p=safe(item['path'])
   if p.exists():
    if p.stat().st_size!=item['bytes'] or digest(p)!=item['sha256']:raise RuntimeError('EXISTING_TARGET_MISMATCH:'+item['path'])
    pending.remove(item);progress=True;continue
   if item['kind'] in ('alias','prefix') and not safe(item['source']).exists():continue
   p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.restoring')
   h=hashlib.sha256();n=0
   with open(tmp,'wb') as out:
    def emit(b):
     nonlocal n
     out.write(b);h.update(b);n+=len(b)
    if item['kind']=='envelope_chunks':
     for part in item['parts']:
      q=safe(part['path'])
      if q.stat().st_size!=part['bytes'] or digest(q)!=part['sha256']:raise RuntimeError('ENCODED_PART_MISMATCH')
      ph=hashlib.sha256();pn=0;nf=0
      for env in decode_envelopes(q.read_bytes()):
       z=zlib.compress(env,6);b=struct.pack('<Q',len(z))+hashlib.sha256(z).digest()+z
       emit(b);ph.update(b);pn+=len(b);nf+=1
      if ph.hexdigest()!=part['restored_sha256'] or pn!=part['restored_bytes'] or nf!=part['frames']:raise RuntimeError('PART_RESTORE_MISMATCH')
    elif item['kind'] in ('gzip','xz'):
     q=safe(item['encoded'])
     if q.stat().st_size!=item['encoded_bytes'] or digest(q)!=item['encoded_sha256']:raise RuntimeError('ENCODED_LOG_MISMATCH')
     with (gzip.open if item['kind']=='gzip' else lzma.open)(q,'rb') as f:
      for b in iter(lambda:f.read(1<<20),b''):emit(b)
    elif item['kind'] in ('alias','prefix'):
     left=item['bytes']
     with open(safe(item['source']),'rb') as f:
      while left:
       b=f.read(min(left,1<<20))
       if not b:raise RuntimeError('ALIAS_TOO_SHORT')
       emit(b);left-=len(b)
    else:raise RuntimeError('UNKNOWN_RESTORATION_KIND')
    out.flush();os.fsync(out.fileno())
   if n!=item['bytes'] or h.hexdigest()!=item['sha256']:
    raise RuntimeError('RESTORED_TARGET_MISMATCH:'+item['path'])
   os.replace(tmp,p);restored+=1;pending.remove(item);progress=True
  if not progress:raise RuntimeError('MISSING_OR_CYCLIC_ALIAS_DEPENDENCIES')
 return {'status':'PASS','restored_files':restored,'verified_reconstruction_targets':len(spec['items']),'new_model_computations':0}
if __name__=='__main__':print(json.dumps(restore(),indent=2))
