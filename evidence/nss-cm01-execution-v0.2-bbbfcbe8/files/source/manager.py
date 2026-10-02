"""Deterministic public-journal manager. No model, scorer or protected inputs."""
from __future__ import annotations
import copy,re,sys,json
from dataclasses import dataclass,asdict
RX=re.compile(r'01\|[0-9a-f]{8}\|[0-9a-f]{16}\|[0-9a-f]{8}\|[0-9a-f]{16}\|[RUH]')
@dataclass(frozen=True)
class Workspace:
    scope:int=0; handle:int=0; revision:int=0; binding_event:int=0; operation:str='U'

def encode(w):
    if not isinstance(w,Workspace):raise TypeError('Workspace required')
    vals=(w.scope,w.handle,w.revision,w.binding_event)
    for x,bits in zip(vals,(32,64,32,64)):
        if type(x) is not int or not 0<=x<2**bits:raise ValueError('field out of range')
    if w.operation not in 'RUH' or len(w.operation)!=1:raise ValueError('bad operation')
    if w.operation=='R' and any(x==0 for x in vals):raise ValueError('reserved zero in R')
    if w.operation=='U' and any(x!=0 for x in vals):raise ValueError('U must use all reserved zeros')
    # H may retain a complete untrusted proposal, or carry all-zero fields.
    if w.operation=='H' and any(x==0 for x in vals) and any(x!=0 for x in vals):raise ValueError('partial H proposal')
    s=f'01|{w.scope:08x}|{w.handle:016x}|{w.revision:08x}|{w.binding_event:016x}|{w.operation}'
    if len(s.encode('ascii'))!=56:raise AssertionError('codec width')
    return s

def decode(s):
    if not isinstance(s,str) or RX.fullmatch(s) is None:raise ValueError('malformed UTF8_BYTE_V1')
    x=s.split('|');w=Workspace(*(int(a,16) for a in x[1:5]),x[5])
    if encode(w)!=s:raise ValueError('noncanonical encoding')
    return w

def key(scope,handle):return f'{scope:08x}/{handle:016x}'

def compile_public(journal,current):
    """One streaming journal pass. All indexes and update costs are reported."""
    records={};bindings={};w=Workspace();transitions=[];writes=0
    for e in journal:
        before=encode(w);typ=e['type']
        if typ in ('register','revise'):
            records[key(e['scope'],e['handle'])]={k:copy.deepcopy(e[k]) for k in ('scope','handle','revision','key','payload_code','payload_symbol')}
            records[key(e['scope'],e['handle'])]['active']=True
            records[key(e['scope'],e['handle'])]['record_event']=e['event']
        elif typ=='delete':
            rk=key(e['scope'],e['handle']);records[rk]['active']=False;records[rk]['revision']=e['revision'];records[rk]['record_event']=e['event']
        elif typ in ('select','correct'):
            bindings[str(e['event'])]={k:copy.deepcopy(e[k]) for k in ('scope','task','handle','revision','event')}
            bindings[str(e['event'])]['conflict']=False
            if e['task']==current['task']:
                w=Workspace(e['scope'],e['handle'],e['revision'],e['event'],'R')
        elif typ=='conflict':
            for b in bindings.values():
                if b['task']==e['task']:b['conflict']=True
            if e['task']==current['task']:w=Workspace(operation='H')
        else:raise ValueError('unknown public event')
        after=encode(w)
        if before!=after:writes+=1
        transitions.append({'event':e['event'],'before':before,'after':after,'changed':before!=after})
    return {'records':records,'bindings':bindings,'workspace':asdict(w),'transitions':transitions,'writes':writes}

def route(w,view,current):
    """At most two indexed reads. Returns query provenance, never a payload."""
    receipts=[]
    def result(action,reason,record=None):
        return {'action':action,'reason':reason,'handle':w.handle if action=='canonical' else None,
                'canonical_key':record['key'] if record is not None else None,
                'record_event':record['record_event'] if record is not None else None,
                'lookups':receipts,'lookup_count':len(receipts)}
    encode(w) # semantic validation is shared with serializer
    if w.operation in ('U','H'):return result('original','unresolved' if w.operation=='U' else 'conflict')
    if w.scope!=current['scope']:return result('abstain','cross_scope')
    b=view['bindings'].get(str(w.binding_event));receipts.append({'index':'binding','key':str(w.binding_event),'found':b is not None,'returned_bytes':len(json.dumps(b,sort_keys=True,separators=(',',':')).encode()) if b else 0})
    if b is None:return result('original','missing_binding')
    if b['conflict']:return result('original','conflict')
    if b['task']!=current['task'] or b['scope']!=w.scope or b['handle']!=w.handle or b['revision']!=w.revision:
        return result('abstain','binding_mismatch')
    r=view['records'].get(key(w.scope,w.handle));receipts.append({'index':'record','key':key(w.scope,w.handle),'found':r is not None,'returned_bytes':len(json.dumps(r,sort_keys=True,separators=(',',':')).encode()) if r else 0})
    if r is None:return result('original','missing_record')
    if not r['active']:return result('abstain','deleted')
    if r['revision']!=w.revision:return result('abstain','stale_revision')
    return result('canonical','validated_public_binding',r)

def deep_size(obj,seen=None):
    if seen is None:seen=set()
    if id(obj) in seen:return 0
    seen.add(id(obj));n=sys.getsizeof(obj)
    if isinstance(obj,dict):n+=sum(deep_size(k,seen)+deep_size(v,seen) for k,v in obj.items())
    elif isinstance(obj,(list,tuple,set)):n+=sum(deep_size(x,seen) for x in obj)
    elif hasattr(obj,'__dict__'):n+=deep_size(vars(obj),seen)
    return n
