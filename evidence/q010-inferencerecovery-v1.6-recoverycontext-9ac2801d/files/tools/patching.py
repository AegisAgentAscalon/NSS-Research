from pathlib import Path
import os,json,hashlib,difflib,datetime
ROOT=Path(os.environ['ROOT'])
def replace(path,old,new,reason):
 p=Path(path);before=p.read_bytes();text=before.decode();assert text.count(old)==1,(p,old,text.count(old));after=text.replace(old,new);p.write_text(after)
 i=len(list((ROOT/'changes').glob('*.json')))+1;stem=ROOT/'changes'/f'{i:03d}_{p.stem}'
 stem.with_suffix('.diff').write_text(''.join(difflib.unified_diff(text.splitlines(True),after.splitlines(True),fromfile=str(p.relative_to(ROOT)),tofile=str(p.relative_to(ROOT)))))
 stem.with_suffix('.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':str(p.relative_to(ROOT)),'before':hashlib.sha256(before).hexdigest(),'after':hashlib.sha256(p.read_bytes()).hexdigest(),'reason':reason},indent=2)+'\n')
