from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 path=ROOT/'MANIFEST.sha256'
 if not path.exists():raise FileNotFoundError('Run from an extracted, packaged release with MANIFEST.sha256')
 count=0
 for line in path.read_text().splitlines():
  digest,name=line.split('  ',1);p=ROOT/name
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise RuntimeError('Integrity failure: '+name)
  count+=1
 print('MANIFEST PASS:',count,'covered files')
if __name__=='__main__':main()
