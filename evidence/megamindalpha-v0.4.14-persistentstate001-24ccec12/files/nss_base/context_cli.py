"""Explicit point-in-time context reads. No implicit training, actions, or publishing.

Output is JSON to stdout. Saved packets are historical bytes until consume performs
fresh owner checks. Exported bytes cannot be recalled by later revocation.
"""
import argparse
import sys
from .catalog_controller import CatalogController
from .context_service import ContextService
from .experience_store import ExperienceArchive
from .generation_store import Generations
from .ledger import Ledger
from .neural_contracts import encoded, read_document
from .qualification_sources import add_source_arguments, source_from_args
from .qualification_store import Qualifications
from .runtime import ContractError


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('store','qualification','ledger','sources'):p.add_argument('--'+key,required=True)
    add_source_arguments(p)
    p.add_argument('--archive')
    sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('build');b.add_argument('--request',required=True)
    for name in ('consume','rehydrate'):
        c=sub.add_parser(name);c.add_argument('--packet',required=True);c.add_argument('--caller',required=True)
        c.add_argument('--packet-hash',required=True)
        if name=='rehydrate':c.add_argument('--selector',required=True)
    a=p.parse_args(argv)
    try:
        archive=ExperienceArchive(a.archive) if a.archive else None
        ctl=CatalogController(Generations(a.store),qualifications=Qualifications(a.qualification),
            source=source_from_args(a),ledger=Ledger(a.ledger),evidence_root=a.sources,archive=archive)
        service=ContextService(ctl,archive=archive)
        if a.command=='build':r=service.build(read_document(a.request))
        else:
            kwargs={'caller_id':a.caller,'expected_packet_sha256':a.packet_hash}
            if a.command=='rehydrate':kwargs['selector']=read_document(a.selector)
            r=getattr(service,a.command)(read_document(a.packet),**kwargs)
        print(encoded(r).decode());return 0 if r['status']=='SUCCESS' else 1
    except (ContractError,OSError) as e:
        print(encoded({'status':getattr(e,'code','INTERNAL_FAILURE'),'data':None,'detail':str(e)}).decode(),file=sys.stderr)
        return 1


if __name__=='__main__':raise SystemExit(main())
