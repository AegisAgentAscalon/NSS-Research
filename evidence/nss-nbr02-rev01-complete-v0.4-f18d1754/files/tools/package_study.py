"""Lossless delivery builder. Never computes or repairs neural evidence."""
import sys,json,hashlib,zipfile,os,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'source'))
from envelope_codec import encode_envelopes,envelopes_from_records,decode_envelopes

def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()
exclude={'MANIFEST.json','DELIVERY_MAP.json'}
files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and '.payload' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.pyc' and str(p.relative_to(ROOT)) not in exclude]
canonical={};aliases=[];encoded=[];included=[]
(ROOT/'.payload').mkdir(exist_ok=True)
for p in files:
    rel=str(p.relative_to(ROOT));hh=digest(p);key=(p.stat().st_size,hh)
    if key in canonical:
        aliases.append({'target':rel,'source':canonical[key],'sha256':hh});continue
    canonical[key]=rel
    if p.name=='records.bin':
        blob=encode_envelopes(envelopes_from_records(p));bp=ROOT/'.payload'/('records-'+hh[:20]+'.xz');bp.write_bytes(blob)
        # Before delivery: every decoded envelope reproduces captured raw bytes.
        import itertools
        for a,b in itertools.zip_longest(envelopes_from_records(p),decode_envelopes(blob)):
            if a!=b:raise RuntimeError('CODEC_ENVELOPE_MISMATCH')
        encoded.append({'target':rel,'sha256':hh,'bytes':p.stat().st_size,'payload':str(bp.relative_to(ROOT)),'payload_sha256':digest(bp),'payload_bytes':len(blob)})
        included.append(bp)
    else:included.append(p)
mapdoc={'format':'REV01_EXACT_EVIDENCE_DELIVERY_V1','codec':'REVEC001 four-byte numeric lanes + XZ preset6','zlib_captured_version':'1.3.1','encoded_records':encoded,'aliases':aliases,'scientific_data_recomputed_on_restore':False}
(ROOT/'DELIVERY_MAP.json').write_text(json.dumps(mapdoc,indent=2))
manifestfiles=files+[ROOT/'DELIVERY_MAP.json']+[ROOT/e['payload'] for e in encoded]
rows=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(manifestfiles)]
(ROOT/'MANIFEST.json').write_text(json.dumps({'format':'REV01_ALL_RETAINED_FILES_V1','files':rows,'total_restored_bytes':sum(x['bytes'] for x in rows)},indent=2))
out=Path(sys.argv[1])
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in included+[ROOT/'DELIVERY_MAP.json',ROOT/'MANIFEST.json']:
        z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)),compress_type=zipfile.ZIP_STORED if '.payload' in p.parts else zipfile.ZIP_DEFLATED)
    if z.testzip() is not None:raise RuntimeError('ZIP_CRC')
if out.stat().st_size>64*1024**2:raise RuntimeError('ZIP_CAP; preserve failed candidate, no evidence removal')
print(json.dumps({'zip':str(out),'bytes':out.stat().st_size,'sha256':digest(out),'manifest_files':len(rows),'restored_bytes':sum(x['bytes'] for x in rows),'encoded_records':encoded,'aliases':len(aliases)},indent=2))
