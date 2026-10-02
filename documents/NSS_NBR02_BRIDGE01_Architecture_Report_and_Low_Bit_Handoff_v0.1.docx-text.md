NEURAL SPACE SYSTEMS

A small bridgeto NSS

BRIDGE01 — Architecture, tests, findingsand low-bit research handoff

Working bounded dummy prototype. A real frozen recurrent checklist model is connected to exact task records and an action checker. Language replies and tool effects are scripted. No real language-model deployment is claimed.

Engineering result

Recorded outcome

Scripted sessions completed

216 / 216

Recurrent event suggestions matching the rule

4,144 / 4,144

Rule-based coordinator

Also completed every case

Next research priority

Low-bit inference and training



Version 0.1  •  29 September 2026

Read the record

1. The decision in plain English

2. What the bridge contains

3. The public rules and state lifetimes

4. What we tested

5. The actual outcomes

6. Verification, costs and limitations

7. How to run it and where a real model would attach

8. Low-bit research is now the exclusive next priority

9. Sources, archive and decision boundary

All other research is on hold after this prototype. The original evidence remains intact; no low-bit experiment was run here.

1. The decision in plain English

We built the small bridge. It connects a language-model-shaped interface, exact task records, a frozen recurrent checklist advisor, and an action checker. It can be run without downloading a language model.

The language slot is a scripted dummy, not a Transformer. The recurrent slot really executes four previously trained neural checkpoints. The action tools simulate work by recording effects in a local SQLite journal; they do not upload files, run shell commands, or contact an external service. This separation is deliberate: we are testing whether the pieces connect correctly, not claiming a finished conversational companion.

Question: Can this arrangement preserve unfinished work, reject invalid proposals and continue across interruption while keeping the learned state separate from exact truth?

Answer at the tested scope: All 216 scripted sessions completed with the declared exact action contract intact. The neural next-item suggestions matched the exact task rule at all 4,144 retained event observations across shadow and active-proposal modes. The ordinary rule coordinator also completed every case. There is no measured superiority of the recurrent coordinator.

Result

Observed outcome

Authored episode setups

24: 12 named recipes, two owner/task naming variants

Integration sessions

216

Sessions completed with correct final task records

216 / 216

Rejected invalid or failed proposals

558

Simulated durable effects

3,474

Duplicate, wrong-order or unapproved durable effects

0

Recurrent event observations matching the exact rule

4,144 / 4,144

New training, low-bit execution, real local-LLM inference

None



Counts are repeated engineering observations, not independent draws from real users. The approval-gate recipe repeats behavior also exercised in the clean recipe; twelve names do not imply twelve independent mechanisms.

Next priority: low-bit inference and training. Longer learning cycles, reader improvement, HSA/segmented extensions, DARP, DIRECT01 and broader integration are on hold. The bridge is preserved as a test surface, not the start of another refinement campaign.

Evidence: results/main/SUMMARY.json; audit/AUDIT.json; fixtures/EPISODES.json. See section 9 for source provenance.

2. What the bridge contains

The language model, controller, archive and action checker communicate through explicit interfaces. They do not share an assumed universal hidden-vector format.

Part

Implemented responsibility

What is not claimed

Language adapter

Creates chat-style messages; receives a six-field JSON proposal. A scripted dummy supplies replies for this test.

Language comprehension or a production LLM integration.

Exact journal

Binds owner, task, revision, events, approvals and simulated receipts. Reconstructs current state.

General semantic memory or authenticated untrusted storage.

Recurrent advisor

Updates a 64-value state per task from SET, CLEAR, RESET and NOOP; proposes the lowest unfinished item.

Learned permissions, arbitrary routing, English parsing or new workflow discovery.

Gate and fake executor

Validates the proposal against current records; records an authorized simulated effect and receipt in one transaction.

Exactly-once execution against arbitrary remote tools.

Snapshot layer

Saves task records and neural state, checks identity/cursors against the journal, and resumes the declared task.

Efficient no-replay startup or automatic migration across changed weights.



Information flow:

trusted source/tool event -> exact journal -> task-specific recurrent update

current task packet -> language adapter -> raw proposal -> validation -> simulated effect/receipt

