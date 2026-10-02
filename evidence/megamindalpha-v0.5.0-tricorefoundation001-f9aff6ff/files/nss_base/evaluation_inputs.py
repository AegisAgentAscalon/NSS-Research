"""Capture bounded, byte-exact local evaluation inputs through public boundaries.

Code, actor and suite permissions are local attestations, not a signature system.
The optional snapshot is development training-lineage data, never a hidden exam.
"""
from hashlib import sha256
import os
from pathlib import Path
import platform

from .dataset_store import DatasetSnapshots
from .evaluation_contracts import (IMPLEMENTATION, MAX_FILE_BYTES, MAX_TOTAL_BYTES,
    catalog, child_path, normalize_plan, normalize_suite, relative_path, validate_material)
from .experience_contracts import bounded_copy
from .runtime import digest, fail
from .serialization import decode, validate

ROOT=Path(__file__).resolve().parents[1]


def local_path(value):
    if not isinstance(value,(str,os.PathLike)):
        fail('VALIDATION_FAILED','Expected a local path')
    try:
        path=Path(value).resolve()
        if '\x00' in str(path):fail('VALIDATION_FAILED','Invalid local path')
        return path
    except (ValueError,TypeError,OSError):fail('VALIDATION_FAILED','Invalid local path')


def _measure_identity():
    paths=sorted([*ROOT.glob('nss_base/*.py'),*ROOT.glob('schemas/*.json'),ROOT/'VERSION'])
    code={'version':IMPLEMENTATION,'files':[{'path':p.relative_to(ROOT).as_posix(),
        'sha256':sha256(p.read_bytes()).hexdigest()} for p in paths],
        'environment':{'python':platform.python_version(),'implementation':platform.python_implementation(),
                       'platform':platform.platform(),'machine':platform.machine()}}
    code['sha256']=digest(code);return code


# Freeze this process's installed-source identity. Changing code in a running
# interpreter is not supported; restart before preparing any new plan.
_PROCESS_IDENTITY = _measure_identity()


def implementation_identity():
    current = _measure_identity()
    if current != _PROCESS_IDENTITY:
        fail('INCOMPATIBLE_CONFIGURATION', 'Installed code/environment changed; restart the evaluation process')
    return current


def _unwrap(result):
    if result['status']!='SUCCESS':fail(result['status'],result['detail'])
    return result['data']


def capture_inputs(plan, root, *, snapshots=None, archive=None, tokenizer_path=None):
    plan=normalize_plan(plan);root=local_path(root)
    if not root.is_dir():fail('INSUFFICIENT_EVIDENCE','Evaluation input directory is unavailable')
    code=implementation_identity()
    if code['sha256']!=plan['implementation_sha256']:
        fail('INCOMPATIBLE_CONFIGURATION','Running code/environment differs from the frozen plan')
    captured={};total=0
    def read(ref,role,schema):
        nonlocal total
        name=relative_path(ref['path']);path=(root/name).resolve()
        if not path.is_relative_to(root):fail('VALIDATION_FAILED','Artifact escapes the selected root')
        if not path.is_file():fail('INSUFFICIENT_EVIDENCE','Pinned evaluation artifact is missing')
        with path.open('rb') as stream:raw=stream.read(MAX_FILE_BYTES+1)
        if len(raw)>MAX_FILE_BYTES:fail('BUDGET_EXHAUSTED','Evaluation artifact exceeds byte budget')
        if sha256(raw).hexdigest()!=ref['sha256']:
            fail('INCOMPATIBLE_CONFIGURATION','Evaluation artifact bytes changed')
        try:text=raw.decode('utf-8')
        except UnicodeError:fail('VALIDATION_FAILED','Evaluation data must be UTF-8 JSON')
        record={'path':name,'role':role,'sha256':ref['sha256'],'text':text}
        if name in captured and captured[name]!=record:
            fail('CONSTRAINT_CONFLICT','One artifact path cannot have conflicting roles or bytes')
        if name not in captured:total+=len(raw)
        if total>MAX_TOTAL_BYTES:fail('BUDGET_EXHAUSTED','Combined evaluation inputs exceed budget')
        captured[name]=record
        parsed=bounded_copy(decode(text));validate(parsed,schema);return parsed
    manifest=plan['candidate']['manifest'];d=read(manifest,'manifest','manifest.schema.json')
    catalog(d)  # Bound candidate size before following any artifact list.
    for ref in [d['core']]+[o['artifact'] for o in d['overlays']]:
        read({'path':child_path(manifest['path'],ref['path']),'sha256':ref['sha256']},'operation','operation.schema.json')
    suite=normalize_suite(read(plan['suite'],'suite','evaluation_suite.schema.json'))
    for test in suite['tests']:
        ref=test['fixture']
        read({'path':child_path(plan['suite']['path'],ref['path']),'sha256':ref['sha256']},'fixture','inputs.schema.json')
    observation=None;selected=plan['development_snapshot']
    if selected is not None:
        if not isinstance(snapshots,DatasetSnapshots):
            fail('CAPABILITY_UNAVAILABLE','A public DatasetSnapshots adapter is required')
        data=_unwrap(snapshots.read_for_use(selected['snapshot_id'],expected_manifest_hash=selected['sha256'],
            purpose='training',split=selected['split'],archive=archive,tokenizer_path=tokenizer_path))
        if data['snapshot']['sha256']!=selected['sha256'] or data['split']!=selected['split']:
            fail('VALIDATION_FAILED','Snapshot consumer returned a mismatched observation')
        observation={**selected,'examples_sha256':digest(data['examples']),'member_count':len(data['examples'])}
        # Do not retain example text, checked_at, or a cached permission grant.
    elif any(x is not None for x in (snapshots,archive,tokenizer_path)):
        fail('VALIDATION_FAILED','Unbound dataset adapters are not permitted')
    material={'schema_version':1,'format':'MegaMindAlpha.EvaluationMaterial001',
        'files':[captured[name] for name in sorted(captured)],'implementation':code,
        'development_observation':observation}
    return validate_material(plan,material)[0]
