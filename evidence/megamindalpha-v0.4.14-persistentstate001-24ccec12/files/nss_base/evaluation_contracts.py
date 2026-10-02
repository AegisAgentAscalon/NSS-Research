"""Pure EvaluationRun001 contracts and bounded, non-neural integer checking.

Verdicts describe synthetic development cases, not authority, neural quality or
independent verification. JSON artifacts never name executable callbacks.
"""
from hashlib import sha256
from pathlib import PurePosixPath

from .experience_contracts import bounded_copy, human, timestamp
from .runtime import Catalog, Overlay, Profile, Transition, digest, fail
from .serialization import decode, validate

FORMAT = 'MegaMindAlpha.EvaluationRun001'
CHECKER = 'exact_integer_sequence_v1'
IMPLEMENTATION = 'evaluation-integer-v1'
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 2 * 1024 * 1024
MAX_VALUES = 64
MAX_OPERATIONS = 16


def relative_path(value):
    if (type(value) is not str or not value or len(value)>512 or '\\' in value
            or ':' in value or '\x00' in value or value.startswith('/')
            or any(p in ('','.', '..') for p in value.split('/'))):
        fail('VALIDATION_FAILED', 'Expected a canonical relative POSIX artifact path')
    return value


def child_path(parent_file, child):
    relative_path(parent_file); relative_path(child)
    return relative_path(str(PurePosixPath(parent_file).parent / child))


def normalize_plan(plan):
    plan = bounded_copy(plan); validate(plan, 'evaluation_plan.schema.json')
    human(plan['actor']); timestamp(plan['at'])
    relative_path(plan['candidate']['manifest']['path']); relative_path(plan['suite']['path'])
    return plan


def normalize_suite(suite):
    suite = bounded_copy(suite); validate(suite, 'evaluation_suite.schema.json')
    human(suite['evaluation_permission']['actor'])
    ids=[t['id'] for t in suite['tests']]
    if len(ids)!=len(set(ids)) or not any(t['mandatory'] for t in suite['tests']):
        fail('VALIDATION_FAILED', 'Test IDs must be unique and one test must be mandatory')
    identities=[(t['fixture']['sha256'],t['checker']) for t in suite['tests']]
    if len(identities)!=len(set(identities)):
        fail('CONSTRAINT_CONFLICT','Duplicate exact input/checker cases require explicit suite redesign, not score reweighting')
    for test in suite['tests']:relative_path(test['fixture']['path'])
    return suite


def catalog(document):
    """Use the existing catalog rules; add Bundle's ordered dependency contract."""
    validate(document, 'manifest.schema.json'); d=document
    if len(d['profiles'])>64 or len(d['transitions'])>128:
        fail('BUDGET_EXHAUSTED', 'Candidate profile/transition metadata exceeds the local bound')
    if len(d['overlays'])>MAX_OPERATIONS-1:
        fail('BUDGET_EXHAUSTED', 'Candidate exceeds this integer experiment operation budget')
    c=Catalog(d['core']['sha256'],d['generation'],d['tokenizer'],d['context_abi'],d['overlay_abi'],
        d['runtime_version'],tuple(Overlay(o['id'],o['artifact']['sha256'],tuple(o['requires']),tuple(o['excludes'])) for o in d['overlays']),
        tuple(Profile(p['id'],tuple(p['overlays']),p['evidence_ref']) for p in d['profiles']),
        tuple(Transition(t['source'],t['destination'],t['state_reuse_policy'],t['evidence_ref']) for t in d['transitions']))
    by_id={o['id']:o for o in d['overlays']}
    for p in c.profiles:
        before=set()
        for name in p.overlays:
            if not set(by_id[name]['requires'])<=before:
                fail('INCOMPATIBLE_CONFIGURATION','Ordered dependencies are incomplete')
            before.add(name)
    for t in d['transitions']:
        replay=t['state_reuse_policy']=='replay'
        if (t['failure_destination']!=t['source'] or t['replay_required']!=replay
                or t['invalidate']!=(['cache','draft'] if replay else [])):
            fail('VALIDATION_FAILED','Transition fixture is inconsistent')
    return c


