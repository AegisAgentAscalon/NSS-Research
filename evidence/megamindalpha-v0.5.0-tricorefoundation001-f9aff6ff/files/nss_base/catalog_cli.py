"""Explicit trusted-local catalogue/task CLI. No implicit model training or effects."""
import argparse
import sys
from .catalog_controller import CatalogController
from .generation_store import Generations
from .experience_store import ExperienceArchive
from .ledger import Ledger
from .neural_contracts import encoded, read_document
from .qualification_sources import add_source_arguments, source_from_args
from .qualification_store import Qualifications
from .runtime import ContractError


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--store', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('inspect'); c.add_argument('--task', required=True); c.add_argument('--caller'); c.add_argument('--scope')
    c = sub.add_parser('state-history'); c.add_argument('--task', required=True); c.add_argument('--caller',required=True); c.add_argument('--scope',required=True)
    c = sub.add_parser('catalog'); c.add_argument('--current', required=True); c.add_argument('--catalog-hash')
    c = sub.add_parser('register'); c.add_argument('--descriptor', required=True); c.add_argument('--reviewer', required=True)
    c = sub.add_parser('select'); c.add_argument('--request', required=True); c.add_argument('--caller', required=True)
    c.add_argument('--ticket'); c.add_argument('--record-hash'); c.add_argument('--scope')
    c = sub.add_parser('apply'); c.add_argument('--operation', required=True)
    c = sub.add_parser('read'); c.add_argument('--ticket', required=True); c.add_argument('--caller', required=True); c.add_argument('--record-hash', required=True); c.add_argument('--scope')
    for name in ('catalog', 'register', 'select', 'apply', 'read'):
        c = sub.choices[name]
        for key in ('qualification', 'ledger', 'sources'):
            c.add_argument('--' + key, required=True)
        c.add_argument('--archive')
        add_source_arguments(c)
    a = p.parse_args(argv)
    try:
        manager = Generations(a.store)
        if a.command in ('inspect','state-history'):
            method=manager.inspect_task if a.command=='inspect' else manager.inspect_state_history
            result=method(a.task,caller_id=a.caller,scope=read_document(a.scope) if a.scope else None)
        else:
            ctl = CatalogController(manager, qualifications=Qualifications(a.qualification),
                source=source_from_args(a), ledger=Ledger(a.ledger), evidence_root=a.sources,archive=ExperienceArchive(a.archive) if a.archive else None)
            if a.command == 'catalog': result = ctl.catalog(expected_current=read_document(a.current), catalog_sha256=a.catalog_hash)
            elif a.command == 'register': result = ctl.register(read_document(a.descriptor), reviewer_id=a.reviewer)
            elif a.command == 'select': result = ctl.select(read_document(a.request), caller_id=a.caller,
                source_ticket=read_document(a.ticket) if a.ticket else None, expected_record_sha256=a.record_hash,scope=read_document(a.scope) if a.scope else None)
            elif a.command == 'apply': result = ctl.apply(read_document(a.operation))
            else: result = ctl.read(read_document(a.ticket), caller_id=a.caller, expected_record_sha256=a.record_hash,scope=read_document(a.scope) if a.scope else None)
        print(encoded(result).decode()); return 0
    except (ContractError, OSError) as e:
        print(encoded({'status': getattr(e, 'code', 'RECOVERY_REQUIRED'), 'detail': str(e), 'recovery':getattr(e,'recovery',None)}).decode(), file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
