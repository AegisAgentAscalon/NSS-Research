"""Synthetic selective recall, learned candidates, and isolated state artifacts.

Token values 0..7 are WRITE, 8..15 are DISTRACTOR, 16 is QUERY.
Target 8 means UNKNOWN. Targets never enter a model input or checkpoint.
This deliberately small benchmark is not a general cognition benchmark.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

import torch
from torch import nn
from safetensors.torch import save_file, load_file

SYMBOLS = 8
QUERY = 16
UNKNOWN = 8
MAX_EVENTS = 160
HIDDEN = 32
KINDS = ('gru', 'transformer')


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def parameter_digest(model: nn.Module) -> str:
    h = hashlib.sha256()
    for name, t in sorted(model.state_dict().items()):
        h.update(name.encode()); h.update(str(tuple(t.shape)).encode())
        h.update(str(t.dtype).encode()); h.update(t.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def tensor_bytes(t: torch.Tensor) -> int:
    return t.numel() * t.element_size()


def validate_tokens(tokens: torch.Tensor) -> None:
    if tokens.dtype != torch.int64 or tokens.ndim != 2 or tokens.shape[1] > MAX_EVENTS:
        raise ValueError('Require a bounded [batch, events] int64 observation tape')
    if tokens.shape[0] < 1 or (tokens.numel() and (tokens.min() < 0 or tokens.max() > QUERY)):
        raise ValueError('Invalid observation token')


def oracle(tokens: torch.Tensor) -> torch.Tensor:
    """Independent exact update semantics, used only for labels/explicit control."""
    validate_tokens(tokens)
    state = torch.full((tokens.shape[0],), UNKNOWN, dtype=torch.long)
    for t in tokens.unbind(1):
        state = torch.where(t < SYMBOLS, t, state)
    return state


def batch(generator: torch.Generator, size: int, delay: int, condition: str = 'train'):
    if size < 1 or not 0 <= delay <= 128 or condition not in ('train','early_cue','overwrite','no_cue'):
        raise ValueError('Invalid batch request')
    # Includes delay+1 pre-query events. A second cue may replace a distractor.
    x = torch.randint(8, 16, (size, delay+1), generator=generator)
    if condition == 'train':
        known = torch.rand(size, generator=generator) >= 0.125
        updates = torch.rand(size, delay+1, generator=generator) < 0.12
        updates[:, 0] = True
        updates &= known[:, None]
        values = torch.randint(0, 8, x.shape, generator=generator)
        x = torch.where(updates, values, x)
    elif condition in ('early_cue', 'overwrite'):
        x[:, 0] = torch.randint(0, 8, (size,), generator=generator)
        if condition == 'overwrite' and delay:
            pos = max(1, (delay+1)//2)
            # Replacement always differs from original. Its distribution stays uniform.
            x[:, pos] = (x[:, 0] + torch.randint(1, 8, (size,), generator=generator)) % 8
    return x, oracle(x)


class RecallModel(nn.Module):
    """Two encoding choices, same form of learned post-encoding refinement.

    The Transformer rehydrates the entire retained bounded tape at query time;
    it is not a KV-cache implementation. The GRU processes each event once.
    No query round updates the persistent event state.
    """
    def __init__(self, kind: str):
        super().__init__()
        if kind not in KINDS:
            raise ValueError('Unknown candidate')
        self.kind = kind
        self.embed = nn.Embedding(17, HIDDEN)
        if kind == 'gru':
            self.encoder = nn.GRU(HIDDEN, HIDDEN, batch_first=True)
        else:
            self.layers = nn.ModuleList([
                nn.TransformerEncoderLayer(HIDDEN, 4, 64, dropout=0.0,
                                           batch_first=True, norm_first=True,
                                           activation='gelu') for _ in range(2)])
        self.refine_norm = nn.LayerNorm(HIDDEN)
        self.refine = nn.Sequential(nn.Linear(HIDDEN, 64), nn.GELU(), nn.Linear(64, HIDDEN))
        self.out_norm = nn.LayerNorm(HIDDEN)
        self.head = nn.Linear(HIDDEN, 9)

    def encode(self, events: torch.Tensor, hidden: torch.Tensor | None = None) -> torch.Tensor:
        validate_tokens(events)
        if self.kind == 'gru':
            if events.shape[1] == 0:
                if hidden is not None:
                    return hidden
                return self.embed.weight.new_zeros((1, events.shape[0], HIDDEN))
            _, h = self.encoder(self.embed(events), hidden)
            return h
        if hidden is not None:
            raise ValueError('Transformer uses exact tape, not GRU hidden state')
        q = events.new_full((events.shape[0], 1), QUERY)
        tape = torch.cat((events, q), dim=1)
        z = self.embed(tape)
        # Fixed sinusoidal positions do not have untrained position lookup rows.
        pos = torch.arange(tape.shape[1], dtype=z.dtype)[:, None]
        scale = torch.exp(torch.arange(0, HIDDEN, 2, dtype=z.dtype) * (-math.log(10000.0)/HIDDEN))
        pe = z.new_zeros(tape.shape[1], HIDDEN)
        pe[:, 0::2] = torch.sin(pos*scale)
        pe[:, 1::2] = torch.cos(pos*scale)
        z = z + pe[None]
        for layer in self.layers:
            z = layer(z)
        return z[:, -1, :]

    def read(self, encoded: torch.Tensor, depth: int) -> torch.Tensor:
        if type(depth) is not int or depth not in (1,2,4,8):
            raise ValueError('Depth must be 1,2,4,8')
        h = encoded.squeeze(0) if self.kind == 'gru' else encoded
        z = h
        for _ in range(depth):
            z = z + 0.1*self.refine(self.refine_norm(z))
        return self.head(self.out_norm(z))

    def forward(self, events: torch.Tensor, depth: int = 1, keep: bool = True) -> torch.Tensor:
        return self.read(self.encode(events if keep else events[:, :0]), depth)


class Session:
    """One scope's experimental state; never connected to the NSS database."""
    def __init__(self, model: RecallModel, scope: str, keep: bool = True):
        if not isinstance(scope, str) or not 1 <= len(scope) <= 120 or type(keep) is not bool:
            raise ValueError('Invalid scope/state policy')
        self.model = model
        self.scope = scope
        self.keep = keep
        self.events = 0
        self.state = (torch.zeros(1, 1, HIDDEN) if model.kind == 'gru'
                      else torch.empty(1, 0, dtype=torch.int64))

    @torch.no_grad()
    def observe(self, events: torch.Tensor) -> None:
        validate_tokens(events)
        if events.shape[0] != 1 or self.events + events.shape[1] > MAX_EVENTS:
            raise ValueError('Scope event budget exceeded')
        if torch.any(events == QUERY):
            raise ValueError('QUERY is not a temporal event')
        self.events += events.shape[1]
        if not self.keep:
            return
        if self.model.kind == 'gru':
            self.state = self.model.encode(events, self.state)
        else:
            self.state = torch.cat((self.state, events), dim=1)

    @torch.no_grad()
    def predict(self, depth: int = 1) -> torch.Tensor:
        encoded = self.state if self.model.kind == 'gru' else self.model.encode(self.state)
        return self.model.read(encoded, depth)

    def checkpoint(self, path: Path) -> dict:
        """Atomic local directory publication; data-only safetensors, never pickle."""
        path = Path(path)
        if path.exists():
            raise FileExistsError(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix='.state-', dir=path.parent))
        try:
            save_file({'state': self.state.detach().contiguous()}, str(tmp/'state.safetensors'))
            body = {'schema': 1, 'study': 'NBR-01/Pilot001', 'kind': self.model.kind,
                    'codec': 'fp32-hidden32-v1' if self.model.kind == 'gru' else 'int64-token-tape-v1',
                    'scope': self.scope, 'keep': self.keep, 'events': self.events,
                    'model_digest': parameter_digest(self.model),
                    'state_sha256': digest_bytes((tmp/'state.safetensors').read_bytes()),
                    'raw_state_bytes': tensor_bytes(self.state)}
            envelope = dict(body, metadata_sha256=digest_bytes(canonical(body)))
            (tmp/'metadata.json').write_bytes(canonical(envelope)+b'\n')
            os.rename(tmp, path)
            return envelope
        finally:
            if tmp.exists():
                shutil.rmtree(tmp)

    @classmethod
    def restore(cls, path: Path, model: RecallModel, scope: str, keep: bool = True):
        path = Path(path)
        if (path/'metadata.json').stat().st_size > 8192 or (path/'state.safetensors').stat().st_size > 8192:
            raise ValueError('Oversized state artifact')
        metadata = json.loads((path/'metadata.json').read_text())
        supplied = metadata.pop('metadata_sha256')
        expected_keys = {'schema','study','kind','codec','scope','keep','events','model_digest','state_sha256','raw_state_bytes'}
        if set(metadata) != expected_keys or supplied != digest_bytes(canonical(metadata)):
            raise ValueError('State metadata integrity/shape mismatch')
        codec = 'fp32-hidden32-v1' if model.kind == 'gru' else 'int64-token-tape-v1'
        if (metadata['schema'] != 1 or metadata['study'] != 'NBR-01/Pilot001' or
            metadata['kind'] != model.kind or metadata['scope'] != scope or
            type(metadata['keep']) is not bool or metadata['keep'] != keep or
            metadata['codec'] != codec or metadata['model_digest'] != parameter_digest(model)):
            raise ValueError('Incompatible state owner, weights, format or policy')
        if type(metadata['events']) is not int or not 0 <= metadata['events'] <= MAX_EVENTS:
            raise ValueError('Invalid event clock')
        if digest_bytes((path/'state.safetensors').read_bytes()) != metadata['state_sha256']:
            raise ValueError('State payload integrity mismatch')
        payload = load_file(str(path/'state.safetensors'))
        if set(payload) != {'state'}:
            raise ValueError('Unexpected state tensor')
        state = payload['state']
        if model.kind == 'gru':
            if state.dtype != torch.float32 or tuple(state.shape) != (1,1,HIDDEN) or not torch.isfinite(state).all():
                raise ValueError('Invalid neural state')
            if not keep and torch.count_nonzero(state):
                raise ValueError('State-off cannot retain hidden activity')
        else:
            validate_tokens(state)
            expected_len = metadata['events'] if keep else 0
            if tuple(state.shape) != (1, expected_len) or torch.any(state == QUERY):
                raise ValueError('Tape/clock mismatch')
        if type(metadata['raw_state_bytes']) is not int or tensor_bytes(state) != metadata['raw_state_bytes']:
            raise ValueError('State byte count differs')
        result = cls(model, scope, keep)
        result.state, result.events = state, metadata['events']
        return result
