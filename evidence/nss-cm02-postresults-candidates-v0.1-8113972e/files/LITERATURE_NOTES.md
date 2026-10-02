# Mechanistic precedents for the CM candidate review

Reviewed 2026-09-24. These are primary-paper abstract checks, not a systematic literature review or replications. No full-text paywall access or paper downloads were used. Findings below describe the papers; implications for NSS are our design inferences. None establishes NSS capability, efficiency or architecture superiority.

| Primary source | What the accessible abstract establishes | Implication for this proposal |
| --- | --- | --- |
| Bulatov, Kuratov and Burtsev, *Recurrent Memory Transformer*, NeurIPS 2022 ([paper](https://arxiv.org/abs/2207.06881)) | Memory tokens are passed between sequence segments; the model is trained to control memory operations alongside sequence processing. | A learned recurrent-memory arm needs a real persistent model state and trained update mechanism. CM-01's serialized reference packet does not supply that mechanism. |
| Rae et al., *Compressive Transformers for Long-Range Sequence Modelling*, 2019 ([paper](https://arxiv.org/abs/1911.05507)) | The model compresses past memories for long-range sequence modelling. | Reducing the width of a reference while retaining its archive does not demonstrate content compression. Compare retained information, reconstruction quality and total storage before making that claim. |
| Graves et al., *Hybrid computing using a neural network with dynamic external memory*, Nature 2016 ([paper](https://www.nature.com/articles/nature20101)) | A neural controller learns to read and write an external memory matrix from data. | Separate storage, addressing and learned control. A deterministic public reference resolver may be useful without demonstrating learned write policy or neural necessity. |

The immediate proposal tests deterministic continuity and reference freshness against ordinary retrieval controls. Learned memory-token writing and compression remain separate future hypotheses requiring a newly specified training experiment. A positive controller-continuity result would justify studying those mechanisms; it would not establish them.

Source-access scope: arXiv abstract pages and Nature's publicly accessible abstract were read. Search results from secondary sites were not used as evidence. The proposed controls and ranking are derived from the returned NSS evidence plus the distinctions above; they are not prescriptions or reported results from these papers.
