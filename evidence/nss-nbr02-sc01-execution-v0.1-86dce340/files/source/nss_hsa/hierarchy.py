"""Versioned graph contract, independent of evidence values and attention arithmetic.

This is the explicit SH01 topology, not an arbitrary recursive hierarchy. Compiling
it never reads task labels, evidence values, learned activations or model weights.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import OrderedDict
import hashlib
import json
import math
from typing import Any, Sequence
import numpy as np
import torch

SCHEMA = 'nss.hsa.topology.v1'
RECORDS_PER_TASK = 4

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()

class HierarchyError(ValueError):
    """Invalid or incompatible topology; code is stable for failure aggregation."""
    def __init__(self, code: str, detail: str = ''):
        self.code = code
        super().__init__(f'{code}: {detail}')

@dataclass(frozen=True)
class Hierarchy:
    dependencies: tuple[tuple[int, ...], ...]
    region_width: int
    scope: str = 'maintenance'

    def __post_init__(self) -> None:
        if not self.dependencies or type(self.region_width) is not int or self.region_width < 1:
            raise HierarchyError('INVALID_LAYOUT')
        if not isinstance(self.scope, str) or not self.scope:
            raise HierarchyError('INVALID_SCOPE')
        if not isinstance(self.dependencies, tuple) or any(not isinstance(d, tuple) for d in self.dependencies):
            raise HierarchyError('MUTABLE_TOPOLOGY')
        for task, deps in enumerate(self.dependencies):
            if len(set(deps)) != len(deps):
                raise HierarchyError('DUPLICATE_DEPENDENCY', str(task))
            if any(type(d) is not int or d < 0 or d >= self.tasks or d == task for d in deps):
                raise HierarchyError('INVALID_DEPENDENCY', str(task))

    @classmethod
    def from_dependencies(cls, dependencies: Sequence[Sequence[int]], *, scope: str = 'maintenance', region_width: int | None = None) -> 'Hierarchy':
        rows = tuple(tuple(d for d in row) for row in dependencies)
        return cls(rows, math.ceil(math.sqrt(len(rows))) if region_width is None else region_width, scope)

    @property
    def tasks(self) -> int: return len(self.dependencies)
    @property
    def regions(self) -> int: return math.ceil(self.tasks / self.region_width)
    @property
    def positions(self) -> int: return 4 * self.tasks + self.regions + 1
    @property
    def global_index(self) -> int: return self.positions - 1

    def to_dict(self) -> dict:
        return {'schema': SCHEMA, 'scope': self.scope, 'region_width': self.region_width,
                'dependencies': [list(d) for d in self.dependencies]}

    @property
    def identity(self) -> str: return digest(self.to_dict())

    def rows(self) -> tuple[tuple[int, ...], ...]:
        """Allowed keys for each query, in a canonical duplicate-free order."""
        n, width, g = self.tasks, self.region_width, self.global_index
        anchors = set(range(4*n, self.positions))
        rows: list[tuple[int, ...]] = []
        for task, deps in enumerate(self.dependencies):
            r = task // width
            keys = set(range(4*task, 4*task+4)) | anchors
            keys.update(4*j for j in range(r*width, min(n, (r+1)*width)))
            for dep in deps: keys.update(range(4*dep, 4*dep+4))
            row = tuple(sorted(keys))
            rows.extend([row] * 4)
        for r in range(self.regions):
            rows.append(tuple(sorted({4*n+r, g} | {4*j for j in range(r*width, min(n, (r+1)*width))})))
        rows.append(tuple(range(4*n, self.positions)))
        return tuple(rows)

@dataclass(frozen=True)
class Bucket:
    start: int
    groups: int
    queries: int
    indices: torch.Tensor  # [batch, groups, key_bound]
    valid: torch.Tensor

@dataclass(frozen=True)
class AttentionPlan:
    """Treat materialized tensors as read-only; validate at trust boundaries."""
    specs: tuple[Hierarchy, ...]
    buckets: tuple[Bucket, ...]
    tensor_digest: str

    @property
    def batch_size(self) -> int: return len(self.specs)
    @property
    def tasks(self) -> int: return self.specs[0].tasks
    @property
    def positions(self) -> int: return self.specs[0].positions
    @property
    def identity(self) -> str: return digest([s.to_dict() for s in self.specs])
    @property
    def device(self) -> torch.device: return self.buckets[0].indices.device

    def assert_matches(self, specs: Sequence[Hierarchy]) -> None:
        if tuple(specs) != self.specs: raise HierarchyError('STALE_TOPOLOGY_PLAN')

    def validate_tensors(self) -> None:
        if _tensor_digest(self.buckets) != self.tensor_digest:
            raise HierarchyError('MUTATED_PLAN_TENSORS')

    def to_bytes(self) -> bytes:
        self.validate_tensors()
        # Serialize authoritative topology, not device-dependent tensors.
        payload = {'schema': 'nss.hsa.plan.v1', 'specs': [s.to_dict() for s in self.specs]}
        return canonical({'payload': payload, 'sha256': digest(payload)})

    @classmethod
    def from_bytes(cls, raw: bytes, *, device: str | torch.device = 'cpu') -> 'AttentionPlan':
        try:
            env = json.loads(raw); p = env['payload']
            if digest(p) != env['sha256']: raise HierarchyError('CORRUPT_PLAN')
            if p['schema'] != 'nss.hsa.plan.v1': raise HierarchyError('WRONG_PLAN_SCHEMA')
            specs = []
            for s in p['specs']:
                if s['schema'] != SCHEMA: raise HierarchyError('WRONG_TOPOLOGY_SCHEMA')
                specs.append(Hierarchy.from_dependencies(s['dependencies'], scope=s['scope'], region_width=s['region_width']))
            return compile_plan(specs, device=device)
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            raise HierarchyError('MALFORMED_PLAN', str(e)) from e

    def accounting(self, *, heads: int = 2, head_dim: int = 16, item_bytes: int = 4) -> dict:
        padded_pairs = sum(b.groups*b.queries*b.indices.shape[-1] for b in self.buckets)*self.batch_size
        valid_pairs = sum(int(b.valid.sum())*b.queries for b in self.buckets)
        packed_values = sum(b.indices.numel() for b in self.buckets)
        return {'positions': self.positions, 'batch_size': self.batch_size,
                'valid_pairs_per_head_layer_batch': valid_pairs,
                'padded_pairs_per_head_layer_batch': padded_pairs,
                'full_dense_pairs_per_head_layer_batch': self.batch_size*self.positions**2,
                'packed_kv_payload_bytes_per_layer': 2*packed_values*heads*head_dim*item_bytes,
                'plan_index_mask_bytes': sum(b.indices.numel()*b.indices.element_size()+b.valid.numel()*b.valid.element_size() for b in self.buckets),
                'note': 'Payload accounting, not whole-process peak memory; Q/result packing and backend workspace are additional.'}

def _tensor_digest(buckets: Sequence[Bucket]) -> str:
    h = hashlib.sha256()
    for b in buckets:
        h.update(canonical([b.start,b.groups,b.queries,list(b.indices.shape)]))
        h.update(b.indices.detach().cpu().numpy().tobytes())
        h.update(b.valid.detach().cpu().numpy().tobytes())
    return h.hexdigest()

def compile_plan(specs: Sequence[Hierarchy], *, device: str | torch.device = 'cpu') -> AttentionPlan:
    """Two batched tiles: all task blocks (Q=4), then region/global blocks (Q=1)."""
    specs = tuple(specs)
    if not specs: raise HierarchyError('EMPTY_BATCH')
    s0 = specs[0]
    if any((s.tasks, s.region_width, s.scope) != (s0.tasks, s0.region_width, s0.scope) for s in specs):
        raise HierarchyError('MIXED_BATCH_LAYOUT_OR_SCOPE')
    all_rows = [s.rows() for s in specs]
    buckets = []
    for start, groups, qcount in ((0, s0.tasks, 4), (4*s0.tasks, s0.regions+1, 1)):
        width = max(len(rows[start+j*qcount]) for rows in all_rows for j in range(groups))
        idx = np.empty((len(specs),groups,width),np.int64)
        valid = np.zeros_like(idx,dtype=bool)
        for bi, rows in enumerate(all_rows):
            for j in range(groups):
                q = start+j*qcount; row = rows[q]
                if any(rows[q+i] != row for i in range(qcount)):
                    raise HierarchyError('NONSHARED_QUERY_GROUP')
                idx[bi,j] = q;idx[bi,j,:len(row)] = row;valid[bi,j,:len(row)] = True
        buckets.append(Bucket(start,groups,qcount,torch.from_numpy(idx).to(device),torch.from_numpy(valid).to(device)))
    result = tuple(buckets)
    return AttentionPlan(specs,result,_tensor_digest(result))

class PlanCache:
    """Bounded LRU of topology plans only. NO activations or learned KV cache."""
    def __init__(self, capacity: int = 8):
        if type(capacity) is not int or capacity < 1: raise HierarchyError('INVALID_CACHE_CAPACITY')
        self.capacity = capacity; self._cache: OrderedDict = OrderedDict();self.hits=0;self.misses=0;self.evictions=0

    def get(self, specs: Sequence[Hierarchy], *, device: str | torch.device = 'cpu') -> AttentionPlan:
        specs = tuple(specs);key=(specs,str(torch.device(device)))
        if key in self._cache:
            self.hits+=1;self._cache.move_to_end(key);return self._cache[key]
        plan=compile_plan(specs,device=device);self.misses+=1;self._cache[key]=plan
        if len(self._cache)>self.capacity:self._cache.popitem(last=False);self.evictions+=1
        return plan

    def __len__(self) -> int: return len(self._cache)
