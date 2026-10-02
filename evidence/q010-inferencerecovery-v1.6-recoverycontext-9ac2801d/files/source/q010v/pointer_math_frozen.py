# Derived from preserved verifier_B/reader_math_audit.py. Only final-logit mask convention
# differs: supplied values remain zero for invalid rows, and no logits are rewritten.
"""Local exact CPU replay plus an independent float64 audit of pointer reads.

This module is verifier-owned. It imports no producer code and treats the
serialized logits, four-field public input, and captured read vector as data.
"""
from __future__ import annotations

import math
from typing import Any, Mapping

import numpy as np
import torch
import torch.nn.functional as torch_functional


class ReaderMathAuditError(ValueError):
    """A serialized reader output failed replay or its independent bound."""


F32_U = 2.0 ** -24
F64_U = 2.0 ** -53
F32_TINY = 2.0 ** -126
F64_SUBNORMAL = float(np.nextafter(np.float64(0.0), np.float64(1.0)))
MASKED_LOGIT = np.float32(-1e4)
NORMALIZE_EPS = 1e-12
MAX_INFORMATIVE_NORMALIZATION_BOUND = 1e-3
UNKNOWN_CODE = np.zeros((1, 1, 17), dtype=np.float32)
UNKNOWN_CODE[0, 0, 16] = np.float32(1.0)


def _gamma(n: int, unit_roundoff: float) -> float:
    product = n * unit_roundoff
    if product >= 1.0:
        raise ReaderMathAuditError("roundoff bound is outside its finite domain")
    return product / (1.0 - product)


def _fsum(values: Any) -> float:
    result = math.fsum(float(value) for value in values)
    if not math.isfinite(result):
        raise ReaderMathAuditError("float64 audit accumulation overflowed")
    return result


def _same_f32_bytes(left: np.ndarray, right: np.ndarray) -> bool:
    a = np.ascontiguousarray(left, dtype=np.float32)
    b = np.ascontiguousarray(right, dtype=np.float32)
    return a.shape == b.shape and a.tobytes(order="C") == b.tobytes(order="C")


