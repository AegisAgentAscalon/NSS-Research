"""Exact segment lifecycle. Deterministic software, not a neural capability."""
from __future__ import annotations
import json,time
from collections import defaultdict
from pathlib import Path
from typing import Any
from common import canonical,sha,write_json

class ContextError(RuntimeError): pass
class VersionedStore:
    def __init__(self):
        self.history=defaultdict(list);self.clock=0;self.read_bytes=0;self.index_lookups=0
        self.actions={};self.effect_count=0
    def publish(self,record:dict):
        d=dict(record);sid=d['id'];old=self.history[sid]
        if old and d['revision']!=old[-1]['revision']+1: raise ContextError('NON_MONOTONIC_REVISION')
        if not old and d['revision']!=1:raise ContextError('INVALID_FIRST_REVISION')
        if old and d['scope']!=old[-1]['scope']:raise ContextError('SCOPE_REBINDING')
        self.clock+=1;d['issued']=self.clock
        blob=canonical(d);entry={'revision':d['revision'],'scope':d['scope'],'issued':self.clock,
             'blob':blob.decode(),'hash':sha(blob),'deps':list(d['deps'])}
        old.append(entry)
    def locate(self,sid:int,scope:str,cutoff:int|None=None):
        self.index_lookups+=1
        if sid not in self.history:raise ContextError('MISSING_RECORD')
        entries=self.history[sid]
        e=next((e for e in reversed(entries) if cutoff is None or e['issued']<=cutoff),None)
        if e is None:raise ContextError('NOT_VISIBLE_AT_CUTOFF')
        if e['scope']!=scope:raise ContextError('WRONG_SCOPE')
        return e
    def get(self,sid,scope,cutoff=None):
        e=self.locate(sid,scope,cutoff);b=e['blob'].encode();self.read_bytes+=len(b)
        if sha(b)!=e['hash']:raise ContextError('SOURCE_DIGEST_MISMATCH')
        return json.loads(b)
    def act_once(self,key:str,payload:dict):
        digest=sha(canonical(payload))
        if key in self.actions:
            if self.actions[key]!=digest:raise ContextError('RECEIPT_PAYLOAD_CONFLICT')
            return 'already_applied'
        self.actions[key]=digest;self.effect_count+=1;return 'applied'
    def dump(self):return {'clock':self.clock,'history':dict(self.history),'actions':self.actions,'effect_count':self.effect_count}
    @classmethod
    def restore(cls,data):
        obj=cls();obj.clock=data['clock'];obj.history=defaultdict(list,{int(k):v for k,v in data['history'].items()})
        obj.actions=data['actions'];obj.effect_count=data['effect_count']
        for entries in obj.history.values():
            for e in entries:
                if sha(e['blob'].encode())!=e['hash']:raise ContextError('RESTORE_DIGEST_MISMATCH')
        return obj

class Manager:
    def __init__(self,store:VersionedStore,persistent:bool,budget:int=100_000):
        self.store=store;self.persistent=persistent;self.budget=budget;self.cache={}
        self.hits=0;self.builds=0;self.invalidations=0;self.returned_bytes=0
    def packet(self,roots:list[int],scope='P',cutoff=None,freeze=0):
        roots=sorted(set(roots))
        key=sha(canonical([roots,scope,cutoff,freeze]))
        # Dependencies are explicit source metadata, no answer-based selection.
        selected=set(roots)
        for sid in roots:selected.update(self.store.locate(sid,scope,cutoff)['deps'])
        proof=[(sid,self.store.locate(sid,scope,cutoff)['hash']) for sid in sorted(selected)]
        cached=self.cache.get(key)
        if self.persistent and cached and cached['proof']==[list(x) for x in proof]:
            if sha(cached['body'].encode())!=cached['hash']:raise ContextError('CACHE_DIGEST_MISMATCH')
            body=cached['body'].encode();self.hits+=1
        else:
            if cached:self.invalidations+=1
            records=[self.store.get(sid,scope,cutoff) for sid in sorted(selected)]
            obj={'schema':'nss.maintenance.packet.v1','scope':scope,'roots':roots,'cutoff':cutoff,
                 'freeze':freeze,'records':records,'proof':proof}
            body=canonical(obj);self.builds+=1
            if len(body)>self.budget:raise ContextError('MANDATORY_CONTEXT_OVER_BUDGET')
            if self.persistent:self.cache[key]={'proof':[list(x) for x in proof], 'body':body.decode(),'hash':sha(body)}
        if len(body)>self.budget:raise ContextError('MANDATORY_CONTEXT_OVER_BUDGET')
        self.returned_bytes+=len(body)
        return body
    def snapshot(self):
        d={'schema':'nss.manager.checkpoint.v1','persistent':self.persistent,'budget':self.budget,'cache':self.cache}
        return {'data':d,'hash':sha(canonical(d))}
    @classmethod
    def restore(cls,store,snapshot):
        if sha(canonical(snapshot['data']))!=snapshot['hash']:raise ContextError('CHECKPOINT_DIGEST_MISMATCH')
        d=snapshot['data'];obj=cls(store,d['persistent'],d['budget']);obj.cache=d['cache'];return obj


def store_from_world(w:dict,scope='P'):
    s=VersionedStore()
    for i in range(len(w['progress'])):
        s.publish({'id':i,'scope':scope,'revision':1,'source':f"{w['id']}/{i}/1",'deps':w['deps'][i],
                   'code':w['codes'][i], 'progress':w['progress'][i],'receipt':w['receipts'][i],
                   'constraint':w['constraints'][i],'nuisance':w['nuisance'][i]})
    return s

def world_from_packet(b:bytes):
    d=json.loads(b);r=d['records'];mp={e['id']:i for i,e in enumerate(r)}
    # Integration requests whole 8-task job groups, whose declared dependencies fit inside.
    if any(dep not in mp for e in r for dep in e['deps']):raise ContextError('UNRESOLVED_READER_DEPENDENCY')
    return {'id':sha(b), 'codes':[e['code'] for e in r],
       'deps':[[mp[j] for j in e['deps']] for e in r], 'progress':[e['progress'] for e in r],
       'receipts':[e['receipt'] for e in r], 'constraints':[e['constraint'] for e in r],
       'nuisance':[e['nuisance'] for e in r], 'freeze':d['freeze']}
