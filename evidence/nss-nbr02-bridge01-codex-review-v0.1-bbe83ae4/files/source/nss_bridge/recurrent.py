"""Frozen learned checklist advisor. No English parsing, permissions, or training.
Original SURFACE01 tensors, same GRU equations as CYCLE01-A, float64 execution.
"""
from __future__ import annotations
import numpy as np
from .util import digest,file_hash

class RecurrentAdvisor:
    def __init__(self,weights_path):
        with np.load(weights_path,allow_pickle=False) as z:
            self.w={k:np.array(z[k],dtype=np.float64,copy=True) for k in z.files}
        expected={'cell.weight_ih':(192,26),'cell.weight_hh':(192,64),'cell.bias_ih':(192,),'cell.bias_hh':(192,),'head.weight':(9,64),'head.bias':(9,)}
        if set(expected)!=set(self.w) or any(self.w[k].shape!=s for k,s in expected.items()): raise ValueError('WEIGHT_SCHEMA')
        if not all(np.isfinite(a).all() for a in self.w.values()): raise ValueError('NONFINITE_WEIGHT')
        self.model_id=file_hash(weights_path);self.banks={};self.trace=[]
        for a in self.w.values(): a.flags.writeable=False
    def init_task(self,key):
        if key in self.banks:raise ValueError('BANK_ALREADY_EXISTS')
        self.banks[key]={'h':np.zeros(64,np.float64),'cursor':0}
    def step(self,key,token,cursor):
        if type(token)!=int or not 0<=token<18:raise ValueError('TOKEN_ABI')
        if key not in self.banks:raise ValueError('UNKNOWN_BANK')
        bank=self.banks[key]
        if cursor!=bank['cursor']+1:raise ValueError('STATE_CURSOR_GAP')
        h=bank['h'];w=self.w
        # one-hot input matmul, kept identical in meaning to the original cell
        x=np.zeros(26,np.float64);x[token]=1
        a=x@w['cell.weight_ih'].T+w['cell.bias_ih'];b=h@w['cell.weight_hh'].T+w['cell.bias_hh']
        ar,az,an=np.split(a,3);br,bz,bn=np.split(b,3)
        r=1/(1+np.exp(-(ar+br)));z=1/(1+np.exp(-(az+bz)))
        n=np.tanh(an+r*bn);hn=(1-z)*n+z*h
        if not np.isfinite(hn).all():raise ValueError('NONFINITE_STATE')
        bank.update(h=hn,cursor=cursor)
        logits=hn@w['head.weight'].T+w['head.bias']
        row={'key':key,'cursor':cursor,'token':token,'h':hn.tolist(),'logits':logits.tolist(),'prediction':int(logits.argmax())}
        self.trace.append(row);return row
    def predict(self,key):
        h=self.banks[key]['h'];z=h@self.w['head.weight'].T+self.w['head.bias']
        return {'next':int(z.argmax()),'logits':z.tolist(),'cursor':self.banks[key]['cursor']}
    def snapshot(self):
        return {'model_id':self.model_id,'state_abi':'GRU26x64_F64_CHECKLIST_V1','banks':{k:{'h':v['h'].tolist(),'cursor':v['cursor']} for k,v in self.banks.items()}}
    def restore(self,obj,expected_keys,cursors):
        if obj.get('model_id')!=self.model_id:raise ValueError('WRONG_MODEL')
        if obj.get('state_abi')!='GRU26x64_F64_CHECKLIST_V1':raise ValueError('WRONG_STATE_ABI')
        if set(obj.get('banks',{}))!=set(expected_keys):raise ValueError('WRONG_TASK_BANKS')
        new={}
        for key,b in obj['banks'].items():
            a=np.asarray(b['h'],dtype=np.float64)
            if a.shape!=(64,) or not np.isfinite(a).all():raise ValueError('BAD_STATE')
            if type(b['cursor'])!=int or b['cursor']!=cursors[key]:raise ValueError('STATE_CURSOR_GAP')
            new[key]={'h':a.copy(),'cursor':b['cursor']}
        self.banks=new
