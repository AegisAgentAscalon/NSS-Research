from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    r=json.loads((ROOT/'spec/REGISTRATION.json').read_text());n=0
    for group in ('files','inherited'):
        for name,digest in r[group].items():assert sha(ROOT/name)==digest,name;n+=1
    fs=[]
    for p in (ROOT/'checkpoints').glob('*.safetensors'):
        m=json.loads(p.with_suffix('.json').read_text());assert sha(p)==m['checkpoint_sha256'];assert m['initial_hash']!=m['final_hash'];fs.append(p.name)
    result={'registered_hashes_verified':n,'new_checkpoint_files':len(fs),'status':'PASS','checks':fs}
    (ROOT/'evidence/INTEGRITY.json').write_text(json.dumps(result,indent=2));print(result)
if __name__=='__main__':main()
