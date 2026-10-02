"""Report-derived no-training cap variant; original parent source is unchanged.

The report identifies a cap change from 80 to 20000. This new implementation
copies the recovered ungated match weights and changes only the declared cap.
It is not asserted to be the missing original 010 implementation.
"""
from __future__ import annotations
import copy
import math
import torch
from torch import nn
from torch.nn import functional as F

class CapOnlyRecordHop(nn.Module):
    def __init__(self, recovered_reader: nn.Module, cap: float = 20000.0):
        super().__init__()
        if not math.isfinite(cap) or cap <= 0:
            raise ValueError('cap must be positive and finite')
        if getattr(recovered_reader, 'gated', False):
            raise ValueError('Only the recovered ungated RecordHop is supported')
        self.match = copy.deepcopy(recovered_reader.match)
        self.cap = float(cap)
        self.eval()
        for p in self.parameters():
            p.requires_grad_(False)

    def forward(self, keys, vals, present, q, depth: int = 4):
        if not isinstance(depth, int) or depth < 1:
            raise ValueError('depth must be a positive integer')
        empty = torch.zeros_like(q)
        empty[:, -1] = 1
        values = torch.cat([vals, empty[:, None, :]], 1)
        h, out = q, []
        for _ in range(depth):
            a = F.normalize(self.match.q(h), dim=-1)
            b = F.normalize(self.match.k(keys), dim=-1)
            sim = torch.einsum('bd,bnd->bn', a, b)
            logits = (sim - self.match.threshold) * self.match.log_scale.exp().clamp(max=self.cap)
            logits = logits.masked_fill(~present, -1e4)
            logits = torch.cat([logits, torch.zeros_like(logits[:, :1])], -1)
            h = F.normalize(torch.einsum('bn,bnd->bd', logits.softmax(-1), values), dim=-1)
            out.append(h)
        return torch.stack(out, 1)
