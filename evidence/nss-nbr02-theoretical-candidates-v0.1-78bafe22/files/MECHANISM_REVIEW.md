# NBR-02 mechanism review and source notes

**Outcome:** the preferred candidate is a proposed diagonal recurrent-sensitivity hybrid, with exact-gradient and frozen-learning controls. It is a small adaptive-rule screen, not demonstrated temporal-credit competence. Luna supplied the independent mechanism critique; root incorporated its findings and finalized this note. No derivative computation, model execution or experiment occurred here.

## Primary literature and limits

Murray's RFLO paper derives an approximate online recurrent learning rule by removing nonlocal gradient contributions and using random output-error feedback. That motivates examining which dependencies a cheaper update omits, but it does not validate the proposed rule. Our tanh recurrence retains a self-recurrent sensitivity term and uses the matched readout transpose for its learning signal; it is not unchanged RFLO and is not claimed to be biologically local. [Murray, 2019](https://elifesciences.org/articles/43299)

Bellec and colleagues study eligibility-based learning in recurrent spiking networks. This is relevant background for separating a retained eligibility quantity from a later learning signal. It is not evidence that the proposed tanh diagonal recurrence is e-prop or inherits its results. [Bellec et al., 2020](https://www.nature.com/articles/s41467-020-17236-y)

The Williams–Zipser primary DOI could not be opened; mirror/search excerpts are recorded for provenance but are not relied on for a scientific claim. Exact access results are in NETWORK_ACCESS.json.

## Accepted reasoning and corrections

These are deductions from the proposed contract, not findings established by the papers or an executed NSS experiment:

- If cue-time parameters, prediction and sufficient learning trace remain unchanged, a later identified label produces the same update. Intervening events are not ancestors of the earlier prediction. Pure feedback delay is therefore an invariance control; trace decay, overwritten information and changed parameters are separate interventions.
- The proposed eligibility recurrence drops cross-neuron derivative paths. A diagonal-recurrence special case should match exact gradients; a fixed development witness with a nontrivial exact-versus-approximate gradient discrepancy tests that the setting exercises omitted paths. Freeze its threshold, norm floor, tolerance and cost before training. Later learned decoupling is a result, not a reason to retune that gate.
- Clone weights at condition-stream start only. Retain learned weights across trials, reset hidden state and temporary traces at receipt boundaries, and keep probes read-only. This preserves parameter learning without a filler-induced live-state confound.
- Compare each learned arm against its own frozen post-initial-fit checkpoint, include both arms in immediate-feedback admission, exclude held-out mappings from earlier exposure, and retain all four seeds after the group gate.
- Full adaptive replay and the shuffled-receipt diagnostic consume real update attempts. The revised schedule is 4,404 per pass and 8,808 across two passes, below the proposed 9,800 global ceiling. Verification, forwards, exact-history operations and evidence storage need separately frozen limits.

Numerical equation verification, task grammar, seed recipes, learning rate, margins and actual-host feasibility remain pre-dispatch work for Chat. This review supports protocol review; it does not qualify a candidate or authorize execution.
