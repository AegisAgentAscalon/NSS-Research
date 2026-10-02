"""Process-exit probes for read-only context assembly; no production fault switch."""
from pathlib import Path
import os
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nss_base.catalog_controller import CatalogController
from nss_base.context_service import ContextService
from nss_base.experience_store import ExperienceArchive
from nss_base.generation_store import Generations
from nss_base.ledger import Ledger
from nss_base.neural_contracts import encoded, fingerprint, read_document
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications

root=Path(sys.argv[1]);mode=sys.argv[2]
archive=ExperienceArchive(root/'context-archive')
controller=CatalogController(Generations(root/'generations'),qualifications=Qualifications(root/'q'),
    source=NeuralEvidence(root/'probe/journal',root/'probe/data'),ledger=Ledger(root/'probe/mock_actions'),evidence_root=root/'context-sources')
service=ContextService(controller,archive=archive)
if mode=='after_task_read':
    old=service._view
    def die(req):old(req);os._exit(81)
    service._view=die
elif mode=='after_archive_read':
    old=archive.read_batch_for_use
    def die(*a,**kw):old(*a,**kw);os._exit(81)
    archive.read_batch_for_use=die
elif mode=='before_return':
    import nss_base.context_service as module
    old=module.seal
    def die(*a,**kw):old(*a,**kw);os._exit(81)
    module.seal=die
if mode=='consume':
    p=read_document(root/'saved-context.json')
    r=service.consume(p,caller_id='local-runner',expected_packet_sha256=fingerprint(p))
else:r=service.build(read_document(root/'context-request.json'))
print(encoded(r).decode());raise SystemExit(0 if r['status']=='SUCCESS' else 1)
