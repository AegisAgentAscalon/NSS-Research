"""Real once-trained numerical fixture; no fabricated PASS verification payloads."""
import atexit
from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import unittest

from nss_base.neural_contracts import fingerprint, read_document
from nss_base.qualification_contracts import POLICY_HASH
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications
from nss_base.qualificationevidence002 import OPERATORS, AT, review_for
from nss_base.runtime import ContractError

try:
    import torch
    HAVE_TORCH = True
except ImportError:
    HAVE_TORCH = False

_CACHE = None


def base_fixture():
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    from nss_base.neuralprobe001 import DEFAULT, run
    td = tempfile.TemporaryDirectory(prefix='qual-tests-base-'); atexit.register(td.cleanup)
    root = Path(td.name)
    p = read_document(DEFAULT); p['seeds'] = [101]; p['precisions'] = ['fp32']
    run(root/'probe', p, withdraw=False)
    source = NeuralEvidence(root/'probe/journal', root/'probe/data')
    q = Qualifications.create(root/'q', OPERATORS)
    requests = {}; receipts = {}
    for id, scope, parents in [('core', {'kind':'PROFILE','profile':'CORE'}, []),
        ('a', {'kind':'PROFILE','profile':'A'}, ['core']), ('ab', {'kind':'PROFILE','profile':'AB'}, ['core']),
        ('edge', {'kind':'TRANSITION','source':'AB','destination':'A','mode':'replay'}, ['core','ab','a'])]:
        r = source.propose(run_id='probe-001', seed=101, precision='fp32', scope=scope,
            producer_id='fixture-builder', request_id=id, at=AT, prerequisites=parents)
        q.prepare(r, source=source); receipt = q.decide(review_for(r), source=source)
        assert receipt['verdict'] == 'QUALIFIED', receipt
        requests[id] = r; receipts[id] = receipt
    backup = tempfile.TemporaryDirectory(prefix='qual-tests-snapshot-'); atexit.register(backup.cleanup)
    shutil.copytree(root, Path(backup.name)/'fixture')
    _CACHE = root, requests, receipts, Path(backup.name)/'fixture'
    return _CACHE


class QualificationCase(unittest.TestCase):
    def setUp(self):
        if not HAVE_TORCH:
            self.skipTest('Optional PyTorch unavailable')
        original, requests, receipts, backup = base_fixture()
        # Snapshots intentionally bind the archive's local path. Restore the fixture
        # at THAT path; copying it elsewhere is not an authorized archive migration.
        shutil.rmtree(original); shutil.copytree(backup, original)
        self.root = original
        self.q = Qualifications(self.root/'q')
        self.source = NeuralEvidence(self.root/'probe/journal', self.root/'probe/data')
        self.requests = deepcopy(requests); self.receipts = deepcopy(receipts)

    def req(self, id='new', profile='CORE', parents=(), producer='fixture-builder'):
        return self.source.propose(run_id='probe-001', seed=101, precision='fp32',
            scope={'kind':'PROFILE','profile':profile}, producer_id=producer, request_id=id,
            at=AT, prerequisites=parents)

    def use(self, id='edge', scope=None, bind=None, sha=None):
        req = self.requests[id]
        return self.q.check_use(id, certificate_sha256=sha or self.receipts[id]['certificate_sha256'],
            expected_claim=scope or req['claim'], expected_binding=bind or req['binding'], source=self.source)

    def revoke(self, id='core', op='withdraw'):
        return {'schema_version':1,'operation_id':op,'request_id':id,
            'certificate_sha256':self.receipts[id]['certificate_sha256'],'reviewer_id':'fixture-reviewer',
            'at':AT,'reason':'Test revocation with immutable history.'}

    def error(self, code, fn, *args, **kwargs):
        with self.assertRaises(ContractError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception
