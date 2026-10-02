"""Explicit development-only roster. Never accepted by the 6000-step main loader."""
from pathlib import Path
import json
import torch
from q010c.protocol import ROOT,sha,ARMS
from q010c.train import load_payload
from q010r.models import load_parent_reader,AttentionPointerReader,model_state_hash

def development_readers():
    models={};identities={}
    for name,cap in [('inherited_801',80.),('cap_only',20000.)]:
        m,info=load_parent_reader(801,cap=cap);models[name]=m;identities[name]=dict(info,scope='INHERITED_DEVELOPMENT_CONTROL',public_sha256=model_state_hash(m))
    for role,arm in ARMS:
        p=ROOT/'inputs/host_profile001'/arm/'step0040.pt';pay=load_payload(p)
        if pay['optimizer_step']!=40:raise ValueError('wrong development checkpoint')
        m=AttentionPointerReader() if role=='attention' else load_parent_reader(801,cap=20000.)[0]
        m.load_state_dict(pay['model_state'],strict=True);m.eval();models[role]=m
        identities[role]={'scope':'REUSED_DEVELOPMENT_40_UPDATES_NOT_MAIN','checkpoint':str(p.relative_to(ROOT)),'checkpoint_sha256':sha(p),'strict_sha256':pay['model_state_sha256'],'public_sha256':model_state_hash(m),'steps':40}
    models['exact_owner']=None;identities['exact_owner']={'scope':'EXACT_ENGINEERED_CONTROL','source_sha256':sha(Path(__file__).with_name('batch_core.py'))}
    return models,identities