The packet names the current task, its eight required steps, current statuses, approval validity, source revision and advisory next step. It never supplies a hidden scorer label. Its exact ledger facts are nevertheless privileged reliable software state; this is not a test of extracting those facts from natural language.

Three operating modes are implemented. Rule uses an exact next-step calculation. Shadow records the neural suggestion but still supplies the rule suggestion to the dummy. Recurrent supplies the neural suggestion, subjects the reply to the same gate and can fall back explicitly to the rule after a bad suggestion. No such fallback was required by a natural neural error in this panel.

The exact model values are unchanged. The same trained event interface is reused; no new authority or task-management role is inferred from the checkpoint's original checklist performance. This is not the old tri-core design.

Code: source/nss_bridge/bridge.py, recurrent.py, journal.py, adapters.py.

3. The public rules and state lifetimes

Every task has exactly eight ordered required steps: collect sources, draft report, prepare data, check report, check data, bundle, review package, publish. Names are dummy application labels for fixed item IDs, not language the recurrent model understands.

All steps start pending. A trusted performed receipt makes the named step done until an explicit reopen. The legal next step is the lowest-numbered pending item. Publishing additionally requires explicit approval for the current task revision. A proposed action, a plan, a note or a model assertion is never an executed-action receipt. Finish is allowed only after all eight steps are done.

The source event interface is separate from the proposal interface. The latter cannot create approval, reopen work, insert a receipt or change the task definition. Additional proposal fields are rejected, rather than treated as authority. The tests include a source note asking for approval to be ignored; the dummy is scripted to submit an invalid permission field. This is a schema/permission-boundary test, not proof of resistance to all language-model prompt injection.

Object

Lifetime and mutation policy

Learned weights

Frozen across every session; original float32 values evaluated in float64.

Recurrent bank

One 64-value vector and event cursor per owner/task; changes only on its own typed events.

Exact completion state

Derived from committed source/receipt events. Neural mistakes cannot rewrite it.

Approval

Tied conservatively to the current task revision; revisions require reapproval before publishing.

Effect receipt

A durable event for a specific task, step, epoch and request. Reopening increments the step epoch.

Request identity

Repeating an identical successful request returns its receipt; reusing the ID for different content is rejected.

Handoff

Journal binding, complete task records, model hash, state ABI, neural vectors and cursors.



SQLite commits the simulated effect and receipt as one event. A deliberately lost reply occurs after that commit. A new bridge instance replays the journal and returns the existing receipt without another effect. This contains the simulated ambiguity because there is no separately executed external side effect. A real tool needs its own idempotency key and outcome-reconciliation protocol.

Checksums detect accidental corruption but do not authenticate an adversary who can replace both content and checksum. The current snapshot loader rebuilds state from the journal before checking the saved envelope. This prioritizes inspectable consistency over fast restoration; do not claim a restart efficiency gain.

Public model-visible rules are retained in every packet and fixtures/EPISODES.json. Source/receipt meanings follow the new protocol rather than unstated English persistence assumptions.

4. What we tested

The fixture contains two tasks per episode, allowing interleaved work and separate recurrent banks. All source changes, deliberate faults and approval arrivals are authored in advance. Accepted proposals advance the fake work; no predicted answer is silently turned into a source receipt.

Recipe group

Exercise

Clean / approval gate

Finish both tasks; attempt publication without permission, then provide a trusted approval.

Restart / lost reply

Resume from a JSON snapshot; recover a receipt committed just before a deliberately lost response.

Revision / reopen

Reject a proposal made against an earlier revision; re-open a completed step and perform it in a new epoch.

Tool failure / malformed response

Do not create a receipt for failed work or invalid JSON; proceed after a later valid request.

Wrong scope / false finish

Reject another owner/task and an unsupported completion claim.

Untrusted note / redundant events

Reject invented permission in model output; carry task progress across forty no-op events.



Each of the 24 setups runs once under Rule and once per original parent under both Shadow and Recurrent: 24 + 96 + 96 = 216. All four parents are included; no stronger checkpoint is substituted after looking at results.

The fixture is an engineering smoke suite, not held-out general orchestration or language evaluation. Two naming variants mostly repeat event histories. Shadow and Recurrent often repeat exactly the same neural event sequence. Report counts as checks, not statistical confidence.

