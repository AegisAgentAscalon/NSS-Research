"""Restore exact captured byte streams and verified replay aliases. No model computation."""
from pathlib import Path
import argparse,gzip,hashlib,json,shutil,sys,zlib
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);args=p.parse_args();root=args.root.resolve()
def path(s):
 q=(root/s).resolve()
 if not q.is_relative_to(root):raise ValueError('UNSAFE_DELIVERY_PATH')
 return q
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def valid(p,n,h):return p.is_file() and p.stat().st_size==n and digest(p)==h
mapping=json.loads(path('DELIVERY_MAP.json').read_text());done=[]
for item in mapping['encodings']:
 dest=path(item['target']);src=path(item['source'])
 if dest.exists():
  if not valid(dest,item['bytes'],item['sha256']):raise RuntimeError('EXISTING_TARGET_MISMATCH:'+item['target'])
  done.append(item['target']);continue
 if not valid(src,item['encoded_bytes'],item['encoded_sha256']):raise RuntimeError('ENCODED_SOURCE_MISMATCH')
 dest.parent.mkdir(parents=True,exist_ok=True);temp=dest.with_name(dest.name+'.restoring')
 try:
  if item['codec']=='gzip':
   with gzip.open(src,'rb') as f,temp.open('wb') as g:shutil.copyfileobj(f,g)
  elif item['codec']=='envelope_xz_v1':
   if zlib.ZLIB_RUNTIME_VERSION!=mapping['zlib_runtime']:raise RuntimeError('BYTE_RECONSTRUCTION_ZLIB_VERSION:'+zlib.ZLIB_RUNTIME_VERSION)
   sys.path.insert(0,str(path('source')))
   from envelope_codec import restore_records
   restore_records(src.read_bytes(),temp)
  else:raise RuntimeError('UNKNOWN_CODEC')
  if not valid(temp,item['bytes'],item['sha256']):raise RuntimeError('RESTORATION_MISMATCH:'+item['target'])
  temp.replace(dest);done.append(item['target'])
 finally:
  if temp.exists():temp.unlink()
for item in mapping['aliases']:
 src=path(item['source']);dest=path(item['target'])
 if not valid(src,item['bytes'],item['sha256']):raise RuntimeError('ALIAS_SOURCE_MISMATCH:'+item['source'])
 if dest.exists():
  if not valid(dest,item['bytes'],item['sha256']):raise RuntimeError('ALIAS_TARGET_MISMATCH')
 else:
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
 done.append(item['target'])
print(json.dumps({'status':'PASS','restored_or_verified_paths':len(done),'new_model_calls':0,'new_updates':0,'logical_aliases_follow_actual_fresh_replay':True},indent=2))
