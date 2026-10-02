"""Reversible grouping of exact captured JSON headers and byte-shuffled raw array payload.
Pure storage codec; never reconstructs scientific data through model arithmetic.
"""
import struct,lzma,zlib,hashlib
MAGIC=b'REVEC001'
def encode_envelopes(envelopes):
    headers=[];payload=[];count=0
    for raw in envelopes:
        n=struct.unpack('<I',raw[:4])[0];h=raw[4:4+n];b=raw[4+n:]
        if len(h)!=n:raise ValueError('TRUNCATED_ENVELOPE')
        headers.append(struct.pack('<II',n,len(b))+h);payload.append(b);count+=1
    mb=b''.join(headers);pb=b''.join(payload);lanes=4;n=len(pb)//lanes*lanes
    shuffled=b''.join(pb[j:n:lanes] for j in range(lanes))+pb[n:]
    return lzma.compress(MAGIC+struct.pack('<QQQQ',count,len(mb),len(pb),lanes)+mb+shuffled,preset=6)
def decode_envelopes(blob):
    raw=lzma.decompress(blob)
    if raw[:8]!=MAGIC:raise ValueError('CODEC_MAGIC')
    count,ml,pl,lanes=struct.unpack('<QQQQ',raw[8:40]);mb=raw[40:40+ml];pb=raw[40+ml:]
    if lanes!=4 or len(pb)!=pl:raise ValueError('CODEC_SHAPE')
    n=pl//lanes*lanes;out=bytearray(pl)
    for j in range(lanes):out[j:n:lanes]=pb[j*(n//lanes):(j+1)*(n//lanes)]
    out[n:]=pb[n:];offset=0;dataoff=0;seen=0
    while offset<len(mb):
        hn,bn=struct.unpack('<II',mb[offset:offset+8]);offset+=8;h=mb[offset:offset+hn];offset+=hn
        yield struct.pack('<I',hn)+h+bytes(out[dataoff:dataoff+bn]);dataoff+=bn;seen+=1
    if seen!=count or dataoff!=pl or offset!=ml:raise ValueError('CODEC_COUNT')
def envelopes_from_records(path):
    with open(path,'rb') as f:
        while True:
            header=f.read(40)
            if not header:return
            if len(header)!=40:raise ValueError('TRUNCATED_FRAME_HEADER')
            n=struct.unpack('<Q',header[:8])[0];b=f.read(n)
            if len(b)!=n or hashlib.sha256(b).digest()!=header[8:]:raise ValueError('FRAME_HASH')
            yield zlib.decompress(b)
def restore_records(blob,path):
    with open(path,'wb') as f:
        for raw in decode_envelopes(blob):
            z=zlib.compress(raw,6);f.write(struct.pack('<Q',len(z))+hashlib.sha256(z).digest()+z)
