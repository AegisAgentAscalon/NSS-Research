"""Pure generation-state queries shared by release and task reducers.

These are storage-owner internals, not a second catalogue or authority.
"""
from copy import deepcopy
from .neural_contracts import fingerprint
from .qualification_contracts import digest_value, identifier
from .runtime import fail


def family(s, key):
    digest_value(key)
    if key not in s['generations']:
        fail('INSUFFICIENT_EVIDENCE', 'Unknown exact generation')
    return s['generations'][key]


def qualified(s, key):
    f = family(s, key)
    if f['certificate'] is None:
        fail('INSUFFICIENT_EVIDENCE', 'Generation-wide closure has not been reviewed')
    if f['revoked']:
        fail('AUTHORIZATION_DENIED', 'Generation qualification withdrawn')
    return f


def source_matches(s, req):
    if req['expected_current'] != s['current']:
        fail('CONSTRAINT_CONFLICT', 'Source pointer changed; a new release request is required')
    target = family(s, req['target_sha256'])['manifest']
    if s['core_identity'] is not None and core_identity(target) != s['core_identity']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Overlay release cannot replace the Primary Core package')
    if req['mode'] == 'ROLLBACK' and req['target_sha256'] not in s['published']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Rollback requires an exact previously published generation')
    if req['mode'] == 'UPDATE' and req['target_sha256'] in s['published']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Returning to a historical generation requires explicit ROLLBACK')


def core_identity(g):
    b = g['binding']
    return fingerprint({k: b[k] for k in ('core_generation', 'tokenizer', 'context_abi', 'overlay_abi', 'precision')} |
                       {'core_sha256': b['checkpoint_hashes']['core']})


def release(s, key):
    identifier(key)
    if key not in s['releases']: fail('INSUFFICIENT_EVIDENCE', 'Unknown exact release grant')
    return s['releases'][key]


def usable(s, r, at):
    g = r['grant']
    if r['status'] in ('PUBLISHED', 'ABANDONED'):
        fail('CONSTRAINT_CONFLICT', 'Grant already spent; only historical inspection is permitted')
    if r['revoked'] or not g['issued_at'] <= at < g['expires_at']:
        fail('AUTHORIZATION_DENIED', 'Release grant withdrawn, expired or clock invalid')
    f = qualified(s, r['request']['target_sha256'])
    if fingerprint(f['certificate']) != r['request']['generation_certificate_sha256']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Release targets different generation qualification')
    source_matches(s, r['request'])


def quiescent(s):
    if any(not v['closed'] for v in s['tickets'].values()):
        fail('RECOVERY_REQUIRED', 'Finish/recover the open managed stage before release')


def ticket_for(s, store_id, ticket_id, profile, caller):
    if s['current']['epoch'] == 0: fail('CAPABILITY_UNAVAILABLE', 'No generation has been adopted')
    f = qualified(s, s['current']['generation_sha256'])
    p = next((p for p in f['manifest']['profiles'] if p['id'] == profile), None)
    if p is None: fail('INCOMPATIBLE_CONFIGURATION', 'Profile is not in the exact released family')
    return {'schema_version': 1, 'store_id': store_id, 'ticket_id': identifier(ticket_id), 'caller_id': caller,
            'configuration': deepcopy(s['current']), 'profile': profile, 'profile_ecid': p['ecid'],
            'state_reuse': 'EXACT_TICKET_ONLY'}


def receipt_for(s, r):
    req = r['request']; previous = deepcopy(s['current'])
    return {'schema_version': 1, 'release_id': req['release_id'], 'request_sha256': fingerprint(req),
            'grant_sha256': fingerprint(r['grant']), 'previous': previous,
            'current': {'epoch': previous['epoch'] + 1, 'generation_sha256': req['target_sha256']},
            'archived_predecessor': previous['generation_sha256'],
            'staged_artifacts_sha256': fingerprint(r['artifacts']), 'status': 'PUBLISHED',
            'scope': 'LOCAL_CATALOG_ONLY', 'runtime_execution_permit': False,
            'production_deployment_authorized': False}


