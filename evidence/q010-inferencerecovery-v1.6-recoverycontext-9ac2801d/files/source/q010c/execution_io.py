"""Artifact and lease helpers for source-repair v1.4.

Standard-library only. No model import, training, or evaluation on import.
Linux local-filesystem execution is the initial supported operator scope.
Untrusted/mutable paths must not be used as checkpoint inputs.
"""
from __future__ import annotations

import contextlib
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import socket
import sys
import tempfile
import traceback
import uuid


class BindingError(RuntimeError):
    pass


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path):
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise BindingError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    def invalid(value):
        raise BindingError(f"nonfinite JSON literal: {value}")
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique, parse_constant=invalid)


def contained(root, relative):
    root = Path(root).resolve()
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise BindingError("invalid relative artifact path")
    rel = PurePosixPath(relative)
    if rel.is_absolute() or any(x in (".", "..") for x in rel.parts) or ":" in relative:
        raise BindingError("unsafe relative artifact path")
    path = root.joinpath(*rel.parts)
    # No symlink-based substitutions, even if they happen to remain within root.
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise BindingError("symlink artifact path")
    resolved = path.resolve()
    if root not in resolved.parents:
        raise BindingError("artifact escaped its root")
    return path


def fsync_directory(path):
    """Require local POSIX directory durability; do not claim remote-FS safety."""
    fd = os.open(Path(path), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def publish_json(path, value):
    """Publish once without clobbering another receipt. JSON is durable first."""
    path = Path(path)
    data = canonical(value) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".publish-", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(tmp, path)  # Fails if the destination already exists.
        fsync_directory(path.parent)
    finally:
        tmp.unlink(missing_ok=True)
    return {"sha256": sha(path), "bytes": path.stat().st_size}


def file_info(root, path):
    root = Path(root).resolve()
    # Preserve the caller's path components until contained() has checked them.
    # Resolving first would hide a symlink and incorrectly bless its target.
    path = Path(path)
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError as exc:
        raise BindingError("artifact path is outside its declared root") from exc
    checked = contained(root, relative)
    if not checked.is_file():
        raise BindingError("missing artifact: " + relative)
    return {"path": relative, "sha256": sha(checked), "bytes": checked.stat().st_size}


def verify_file(root, info):
    if not isinstance(info, dict):
        raise BindingError("invalid artifact binding")
    path = contained(root, info.get("path"))
    if not path.is_file() or path.stat().st_size != info.get("bytes") or sha(path) != info.get("sha256"):
        raise BindingError("artifact byte identity mismatch: " + str(info.get("path")))
    return path


def tree_inventory(root):
    root = Path(root).resolve()
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise BindingError("symlink in artifact tree")
        if path.is_file():
            info = file_info(root, path)
            result[info.pop("path")] = info
    return result


def verify_tree(root, expected):
    if tree_inventory(root) != expected:
        raise BindingError("artifact tree differs from its committed inventory")


@contextlib.contextmanager
def lease(path):
    """Kernel-owned local advisory lock; released on process exit.

    The lock inode is retained. Deleting it while locked would allow a second
    operator to lock a different inode under the same pathname.
    """
    if sys.platform != "linux":
        raise RuntimeError("v1.4 operator lease is Linux-only; Windows is not validated")
    import fcntl
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    acquired = False
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BindingError("another operator holds this resource lease") from exc
        acquired = True
        record = canonical({"pid": os.getpid(), "host": socket.gethostname(), "utc": utc()})
        os.ftruncate(fd, 0)
        os.write(fd, record)
        os.fsync(fd)
        yield
    finally:
        if acquired:
            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def new_attempt(root, category="attempts"):
    parent = contained(Path(root), category)
    parent.mkdir(parents=True, exist_ok=True)
    attempt = parent / ("a-" + uuid.uuid4().hex)
    attempt.mkdir(exist_ok=False)
    return attempt


def report_failure(attempt, exc, **context):
    """Never require intact scientific source to report that source is broken.

    If even disk reporting fails, retain the original error and print the
    reporting failure separately to stderr. Never replace it with a success.
    """
    value = {"status": "FAILED_OR_PARTIAL", "utc": utc(), "pid": os.getpid(),
             "error": repr(exc), "traceback": traceback.format_exc(), **context}
    try:
        publish_json(Path(attempt) / ("FAILURE-" + uuid.uuid4().hex + ".json"), value)
    except BaseException as report_error:
        print(json.dumps({"failure_report_write_error": repr(report_error),
                          "original_error": repr(exc), "context": context}, default=str),
              file=sys.stderr, flush=True)


def portable_paths(value, roots):
    """Normalize known filesystem roots only; never alter tensor/checkpoint bytes."""
    if isinstance(value, dict):
        return {key: portable_paths(item, roots) for key, item in value.items()}
    if isinstance(value, list):
        return [portable_paths(item, roots) for item in value]
    if isinstance(value, tuple):
        return [portable_paths(item, roots) for item in value]
    if isinstance(value, str):
        for name, root in sorted(roots.items(), key=lambda pair: -len(str(pair[1]))):
            prefix = str(Path(root).resolve())
            if value == prefix:
                return "${" + name + "}"
            if value.startswith(prefix + os.sep):
                return "${" + name + "}/" + Path(value).relative_to(prefix).as_posix()
    return value


def prior_attempt_cost(root, category, binding, *, review_path=None, review_sha256=None):
    """Account completed invocations, or use an explicitly pinned failure review.

    The review is new evidence. It never replaces a missing/failed END receipt.
    Unknown elapsed time cannot silently become zero. A conservative upper bound
    may be used when that bound has actually been established by the operator.
    """
    import math
    review = None
    if review_path is not None or review_sha256 is not None:
        if review_path is None or not review_sha256 or sha(review_path) != review_sha256:
            raise BindingError("resume-review pin mismatch")
        review = read_json(review_path)
        if (review.get("schema") != "q010-reviewed-resume-v1.4"
                or review.get("binding_sha256") != binding):
            raise BindingError("resume review belongs to a different run")
    total = 0.0
    reviewed = set()
    for attempt in sorted((Path(root) / category).glob("a-*")):
        end = read_json(attempt / "END.json") if (attempt / "END.json").is_file() else None
        if end is not None and end.get("binding_sha256") != binding:
            raise BindingError("old invocation has the wrong run identity")
        disposition = None if end is None else end.get("disposition", end.get("status"))
        if disposition in ("PAUSED_CHECKPOINTED", "COMPLETE_FIT_NOT_QUALIFICATION",
                            "CAPTURE_COMPLETE_INDEPENDENT_SCORING_REQUIRED"):
            seconds = end.get("elapsed_seconds")
        else:
            rel = attempt.relative_to(root).as_posix()
            row = None if review is None else review.get("attempts", {}).get(rel)
            if (not isinstance(row, dict) or row.get("decision") != "RESUME_FROM_LAST_COMMITTED_STATE"
                    or row.get("tree_sha256") != digest(tree_inventory(attempt))
                    or row.get("accounting_basis") not in ("measured", "conservative_upper_bound")):
                raise BindingError("interrupted/failed invocation needs an explicit evidence-and-cost review: " + rel)
            seconds = row.get("accounted_seconds")
            if end is not None and seconds is not None and seconds < end.get("elapsed_seconds", 0):
                raise BindingError("review cannot reduce already measured elapsed time")
            reviewed.add(rel)
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds < 0:
            raise BindingError("missing or invalid invocation time accounting")
        total += seconds
    if review is not None and reviewed != set(review.get("attempts", {})):
        raise BindingError("resume review has unmatched or unnecessary invocation entries")
    return total
