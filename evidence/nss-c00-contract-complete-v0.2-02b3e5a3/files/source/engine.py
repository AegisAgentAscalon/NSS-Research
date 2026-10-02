"""Deterministic finite-panel review. Only an explicit public dictionary is input."""
from __future__ import annotations
import hashlib
import json

REVIEW_CALLS = 0


def canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(obj: object) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def target_probability(p1: int, label: int) -> int:
    return p1 if label else 1000-p1


def review(public: dict) -> dict:
    """No IO, mutable shared state, hidden outcome, threshold fitting or model calls."""
    global REVIEW_CALLS
    REVIEW_CALLS += 1
    if REVIEW_CALLS > 10000: raise RuntimeError("RULE_EVALUATION_CAP")
    ih = digest(public)
    def answer(decision, reasons, metrics=None):
        return {"decision": decision, "reasons": sorted(set(reasons)),
                "input_hash": ih, "metrics": metrics or {},
                "review_version": "C00_RULE_V2"}
    try:
        s, c, p = public["snapshot"], public["candidate"], public["policy"]
        for k in ("min_focal", "min_old", "parent_drop", "epoch_drop"):
            if type(p[k]) is not int or not 0 <= p[k] <= 1000:
                return answer("REJECT", ["BAD_POLICY"])
        if type(public["tick"]) is not int or type(c["deadline"]) is not int:
            return answer("REJECT", ["BAD_CLOCK"])
        if public["tick"] < 0 or c["deadline"] < 0:
            return answer("REJECT", ["BAD_CLOCK"])
        if any(type(c[k]) is not bool for k in ("permitted","authority_valid","state_compatible","pending_trace")):
            return answer("REJECT",["BAD_BOOLEAN_FIELD"])
        reasons=[]
        if c["domain"] != "parameter_candidate": reasons.append("WRONG_DOMAIN")
        if not c["permitted"]: reasons.append("NO_PERMISSION")
        if c["evidence_origin"] != "verified_fixture": reasons.append("UNSUPPORTED_ORIGIN")
        if not c["authority_valid"]: reasons.append("INVALID_AUTHORITY")
        if digest(c["artifact"]) != c["artifact_hash"]: reasons.append("ARTIFACT_HASH")
        if c["measured_artifact"] != c["artifact_hash"]: reasons.append("MEASUREMENT_BINDING")
        if c["artifact"]["revision_id"] != c["revision_id"]: reasons.append("CANDIDATE_ID")
        measurements=c["artifact"]["p1_milli"]
        for value in measurements.values():
            if type(value) is not int or not 0<=value<=1000: reasons.append("BAD_PROBABILITY")
        for spec in s["requirements"].values():
            if type(spec["target"]) is not int or spec["target"] not in (0,1): reasons.append("BAD_TARGET")
        if reasons: return answer("REJECT", reasons)
        reasons=[]
        if c["parent_id"] != s["accepted_id"]: reasons.append("STALE_PARENT")
        if c["epoch_id"] != s["epoch_id"]: reasons.append("STALE_EPOCH")
        if c["schema_id"] != s["schema_id"]: reasons.append("SCHEMA_MISMATCH")
        if c["completion"] != "committed": reasons.append("UNKNOWN_COMPLETION")
        if c["state_compatible"] is not True: reasons.append("STATE_UNRESOLVED")
        if c["pending_trace"] is not False: reasons.append("PENDING_TRACE")
        if c["receipt_cutoff"] > s["cutoff"]: reasons.append("FUTURE_EVIDENCE")
        req=s["requirements"]
        if set(measurements) != set(req): reasons.append("INCOMPLETE_PANEL")
        if set(c["receipt_revisions"]) != set(req): reasons.append("RECEIPT_COVERAGE")
        for key, spec in req.items():
            if c["receipt_revisions"].get(key) != spec["revision"]:
                reasons.append("STALE_RECEIPT")
            if spec["released_at"] > s["cutoff"]: reasons.append("UNRELEASED_TARGET")
            if spec["kind"] == "old" and spec["revision"] != s["epoch_target_revisions"].get(key):
                reasons.append("REQUALIFICATION_REQUIRED")
        if reasons: return answer("DEFER",reasons)
        metrics={"late": public["tick"] > c["deadline"], "by_capability": {}}
        for key,spec in req.items():
            q=target_probability(measurements[key],spec["target"])
            pred=1 if measurements[key]>500 else 0
            entry={"prob_milli":q,"class_correct":pred==spec["target"]}
            if spec["kind"]=="old":
                before=target_probability(s["parent_p1"][key],spec["target"])
                anchor=target_probability(s["anchor_p1"][key],spec["target"])
                entry.update(parent_drop=before-q,epoch_drop=anchor-q)
                if pred != spec["target"]: reasons.append("OLD_CLASS")
                if q<p["min_old"]: reasons.append("OLD_FLOOR")
                if before-q>p["parent_drop"]: reasons.append("PARENT_BUDGET")
                if anchor-q>p["epoch_drop"]: reasons.append("EPOCH_BUDGET")
            else:
                if pred != spec["target"]: reasons.append("FOCAL_CLASS")
                if q<p["min_focal"]: reasons.append("FOCAL_FLOOR")
            metrics["by_capability"][key]=entry
        return answer("DEFER" if reasons else "ADOPT_ELIGIBLE",reasons or ["CONTRACT_SATISFIED"],metrics)
    except (KeyError,TypeError,ValueError,AttributeError):
        return answer("REJECT",["MALFORMED_RECORD"])
