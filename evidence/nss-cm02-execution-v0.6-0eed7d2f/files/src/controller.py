"""Transparent public-only reference controllers. No access to templates, seeds or truth."""
from __future__ import annotations
import copy,re,sys,time
import numpy as np
from io_utils import canonical,array_digest
PAT=re.compile(r'01\|([0-9a-f]{8})\|([0-9a-f]{16})\|([0-9a-f]{8})\|([0-9a-f]{16})\|([RUH])\Z')
EMPTY=(1,0,0,0,0,'U')
def valid_fields(v):
    if not isinstance(v,tuple) or len(v)!=6:raise ValueError('workspace tuple')
    version,scope,handle,revision,event,op=v
    if version!=1 or any(type(x) is not int for x in v[:5]):raise ValueError('version/integer')
    if not 0<=scope<2**32 or not 0<=handle<2**64 or not 0<=revision<2**32 or not 0<=event<2**64:raise ValueError('field range')
    if op=='R' and min(scope,handle,revision,event)>0:return v
    if op=='U' and v==EMPTY:return v
    if op=='H' and scope>0 and handle==revision==0 and event>0:return v
    raise ValueError('reserved fields')
def encode(v):
    version,s,h,r,e,op=valid_fields(v);x=f'01|{s:08x}|{h:016x}|{r:08x}|{e:016x}|{op}'
    assert len(x)==56;return x
def decode(s):
    if not isinstance(s,str):raise ValueError('expected ASCII text')
    m=PAT.fullmatch(s)
    if m is None:raise ValueError('bad control grammar')
    return valid_fields((1,*(int(t,16) for t in m.groups()[:4]),m.group(5)))
def deep_size(root):
    """Unique Python object graph. NumPy owners include their bytes; tensor storage once."""
    seen=set();storages=set()
    def visit(o):
        if id(o) in seen:return 0
        seen.add(id(o));n=sys.getsizeof(o)
        if isinstance(o,np.ndarray):
            if o.base is not None:n+=visit(o.base)
        elif isinstance(o,dict):n+=sum(visit(k)+visit(v) for k,v in o.items())
        elif isinstance(o,(tuple,list,set,frozenset)):n+=sum(visit(v) for v in o)
        elif type(o).__module__==__name__ and hasattr(o,'__dict__'):
            n+=visit(vars(o))
        elif hasattr(o,'_parameters') and hasattr(o,'_modules'):
            n+=visit(vars(o))
        elif type(o).__module__.startswith('torch'):
            if hasattr(o,'untyped_storage'):
                st=o.untyped_storage();key=(st.data_ptr(),st.nbytes())
                if key not in storages:storages.add(key);n+=st.nbytes()
            elif hasattr(o,'__dict__'):n+=visit(vars(o))
        return n
    return visit(root)
def cache_key(model_hash,arrays):return model_hash+':stage0:'+array_digest(arrays)
def public_projection(envelope):
    """No private/future field enters the controller API."""
    return copy.deepcopy(envelope['public'])
def zero_work():
    return dict(event_updates=0,index_reads=0,index_writes=0,lookup_returned_bytes=0,journal_append_bytes=0,
      record_rewritten_bytes=0,binding_rewritten_bytes=0,task_field_semantic_bytes_rewritten=0,
      workspace_ascii_bytes_rewritten=0,selection_object_bytes_reallocated=0,packet_encodes=0,packet_decodes=0,
      decoded_field_sets=0,query_visits=0,scan_event_visits=0,payload_fetches=0,payload_returned_bytes=0,
      row_writes=0,numerical_bytes_rewritten=0,peak_transient_unique_graph_bytes=0)
def merge_work(a,b):
    for k,v in b.items():
        if k=='peak_transient_unique_graph_bytes':a[k]=max(a[k],v)
        else:a[k]+=v
    return a
