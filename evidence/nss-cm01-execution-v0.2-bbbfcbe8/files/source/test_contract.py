"""Non-neural codec, control-lifecycle, and isolation unit tests."""
from __future__ import annotations
import copy,unittest
from dataclasses import asdict
from manager import Workspace,encode,decode,compile_public,route

class ContractTests(unittest.TestCase):
    def test_roundtrip(self):
        for op,w in [('R',Workspace(3,17,4,91,'R')),('U',Workspace()),('H',Workspace(operation='H')),('H',Workspace(3,17,4,91,'H'))]:
            self.assertEqual(decode(encode(w)),w);self.assertEqual(len(encode(w)),56)
    def test_edges(self):
        w=Workspace(2**32-1,2**64-1,2**32-1,2**64-1,'R');self.assertEqual(decode(encode(w)),w)
    def test_bad_inputs(self):
        good=encode(Workspace(3,17,4,91,'R'))
        invalid=[good+'\n',good+' ',good.upper(),good.replace('00000003','0000003'),good.replace('R','X'),good.replace('01|','02|'),good.replace('|','¦'),'',good*2,
                 '01|00000000|0000000000000011|00000004|000000000000005b|R',good[:-1]+'U',good[:-1]+'H\n']
        for x in invalid:
            with self.subTest(x=x):
                with self.assertRaises((ValueError,TypeError)):decode(x)
    def test_bad_fields(self):
        for w in [Workspace(-1,1,1,1,'R'),Workspace(2**32,1,1,1,'R'),Workspace(1,2**64,1,1,'R'),Workspace(1,1,0,1,'R'),Workspace(True,1,1,1,'R'),Workspace(1,1,1,1,'U'),Workspace(1,0,0,0,'H')]:
            with self.assertRaises((ValueError,TypeError)):encode(w)
    def history(self):
        return [{'type':'register','event':10,'scope':3,'handle':17,'revision':1,'key':[1.]+[0.]*16,'payload_code':[0.,1.]+[0.]*15,'payload_symbol':2},
                {'type':'select','event':91,'scope':3,'task':7,'handle':17,'revision':1}]
    def test_grounded_and_budget(self):
        v=compile_public(self.history(),{'scope':3,'task':7});r=route(Workspace(**v['workspace']),v,{'scope':3,'task':7})
        self.assertEqual(r['action'],'canonical');self.assertEqual(r['lookup_count'],2);self.assertNotIn('payload_symbol',r)
    def test_resident_without_rewrite(self):
        h=self.history();w0=compile_public(h,{'scope':3,'task':7})['workspace']
        for i in range(32):
            h.append(dict(h[0],event=100+i,handle=200+i))
        v=compile_public(h,{'scope':3,'task':7});self.assertEqual(v['workspace'],w0);self.assertEqual(v['writes'],1)
    def test_stale(self):
        h=self.history()+[dict(self.history()[0],type='revise',revision=2,event=92)]
        v=compile_public(h,{'scope':3,'task':7});r=route(Workspace(**v['workspace']),v,{'scope':3,'task':7});self.assertEqual(r['reason'],'stale_revision')
    def test_delete(self):
        h=self.history()+[{'type':'delete','event':92,'scope':3,'handle':17,'revision':2}]
        v=compile_public(h,{'scope':3,'task':7});self.assertEqual(route(Workspace(**v['workspace']),v,{'scope':3,'task':7})['reason'],'deleted')
    def test_scope(self):
        v=compile_public(self.history(),{'scope':3,'task':7});r=route(Workspace(**v['workspace']),v,{'scope':4,'task':7});self.assertEqual(r['reason'],'cross_scope');self.assertEqual(r['lookup_count'],0)
    def test_wrong_binding(self):
        v=compile_public(self.history(),{'scope':3,'task':7});r=route(Workspace(3,18,1,91,'R'),v,{'scope':3,'task':7});self.assertEqual(r['reason'],'binding_mismatch')
    def test_unresolved(self):
        v=compile_public(self.history(),{'scope':3,'task':7})
        self.assertEqual(route(Workspace(),v,{'scope':3,'task':7})['action'],'original')
        self.assertEqual(route(Workspace(3,17,1,93,'R'),v,{'scope':3,'task':7})['action'],'original')
    def test_conflict(self):
        h=self.history()+[{'type':'conflict','event':92,'task':7}];v=compile_public(h,{'scope':3,'task':7})
        self.assertEqual(v['workspace']['operation'],'H');self.assertEqual(route(Workspace(**v['workspace']),v,{'scope':3,'task':7})['action'],'original')
    def test_no_payload_authority(self):
        h=self.history();v1=compile_public(h,{'scope':3,'task':7});h[0]['payload_symbol']=777
        v2=compile_public(h,{'scope':3,'task':7})
        r1=route(Workspace(**v1['workspace']),v1,{'scope':3,'task':7});r2=route(Workspace(**v2['workspace']),v2,{'scope':3,'task':7})
        # Traffic accounting changes with payload byte length; query/action/provenance must not.
        for f in ('action','reason','canonical_key','handle','record_event'):self.assertEqual(r1[f],r2[f])
if __name__=='__main__':unittest.main(verbosity=2)
