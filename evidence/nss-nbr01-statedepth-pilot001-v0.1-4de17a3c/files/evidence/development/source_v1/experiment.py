"""Actual CPU training/evaluation. Run explicitly; never downloads dependencies."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import sys
import time
import resource

import numpy as np
import torch
from torch import nn
from safetensors.torch import save_file, load_file

from .core import RecallModel, Session, batch, parameter_digest, tensor_bytes, canonical, digest_bytes

ROOT = Path(__file__).resolve().parents[1]


def configure():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    # Disable fused inference fast paths to make query batching/restart checks transparent.
    torch.backends.mha.set_fastpath_enabled(False)


def environment():
    import safetensors
    return {'python':sys.version, 'platform':platform.platform(), 'torch':torch.__version__,
            'numpy':np.__version__, 'safetensors':safetensors.__version__,
            'cuda_available':torch.cuda.is_available(), 'threads':torch.get_num_threads(),
            'scope':'execution_environment_NOT_user_device', 'energy':'NOT_MEASURED',
            'forge':'NOT_CONNECTED', 'runtime':'NOT_CONNECTED'}


def train(kind: str, seed: int, steps: int, output: Path):
    torch.manual_seed(seed)
    model = RecallModel(kind)
    start = {k:v.detach().clone() for k,v in model.state_dict().items()}
    initial_digest = parameter_digest(model)
    opt = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=0.0001)
    g = torch.Generator().manual_seed(10000+seed)
    rng = random.Random(20000+seed)
    batch_hash = hashlib.sha256()
    log=[]; examples=events=0; refinements=0; encoding_work=0
    begin=time.perf_counter(); begin_cpu=time.process_time()
    for step in range(steps):
        delay=rng.randint(0,16); depth=(1,2,4)[step%3]
        x,y=batch(g,64,delay)
        batch_hash.update(x.numpy().tobytes());batch_hash.update(y.numpy().tobytes())
        batch_hash.update(str(depth).encode())
        model.train();opt.zero_grad(set_to_none=True)
        logits=model(x,depth); loss=nn.functional.cross_entropy(logits,y)
        if not torch.isfinite(loss):raise RuntimeError('Nonfinite loss')
        loss.backward()
        if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in model.parameters()):
            raise RuntimeError('Nonfinite gradients')
        grad=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
        opt.step()
        examples+=len(y);events+=x.numel();refinements+=depth*len(y)
        encoding_work += x.numel() if kind=='gru' else 2*len(y)*(x.shape[1]+1)**2
        if step==0 or (step+1)%100==0 or step==steps-1:
            row={'step':step+1,'loss':float(loss.detach()),'grad_norm_before_clipping':float(grad),
                 'batch_accuracy':float((logits.argmax(1)==y).float().mean()),'delay':delay,'depth':depth}
            log.append(row);print(kind,seed,row,flush=True)
    elapsed=time.perf_counter()-begin; cpu=time.process_time()-begin_cpu
    model.eval()
    # Clear gradient tensors before inference memory measurements.
    opt.zero_grad(set_to_none=True)
    tensors={k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()}
    checkpoint=output/f'{kind}_seed{seed}.safetensors'
    save_file(tensors,str(checkpoint))
    reloaded=RecallModel(kind);reloaded.load_state_dict(load_file(str(checkpoint)));reloaded.eval()
    if parameter_digest(model)!=parameter_digest(reloaded):raise RuntimeError('Reload mismatch')
    changed=sum(int(torch.count_nonzero(v-start[k])) for k,v in model.state_dict().items())
    if changed==0:raise RuntimeError('No actual weight update')
    opt_bytes=sum(tensor_bytes(v) for s in opt.state.values() for v in s.values() if isinstance(v,torch.Tensor))
    metrics={'kind':kind,'seed':seed,'steps':steps,'examples':examples,'observed_events':events,
             'train_batch_digest':batch_hash.hexdigest(),'trained_depths':[1,2,4],
             'refinement_vector_steps':refinements,
             'encoding_work_units':encoding_work,
             'encoding_work_unit': 'GRU_event_updates' if kind=='gru' else 'attention_query_key_pairs_across_two_layers',
             'train_wall_seconds':elapsed,'train_process_cpu_seconds':cpu,
             'parameter_count':sum(p.numel() for p in model.parameters()),
             'parameter_bytes':sum(tensor_bytes(p) for p in model.parameters()),
             'gradient_bytes_when_allocated':sum(tensor_bytes(p) for p in model.parameters()),
             'optimizer_tensor_bytes':opt_bytes,'changed_parameter_elements':changed,
             'initial_parameter_digest':initial_digest,'final_parameter_digest':parameter_digest(model),
             'checkpoint_sha256':digest_bytes(checkpoint.read_bytes()),'checkpoint_file_bytes':checkpoint.stat().st_size,
             'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
             'rss_note':'process high-water mark includes interpreter/framework/training copies; not attributable solely to this model',
             'training_logs':log,'exact_weight_reload':True,'evaluation_parameter_updates':0}
    return model,metrics


@torch.no_grad()
def evaluate(model: RecallModel, seed:int, count:int=256):
    before=parameter_digest(model);rows=[]
    for delay in (0,4,16,64,128):
        for ci,cond in enumerate(('early_cue','overwrite','no_cue')):
            g=torch.Generator().manual_seed(300000+seed*100+delay*3+ci)
            x,y=batch(g,count,delay,cond)
            data_digest=digest_bytes(x.numpy().tobytes()+y.numpy().tobytes())
            for keep in (False,True):
                enc_start=time.perf_counter()
                encoded=model.encode(x if keep else x[:,:0])
                enc_time=time.perf_counter()-enc_start
                for depth in (1,2,4,8):
                    ts=time.perf_counter();logits=model.read(encoded,depth);elapsed=time.perf_counter()-ts
                    if not torch.isfinite(logits).all():raise RuntimeError('Nonfinite evaluation output')
                    pred=logits.argmax(1)
                    rows.append({'kind':model.kind,'seed':seed,'delay':delay,'condition':cond,'keep':keep,'depth':depth,
                                 'n':count,'correct':int((pred==y).sum()),'unknown_predictions':int((pred==8).sum()),
                                 'accuracy':float((pred==y).double().mean()),'dataset_sha256':data_digest,
                                 'encoding_batch_seconds':enc_time,'readout_batch_seconds':elapsed,
                                 'note':'encoding cached across depth cells; times are descriptive, not equal-compute measurements'})
    if before!=parameter_digest(model):raise RuntimeError('Evaluation changed weights')
    return rows


@torch.no_grad()
def lifecycle(model:RecallModel, seed:int, output:Path):
    g=torch.Generator().manual_seed(70000+seed)
    x,_=batch(g,1,64,'overwrite');scope=f'pilot-{seed}'
    state=Session(model,scope);state.observe(x[:,:32])
    prefix=state.state.clone();clock=state.events
    repeated=[state.predict(d).clone() for d in (1,2,4,8)]
    if not torch.equal(prefix,state.state) or state.events!=clock:raise RuntimeError('Readout mutated temporal state')
    directory=output/f'{model.kind}_seed{seed}_state'
    state.checkpoint(directory)
    restored=Session.restore(directory,model,scope)
    if not torch.equal(restored.state,state.state):raise RuntimeError('State reload mismatch')
    for d,v in zip((1,2,4,8),repeated):
        if not torch.equal(v,restored.predict(d)):raise RuntimeError('Query reload mismatch')
    state.observe(x[:,32:]);restored.observe(x[:,32:])
    if not torch.equal(state.predict(4),restored.predict(4)):raise RuntimeError('Continuation mismatch')
    scope_rejected=weights_rejected=False
    try:Session.restore(directory,model,scope+'-different')
    except ValueError:scope_rejected=True
    other=RecallModel(model.kind);other.load_state_dict(model.state_dict());
    with torch.no_grad():next(other.parameters()).view(-1)[0].add_(0.01)
    try:Session.restore(directory,other,scope)
    except ValueError:weights_rejected=True
    empty=Session(model,scope+'-reset')
    direct=model(x[:,:0],1)
    reset_equal=torch.equal(empty.predict(1),direct)
    if not(scope_rejected and weights_rejected and reset_equal):raise RuntimeError('Scope/model/reset validation failed')
    return {'seed':seed,'kind':model.kind,'checkpoint_event_count':32,'continued_event_count':state.events,
            'query_does_not_mutate_state':True,'exact_state_restore':True,'exact_continuation':True,
            'wrong_scope_rejected':scope_rejected,'wrong_weights_rejected':weights_rejected,'reset_equals_fresh':reset_equal,
            'raw_prefix_state_bytes':tensor_bytes(prefix),
            'checkpoint_files_total_bytes':sum(p.stat().st_size for p in directory.iterdir()),
            'raw_final_state_bytes':tensor_bytes(state.state)}


@torch.no_grad()
def interventions(model:RecallModel,seed:int,count:int=256):
    g=torch.Generator().manual_seed(90000+seed)
    x,y=batch(g,count,64,'early_cue')
    changed=x.clone();changed[:,0]=(changed[:,0]+1)%8
    distract=x.clone();distract[:,1:]=8+((distract[:,1:]-8+3)%8)
    base=model(x,4).argmax(1);sub=model(changed,4).argmax(1);noise=model(distract,4).argmax(1)
    result={'seed':seed,'kind':model.kind,'n':count,
            'original_accuracy':float((base==y).double().mean()),
            'substituted_cue_accuracy':float((sub==((y+1)%8)).double().mean()),
            'distractor_replacement_accuracy':float((noise==y).double().mean()),
            'distractor_prediction_agreement':float((noise==base).double().mean())}
    if model.kind=='gru':
        h=model.encode(x)
        eps=torch.randn(h.shape,generator=g)*0.1
        corrupt=h+eps
        prediction=model.read(corrupt,4).argmax(1)
        cue=torch.randint(0,8,(count,1),generator=g)
        updated=model.encode(cue,corrupt)
        result.update({'latent_perturbation_std':0.1,'perturbed_accuracy':float((prediction==y).double().mean()),
                       'new_cue_after_perturbation_accuracy':float((model.read(updated,4).argmax(1)==cue[:,0]).double().mean()),
                       'perturbation_scope':'GRU_ONLY_NOT_REPRESENTATION_MATCHED'})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kind',choices=('gru','transformer'),required=True)
    p.add_argument('--seed',type=int,required=True)
    p.add_argument('--steps',type=int,default=600)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--eval-count',type=int,default=256)
    args=p.parse_args()
    if not 1<=args.steps<=2000 or not 8<=args.eval_count<=1024:raise SystemExit('Out-of-budget request')
    configure();args.output.mkdir(parents=True,exist_ok=True)
    result_path=args.output/f'{args.kind}_seed{args.seed}.json'
    if result_path.exists() or (args.output/f'{args.kind}_seed{args.seed}.safetensors').exists():
        raise SystemExit('Refusing to overwrite an existing run')
    manifest={'protocol_sha256':digest_bytes((ROOT/'spec/protocol.json').read_bytes()),
              'source_sha256':{str(p.relative_to(ROOT)):digest_bytes(p.read_bytes()) for p in sorted((ROOT/'nbr01_pilot').glob('*.py'))},
              'environment':environment(),'seed':args.seed,'kind':args.kind,'steps':args.steps}
    (args.output/f'{args.kind}_seed{args.seed}_prerun.json').write_bytes(canonical(manifest)+b'\n')
    model,metrics=train(args.kind,args.seed,args.steps,args.output)
    result={'study':'NBR-01/Pilot001','phase':'PILOT_NOT_CONFIRMATORY','manifest':manifest,'training':metrics,
            'evaluation':evaluate(model,args.seed,args.eval_count),
            'lifecycle':lifecycle(model,args.seed,args.output),
            'interventions':interventions(model,args.seed,args.eval_count)}
    result_path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('COMPLETE',str(result_path),flush=True)


if __name__=='__main__':main()
