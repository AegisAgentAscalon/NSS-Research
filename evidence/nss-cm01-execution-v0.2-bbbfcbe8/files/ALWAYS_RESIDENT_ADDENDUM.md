# Always-resident management context — proposed semantics

Status: architectural interpretation and follow-up specification notes, not a new executed candidate.

A small workspace may remain resident and be made available at each active recurrent step. Reuse fixed slots rather than append historical tokens. Distinguish (1) residency, (2) consultation frequency, and (3) rewrite frequency. Event-triggered rewriting can coexist with consultation at every step. An idle core need not execute merely to retain its workspace.

A controller interprets the tokens and updates the recurrent state or requests memory operations. Tokens themselves are not autonomous managers. Important references and write requests require provenance and revision checks. Retrieved evidence can temporarily exceed the persistent workspace budget; count that traffic separately.

A future native step could be specified as h_next = F(h, input, workspace, retrieved_evidence), with workspace_next = G(observable_events, h_next, workspace) only at declared update boundaries. This is a candidate interface, not a claim that the frozen Q010 models implement F/G in this form.

CM-01 tested a deterministic 56-byte reference manager and one-stage numerical reads. It did not test continual access inside a learned recurrence or learned storage writing. The software retention unit test is not a substitute for CM-02/03 continuity/cadence studies or CM-05 native training.

Required future comparisons: same resident buffer read each step versus event-only reads; fixed versus event-triggered/periodic rewriting; no workspace; identical structured fields; workspace plus archive with recurrent state disabled; total-memory/compute matched models. Keep constraints and hypotheses separate from demonstrated results. Do not train or edit the original 15 Q010 exports.
