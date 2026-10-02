# Original G01–G22 question register — preserved reference

The table and original priority note below are copied verbatim from S6, `program/G01_G22_REGISTER.md`. This is a documentary reference, not a new priority decision. For current status use START_HERE.md and CURRENT_STATUS.json in this handoff.

| ID | Problem | Priority | Original core question |
|---|---|---|---|
| G01 | Biological transfer | A | Which mechanisms are supported in humans, other mammals or flies, and which are only analogies? |
| G02 | Baseline competence | A | Is a failure caused by architecture, insufficient training, poor data or weak interfaces? |
| G03 | Persistent temporal state | A | What survives events, interruptions and restarts without transcript growth? |
| G04 | Recurrent depth | A | Does extra internal processing improve unfamiliar problems? |
| G05 | Recurrent stability | A | Do feedback, quantization or stale state amplify errors or cause loops? |
| G06 | Representation and binding | B | Can entities, relations, quantities and actions be recombined without confusion? |
| G07 | Exact/compact memory | A | What is lossless, what is approximate, and what must be rehydrated? |
| G08 | Delayed credit | A | Which past activity deserves which update? |
| G09 | Selective plasticity | A | Can new competence improve without destroying old competence? |
| G10 | Learning timing | A | When does a candidate update become the serving revision? |
| G11 | Sparse execution | B | Does sparsity reduce actual work and memory, not just nonzero counts? |
| G12 | Low-bit learning state | A | Can traces and updates retain useful information at 1–2 bits? |
| G13 | World-model reliability | A | Do predictions remain useful under new states, actions and longer horizons? |
| G14 | Reflection and replay | B | Does idle computation improve later work beyond extra data or ordinary search? |
| G15 | Appraisal | B | Does affect improve priorities without becoming fact, permission or pressure on the user? |
| G16 | Validation | A | Can the critic catch unsupported claims while preserving useful supported answers? |
| G17 | Neural interfaces | A | Do cores actually use exchanged information, and does it survive revision changes? |
| G18 | Scheduling/resources | A | What does always-active Primary participation cost with alternating auxiliaries? |
| G19 | Generation continuity | B | Can competence, memory use and agreed defining behavior survive replacement? |
| G20 | Evidence and privacy | A | Can generated material leak into facts, permissions or unauthorized learning? |
| G21 | Executable training tooling | A | Can NSS manage approved jobs through the same engine as ordinary LLM training? |
| G22 | Whole-system value | C | Does the combination earn its complexity and scale? |

Original priority note: first research focus **G03 + G04 + G08 + G12**, after **G02** and source/capability reconciliation; **G16–G18 are integration gates**. Evidence handling must not be deferred until a dreamer/learner is already connected to persistent memory.
