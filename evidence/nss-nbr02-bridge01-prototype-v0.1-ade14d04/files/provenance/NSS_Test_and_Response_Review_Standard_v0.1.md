# NSS — Test and Response Dual Review Standard

**Version 0.1 | 28 September 2026 | Evaluation policy and recording contract**

**ELI5:** Keep the exam paper and the student's original answer. Check both whether the question was fair and whether the answer was justified. An answer key is a hypothesis about the correct answer, not a substitute for evidence.

**Status:** Documented in response to the owner's instruction. This document and its blank record template do not constitute a completed semantic audit, a newly implemented automatic semantic grader, a corrected corpus, or a model experiment. No historical scores are changed.

## 1. One auditable trail from test to judgment

Retain every administered item and every raw response, including apparent successes, failures, invalid outputs, abstentions, retries and interrupted attempts. Deduplicate identical immutable evidence if useful, but retain an exact resolvable link for every observation. A checksum without accessible bytes is not sufficient.

The item record must preserve the actual model-visible instructions, question, evidence, record order, public task rules, output contract, and any earlier output or feedback that entered the context. Retain the serialized prompt and actual input token IDs/tokenizer identity where tokenization or truncation is used. Record omitted or truncated material: the reviewer must judge the input received, not a fuller intended prompt. If the historical input cannot be reconstructed exactly, mark that limit rather than inventing it.

Retain the unedited response tokens/text before parsing, normalization, repair or rejection. For a fixed-field reader, retain the original field atoms and their documented public meanings. Link the study/item/version, model checkpoint, seed, inference settings, attempt, timing and source identities. Hidden authoring facts, target labels and scorer configuration stay in a separate private portion; never feed them to the tested model or use them as if they were public evidence.

Existing output arrays can be linked through exact file/member/row locators; they need not be rewritten or copied into every review record. Any derived decode receives its own identity and is not passed off as the original response bytes.

## 2. Review the question before trusting its key

Start from only what the model was allowed to see. Where practical, hide model identity, existing grade, and the hidden key during the first test-validity assessment. Do this before training/evaluation on development templates; repeat it on realized evaluation items and inspect the returned answers for newly revealed flaws.

For each item, establish:

- What is being requested: observed behavior, assigned state, last-known record, required action, prediction, or inference?
- Which conclusions are justified by the public evidence and rules? Is one answer entailed, are several responses acceptable, or is there insufficient/conflicting evidence?
- What assumptions would be necessary? Were persistence, scope, temporal boundaries, change-log completeness, or other synthetic conventions actually stated?
- Does the output format permit an appropriate answer, including uncertainty when warranted?
- After this assessment, does the hidden key and scoring rule agree with those public conditions?

An intentionally underdetermined question can be a **valid** test of uncertainty when its expected response acknowledges that limitation. Underdetermination is a test defect when the key demands an unjustified unique answer. A model can learn a private synthetic convention from examples, but success under that convention must not silently be called evidence-only English comprehension.

Assess answerability and test/key quality separately. Useful answerability labels: `single_supported`, `multiple_supported`, `insufficient_evidence`, `conflicting_evidence`, `unresolved`. Useful test-quality labels: `valid`, `ambiguous_wording`, `missing_public_rule`, `key_not_justified`, `format_blocks_appropriate_response`, `input_construction_defect`, `unresolved`, `unreviewed`.

## 3. Review the response against the public test

Preserve the original deterministic/key score. Add a separate semantic judgment explaining whether the response was appropriate under the actual wording. Check all asserted content, including completion claims, action order, evidence binding, scope and explanations when present. Correct structured fields do not validate contradictory prose. Fluency is not evidence of correctness.

The response may be supported, appropriately uncertain, appropriately identify conflict, partly supported, contradicted, unsupported, or make an unjustified definite claim. An incomplete or unavailable response is not silently a wrong semantic answer; record its execution/interface status separately. Do not infer good reasoning solely from an abstention or from a lucky answer-key match.

For each judgment, cite the exact public passage(s), rule(s), or absence of information on which it depends and give a brief rationale. Record material claims individually where the response mixes correct and unsupported assertions. This is an auditable explanation of the decision, not a requirement to expose a model's private reasoning.

**A defective test never automatically passes every answer.** An appropriate uncertainty statement may deserve credit while a wrong-project assertion remains unsupported. Conversely, an output can match the original key and still be unjustifiably certain.

## 4. Keep review fair across models

Review apparent passes as well as failures. An item-level defect belongs to the exact public prompt and applies consistently to every model receiving it; do not invalidate a question only for the model whose score we prefer. Each distinct response still needs its own response-level judgment. Shared template reviews can support, but cannot replace, checking that an individual instantiation preserves the intended meaning.

