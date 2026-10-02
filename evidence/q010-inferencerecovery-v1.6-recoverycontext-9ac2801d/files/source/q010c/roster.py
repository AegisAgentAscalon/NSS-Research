"""Bind completed fits only after training; never rewrite the pre-main lock."""
from __future__ import annotations
from pathlib import Path
from q010c import execution_io as io
from q010c.protocol import SEEDS, ARMS

ROSTER_SCHEMA = "q010-checkpoint-roster-v1.4"


def read_roster(root, pinned_sha256):
    root = Path(root).resolve()
    path = root / "CHECKPOINT_ROSTER_LOCK.json"
    if not pinned_sha256 or io.sha(path) != pinned_sha256:
        raise io.BindingError("explicit checkpoint-roster pin does not match")
    roster = io.read_json(path)
    if roster.get("schema") != ROSTER_SCHEMA:
        raise io.BindingError("unsupported checkpoint roster")
    rows = roster.get("fits", [])
    expected = {(s, r) for s in SEEDS for r, _ in ARMS}
    actual = [(row.get("seed"), row.get("role")) for row in rows]
    if len(actual) != 15 or len(set(actual)) != 15 or set(actual) != expected:
        raise io.BindingError("roster is not exactly the fifteen declared fits")
    for row in rows:
        io.verify_file(root, row["completion"])
    return roster


def publish_roster(root, *, protocol_sha256, source_lock_sha256):
    from q010c.train import verify_completed_fit
    root = Path(root).resolve()
    with io.lease(root / "OPERATOR.lock"):
        rows = []
        for seed in SEEDS:
            for role, arm in ARMS:
                fit = root / f"seed{seed}" / role
                complete = verify_completed_fit(fit)
                config = io.read_json(fit / "FIT_CONFIG.json")
                if (complete.get("seed") != seed or complete.get("role") != role
                        or complete.get("attempt_role") != "main"
                        or complete.get("protocol_sha256") != protocol_sha256
                        or complete.get("source_lock_sha256") != source_lock_sha256
                        or complete.get("binding_sha256") != io.digest(config)
                        or config.get("arm") != arm or config.get("seed") != seed
                        or config.get("role") != role or config.get("planned_updates") != 6000):
                    raise io.BindingError("fit does not belong to this frozen main study")
                rows.append({"seed": seed, "role": role, "arm": arm,
                             "completion": io.file_info(root, fit / "COMPLETE.json"),
                             "fit_config": io.file_info(root, fit / "FIT_CONFIG.json"),
                             "strict_sha256": complete["final_strict_sha256"],
                             "public_sha256": complete["final_public_sha256"]})
        value = {"schema": ROSTER_SCHEMA, "utc": io.utc(),
                 "protocol_sha256": protocol_sha256, "source_lock_sha256": source_lock_sha256,
                 "fits": rows, "scope": "ALL15_FINAL_MAIN_FITS_NOT_EVALUATION_QUALIFICATION"}
        io.publish_json(root / "CHECKPOINT_ROSTER_LOCK.json", value)
        return value


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fits", type=Path, required=True)
    parser.add_argument("--protocol-sha256", required=True)
    parser.add_argument("--source-lock-sha256", required=True)
    args = parser.parse_args()
    publish_roster(args.fits, protocol_sha256=args.protocol_sha256,
                   source_lock_sha256=args.source_lock_sha256)
