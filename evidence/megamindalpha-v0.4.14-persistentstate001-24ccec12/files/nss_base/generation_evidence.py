"""Generation-wide closure over exact, independently recorded child claims.

Uses public qualification/source APIs only. This checker does not grant release
permission, invent subset compatibility, train weights, or broaden neural claims.
"""
from copy import deepcopy
from .generation_contracts import artifact_bundle, generation
from .neural_contracts import fingerprint
from .qualification_sources import require_source
from .qualification_store import Qualifications
from .runtime import fail


def check_family(value, *, qualifications, source):
    g = generation(value); source = require_source(source)
    if type(qualifications) is not Qualifications:
        fail('VALIDATION_FAILED', 'Only the installed local qualification owner is supported')
    for p in g['profiles']:
        qualifications.check_use(p['evidence']['id'], certificate_sha256=p['evidence']['sha256'],
            expected_claim={'kind': 'PROFILE', 'profile': p['id']}, expected_binding=g['binding'], source=source)
    for t in g['transitions']:
        qualifications.check_use(t['evidence']['id'], certificate_sha256=t['evidence']['sha256'],
            expected_claim={'kind': 'TRANSITION', 'source': t['source'],
                            'destination': t['destination'], 'mode': t['mode']},
            expected_binding=g['binding'], source=source)
    b = g['binding']
    view = source.view(b['run_id'], b['trial_seed'], b['precision'])
    if view[4] != b:
        fail('INCOMPATIBLE_CONFIGURATION', 'Family targets a different source binding')
    names = ['core'] + [m['id'] for m in g['members']]
    return artifact_bundle({k: deepcopy(view[1]['artifacts'][k]) for k in names}, g)


def from_evidence(generation_id, producer_id, profile_ids, transition_ids, *, qualifications):
    """Assemble, not approve, a manifest from existing immutable certificates."""
    if type(qualifications) is not Qualifications:
        fail('VALIDATION_FAILED', 'Built-in qualification store required')
    records = [qualifications.inspect(k) for k in [*profile_ids, *transition_ids]]
    if not records or any(r['status'] != 'QUALIFIED' or r['certificate'] is None for r in records):
        fail('INSUFFICIENT_EVIDENCE', 'An exact accepted certificate is required for each selected claim')
    b = records[0]['request']['binding']
    if any(r['request']['binding'] != b for r in records):
        fail('INCOMPATIBLE_CONFIGURATION', 'Cannot mix independently bound candidate runs')
    from .generation_contracts import PROFILE_MEMBERS
    profiles = []; edges = []
    for i, r in enumerate(records):
        c = r['request']['claim']; ref = {'id': r['request']['request_id'], 'sha256': fingerprint(r['certificate'])}
        if i < len(profile_ids):
            if c['kind'] != 'PROFILE': fail('INCOMPATIBLE_CONFIGURATION', 'Expected a profile certificate')
            profiles.append({'id': c['profile'], 'members': PROFILE_MEMBERS[c['profile']],
                             'ecid': b['profile_ecids'][c['profile']], 'evidence': ref})
        else:
            if c['kind'] != 'TRANSITION': fail('INCOMPATIBLE_CONFIGURATION', 'Expected a transition certificate')
            edges.append({'source': c['source'], 'destination': c['destination'], 'mode': c['mode'],
                          'state_policy': 'DISCARD_AND_REPLAY', 'evidence': ref})
    names = sorted({a for p in profiles for a in p['members']})
    return generation({'schema_version': 1, 'generation_id': generation_id, 'producer_id': producer_id,
        'binding': deepcopy(b), 'members': [{'id': a, 'sha256': b['checkpoint_hashes'][a], 'requires': []} for a in names],
        'profiles': sorted(profiles, key=lambda p: p['id']),
        'transitions': sorted(edges, key=lambda t: (t['source'], t['destination'])),
        'purpose': 'BOUNDED_CANDIDATE_OVERLAY_GENERATION' if 'source_format' in b else 'BOUNDED_NEURAL_PROBE_GENERATION'})
