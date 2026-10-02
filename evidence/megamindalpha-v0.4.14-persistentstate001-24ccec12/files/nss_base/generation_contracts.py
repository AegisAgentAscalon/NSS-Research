"""OverlayGenerationManager001: exact local release contracts, not serving permits.

Only installed original-probe A/B and new-candidate A2/B evidence families,
profiles and their qualified directed edges are supported. A release cannot claim new neural performance, authentication or Runtime
execution authority. Profile/transition evidence is necessary but not release consent.
"""
from copy import deepcopy
from .local_journal import epoch
from .neural_contracts import encoded, fields, fingerprint
from .qualification_contracts import binding, digest_value, identifier, text, CANDIDATE_FORMAT
from .runtime import fail

FORMAT = 'MegaMindAlpha.OverlayGenerationManager001'
OPERATION = 'PUBLISH_LOCAL_OVERLAY_GENERATION'
ROLES = ('PRODUCER', 'REVIEWER', 'ISSUER', 'OPERATOR')
PROFILE_MEMBERS = {'CORE': [], 'A': ['A'], 'B': ['B'], 'AB': ['A', 'B'], 'A2': ['A2'], 'A2B': ['A2', 'B']}
EDGES = (('AB', 'A'), ('A', 'CORE'), ('A2B', 'A2'), ('A2', 'CORE'))
POLICY = {'version': 1, 'operation': OPERATION, 'scope': 'TRUSTED_LOCAL_GENERATION_CATALOG',
          'max_ttl_seconds': 900, 'max_uses': 1, 'core_only_required': True,
          'release_boundary': 'NO_OPEN_MANAGED_STAGES', 'state_reuse': 'NONE_ACROSS_RELEASES',
          'authentication': False, 'runtime_execution_permit': False,
          'production_deployment_authorized': False}
POLICY_HASH = fingerprint(POLICY)


def _version(x):
    if type(x) is not int or x != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported generation schema')


def _items(value, low, high):
    if type(value) is not list or not low <= len(value) <= high:
        fail('VALIDATION_FAILED', 'List outside declared bounds')
    return value


def _unique(keys):
    if len(keys) != len(set(keys)):
        fail('VALIDATION_FAILED', 'Duplicate identity')


def exact(actual, expected):
    # Canonical JSON avoids bool == int and silently ignored extra fields.
    if encoded(actual) != encoded(expected):
        fail('VALIDATION_FAILED', 'Exact stored binding differs')


def configuration(value):
    fields(value, ('epoch', 'generation_sha256'))
    if type(value['epoch']) is not int or not 0 <= value['epoch'] <= 1000000:
        fail('VALIDATION_FAILED', 'Invalid generation epoch')
    if value['epoch'] == 0:
        if value['generation_sha256'] is not None:
            fail('VALIDATION_FAILED', 'Uninitialized pointer must be empty')
    else:
        digest_value(value['generation_sha256'])
    return deepcopy(value)


def store_manifest(x):
    fields(x, ('schema_version', 'format', 'store_id', 'policy_sha256', 'operators'))
    _version(x['schema_version']); identifier(x['store_id']); encoded(x)
    if x['format'] != FORMAT or x['policy_sha256'] != POLICY_HASH or fingerprint(POLICY) != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Wrong generation store or changed policy')
    ops = _items(x['operators'], 3, 32)
    for o in ops:
        fields(o, ('id', 'roles')); identifier(o['id'])
        rs = _items(o['roles'], 1, len(ROLES))
        if any(type(r) is not str or r not in ROLES for r in rs):
            fail('VALIDATION_FAILED', 'Unknown declared generation role')
        _unique(rs)
    _unique([o['id'] for o in ops])
    if any(not any(r in o['roles'] for o in ops) for r in ROLES):
        fail('VALIDATION_FAILED', 'A required generation role is missing')
    return deepcopy(x)


def role(m, actor, expected):
    identifier(actor)
    if not any(o['id'] == actor and expected in o['roles'] for o in m['operators']):
        fail('AUTHORIZATION_DENIED', 'Declared role absent')


def evidence_ref(x):
    fields(x, ('id', 'sha256')); identifier(x['id']); digest_value(x['sha256'])


