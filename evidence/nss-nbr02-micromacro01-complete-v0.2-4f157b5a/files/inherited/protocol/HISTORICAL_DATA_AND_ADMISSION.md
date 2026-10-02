# REHEARSE01 v0.1 — data, IDs and prospective admission
All recipes below are proposed and must be implemented/source-locked before any episode or label draw.
No concrete main mapping or stimulus was generated in this review.

## 1. Coordinates, scopes and examples
Scope0 old cues0..3; scope1 old4..7.
Scope0 development8,9; scope1 development10,11.
Scope0 held-out12..15; scope1 held-out16..19.
START=22; PRIME=20+scope. Single-example prefix=[22,20+scope,cue].

For groups old/development/heldout and each scope independently, initialize NumPy PCG64 with
SEEDS.json label labels/{group}/scope{s}, permute that group's listed ascending cue coordinates,
assign label1 to the first half and0 to the second. This keeps groups balanced as in the inherited recipe.
Draw old after source lock, development after technical cost admission, and heldout only after A0 and
B1-only calibration are frozen. A failed gate never instantiates the held-out labels.

Base index b=0..11; f=b+8.
Protected old p=[4,5,0,1,4,5,6,7,0,1,2,3][b].
Development bases0..3; heldout4..11.
Cue chronology f,p,f,f,p,f; f uses its initial label in trial1 and its flipped label at trials3,4,6.
p retains its old label at trials2,5. Main delays are zero.
The public change detector uses previous released outcome per scoped key; no branch selection from b,
trial index, hidden reversal flags, future suffix or scorer output.

## 2. Fresh fits and teaching orders
For fit0..3, use the dedicated initialization and initial-order seeds in SEEDS.json.
G and L share initial parameter bytes and the same teaching examples, but never an optimizer state.

Draw row-major:
W uniform[-sqrt(6/39),sqrt(6/39)] with shape16×23; cast f32.
U uniform[-.05,.05] shape16×16 plus float64 .25*identity; cast f32.
b=zeros16 f32; V uniform[-.02,.02] shape2×16; cast f32; a=zeros2.
Concatenate in W,U,b,V,a order. Preserve generator state before and after draws.
No label-conditioned initialization.

The order generator concatenates independent full permutations of0..7 until at least100 entries, truncates
at100, and records its generator states/order. Apply exactly100 online clip1 updates to each method.
A new initial fit never loads an older model checkpoint. Retain every old performance miss and all fit identities.

Technical cost probes use the fixed technical map from FIXTURES.md and ten warmups per method,
followed by two full four-branch contexts per method. Total100 applications. They use the separate probe
initialization/order; all probe weights are discarded. Technical labels are not main development labels.

## 3. New ID recipe and namespace accounting
Seeds are first8 SHA256 bytes (big-endian uint64) of ASCII:
    NSS-NBR02-REHEARSE01-REVIEW-v0.1/{allocation_label}.
This proposal checks33 direct allocations for within-set uniqueness; it does not claim a full historical collision
audit. Execution preflight must scan available prior seed/source/receipt text, report scope and gaps, and
stop on an actual unrelated identity collision without resampling.

Receipt ASCII preimage:
    REHEARSE01-v0.1|{wire_seed:016x}|{phase}|{base_tag}|{trial}|receipt
receipt ID = first8 SHA256 bytes, lowercase16-character hex; all-zero or unrelated collisions stop.
Initial base_tag=fit{fit:02}; main=base{b:02}; probe/fixture=case{c}; sandbox=bad-{method}-{label}-{defect}.
Use wire/main for initial/main; wire/probe for probes; wire/fixture for fixtures; wire/faults for sandbox.
Initial G/L intentionally consume corresponding data in distinct learner namespaces. Branches intentionally
reference the same environmental receipt; their consumption key is learner/condition/branch/receipt.

Rehearsal operation ID is full SHA256 of canonical JSON containing schema, learner namespace, branch,
parent online application ID, batch ordinal0 and ordered source receipt IDs. Do not call it new feedback.
Source record hash includes schema, cue/scope/features, released label and receipt/version provenance.
Shared hashes do not hide different metadata; exact aliasing requires identical complete stored bytes.

All generators and actor code are fixed before draws. Full RNG and cursor states, instantiated receipts,
labels in isolated scorer/generator records, and source/public-prefix identities are retained.
Known old maps and simple binary label grammars can repeat. Report complete map and normalized history
overlap with accessible DC01/REV01/PROTECT01 evidence. Never resample to find a favorable or artificially novel
mapping. Missing earlier random draws remain unverified, not implicitly disjoint.

## 4. Score pools and A0
B1 primary development pool=4bases × trials2,3,4,5,6, always after its real clip1 update:20 rows per fit.
K=4bases × focal trials3,4,6:12 rows per fit. Trial1 first exposure is excluded; protected-old probes are excluded.
Every K row is fixed before scores. Its target is available through the applicable lawful receipt, not beforehand.

For each arm/fit report:
initial old accuracy /8; B1 overall /20; N overall /20; B1_K /12; N_K /12; H=12-N_K;
gain=B1_K-N_K; normalized_gain=gain/H only for H>0; integer test 2*gain>=H.
The numerator can be negative. It subtracts newly introduced errors on formerly N-correct cases.
Zero H is not divided, set to1, or auto-passed.

All three must hold for a fit to be informative-and-admitted:
old8/8; B1>=16/20; H>0 and 2*gain>=H.
Require>=3/4 in EACH method. Retain all4 after group admission.
No guarantee that this new rule will admit the models; it removes one impossible-count design, not the
possibility of an honest saturation/competence stop.

The0.5 fraction is Codex's prospective pragmatic choice, not statistically calibrated. It demands recovery of
at least half the fixed available frozen-control misses, while the absolute floor prevents grossly weak total
performance. With small H one changed outcome can alter admission; publish the integers and keep a strong N.
The prior PROTECT01 development data are not used to set or validate this rule.

## 5. Confidence calibration
B1 only; trials3 and4 of each development context compared with common post-trial2 old inventory.
For each of32 base/fit/checkpoint units per method, average loss and probability margin across8 old cues.
Take absolute changes from its own pre-fork reference; q_loss/q_margin are medians of these32 observations.
tau_loss=min(.01,max(.002,q_loss)); tau_margin=min(.02,max(.005,q_margin)).
No use of U/F/R results, held-out labels, historical favorable tau values or best-fit selection.
Loss is logaddexp(logit0,logit1)-logit_y evaluated stably in independent float64 scoring;
probability margin is p_y-p_other. Tie class0; zero logit margin can be correct for label0.
