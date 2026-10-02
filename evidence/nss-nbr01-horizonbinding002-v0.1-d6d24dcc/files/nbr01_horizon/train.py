"""Small task-specific preparation, not an alternative generic Forge engine."""
from __future__ import annotations
import hashlib, json, random, time
from pathlib import Path
import torch
from torch import nn
from safetensors.torch import save_file
from .data import training_batch
from .models import MemoryModel
from .util import weights_digest, write_json, source_identity, sha, environment


def train(root, output, kind, seed, curriculum, steps):
    root, output = Path(root), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    stem = f'{kind}_{curriculum}_seed{seed}'
    target = output / (stem + '.json')
    if target.exists() or (output / (stem + '.safetensors')).exists():
        raise FileExistsError('Refuse to overwrite a completed run')
    maxlen = {'short': 16, 'wide': 64}[curriculum]
    torch.manual_seed(seed)
    m = MemoryModel(kind)
    initial = {k: v.detach().clone() for k, v in m.state_dict().items()}
    init_digest = weights_digest(m)
    opt = torch.optim.AdamW(m.parameters(), lr=0.003, weight_decay=0.0001)
    g = torch.Generator().manual_seed(100_000 + seed)
    r = random.Random(200_000 + seed)
    out_prerun = output / (stem + '.prerun.json')
    write_json(out_prerun, dict(status='NOT_RUN', time_unix=time.time(), source=source_identity(root),
        protocol_sha256=sha(root/'spec/protocol.json'), kind=kind, seed=seed,
        curriculum=curriculum, steps=steps, initial_parameter_digest=init_digest))
    h = hashlib.sha256(); logs = []; events = 0
    t0, cpu0 = time.perf_counter(), time.process_time()
    import psutil, threading
    proc = psutil.Process(); rss = [proc.memory_info().rss]; stop = threading.Event()
    def sample():
        while not stop.wait(.005):
            rss.append(proc.memory_info().rss)
    thread = threading.Thread(target=sample, daemon=True); thread.start()
    try:
        for step in range(steps):
            length = r.randint(1, maxlen)
            x, y = training_batch(g, 48, length)
            h.update(x.numpy().tobytes()); h.update(y.numpy().tobytes())
            events += len(x) * length
            m.train(); opt.zero_grad(set_to_none=True)
            z = m(x); loss = nn.functional.cross_entropy(z.reshape(-1, 9), y.flatten())
            if not torch.isfinite(loss):
                raise RuntimeError('Nonfinite loss')
            loss.backward()
            if any(p.grad is not None and not torch.isfinite(p.grad).all() for p in m.parameters()):
                raise RuntimeError('Nonfinite gradient')
            norm = nn.utils.clip_grad_norm_(m.parameters(), 1.)
            opt.step()
            if step == 0 or (step+1) % 150 == 0 or step == steps-1:
                row = dict(step=step+1, loss=float(loss.detach()),
                           accuracy=float((z.argmax(-1)==y).float().mean()),
                           length=length, grad_norm=float(norm))
                logs.append(row); print(stem, row, flush=True)
    finally:
        stop.set(); thread.join(); rss.append(proc.memory_info().rss)
    elapsed, cpu = time.perf_counter()-t0, time.process_time()-cpu0
    opt_bytes = sum(v.numel()*v.element_size() for s in opt.state.values() for v in s.values() if torch.is_tensor(v))
    opt.zero_grad(set_to_none=True); m.eval()
    tensors = {k: v.detach().contiguous() for k, v in m.state_dict().items()}
    p = output / (stem + '.safetensors'); save_file(tensors, str(p))
    changed = sum(int((v != initial[k]).sum()) for k,v in m.state_dict().items())
    if changed == 0:
        raise RuntimeError('No learned parameter changed')
    result = dict(kind=kind, seed=seed, curriculum=curriculum, steps=steps,
        examples=steps*48, supervised_key_answers=steps*48*4, observed_events=events,
        train_batch_sha256=h.hexdigest(), initial_parameter_digest=init_digest,
        final_parameter_digest=weights_digest(m), changed_parameter_elements=changed,
        parameter_count=sum(p.numel() for p in m.parameters()),
        parameter_bytes=sum(p.numel()*p.element_size() for p in m.parameters()),
        gradient_bytes_when_allocated=sum(p.numel()*p.element_size() for p in m.parameters()),
        optimizer_tensor_bytes=opt_bytes, train_wall_seconds=elapsed, train_cpu_seconds=cpu,
        rss_process_peak_5ms_sample_bytes=max(rss), logs=logs,
        checkpoint_sha256=sha(p), checkpoint_bytes=p.stat().st_size,
        preparation_only=True, evaluation_parameter_updates=0, environment=environment(),
        timing_excludes='Interpreter startup, evaluation, calibration, replay, reporting, all other fits')
    write_json(target,result)
    return m, result
