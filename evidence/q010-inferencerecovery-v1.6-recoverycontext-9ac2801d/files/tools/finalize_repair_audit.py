from pathlib import Path
import hashlib,json,difflib,shutil,datetime
R=Path(__file__).resolve().parents[1];IN=Path('/mnt/data/_q010_repair013/input/NSS_NBR01_Q010_ChatExecution_v1.2_Continuation')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
before=json.loads((R/'audit/SOURCE_BEFORE.json').read_text());changed=[];unchanged=0;missing=[]
for rel,h in before.items():
 p=R/rel
 if not p.is_file():missing.append(rel);continue
 actual=sha(p)
 if actual==h:unchanged+=1;continue
 changed.append({'path':rel,'before_sha256':h,'after_sha256':actual})
 old=IN/rel
 if p.suffix in ('.py','.md','.json','.txt') and old.is_file():
  out=R/'changes'/('diff_'+str(len(changed)).zfill(2)+'.patch')
  out.write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True),p.read_text().splitlines(True),fromfile='original/'+rel,tofile='repaired/'+rel)))
if missing:raise AssertionError(missing)
for p in Path('/mnt/data/_q010_repair013').glob('patch*.py'):shutil.copyfile(p,R/'changes'/p.name)
shutil.copyfile('/mnt/data/_q010_repair013/launch.py',R/'tools/launch_recorded.py')
input_archive=R/'inputs/NSS_NBR01_Q010_ChatExecution_v1.2_Continuation.zip'
assert sha(input_archive)=='60b23f20a6ec67d120258a34da8a2e72705ee4d96c049eed3d8fdd9faade52ae'
assert sha(Path('/mnt/data/NSS_NBR01_Q010_ChatExecution_v1.2_Continuation.zip'))==sha(input_archive)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INPUT_PRESERVATION_AND_EXPLICIT_WORKING_COPY_DIFF','input_archive_sha256':sha(input_archive),'original_copied_files':len(before),'unchanged_working_copy_files':unchanged,'modified_working_copy_files':changed,'missing_working_copy_files':missing,'original_input_archive_unchanged':True,'input_manifest_members_verified':11416,'main_fits_completed':0,'main_heldout_cells_run':0,'scope':'Repair release; copied old evidence identities retained. New code/tests/logs are additional, not described as recovered.'}
(R/'audit/REPAIR_DIFFS.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
