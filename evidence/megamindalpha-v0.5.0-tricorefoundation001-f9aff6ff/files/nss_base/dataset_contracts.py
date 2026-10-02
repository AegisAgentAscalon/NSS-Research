"""DatasetSnapshot001 pure contracts; declared lineage is not semantic truth.

One exact reviewed statement -> one UTF-8 text example. No tokenization, arbitrary
transform execution, learned curation or training. Split checks are local to this
snapshot and based on declared families, shared source bytes and exact text.
"""
from hashlib import sha256

from .experience_contracts import bounded_copy, human, source_metadata, timestamp
from .runtime import digest, fail
from .serialization import validate

FORMAT = 'MegaMindAlpha.DatasetSnapshot001'
PROJECTION_VERSION = 'dataset-projection-v1'
MAX_MEMBERS = 32
MAX_MANIFEST_BYTES = 4 * 1024 * 1024
MAX_TOKENIZER_BYTES = 32 * 1024 * 1024
SPLITS = ('train', 'validation')


def normalize_request(request):
    request = bounded_copy(request)
    validate(request, 'dataset_build.schema.json')
    timestamp(request['at']); human(request['actor'])
    ids = [m['experience_id'] for m in request['members']]
    if len(ids) != len(set(ids)):
        fail('VALIDATION_FAILED', 'Select each experience exactly once')
    if not any(m['split'] == 'train' for m in request['members']):
        fail('VALIDATION_FAILED', 'A training snapshot needs at least one train member')
    request['members'].sort(key=lambda m: m['experience_id'])
    return request


def references(request):
    return [{k: m[k] for k in ('experience_id', 'revision', 'sha256')} for m in request['members']]


def project(text, transform):
    if transform == 'normalize_newlines_v1':
        text = text.replace('\r\n', '\n').replace('\r', '\n')
    elif transform != 'curated_text_v1':
        fail('VALIDATION_FAILED', 'Unknown non-executable projection')
    if not text.strip():
        fail('VALIDATION_FAILED', 'An empty/whitespace example is not useful training input')
    return text


def _validate_view(view, request):
    validate(view, 'experience_use_view.schema.json')
    timestamp(view['updated_at']); timestamp(view['statement']['recorded_at'])
    source_metadata(view['sources'])
    if (view['purpose'] != 'training' or view['review']['status'] != 'APPROVED'
            or view['permission']['status'] != 'ALLOWED'):
        fail('VALIDATION_FAILED', 'Manifest did not capture approved training eligibility')
    for record, actor_key in ((view['review'], 'reviewer'), (view['permission'], 'actor')):
        if record[actor_key] is None or record['at'] is None:
            fail('VALIDATION_FAILED', 'Missing review/permission observation')
        human(record[actor_key]); timestamp(record['at'])
        if record['at'] > view['updated_at']:
            fail('VALIDATION_FAILED', 'Permission/review observation is newer than the revision')
    if not view['permission']['permission_ref']:
        fail('VALIDATION_FAILED', 'Missing attested permission reference')
    if view['updated_at'] > request['at']:
        fail('VALIDATION_FAILED', 'Snapshot request predates selected review/revision')
    support = view['statement']['support_ids']
    if len(support) != len(set(support)) or not set(support) <= {s['id'] for s in view['sources']}:
        fail('VALIDATION_FAILED', 'Broken supporting-source references')


def validate_manifest(manifest):
    manifest = bounded_copy(manifest)
    validate(manifest, 'dataset_manifest.schema.json')
    request = normalize_request(manifest['request'])
    if request != manifest['request'] or digest(request) != manifest['request_sha256']:
        fail('VALIDATION_FAILED', 'Manifest request identity/order is inconsistent')
    if len(manifest['members']) != len(request['members']):
        fail('VALIDATION_FAILED', 'Manifest membership differs from explicit selection')
    families, source_splits, texts = {}, {}, set()
    for member, selection, reference in zip(manifest['members'], request['members'], references(request)):
        view = member['view']; _validate_view(view, request)
        if member['split'] != selection['split'] or view['reference'] != reference:
            fail('VALIDATION_FAILED', 'Member selection/reference differs from the request')
        text = project(view['statement']['text'], request['transform'])
        h = sha256(text.encode('utf-8')).hexdigest()
        if text != member['text'] or h != member['text_sha256']:
            fail('VALIDATION_FAILED', 'Projected example does not match its source statement')
        if h in texts:
            fail('CONSTRAINT_CONFLICT', 'Duplicate projected example; explicitly curate membership')
        texts.add(h)
        split = member['split']; family = view['family_id']
        if family in families and families[family] != split:
            fail('CONSTRAINT_CONFLICT', 'Declared source family crosses split boundary')
        families[family] = split
        for source in view['sources']:
            h = source['sha256']
            if h in source_splits and source_splits[h] != split:
                fail('CONSTRAINT_CONFLICT', 'Shared exact source bytes cross split boundary')
            source_splits[h] = split
    return manifest


def make_manifest(request, batch):
    request = normalize_request(request)
    if type(batch) is not dict or set(batch) != {'archive_binding', 'views'}:
        fail('VALIDATION_FAILED', 'Malformed archive batch observation')
    if type(batch['views']) is not list or len(batch['views']) != len(request['members']):
        fail('VALIDATION_FAILED', 'Archive returned an incomplete batch')
    members = []
    for selection, view in zip(request['members'], batch['views']):
        validate(view, 'experience_use_view.schema.json')
        text = project(view['statement']['text'], request['transform'])
        members.append({'split': selection['split'], 'view': view, 'text': text,
                        'text_sha256': sha256(text.encode('utf-8')).hexdigest()})
    return validate_manifest({'format': FORMAT, 'schema_version': 1,
        'projection_version': PROJECTION_VERSION, 'archive_binding': batch['archive_binding']['sha256'],
        'request': request, 'request_sha256': digest(request), 'members': members})


def receipt(manifest):
    return {'snapshot_id': manifest['request']['snapshot_id'], 'sha256': digest(manifest),
            'member_count': len(manifest['members'])}
