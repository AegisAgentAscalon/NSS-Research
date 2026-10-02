# Source and run chronology

1. Verified original archive hashes/CRC and inspected Pilot001's source and full report.
2. Implemented a new four-address task and candidate memory mechanisms. Development seed 141 was used, never a protected main seed.
3. A 450-step soft fit and two 1,800-step slot fits completed. A combined host command timed out during the initial GRUCell fit (last logged step 1,200); the reader had not started. The incomplete attempt remains recorded.
4. Replaced the slow per-event GRUCell implementation with exact-address packed GRU execution, checked against an independent sequential GRUCell fixture. The old source is in evidence/development/source_before_gru_optimization. Optimized GRU and reader 1,800-step development fits completed. Clear and training-distribution development screens are retained, including weak results.
5. Froze 2,400 steps and the final eight-condition protocol before all 40 main fits. REGISTRATION.json binds every experimental module and unit test present at that point. No main protected horizon cells had been scored.
6. All 40 main fits completed; no main fit was dropped or retried for performance. Added replay/snapshot/belief-control utilities in a separately registered supplement before protected scoring. The belief control's knowledge advantage is declared.
7. Published all ten calibration thresholds before any main episode scoring; then scored all 3,840 model cells and 240 exact-control cells. Core experimental files remained unchanged.
8. After seeing the tool-reader weak-write failure, registered a clearly post-hoc qualified-event-view diagnostic. It changes the experimental interface view, not raw observations, weights or original main results.
9. Replayed every checkpoint and main metric in a fresh interpreter; reproduced all supplementary cells/configurations. Repeated one entire 2,400-step training trajectory exactly. Foundation 68-test regression and 974-file manifest also passed.
10. Final packaging uses a fresh extraction, manifest verification, source-lock verification, checkpoint hashes and the 33-test study suite. The delivery receipt records that check separately from the full result replay.

The optimized development model source matches the final models.py. The earlier data.py snapshot retains the training generator used before the observation-noise evaluation branch was added. Development pre-run hashes record the source present at each stage. Main experimental files never changed after registration.

This is a local chronology, not external peer review, third-party preregistration, production qualification or permission to deploy.
