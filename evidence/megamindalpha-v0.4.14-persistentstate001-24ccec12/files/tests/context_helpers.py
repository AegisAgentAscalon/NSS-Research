"""Shared synthetic context fixture using the real task owner and reviewed archive."""
from copy import deepcopy
import shutil
from catalog_helpers import CatalogCase, CALLER
from dataset_helpers import capture_request, change, ok
from nss_base.catalog_controller import CatalogController
from nss_base.context_contracts import make_request
from nss_base.context_service import ContextService
from nss_base.experience_store import ExperienceArchive
from nss_base.neural_contracts import fingerprint


class ContextCase(CatalogCase):
    def setUp(self):
        super().setUp()
        source = self.root/'context-sources'; shutil.copytree(self.sources, source)
        self.sources = source
        self.ctl = CatalogController(self.manager, ledger=self.ledger, evidence_root=source, **self.ev)
        self.archive = ExperienceArchive.create(self.root/'context-archive')
        self.service = ContextService(self.ctl, archive=self.archive)

    def start_context(self, mutate=None):
        command = self.start_command()
        if mutate:
            mutate(command['record'])
            command['request']['stage']=deepcopy(command['record']['stage'])
        self.ctl.apply(command)
        return make_request(self.read(), CALLER)

    def add_experience(self, req, id='exp1', *, required=False, priority=0, statement=None, content=None, allowed=True):
        ok(self.archive.capture(capture_request(id, text=statement, source=content)))
        ok(change(self.archive,id,'REVIEW',{'decision':'APPROVED'}))
        if allowed: ok(change(self.archive,id,'PERMISSION',{'purpose':'retrieval','decision':'ALLOWED','permission_ref':'fixture:read'}))
        ref=ok(self.archive.inspect(id))['reference']
        req['archive_binding']=ok(self.archive.binding())
        req['experiences'].append({'reference':ref,'required':required,'priority':priority})
        req['experiences'].sort(key=lambda c:c['reference']['experience_id'])
        return ref

    def consume(self, packet, caller=CALLER):
        return self.service.consume(packet, caller_id=caller, expected_packet_sha256=fingerprint(packet))

    def built(self, req):
        return ok(self.service.build(req))

    def rejected(self, code, result):
        self.assertEqual(result['status'],code,result); self.assertIsNone(result['data']); return result
