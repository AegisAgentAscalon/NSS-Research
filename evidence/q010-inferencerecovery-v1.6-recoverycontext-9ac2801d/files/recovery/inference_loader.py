"""Read-only binding of v1.4 exports to their original protocol; never a trainer restore."""
from pathlib import Path
from typing import Any
import hashlib, json
import numpy as np
import torch
from safetensors.torch import load_file

ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/'workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0'
EXPECTED_PROTOCOL='0425f7a75643f3f6f612b754d6d65c86541ef753ad92fe8fafa26ddd33db9ff5'
SEEDS=tuple(range(1201,1206)); ARMS={'ordinary':'ordinary_continuation','near':'close_identity_continuation','attention':'task_adapted_attention'}

def sha(path:Path)->str:
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(path:Path)->Any:
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    return json.loads(path.read_text(),object_pairs_hook=unique)
def safe(base:Path,name:str)->Path:
    rel=Path(name)
    if rel.is_absolute() or '..' in rel.parts:raise ValueError('unsafe artifact path')
    p=base
    for part in rel.parts:
        p=p/part
        if p.is_symlink():raise ValueError('symlink artifact path')
    if not p.is_file() or not p.resolve().is_relative_to(base.resolve()):raise ValueError('absent or escaping artifact')
    return p

def deny_training()->None:
    """Fail closed if this evaluation process attempts optimization or backpropagation."""
    def forbidden(*args,**kwargs):raise RuntimeError('INFERENCE_ONLY: optimizer/backpropagation forbidden')
    torch.optim.Optimizer.__init__=forbidden
    torch.autograd.backward=forbidden
    torch.autograd.grad=forbidden
    torch.set_grad_enabled(False)

def inspect_exports(root:Path=ROOT)->dict:
    from q010r.training import _hash_tensor_map
    from q010r.models import model_state_hash_from_state
    p=root/'protocol/ORIGINAL_FROZEN_PROTOCOL.json'
    if sha(p)!=EXPECTED_PROTOCOL:raise ValueError('original protocol mismatch')
    protocol=read(p)
    if protocol['id']!='NSS_NBR01_Q010_Reconstruction_v1.4' or protocol['main_seeds']!=list(SEEDS):raise ValueError('wrong protocol domain')
    exports=root/'provenance/saved_main_exports'; records=root/'provenance/saved_main_records'
    manifest=read(exports/'WEIGHTS_MANIFEST.json');lock=read(root/'protocol/ORIGINAL_CHECKPOINT_ROSTER_LOCK.json')
    expected={(s,r) for s in SEEDS for r in ARMS}
    for rows,label in [(manifest['files'],'exports'),(lock['rows'],'original roster')]:
        if len(rows)!=15 or {(x['seed'],x['role']) for x in rows}!=expected:raise ValueError('incomplete/duplicate '+label)
    out=[]
    for rec in manifest['files']:
        seed,role=rec['seed'],rec['role'];arm=ARMS[role]
        if rec['arm']!=arm or rec['file']!=f'{role}_{seed}.safetensors' or rec['updates']!=6000:raise ValueError('export binding')
        lr=next(r for r in lock['rows'] if (r['seed'],r['role'])==(seed,role))
        folder=f'results/main_fits/seed{seed}/{role}'
        if lr['manifest']!=folder+'/fit_manifest.json' or lr['complete']!=folder+'/COMPLETE.json' or lr['checkpoint']!=folder+'/final_checkpoint.pt.xz':raise ValueError('roster path binding')
        fm_path=safe(records,lr['manifest']);cp_path=safe(records,lr['complete'])
        if sha(fm_path)!=lr['manifest_sha256'] or sha(cp_path)!=lr['complete_sha256']:raise ValueError('record hash mismatch')
        fm=read(fm_path);complete=read(cp_path);ident=fm['identity'];cfg=ident['config']
        if any(x!=seed for x in [fm['paired_seed'],ident['paired_seed'],cfg['paired_seed'],complete['seed']]):raise ValueError('seed mismatch')
        if any(x!=arm for x in [fm['arm'],ident['arm'],cfg['arm']]) or complete['role']!=role:raise ValueError('arm mismatch')
        if complete['attempt_role']!='main' or cfg['fit_role']!='main' or cfg['study_phase']!='main_fits':raise ValueError('development/reproduction substitution')
        if any(x!=6000 for x in [fm['completed_steps'],fm['data_cursor']['next_batch_index'],complete['updates'],cfg['max_steps']]):raise ValueError('incomplete recorded cursor')
        if any(x!=EXPECTED_PROTOCOL for x in [fm['protocol_sha256'],ident['protocol_sha256'],complete['protocol_sha256']]):raise ValueError('rebound protocol')
        seeds=protocol['rng'][str(seed)][role]
        if cfg['sampler_seed']!=seeds['sampler_seed'] or cfg['training_torch_seed']!=seeds['training_torch_seed']:raise ValueError('RNG domain mismatch')
        for name,h in ident['source']['files'].items():
            src=STAGE/name if name.startswith('plan/') else STAGE/'implementation_A/q010r'/name
            if sha(src)!=h:raise ValueError('original source drift: '+name)
        file=safe(exports,rec['file'])
        if sha(file)!=rec['sha256']:raise ValueError('raw export hash mismatch')
        state=load_file(str(file),device='cpu')
        if any(v.dtype!=torch.float32 or not bool(torch.isfinite(v).all()) for v in state.values()):raise ValueError('nonfloat32/nonfinite export')
        strict=_hash_tensor_map(state);public=model_state_hash_from_state(state)
        if any(x!=strict for x in [rec['strict_sha256'],lr['final_strict_sha256'],complete['final_strict_sha256'],fm['final_checkpoint']['model_state_sha256']]):raise ValueError('strict dtype-inclusive hash mismatch')
        if any(x!=public for x in [rec['public_sha256'],lr['final_public_sha256'],complete['final_public_sha256'],fm['final_weight_sha256']]):raise ValueError('public hash mismatch')
        parameters=sum(v.numel() for v in state.values()); nbytes=sum(v.numel()*v.element_size() for v in state.values())
        if parameters!=rec['parameters'] or parameters!=(86464 if role=='attention' else 818) or nbytes!=rec['tensor_bytes']:raise ValueError('architecture size mismatch')
        trace=records/folder/'numeric_trace.npz'
        trace_present=trace.is_file()
        if trace_present:
            safe(records,folder+'/numeric_trace.npz')
            with np.load(trace,allow_pickle=False) as z:
                if not np.array_equal(z['optimizer_step'],np.arange(1,6001)) or len(z['loss'])!=6000 or not np.isfinite(z['loss']).all():raise ValueError('recorded trace invalid')
        if (records/rec['source_checkpoint']).exists():raise ValueError('unexpected full checkpoint; review scope')
        out.append(dict(seed=seed,role=role,arm=arm,file=rec['file'],sha256=rec['sha256'],strict_sha256=strict,public_sha256=public,parameters=parameters,tensor_bytes=nbytes,recorded_updates=6000,trace_sha256=sha(trace) if trace_present else None,raw_numeric_trace_available=trace_present,trace_status="freshly_verified" if trace_present else "missing_here_previously_audited_in_v15",fit_manifest_sha256=sha(fm_path),original_checkpoint_recorded_sha256=lr['checkpoint_sha256'],full_optimizer_rng_checkpoint_available=False,partial_stream_rng_metadata_present=True,original_start_public_sha256=lr['start_public_sha256']))
    return dict(status='PASS_SAVED_EXPORT_BINDING_NOT_TRAINING_REPRODUCTION',models=out,original_protocol_sha256=EXPECTED_PROTOCOL,original_roster_sha256=sha(root/'protocol/ORIGINAL_CHECKPOINT_ROSTER_LOCK.json'),exports_manifest_sha256=sha(exports/'WEIGHTS_MANIFEST.json'),new_optimizer_updates=0,training_resume_supported=False)

