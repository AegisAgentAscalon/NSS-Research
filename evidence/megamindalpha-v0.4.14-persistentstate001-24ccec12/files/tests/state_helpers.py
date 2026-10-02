"""Reuse real catalogue/experience fixtures; scoped state adds no other store."""
from copy import deepcopy
from context_helpers import ContextCase
from catalog_helpers import CALLER
from dataset_helpers import ok, capture_request, change
from nss_base.catalog_controller import CatalogController
from nss_base.context_contracts import make_request
from nss_base.context_service import ContextService
from nss_base.neural_contracts import fingerprint
from nss_base.state_contracts import prepare, attest, POLICY
from nss_base.generation_store import now_seconds

SCOPE={'agent_id':'test-cerys','project_id':'test-nss','session_id':'state-session-1'}
POLICY_DOC={'policy_id':POLICY,'instruction_policy_sha256':fingerprint({'root':'fixed test instructions'}),'max_record_bytes':65536}
REF={'kind':'TASK','source_id':'source-1','field_id':'speed'}


class StateCase(ContextCase):
    def setUp(self):
        super().setUp()
        self.ctl=CatalogController(self.manager,ledger=self.ledger,evidence_root=self.sources,archive=self.archive,**self.ev)
        self.service=ContextService(self.ctl,archive=self.archive)
        self.started()
        self.events=0

    def history(self):
        return self.ctl.inspect('catalog-task',caller_id=CALLER,scope=SCOPE)

    def state_view(self, *, live=True):
        h=self.history()
        if live:
            return self.ctl.read(h['ticket'],caller_id=CALLER,scope=SCOPE,
                expected_record_sha256=fingerprint(h['work']['record']))
        return {'ticket':h['ticket'],'record':h['work']['record']}

    def approve(self, c):
        t=self.clock
        return attest(c,reviewer_id='generation-reviewer',reviewed_at=t,expires_at=t+600,
                      reason='Scripted human declaration for fixture; no authenticated reviewer')

    def bind_command(self):
        v=super().read()
        return self.approve(prepare(v,operation_id='state-bind',proposer_id='fake-proposer',proposer_version='v1',
            state_scope=SCOPE,policy=POLICY_DOC,archive_binding=ok(self.archive.binding())))

    def bind(self):
        c=self.bind_command();self.ctl.apply(c);return c

    def proposal(self, deltas, *, op=None):
        self.events+=1
        return prepare(self.state_view(live=False),operation_id=op or 'update-'+str(self.events),
            proposer_id='fake-proposer',proposer_version='v1',state_scope=SCOPE,deltas=deltas)

    def updated(self, deltas, *, op=None):
        c=self.approve(self.proposal(deltas,op=op));return self.ctl.apply(c)

    def note(self, id='note-1', **kw):
        note={'id':id,'text':'Earlier speed observation matters to this task.', 'kind':'CLAIM',
            'status':'HYPOTHESIS','confidence':None,'mandatory':False,'identity_sensitive':False,'expires_at':None}
        note.update(kw)
        return {'op':'ADD_NOTE','source_refs':[deepcopy(REF)],'note':note}

    def life_command(self, action, **extra):
        h=self.history()
        self.events+=1
        c={'schema_version':2,'operation_id':'life-'+str(self.events),'caller_id':CALLER,'scope':deepcopy(SCOPE),
            'action':action,'source_ticket':h['ticket'],'expected_record_sha256':fingerprint(h['work']['record'])}
        if action=='FINISH':c.update(results=[],receipts=[])
        if action=='CANCEL':c.update(receipts=[],reason='Explicit scoped cancellation')
        c.update(extra);return c
