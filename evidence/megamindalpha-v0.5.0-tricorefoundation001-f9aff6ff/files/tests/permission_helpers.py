"""Real qualification fixture + isolated local grant/result owners."""
from copy import deepcopy
from unittest.mock import patch
import time
from qualification_helpers import QualificationCase
from nss_base.ledger import Ledger
from nss_base.neural_contracts import fingerprint
from nss_base.permission_executor import ReplayExecutor
from nss_base.permission_store import Permissions
from nss_base.permission_replay import prepare_request, execute_once
from nss_base.localnexuspermissions002 import OPERATORS


class PermissionCase(QualificationCase):
    def setUp(self):
        super().setUp()
        self.permits = Permissions.create(self.root/'permissions', OPERATORS)
        self.executor = ReplayExecutor.create(self.root/'executor')
        self.ledger = Ledger(self.root/'probe/mock_actions')
        self.clock = int(time.time()) + 10
        self.clock_patch = patch('nss_base.permission_store.now_seconds', side_effect=lambda: self.clock)
        self.clock_patch.start(); self.addCleanup(self.clock_patch.stop)
        self.operation = prepare_request(qualifications=self.q, source=self.source, qualification_id='edge',
            request_id='permission-1', caller_id='local-runner', task_id='neural-probe-replay', ledger=self.ledger)

    def issue(self, req=None, **kw):
        opts = {'issuer_id':'local-owner','ttl_seconds':100,'qualifications':self.q,'source':self.source}
        opts.update(kw)
        return self.permits.issue(req or self.operation, **opts)

    def granted(self):
        s = self.issue(); return fingerprint(s['grant'])

    def begin(self, h, req=None, **kw):
        opts = {'grant_sha256':h,'caller_id':'local-runner','qualifications':self.q,'source':self.source}
        opts.update(kw); return self.permits.begin(req or self.operation, **opts)

    def dispatch(self, h, **kw):
        opts = {'grant_sha256':h,'caller_id':'local-runner','qualifications':self.q,'source':self.source}
        opts.update(kw); return self.permits.check_dispatch(self.operation, **opts)

    def execute_permission(self, h, req=None, **kw):
        opts = {'grant_sha256':h,'caller_id':'local-runner','qualifications':self.q,'source':self.source,
                'executor':self.executor,'ledger':self.ledger}
        opts.update(kw); return execute_once(self.permits, req or self.operation, **opts)

    def withdraw(self, h, **kw):
        opts = {'grant_sha256':h,'actor_id':'local-owner','revocation_id':'withdraw-1','reason':'Test local revocation'}
        opts.update(kw); return self.permits.revoke(self.operation['request_id'], **opts)

    def reconcile(self, h, **kw):
        opts = {'grant_sha256':h,'actor_id':'local-owner','executor':self.executor,'reconcile':True}
        opts.update(kw); return self.permits.finish(self.operation, **opts)
