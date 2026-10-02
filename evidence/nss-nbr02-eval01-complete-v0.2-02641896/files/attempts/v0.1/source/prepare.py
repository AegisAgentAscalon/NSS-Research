"""Extract authenticated-by-source-hash retained measurements; never import a model.
Complete raw frames are restored in memory for identity validation, not recomputed.
"""
from pathlib import Path
import argparse, collections, csv, gzip, hashlib, io, json, lzma, math, struct, zlib

def jbytes(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def writej(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(x,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')
def prob(logits,y):
 m=float(logits[y])-float(logits[1-y]);return 1/(1+math.exp(-m)) if m>=0 else math.exp(m)/(1+math.exp(m))
def unpack_frames(blob,expected):
 raw=lzma.decompress(blob)
 assert raw[:8]==b'REVEC001','RAW_MAGIC'
 count,hlen,plen,lanes=struct.unpack('<QQQQ',raw[8:40]);assert lanes==4
 headers=memoryview(raw)[40:40+hlen];shuffled=memoryview(raw)[40+hlen:];assert len(shuffled)==plen
 payload=bytearray(plen);n=plen//4*4
 for i in range(4):payload[i:n:4]=shuffled[i*(n//4):(i+1)*(n//4)]
 payload[n:]=shuffled[n:]
 hp=pp=0;aliases={};recordhash=hashlib.sha256();totalbytes=0;arrcount=0;elements=0
 for index in range(1,count+1):
  hn,pn=struct.unpack('<II',headers[hp:hp+8]);hp+=8;hb=bytes(headers[hp:hp+hn]);hp+=hn
  pb=bytes(payload[pp:pp+pn]);pp+=pn
  envelope=struct.pack('<I',hn)+hb+pb;packed=zlib.compress(envelope,6)
  frame=struct.pack('<Q',len(packed))+hashlib.sha256(packed).digest()+packed
  recordhash.update(frame);totalbytes+=len(frame)
  h=json.loads(hb);values={}
  for name,d in h['arrays'].items():
   if 'alias' in d:b=aliases[d['alias']]
   else:
    b=pb[d['offset']:d['offset']+d['bytes']];assert len(b)==d['bytes'];aliases[d['identity']]=b
   assert digest(b)==d['sha256'],'ARRAY_HASH'
   arrcount+=1;elements+=math.prod(d['shape']);values[name]=b
  yield index,h,values,digest(envelope)
 assert hp==hlen and pp==plen,'FRAME_COUNTS'
 assert totalbytes==expected['bytes'] and recordhash.hexdigest()==expected['sha256'],'RESTORED_RECORD_IDENTITY'
 return

def run(root,archive_dir):
 config=json.loads((root/'protocol/CONFIG.json').read_text());audits={};allcases=[]
 for name,spec in config['sources'].items():
  path=archive_dir/spec['archive'];b=path.read_bytes()
  assert len(b)==spec['bytes'] and digest(b)==spec['sha256'],'SOURCE_ZIP_IDENTITY'
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   assert z.testzip() is None,'ZIP_CRC';prefix=spec['root'];manifest=json.loads(z.read(prefix+'MANIFEST.json'))
   entries={v['path']:v for v in manifest['files']};physical=0
   for rel,e in entries.items():
    if prefix+rel in z.namelist():
     bb=z.read(prefix+rel);assert len(bb)==e['bytes'] and digest(bb)==e['sha256'],rel;physical+=1
   def member(rel):
    bb=z.read(prefix+rel);assert digest(bb)==entries[rel]['sha256'];return bb
   dm=json.loads(member('DELIVERY_MAP.json'))
   if 'encoded_records' in dm:
    desc=next(x for x in dm['encoded_records'] if x['target']=='raw/primary/worker/records.bin');blob=member(desc['payload'])
   else:
    desc=next(x for x in dm['encodings'] if x['target']=='raw/primary/worker/records.bin');blob=member(desc['source'])
   tablebytes=member('raw/primary/final_audit/QUERY_ROWS.csv')
   rows=list(csv.DictReader(io.StringIO(tablebytes.decode())))
   sub=root/'inputs'/name;sub.mkdir(parents=True,exist_ok=True)
   (sub/'ORIGINAL_QUERY_ROWS.csv').write_bytes(tablebytes)
   (sub/'SOURCE_REPORT.md').write_bytes(member('REPORT.md'))
   (sub/'SOURCE_MANIFEST.json').write_bytes(member('MANIFEST.json')) if 'MANIFEST.json' in entries else (sub/'SOURCE_MANIFEST.json').write_bytes(z.read(prefix+'MANIFEST.json'))
   selected={int(r['frame']):r for r in rows if r['phase'] in ('development','heldout') and r['arm'] in ('G','L') and r['kind'] in ('focal','old')}
   allrowbyframe={int(r['frame']):r for r in rows};assert len(allrowbyframe)==len(rows)
   current_table={};statehash=None;measurements={};rawproof=[];checked=0;negative=0;frames=0;arrcount=0;elems=0;maxlossdiff=0.;releases=[]
   for idx,h,values,ehash in unpack_frames(blob,desc):
    frames+=1;arrcount+=len(h['arrays']);elems+=sum(math.prod(d['shape']) for d in h['arrays'].values())
    m=h['metadata'];k=m['kind']
    if k=='load':statehash=digest(values['params'])
    if k in ('management_load','cue') and 'table' in m:current_table=m['table']
    if k in ('update','frozen_receipt') and 'table_after' in m:
     current_table=m['table_after'];releases.append({'frame':idx,'envelope_sha256':ehash,'metadata':m})
    if k in ('update','batch_apply') and 'post' in values:statehash=digest(values['post'])
    if idx in allrowbyframe:
     rr=allrowbyframe[idx];assert 'logits' in values;logits=list(struct.unpack('<2f',values['logits']))
     assert logits==[float(rr['logit0']),float(rr['logit1'])],'SCORE_TO_RAW_LOGITS'
     y=int(rr['target']);pred=int(logits[1]>logits[0]);mar=logits[y]-logits[1-y]
     loss=max(0.,-mar)+math.log1p(math.exp(-abs(mar)))
     assert pred==int(rr['predicted']) and int(pred==y)==int(rr['correct'])
     maxlossdiff=max(maxlossdiff,abs(loss-float(rr['loss'])));assert abs(loss-float(rr['loss']))<=2e-12
     checked+=1;negative+=int(pred!=y)
    if idx not in selected:continue
    r=selected[idx];scope=int(r['scope']);cue=int(r['cue']);y=int(r['target'])
    entry=current_table.get(f'{scope}:{cue}')
    assert entry is not None and int(entry['label'])==y,('PUBLIC_TABLE_TARGET',name,idx,scope,cue)
    version=m.get('parameter_version',m.get('version'))
    assert version==statehash,('STATE_VERSION',name,idx,version,statehash)
    c=m['context'];assert c['session']==r['session'] and c['branch']==r['branch'] and int(c['trial'])==int(r['trial'])
    rec={'record_id':f'{name}:frame:{idx}','frame':idx,'source':name,'session':r['session'],'phase':r['phase'],'method':r['method'],'fit':int(r['fit']),'base':int(r['base']),'branch':r['branch'],'trial':int(r['trial']),'stage':r.get('stage','post_real'),'cue':cue,'scope':scope,'target':y,'kind':r['kind'],'logits':logits,'parameter_version':version,'receipt':entry,'envelope_sha256':ehash,'array_sha256':h['arrays']['logits']['sha256']}
    measurements[idx]=rec
    rawproof.append({'frame':idx,'header':h,'logits_hex':values['logits'].hex(),'envelope_sha256':ehash})
   assert checked==len(rows) and len(measurements)==len(selected),'ROW_COUNTS'
   writej(sub/'RAW_QUERY_PROOFS.json',rawproof)
   writej(sub/'MEASUREMENTS.json',list(measurements.values()))
   # Keep the actual captured receipt-table update metadata, not private future labels.
   writej(sub/'RELEASE_RECORDS.json',releases)
   groups=collections.defaultdict(list)
   for r in measurements.values():groups[(r['session'],r['branch'],r['trial'],r['stage'])].append(r)
   parents={};metadata={}
   for key,rs in groups.items():
    sess,branch,tr,stage=key
    assert len(rs)==9 and {r['cue'] for r in rs if r['kind']=='old'}==set(range(8)),('BAD_QUERY_GROUP',name,key,len(rs))
    assert len({r['parameter_version'] for r in rs})==1
    if branch=='COMMON' and tr==2:
     parents[sess]=rs
   seen={};occasions=0
   for key,rs in sorted(groups.items(),key=lambda x:min(r['frame'] for r in x[1])):
    sess,branch,tr,stage=key
    if branch=='COMMON' or tr<3:continue
    assert tr<=6 and stage in ('post_real','post_extra')
    parent=parents[sess];old=sorted([r for r in rs if r['kind']=='old'],key=lambda r:r['cue']);f=next(r for r in rs if r['kind']=='focal');po=sorted([r for r in parent if r['kind']=='old'],key=lambda r:r['cue']);pf=next(r for r in parent if r['kind']=='focal')
    assert [r['target'] for r in old]==[r['target'] for r in po]
    assert f['cue']==pf['cue'] and f['target']!=pf['target'],'NEW_TARGET_NOT_REVERSAL'
    cells=collections.Counter((r['scope'],r['target']) for r in po);assert cells=={(0,0):2,(0,1):2,(1,0):2,(1,1):2},cells
    ky=(sess,f['parameter_version'],f['target']);alias={'branch':branch,'trial':tr,'stage':stage,'frames':[r['frame'] for r in rs]};occasions+=1
    if ky in seen:
     other=seen[ky];assert [r['logits'] for r in old]==[r['logits'] for r in other['old']] and f['logits']==other['focal']['logits'];other['aliases'].append(alias);continue
    ident=digest(jbytes([name,*ky]))
    case={'id':ident,'source':name,'phase':f['phase'],'method':f['method'],'fit':f['fit'],'base':f['base'],'session':sess,'parameter_version':f['parameter_version'],'parent_version':pf['parameter_version'],'anchor_version':pf['parameter_version'],'focal':f,'old':old,'parent_focal':pf,'parent_old':po,'aliases':[alias], 'prior_complete_inventory_records':9,'candidate_evidence_origin':'previously captured neural logits','live_adoption':False}
    seen[ky]=case
   cases=list(seen.values());allcases+=cases
   audits[name]={'archive':spec,'zip_crc':True,'direct_manifest_files_verified':physical,'manifest_logical_total':len(entries),'raw_primary_record_bytes_reconstructed_and_hash_verified':desc['bytes'],'raw_primary_record_sha256':desc['sha256'],'frames':frames,'array_occurrences_checked':arrcount,'numeric_elements':elems,'query_rows_checked':checked,'original_wrong_class_rows_preserved':negative,'max_score_loss_difference':maxlossdiff,'selected_measurements':len(measurements),'contexts':len(parents),'candidate_occasions':occasions,'distinct_candidate_versions':len(cases),'aliases_collapsed':occasions-len(cases),'replay_not_rerun':True,'secondary_alias_files_not_all_restored':True}
 assert len(allcases)<=config['caps']['candidates'];allcases.sort(key=lambda x:x['id'])
 writej(root/'inputs/CANDIDATES.json',allcases)
 writej(root/'audit/EXTRACTION.json',audits)
 print(json.dumps({k:{f:v for f,v in a.items() if f in ['query_rows_checked','contexts','candidate_occasions','distinct_candidate_versions','aliases_collapsed']} for k,a in audits.items()},indent=2))

if __name__=='__main__':
 import zipfile
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--archives',type=Path,required=True);a=p.parse_args();run(a.root,a.archives)
