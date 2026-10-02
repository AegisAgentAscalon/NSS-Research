"""Bounded host operator around the supplied Trainer; mathematical updates unchanged."""
from __future__ import annotations
import argparse,contextlib,copy,datetime,fcntl,gc,hashlib,json,lzma,os,resource,shutil,sys,time,traceback
from pathlib import Path
from typing import Any
import numpy as np,psutil,torch
from q010r import run_pilot,training,evaluation as ev,main_execution
from q010r.models import model_state_hash
from q010c.protocol import ROOT,STAGING,ARMS,SEEDS,VERSION,seed_plan,sha,digest

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def exclusive_json(path:Path,obj:Any):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def load_payload(path:Path)->dict:
 # Files are produced here or byte-verified from the authorized handoff; no
 # arbitrary remote pickle is accepted. XZ is archival compression, not quantization.
 opener=lzma.open if path.suffix=='.xz' else open
 with opener(path,'rb') as f:payload=torch.load(f,map_location='cpu',weights_only=False)
 state=payload.get('model_state')
 if not isinstance(state,dict):raise ValueError('checkpoint lacks a model tensor map')
 if training._hash_tensor_map(state)!=payload.get('model_state_sha256'):raise ValueError('strict payload digest mismatch')
 return payload

def create_trainer(seed:int,role:str,protocol_sha:str,*,attempt_role:str='main',run_id:str|None=None):
 arm=dict(ARMS)[role];rng=seed_plan(seed,arm);torch.manual_seed(int(rng['global_torch_seed']))
 tr=run_pilot.make_main_trainer(arm,paired_seed=seed,run_id=run_id or f'q01014-{attempt_role}-s{seed}-{role}',protocol_sha256=protocol_sha,sampler_seed=int(rng['sampler_seed']),training_torch_seed=int(rng['training_torch_seed']),model_init_seed=rng['model_init_seed'])
 return tr,rng

def zero_start_check(protocol_sha:str)->dict:
 """Runtime validation of the actual formerly-unexecuted zero-start correction."""
 rows=[]
 for seed in SEEDS:
  for role,arm in ARMS:
   tr,rng=create_trainer(seed,role,protocol_sha);m=tr.manifest(status='failed');expected=ev._fit_manifest_projection(m);expected['reader_id']=role
   if expected['completed_steps']!=0 or expected['last_joint_checkpoint_step']!=0:raise AssertionError('factory ran updates')
   expected['completed_steps']=6000;expected['last_joint_checkpoint_step']=6000
   rng['rng_start_sha256']=m['rng_start_sha256'];fit=main_execution.MainFit(seed,role,arm,tr.config.run_id,expected,rng)
   receipt=main_execution._check_constructed_trainer(fit,trainer=tr,evaluation=ev)
   strict=training._hash_tensor_map(tr.model.state_dict());public=model_state_hash(tr.model)
   main_execution._strict_tensor_fingerprints(tr.model.state_dict(),payload_tensor_sha256=strict,receipt_tensor_sha256=strict,public_model_value_sha256=public,evaluation=ev,training=training,torch=torch)
   try:main_execution._strict_tensor_fingerprints(tr.model.state_dict(),payload_tensor_sha256=public,receipt_tensor_sha256=public,public_model_value_sha256=public,evaluation=ev,training=training,torch=torch)
   except main_execution.MainExecutionError:pass
   else:raise AssertionError('public hash incorrectly accepted as strict hash')
   saved=tr.optimizer_step;tr.optimizer_step=1
   try:main_execution._check_constructed_trainer(fit,trainer=tr,evaluation=ev)
   except RuntimeError:pass
   else:raise AssertionError('nonzero fake cursor accepted')
   finally:tr.optimizer_step=saved
   rows.append({'seed':seed,'reader':role,'actual_updates':tr.optimizer_step,'stream_cursor':tr.stream.next_batch_index,'runtime_zero_start_check':'PASS','negative_cursor_test':'PASS','strict_public_separation':'PASS','expectation':expected,'rng':rng,'receipt':receipt});del tr;gc.collect()
 return {'status':'PASS','scope':'15 real zero-update main trainer constructions; original checker, real parent weights and RNG; no optimizer steps','rows':rows,'utc':utc()}