Use a frozen semantic rubric and test-selection policy. The target is paired item/response review throughout the scored panel. Where a full semantic review is infeasible, publish review coverage and mark the remaining responses `unreviewed`; do not impute a representative all-panel semantic score from a selected subset. If sampling is used, declare it in advance or label it retrospective and descriptive. Disagreements and uncertain interpretations remain visible. A second pass by the same assistant is not independent replication; a separate Codex or human review counts only if it actually occurs, with its identity and notes recorded.

When responses reveal a new defect after scoring, record the discovery and apply a separately versioned adjudication across all affected arms. Freeze that adjudication before calculating revised totals. Do not use hidden author intentions or outside knowledge to fill a gap in a source-only task. The reviewer is fallible; unresolved cases do not become forced verdicts.

## 5. Report two results and the coverage between them

Every result summary should include:

1. Original answer-key scores under the historical protocol, with their original denominators.
2. Test-quality counts: valid, disputed/defective, unresolved and not reviewed, by family.
3. Response-appropriateness outcomes on the reviewed, adjudicated set, with exact eligibility and denominator.
4. Raw-versus-semantic disagreements: key-fail but appropriate, key-pass but unsupported, other partial judgments, and unresolved cases.
5. Review coverage, model/seed and underlying-history breakdowns, and the item IDs behind every exclusion or changed interpretation.

Keep intentionally insufficient-evidence items in their own clearly identified valid family when appropriate; do not drop them merely because there is no unique factual answer. Separate severity, such as false completion, from a pooled accuracy score. For a revised comparable score, the same reviewed item set must be used across arms; publish coverage gaps rather than compare different favorable subsets. Do not treat repeated token fields or repeated model runs as independent histories.

An aggregate semantic score is allowed only when its eligibility and pass mapping are stated. A flexible claim-level judgment need not be collapsed into one percentage. Original scores remain recoverable alongside any corrected-key or semantic result. New interpretations are not new model observations.

## 6. Illustrative decision table — not model outputs

| Public test | Illustrative response | Review outcome |
|---|---|---|
| Maple used blue on day 3. What did it use on day 4? No persistence or complete-log rule is supplied. | The day-4 use is not established; blue is only the recorded day-3 use. | Appropriate uncertainty. A key insisting on blue as the unique day-4 answer is not justified. |
| Same test. | It definitely used blue on day 4. | May match the key, but claims more than the evidence establishes. Do not silently grant semantic success. |
| Maple is assigned blue for days 3 through 5, inclusive. Which folder is assigned on day 4? | Blue. | Supported by the explicit interval. This does not assert that actual use complied with the assignment. |
| Same explicit assignment; Birch is assigned gold. | Gold, because Birch has gold. | Wrong-project/unsupported response. Distractor presence does not undermine Maple's explicit assignment. |

These examples are newly authored demonstrations of the standard. They were not generated by the LAB models, scored as experimental evidence, or added to confirmation.

## 7. What happens before the next LAB training comparison

The immediate prerequisite is the public-wording/answer-support audit, not more parameters or curriculum updates. Inspect the actual retained prompts, original targets and recorded answers using this paired view. Start with the known temporal issue, then cover the other families; do not assume they are valid or invalid merely by association. Include records that passed the old key.

If the corpus needs changes, preserve the old version and freeze an explicit new task contract, wording, allowed responses and scorer. Revised prompts require new model observations to assess their effects; a paper relabeling cannot establish that the model would have answered a corrected question. Retrospective regrading of old responses must be labeled as such. Material used for repair or tuning is no longer untouched confirmation. Use fresh grouped confirmation for any later preparation experiment.

The broader audit and its review coverage remain pending. LAB02-BIND remains proposed after that review. Nothing here authorizes a new model fit or reopens HSA, DARP, or scaling.

## 8. Sources and execution boundary

- Owner's current instruction: retain each administered test and answer; evaluate both the test and the response when grading.
- `NSS_LAB_Temporal_Wording_Review_v0.1.md`, Trigger and finding; Direct source observations; Scope and interpretation. This review identifies the concrete unstated-persistence issue and preserves original source identities.
- `NSS_Research_Checklist_CURRENT.md`, version 0.11, Before the next run. The prior checklist places public-wording review ahead of LAB02-BIND.
- `NSS_DIRECT01_Chat_Handoff_v0.1.md`, lines 37–39 in the provided handoff. It distinguishes exact-rule checking from source-grounded language review. This standard adds no DIRECT01 dispatch.

This update writes a policy, blank record template and synchronized checklist only. It does not claim that archived responses have now received semantic review, that a language-semantic oracle has been implemented, or that any model was run. No historical archive is merged, changed or rescored.
