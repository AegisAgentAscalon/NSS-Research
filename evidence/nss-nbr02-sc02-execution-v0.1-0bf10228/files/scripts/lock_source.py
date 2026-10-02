from support import *
files={}
for folder in ['source','scripts','tests','checkpoints']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file()and '__pycache__'not in p.parts:files[str(p.relative_to(ROOT))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
p=ROOT/'PROTOCOL.md';files['PROTOCOL.md']={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
if(ROOT/'SOURCE_LOCK.json').exists():raise RuntimeError('source already locked')
save(ROOT/'SOURCE_LOCK.json',{'schema':'nss.sc02.lock.v1','files':files,'runtime':runtime(),'phase':'AFTER_DEVELOPMENT_BEFORE_FRESH_GENERATION'})
print('locked',len(files),'files')