class Controller:
    def __init__(self,kind,book,active,symbols):
        if kind not in ('W','I','L'):raise ValueError(kind)
        self.kind=kind
        self.state=dict(journal=[],records={},bindings={},entries={},task_scopes={},current={},row_map={},
          keys=np.zeros((16,17),np.float32),values=np.zeros((16,17),np.float32),valid=np.zeros(16,bool),
          book=np.asarray(book,np.float32).copy(),active=np.asarray(active,bool).copy(),symbols=np.asarray(symbols,np.int64).copy())
        if kind=='L':self.state['revision_index']={}
    def _fields(self,task,w):
        v=self.state['entries'].get(task);w['index_reads']+=1
        if v is None:return EMPTY
        w['lookup_returned_bytes']+=56 if self.kind=='W' else 26
        if self.kind=='W':w['packet_decodes']+=1;w['decoded_field_sets']+=1;return decode(v)
        return valid_fields(v)
    def _set(self,task,v,w):
        valid_fields(v)
        new=encode(v) if self.kind=='W' else tuple(list(v))
        if self.kind=='W':w['packet_encodes']+=1;w['workspace_ascii_bytes_rewritten']+=56
        w['selection_object_bytes_reallocated']+=sys.getsizeof(new)
        w['task_field_semantic_bytes_rewritten']+=26;w['index_writes']+=1;self.state['entries'][task]=new
    def apply(self,event):
        st=self.state;w=zero_work();w['event_updates']=1;e=copy.deepcopy(event)
        if type(e.get('event')) is not int or not 0<e['event']<2**64:raise ValueError('malformed event id')
        typ=e['type'];st['journal'].append(e);w['journal_append_bytes']=len(canonical(e))
        if typ in ('register','revise','delete'):
            k=(e['scope'],e['handle'])
            if not 0<e['scope']<2**32 or not 0<e['handle']<2**64:raise ValueError('bad record identifier')
            if typ=='register':
                if k in st['records'] or e['revision']!=1:raise ValueError('duplicate registration')
                kb=np.asarray(e['key'],np.float32).tobytes()
                if kb in st['row_map'] or not 0<=e['row']<16:raise ValueError('key collision/row')
                st['row_map'][kb]=e['row'];w['index_writes']+=1
            else:
                old=st['records'].get(k);w['index_reads']+=1
                if old is None or not old['active'] or e['revision']!=old['revision']+1:raise ValueError('noncontiguous or resurrected record')
                w['lookup_returned_bytes']+=len(canonical(old))
                if typ=='revise' and e['key']!=old['key']:raise ValueError('key changed')
            if typ=='delete':
                rec=dict(old,active=False,revision=e['revision'],event=e['event'])
            else:rec=dict(e,active=True)
            st['records'][k]=rec;w['index_writes']+=1;w['record_rewritten_bytes']=len(canonical(rec))
            if self.kind=='L':st['revision_index'][(e['scope'],e['handle'],e['revision'])]=e;w['index_writes']+=1
            row=st['row_map'][np.asarray(rec['key'],np.float32).tobytes()];w['index_reads']+=1;w['lookup_returned_bytes']+=8
            st['valid'][row]=rec['active'];st['keys'][row]=rec['key'] if rec['active'] else 0;st['values'][row]=rec['payload_code'] if rec['active'] else 0
            w['row_writes']+=1;w['numerical_bytes_rewritten']+=137
        elif typ=='activate':
            if st['current'] or st['entries']:raise ValueError('activation repeated')
            for item in e['task_contexts']:
                if item['task'] in st['entries']:raise ValueError('duplicate task')
                st['task_scopes'][item['task']]=item['scope'];self._set(item['task'],EMPTY,w)
            st['current']={'task':e['task'],'scope':e['scope']}
            if st['task_scopes'].get(e['task'])!=e['scope']:raise ValueError('activation scope')
        elif typ=='switch':
            if st['task_scopes'].get(e['task'])!=e['scope']:raise ValueError('switch scope')
            st['current']={'task':e['task'],'scope':e['scope']}
        elif typ in ('select','correct','conflict'):
            if st['task_scopes'].get(e['task'])!=e['scope']:raise ValueError('task namespace mismatch')
            prev=self._fields(e['task'],w)
            if prev[4] in st['bindings']:
                oldb=st['bindings'][prev[4]];oldb['closed_by']=e['event'];w['index_writes']+=1;w['binding_rewritten_bytes']+=len(canonical(oldb))
            if typ=='conflict':v=(1,e['scope'],0,0,e['event'],'H')
            else:v=(1,e['scope'],e['handle'],e['revision'],e['event'],'R')
            st['bindings'][e['event']]={'event':e,'closed_by':None};w['index_writes']+=1;w['binding_rewritten_bytes']+=len(canonical(st['bindings'][e['event']]))
            self._set(e['task'],v,w)
        else:raise ValueError('unknown public event')
        return w
    def route(self):
        st=self.state;w=zero_work();w['query_visits']=1;v=self._fields(st['current']['task'],w)
        # The transient tuple is never retained by a W controller.
        w['peak_transient_unique_graph_bytes']=deep_size({'state':st,'decoded':v})
        _,scope,h,rev,eid,op=v;rec=None
        def done(action,reason):
            return {'action':action,'reason':reason,'fields':list(v),
                    'canonical_key':rec['key'] if action=='canonical' else None},w
        if op!='R':return done('original','conflict' if op=='H' else 'unselected')
        if scope!=st['current']['scope']:return done('abstain','cross_scope')
        b=st['bindings'].get(eid);w['index_reads']+=1
        if b is None:return done('original','missing_binding')
        w['lookup_returned_bytes']+=len(canonical(b));be=b['event']
        if b['closed_by'] is not None:return done('abstain','superseded_binding')
        if be['type'] not in ('select','correct'):return done('original','conflict')
        if (be['task'],be['scope'],be['handle'],be['revision'])!=(st['current']['task'],scope,h,rev):return done('abstain','binding_mismatch')
        rec=st['records'].get((scope,h));w['index_reads']+=1
        if rec is None:return done('original','missing_record')
        w['lookup_returned_bytes']+=len(canonical(rec))
        if not rec['active']:return done('abstain','deleted')
        if rec['revision']!=rev:
            if self.kind!='L':return done('abstain','stale_revision')
            for rr in range(rev,rec['revision']+1):
                er=st['revision_index'].get((scope,h,rr));w['index_reads']+=1
                if er is None:return done('abstain','broken_revision_chain')
                w['lookup_returned_bytes']+=len(canonical(er))
                if er['type'] not in ('register','revise') or er['key']!=rec['key']:return done('abstain','broken_revision_chain')
            return done('canonical','observed_latest_revision')
        return done('canonical','validated_pinned_revision')
    def exact(self,route):
        w=zero_work();pred=-1
        if route['action']=='canonical':
            _,s,h,_,_,_=route['fields'];rec=self.state['records'][(s,h)];w['index_reads']=1;w['payload_fetches']=1
            pred=rec['payload_symbol'];w['payload_returned_bytes']=len(canonical({'payload_code':rec['payload_code'],'payload_symbol':pred}));w['lookup_returned_bytes']=w['payload_returned_bytes']
        return int(pred),w
    def memory(self,query,model=None):
        root={'controller':self,'query':query}
        if model is not None:root['model']=model
        serial={k:v for k,v in self.state.items() if k not in ('keys','values','valid','book','active','symbols','row_map','records','bindings','entries','task_scopes','revision_index')}
        # A normalized, lossless inventory; shared Python objects may serialize repeatedly.
        serial['records']=[[list(k),v] for k,v in sorted(self.state['records'].items())]
        serial['bindings']=[[k,v] for k,v in sorted(self.state['bindings'].items())]
        serial['entries']=[[k,v] for k,v in sorted(self.state['entries'].items())]
        serial['task_scopes']=[[k,v] for k,v in sorted(self.state['task_scopes'].items())]
        serial['row_map']=[[k.hex(),v] for k,v in sorted(self.state['row_map'].items())]
        if self.kind=='L':serial['revision_index']=[[list(k),v] for k,v in sorted(self.state['revision_index'].items())]
        return {'whole_unique_python_graph_bytes':deep_size(root),'controller_unique_graph_bytes':deep_size(self.state),
                'canonical_state_metadata_bytes':len(canonical(serial)),
                'state_array_bytes':sum(v.nbytes for v in self.state.values() if isinstance(v,np.ndarray)),
                'query_bytes':query.nbytes,'selection_semantic_field_bytes':26*len(self.state['entries']),
                'selection_ascii_bytes':56*len(self.state['entries']) if self.kind=='W' else 0,
                'selection_dictionary_unique_graph_bytes':deep_size(self.state['entries']),
                'entries':len(self.state['entries']),'journal_events':len(self.state['journal'])}
def scan_control(journal,book,active,symbols,query):
    c=Controller('I',book,active,symbols);w=zero_work()
    for e in journal:merge_work(w,c.apply(e));w['scan_event_visits']+=1
    r,rw=c.route();merge_work(w,rw);pred,pw=c.exact(r);merge_work(w,pw)
    memory={'persistent_unique_graph_bytes':deep_size({'journal':journal,'book':book,'active':active,'symbols':symbols}),
            'peak_transient_unique_graph_bytes':deep_size({'journal':journal,'reconstructed':c,'query':query}),
            'canonical_observed_journal_bytes':len(canonical(journal))}
    return r,pred,w,memory