The protocol, source, fixtures and model exports were frozen in 14 lock entries before main execution. The post-result independent audit source was separately frozen before auditing. The preflight passed 41 checks, including malformed inputs, wrong task/owner/revision, repeated requests, stale snapshots, wrong model/state binding, and interrupted reply handling.

The HTTP adapter was exercised against a real loopback HTTP server implementing the expected reply envelope. The reply generator behind that server was still scripted. No llama.cpp executable or real language checkpoint ran. Any live model's response quality, tokenizer behavior and model-specific schema support still require integration testing.

Protocol: protocol/PROTOCOL.md. Case source: source/nss_bridge/runner.py. Preflight: results/PREFLIGHT.json.

5. The actual outcomes

All systems completed the authored work. That is useful evidence about the bridge's wiring and explicit guards. It is not evidence that recurrence beats the conventional coordinator.

Mode

Sessions

Correct final sessions

Recurrent event answers

Rejected proposals

Exact rule

24

24

Not applicable

62

Rule with neural shadow

96

96

2,072 / 2,072

248

Guarded recurrent suggestions

96

96

2,072 / 2,072

248



The learned suggestions never produced a false DONE on the observed event panel. Existing historical mistakes are not erased: this is a different, mostly simple event distribution and uses the original parents rather than claiming a new universally reliable checkpoint.

Raw response disposition

Count

Normal response confirming a simulated effect

3,456

Receipt committed but reply deliberately lost

18

Replay returning that existing receipt

18

Legitimate finish response

432

Approval-required rejection

432

Other rejection categories, 18 each

126



The other categories are malformed JSON, wrong owner, wrong task, stale revision, false completion, unsupported extra proposal fields, and simulated tool failure. Thus 558 rejections are expected containment events, not correct model answers. There are 3,474 distinct simulated effects: 3,456 normally acknowledged plus the 18 whose initial replies were lost. Replaying those 18 receipts causes no additional effect.

A representative restart episode makes progress on both Report and Data, saves the envelope, opens a new bridge instance, verifies the recorded history and continues. A representative lost-reply episode records a step durably, raises an injected interruption before returning, then recovers the existing receipt. Both retain the same task and source boundaries.

All exact prompts, six-field replies and acceptance/rejection reasons are stored. The dummy response is explicitly tagged as scripted; the recurrent trace separately retains every actual input token, hidden state, logits, prediction and exact event-rule label. Accepted records never overwrite the raw rejected candidate.

