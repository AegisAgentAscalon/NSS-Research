"""Verify a prepared workspace before importing its numerical implementation.

No implicit training. A command and its required frozen identities are explicit.
Use --help for the required paths; validation itself uses only the standard library.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import runpy
import sys


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(path):
    def unique(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError("duplicate JSON key: " + k)
            out[k] = v
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", type=Path, required=True)
    p.add_argument("--manifest-sha256", required=True)
    p.add_argument("command", choices=["fit", "roster", "capture", "status"])
    args, forwarded = p.parse_known_args()
    root = args.workspace.resolve()
    manifest = root / "MANIFEST.json"
    if sha(manifest) != args.manifest_sha256:
        raise ValueError("workspace manifest does not match the explicitly supplied pin")
    entries = read(manifest)["files"]
    for rel, info in entries.items():
        rp = PurePosixPath(rel)
        if rp.is_absolute() or ".." in rp.parts or "\\" in rel or ":" in rel:
            raise ValueError("unsafe workspace member")
        path = root
        for part in rp.parts:
            path = path / part
            if path.is_symlink():
                raise ValueError("symlink in preserved workspace")
        if not path.is_file() or path.stat().st_size != info["bytes"] or sha(path) != info["sha256"]:
            raise ValueError("workspace source/dependency drift: " + rel)
    own = Path(__file__).resolve()
    if own != root / "tools/q010.py" or "tools/q010.py" not in entries:
        raise ValueError("launch the entry point belonging to this verified workspace")
    if args.command == "status":
        sp = argparse.ArgumentParser()
        sp.add_argument("--run-root", type=Path, required=True)
        q = sp.parse_args(forwarded)
        runs = q.run_root.resolve()
        rows = []
        for seed in range(1201, 1206):
            for arm in ("ordinary", "near", "attention"):
                fit = runs / f"seed{seed}" / arm
                marker = fit / "COMPLETE.json"
                commits = sorted((fit / "commits").glob("step*.json"))
                rows.append({"seed": seed, "role": arm,
                    "completion_receipt_present": marker.is_file(),
                    "latest_claimed_step": read(commits[-1]).get("step") if commits else None})
        print(json.dumps({"scope": "READ_ONLY_RECEIPT_INVENTORY_NOT_PROCESS_OR_MODEL_VERIFICATION",
                          "fits": rows}, indent=2))
        return
    sys.dont_write_bytecode = True
    os.environ.update(OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                      PYTHONDONTWRITEBYTECODE="1")
    staging = root / "workspace/.research_work/NSS_NBR01_Qualification010_Reconstruction_v1.0"
    sys.path[:0] = list(map(str, (root / "source", staging / "implementation_A", staging / "verification_B")))
    module = {"fit": "q010c.train", "roster": "q010c.roster", "capture": "q010c.capture_runner"}[args.command]
    sys.argv = [module, *forwarded]
    runpy.run_module(module, run_name="__main__")


if __name__ == "__main__":
    main()
