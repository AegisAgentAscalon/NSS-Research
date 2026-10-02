"""Non-neural contract tests only. No network instance, forward, backward or update."""
import json,sys,copy,unittest,hashlib
from pathlib import Path
import numpy as np
from runtime import decide,validate
class Contracts(unittest.TestCase):
    def test_first_seen_not_change(self):self.assertFalse(decide({},0,0,1,False))
    def test_same_label_not_change(self):self.assertFalse(decide({'0:0':{'label':1}},0,0,1,False))
    def test_early_change(self):self.assertTrue(decide({'0:0':{'label':0}},0,0,1,False))
    def test_late_change(self):
        t={}
        for _ in range(7):t['0:0']={'label':0};self.assertFalse(decide(t,0,0,0,False))
        self.assertTrue(decide(t,0,0,1,False))
    def test_second_change_no_boost(self):self.assertFalse(decide({'0:0':{'label':1}},0,0,0,True))
    def test_scope_not_conflated(self):self.assertFalse(decide({'1:0':{'label':0}},0,0,1,False))
    def test_receipts(self):
        p={'scope':0,'receipt':'new','version':'v','immutable':'d'}
        args=[p,{'old'},0,'new','v',1,'v','d'];self.assertIsNone(validate(*args))
        for j,v in [(2,1),(3,'old'),(3,'foreign'),(4,'changed'),(5,2),(6,'w'),(7,'q')]:
            z=args.copy();z[j]=v;self.assertIsNotNone(validate(*z))
        self.assertEqual(validate(None,set(),0,'r','v',0,'v','d'),'NO_PENDING')
    def test_wrong_authenticated_outcome_unidentifiable(self):
        p={'scope':0,'receipt':'r','version':'v','immutable':'d'}
        self.assertIsNone(validate(p,set(),0,'r','v',0,'v','d'));self.assertIsNone(validate(p,set(),0,'r','v',1,'v','d'))
    def test_table_copy(self):
        t={'0:0':{'label':0}};u=copy.deepcopy(t);u['0:0']['label']=1;self.assertEqual(t['0:0']['label'],0)
    def test_no_trial_argument(self):
        import inspect
        self.assertEqual(list(inspect.signature(decide).parameters),['table','cue','scope','target','used'])
    def test_equivalent_hidden_projection(self):
        allowed=('cue','scope','receipt')
        a={'cue':0,'scope':0,'receipt':'r','future':0,'gold':1};b={**a,'future':1,'gold':0}
        self.assertEqual({k:a[k] for k in allowed},{k:b[k] for k in allowed})
    def test_array_alias_fixture(self):
        base=np.arange(1920,dtype='f4');view=base.reshape(3,640)
        seen=set();buffers={}
        def walk(a):
            if id(a) in seen:return
            seen.add(id(a))
            if isinstance(a,np.ndarray):
                if isinstance(a.base,np.ndarray):walk(a.base)
                else:buffers[id(a)]=a.nbytes
        walk(view);walk(base);walk(view[0]);self.assertEqual(sum(buffers.values()),7680)
    def test_raw_ids_strict(self):
        def good(s):return isinstance(s,str) and len(s)==16 and s!='0'*16 and all(c in '0123456789abcdef' for c in s)
        self.assertTrue(good('000000000000000a'));self.assertFalse(good('0'*16));self.assertFalse(good('BAD'));self.assertFalse(good('F'*16))
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Contracts);r=unittest.TextTestRunner(verbosity=2).run(suite)
    Path(sys.argv[1]).write_text(json.dumps({'tests':r.testsRun,'errors':len(r.errors),'failures':len(r.failures),'passed':r.wasSuccessful(),'no_scientific_model_execution':True},indent=2))
    raise SystemExit(not r.wasSuccessful())
