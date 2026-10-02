"""Four independent addresses, eight values, an observed admission score.

An event is [address, value, score] in float32. Addresses/values are exact
small integers. Scores >= 0.5 qualify; lower scores must leave memory alone.
Address 4 is an explicit scope RESET. The score is a synthetic policy signal,
not a calibrated factual confidence or a hidden truth label.
"""
from __future__ import annotations
import hashlib
import torch

KEYS, VALUES, UNKNOWN, RESET = 4, 8, 8, 4
CONDITIONS = ('retain', 'mixed_unknown', 'overwrite', 'interference',
              'near_reject', 'near_write', 'reset', 'noisy_observation')
HORIZONS = (0, 16, 64, 256, 1024, 4096)
MAX_EVENTS = 4200


def validate(x: torch.Tensor) -> None:
    if x.dtype != torch.float32 or x.ndim != 3 or x.shape[-1] != 3:
        raise ValueError('Expected float32 [batch, events, 3]')
    if not 1 <= x.shape[0] <= 512 or not 0 <= x.shape[1] <= MAX_EVENTS:
        raise ValueError('Batch/event budget exceeded')
    if not torch.isfinite(x).all():
        raise ValueError('Nonfinite event')
    if x.numel():
        k, v, q = x.unbind(-1)
        if ((k < 0) | (k > RESET) | (k != k.floor())).any():
            raise ValueError('Invalid address')
        if ((v < 0) | (v >= VALUES) | (v != v.floor())).any():
            raise ValueError('Invalid value')
        if ((q < 0) | (q > 1)).any():
            raise ValueError('Score outside [0,1]')


def labels_loop(x: torch.Tensor) -> torch.Tensor:
    """Sequential environment semantics, used for task targets only."""
    validate(x)
    y = torch.full((len(x), KEYS), UNKNOWN, dtype=torch.long)
    b = torch.arange(len(x))
    for e in x.unbind(1):
        k, v, q = e[:, 0].long(), e[:, 1].long(), e[:, 2]
        reset = k == RESET
        y[reset] = UNKNOWN
        admitted = (~reset) & (q >= 0.5)
        y[b[admitted], k[admitted]] = v[admitted]
    return y


