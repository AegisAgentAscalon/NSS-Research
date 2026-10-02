"""One real trained/qualified fixture, copied at its pinned path between tests.

No fabricated PASS records, no parallel mutation. Numerical fixture setup is cached;
individual tests exercise local release behavior, not repeated learning claims.
"""
import atexit
from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch
from qualification_helpers import base_fixture, HAVE_TORCH
from nss_base.generation_evidence import from_evidence
from nss_base.generation_store import Generations
from nss_base.neural_contracts import fingerprint
from nss_base.overlaygenerationmanager001 import OPERATORS
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications
from nss_base.qualificationevidence002 import AT, review_for
from nss_base.runtime import ContractError

_CACHE = None


def generation_fixture():
    global _CACHE
    if _CACHE is not None: return _CACHE
    root, _, _, backup = base_fixture()
    shutil.rmtree(root); shutil.copytree(backup, root)
    q = Qualifications(root/'q'); source = NeuralEvidence(root/'probe/journal', root/'probe/data')
    req = source.propose(run_id='probe-001', seed=101, precision='fp32',
        scope={'kind':'TRANSITION','source':'A','destination':'CORE','mode':'replay'},
        producer_id='fixture-builder', request_id='core-return', at=AT, prerequisites=['core','a'])
    q.prepare(req, source=source)
    assert q.decide(review_for(req), source=source)['verdict'] == 'QUALIFIED'
    manager = Generations.create(root/'generations', OPERATORS)
    manifests = [from_evidence('overlays-1','fixture-builder',['core','a'],['core-return'],qualifications=q),
                 from_evidence('overlays-2','fixture-builder',['core','a','ab'],['edge','core-return'],qualifications=q)]
    for g in manifests:
        manager.propose(g, qualifications=q, source=source)
        manager.qualify(fingerprint(g), reviewer_id='generation-reviewer', qualifications=q, source=source)
    snapshot = tempfile.TemporaryDirectory(prefix='generation-tests-'); atexit.register(snapshot.cleanup)
    shutil.copytree(root, Path(snapshot.name)/'fixture')
    _CACHE = (root, Path(snapshot.name)/'fixture', manifests)
    return _CACHE


class GenerationCase(unittest.TestCase):
    def setUp(self):
        if not HAVE_TORCH: self.skipTest('Optional PyTorch unavailable')
        root, backup, gs = generation_fixture()
        shutil.rmtree(root); shutil.copytree(backup, root)
        self.root = root; self.gs = deepcopy(gs); self.hashes = [fingerprint(g) for g in gs]
        self.q = Qualifications(root/'q'); self.source = NeuralEvidence(root/'probe/journal', root/'probe/data')
        self.manager = Generations(root/'generations'); self.ev = {'qualifications':self.q,'source':self.source}
        self.clock = int(time.time()) + 20
        p = patch('nss_base.generation_store.now_seconds', side_effect=lambda: self.clock)
        p.start(); self.addCleanup(p.stop)

    def error(self, code, fn, *args, **kwargs):
        with self.assertRaises(ContractError) as caught: fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code, str(caught.exception))

    def request(self, target=0, id='release-1', mode='BOOTSTRAP'):
        return self.manager.make_request(self.hashes[target], release_id=id, caller_id='local-runner', mode=mode, reason='Test release')

    def issued(self, target=0, id='release-1', mode='BOOTSTRAP'):
        r = self.request(target, id, mode)
        s = self.manager.issue(r, issuer_id='release-owner', ttl_seconds=300, **self.ev)
        return id, {'grant_sha256':fingerprint(s['grant']), 'caller_id':'local-runner', **self.ev}

    def adopted(self, target=0, id='release-1', mode='BOOTSTRAP'):
        id, opts = self.issued(target, id, mode)
        for f in (self.manager.prepare, self.manager.stage, self.manager.publish): f(id, **opts)
        return id, opts

    def withdraw_child(self, id='core'):
        c = self.q.inspect(id)['certificate']
        return self.q.revoke({'schema_version':1, 'operation_id':'revoke-'+id, 'request_id':id,
            'certificate_sha256':fingerprint(c), 'reviewer_id':'fixture-reviewer', 'at':AT,'reason':'Test withdrawal'})