def generation(x):
    fields(x, ('schema_version', 'generation_id', 'producer_id', 'binding', 'members',
               'profiles', 'transitions', 'purpose'))
    _version(x['schema_version']); identifier(x['generation_id']); identifier(x['producer_id'])
    b = binding(x['binding']); encoded(x)
    candidate = b.get('source_format') == CANDIDATE_FORMAT
    allowed = ('A2', 'B') if candidate else ('A', 'B')
    purpose = 'BOUNDED_CANDIDATE_OVERLAY_GENERATION' if candidate else 'BOUNDED_NEURAL_PROBE_GENERATION'
    if x['purpose'] != purpose:
        fail('INCOMPATIBLE_CONFIGURATION', 'Not a generic model deployment manifest')
    members = {}
    for a in _items(x['members'], 0, 2):
        fields(a, ('id', 'sha256', 'requires'))
        if type(a['id']) is not str or a['id'] not in allowed or a['id'] in members:
            fail('VALIDATION_FAILED', "Only this evidence family's exact slot members are supported")
        digest_value(a['sha256'])
        if a['sha256'] != b['checkpoint_hashes'][a['id']]:
            fail('INCOMPATIBLE_CONFIGURATION', 'Member differs from bound checkpoint')
        deps = _items(a['requires'], 0, 1)
        if any(type(d) is not str or d not in allowed or d == a['id'] for d in deps):
            fail('VALIDATION_FAILED', 'Invalid slot dependency')
        members[a['id']] = a
    for a in members.values():
        for dep in a['requires']:
            if dep not in members or a['id'] in members[dep]['requires']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Missing or cyclic member dependency')
    profiles = {}
    for p in _items(x['profiles'], 1, 4):
        fields(p, ('id', 'members', 'ecid', 'evidence'))
        if type(p['id']) is not str or p['id'] not in b['profile_ecids'] or p['id'] in profiles:
            fail('VALIDATION_FAILED', 'Unknown/duplicate activation profile')
        exact(p['members'], PROFILE_MEMBERS[p['id']]); evidence_ref(p['evidence'])
        if p['ecid'] != b['profile_ecids'][p['id']]:
            fail('INCOMPATIBLE_CONFIGURATION', 'Profile ECID differs')
        for a in p['members']:
            if a not in members or any(d not in p['members'] for d in members[a]['requires']):
                fail('INCOMPATIBLE_CONFIGURATION', 'Activation violates member/dependency closure')
        profiles[p['id']] = p
    if 'CORE' not in profiles:
        fail('INCOMPATIBLE_CONFIGURATION', 'Every generation requires a qualified Core-only profile')
    if set(members) != {a for p in profiles.values() for a in p['members']}:
        fail('INCOMPATIBLE_CONFIGURATION', 'An unused member is not a qualified family extension')
    edges = []
    for t in _items(x['transitions'], 0, 2):
        fields(t, ('source', 'destination', 'mode', 'state_policy', 'evidence'))
        edge = (t['source'], t['destination'])
        if any(type(a) is not str for a in edge) or edge not in EDGES:
            fail('INCOMPATIBLE_CONFIGURATION', 'No implemented evidence checker for that directed edge')
        if any(a not in profiles for a in edge) or t['mode'] != 'replay' or t['state_policy'] != 'DISCARD_AND_REPLAY':
            fail('INCOMPATIBLE_CONFIGURATION', 'Unknown endpoints or state-reuse policy')
        evidence_ref(t['evidence']); edges.append(edge)
    _unique(edges)
    reached = {'CORE'}
    for _ in range(len(profiles)):
        reached.update(a for a, b in edges if b in reached)
    if set(profiles) != reached:
        fail('INCOMPATIBLE_CONFIGURATION', 'Every selected profile needs a declared qualified return to Core-only')
    _unique([p['evidence']['id'] for p in x['profiles']] + [t['evidence']['id'] for t in x['transitions']])
    return deepcopy(x)


def artifact_hashes(g):
    g = generation(g)
    return {'core': g['binding']['checkpoint_hashes']['core'], **{m['id']: m['sha256'] for m in g['members']}}


def artifact_bundle(x, g):
    fields(x, tuple(artifact_hashes(g)))
    exact({k: fingerprint(v) for k, v in x.items()}, artifact_hashes(g))
    return deepcopy(x)


def release_request(x):
    fields(x, ('schema_version', 'release_id', 'operation', 'caller_id', 'target_sha256',
               'generation_certificate_sha256', 'expected_current', 'reason', 'mode'))
    _version(x['schema_version']); identifier(x['release_id']); identifier(x['caller_id'])
    digest_value(x['target_sha256']); digest_value(x['generation_certificate_sha256'])
    configuration(x['expected_current']); text(x['reason'])
    if x['operation'] != OPERATION or type(x['mode']) is not str or x['mode'] not in ('BOOTSTRAP', 'UPDATE', 'ROLLBACK'):
        fail('INCOMPATIBLE_CONFIGURATION', 'Replay grants are not release grants')
    if (x['mode'] == 'BOOTSTRAP') != (x['expected_current']['epoch'] == 0):
        fail('INCOMPATIBLE_CONFIGURATION', 'Bootstrap/update source mismatch')
    if x['target_sha256'] == x['expected_current']['generation_sha256']:
        fail('CONSTRAINT_CONFLICT', 'Current generation cannot be republished as an update')
    encoded(x); return deepcopy(x)


def generation_certificate(g, reviewer, at, m):
    g = generation(g); role(m, reviewer, 'REVIEWER'); epoch(at)
    if reviewer in (g['producer_id'], g['binding'].get('candidate_lineage', {}).get('producer_id')):
        fail('AUTHORIZATION_DENIED', 'Producer cannot qualify its own generation')
    return {'schema_version': 1, 'generation_sha256': fingerprint(g), 'reviewer_id': reviewer,
            'issued_at': at, 'policy_sha256': POLICY_HASH, 'kind': 'GENERATION_CATALOG_CLOSURE',
            'claim': 'Exact members, profiles, returns and evidence are bound; no new neural claim.',
            'release_authorized': False, 'runtime_execution_permit': False}


def release_grant(req, issuer, issued, expires, m):
    req = release_request(req); role(m, issuer, 'ISSUER'); role(m, req['caller_id'], 'OPERATOR')
    epoch(issued); epoch(expires)
    if issuer == req['caller_id']:
        fail('AUTHORIZATION_DENIED', 'Executor cannot issue its own release approval')
    if not 1 <= expires - issued <= POLICY['max_ttl_seconds']:
        fail('VALIDATION_FAILED', 'Release grant lifetime exceeds local policy')
    return {'schema_version': 1, 'store_id': m['store_id'], 'request_sha256': fingerprint(req),
            'issuer_id': issuer, 'issued_at': issued, 'expires_at': expires, 'max_uses': 1,
            'policy_sha256': POLICY_HASH, 'authority': POLICY['scope'],
            'catalog_publication_authorized': True, 'runtime_execution_permit': False,
            'production_deployment_authorized': False}
