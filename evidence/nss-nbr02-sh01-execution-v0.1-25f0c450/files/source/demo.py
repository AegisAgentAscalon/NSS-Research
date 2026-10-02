"""Read a typed-record JSON packet and emit a source-bound maintenance disposition.
No external action, candidate publication, or model update is performed.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import torch
from common import Reader,batch,model_hash,canonical,sha,CLASSES,setup
from store import world_from_packet,ContextError
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,default=ROOT/'examples/packet.json')
    p.add_argument('--reader',choices=['dense','hsa'],default='hsa')
    p.add_argument('--checkpoint',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args();setup()
    cp_path=a.checkpoint or ROOT/f'checkpoints/8801_{a.reader}_0600.pt'
    try:
        raw=a.packet.read_bytes();doc=json.loads(raw)
        if doc.get('schema')!='nss.maintenance.packet.v1':raise ContextError('WRONG_PACKET_SCHEMA')
        proof=dict(doc['proof'])
        ids=[r['id'] for r in doc['records']]
        if len(set(ids))!=len(ids):raise ContextError('DUPLICATE_RECORD_ID')
        for record in doc['records']:
            if record['scope']!=doc['scope']:raise ContextError('WRONG_RECORD_SCOPE')
            if sha(canonical(record))!=proof.get(record['id']):raise ContextError('PACKET_RECORD_DIGEST_MISMATCH')
        w=world_from_packet(raw);x,ix,v,y=batch([w]);n=len(w['progress'])
        cp=torch.load(cp_path,weights_only=False,map_location='cpu');m=Reader();m.load_state_dict(cp['model']);m.eval()
        if model_hash(m)!=cp['model_hash']:raise ContextError('CHECKPOINT_MODEL_HASH_MISMATCH')
        with torch.no_grad():scores=m(x,ix,v,n,a.reader).softmax(-1)[0].numpy()
        output={'schema':'nss.maintenance.output.v1','packet_sha256':sha(raw),'model_sha256':model_hash(m),
           'reader':a.reader,'scope':doc['scope'],'training_updates':cp['step'],
           'dispositions':[{'task':r['id'],'revision':r['revision'],'source':r['source'],
               'status':CLASSES[int(scores[i].argmax())],'score':float(scores[i].max()),
               'dependencies':r['deps']} for i,r in enumerate(doc['records']) if r['id'] in doc['roots']],
           'limitations':['typed synthetic records, not language comprehension','scores are not calibrated probabilities',
                          'record selection/version authority supplied by software','advisory output; no action executed']}
        text=json.dumps(output,indent=2)
        if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text+'\n')
        print(text)
    except (OSError,ValueError,KeyError,ContextError) as e:
        print(json.dumps({'status':'ERROR','type':type(e).__name__,'detail':str(e)}),file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
