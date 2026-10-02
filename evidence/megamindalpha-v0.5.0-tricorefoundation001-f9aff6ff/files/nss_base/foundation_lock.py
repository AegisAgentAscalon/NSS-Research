"""Cross-process cooperative worker exclusion; OS releases locks on process exit.

A lock file is not another task database. Only Generations holds durable state.
Trusted callers use this lock before model execution and interrupted-job recovery.
It is not a sandbox against hostile code with direct access to the database.
"""
from contextlib import contextmanager
from pathlib import Path
import os
from .runtime import fail


@contextmanager
def worker_lock(directory):
    path = Path(directory) / '.foundation-worker.lock'
    f = path.open('a+b')
    locked = False
    try:
        if os.name == 'nt':
            import msvcrt
            f.seek(0, 2)
            if f.tell() == 0: f.write(b'0'); f.flush()
            f.seek(0)
            try: msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError: fail('CONSTRAINT_CONFLICT', 'Another live worker holds the component execution slot')
        else:
            import fcntl
            try: fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError: fail('CONSTRAINT_CONFLICT', 'Another live worker holds the component execution slot')
        locked = True
        yield
    finally:
        if locked:
            if os.name == 'nt':
                import msvcrt
                f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        f.close()
