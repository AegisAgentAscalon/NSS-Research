# Development record (before any main seeds)

All first-stage 1200-step pilots are preserved. Record-hop and gated-hop learned
the short visible task. A flat GRU snapshot compressor did not. The standard
latent-space cross-attention variants needed more preparation; 6000-step raw
fits improved known facts but did not pass joint known/UNKNOWN competence.

A code-space alignment variant was therefore added BEFORE main registration:
each cross-attention output is decoded to the same numerical entity-code space
as the initial query and re-encoded by the same q_in. This tests a restricted
interface, not a novel full Transformer. Original latent-continuation classes,
checkpoints and losses remain replayable with their original kind names. The
new names are tied_aligned / fixed_aligned4. No held-out main episode or main
seed was used to make this choice. Alignment pilots still use seed741.

Aligned attention variants did not resolve UNKNOWN/repeated-depth reliability at
6000 steps on the development seed; both remain negative development evidence.
The original raw fixed4 attention had the stronger development result and is
retained with raw tied attention as main generic cross-attention candidates.
A four-stage UNshared content-attention control is added to match RecordHop's
strong field-structured inductive bias. It caps at four rounds by default; a
separately labelled cycled4 intervention may reuse its four trained stages.
No claim of a fair eight-step-vs-four-step architecture victory is permitted.

Before main registration, binder negative-sample construction was corrected:
fresh real-entity codes now live in the same first16 coordinates as existing
real-entity codes, rather than all17 coordinates. Otherwise the sentinel-axis
coordinate could partly reveal whether a query was new. Original training source,
pilot loss and checkpoint are retained; no main fit used the defective sampler.
