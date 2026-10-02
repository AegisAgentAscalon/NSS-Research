"""Reuse the once-trained and qualified numerical fixture; no fabricated scores."""
import atexit
from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
from qualification_helpers import QualificationCase
from nss_base.boundedlearnercoordinator001 import OPERATORS, local_config, plan_from_reviewed_data
from nss_base.learner_cli import initialize, open_learner
from nss_base.neural_data import ProbeData
from nss_base.neural_contracts import fingerprint
from nss_base.learner_contracts import operation_id

CACHE=None
CLOCK=2000000000


class LearnerCase(QualificationCase):
    def setUp(self):
        global CACHE
        super().setUp()
        if CACHE is None:
            ProbeData.create(self.root/'learning-data')
            # Fixture's qualification store has its own original name, q.
            self.config=local_config(self.root);self.config['qualifications']=str(self.root/'q')
            initialize(self.config,OPERATORS)
            self.co=open_learner(self.config,clock=lambda:CLOCK)
            temp=tempfile.TemporaryDirectory(prefix='learner-fixture-');atexit.register(temp.cleanup)
            shutil.copytree(self.root,Path(temp.name)/'fixture')
            CACHE=Path(temp.name)/'fixture',self.config
        else:
            path,self.config=CACHE;self.config=deepcopy(self.config)
            shutil.rmtree(self.root);shutil.copytree(path,self.root)
            self.co=open_learner(self.config,clock=lambda:CLOCK)
        self.plan=plan_from_reviewed_data(self.co,steps=180)
        self.data=ProbeData(self.root/'learning-data')

    def ready(self,**kwargs):
        p=deepcopy(self.plan);p.update(kwargs);self.co.prepare(p)
        self.co.cycles.approve(p['cycle_id'],approver_id='human-operator',expires_at=CLOCK+600,at=CLOCK)
        return p

    def complete(self):
        self.ready();return self.co.advance(self.plan['cycle_id'],caller_id='learner-worker')

    def candidate(self):return self.co.training.inspect(operation_id(self.plan,'TRAIN'))
    def evaluation(self):return self.co.evaluations.inspect(operation_id(self.plan,'EVALUATE'))
