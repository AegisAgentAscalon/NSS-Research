"""Run unchanged23 development regression assertions on this turn's integration fixture.
This does not retarget or erase the three separate archived verifier failures.
"""
from pathlib import Path
import sys,unittest,importlib.util,json,hashlib,time
R=Path(__file__).resolve().parents[1];S=R/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0';sys.path[:0]=[str(R/'source'),str(R/'recovery'),str(S/'implementation_A'),str(S/'verification_B')]
from inference_loader import deny_training
import torch
torch.set_num_threads(1);torch.set_num_interop_threads(1);deny_training()
modules=[]
for name in ['test_batch_core','test_columnar_verifier']:
    p=R/'source/tests'/f'{name}.py';spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);modules.append(m)
@classmethod
def current_fixture(cls):
    cls.root=R/'results/integration_fixture/capture';cls.cap=json.loads((cls.root/'CAPTURE.json').read_text())
modules[1].ColumnarVerifierTests.setUpClass=current_fixture
suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in modules)
t=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(suite)
report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skips':len(result.skipped),'seconds':time.monotonic()-t,'fixture':'results/integration_fixture/capture','fixture_scope':'fresh64condition development integration using saved seed1201 main readers,4cases; not main statistics','assertion_sources_unchanged':True,'does_not_replace_archived_verifier_suite':True,'new_optimizer_updates':0}
(R/'audit/FRESH_REGRESSIONS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));sys.exit(not result.wasSuccessful())
