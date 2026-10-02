# Proposed NSS chat / Codex research-team workflow

This is a division of responsibilities to use when the user launches the work. No agent was launched by producing this document. Both the chat and Codex researchers can propose mechanisms, derive mathematics, review papers and challenge conclusions; Codex is not restricted to transcription/coding.

## Shared goal, separate jobs

The user directs research goals, accepted scope, compute spend, release choices and architecture changes. This chat is the main venue for explanations, cross-study synthesis and experiment decisions. A repository-grounded Codex coordinator manages implementation, execution and evidence delivery. Results return here with commit/run IDs, raw evidence and unresolved issues, not only a narrative.

A compact useful team is a coordinator plus three focused workers:

| Role | Main output | Separation |
|---|---|---|
| Theory/protocol researcher | Source map, candidate alternatives, explicit assumptions, mechanisms and controls | Does not silently revise the frozen main protocol after results. |
| Numerical implementation owner | Reproducible source, training/resume jobs and actual candidate artifacts | Does not self-certify main outcomes from prose. |
| Measurement/repro reviewer | Independent scorer, failure tests, full-state checks, resource and delivery receipts | Can reject a claim; cannot erase inconvenient experiments. |

Treat release auditing as a distinct pass, performed by a reviewer not responsible for the modified implementation where feasible. Larger issues can justify another specialized worker, but don't create a huge permanent team before measuring coordination and usage cost. One integration owner and bounded resource scheduler remain responsible.

## Branch/permission boundaries

Use real separate Git worktrees or otherwise isolated checkouts for concurrent writes. Worktrees isolate files; they do not isolate shared CPUs, memory, caches, datasets or external permissions. One worker owns each file area. Merge only after review/tests. Do not assume a new chat has read another chat's context or local files. Supply the approved protocol and actual source snapshot.

Current official Codex documentation describes subagent delegation, per-agent configurations, project AGENTS.md and isolated Git worktrees. Available models/efforts depend on the installed client/account. Use the user's selected Astra Ultra where available rather than inventing automatic access. Documentation references (consulted for this proposal):
- https://developers.openai.com/codex/models/
- https://developers.openai.com/codex/multi-agent/
- https://developers.openai.com/codex/app/worktrees/
- https://developers.openai.com/codex/guides/agents-md/
These currently redirect to the official ChatGPT Learn documentation.

## One durable experiment record

Keep a small experiment ledger keyed by experiment ID and candidate/source revision, with status such as planned,development,locked,running,completed,qualified-for-scope,failed,or reported-original-artifacts-unavailable. A report and an executable package are separate artifact types. Retain an open-questions register with exact failed conditions and ownership; it is not a backlog permission to widen every current study.

Each run records input/source hashes, environment, seed/RNG setup, data split, configuration, actual command, permitted surfaces, timestamps, compute/storage costs, exit status and outputs. A model writes hypotheses; actual programs produce measurements. Generated summaries never replace raw outcomes.

Changing a candidate, runtime, sampler or scorer changes the versioned evidence lineage. Experiments with different evidence, teacher budgets or objectives are not automatically comparable. Reconstruction and novel research stay on separate branches until reviewed.

## What parallelism should buy us

For recovery: source archaeology, implementation, and a separate scorer can progress in parallel after interfaces are agreed. Training starts only when data/model/protocol contracts are pinned. For later hard questions, assign workers competing causal explanations and discriminating tests, not merely several attempts to agree with the favorite idea.

Example: one worker tests representation ambiguity; another tests binding/ownership mistakes; the verifier constructs cases where the predictions differ. A biological-reference reviewer can separately map a mechanism to organism/task evidence without calling analogy validation.

Several agents agreeing is not independent empirical replication. Fresh code/scoring paths, new runs and eventually another machine matter. Independent local user operation is still not a blind third-party study, and neither is a substitute for longitudinal product testing.

## Avoiding another lost release

Code/spec/tests and a small release index should be saved first; checkpoint and raw-evidence shards follow as separate artifacts. A minimum executable pack must be genuinely executable, not just the report. Its dependency list and optional-evidence requirements must be explicit. Verify and acknowledge durable copies before treating a release as handed over.

Original archives stay immutable. No unrequested external uploads/public repositories or account setup. The selected user workspace becomes the durable research location once actually established; this chat remains a collaborator rather than the sole file store.

## Immediate assignment

Use Qualification010 reconstruction as the team's first bounded job. It has a surviving source base, a detailed historical specification and known failures to preserve. Deliver a verified new artifact and historical comparison before NBR02. Do not task the team with 'solve NSS' or change the tri-core design simply because multiple agents are available.
