from __future__ import annotations
import hashlib, json, os, platform, sys, time
from pathlib import Path
import numpy as np
import torch
from safetensors.torch import load_file


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def write_json(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(obj, indent=2, sort_keys=True, allow_nan=False).encode() + b'\n'
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_bytes(raw); os.replace(tmp, path)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def weights_digest(model):
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode()); h.update(str(tuple(v.shape)).encode()); h.update(str(v.dtype).encode())
        h.update(v.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def source_identity(root):
    root = Path(root)
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*.py'))
            if not any(part in ('reference', 'evidence', '__pycache__') for part in p.relative_to(root).parts)}


def environment():
    import psutil, safetensors
    return dict(python=sys.version, platform=platform.platform(), torch=torch.__version__,
                numpy=np.__version__, safetensors=safetensors.__version__, psutil=psutil.__version__,
                threads=torch.get_num_threads(), cuda=torch.cuda.is_available(),
                scope='SANDBOX_CPU_NOT_USER_DEVICE', energy='NOT_MEASURED',
                forge='NOT_CONNECTED', runtime='NOT_CONNECTED')


def configure():
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)


def load_model(path, kind):
    from .models import MemoryModel
    m = MemoryModel(kind)
    m.load_state_dict(load_file(str(path))); m.eval()
    return m
