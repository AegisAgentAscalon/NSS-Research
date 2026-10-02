import sys,json,zlib,struct,hashlib,time,gzip,os
from pathlib import Path
R=Path('/mnt/data/NSS_NBR02_MICROMACRO01_Execution_v0.2')
sys.path.insert(0,str(R/'source'))
from envelope_codec import encode_envelopes,decode_envelopes,envelopes_from_records
# Administrative lossless packaging only; no model or numerical analysis.
D=R/'delivery';D.mkdir(exist_ok=True)
P=D/'RESTORATION.json'
spec=json.loads(P.read_text()) if P.exists() else {'schema':'NSS_RESTORE_v1','zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,'items':[],'events':[]}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def save():
 tmp=P.with_suffix('.tmp');tmp.write_text(json.dumps(spec,sort_keys=True,indent=2));os.replace(tmp,P)
def record(rel):
 p=R/rel;target={'path':rel,'bytes':p.stat().st_size,'sha256':sha(p)}
 pref=hashlib.sha256(rel.encode()).hexdigest()[:14];parts=[];count=0;allh=hashlib.sha256();allbytes=0;chunk=[];beg=time.time()
 def emit(envs):
  nonlocal count,allbytes
  index=len(parts);blob=encode_envelopes(envs);out=D/(pref+f'_{index:03d}.xz');out.write_bytes(blob)
  orig=b'';h=hashlib.sha256();n=0
  for src,rest in zip(envs,decode_envelopes(blob),strict=True):
   if src!=rest:raise RuntimeError('CODEC_BYTE_ROUNDTRIP')
   z=zlib.compress(rest,6);fr=struct.pack('<Q',len(z))+hashlib.sha256(z).digest()+z
   h.update(fr);allh.update(fr);n+=len(fr);allbytes+=len(fr);count+=1
  parts.append({'path':str(out.relative_to(R)),'bytes':len(blob),'sha256':sha(out),'frames':len(envs),'restored_bytes':n,'restored_sha256':h.hexdigest()})
  print(json.dumps({'target':rel,'parts':len(parts),'frames':count,'bytes_restored':allbytes,'elapsed':time.time()-beg}),flush=True)
 for e in envelopes_from_records(p):
  chunk.append(e)
  if len(chunk)==4096:emit(chunk);chunk=[]
 if chunk:emit(chunk)
 if allh.hexdigest()!=target['sha256'] or allbytes!=target['bytes']:raise RuntimeError('ORIGINAL_FRAME_STREAM_DIFF')
 spec['items'].append({**target,'kind':'envelope_chunks','parts':parts,'frames':count});save();p.unlink()
 spec['events'].append({'action':'seal_closed_record_file_after_exact_byte_roundtrip','path':rel,'host_epoch':time.time(),'frames':count,'source_bytes':target['bytes'],'encoded_bytes':sum(x['bytes'] for x in parts)});save()
def sealtext(rel):
 p=R/rel;target={'path':rel,'bytes':p.stat().st_size,'sha256':sha(p)};q=D/(hashlib.sha256(rel.encode()).hexdigest()[:16]+'.gz')
 with open(p,'rb') as f,open(q,'wb') as out:
  with gzip.GzipFile(fileobj=out,mode='wb',mtime=0,compresslevel=6,filename='') as g:
   for b in iter(lambda:f.read(1<<20),b''):g.write(b)
 h=hashlib.sha256();n=0
 with gzip.open(q,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b);n+=len(b)
 if h.hexdigest()!=target['sha256'] or n!=target['bytes']:raise RuntimeError('GZIP_ROUNDTRIP')
 spec['items'].append({**target,'kind':'gzip','encoded':str(q.relative_to(R)),'encoded_bytes':q.stat().st_size,'encoded_sha256':sha(q)});save();p.unlink()
 spec['events'].append({'action':'seal_closed_text_after_exact_byte_roundtrip','path':rel,'host_epoch':time.time(),'source_bytes':n,'encoded_bytes':q.stat().st_size});save();print('SEALED',rel,flush=True)
if __name__=='__main__':
 mode,rel=sys.argv[1:3]
 (record if mode=='record' else sealtext)(rel)
