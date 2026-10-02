"""Read-only bounded context service on existing public task and experience owners.

No new DB, task pointer, permission store, learned retrieval or optimizer. Returned
bytes are not recallable. Freshness checks are point-in-time, not cross-store leases.
"""
from copy import deepcopy
from functools import wraps
from .catalog_controller import CatalogController
from .catalog_contracts import require_state_identity
from .context_contracts import request, packet, seal
from .context_plan import EvidenceReader, assemble, unwrap
from .experience_store import ExperienceArchive
from .neural_contracts import fields, fingerprint
from .qualification_contracts import digest_value
from .experience_contracts import identifier, bounded_copy
from .runtime import ContractError, fail


def _public(method):
    @wraps(method)
    def call(*args, **kw):
        try:
            return {'status': 'SUCCESS', 'data': method(*args, **kw), 'detail': '', 'recovery': None}
        except ContractError as e:
            return {'status': e.code, 'data': None, 'detail': str(e), 'recovery': getattr(e, 'recovery', None)}
        except (OSError, UnicodeError, RecursionError) as e:
            return {'status': 'INTERNAL_FAILURE', 'data': None,
                'detail': 'Context read failed: '+type(e).__name__, 'recovery': None}
    return call


class ContextService:
    def __init__(self, controller, *, archive=None):
        if type(controller) is not CatalogController or (archive is not None and type(archive) is not ExperienceArchive):
            fail('VALIDATION_FAILED', 'Use installed task and optional experience owners')
        self.controller = controller; self.archive = archive

    def _view(self, req):
        v = self.controller.read(req['ticket'], caller_id=req['caller_id'],
            expected_record_sha256=req['expected_record_sha256'], scope=req.get('state_scope'))
        require_state_identity(req['expected_task_state_identity'], v)
        return v

    def _build(self, value):
        req = request(value); view = self._view(req)
        if req['experiences']:
            if self.archive is None: fail('INSUFFICIENT_EVIDENCE', 'Requested experience owner is unavailable')
            if unwrap(self.archive.binding()) != req['archive_binding']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Context uses a different archive owner')
        reader = EvidenceReader(self.controller.inputs['evidence_root'], self.archive, view['record'],
                                req['budget']['max_evidence_bytes'])
        payload, omissions = assemble(req, view, reader)
        # An operation-local cache is not permission. Revalidate selected records as
        # one batch and the live stage after assembly, before any payload is returned.
        selected = [e['reference'] for e in payload['experiences']]
        if selected: unwrap(self.archive.read_batch_for_use(selected, purpose='retrieval'))
        reader.verify_files()
        if self._view(req)['task_state_identity'] != view['task_state_identity']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Task changed during context assembly')
        return seal(req, view, payload, omissions, reader.used)

    @_public
    def build(self, value):
        return self._build(value)

    def _consume(self, value, caller_id, expected_packet_sha256):
        digest_value(expected_packet_sha256); p = packet(value)
        if fingerprint(p) != expected_packet_sha256: fail('VALIDATION_FAILED', 'Packet bytes differ from requested digest')
        if caller_id != p['request']['caller_id']: fail('AUTHORIZATION_DENIED', 'Packet belongs to a different caller')
        current = self._build(p['request'])
        if current != p:
            fail('INCOMPATIBLE_CONFIGURATION', 'Context inputs changed; explicitly build a new packet')
        return p

    @_public
    def consume(self, value, *, caller_id, expected_packet_sha256):
        p = self._consume(value, caller_id, expected_packet_sha256)
        return {'packet_sha256': fingerprint(p), 'task_state_identity': p['binding']['task_state_identity'],
                'payload': deepcopy(p['payload']), 'context_bytes': p['usage']['context_bytes'],
                'runtime_execution_permit': False, 'training_authorized': False}

    @_public
    def rehydrate(self, value, *, caller_id, expected_packet_sha256, selector):
        """Expand an already-selected exact reference, never its whole archive.

        The new packet must fit the original explicit budget. The prior packet and
        TaskRecord are never edited; failure returns no partial new context.
        """
        p = self._consume(value, caller_id, expected_packet_sha256); req = deepcopy(p['request'])
        if type(selector) is not dict or selector.get('kind') not in ('TASK_FIELD', 'EXPERIENCE_SLICE'):
            fail('VALIDATION_FAILED', 'Specify an exact task field or approved evidence slice')
        selector = bounded_copy(selector)
        if selector['kind'] == 'TASK_FIELD':
            fields(selector, ('kind','source_id','field_id'))
            identifier(selector['source_id']); identifier(selector['field_id'])
            if selector['source_id'] not in {s['id'] for s in p['payload']['sources']}:
                fail('INSUFFICIENT_EVIDENCE', 'Source is not referenced by this packet')
            s = {k:selector[k] for k in ('source_id','field_id')}
            if s not in req['source_fields']: req['source_fields'].append(s)
            req['source_fields'].sort(key=lambda s: (s['source_id'],s['field_id']))
        else:
            fields(selector, ('kind','experience_id','source_id','source_sha256','start_byte','end_byte'))
            identifier(selector['experience_id']); identifier(selector['source_id']); digest_value(selector['source_sha256'])
            ev = next((e for e in p['payload']['experiences'] if e['reference']['experience_id']==selector['experience_id']),None)
            if ev is None or not any(s['id']==selector['source_id'] and s['sha256']==selector['source_sha256'] for s in ev['sources']):
                fail('INSUFFICIENT_EVIDENCE', 'Source is not in the selected permitted experience')
            s={k:v for k,v in selector.items() if k!='kind'}
            if s not in req['evidence_slices']: req['evidence_slices'].append(s)
            req['evidence_slices'].sort(key=lambda s:(s['experience_id'],s['source_id'],s['start_byte'],s['end_byte']))
        return self._build(req)
