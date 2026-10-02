"""Storage-only continuation amendment. No model/optimizer imports or scientific rules."""
import json,struct,zlib,lzma,hashlib,time,math
from pathlib import Path

def raw_frames(path):
    with open(path,'rb') as f:
        while hd:=f.read(40):
            if len(hd)!=40: raise ValueError('TRUNCATED_HEADER')
            n=struct.unpack('<Q',hd[:8])[0]; b=f.read(n)
            if len(b)!=n or hashlib.sha256(b).digest()!=hd[8:]:raise ValueError('FRAME_DIGEST')
            raw=zlib.decompress(b); hn=struct.unpack('<I',raw[:4])[0]; meta=json.loads(raw[4:4+hn]); yield hd,b,raw,meta

def envelope_bytes(path,phase=None,plan=None):
    out=bytearray()
    for hd,b,r,h in raw_frames(path):
        if phase is None or plan['sessions'][h['metadata']['context']['session']]['phase']==phase:
            # Preserve original compressed length/digest and decoded bytes, verifying reversible original byte reconstruction.
            q=zlib.compress(r,6)
            if q!=b:raise ValueError('ZLIB_ROUNDTRIP')
            out.extend(struct.pack('<Q',len(r)));out.extend(r)
    return bytes(out)

def schema_table():
    # Scheduler counts, no targets or stimuli generated. Conditions=72*4fits*4methods.
    counts={'load':1214,'cue_G':2216,'cue_L':2216,'cue_N':3456,'fillers':7880,'update':4424,'frozen_receipt':3456,'query':16308,'checkpoint':1224,'derivative':8}
    # Full, no-alias numerical bytes are from actual serialized array dtypes/shapes.
    n={'load':2696,'cue_G':2696+4*16*4+2*8,'cue_L':2696+4*16*4+2*8+3*640*4,'cue_N':2696+4*16*4+2*8,'fillers':33*16*4,'update':674*4*2+8,'frozen_receipt':2696,'query':4*16*4+16,'checkpoint':2696+5056+2496,'derivative':2696}
    # Explicit engineering maxima for variable canonical headers; enforced/tested separately, not a compression theorem.
    h={'load':512,'cue_G':5120,'cue_L':2560,'cue_N':2560,'fillers':768,'update':1792,'frozen_receipt':1536,'query':1536,'checkpoint':9216,'derivative':768}
    rows=[{'kind':k,'count_per_full_pass':v,'full_array_bytes_per_record':n[k],'header_allowance':h[k],'unalias_logical_envelope_bytes_two_passes':2*v*(4+h[k]+n[k])}for k,v in counts.items()]
    return rows

def admit(run,growth,elapsed,before):
    root=run.parent.parent;plan=json.loads((run/'private/PLAN.json').read_text());fr=run/'worker/records.bin'
    cost=envelope_bytes(fr,'cost',plan);blob=lzma.compress(cost,format=lzma.FORMAT_XZ,preset=6)
    assert lzma.decompress(blob)==cost
    # Identical safety multiplier/application allowance/non-update reserve; only measured lossless representation changes.
    delivery=int(math.ceil(len(blob)/100*4424*2+18*1024**2))
    rows=schema_table();maxs={};headers={};raws={}
    for hd,b,r,h in raw_frames(fr):
        kind=h['metadata']['kind']; arm=h['metadata']['arm']; kind=kind+'_'+arm if kind=='cue' else kind
        maxs[kind]=max(maxs.get(kind,0),len(b)+40);hn=struct.unpack('<I',r[:4])[0];headers[kind]=max(headers.get(kind,0),hn);raws[kind]=max(raws.get(kind,0),sum(a['bytes'] for a in h['arrays'].values()))
    # Frozen controls have no observed cost-probe frames; use their explicit full-array plus header envelope bound.
    maxs['cue_N']=4+2560+272+64;maxs['frozen_receipt']=4+1536+64 # Frozen params already stored by LOAD; mandatory exact aliases.
    # Load/checkpoint numerical payloads repeat already retained exact parameter/RNG arrays; worst observed frames include first full RNG capture.
    contrib=[]
    for r in rows:
        k=r['kind'];m=maxs[k]; assert headers.get(k,0)<=r['header_allowance']; assert raws.get(k,0)<=r['full_array_bytes_per_record']
        contrib.append({**r,'observed_or_control_bound_encoded_max':m,'forecast_encoded_two_passes':math.ceil(2*r['count_per_full_pass']*m)})
    rawforecast=sum(x['forecast_encoded_two_passes'] for x in contrib)+32*1024**2
    start=json.loads((root/'audit/START.json').read_text())['start_epoch'];runelapsed=time.time()-start
    timeforecast=elapsed/100*8848*2+runelapsed
    rec={'status':'PASS' if delivery<=64*1024**2 and rawforecast<=256*1024**2 and timeforecast<=6500 else 'FAIL',
      'probe_updates':100,'wall_including_audit':elapsed,'record_growth_old_codec':growth,'cost_decoded_envelope_bytes':len(cost),'cost_xz_bytes':len(blob),
      'delivery_projection_with_2x_margin_and_verified_replay_dedup':delivery,'delivery_limit':64*1024**2,
      'component_rows':contrib,'encoded_capture_projection_with_32MiB_nonnumeric_reserve':rawforecast,'capture_limit':256*1024**2,
      'noalias_logical_envelope_total':sum(r['unalias_logical_envelope_bytes_two_passes'] for r in rows),
      'logical_bytes_not_identical_to_losslessly_encoded_capture_bytes':True,'size_estimates_are_not_proved_compression_bounds':True,
      'cost_codec_roundtrip_exact':True,'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,'projected_total_active_seconds':timeforecast,
      'old_fixed_209MiB_boolean_removed':True,'all_shapes_and_counts_explicit':True,
      'overrun_policy':'independent supervisor stops at actual caps; no evidence dropped',
      'assumptions':['new array/value distributions can change compression','frozen parameters must alias exact LOAD bytes; all new state/logit payload still counted','cross-pass delivery sharing only after genuine exact adaptive replay','long filler maxima measured by the clean 32-filler fixture','non-numeric reserve is a budget allocation, not a mathematical proof']}
    rec['passed']=rec['status']=='PASS'
    return rec
