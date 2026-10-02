"""Pure generation lifecycle reducer. No filesystem, neural execution or authority I/O.

A complete journal reconstructs current pointer, archive, grants and open managed
stages. There is no independently writable 'current' or revocation cache to drift.
"""
from copy import deepcopy
from .generation_contracts import (artifact_bundle, configuration, exact, generation,
    generation_certificate, release_grant, release_request, role)
from .neural_contracts import fields, fingerprint
from .qualification_contracts import digest_value, identifier, text
from .runtime import fail


# Re-export prior query names for callers; implementations have one owner.
from .generation_views import (family, qualified, source_matches, core_identity,
    release, usable, quiescent, ticket_for, receipt_for)
from .catalog_tasks import reduce_catalog_event


def reduce_events(m, events):
    s = {'generations': {}, 'releases': {}, 'tickets': {}, 'published': {},
         'current': {'epoch': 0, 'generation_sha256': None}, 'core_identity': None,
         'catalogs': {}, 'task_heads': {}, 'task_operations': {}}
    names = set()
    for event in events:
        kind, b, at = event['kind'], event['body'], event['at']
        if kind == 'PROPOSE':
            g = generation(b); role(m, g['producer_id'], 'PRODUCER'); h = fingerprint(g)
            if h in s['generations'] or g['generation_id'] in names:
                fail('VALIDATION_FAILED', 'Released names and manifests cannot be overwritten')
            names.add(g['generation_id'])
            s['generations'][h] = {'manifest': g, 'certificate': None, 'revoked': False}
        elif kind == 'QUALIFY':
            fields(b, ('generation_sha256', 'certificate'))
            f = family(s, b['generation_sha256']); c = b['certificate']
            if f['certificate'] is not None: fail('VALIDATION_FAILED', 'Qualification is immutable')
            if type(c) is not dict or 'reviewer_id' not in c: fail('VALIDATION_FAILED', 'Missing reviewer')
            exact(c, generation_certificate(f['manifest'], c['reviewer_id'], at, m)); f['certificate'] = c
        elif kind == 'ISSUE':
            fields(b, ('request', 'grant')); req = release_request(b['request']); g = b['grant']
            if type(g) is not dict or not {'issuer_id', 'expires_at'} <= g.keys():
                fail('VALIDATION_FAILED', 'Invalid release grant')
            exact(g, release_grant(req, g['issuer_id'], at, g['expires_at'], m))
            if req['release_id'] in s['releases']: fail('VALIDATION_FAILED', 'Release ID reuse')
            f = qualified(s, req['target_sha256']); source_matches(s, req)
            if req['generation_certificate_sha256'] != fingerprint(f['certificate']):
                fail('INCOMPATIBLE_CONFIGURATION', 'Wrong generation certificate')
            s['releases'][req['release_id']] = {'request': req, 'grant': g, 'status': 'GRANTED',
                'revoked': False, 'artifacts': None, 'receipt': None}
        elif kind in ('REVOKE_RELEASE', 'REVOKE_QUALIFICATION'):
            fields(b, ('id', 'actor_id', 'reason')); text(b['reason'])
            if kind == 'REVOKE_RELEASE':
                role(m, b['actor_id'], 'ISSUER'); obj = release(s, b['id'])
            else:
                role(m, b['actor_id'], 'REVIEWER'); obj = family(s, b['id'])
            obj['revoked'] = True
        elif kind in ('PREPARE', 'STAGE', 'PUBLISH', 'ABANDON'):
            keys = ('release_id', 'caller_id') + (('artifacts',) if kind == 'STAGE' else
                   ('receipt',) if kind == 'PUBLISH' else ('reason',) if kind == 'ABANDON' else ())
            fields(b, keys); r = release(s, b['release_id']); role(m, b['caller_id'], 'OPERATOR')
            if b['caller_id'] != r['request']['caller_id']: fail('AUTHORIZATION_DENIED', 'Wrong release caller')
            if kind == 'ABANDON':
                text(b['reason'])
                if r['status'] not in ('GRANTED', 'PREPARED', 'STAGED'):
                    fail('VALIDATION_FAILED', 'Cannot abandon finalized release')
                r['status'] = 'ABANDONED'; continue
            usable(s, r, at); quiescent(s)
            expected = {'PREPARE': 'GRANTED', 'STAGE': 'PREPARED', 'PUBLISH': 'STAGED'}[kind]
            if r['status'] != expected: fail('VALIDATION_FAILED', 'Invalid release lifecycle edge')
            if kind == 'PREPARE': r['status'] = 'PREPARED'
            elif kind == 'STAGE':
                f = family(s, r['request']['target_sha256'])
                r['artifacts'] = artifact_bundle(b['artifacts'], f['manifest']); r['status'] = 'STAGED'
            else:
                exact(b['receipt'], receipt_for(s, r)); r['receipt'] = b['receipt']; r['status'] = 'PUBLISHED'
                s['current'] = configuration(b['receipt']['current'])
                s['published'][s['current']['generation_sha256']] = b['release_id']
                s['core_identity'] = core_identity(family(s, s['current']['generation_sha256'])['manifest'])
        elif kind in ('CATALOG_REGISTER', 'CATALOG_TASK'):
            reduce_catalog_event(m, s, event)
        elif kind == 'PIN':
            fields(b, ('ticket',)); t = b['ticket']
            if type(t) is not dict or not {'caller_id', 'ticket_id', 'profile'} <= t.keys():
                fail('VALIDATION_FAILED', 'Malformed managed stage ticket')
            role(m, t['caller_id'], 'OPERATOR'); quiescent(s)
            if t['ticket_id'] in s['tickets']: fail('VALIDATION_FAILED', 'Stage identity reuse')
            exact(t, ticket_for(s, m['store_id'], t['ticket_id'], t['profile'], t['caller_id']))
            s['tickets'][t['ticket_id']] = {'ticket': t, 'closed': False}
        elif kind == 'UNPIN':
            fields(b, ('ticket',)); t = b['ticket']
            if type(t) is not dict or 'ticket_id' not in t or t['ticket_id'] not in s['tickets']:
                fail('VALIDATION_FAILED', 'Unknown stage ticket')
            saved = s['tickets'][t['ticket_id']]
            exact(saved['ticket'], t)
            if saved['closed']: fail('VALIDATION_FAILED', 'Duplicate stage close event')
            if 'work' in saved:
                fail('CONSTRAINT_CONFLICT', 'Managed task must finish/cancel through its TaskRecord API')
            saved['closed'] = True
        else:
            fail('VALIDATION_FAILED', 'Unknown generation journal event')
    return s
