"""Bounded condition-group coordinator; source repair, runtime validation pending.

Uses the inherited evaluator unchanged inside each group. An incomplete group is
retained and recomputed, not resumed mid-operation. No training is performed.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import shutil
import time
import sys

from q010c import execution_io as io
from q010c.protocol import ROOT, SEEDS


def checked_group(out, record, group, wanted, binding):
    if (record.get("group") != group or record.get("conditions") != wanted
            or record.get("binding_sha256") != binding):
        raise io.BindingError("condition-group binding mismatch")
    root = io.contained(out, record["directory"])
    io.verify_tree(root, record["files"])
    cap = io.read_json(root / "CAPTURE.json")
    if set(row["condition"] for row in cap["chunks"]) != set(wanted):
        raise io.BindingError("captured group is missing or adds a condition")
    if cap["weights_before"] != cap["weights_after"]:
        raise io.BindingError("evaluation changed learned parameters")
    return root, cap


def checked_complete(out, binding):
    result = io.read_json(out / "COMPLETE.json")
    if (result.get("schema") != "q010-capture-publication-v1.4"
            or result.get("binding_sha256") != binding or result.get("groups") != 8):
        raise io.BindingError("capture completion binding mismatch")
    for commit in result["commits"]:
        io.verify_file(out, commit)
    view = io.contained(out, result["publication"])
    io.verify_tree(view, result["files"])
    return result


def publish_view(out, groups, records, binding, mode, resource_check, verify_source):
    """A new publication attempt never overwrites a partly published view."""
    view = io.new_attempt(out, "publications")
    combined = None
    chunks = []
    seconds = 0.0
    peak = 0
    sums = {key: 0 for key in ("chains", "logical_stage_evaluations", "actual_noise_events",
                                "maintenance_sweeps", "qualified_unrelated_writes")}
    for index, record in enumerate(records):
        resource_check()
        root, cap = checked_group(out, record, index, groups[index], binding)
        if combined is None:
            combined = dict(cap)
        elif (cap["weights_before"] != combined["weights_before"]
              or cap["weights_after"] != combined["weights_after"]):
            raise io.BindingError("different readers across groups")
        for cid in groups[index]:
            shutil.copytree(io.contained(root, cid), view / cid)
        chunks.extend(cap["chunks"])
        seconds += cap["seconds"]
        peak = max(peak, cap["peak_rss_bytes"])
        for key in sums:
            sums[key] += cap[key]
    if combined is None:
        raise io.BindingError("cannot publish an empty capture")
    combined.update(sums, cells=64, chunks=chunks, seconds=seconds,
                    peak_rss_bytes=peak, utc=io.utc())
    first = io.contained(out, records[0]["directory"])
    header = io.read_json(first / "START.json")
    header.update(selected_cells=None, scope="FULL_MATRIX" if mode == "main" else "DEVELOPMENT_SUBSET")
    io.publish_json(view / "START.json", header)
    io.publish_json(view / "CAPTURE.json", combined)
    # Make copied numerical data durable before publishing a completion marker.
    for path in view.rglob("*"):
        if path.is_file():
            with path.open("rb") as stream:
                os.fsync(stream.fileno())
    for directory in sorted((p for p in view.rglob("*") if p.is_dir()),
                            key=lambda p: len(p.parts), reverse=True):
        io.fsync_directory(directory)
    io.fsync_directory(view)
    verify_source()
    resource_check()
    result = {"schema": "q010-capture-publication-v1.4", "utc": io.utc(),
              "binding_sha256": binding, "groups": 8, "mode": mode,
              "publication": view.relative_to(out).as_posix(), "files": io.tree_inventory(view),
              "commits": [io.file_info(out, out / "commits" / f"group{i:02d}.json") for i in range(8)],
              "status": "CAPTURE_COMPLETE_INDEPENDENT_SCORING_REQUIRED", "optimizer_updates": 0}
    io.publish_json(out / "COMPLETE.json", result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["development", "main"], required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--fits", type=Path)
    parser.add_argument("--roster-sha256")
    parser.add_argument("--protocol", type=Path)
    parser.add_argument("--source-lock", type=Path)
    parser.add_argument("--protocol-sha256")
    parser.add_argument("--source-lock-sha256")
    parser.add_argument("--resume-review", type=Path)
    parser.add_argument("--resume-review-sha256")
    parser.add_argument("--max-new-groups", type=int, default=1)
    parser.add_argument("--soft-seconds", type=float, default=120.0)
    args = parser.parse_args(argv)
    if not 1 <= args.max_new_groups <= 8 or not 0 < args.soft_seconds <= 1800:
        raise ValueError("invalid bounded invocation limits")
    out, run_root = args.out.resolve(), args.run_root.resolve()
    if run_root not in out.parents or ROOT.resolve() in run_root.parents or ROOT.resolve() == run_root:
        raise io.BindingError("output must be in a separate run tree")
    import torch
    import psutil
    from q010c.evaluate import capture_seed, load_readers
    from q010r.conditions import condition_cells
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    if args.mode == "main":
        if args.seed not in SEEDS or args.fits is None or not args.roster_sha256:
            raise io.BindingError("main capture requires its seed and explicit final roster")
        if None in (args.protocol, args.source_lock, args.protocol_sha256, args.source_lock_sha256):
            raise io.BindingError("main capture requires pinned protocol and source lock")
        from q010c.train import _validate_execution_contract
        from q010c.roster import read_roster
        proto, verify_source, _starts = _validate_execution_contract(args.protocol, args.source_lock,
                args.protocol_sha256, args.source_lock_sha256)
        roster = read_roster(args.fits, args.roster_sha256)
        if (roster["protocol_sha256"] != args.protocol_sha256
                or roster["source_lock_sha256"] != args.source_lock_sha256):
            raise io.BindingError("final roster and frozen experiment do not agree")
        resources = dict(proto["resources"])
        hard_wall = resources.get("evaluation_seed_wall_hard_seconds")
        if isinstance(hard_wall, bool) or not isinstance(hard_wall, (int, float)) or hard_wall <= 0:
            raise io.BindingError("missing frozen per-seed evaluation wall limit")
        seed, split, count = args.seed, "heldout", None
    else:
        if args.seed is not None or args.fits is not None or args.roster_sha256:
            raise io.BindingError("development input identities are fixed, not main inputs")
        proto = None
        seed, split, count = 91401, "development", 4
        resources = {"maximum_worker_rss_bytes": 1073741824,
                     "minimum_free_disk_bytes": 2147483648,
                     "maximum_new_output_bytes": 2147483648}
        hard_wall = 1800
        # The bootstrap checks this entire immutable workspace before code import.
        manifest_path = ROOT / "MANIFEST.json"
        original_manifest_hash = io.sha(manifest_path)
        closure = io.read_json(manifest_path)["files"]
        def verify_source():
            if io.sha(manifest_path) != original_manifest_hash:
                raise io.BindingError("workspace manifest drift")
            for rel, expected in closure.items():
                io.verify_file(ROOT, {"path": rel, **expected})
        verify_source()
    ids = [cell.condition_id for cell in condition_cells()]
    if len(ids) != 64 or len(set(ids)) != 64:
        raise io.BindingError("expected exactly the declared 64 condition types")
    groups = [ids[i:i+8] for i in range(0, 64, 8)]
    with io.lease(run_root / "OPERATOR.lock"):
        if args.mode == "main":
            models, identities = load_readers(seed, args.fits, roster_sha256=args.roster_sha256)
        else:
            from q010c.development import development_readers
            models, identities = development_readers()
        from q010r.training import runtime_identity
        config = {"schema": "q010-group-execution-v1.4", "mode": args.mode,
                  "seed": seed, "split": split, "development_count": count,
                  "groups": groups, "readers": io.portable_paths(identities,
                         {"PACKAGE": ROOT, "FITS": args.fits} if args.fits else {"PACKAGE": ROOT}),
                  "runtime": runtime_identity(), "source_manifest_sha256": io.sha(ROOT / "MANIFEST.json"),
                  "wrapper_sha256": io.sha(Path(__file__)), "protocol_sha256": args.protocol_sha256,
                  "source_lock_sha256": args.source_lock_sha256, "roster_sha256": args.roster_sha256,
                  "resources": resources, "evaluation_seed_wall_hard_seconds": hard_wall,
                  "optimizer_updates": 0}
        binding = io.digest(config)
        if (out / "COMPLETE.json").exists():
            return checked_complete(out, binding)
        out.mkdir(parents=True, exist_ok=True)
        if (out / "CONFIG.json").exists():
            if io.read_json(out / "CONFIG.json") != config:
                raise io.BindingError("resume changes runtime/source/weights/condition identity")
        else:
            if any(out.iterdir()):
                raise io.BindingError("unrecognized nonempty destination")
            io.publish_json(out / "CONFIG.json", config)
        prior_seconds = io.prior_attempt_cost(out, "invocations", binding,
                review_path=args.resume_review, review_sha256=args.resume_review_sha256)
        invocation = io.new_attempt(out, "invocations")
        if args.resume_review is not None:
            if io.sha(args.resume_review) != args.resume_review_sha256:
                raise io.BindingError("resume review changed before invocation")
            shutil.copy2(args.resume_review, invocation / "RESUME_REVIEW.json")
        start = time.monotonic()
        status = "FAILED_OR_PARTIAL"
        io.publish_json(invocation / "START.json", {"pid": os.getpid(), "utc": io.utc(),
                "binding_sha256": binding, "prior_seconds": prior_seconds,
                "resume_review_sha256": args.resume_review_sha256})
        def resource_check():
            row = {"elapsed_seconds": prior_seconds + time.monotonic() - start,
                   "rss_bytes": psutil.Process().memory_info().rss,
                   "free_bytes": shutil.disk_usage(run_root).free,
                   "output_bytes": sum(p.stat().st_size for p in run_root.rglob("*") if p.is_file())}
            with (invocation / "resources.jsonl").open("a") as f:
                import json
                f.write(json.dumps(row, sort_keys=True) + "\n"); f.flush()
            if (row["elapsed_seconds"] > hard_wall
                    or row["rss_bytes"] > resources["maximum_worker_rss_bytes"]
                    or row["free_bytes"] < resources["minimum_free_disk_bytes"]
                    or row["output_bytes"] > resources["maximum_new_output_bytes"]):
                raise RuntimeError("observed capture resource ceiling reached")
        try:
            records = []
            produced = 0
            for index, wanted in enumerate(groups):
                marker = out / "commits" / f"group{index:02d}.json"
                if marker.exists():
                    rec = io.read_json(marker)
                    checked_group(out, rec, index, wanted, binding)
                    records.append(rec)
                    continue
                if produced and (produced >= args.max_new_groups or time.monotonic()-start >= args.soft_seconds):
                    status = "PAUSED_CHECKPOINTED"
                    return {"status": status, "groups_committed": len(records), "optimizer_updates": 0}
                verify_source(); resource_check()
                attempt = io.new_attempt(out, f"groups/g{index:02d}")
                # capture_seed requires its destination not to exist.
                target = attempt / "capture"
                capture_seed(seed, models, identities, target, split=split,
                             selected_cells=wanted, development_count=count)
                verify_source(); resource_check()
                rec = {"group": index, "conditions": wanted, "binding_sha256": binding,
                       "directory": target.relative_to(out).as_posix(),
                       "files": io.tree_inventory(target), "utc": io.utc()}
                checked_group(out, rec, index, wanted, binding)
                io.publish_json(marker, rec)
                records.append(rec); produced += 1
                print(f"COMMITTED group {index + 1}/8; seed={seed}; mode={args.mode}", flush=True)
            result = publish_view(out, groups, records, binding, args.mode, resource_check, verify_source)
            status = "CAPTURE_COMPLETE_INDEPENDENT_SCORING_REQUIRED"
            return result
        except BaseException as exc:
            io.report_failure(invocation, exc, binding_sha256=binding)
            raise
        finally:
            try:
                io.publish_json(invocation / "END.json", {"utc": io.utc(), "status": status,
                        "binding_sha256": binding, "elapsed_seconds": time.monotonic() - start})
            except BaseException as exc:
                print("Unable to close invocation receipt: " + repr(exc), file=sys.stderr, flush=True)


if __name__ == "__main__":
    result = main()
    print(result, flush=True)
    raise SystemExit(75 if result.get("status") == "PAUSED_CHECKPOINTED" else 0)
