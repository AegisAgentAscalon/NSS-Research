from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    lock=json.loads((ROOT/'SOURCE_LOCK.json').read_text())
    for key,d in lock['files'].items():
        p=ROOT/key
        assert p.stat().st_size==d['bytes'],key
        assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'],key
    print('source/fixture/checkpoint lock verified',len(lock['files']))
if __name__=='__main__':main()
