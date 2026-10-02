"""One reusable real-evidence fixture; no fabricated qualification results."""
from copy import deepcopy
from pathlib import Path
import atexit
import shutil
import tempfile
from generation_helpers import GenerationCase
from nss_base.catalog_controller import CatalogController, fixture_descriptor
from nss_base.neural_contracts import fingerprint, read_document, pairs
from nss_base.ledger import Ledger

ROOT = Path(__file__).resolve().parents[1]
DECLARATIONS = {
    'A': {'capabilities': ['shared', 'solve'], 'load_units': 2, 'step_units': 2, 'max_pairs': 64},
    'AB': {'capabilities': ['interpret', 'shared'], 'load_units': 4, 'step_units': 3, 'max_pairs': 64},
    'CORE': {'capabilities': ['control', 'identity'], 'load_units': 0, 'step_units': 1, 'max_pairs': 64},
}
CALLER = 'local-runner'
_CATALOG_FIXTURE = None


class CatalogCase(GenerationCase):
    def setUp(self):
        global _CATALOG_FIXTURE
        super().setUp()
        self.sources = ROOT/'fixtures/stagehandoff001'
        if _CATALOG_FIXTURE is None:
            self.adopted(1)
            self.ledger = Ledger(self.root/'probe/mock_actions')
            self.ctl = CatalogController(self.manager, ledger=self.ledger, evidence_root=self.sources, **self.ev)
            self.artifacts = self.manager.inspect_release('release-1')['artifacts']
            self.desc = fixture_descriptor(self.gs[1], self.artifacts, catalog_id='catalog-1',
                author_id='fixture-builder', declarations=deepcopy(DECLARATIONS))
            self.catalog_hash = self.ctl.register(self.desc, reviewer_id='generation-reviewer')['catalog_sha256']
            temp = tempfile.TemporaryDirectory(prefix='catalog-fixture-'); atexit.register(temp.cleanup)
            shutil.copytree(self.root, Path(temp.name)/'fixture')
            _CATALOG_FIXTURE = (Path(temp.name)/'fixture', self.desc, self.artifacts)
        else:
            path, self.desc, self.artifacts = _CATALOG_FIXTURE
            self.desc=deepcopy(self.desc); self.artifacts=deepcopy(self.artifacts)
            shutil.rmtree(self.root); shutil.copytree(path,self.root)
            from nss_base.generation_store import Generations
            self.manager=Generations(self.root/'generations')
            self.ledger=Ledger(self.root/'probe/mock_actions')
            self.ctl=CatalogController(self.manager,ledger=self.ledger,evidence_root=self.sources,**self.ev)
            self.catalog_hash=fingerprint(self.desc)

    def req(self, cap='interpret', stage='s1', mode='WORK', task='catalog-task'):
        return {'schema_version': 1, 'catalog_sha256': self.catalog_hash,
            'expected_current': self.manager.inspect()['current'], 'task_id': task,
            'stage': {'id': stage, 'mode': mode, 'sealed': False, 'objective': 'Fixture stage',
                'required_facts': [], 'requested_output': 'Preserve task state'},
            'capabilities': [cap], 'pairs': pairs('test')[:4],
            'budget': {'max_document_bytes': 1000000, 'max_cost_units': 10000}}

    def start_command(self, cap='interpret', mode='WORK', task='catalog-task'):
        req = self.req(cap=cap, mode=mode, task=task)
        record = read_document(self.sources/'task_record.json')
        record.update(task_id=task, stage=deepcopy(req['stage']))
        record['receipts'] = [{'key': k, 'kind': 'mock_action', 'receipt': self.ledger.inspect(k)['receipt']}
                              for k in self.ledger.action_keys(task)]
        return {'schema_version': 1, 'action': 'START', 'operation_id': 'start:'+task,
            'caller_id': CALLER, 'ticket_id': 'ticket:'+task, 'request': req, 'record': record}

    def started(self, **kw):
        c = self.start_command(**kw); r = self.ctl.apply(c)
        return c, r

    def command(self, action, *, task='catalog-task', op=None, **extras):
        v = self.ctl.inspect(task)
        c = {'schema_version': 1, 'action': action, 'operation_id': op or action.lower()+':'+v['ticket']['ticket_id'],
            'caller_id': CALLER, 'source_ticket': v['ticket'], 'expected_record_sha256': fingerprint(v['work']['record'])}
        if action == 'FINISH': c.update(results=[], receipts=[])
        elif action == 'CANCEL': c.update(receipts=[], reason='Explicit local cancellation retaining evidence')
        c.update(extras); return c

    def finished(self, task='catalog-task'):
        return self.ctl.apply(self.command('FINISH', task=task))

    def move_command(self, cap='solve', stage='s2', mode='WORK', task='catalog-task'):
        return self.command('MOVE', task=task, op='move:'+stage,
            ticket_id='ticket:'+stage, request=self.req(cap=cap, stage=stage, mode=mode, task=task))

    def read(self, task='catalog-task'):
        v = self.ctl.inspect(task)
        return self.ctl.read(v['ticket'], caller_id=CALLER, expected_record_sha256=fingerprint(v['work']['record']))