from q010c import execution_io as io


def _validate_execution_contract(protocol_path, lock_path, protocol_pin, lock_pin):
    if not protocol_pin or not lock_pin:
        raise io.BindingError("explicit protocol and source-lock digests are required")
    if sha(protocol_path) != protocol_pin or sha(lock_path) != lock_pin:
        raise io.BindingError("protocol/source-lock byte identity mismatch")
    proto, lock = io.read_json(protocol_path), io.read_json(lock_path)
    if proto.get("status") != "FROZEN_FOR_CONFIRMATORY_EXECUTION":
        raise io.BindingError("a draft or source-repair package is not a main-run authorization")
    if (proto.get("main_steps_per_fit") != 6000 or proto.get("main_fit_count") != 15
            or proto.get("main_seeds") != list(SEEDS) or proto.get("arms") != dict(ARMS)):
        raise io.BindingError("the complete three-arm/five-seed/6000-step scope is required")
    if lock.get("protocol_sha256") != protocol_pin or not isinstance(lock.get("files"), dict):
        raise io.BindingError("source lock is not bound to the frozen protocol")
    required = set()
    # Exact runtime/parent dependency closure, excluding generated Python cache.
    bases = [ROOT / "tools", ROOT / "source/q010c", ROOT / "source/q010v",
             STAGING / "implementation_A/q010r", STAGING / "implementation_A/reference",
             STAGING / "verification_B"]
    for base in bases:
        for path in base.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix in (
                    ".py", ".pt", ".npz", ".safetensors", ".json"):
                required.add(path.relative_to(ROOT).as_posix())
    required.add((STAGING / "plan/main_data_recipe.md").relative_to(ROOT).as_posix())
    required.add((STAGING / "plan/condition_matrix.json").relative_to(ROOT).as_posix())
    if not required.issubset(lock["files"]):
        raise io.BindingError("incomplete source/start/recipe lock")
    def verify():
        if sha(protocol_path) != protocol_pin or sha(lock_path) != lock_pin:
            raise io.BindingError("frozen execution document drift")
        for rel, expected in lock["files"].items():
            path = io.contained(ROOT, rel)
            if not path.is_file() or sha(path) != expected:
                raise io.BindingError("locked input drift: " + rel)
    verify()
    if proto.get("runtime_identity") != training.runtime_identity():
        raise io.BindingError("runtime differs from the explicit frozen execution identity")
    resources = proto.get("resources", {})
    for key in ("per_fit_wall_hard_seconds", "maximum_worker_rss_bytes",
                "minimum_free_disk_bytes", "maximum_new_output_bytes",
                "checkpoint_every_updates", "resource_sample_every_updates"):
        value = resources.get(key)
        if isinstance(value, bool) or not isinstance(value, (float, int)) or value <= 0:
            raise io.BindingError("missing/invalid frozen resource field: " + key)
    for key in ("checkpoint_every_updates", "resource_sample_every_updates"):
        if type(resources[key]) is not int or not 1 <= resources[key] <= 6000:
            raise io.BindingError("update intervals must be integer counts in 1..6000")
    starts = lock.get("expected_starts", {})
    if set(starts) != {f"{seed}:{role}" for seed in SEEDS for role, _ in ARMS}:
        raise io.BindingError("pre-main lock lacks all fifteen zero-start identities")
    # Initial RNG identity includes the protocol hash through the stream state.
    # Store these identities in the later lock, not inside their own protocol.
    return proto, verify, starts


