"""Learned memory mechanisms with openly engineered exact address dispatch.

All arms see the same events. A four-slot organization and an explicit RESET
boundary are supplied, not learned. This study does not prove learned binding
of arbitrary names. The full-tape reader is a two-block cross-attention
Transformer, not the Pilot001 all-token self-attention encoder.
"""
from __future__ import annotations
import math
import torch
from torch import nn
from .data import KEYS, RESET, validate

WIDTH = 16
KINDS = ('soft_slots', 'hard_slots', 'gru_slots', 'tape_reader')


class CrossBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.attn = nn.MultiheadAttention(WIDTH, 2, dropout=0, batch_first=True)
        self.norm1 = nn.LayerNorm(WIDTH)
        self.norm2 = nn.LayerNorm(WIDTH)
        self.mlp = nn.Sequential(nn.Linear(WIDTH, 32), nn.GELU(), nn.Linear(32, WIDTH))
        self.age_strength = nn.Parameter(torch.tensor(0.5))

    def forward(self, z, memory, allowed, age):
        # Attention scores retain access to every event, with learned relative
        # log-age bias. No fixed context window or untrained position table.
        B, K, _ = z.shape
        bias = -nn.functional.softplus(self.age_strength) * torch.log1p(age)
        bias = bias[:, None, :].expand(B, K, -1).masked_fill(~allowed, float('-inf'))
        bias = bias[:, None].expand(B, 2, K, -1).reshape(B * 2, K, -1)
        a, _ = self.attn(self.norm1(z), memory, memory, attn_mask=bias, need_weights=False)
        z = z + a
        return z + self.mlp(self.norm2(z))


class MemoryModel(nn.Module):
    def __init__(self, kind: str):
        super().__init__()
        if kind not in KINDS:
            raise ValueError('Unknown architecture')
        self.kind = kind
        self.value = nn.Embedding(8, WIDTH)
        if kind in ('soft_slots', 'hard_slots'):
            self.gate = nn.Sequential(nn.Linear(1, 16), nn.Tanh(), nn.Linear(16, 1))
        elif kind == 'gru_slots':
            self.cell = nn.GRUCell(WIDTH + 1, WIDTH)
        else:
            self.event = nn.Linear(WIDTH + 1, WIDTH)
            self.empty = nn.Parameter(torch.randn(WIDTH) * 0.1)
            self.query = nn.Parameter(torch.randn(WIDTH) * 0.1)
            self.blocks = nn.ModuleList([CrossBlock(), CrossBlock()])
        self.head = nn.Sequential(nn.LayerNorm(WIDTH), nn.Linear(WIDTH, 32),
                                  nn.GELU(), nn.Linear(32, 9))

    def gates(self, x):
        if self.kind not in ('soft_slots', 'hard_slots'):
            raise ValueError('No scalar admission gate')
        return torch.sigmoid(self.gate(x[:, :, 2:3])).squeeze(-1)

    def encode(self, x, state=None, mode='native', threshold=0.5):
        validate(x)
        if mode not in ('native', 'hard', 'close_low') or not 0 <= threshold <= 1:
            raise ValueError('Invalid transition policy')
        if self.kind == 'tape_reader':
            if state is not None:
                raise ValueError('Tape reader retains source events, not slot state')
            return self._tape(x)
        B, T, _ = x.shape
        h = x.new_zeros(B, KEYS, WIDTH) if state is None else state
        if h.shape != (B, KEYS, WIDTH) or h.dtype != torch.float32 or not torch.isfinite(h).all():
            raise ValueError('Incompatible slot state')
        if T == 0:
            return h
        keys = x[:, :, 0].long()
        val = self.value(x[:, :, 1].long())
        if self.kind == 'gru_slots':
            inputs = torch.cat((val, x[:, :, 2:3]), -1)
            for t in range(T):
                k = keys[:, t]
                old = h[torch.arange(B), k.clamp_max(KEYS - 1)]
                new = self.cell(inputs[:, t], old)
                onehot = nn.functional.one_hot(k.clamp_max(KEYS - 1), KEYS).to(x.dtype)
                h = h * (1 - onehot[:, :, None]) + new[:, None, :] * onehot[:, :, None]
                h = torch.where((k == RESET)[:, None, None], torch.zeros_like(h), h)
            return h
        g = self.gates(x)
        if self.kind == 'hard_slots' and mode == 'native':
            discrete = (g >= threshold).to(g.dtype)
            g = g + (discrete - g).detach()  # explicit straight-through training
        elif mode == 'hard':
            g = (g >= threshold).to(g.dtype)
        elif mode == 'close_low':
            g = torch.where(g >= threshold, g, 0.0)
        match = (keys[:, :, None] == torch.arange(KEYS)).to(x.dtype)
        writes = g[:, :, None] * match
        # Closed-form affine recurrence. Exclusive products avoid division by
        # zero for hard gates, and do not retain an ever-growing serving tape.
        a = 1 - writes
        a = torch.where((keys == RESET)[:, :, None], torch.zeros_like(a), a)
        reverse = torch.flip(a, (1,))
        prod = torch.cumprod(reverse, dim=1)
        exclusive = torch.flip(torch.cat((torch.ones_like(prod[:, :1]), prod[:, :-1]), 1), (1,))
        coefficients = exclusive * writes
        return h * prod[:, -1, :, None] + torch.einsum('btk,bth->bkh', coefficients, val)

    def _tape(self, x):
        B, T, _ = x.shape
        ev = self.event(torch.cat((self.value(x[:, :, 1].long()), x[:, :, 2:3]), -1))
        memory = torch.cat((self.empty[None, None, :].expand(B, 1, -1), ev), 1)
        t = torch.arange(T, device=x.device)[None, :].expand(B, -1)
        last_reset = torch.where(x[:, :, 0] == RESET, t, -1).amax(1) if T else torch.full((B,), -1)
        allowed = ((x[:, None, :, 0] == torch.arange(KEYS)[None, :, None]) &
                   (t[:, None, :] > last_reset[:, None, None]))
        allowed = torch.cat((torch.ones(B, KEYS, 1, dtype=torch.bool), allowed), -1)
        # The empty token is older than all real events.
        age = torch.cat((torch.full((B, 1), float(T)), (T - 1 - t).float()), 1)
        z = self.query[None, None].expand(B, KEYS, -1)
        for block in self.blocks:
            z = block(z, memory, allowed, age)
        return z

    def forward(self, x, mode='native', threshold=0.5):
        return self.head(self.encode(x, mode=mode, threshold=threshold))

    @torch.no_grad()
    def predict_chunked(self, x, mode='native', threshold=0.5, chunk=256):
        validate(x)
        if self.kind == 'tape_reader':
            return self(x)
        h = x.new_zeros(len(x), KEYS, WIDTH)
        for start in range(0, x.shape[1], chunk):
            h = self.encode(x[:, start:start + chunk], h, mode, threshold)
        return self.head(h)
