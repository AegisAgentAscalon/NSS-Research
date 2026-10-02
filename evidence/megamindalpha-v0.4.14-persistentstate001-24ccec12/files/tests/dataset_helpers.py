"""Synthetic, explicitly attested test data. No private or learned material."""
from hashlib import sha256
from pathlib import Path
import copy
import json

from nss_base.experience_store import ExperienceArchive

AT = '2026-09-10T13:00:00Z'
HUMAN = {'id': 'fixture-operator', 'kind': 'HUMAN', 'version': 'scripted-v1'}
MODEL = {'id': 'fixture-model', 'kind': 'MODEL', 'version': 'not-neural-v1'}


def ok(result):
    if result['status'] != 'SUCCESS':
        raise AssertionError(result)
    return result['data']


def capture_request(id='exp1', *, text=None, source=None, family=None):
    content = source or ('Synthetic source ' + id + ': speed is 10 m/s.')
    return {'schema_version': 1, 'operation_id': 'capture:' + id,
        'experience_id': id, 'actor': MODEL.copy(), 'at': AT,
        'observation': {'kind': 'EXTERNAL_RECORD', 'execution': None,
            'summary': 'Synthetic example for dataset tests.', 'outcome': 'UNKNOWN', 'check_refs': []},
        'family_id': family or 'family:' + id, 'sensitivity': 'ORDINARY',
        'evidence': [{'id': 'source1', 'kind': 'REFERENCE', 'author': HUMAN.copy(),
            'recorded_at': AT, 'media_type': 'text/plain',
            'sha256': sha256(content.encode()).hexdigest(), 'content': content,
            'generator': None, 'parent_source_ids': [], 'rights_note': 'Self-authored software fixture.'}],
        'statement': {'text': text or ('Reviewed fixture ' + id + ': speed is 10 m/s.'),
            'uncertainty': 'LOW', 'support_ids': ['source1']}}


def change(archive, id, action, payload, *, operation_id=None, actor=None):
    ref = ok(archive.inspect(id))['reference']
    return archive.change({'schema_version': 1, 'operation_id': operation_id or f'change:{id}:{ref["revision"]}:{action}',
        'experience_id': id, 'expected_revision_hash': ref['sha256'], 'actor': copy.deepcopy(actor or HUMAN),
        'at': AT, 'reason': 'Scripted human-attestation fixture, not real human review.',
        'action': action, 'payload': payload})


def approved(archive, id='exp1', **kw):
    ok(archive.capture(capture_request(id, **kw)))
    ok(change(archive, id, 'REVIEW', {'decision': 'APPROVED'}))
    return ok(change(archive, id, 'PERMISSION', {'purpose': 'training', 'decision': 'ALLOWED',
                  'permission_ref': 'fixture:training-rights'}))['reference']


def revoke(archive, id='exp1', *, purpose='training', operation_id=None):
    view = ok(archive.inspect(id))
    return archive.revoke_source({'schema_version': 1, 'operation_id': operation_id or 'revoke:' + id + ':' + purpose,
        'actor': HUMAN.copy(), 'at': AT, 'reason': 'Synthetic rights withdrawal.',
        'permission_ref': 'fixture:withdrawal', 'source_sha256': view['record']['sources'][0]['sha256'], 'purpose': purpose})


def tokenizer(root):
    p = Path(root) / 'tokenizer.json'
    p.write_text('{"format":"identity-only-fixture","version":1}\n', encoding='utf-8')
    return p, {'id': 'fixture-tokenizer', 'version': '1', 'sha256': sha256(p.read_bytes()).hexdigest()}


def build_request(refs, tok, *, sid='snapshot1', op=None, transform='curated_text_v1'):
    return {'schema_version': 1, 'snapshot_id': sid, 'operation_id': op or 'build:' + sid,
        'actor': HUMAN.copy(), 'at': AT, 'reason': 'Explicit synthetic training selection.',
        'purpose': 'training', 'transform': transform, 'tokenizer': copy.deepcopy(tok),
        'members': [{**r, 'split': 'train' if i == 0 else 'validation'} for i, r in enumerate(refs)]}