def load_readers(seed:int,root:Path=ROOT)->tuple[dict,dict]:
    from q010r.models import load_parent_reader, AttentionPointerReader,model_state_hash
    if type(seed) is not int or seed not in SEEDS:raise ValueError('unknown main paired seed')
    audit=inspect_exports(root); models={};identities={}
    for role,cap in [('inherited',80.),('cap_only',20000.)]:
        model,receipt=load_parent_reader(seed-400,cap=cap);model.requires_grad_(False);model.eval()
        rid=f'inherited_{seed-400}' if role=='inherited' else role
        receipt['weights_path']=str(Path(receipt['weights_path']).relative_to(root));receipt['public_sha256']=model_state_hash(model);receipt['paired_seed']=seed
        models[rid]=model;identities[rid]=receipt
    for rec in audit['models']:
        if rec['seed']!=seed:continue
        role=rec['role'];state=load_file(str(root/'provenance/saved_main_exports'/rec['file']),device='cpu')
        model=AttentionPointerReader() if role=='attention' else load_parent_reader(seed-400,cap=20000.)[0]
        model.load_state_dict(state,strict=True);model.requires_grad_(False);model.eval()
        if model_state_hash(model)!=rec['public_sha256']:raise ValueError('loaded model mismatch')
        if role!='attention' and identities['cap_only']['public_sha256']!=rec['original_start_public_sha256']:raise ValueError('inherited pairing mismatch')
        models[role]=model;identities[role]=dict(rec,scope='ORIGINAL_V14_MAIN_EXPORT_INFERENCE_ONLY',original_protocol_sha256=EXPECTED_PROTOCOL)
    models['exact_owner']=None;identities['exact_owner']={'kind':'privileged actual-owner traversal','source_sha256':sha(root/'source/q010c/batch_core.py')}
    return models,identities