def committed_checkpoints(output, binding):
    records = []
    for marker in sorted((output / "commits").glob("step*.json")):
        rec = io.read_json(marker)
        if (rec.get("kind") != "joint_training_checkpoint" or
                rec.get("binding_sha256") != binding or
                marker.name != f"step{rec.get('step', -1):06d}.json"):
            raise io.BindingError("checkpoint commit binding mismatch")
        io.verify_file(output, rec["checkpoint"])
        io.verify_file(output, rec["fit_manifest"])
        records.append(rec)
    if records and (records[0]["step"] != 0 or any(
            b["step"] <= a["step"] for a, b in zip(records, records[1:]))):
        raise io.BindingError("invalid committed checkpoint sequence")
    return records


def verify_completed_fit(output, *, binding=None):
    """Verify final publication without rerunning or silently replacing it."""
    rec = io.read_json(output / "COMPLETE.json")
    if (rec.get("schema") != "q010-fit-completion-v1.4" or rec.get("updates") != 6000
            or (binding is not None and rec.get("binding_sha256") != binding)):
        raise io.BindingError("invalid complete-fit receipt")
    root = io.contained(output, rec["publication"])
    io.verify_tree(root, rec["files"])
    commit = io.read_json(io.verify_file(output, rec["final_commit"]))
    if commit["step"] != 6000 or commit["binding_sha256"] != rec["binding_sha256"]:
        raise io.BindingError("completion is not linked to its final committed state")
    io.verify_file(output, commit["checkpoint"])
    io.verify_file(output, commit["fit_manifest"])
    if (io.sha(root / "checkpoint_step_006000.pt") != commit["checkpoint"]["sha256"]
            or io.sha(root / "fit_manifest.json") != commit["fit_manifest"]["sha256"]
            or rec.get("final_strict_sha256") != commit.get("strict_sha256")
            or rec.get("final_public_sha256") != commit.get("public_sha256")
            or rec["binding_sha256"] != io.digest(io.read_json(output / "FIT_CONFIG.json"))):
        raise io.BindingError("final publication is not the committed checkpoint/configuration")
    return rec