Detailed evidence: results/main/cases/*/RESULT.json; audit/AUDIT.json. Selected readable examples: docs/TESTS_AND_ANSWERS.md.

6. Verification, costs and limitations

A separately executed audit replayed the exact journal with set-based task state, independently of the bridge's Boolean state representation. It checked order, revisions, current approval, step epochs, duplicate effects and legitimate finish assertions. All 216 sessions satisfied those checks.

All 216 complete episodes were regenerated in a new Python process using fresh temporary journals. Every retained non-timing result, including raw messages, numeric states and snapshots, matched exactly. There are 4,482 recorded proposal/interruption entries; these include the 18 initial lost-reply observations, which are not normal completed responses.

For all 4,144 recorded recurrent event updates, independent PyTorch GRUCell/Linear computation was compared with the NumPy implementation. Across 302,512 hidden/logit scalars there were zero violations of the predeclared float64 envelope and zero differing class predictions. The maximum absolute difference was 7.11e-15. This is full coverage of the retained main event traces, not a guarantee about every possible future input.

Resource observation

Value / boundary

Learned parameters per active recurrent checkpoint

18,249

Numerical weight bytes during inference

145,992: float64, not low-bit

Live recurrent payload per task

512 bytes for 64 float64 values; cursor/object overhead extra

Largest model-visible packet

1,574 UTF-8 bytes; no language-token measurement

Largest retained JSON snapshot

8,872 bytes; exact records and journal storage are additional

Main measured runner core

6.331 seconds for 216 sessions

Recorded main-process peak RSS

99,147,776 bytes; includes Python/NumPy/SQLite, no real LLM

Independent audit core

7.861 seconds; separate PyTorch process



Times are this CPU environment's observed implementation costs, not a model-serving speed benchmark or total research bill. They include repeated dummy calls and durable SQLite writes, not real language generation. No efficiency advantage is inferred from comparisons of unequal repeated counts.

There were no unexpected main interruptions. Explicit crashes were authored tests. The request-round bound was enforced. The protocol's overall time/RSS/artifact limits were checked after the run rather than continuously enforced; this implementation limitation is recorded, not disguised as an OS sandbox. The checked footprint remained below 64 MiB before packaging.

No new fits, optimizer applications, gradient updates, low-bit tests, model downloads or live language inference occurred. There is no generalized learned routing, dynamic dependency planning, autonomous semantic critic, cross-weight state migration, self-directed training or product qualification.

7. How to run it and where a real model would attach

The default demo is offline and safe to inspect. It writes a new local output directory containing a SQLite journal, JSON snapshots and raw traces. Do not point it at important data or treat its fake receipts as external actions.

Requirements: Python and NumPy. This run used Python 3.13.5 and NumPy 2.3.5. PyTorch 2.10.0+cpu is required only for the supplied independent numerical audit and original checkpoint extraction. The executable demo uses exported NumPy weight arrays; no model download is necessary.

From the extracted package root:

python run_demo.py --out demo_output

python verify_package.py

Use a fresh output directory. The demo invokes one recurrent restart case with parent4101; the complete retained study used all four parents. The small example is not a selected best-fit result. Full study replay is available through the source runner and should use a separate output location.

The optional LocalChatClient sends explicit task packets to an already-running loopback chat-completion endpoint. It disables environment proxies and redirects, bounds request/response bytes, and does not download a model. It accepts literal 127.0.0.1 or ::1 HTTP endpoints only. Normal proposal validation still applies to the returned text.

A local server such as llama.cpp documents chat-completion routes and structured response support [E01]. That supplies an interface target, not evidence of compatibility with every model or server version. This run tested only a loopback dummy server. A real integration must pin the runtime/model, inspect its actual raw outputs, handle token limits and establish its ability to translate user instructions into faithful proposals.

No latent vector is injected into a transformer. The proposed bridge communicates through text/JSON packets; the transformer's KV cache and the controller's recurrent bank remain separate. Native HSA integration is not part of this bridge.

Replacing fake tool receipts with actual side effects requires write-ahead intent, external idempotency support where available, and explicit reconciliation of unknown outcomes. The current atomic simulation is not a proof of that distributed protocol. Automatic parameter changes are absent; candidate training/publication is a later interface, now on hold for low-bit work.

8. Low-bit research is now the exclusive next priority

Owner decision: after this dummy bridge, focus on low-bit inference and training. Put other research on hold until a declared practical low-bit working point exists or the owner changes the priority. This does not erase prior failures or authorize automatic future runs.

Low-bit means several different experiments. Making a checkpoint file smaller is not the same as using low-bit arithmetic, and storing weights compactly is not the same as training with little memory. Exact evidence, source IDs and action receipts must remain exact.

Next lane

ELI5 question

First bounded comparison to specify

LB01: inference and state

Can the same learned behavior run using fewer bits without losing required decisions or state continuity?

Establish a float32 working reference; test weight storage and recurrent-state precision separately, with packed byte counts and fixed event fixtures. Candidate weight points: 8-bit and 4-bit. No automatic full precision cross-product.

LB02: learning memory

Can it still learn and repair while keeping less training state?

Full-parameter adaptation remains a real objective. Compare full-precision optimizer state with one compressed-state method, retaining current/old-task checks and exact update/resume evidence.

LB03: more aggressive precision, conditional

Can lower-bit weights/updates work without hiding a large full-precision learner underneath?

Only after simpler results are informative, investigate 4-bit/ternary/2-bit paths, accumulation/rounding, and trace-specific hypotheses. Count every master/residual array.



The first action is the LB01 precision and resource protocol, using retained small checkpoints as cheap instruments. Existing exact work state and the bridge trace provide controlled repeatability; they do not qualify quantized language-model inference. Representative matrix shapes and eventual target hardware are needed before claiming native-kernel speed gains or whole-companion affordability.

A practical resolution should establish at least one usable inference path and one usable learning path with explicit precision maps, acceptable measured behavior, reproducible interruption/resume, and real resource accounting. They may use different or mixed precisions. This is not a demand that every tensor become two-bit, but neither is frozen-base adapter training a substitute for answering the full-adaptation question.

Numerical quality, packed storage, working tensor memory and native execution must be reported separately. Dequantize-then-float execution is useful for measuring sensitivity, but is not a native low-bit kernel. Wider gradient or master accumulators are legitimate if declared and counted. Python/framework overhead and other allocations may dominate tiny models; report both isolated tensor/state payloads and process-level peaks without claiming proportional total savings.

The original NSS handoff already distinguishes weights, recurrent state, optimizer moments, eligibility traces, master accumulators, activations and exact records [S02, low-bit section]. Public BitNet releases also distinguish packed ternary inference weights from BF16 training weights [E02]. Four-bit optimizer research concerns optimizer moments [E03]; QLoRA trains additions through a frozen quantized base [E04]. These are leads and distinctions, not results reproduced here.

On hold: CYCLE01-B, new-procedure learning, further reader preparation, pretrained companion evaluation, HSA/segmented extensions, DARP, DIRECT01, malleable-representation candidates, and expanded bridge integration. Previously named returns remain recorded. Fixing a blocker necessary for low-bit evaluation is allowed within that work; unrelated experiments are not quietly resumed.

9. Sources, archive and decision boundary

Retained research sources

[S01] NSS_NBR02_CYCLE01A_Feasibility_v0.1.zip and its original delivery receipt. Before extraction, the archive digest, manifest digest, exact membership and all 803 declared payload byte counts/SHA-256 values were checked. Reading the ZIP payloads also exercised CRC verification. This did not rerun CYCLE01-A or requalify its result. Selected original parent files and source extracts remain in this package.

[S02] NSS_Research_and_Architecture_Chat_Handoff_v1.0.md, especially task-state/evidence lifetimes and low-bit learning-state costs. Historical topology and priority language is not reinstated. Current user decisions control this prototype's scope and subsequent low-bit focus.

[S03] NSS_Test_and_Response_Review_Standard_v0.1.md. Raw tests and answers are retained. Finite rule checking covers the actual numerical/code inputs. No broad semantic critic or independent human review was implemented.

[S04] Prior current checklist v0.19. Its 54 historical entries are preserved unchanged; BRIDGE01 becomes entry55. Optional returns and prior literature leads remain recorded under a scheduling hold.

External interface and literature references

[E01] llama.cpp server README, official ggml-org repository, accessed 29 September 2026: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md . Used only to document a compatible-shaped future interface; no server/model download or paper reproduction.

[E02] Microsoft, bitnet-b1.58-2B-4T-bf16 official model card: https://huggingface.co/microsoft/bitnet-b1.58-2B-4T-bf16 . Precision-lifetime distinction only.

[E03] Li, Chen and Zhu, Memory Efficient Optimizers with 4-bit States: https://arxiv.org/abs/2309.01507 . Candidate optimizer-state compression lead; not an NSS result.

[E04] Dettmers et al., QLoRA: Efficient Finetuning of Quantized LLMs: https://arxiv.org/abs/2305.14314 . Frozen quantized base plus trainable additions; not full low-bit weight training.

Where the evidence lives

Path

Contents

source/nss_bridge/

Executable bridge, recurrent equations, journal, adapters, runner.

models/

Four original source-parent PT files and lossless NPZ exports.

protocol/

Main prospective protocol and pre-main source/input hashes.

fixtures/EPISODES.json

Authored task names, scopes and scenario recipes.

results/main/cases/

Every test, raw reply, source journal, model trace and JSON handoff.

audit/

Independent replay/recount/numerical checks; frozen audit source identity.

provenance/

Source identities, original receipts/reports and prior checklist snapshots.

docs/

Architecture/report, readable examples, run instructions and Codex handoff.



Final decision: retain BRIDGE01 as an executable dummy integration reference. It shows that the interfaces can be wired together on controlled tasks; it neither establishes a general learned orchestrator nor proves a benefit over exact coordination. Freeze further expansion and move to low-bit inference and training. No low-bit model was run in this pass.