def replay_and_audit_pointer_read(
    logits: Any,
    values: Any,
    valid: Any,
    *,
    captured_read_code: Any | None = None,
    captured_weights: Any | None = None,
    captured_pre_norm: Any | None = None,
) -> dict[str, Any]:
    """Replay CPU Torch's declared primitives, then audit with float64 bounds.

    Inputs must be the exact float32 logits and public ``values`` plus boolean
    ``valid`` mask from the evidence bundle. The input contains final logits, already masked by the relevant reader
    contract; this audit does not change them. Invalid public values are zero. The float64 calculations
    independently bound the local CPU float32 softmax, weighted reduction, and
    normalization. A non-informative bound fails closed.
    """
    raw_logits = np.asarray(logits)
    raw_values = np.asarray(values)
    raw_valid = np.asarray(valid)
    if raw_logits.dtype != np.dtype(np.float32) or raw_logits.ndim != 2 or raw_logits.shape[1] != 17:
        raise ReaderMathAuditError("logits must be finite float32 [batch,17]")
    if raw_values.dtype != np.dtype(np.float32) or raw_values.shape != (raw_logits.shape[0], 16, 17):
        raise ReaderMathAuditError("values must be finite float32 [batch,16,17]")
    if raw_valid.dtype != np.dtype(np.bool_) or raw_valid.shape != (raw_logits.shape[0], 16):
        raise ReaderMathAuditError("valid must be boolean [batch,16]")
    if (not np.isfinite(raw_logits).all() or not np.isfinite(raw_values).all()
            or raw_logits.shape[0] == 0):
        raise ReaderMathAuditError("logits/values must be non-empty and finite")
    if np.any(raw_values[~raw_valid] != np.float32(0.0)):
        raise ReaderMathAuditError("public values for invalid rows must be exactly zero")

    # Match the captured CPU arithmetic without changing the caller's global
    # thread setting. The producer's local contract is Torch CPU, float32.
    old_threads = torch.get_num_threads()
    try:
        if old_threads != 1:
            torch.set_num_threads(1)
        with torch.no_grad():
            t_logits = torch.from_numpy(np.ascontiguousarray(raw_logits)).to(device="cpu")
            t_values = torch.from_numpy(np.ascontiguousarray(raw_values)).to(device="cpu")
            t_valid = torch.from_numpy(np.ascontiguousarray(raw_valid)).to(device="cpu")
            masked_t = t_logits.clone()
            # Columnar captures contain FINAL logits, including the exact-control +/-20 convention.
            # Do not remask an already-computed distribution; validate masks at the caller.
            weights_t = torch.softmax(masked_t, dim=-1, dtype=torch.float32)
            null_t = torch.from_numpy(UNKNOWN_CODE).expand(raw_logits.shape[0], -1, -1)
            memory_t = torch.cat((t_values, null_t), dim=1)
            pre_norm_t = torch.einsum("bn,bnd->bd", weights_t, memory_t)
            read_code_t = torch_functional.normalize(
                pre_norm_t, p=2.0, dim=-1, eps=NORMALIZE_EPS,
            )
    finally:
        if old_threads != 1:
            torch.set_num_threads(old_threads)

    weights32 = weights_t.detach().cpu().numpy().copy()
    pre_norm32 = pre_norm_t.detach().cpu().numpy().copy()
    read_code32 = read_code_t.detach().cpu().numpy().copy()
    masked32 = masked_t.detach().cpu().numpy().copy()
    for name, array in (("masked logits", masked32), ("Torch weights", weights32),
                        ("Torch pre_norm", pre_norm32), ("Torch read_code", read_code32)):
        if not np.isfinite(array).all():
            raise ReaderMathAuditError(f"{name} contains overflow or non-finite values")

    if captured_read_code is not None and not _same_f32_bytes(captured_read_code, read_code32):
        raise ReaderMathAuditError("captured read_code is not byte-identical to exact CPU Torch replay")
    if captured_weights is not None and not _same_f32_bytes(captured_weights, weights32):
        raise ReaderMathAuditError("captured pointer weights are not byte-identical to exact CPU Torch replay")
    if captured_pre_norm is not None and not _same_f32_bytes(captured_pre_norm, pre_norm32):
        raise ReaderMathAuditError("captured pre_norm is not byte-identical to exact CPU Torch replay")

    weights64_rows: list[np.ndarray] = []
    x64_rows: list[np.ndarray] = []
    y64_rows: list[np.ndarray] = []
    weight_bounds_rows: list[np.ndarray] = []
    pre_norm_bounds_rows: list[np.ndarray] = []
    normalization_bounds: list[float] = []
    max_weight_residuals: list[float] = []
    max_pre_norm_residuals: list[float] = []
    read_code_residuals: list[float] = []

    for batch_index in range(raw_logits.shape[0]):
        masked64 = raw_logits[batch_index].astype(np.float64, copy=True)
        # Inputs are the same final logits used for the captured pointer copy.
        shift64 = float(np.max(masked64))
        z64 = masked64 - shift64
        try:
            e64 = np.exp(z64)
        except FloatingPointError as exc:
            raise ReaderMathAuditError("float64 exponential failed") from exc
        if not np.isfinite(e64).all():
            raise ReaderMathAuditError("float64 softmax reference overflowed")
        total64 = _fsum(e64)
        if total64 < 1.0:
            raise ReaderMathAuditError("stable float64 softmax denominator is below one")
        w64 = e64 / total64
        if not np.isfinite(w64).all():
            raise ReaderMathAuditError("float64 softmax reference is non-finite")

        # Account for float32 shift/subtraction and the declared local bound of
        # 2u relative error for normal float32 exp outputs. Below the smallest
        # normal, permit full flush-to-zero error. This is a platform contract,
        # not a general theorem about every libm/PyTorch build.
        d = F32_U * np.abs(z64) + F32_TINY
        with np.errstate(over="ignore", invalid="ignore"):
            exp_d = np.exp(d)
            rel_exp_error = np.expm1(d) + 2.0 * F32_U * exp_d
        if not np.isfinite(rel_exp_error).all():
            raise ReaderMathAuditError("softmax exponential allowance overflowed")
        e_error = e64 * rel_exp_error
        subnormal = e64 < F32_TINY
        e_error[subnormal] += e64[subnormal]
        # Preserve an outward bound when the float64 reference itself underflows.
        e_error[(e64 == 0.0) & np.isfinite(z64)] += F64_SUBNORMAL
        if not np.isfinite(e_error).all():
            raise ReaderMathAuditError("softmax absolute error bound overflowed")
        sum_e_plus_error = _fsum(e64 + e_error)
        e_sum_error = (
            _fsum(e_error)
            + _gamma(16, F32_U) * sum_e_plus_error
            + _gamma(18, F64_U) * sum_e_plus_error
        )
        if not math.isfinite(e_sum_error) or e_sum_error >= total64:
            raise ReaderMathAuditError("softmax numerical bound is non-informative")
        weight_bounds = (
            (e_error + w64 * e_sum_error) / (total64 - e_sum_error) * (1.0 + F32_U)
            + F32_U * w64
        )
        if not np.isfinite(weight_bounds).all() or np.any(weight_bounds < 0.0):
            raise ReaderMathAuditError("softmax component bound is non-finite or negative")
        weight_residuals = np.abs(weights32[batch_index].astype(np.float64) - w64)
        if np.any(weight_residuals > weight_bounds):
            index = int(np.argmax(weight_residuals - weight_bounds))
            raise ReaderMathAuditError(
                f"Torch softmax component {index} exceeds the declared float64 bound"
            )

        memory64 = np.concatenate((raw_values[batch_index].astype(np.float64),
                                   np.asarray([[0.0] * 16 + [1.0]], dtype=np.float64)), axis=0)
        products64 = w64[:, None] * memory64
        x64 = np.asarray([_fsum(products64[:, j]) for j in range(17)], dtype=np.float64)
        absolute_f32_products = np.abs(
            weights32[batch_index].astype(np.float64)[:, None] * memory64
        )
        absolute_reference_products = np.abs(products64)
        a_j = np.asarray([_fsum(absolute_f32_products[:, j]) for j in range(17)])
        ref_abs_j = np.asarray([_fsum(absolute_reference_products[:, j]) for j in range(17)])
        weight_effect_j = np.asarray([
            _fsum(weight_bounds * np.abs(memory64[:, j])) for j in range(17)
        ])
        pre_norm_bounds = (
            _gamma(34, F32_U) * a_j
            + weight_effect_j
            + 34.0 * F32_TINY
            + _gamma(34, F64_U) * ref_abs_j
        )
        if not np.isfinite(pre_norm_bounds).all() or np.any(pre_norm_bounds < 0.0):
            raise ReaderMathAuditError("weighted-reduction bound is non-finite or negative")
        pre_norm_residuals = np.abs(pre_norm32[batch_index].astype(np.float64) - x64)
        if np.any(pre_norm_residuals > pre_norm_bounds):
            index = int(np.argmax(pre_norm_residuals - pre_norm_bounds))
            raise ReaderMathAuditError(
                f"Torch pre_norm component {index} exceeds the cancellation-aware bound"
            )

        norm64 = math.hypot(*(float(value) for value in x64))
        denominator64 = max(norm64, NORMALIZE_EPS)
        y64 = x64 / denominator64
        b_y = (
            2.0 * math.hypot(*(float(value) for value in pre_norm_bounds)) / denominator64
            + _gamma(64, F32_U)
            + 17.0 * F32_TINY / denominator64
            + _gamma(64, F64_U)
        )
        if not math.isfinite(b_y) or b_y >= MAX_INFORMATIVE_NORMALIZATION_BOUND:
            raise ReaderMathAuditError(
                f"normalized-code audit is numerically indeterminate (bound={b_y!r})"
            )
        y_residual = math.hypot(*(
            float(a) - float(b)
            for a, b in zip(read_code32[batch_index], y64, strict=True)
        ))
        if not math.isfinite(y_residual) or y_residual > b_y:
            raise ReaderMathAuditError("Torch read_code exceeds the normalized float64 bound")

        weights64_rows.append(w64)
        x64_rows.append(x64)
        y64_rows.append(y64)
        weight_bounds_rows.append(weight_bounds)
        pre_norm_bounds_rows.append(pre_norm_bounds)
        normalization_bounds.append(b_y)
        max_weight_residuals.append(float(np.max(weight_residuals)))
        max_pre_norm_residuals.append(float(np.max(pre_norm_residuals)))
        read_code_residuals.append(float(y_residual))

    return {
        "masked_logits": masked32,
        "weights": weights32,
        "pre_norm": pre_norm32,
        "read_code": read_code32,
        "selected_row": np.argmax(masked32, axis=-1).astype(np.int64, copy=False),
        "weights64": np.stack(weights64_rows),
        "pre_norm64": np.stack(x64_rows),
        "read_code64": np.stack(y64_rows),
        "weight_bounds": np.stack(weight_bounds_rows),
        "pre_norm_bounds": np.stack(pre_norm_bounds_rows),
        "normalization_bounds": np.asarray(normalization_bounds, dtype=np.float64),
        "max_weight_residuals": np.asarray(max_weight_residuals, dtype=np.float64),
        "max_pre_norm_residuals": np.asarray(max_pre_norm_residuals, dtype=np.float64),
        "read_code_residuals": np.asarray(read_code_residuals, dtype=np.float64),
        "audit_contract": "q010v-final-logits-f32-local-replay-plus-f64-bound-v1",
    }


def verify_captured_pointer_arrays(
    logits: Any,
    values: Any,
    valid: Any,
    *,
    captured_read_code: Any,
    captured_weights: Any | None = None,
    captured_pre_norm: Any | None = None,
) -> dict[str, Any]:
    """Convenience wrapper for serialized evidence verifier call sites."""
    try:
        return replay_and_audit_pointer_read(
            logits, values, valid, captured_read_code=captured_read_code,
            captured_weights=captured_weights, captured_pre_norm=captured_pre_norm,
        )
    except (ReaderMathAuditError, RuntimeError, ValueError, TypeError) as exc:
        if isinstance(exc, ReaderMathAuditError):
            raise
        raise ReaderMathAuditError(f"CPU pointer replay/audit failed: {exc}") from exc
