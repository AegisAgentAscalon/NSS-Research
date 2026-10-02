import json
from safetensors.torch import load_file
from .common import ROOT,weights_hash
from .resolver import Resolver,MatchHead
METHODS=('none','normalize','nearest','learned','A_nearest','A_learned','B_nearest','B_learned','reject_all')
MAIN_SEEDS=tuple(range(1001,1006))

def load_gate(seed,dev=False):
    folder=ROOT/('evidence/development' if dev else 'checkpoints')
    h=MatchHead();h.load_state_dict(load_file(str(folder/f'match_head_{seed}.safetensors')));h.eval()
    for p in h.parameters():p.requires_grad_(False)
    cfg=json.loads((folder/f'calibration_{seed}.json').read_text())
    return h,cfg

def resolver(method,models,head,cfg):
    par=cfg['A'] if method.startswith(('A_','distance_','margin_')) else cfg['B'] if method.startswith('B_') else {}
    return Resolver(method,par,head,models['dictionary'])

def contract(r,models):
    return {'abi':'nbr008-membership-v1','method':r.method,'calibration':r.params,
            'head':weights_hash(r.head) if r.head is not None else None,
            'parents':{k:weights_hash(v) for k,v in models.items()},
            'unreadable_policy':'sticky_until_qualified_write_or_clear','capacity':16}
