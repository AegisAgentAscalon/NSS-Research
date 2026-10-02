"""Current-role context still goes through the original purpose-aware archive."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest
from dataset_helpers import capture_request, change, revoke, ok
from nss_base.experience_store import ExperienceArchive
from nss_base.foundation_demo import setup, live_view
from nss_base.foundation_runner import CycleRunner
from nss_base.context_service import ContextService
from nss_base.context_contracts import make_request
from nss_base.neural_contracts import fingerprint
from nss_base.runtime import ContractError


class FoundationArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'run'
        self.store,service,_,self.adapters,_=setup(self.root)
        self.archive=ExperienceArchive.create(self.root/'archive')
        self.service=ContextService(service.controller,archive=self.archive)
        self.runner=CycleRunner(self.store,self.service,self.adapters)
        ok(self.archive.capture(capture_request('exp1')))
        ok(change(self.archive,'exp1','REVIEW',{'decision':'APPROVED'}))
        ok(change(self.archive,'exp1','PERMISSION',{'purpose':'retrieval','decision':'ALLOWED','permission_ref':'test:retrieval-only'}))
        self.ref=ok(self.archive.inspect('exp1'))['reference']
        self.request=make_request(live_view(self.store,self.root),'builder')
        self.request['archive_binding']=ok(self.archive.binding())
        self.request['experiences']=[{'reference':self.ref,'required':True,'priority':0}]

    def packet(self):return ok(self.service.build(self.request))

    def test_original_archive_retrieval_in_current_role_context(self):
        p=self.packet();self.assertEqual(p['payload']['experiences'][0]['reference'],self.ref)
        result=self.runner.run_tick(p,operation_id='archive-read',phase='TASK',experience_cutoff=1)
        self.assertIn(self.ref['sha256'],result['messages'][0]['source_references'])
        self.assertFalse(result['training_authorized'])

    def test_retrieval_permission_does_not_grant_training(self):
        self.packet()
        self.assertEqual(self.archive.read_for_use('exp1',purpose='training',expected_revision_hash=self.ref['sha256'])['status'],'TRAINING_RESTRICTED')

    def test_revoked_archive_source_blocks_context_consumption(self):
        p=self.packet();ok(revoke(self.archive,purpose='retrieval'))
        result=self.service.consume(p,caller_id='builder',expected_packet_sha256=fingerprint(p))
        self.assertEqual(result['status'],'TRAINING_RESTRICTED');self.assertIsNone(result['data'])

    def test_archive_revocation_during_callback_prevents_state_commit(self):
        p=self.packet();old=self.adapters['SECONDARY'].step
        def revoke_midway(req,state):
            out=old(req,state);ok(revoke(self.archive,purpose='retrieval'));return out
        with patch.object(self.adapters['SECONDARY'],'step',side_effect=revoke_midway):
            with self.assertRaises(ContractError) as e:
                self.runner.run_tick(p,operation_id='revocation-race',phase='TASK',experience_cutoff=1)
        self.assertEqual(e.exception.code,'TRAINING_RESTRICTED')
        view=live_view(self.store,self.root);self.assertEqual(view['ticks'],0);self.assertEqual(view['states'],{})

    def test_wrong_archive_binding_rejected(self):
        other=ExperienceArchive.create(self.root/'other-archive');self.request['archive_binding']=ok(other.binding())
        self.assertEqual(self.service.build(self.request)['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_withdrawn_required_experience_is_not_silently_omitted(self):
        p=self.packet();ok(change(self.archive,'exp1','WITHDRAW',{}))
        result=self.service.consume(p,caller_id='builder',expected_packet_sha256=fingerprint(p))
        self.assertNotEqual(result['status'],'SUCCESS');self.assertIsNone(result['data'])


if __name__=='__main__':unittest.main()
