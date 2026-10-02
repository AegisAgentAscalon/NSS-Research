# RET-TRAIN-SELFPLAY-001 — deferred primary-literature review
User supplied screenshot: Self-Play Pretraining with Zero Data (arXiv:2609.30063v1, submitted24September2026).
Verified online at https://arxiv.org/html/2609.30063v1 on this execution turn. Authors: Aditya Cowsik,
Kfir Dolev, Michael Y. Li, G. Bruno De Luca, Nourya Cohen, Noah D. Goodman, Yoav Levine.

Primary-source mechanism summary: two randomly initialized autoregressive Transformers co-train.
A generator proposes executable programs producing byte sequences; a learner predicts those bytes.
The learner uses cross-entropy; the generator uses reinforcement-learning rewards tied to learning
progress. The authors report transfer to held-out natural-data prediction. This is an initial proof
of concept, not an NSS result. Zero-data refers to the natural training corpus, not zero generated
examples, compute, architecture choices or execution machinery.

Future questions (our proposals): compare learned task generation with cost-matched fixed procedural
curricula; preserve interpreter/verifier correctness, generation failures and compute; distinguish
structure transfer from learning contingent real-world facts. Consider as a training/synthetic-data
and later dream-maintenance lead, not implemented in TIMING01. No code/model downloaded or run.