def validate_material(plan, material):
    plan=normalize_plan(plan); material=bounded_copy(material)
    validate(material,'evaluation_material.schema.json')
    files=material['files']; paths=[f['path'] for f in files]
    if paths!=sorted(set(paths)):
        fail('VALIDATION_FAILED','Material paths must be uniquely sorted')
    total=0; by_path={}
    schemas={'manifest':'manifest.schema.json','operation':'operation.schema.json',
             'suite':'evaluation_suite.schema.json','fixture':'inputs.schema.json'}
    for f in files:
        relative_path(f['path']); raw=f['text'].encode('utf-8');total+=len(raw)
        if len(raw)>MAX_FILE_BYTES or total>MAX_TOTAL_BYTES:
            fail('BUDGET_EXHAUSTED','Material exceeds byte budget')
        if sha256(raw).hexdigest()!=f['sha256']:
            fail('VALIDATION_FAILED','Captured file bytes do not match digest')
        parsed=bounded_copy(decode(f['text']));validate(parsed,schemas[f['role']]);by_path[f['path']]=(f,parsed)
        if f['role']=='fixture' and len(parsed['values'])>MAX_VALUES:
            fail('BUDGET_EXHAUSTED','Too many integer inputs')
    used=set()
    def get(ref,role):
        if ref['path'] not in by_path:fail('VALIDATION_FAILED','Material is missing a pinned artifact')
        f,obj=by_path[ref['path']];used.add(f['path'])
        if f['sha256']!=ref['sha256'] or f['role']!=role:
            fail('VALIDATION_FAILED','Artifact role or digest differs from its reference')
        return obj
    manifest_ref=plan['candidate']['manifest']; d=get(manifest_ref,'manifest');c=catalog(d)
    p=c.profile(plan['candidate']['profile'])
    ecid=digest({'ecid_schema':'001A-1','manifest':d,'active_profile':p.id})
    if ecid!=plan['candidate']['expected_ecid']:
        fail('INCOMPATIBLE_CONFIGURATION','Candidate profile ECID differs')
    def operation(ref):return get({'path':child_path(manifest_ref['path'],ref['path']),'sha256':ref['sha256']},'operation')
    core=operation(d['core']);overlay_ops={o['id']:operation(o['artifact']) for o in d['overlays']}
    operations=[core]+[overlay_ops[name] for name in p.overlays]
    suite=normalize_suite(get(plan['suite'],'suite')); cases=[]
    for test in suite['tests']:
        ref={'path':child_path(plan['suite']['path'],test['fixture']['path']),'sha256':test['fixture']['sha256']}
        inputs=get(ref,'fixture')
        cases.append((test,inputs))
    if used!=set(by_path):fail('VALIDATION_FAILED','Unreferenced material is not allowed')
    code=material['implementation']; names=[f['path'] for f in code['files']]
    if names!=sorted(set(names)):fail('VALIDATION_FAILED','Code paths must be uniquely sorted')
    for name in names:relative_path(name)
    actual=digest({k:v for k,v in code.items() if k!='sha256'})
    if actual!=code['sha256'] or actual!=plan['implementation_sha256']:
        fail('INCOMPATIBLE_CONFIGURATION','Implementation identity differs')
    snapshot=plan['development_snapshot']; observation=material['development_observation']
    if snapshot is None:
        if observation is not None:fail('VALIDATION_FAILED','Unexpected development observation')
    elif observation is None or any(observation[k]!=snapshot[k] for k in ('snapshot_id','sha256','split')):
        fail('VALIDATION_FAILED','Development snapshot observation differs')
    return material, suite, operations, cases


def evaluate_repeat(plan, material, repeat, remaining):
    """Only pure bounded integer operations. No calls, weights, tools or file reads."""
    material,suite,operations,cases=validate_material(plan,material)
    if type(repeat) is not int or not 1<=repeat<=plan['repeats'] or type(remaining) is not int or remaining<0:
        fail('VALIDATION_FAILED','Invalid repeat/budget')
    rows=[]
    for test,inputs in cases[:remaining]:
        values=list(inputs['values'])
        for op in operations:values=[x*op['multiply']+op['add'] for x in values]
        rows.append({'repeat':repeat,'test_id':test['id'],'test_version':test['version'],
            'input_sha256':digest(inputs),'expected_sha256':digest(test['expected']),
            'observed':values,'observed_sha256':digest(values),'passed':values==test['expected']})
    return rows


def make_report(plan, material, rows=None):
    material,suite,_,cases=validate_material(plan,material); expected=[];remaining=plan['max_evaluations']
    for repeat in range(1,plan['repeats']+1):
        new=evaluate_repeat(plan,material,repeat,remaining);expected.extend(new);remaining-=len(new)
    if rows is not None and bounded_copy(rows)!=expected:
        fail('VALIDATION_FAILED','Trial matrix differs from the pinned deterministic computation')
    repeats=[]; hashes=[];size=len(cases)
    for repeat in range(1,plan['repeats']+1):
        subset=[{k:v for k,v in r.items() if k!='repeat'} for r in expected if r['repeat']==repeat]
        h=digest(subset);complete=len(subset)==size
        repeats.append({'repeat':repeat,'complete':complete,'sha256':h})
        if complete:hashes.append(h)
    completed=len(expected);planned=size*plan['repeats'];incomplete=completed!=planned
    reproducible=None if incomplete or plan['repeats']<2 else len(set(hashes))==1
    mandatory={t['id'] for t in suite['tests'] if t['mandatory']}
    passes=sum(r['passed'] for r in expected)
    accepted=(not any(not r['passed'] and r['test_id'] in mandatory for r in expected)
              and passes*10000>=planned*suite['minimum_pass_basis_points'])
    verdict='INCONCLUSIVE' if incomplete else ('PASS' if accepted else 'FAIL')
    report={'schema_version':1,'format':FORMAT,'run_id':plan['run_id'],'plan_sha256':digest(plan),
        'material_sha256':digest(material),'checker':CHECKER,'scope':'DEVELOPMENT_SYNTHETIC_NOT_RELEASE_QUALIFICATION',
        'authority':'NONE','expected_checks':planned,'completed_checks':completed,'verdict':verdict,
        'stop_reason':'BUDGET_EXHAUSTED' if incomplete else 'COMPLETE','reproducible':reproducible,
        'trials':expected,'repeats':repeats}
    validate(report,'evaluation_report.schema.json');return report


def validate_report(plan,material,report):
    report=bounded_copy(report);validate(report,'evaluation_report.schema.json')
    if report!=make_report(plan,material):
        fail('VALIDATION_FAILED','Stored result differs from its exact inputs, trial matrix or thresholds')
    return report


def comparison_scope(plan,material):
    material,suite,_,_=validate_material(plan,material)
    return digest({'suite':plan['suite'],'fixtures':[f for f in material['files'] if f['role']=='fixture'],
        'repeats':plan['repeats'],'max_evaluations':plan['max_evaluations'],
        'implementation':material['implementation'], 'checker':CHECKER})
