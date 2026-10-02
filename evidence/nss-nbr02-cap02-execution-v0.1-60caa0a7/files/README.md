# CAP02 execution bundle

Fixed-budget preparation diagnostic for the existing typed NSS maintenance reader. See REPORT.md for results and limitations; PROTOCOL.md defines prospective decisions. Runnable on the recorded Python/PyTorch/NumPy CPU environment in SOURCE_FIXTURE_LOCK.json; no remote model required.

All scientific work is already complete. Do not rerun training into this directory. To independently reproduce, copy the bundle to a new output directory, retain parents/source/fixtures/protocol and remove generated checkpoints/results/audit outputs as appropriate; new run IDs and receipts must be used. `python source/cap02.py train --seed 8801` performs four96-step continuations; repeat only as a separately authorized replication, not repair of historical outcomes. The source preparation function's historical overlap check expects the supplied SH01 archive; serialized source fixtures make it unnecessary for replay.

For inference/count auditing of retained outputs: `python audit/recount_and_replay.py`. This writes audit/summary files, not training checkpoints. Use a copy to preserve delivered bytes. `source/cap02.py stream --seed ...` repeats the declared selected mixed-endpoint32-position checks, not new training.

Archive includes parent states, all60 original continuation checkpoints, raw fixtures, every endpoint output and the complete training journals. Zip hashes and the manifest detect accidental corruption; they are not authenticated adversarial storage.
