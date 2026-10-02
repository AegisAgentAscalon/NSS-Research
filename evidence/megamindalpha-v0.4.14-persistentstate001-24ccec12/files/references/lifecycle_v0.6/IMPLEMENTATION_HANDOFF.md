# NSS learning lifecycle — implementation handoff

## Scope
Documentation is updated; the runtime/repository is unchanged. This is not a claim that new APIs, neural evaluation, profile scheduling or curation automation exist yet. The current approved user request was to update documents.

## Sources of design authority
Read Adjustment Brief v0.6, then the relevant sections of Core Concept v0.6, Master Contract Framework v0.3, Context & Cognition v0.3, and Learning/Evaluation/Lineage v0.1. Flowchart Architecture v0.3 illustrates those rules. In a conflict, stop and log the conflict rather than silently trusting an arrow or a generated example.

The reviewed Logic Atlas schema-v2 and its repository code remain the executable historical baseline until a deliberate integration pass. Use LOGIC_ATLAS_CHANGE_MAP.md to find affected existing IDs. Do not flatten 25 implementation flows into ten overview figures.

## Suggested bounded sequence when implementation is separately requested
1. Audit and identify the actual supplied repository baseline; reproduce tests and source hashes. Do not import historical 81/121 test counts as fresh evidence.
2. Define concrete serialized TaskRecord fields and validators first. Implement LT-01 through LT-03 and LT-14 around an existing deterministic runtime: one active QAP, dependency closure, directed transitions, Q0 return, ECID rejection and safe replay. No learned-router claim yet.
3. Add immutable DatasetSnapshot selection and permission/review state. Implement LT-04 through LT-06 with mock records; do not fetch external datasets or train weights as part of schema validation.
4. Define EvaluationPlan / EvaluationAssessment evidence binding and protected-suite exposure records. Implement LT-07 and LT-08 using deterministic mock judgments first. Keep candidate outputs untrusted and qualifier/releaser authority separate.
5. Add evidence-only CoreUpgradeProposal and lineage records for LT-10 and LT-11. The initial root Core has no parent; successor records name one parent and separately enumerate all contributing datasets/teachers/overlays. No mutation of accepted Core weights.
6. Only in a separately approved neural experiment, implement the selected overlay type, training curriculum and numerical runtime. Test LT-09 and LT-12 with matched controls, several generations, measured resources and predeclared tolerances. LT-13 can first use mock AR/DARP outputs to prove a shared validation gate; a real DARP model is not required.

## Decisions to make before code
Exact schema field types, unknown-field rejection, serialization/hash canonicalization, retention/deletion/revocation behavior, grants/expiry, crash points, tested QAP transitions, numerical precision and tolerances, dataset split boundaries, benchmark acceptance thresholds, resource caps, and evaluator calibration criteria. Missing criteria block release qualification; they are not default passes.

## Non-negotiable boundaries
The same accepted Core may act as a judge, but its score is evidence, not an authorization token. Use compatible Core-only evaluation state. Candidate weights never change the accepted Core or production overlays. Profile swaps are not mere index updates. Replaying computation must not repeat committed actions or delivered output. An unknown action outcome requires reconciliation, not a blind retry. A Core-fitness proposal is not permission to train or deploy.

## Per-pass delivery
Small owned interfaces, concrete stimulus/expected-result tests, complete test output, negative/fault cases, dependency checks, a plan-deviation log, source/artifact hashes, updated progress and handoff. Report mock/software checks separately from neural performance evidence. Optimize repeated mechanics only after behavior is covered; do not hide decisions or bypass trust boundaries.
