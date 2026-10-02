from . import ROOT
from nbr006.common import setup,utc,sha,dump,weights_hash,save_model,env as _base_env
from nbr006 import models,data
from nbr007.repair import DictionaryRepair
from safetensors.torch import load_file
import torch

def parents(pair):
    if pair not in range(1,6):raise ValueError('Parent pair must be 1..5')
    folder=ROOT/'reference/parent_checkpoints'
    out={k:models.make(k) for k in ('record_hop','gated_hop','binder')}
    out['dictionary']=DictionaryRepair()
    for k,m in out.items():
        file=f'learned_dictionary_{900+pair}' if k=='dictionary' else f'{k}_{800+pair}'
        m.load_state_dict(load_file(str(folder/(file+'.safetensors'))));m.eval()
        for p in m.parameters():p.requires_grad_(False)
    return out

def model_hashes(d):return {k:weights_hash(v) for k,v in d.items()}


def env():
    import resource
    d=_base_env();d["max_rss_kib"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;return d