def fit(seed:int, role:str, output:Path, *, attempt_role:str="main",
        protocol_path:Path|None=None, source_lock_path:Path|None=None,
        protocol_sha256:str|None=None, source_lock_sha256:str|None=None,
        max_new_updates:int=250, invocation_soft_seconds:float=120.0,
        run_root:Path|None=None, resume_review:Path|None=None, resume_review_sha256:str|None=None) -> dict:
    """One bounded invocation of a fixed 6000-update fit.

    A pause changes execution granularity, never the planned number of updates.
    New invocations retain prior attempts and restore a verified joint checkpoint.
    Unknown crash-duration accounting requires explicit review, not silent restart.
    No automatic archive compression or deletion of checkpoints occurs here.
    """
    if seed not in SEEDS or role not in dict(ARMS) or attempt_role not in ("main", "reproduction"):
        raise io.BindingError("unknown declared fit")
    if type(max_new_updates) is not int or not 1 <= max_new_updates <= 6000:
        raise ValueError("max_new_updates must be 1..6000")
    if not 0 < invocation_soft_seconds <= 1800:
        raise ValueError("invocation soft bound must be 0..1800 seconds")
    output = Path(output).resolve()
    run_root = Path(run_root).resolve() if run_root else output.parent.parent
    if run_root not in output.parents or ROOT.resolve() == run_root or ROOT.resolve() in run_root.parents:
        raise io.BindingError("output must belong to a separate run tree outside the source package")
    protocol_path = Path(protocol_path or ROOT / "protocol/FROZEN_PROTOCOL.json").resolve()
    source_lock_path = Path(source_lock_path or ROOT / "protocol/TRAINING_SOURCE_LOCK.json").resolve()
    proto, verify_sources, expected_starts = _validate_execution_contract(
        protocol_path, source_lock_path, protocol_sha256, source_lock_sha256)
    resources = proto["resources"]
    config = {"schema": "q010-fit-execution-v1.4", "role": role, "arm": dict(ARMS)[role],
              "seed": seed, "attempt_role": attempt_role,
              "run_id": f"q01014-{attempt_role}-s{seed}-{role}",
              "protocol_sha256": protocol_sha256, "source_lock_sha256": source_lock_sha256,
              "planned_updates": 6000, "rng": seed_plan(seed, dict(ARMS)[role])}
    binding = io.digest(config)
    # One scarce-resource operator for the entire supplied run root, not per fit.
    with io.lease(run_root / "OPERATOR.lock"):
        if (output / "COMPLETE.json").exists():
            return verify_completed_fit(output, binding=binding)
        output.mkdir(parents=True, exist_ok=True)
        config_path = output / "FIT_CONFIG.json"
        if config_path.exists():
            if io.read_json(config_path) != config:
                raise io.BindingError("resume configuration changed")
        else:
            if any(output.iterdir()):
                raise io.BindingError("unrecognized nonempty fit destination")
            io.publish_json(config_path, config)
        previous_seconds = io.prior_attempt_cost(output, "attempts", binding,
                review_path=resume_review, review_sha256=resume_review_sha256)
        commits = committed_checkpoints(output, binding)
        attempt = io.new_attempt(output)
        if resume_review is not None:
            # Retain the exact accepted review; do not mutate the failed attempt.
            if io.sha(resume_review) != resume_review_sha256:
                raise io.BindingError("resume review changed before invocation")
            shutil.copy2(resume_review, attempt / "RESUME_REVIEW.json")
        start = time.monotonic()
        tr = None
        last = commits[-1] if commits else None
        disposition = "FAILED_OR_PARTIAL"
        stop_reason = None
        samples = []
        io.publish_json(attempt / "START.json", {"utc": utc(), "pid": os.getpid(),
            "binding_sha256": binding, "previous_accounted_seconds": previous_seconds,
            "resume_review_sha256": resume_review_sha256,
            "resumed_step": None if last is None else last["step"],
            "invocation_max_new_updates": max_new_updates, "soft_seconds": invocation_soft_seconds})
        def event(kind, **data):
            row = {"event": kind, "utc": utc(), "pid": os.getpid(),
                   "seed": seed, "role": role, **data}
            with (attempt / "events.jsonl").open("a", encoding="utf-8") as log:
                log.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
                log.flush(); os.fsync(log.fileno())
            print(json.dumps(row, sort_keys=True, allow_nan=False), flush=True)
        def sample(step):
            used = sum(p.stat().st_size for p in run_root.rglob("*") if p.is_file())
            r = {"utc": utc(), "step": step, "rss_bytes": psutil.Process().memory_info().rss,
                 "elapsed_seconds": time.monotonic() - start,
                 "free_disk_bytes": shutil.disk_usage(run_root).free, "run_tree_bytes": used}
            samples.append(r)
            with (attempt / "resources.jsonl").open("a") as log:
                log.write(json.dumps(r, sort_keys=True) + "\n"); log.flush()
            if r["rss_bytes"] > resources["maximum_worker_rss_bytes"]:
                raise RuntimeError("worker memory ceiling")
            if previous_seconds + r["elapsed_seconds"] > resources["per_fit_wall_hard_seconds"]:
                raise RuntimeError("cumulative measured fit wall ceiling")
            if r["free_disk_bytes"] < resources["minimum_free_disk_bytes"]:
                raise RuntimeError("free disk floor")
            if r["run_tree_bytes"] > resources["maximum_new_output_bytes"]:
                raise RuntimeError("complete run-tree storage ceiling")
            return r
        def checkpoint():
            nonlocal last
            verify_sources()
            step = int(tr.optimizer_step)
            if last is not None and last["step"] == step:
                return last
            if tr.recovery_required or tr.stream.next_batch_index != step or len(tr.trace) != step:
                raise io.BindingError("checkpoint requested from non-joint training state")
            cp = attempt / f"checkpoint_{step:06d}.pt"
            raw = tr.save_checkpoint(cp)
            io.fsync_directory(cp.parent)
            payload = load_payload(cp)
            strict = training._hash_tensor_map(payload["model_state"])
            public = model_state_hash(tr.model)
            if payload["optimizer_step"] != step or payload["identity"] != tr.identity:
                raise io.BindingError("checkpoint reload identity/cursor mismatch")
            main_execution._strict_tensor_fingerprints(tr.model.state_dict(),
                payload_tensor_sha256=strict, receipt_tensor_sha256=raw["model_state_sha256"],
                public_model_value_sha256=public, evaluation=ev, training=training, torch=torch)
            manifest = attempt / f"manifest_{step:06d}.json"
            io.publish_json(manifest, tr.manifest(status="complete" if step == 6000 else "stopped", final_checkpoint=raw))
            rec = {"kind": "joint_training_checkpoint", "binding_sha256": binding, "step": step,
                   "checkpoint": io.file_info(output, cp), "fit_manifest": io.file_info(output, manifest),
                   "strict_sha256": strict, "public_sha256": public,
                   "rng_sha256": payload["rng_state_sha256"], "utc": utc()}
            io.publish_json(output / "commits" / f"step{step:06d}.json", rec)
            last = rec
            event("CHECKPOINT_COMMITTED", step=step, raw_bytes=raw["bytes"])
            return rec
        try:
            sample(0 if last is None else last["step"])
            tr, rng = create_trainer(seed, role, protocol_sha256,
                                    attempt_role=attempt_role, run_id=config["run_id"])
            expected_start = expected_starts.get(f"{seed}:{role}")
            actual_start = {"public_sha256": model_state_hash(tr.model),
                            "strict_sha256": training._hash_tensor_map(tr.model.state_dict()),
                            "rng_start_sha256": tr.manifest(status="failed")["rng_start_sha256"],
                            "sampler_seed": int(rng["sampler_seed"]),
                            "training_torch_seed": int(rng["training_torch_seed"]),
                            "model_init_seed": rng["model_init_seed"],
                            "global_torch_seed": int(rng["global_torch_seed"])}
            if actual_start != expected_start or tr.optimizer_step != 0 or tr.stream.next_batch_index != 0:
                raise io.BindingError("zero-start state differs from the frozen per-fit preflight")
            event("TRAINER_CONSTRUCTED", step=0)
            if last is not None:
                cp = io.verify_file(output, last["checkpoint"])
                # Existing Trainer stages every field, then atomically restores or rolls back.
                tr.restore_checkpoint(cp)
                if (tr.optimizer_step != last["step"] or model_state_hash(tr.model) != last["public_sha256"]
                        or training._hash_tensor_map(tr.model.state_dict()) != last["strict_sha256"]):
                    raise io.BindingError("restored training cursor or weights differ")
                event("CHECKPOINT_RESTORED", step=tr.optimizer_step)
            else:
                checkpoint()  # A real zero-step joint checkpoint before any update.
            begin = int(tr.optimizer_step)
            target = min(6000, begin + max_new_updates)
            with (attempt / "trace.jsonl").open("x") as trace:
                while tr.optimizer_step < target:
                    if time.monotonic() - start >= invocation_soft_seconds:
                        stop_reason = "INVOCATION_SOFT_BOUND"
                        break
                    row = tr.train_step()
                    trace.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
                    step = int(tr.optimizer_step)
                    if step % int(resources["resource_sample_every_updates"]) == 0:
                        trace.flush(); verify_sources(); sample(step)
                        event("PROGRESS", step=step, loss=row["loss"])
                    if step % int(resources["checkpoint_every_updates"]) == 0:
                        trace.flush(); os.fsync(trace.fileno()); checkpoint()
                trace.flush(); os.fsync(trace.fileno())
            checkpoint()
            sample(tr.optimizer_step)
            if tr.optimizer_step < 6000:
                disposition = "PAUSED_CHECKPOINTED"
                stop_reason = stop_reason or "INVOCATION_UPDATE_BOUND"
                event(disposition, step=tr.optimizer_step, reason=stop_reason)
                return {"status": disposition, "step": tr.optimizer_step, "binding_sha256": binding}
            # Stage publication; an interrupted attempt leaves its evidence intact.
            publication = io.new_attempt(output, "publications")
            source_manifest = io.verify_file(output, last["fit_manifest"])
            shutil.copy2(source_manifest, publication / "fit_manifest.json")
            cp_source = io.verify_file(output, last["checkpoint"])
            os.link(cp_source, publication / "checkpoint_step_006000.pt")
            arrays = {key: np.asarray([row[key] for row in tr.trace]) for key in (
                "optimizer_step", "loss", "gradient_norm_before_clip", "row_loss_by_stage",
                "code_loss_by_stage", "learning_rate", "input_rng_state_sha256",
                "output_rng_state_sha256", "training_data_sha256", "public_input_sha256_by_stage")}
            with (publication / "numeric_trace.npz").open("xb") as stream:
                np.savez_compressed(stream, **arrays); stream.flush(); os.fsync(stream.fileno())
            with (publication / "fit_manifest.json").open("rb") as stream:
                os.fsync(stream.fileno())
            io.fsync_directory(publication)
            verify_sources()
            result = {"schema": "q010-fit-completion-v1.4", "status": "COMPLETE_FIT_NOT_QUALIFICATION",
                      "seed": seed, "role": role, "attempt_role": attempt_role,
                      "binding_sha256": binding, "protocol_sha256": protocol_sha256,
                      "source_lock_sha256": source_lock_sha256, "updates": 6000,
                      "publication": publication.relative_to(output).as_posix(),
                      "files": io.tree_inventory(publication),
                      "final_commit": io.file_info(output, output / "commits/step006000.json"),
                      "elapsed_accounted_seconds": previous_seconds + time.monotonic() - start,
                      "final_strict_sha256": last["strict_sha256"],
                      "final_public_sha256": last["public_sha256"], "utc": utc()}
            io.publish_json(output / "COMPLETE.json", result)
            disposition = "COMPLETE_FIT_NOT_QUALIFICATION"
            event(disposition, step=6000)
            return result
        except BaseException as exc:
            io.report_failure(attempt, exc, binding_sha256=binding,
                              last_committed_step=None if last is None else last["step"],
                              observed_optimizer_step=None if tr is None else tr.optimizer_step)
            raise
        finally:
            # Do not call trainer.manifest here: source drift must not suppress failure evidence.
            try:
                io.publish_json(attempt / "END.json", {"utc": utc(), "pid": os.getpid(),
                    "binding_sha256": binding, "disposition": disposition,
                    "elapsed_seconds": time.monotonic() - start,
                    "last_committed_step": None if last is None else last["step"],
                    "stop_reason": stop_reason})
            except BaseException as end_error:
                print(json.dumps({"end_receipt_failure": repr(end_error)}), file=sys.stderr, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--role", choices=[r for r, _ in ARMS], required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--run-root", type=Path, required=True)
    p.add_argument("--attempt-role", choices=["main", "reproduction"], default="main")
    p.add_argument("--protocol", type=Path, required=True)
    p.add_argument("--source-lock", type=Path, required=True)
    p.add_argument("--protocol-sha256", required=True)
    p.add_argument("--source-lock-sha256", required=True)
    p.add_argument("--resume-review", type=Path)
    p.add_argument("--resume-review-sha256")
    p.add_argument("--max-new-updates", type=int, default=250)
    p.add_argument("--soft-seconds", type=float, default=120.0)
    a = p.parse_args()
    torch.set_num_threads(1); torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    result = fit(a.seed, a.role, a.output, attempt_role=a.attempt_role,
        protocol_path=a.protocol, source_lock_path=a.source_lock,
        protocol_sha256=a.protocol_sha256, source_lock_sha256=a.source_lock_sha256,
        max_new_updates=a.max_new_updates, invocation_soft_seconds=a.soft_seconds, run_root=a.run_root,
        resume_review=a.resume_review, resume_review_sha256=a.resume_review_sha256)
    raise SystemExit(75 if result.get("status") == "PAUSED_CHECKPOINTED" else 0)
