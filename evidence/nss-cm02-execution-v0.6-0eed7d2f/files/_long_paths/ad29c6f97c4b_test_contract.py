"""Deterministic toy fixtures only: no random cases or model forwards."""
from __future__ import annotations
import copy,unittest,sys
import numpy as np
from controller import Controller,encode,decode,EMPTY,scan_control,cache_key,deep_size,public_projection
from io_utils import canonical

class ContractTests(unittest.TestCase):
    def toy(self,kind='W'):
        book=np.zeros((16,17),np.float32);book[:,:16]=np.eye(16,dtype=np.float32)
        c=Controller(kind,book,np.ones(16,bool),np.arange(16,dtype=np.int64))
        for i in range(3):c.apply(dict(type='register',event=10+i,scope=3 if i<2 else 4,handle=17+i,revision=1,row=i,key=book[i].tolist(),payload_code=book[(i+1)%3].tolist(),payload_symbol=(i+1)%3))
        c.apply(dict(type='activate',event=20,task=7,scope=3,task_contexts=[{'task':7,'scope':3},{'task':8,'scope':4}]))
        c.apply(dict(type='select',event=91,scope=3,task=7,handle=17,revision=1))
        return c
    def test_codec(self):
        for v in [EMPTY,(1,3,17,1,91,'R'),(1,3,0,0,92,'H'),(1,2**32-1,2**64-1,2**32-1,2**64-1,'R')]:
            self.assertEqual(len(encode(v)),56);self.assertEqual(decode(encode(v)),v)
    def test_malformed_and_reserved(self):
        s=encode((1,3,17,1,91,'R'))
        bad=[s+'\n',s+' ',s.replace('|','¦'),s.upper(),s.replace('01|','02|'),s[:-1]+'X',s.replace('00000003','0000003'),'',s*2]
        for text in bad:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):decode(text)
        for v in [(1,0,17,1,91,'R'),(True,3,17,1,91,'R'),(1,3,0,0,0,'H'),(1,2**32,1,1,1,'R')]:
            with self.assertRaises(ValueError):encode(v)
    def test_two_empty_slots_then_one_task(self):
        c=self.toy();self.assertEqual(len(c.state['entries']),2);self.assertEqual(decode(c.state['entries'][8]),EMPTY)
        self.assertEqual(c.route()[0]['action'],'canonical')
    def test_representation_parity_and_scan(self):
        w=self.toy('W');i=self.toy('I');wr=w.route()[0];ir=i.route()[0];self.assertEqual(wr,ir)
        sr,sp,_,_=scan_control(w.state['journal'],w.state['book'],w.state['active'],w.state['symbols'],w.state['book'][0])
        self.assertEqual(sr,wr);self.assertEqual(sp,1)
        self.assertTrue(all(isinstance(x,str) for x in w.state['entries'].values()));self.assertTrue(all(isinstance(x,tuple) for x in i.state['entries'].values()))
    def test_switch_keeps_other_task(self):
        c=self.toy();saved=c.state['entries'][7]
        c.apply(dict(type='select',event=92,scope=4,task=8,handle=19,revision=1));c.apply(dict(type='switch',event=93,scope=4,task=8))
        self.assertEqual(c.state['entries'][7],saved);self.assertEqual(c.route()[0]['fields'][2],19)
        c.apply(dict(type='switch',event=94,scope=3,task=7));self.assertEqual(c.route()[0]['fields'][2],17)
    def revision(self,c):return dict(type='revise',event=92,scope=3,handle=17,revision=2,key=c.state['book'][0].tolist(),payload_code=c.state['book'][2].tolist(),payload_symbol=2)
    def test_revision_pinned_vs_latest(self):
        for kind in ('W','I','L'):
            c=self.toy(kind);before=copy.deepcopy(c.state['entries']);c.apply(self.revision(c));self.assertEqual(before,c.state['entries'])
            r=c.route()[0];self.assertEqual(r['reason'],'observed_latest_revision' if kind=='L' else 'stale_revision');self.assertEqual(c.exact(r)[0],2 if kind=='L' else -1)
    def test_correction_refreshes(self):
        c=self.toy();c.apply(self.revision(c));c.apply(dict(type='correct',event=93,scope=3,task=7,handle=17,revision=2,supersedes=91))
        self.assertEqual(c.route()[0]['action'],'canonical');self.assertEqual(c.exact(c.route()[0])[0],2)
    def test_deletion_and_no_resurrection(self):
        for k in ('W','I','L'):
            c=self.toy(k);c.apply(dict(type='delete',event=92,scope=3,handle=17,revision=2));r=c.route()[0]
            self.assertEqual(r['reason'],'deleted');self.assertEqual(c.exact(r)[0],-1);self.assertFalse(c.state['valid'][0]);self.assertTrue(np.all(c.state['keys'][0]==0))
            with self.assertRaises(ValueError):c.apply(dict(self.revision(c),event=93,revision=3))
    def test_missing_binding(self):
        c=self.toy();c.state['entries'][7]=encode((1,3,17,1,999,'R'));self.assertEqual(c.route()[0]['reason'],'missing_binding')
    def test_wrong_scope_and_wrong_binding(self):
        c=self.toy();c.state['current']['scope']=4;self.assertEqual(c.route()[0]['reason'],'cross_scope')
        c=self.toy();c.state['entries'][7]=encode((1,3,18,1,91,'R'));self.assertEqual(c.route()[0]['reason'],'binding_mismatch')
    def test_conflict_and_resolution(self):
        c=self.toy();c.apply(dict(type='conflict',event=92,scope=3,task=7,handles=[17,18]));self.assertEqual(c.route()[0]['reason'],'conflict')
        c.apply(dict(type='correct',event=93,scope=3,task=7,handle=18,revision=1,supersedes=92,resolves=92));self.assertEqual(c.route()[0]['fields'][2],18)
    def test_queries_never_refresh(self):
        c=self.toy();c.apply(self.revision(c));before=copy.deepcopy((c.state['entries'],c.state['journal'],c.state['records'],c.state['bindings']))
        for _ in range(8):c.route()
        self.assertEqual(before,(c.state['entries'],c.state['journal'],c.state['records'],c.state['bindings']))
    def test_prefix_and_label_isolation_sensitive_to_observation(self):
        c=self.toy();hist=copy.deepcopy(c.state['journal'])
        def run(envelope):
            h=public_projection(envelope);other=Controller('W',c.state['book'],c.state['active'],c.state['symbols'])
            for event in h:other.apply(event)
            return other.route()[0]
        a=run({'public':hist,'private':{'expected':1},'future':[self.revision(c)]})
        b=run({'public':hist,'private':{'expected':777},'future':[{'type':'delete'}]})
        self.assertEqual(a,b)
        observed=hist+[dict(type='correct',event=92,scope=3,task=7,handle=18,revision=1,supersedes=91)]
        self.assertNotEqual(a,run({'public':observed,'private':{},'future':[]}))
    def test_no_expected_answer_in_route(self):
        c=self.toy();r=c.route()[0];self.assertNotIn('payload_symbol',r);self.assertNotIn('expected',r)
        c.state['records'][(3,17)]['payload_symbol']=999;self.assertEqual(c.route()[0],r)
    def test_cache_all_inputs_and_model_identity(self):
        c=self.toy();a={k:c.state[k].copy() for k in ('keys','values','valid','book','active','symbols')};a['query']=c.state['book'][0].copy()
        key=cache_key('hash1',a);self.assertNotEqual(key,cache_key('hash2',a))
        for k in a:
            v={x:y.copy() for x,y in a.items()};v[k].flat[0]=not v[k].flat[0] if v[k].dtype==bool else v[k].flat[0]+1
            self.assertNotEqual(key,cache_key('hash1',v))
        v={x:y.copy() for x,y in a.items()};v['query']=v['query'].astype(np.float64);self.assertNotEqual(key,cache_key('hash1',v))
    def test_unique_graph_shared_objects(self):
        x=[float(3.5)];a=[x,x];b=[x,copy.deepcopy(x)];self.assertLess(deep_size(a),deep_size(b))
    def test_malformed_identifier_rejected(self):
        c=self.toy()
        with self.assertRaises(ValueError):c.apply(dict(type='switch',event=0,scope=3,task=7))
    def test_unchanged_packet_through_background_updates(self):
        c=self.toy();old=c.state['entries'][7]
        for n in range(32):c.apply(dict(type='revise',event=200+n,scope=4,handle=19,revision=n+2,key=c.state['book'][2].tolist(),payload_code=c.state['book'][n%3].tolist(),payload_symbol=n%3))
        self.assertEqual(c.state['entries'][7],old)
if __name__=='__main__':unittest.main(verbosity=2)