def exact_latest(x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Independent vectorized observation-only control: latest source per key.

    Returns integer answers and a four-record view of actual selected source
    events. Unknown slots get a non-admitted dummy. No target argument exists.
    """
    validate(x)
    B, T, _ = x.shape
    y = torch.full((B, KEYS), UNKNOWN, dtype=torch.long)
    records = x.new_zeros(B, KEYS, 3)
    records[:, :, 0] = torch.arange(KEYS)
    if T == 0:
        return y, records
    t = torch.arange(1, T + 1)[None, :]
    last_reset = torch.where(x[:, :, 0] == RESET, t, 0).amax(1)
    for k in range(KEYS):
        eligible = ((x[:, :, 0] == k) & (x[:, :, 2] >= 0.5)
                    & (t > last_reset[:, None]))
        idx = torch.where(eligible, t, 0).amax(1)
        has = idx > 0
        b = torch.arange(B)[has]
        records[has, k] = x[b, idx[has] - 1]
        y[has, k] = records[has, k, 1].long()
    return y, records


def _events(g: torch.Generator, n: int, length: int) -> torch.Tensor:
    x = torch.empty(n, length, 3, dtype=torch.float32)
    x[:, :, 0] = torch.randint(KEYS, (n, length), generator=g)
    x[:, :, 1] = torch.randint(VALUES, (n, length), generator=g)
    x[:, :, 2] = 0.05 + 0.40 * torch.rand(n, length, generator=g)
    return x


def training_batch(g: torch.Generator, n: int, length: int) -> tuple[torch.Tensor, torch.Tensor]:
    if not 1 <= length <= 64:
        raise ValueError('Training length must be in 1..64')
    x = _events(g, n, length)
    # Independent eligibility for each address creates missing-record examples.
    can_write = torch.rand(n, KEYS, generator=g) >= 0.25
    permitted = can_write.gather(1, x[:, :, 0].long())
    admits = (torch.rand(n, length, generator=g) < 0.30) & permitted
    qhi = 0.55 + 0.40 * torch.rand(n, length, generator=g)
    x[:, :, 2] = torch.where(admits, qhi, x[:, :, 2])
    # Ten percent of streams have an explicit mid-stream reset.
    if length >= 4:
        reset = torch.rand(n, generator=g) < 0.10
        x[reset, length // 2, 0] = RESET
        x[reset, length // 2, 2] = 0.0
    return x, labels_loop(x)


def evaluation_batch(seed: int, condition: str, horizon: int, n: int = 128):
    if condition not in CONDITIONS or horizon not in HORIZONS:
        raise ValueError('Unknown registered condition/horizon')
    ci = CONDITIONS.index(condition)
    g = torch.Generator().manual_seed(8_000_000 + seed * 100_000 + ci * 10_000 + horizon)
    # Eight prefix events in all conditions: one record per address followed
    # by four rejection events, real overwrites, or a reset + new scope.
    x = _events(g, n, 8 + horizon)
    keys = torch.rand(n, KEYS, generator=g).argsort(1)
    x[:, :4, 0] = keys
    x[:, :4, 2] = 0.80 + 0.15 * torch.rand(n, KEYS, generator=g)
    protected = keys[:, 0].long()
    if condition == 'mixed_unknown':
        x[:, 2:4, 2] = 0.10
    elif condition == 'overwrite':
        x[:, 4:8, 0] = keys
        x[:, 4:8, 1] = (x[:, :4, 1] + torch.randint(1, VALUES, (n, KEYS), generator=g)) % VALUES
        x[:, 4:8, 2] = 0.85
    elif condition == 'interference' and horizon:
        suffix = x[:, 8:]
        valid_other = ((suffix[:, :, 0] != protected[:, None]) &
                       (torch.rand(n, horizon, generator=g) < 0.40))
        suffix[:, :, 2] = torch.where(valid_other, 0.85, suffix[:, :, 2])
    elif condition == 'near_reject':
        # Visible, unambiguous by the declared policy, but outside train margin.
        x[:, 4:, 2] = 0.480 + 0.019 * torch.rand(n, 4 + horizon, generator=g)
    elif condition == 'near_write':
        x[:, :4, 2] = 0.501 + 0.019 * torch.rand(n, 4, generator=g)
    elif condition == 'reset':
        x[:, 4, 0] = RESET
        x[:, 4, 2] = 0.0
        x[:, 5:7, 0] = keys[:, :2]
        x[:, 5:7, 1] = (x[:, :2, 1] + 1) % VALUES
        x[:, 5:7, 2] = 0.85
    if condition == 'noisy_observation' and horizon:
        # Hidden intended scores are used ONLY to establish environment truth.
        # Every inference arm receives only the same corrupted observations.
        admitted = torch.rand(n, horizon, generator=g) < 0.08
        x[:, 8:, 2] = torch.where(admitted,
            0.55 + 0.20 * torch.rand(n, horizon, generator=g),
            0.25 + 0.20 * torch.rand(n, horizon, generator=g))
    y = labels_loop(x)
    if condition == 'noisy_observation':
        noise = 0.10 * torch.randn(x[:, :, 2].shape, generator=g)
        x[:, :, 2] = (x[:, :, 2] + noise).clamp(0, 1)
    exact, _ = exact_latest(x)
    if condition != 'noisy_observation' and not torch.equal(y, exact):
        raise RuntimeError('Independent exact control disagrees with environment')
    return x, y, protected


def digest(x: torch.Tensor, y: torch.Tensor) -> str:
    return hashlib.sha256(x.contiguous().numpy().tobytes() + y.contiguous().numpy().tobytes()).hexdigest()
