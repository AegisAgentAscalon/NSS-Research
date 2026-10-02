"""Terminates deliberately inside archive transaction boundaries; synthetic data."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nss_base.experience_store import ExperienceArchive
from nss_base.serialization import read_json

if __name__=='__main__':
    directory,kind,request_file,point=sys.argv[1:]
    store=ExperienceArchive(directory)
    method={'capture':store.capture,'change':store.change,'revoke':store.revoke_source}[kind]
    result=method(read_json(request_file),fault_at=point)
    print(result)
    raise SystemExit(3) # Expected path exits via the crash hook with 74.
