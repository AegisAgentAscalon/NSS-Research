"""One genuinely trained candidate fixture, restored per test at its pinned path."""
import atexit
from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch
from nss_base.boundedlearnercoordinator001 import prepare_learning_fixture
from nss_base.candidateacceptance001 import candidate_source, proposed_claims
from nss_base.generation_evidence import from_evidence
from nss_base.generation_store import Generations
from nss_base.learner_cli import open_learner
from nss_base.ledger import Ledger
from nss_base.neural_contracts import fingerprint
from nss_base.neural_data import ProbeData
from nss_base.qualificationevidence002 import AT, review_for
from nss_base.runtime import ContractError

_CACHE=None


def fixture():
    global _CACHE
    if _CACHE is None:
        import importlib.util
        if importlib.util.find_spec('torch') is None: raise unittest.SkipTest('Optional PyTorch not installed')
        temp=tempfile.TemporaryDirectory(prefix='candidate-acceptance-tests-');atexit.register(temp.cleanup)
        root=Path(temp.name)/'work';f=prepare_learning_fixture(root);co=f['co'];source=candidate_source(co)
        reqs=proposed_claims(source,f['plan'])
        for req in reqs:
            co.qualifications.prepare(req,source=source)
            assert co.qualifications.decide(review_for(req),source=source)['verdict']=='QUALIFIED'
        family=from_evidence('candidate-test-family','fixture-builder',[r['request_id'] for r in reqs[:3]],
            [r['request_id'] for r in reqs[3:]],qualifications=co.qualifications)
        f['manager'].propose(family,qualifications=co.qualifications,source=source)
        f['manager'].qualify(fingerprint(family),reviewer_id='generation-reviewer',qualifications=co.qualifications,source=source)
        backup=Path(temp.name)/'backup';shutil.copytree(root,backup)
        _CACHE=(root,backup,deepcopy(f['config']),deepcopy(f['plan']),family,reqs)
    return _CACHE


class CandidateCase(unittest.TestCase):
    def setUp(self):
        root,backup,config,plan,family,reqs=fixture()
        shutil.rmtree(root);shutil.copytree(backup,root)
        self.root=root;self.config=deepcopy(config);self.plan=deepcopy(plan)
        self.family=deepcopy(family);self.reqs=deepcopy(reqs);self.target=fingerprint(family)
        self.co=open_learner(config);self.q=self.co.qualifications;self.source=candidate_source(self.co)
        self.manager=Generations(root/'generations');self.ev={'qualifications':self.q,'source':self.source}
        self.parent_ev={'qualifications':self.q,'source':self.co.source}
        self.parent=self.manager.inspect()['current'];self.clock=int(time.time())+10
        self.clockpatch=patch('nss_base.generation_store.now_seconds',side_effect=lambda:self.clock)
        self.clockpatch.start();self.addCleanup(self.clockpatch.stop)

    def error(self,code,fn,*a,**kw):
        with self.assertRaises(ContractError) as e:fn(*a,**kw)
        self.assertEqual(e.exception.code,code,str(e.exception))

    def fresh(self,name='fresh-core',profile='CORE',prerequisites=()):
        return self.source.propose(run_id=self.plan['cycle_id'],seed=self.plan['recipe']['seed'],
            precision=self.plan['parent']['precision'],scope={'kind':'PROFILE','profile':profile},
            producer_id='fixture-builder',request_id=name,at=AT,prerequisites=prerequisites)

    def use(self,name='candidate-a2b',**override):
        r=self.q.inspect(name)
        args={'certificate_sha256':fingerprint(r['certificate']),'expected_claim':r['request']['claim'],
              'expected_binding':r['request']['binding'],'source':self.source}
        args.update(override);return self.q.check_use(name,**args)

    def withdraw(self,name='candidate-core'):
        c=self.q.inspect(name)['certificate']
        return self.q.revoke({'schema_version':1,'operation_id':'withdraw:'+name,'request_id':name,
            'certificate_sha256':fingerprint(c),'reviewer_id':'fixture-reviewer','at':AT,'reason':'Test withdrawal'})

    def request(self,name='candidate-release',target=None,mode='UPDATE'):
        return self.manager.make_request(target or self.target,release_id=name,caller_id='local-runner',mode=mode,reason='Test exact release')

    def issue(self,name='candidate-release'):
        req=self.request(name);r=self.manager.issue(req,issuer_id='release-owner',ttl_seconds=300,**self.ev)
        return {'caller_id':'local-runner','grant_sha256':fingerprint(r['grant']),**self.ev}

    def adopt(self,name='candidate-release'):
        opts=self.issue(name)
        for fn in (self.manager.prepare,self.manager.stage,self.manager.publish):fn(name,**opts)
        return opts

    def assert_no_training_or_effect(self):
        self.assertEqual(self.co.training.audit()['attempts'],1)
        self.assertEqual(Ledger(self.root/'probe/mock_actions').effect_count(),1)
