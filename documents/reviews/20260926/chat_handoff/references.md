# NSS research handoff references

Prepared 26 September 2026 for the dedicated NSS Chat. This annotated reference set preserves the selected citations in both supplied architecture handoffs: **A-R01–A-R27** means the labels in `NSS_Architecture_Learning_and_Evaluation_Handoff_v0.1.docx`; **C-R1–C-R23** means the labels in `NSS_Cognition_Architecture_and_Low_Bit_Learning_Handoff_v1.0.docx`. Repeated papers retain both labels on one record. The bibliography is deliberately limited to sources already cited in those documents; it is not a new broad literature survey.

## How to use these sources

The literature serves three roles: candidate computational mechanisms and controls; observations or models in specific nervous systems; and implementation guidance on model storage and memory. None is direct evidence that an NSS study passed, a proposed module exists in code, or the full architecture works. NSS results remain in the reports, protocols, and archives indexed in `RESEARCH_INDEX.md`.

The fruit-fly work cautions against simple size analogies. FlyWire is an adult female *Drosophila* wiring map, not a complete record of effective strengths, dynamic states, learning rules, modulation, sensory history, or behavior. Separate fly studies add task-specific models and interventions. The safe inference is methodological: circuit structure can constrain hypotheses, and scoped models can make testable predictions. A biological neuron is not one artificial parameter, a synapse is not one scalar weight, and connectome cell counts cannot be directly compared with language-model parameter counts. A fly central-brain model of selected sensorimotor transformations is not a functioning digital fly.

Keep human and other-mammal studies distinct. Gidon et al. measured dendritic activity in human cortical tissue ex vivo; Hassabis et al. studied people with hippocampal amnesia; Liu et al. studied replay in people. Murray et al. analyzed macaque working-memory recordings, and the sleep papers concern mice. These results motivate questions about population codes and replay but are not human sleep experiments or NSS schedules. Biological sleep does not establish that an agent should “dream,” that synthetic replay preserves experience, or that one subsystem should train another overnight.

Low-bit citations support experiments, not claims that a whole learner operates at its parameter tensor’s nominal bitwidth. Moments, eligibility traces, gradients, master values, scales, indices, RNG, activations, temporary buffers, and KV caches have distinct costs and error dynamics. Two-bit optimizer results do not establish two-bit trace learning. BitNet’s “1.58-bit” label describes ternary weights; its official release separates packed inference weights from BF16 training weights. Measure actual bytes and retain a higher-precision reference.

Bibliographic metadata and claim-relevant abstracts or primary pages were checked online on 26 September 2026. Full papers were not exhaustively re-reviewed or reproduced. Where the publisher denied access or required cookies, the record below says so and uses an official index/author source only for the limited metadata or abstract it exposed. “NSS use” describes the role the original handoffs assigned to a citation and the boundary needed for a fair transfer.

## Annotated bibliography

### Recurrent computation, state, and model controls

1. **A-R02.** De et al. (2024), [“Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models”](https://arxiv.org/abs/2402.19427), cited arXiv version 2402.19427; publication status not checked. The record describes Hawk and a recurrence/local-attention hybrid; it is a candidate efficient sequence-model control, not evidence for persistent personal memory or continual adaptation.

2. **A-R03.** Sun et al. (2024; revised 2025), [“Learning to (Learn at Test Time): RNNs with Expressive Hidden States”](https://arxiv.org/abs/2407.04620), cited arXiv version 2407.04620; publication status not checked. Its hidden state is itself updated as a learned model on test sequences. For NSS this separates adaptive sequence state from ordinary fixed recurrent state; the reported language-model evaluations do not qualify long-term companion memory.

3. **A-R04.** Behrouz, Zhong, and Mirrokni (2025), [“Titans: Learning to Memorize at Test Time”](https://arxiv.org/abs/2501.00663), cited arXiv version 2501.00663; publication status not checked. The proposed neural long-term-memory module is paired with attention and tested on language, reasoning, genomics, and time series. It is a memory mechanism comparator, not proof of reliable autobiographical recall or safe revision.

4. **C-R1.** Vaswani et al. (2017), [“Attention Is All You Need”](https://arxiv.org/abs/1706.03762), arXiv:1706.03762. The Transformer uses attention rather than recurrent/convolutional sequence layers in its original design. It anchors the standard baseline; fixed-depth attention alone does not provide a versioned external evidence archive or online lifelong learning.

5. **C-R2.** Dehghani et al. (2018; ICLR 2019), [“Universal Transformers”](https://arxiv.org/abs/1807.03819), arXiv:1807.03819. This is a parallel-in-time, self-attentive recurrent model with repeated computation and halting. It is relevant to testing learned recurrent depth; repeated refinement is not the same variable as retaining state across real-world episodes.

6. **C-R3.** Dai et al. (2019; ACL 2019), [“Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context”](https://arxiv.org/abs/1901.02860), arXiv:1901.02860. Segment recurrence extends context across chunks. It is a strong context-state control, but its evaluated recurrence is not an exact fact store, a user-memory policy, or a changed-weight continuation guarantee.

7. **C-R4.** Geiping et al. (2025), [“Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach”](https://arxiv.org/abs/2502.05171), cited arXiv version 2502.05171; publication status not checked. The paper studies iterative latent computation at inference. NSS should compare added within-problem computation separately from elapsed-event state and parameter learning; the work does not establish lifelong memory.

8. **C-R5.** Gu and Dao (2023), [“Mamba: Linear-Time Sequence Modeling with Selective State Spaces”](https://arxiv.org/abs/2312.00752), arXiv:2312.00752. Selective state-space sequence modeling is a relevant recurrent-style baseline. Its sequence efficiency is not evidence of adaptation across sessions or of a three-core role topology.

### Continual learning, repair, replay, and evaluation

9. **A-R01.** Duncker et al. (2020), [“Organizing recurrent network dynamics by task-computation to enable continual learning”](https://proceedings.neurips.cc/paper/2020/hash/a576eafbce762079f7d1f77fca1c5cc2-Abstract.html), NeurIPS 33, peer-reviewed proceedings. The method protects task-relevant activity subspaces while reusing compatible dynamics. It is a literature lead for preserving recurrent computation, not the same method as NSS’s PROTECT01 output-margin constraint.

10. **A-R05.** Schwarz et al. (2018), [“Progress & Compress: A scalable framework for continual learning”](https://proceedings.mlr.press/v80/schwarz18a.html), ICML/PMLR 80:4528–4537, peer-reviewed proceedings. An active column learns and is consolidated into a knowledge base while protecting earlier tasks. It motivates explicit candidate/serving comparisons; its task setup and transfer process differ from NSS’s stateful companion goal.

11. **A-R06.** Riemer et al. (2019), [“Learning to Learn without Forgetting by Maximizing Transfer and Minimizing Interference”](https://arxiv.org/abs/1810.11910), ICLR 2019; arXiv:1810.11910. Meta-Experience Replay combines episodic replay and meta-learning to trade off transfer and interference. It motivates replay and correction-policy controls, not an indefinitely improving repair agent.

12. **A-R07.** Javed and White (2019), [“Meta-Learning Representations for Continual Learning”](https://proceedings.neurips.cc/paper/2019/hash/f4dd765c12f2ef67f98f3558c282a9cd-Abstract.html), NeurIPS 32, peer-reviewed proceedings. The work meta-learns representations intended to support future online acquisition. It is relevant to successor initialization; it does not prove transfer for NSS’s personalized data or its complete architecture.

13. **A-R08.** Andrychowicz et al. (2016), [“Learning to learn by gradient descent by gradient descent”](https://arxiv.org/abs/1606.04474), arXiv:1606.04474. Learned optimizers show that update rules can themselves be trained for families of tasks. The NSS handoff treats this as a later repair-policy direction, not a ready-made general repair controller.

14. **A-R09.** Dohare et al. (2024), [“Loss of plasticity in deep continual learning”](https://www.nature.com/articles/s41586-024-07711-7), *Nature* 632:768–774, version of record. It distinguishes loss of the ability to learn new tasks from catastrophic forgetting of old examples and reports continual-backpropagation remedies in tested benchmarks. This supports measuring future learnability separately; it does not show the same effect or remedy in NSS.

15. **A-R12.** Shin et al. (2017), [“Continual Learning with Deep Generative Replay”](https://arxiv.org/abs/1705.08690), arXiv:1705.08690. A generative model supplies synthetic past-like examples during sequential learning. It motivates replay controls, but generated samples are not exact recovery of a user’s historical facts or provenance.

16. **A-R13.** Wang et al. (2018), [“Dataset Distillation”](https://arxiv.org/abs/1811.10959), arXiv:1811.10959. The paper studies small synthetic training sets that preserve learning behavior for bounded image tasks. It motivates compressed-practice comparisons, not a general lossless summary of personal experience.

17. **A-R14.** Hinton, Vinyals, and Dean (2015), [“Distilling the Knowledge in a Neural Network”](https://arxiv.org/abs/1503.02531), arXiv:1503.02531. Teacher outputs can train a student to imitate behavior. NSS may use this as a teaching mechanism, while keeping exact source records separate because distillation does not guarantee lossless transfer.

18. **A-R10.** Ribeiro et al. (2020), [“Beyond Accuracy: Behavioral Testing of NLP Models with CheckList”](https://aclanthology.org/2020.acl-main.442/), ACL 2020, peer-reviewed proceedings. Capability-by-test-type matrices help expose behavior failures beyond aggregate accuracy. It supports extending regression libraries, not proof that a finite suite catches all future defects.

19. **A-R11.** Dwork et al. (2015), [“Generalization in Adaptive Data Analysis and Holdout Reuse”](https://arxiv.org/abs/1506.02629), arXiv:1506.02629. Repeated adaptive use can overfit a holdout; the paper studies methods for controlled reuse. This supports separating development/guard cases from independent confirmation in NSS; it is not itself a test-suite migration method.

20. **A-R15.** Lewis et al. (2020), [“Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”](https://arxiv.org/abs/2005.11401), arXiv:2005.11401. Retrieval and parametric generation can jointly support bounded knowledge tasks. It grounds the distinction between retrieval-assisted performance and learned neural competence; it does not make those outcomes interchangeable.

21. **A-R17.** Cowsik et al. (2026), [“Self-Play Pretraining with Zero Data”](https://arxiv.org/abs/2609.30063v1), cited arXiv version 2609.30063v1, submitted 24 September 2026; publication status not checked. The proof of concept trains a generator and learner from random initialization on computable byte sequences, then tests natural-data transfer. NSS’s proposal starts from pretrained components and existing experience, so it is not a reproduction or evidence of the same transfer.

22. **A-R27.** Chen, Goodfellow, and Shlens (2016), [“Net2Net: Accelerating Learning via Knowledge Transfer”](https://arxiv.org/abs/1511.05641), arXiv:1511.05641. Function-preserving network transformations are demonstrated for supported architectures. This is a model-growth lead, not a general operation for migrating NSS parameters, state, interfaces, and evidence.

### Fly circuits and mammalian memory observations

23. **A-R18; C-R7.** Dorkenwald et al. (2024), [“Neuronal wiring diagram of an adult brain”](https://www.nature.com/articles/s41586-024-07558-y), *Nature* 634:124–138, version of record. The FlyWire adult female fly reconstruction contains 139,255 neurons and roughly 50 million chemical synapses. It is a structural map with annotations, not a complete dynamical or learning model.

24. **A-R19.** Shiu et al. (2024), [“A Drosophila computational brain model reveals sensorimotor processing”](https://www.nature.com/articles/s41586-024-07763-9), *Nature* 634:210–219, version of record. A connectome-based leaky-integrate-and-fire model predicted selected feeding and grooming circuitry; predictions were tested with neural and behavioral interventions. Its scope is specified sensorimotor tasks, not whole-animal cognition.

25. **A-R20; C-R8.** Lappalainen et al. (2024), [“Connectome-constrained networks predict neural activity across the fly visual system”](https://www.nature.com/articles/s41586-024-07939-3), *Nature* 634:1132–1140, version of record. The authors constrain a motion-pathway model with measured connectivity, optimize unknown cellular/synaptic properties for a visual task, and compare predicted activity with 26 studies. This supports structure-plus-task fitting, not a unique computation from wiring alone.

26. **C-R9.** Turner-Evans et al. (2020), [“The Neuroanatomical Ultrastructure and Function of a Biological Ring Attractor”](https://doi.org/10.1016/j.neuron.2020.08.006), *Neuron* 108:145–163.e10, version of record. Connectomic reconstruction and functional measurements examine a fly heading circuit. It supports a task-specific circular-state hypothesis; ring geometry is not a general model of thought.

27. **C-R10.** Aso et al. (2014), [“Mushroom body output neurons encode valence and guide memory-based action selection in Drosophila”](https://elifesciences.org/articles/4580), *eLife* 3:e04580, version of record. The study links mushroom-body output activity with learned valence and approach/avoidance selection. It motivates separating stored associations from their behavioral use; its circuit roles do not map one-for-one onto NSS modules.

28. **A-R21.** Hige et al. (2015), [“Heterosynaptic Plasticity Underlies Aversive Olfactory Learning in Drosophila”](https://pubmed.ncbi.nlm.nih.gov/26637800/), *Neuron* 88:985–998, version of record (DOI 10.1016/j.neuron.2015.11.003). The study reports timing- and compartment-dependent plasticity in mushroom-body output synapses. It motivates tests of eligibility and learning-signal timing, not a universal credit-assignment rule.

29. **A-R22.** Seelig and Jayaraman (2015), [“Neural dynamics for landmark orientation and angular path integration”](https://www.nature.com/articles/nature14446), *Nature* 521:186–191, version of record. Fly ellipsoid-body population activity tracks landmarks, self-motion, and persistent heading. The ring-attractor interpretation fits a circular navigation variable, not a generic memory system.

30. **C-R11.** Gidon et al. (2020), [“Dendritic action potentials and computation in human layer 2/3 cortical neurons”](https://pubmed.ncbi.nlm.nih.gov/31896716/), *Science* 367:83–87, version of record (DOI 10.1126/science.aax6239). Ex-vivo human cortical neurons showed graded calcium-mediated dendritic action potentials and nonlinear input computation. The publisher page returned 403 during this check; PubMed exposed the abstract and bibliographic record. This supports biological computational richness, not a requirement to reproduce ion-channel detail.

31. **C-R12.** Hassabis et al. (2007), [“Patients with hippocampal amnesia cannot imagine new experiences”](https://pmc.ncbi.nlm.nih.gov/articles/PMC1773058/), *PNAS* 104:1726–1731 (DOI 10.1073/pnas.0610561104). The patient study reports difficulty constructing richly detailed new imagined scenes. The PNAS page redirected to a cookie screen; the primary PMC article was accessible. A lesion study does not establish a single exclusive imagination module.

32. **A-R24; C-R13.** Liu et al. (2019), [“Human Replay Spontaneously Reorganizes Experience”](https://doi.org/10.1016/j.cell.2019.06.012), *Cell* 178:640–652.e14, version of record. The source handoffs cite human replay that reorganizes recently learned sequence structure. The publisher returned 403 in this check; bibliographic metadata was accessible through indexing. This is not subjective dream evidence or proof that generated replay preserves exact source episodes.

33. **A-R23.** Murray et al. (2017), [“Stable population coding for working memory coexists with heterogeneous neural dynamics in prefrontal cortex”](https://www.pnas.org/doi/10.1073/pnas.1619449114), *PNAS* 114:394–399, version of record. The paper analyzes lateral prefrontal recordings from macaques doing seconds-long working-memory tasks and finds a stable population subspace despite dynamic single-neuron activity. This is nonhuman-primate evidence, not a human experiment or post-update state-migration result.

34. **A-R25.** Chang et al. (2025), [“Sleep microstructure organizes memory replay”](https://www.nature.com/articles/s41586-024-08340-w), *Nature* 637:1161–1169, version of record. In naturally sleeping mice, non-REM substates segregated replay of recent and prior experiences; timed ripple disruption affected recent-memory recall. This is mouse sleep physiology, not a recommended NSS schedule or evidence about human overnight learning.

35. **A-R26.** Li et al. (2017), [“REM sleep selectively prunes and maintains new synapses in development and learning”](https://www.nature.com/articles/nn.4479), *Nature Neuroscience* 20:427–437, version of record (DOI 10.1038/nn.4479). Mouse motor-cortex work links REM sleep to selective pruning and maintenance of newly formed spines. The authors limit the study to specific neurons and contexts; it does not justify arbitrary software pruning or a fixed sleep-cycle design.

### Learning, world models, and low-bit state

36. **A-R16; C-R14.** Hafner et al. (2023; revised 2024), [“Mastering Diverse Domains through World Models”](https://arxiv.org/abs/2301.04104), cited arXiv version 2301.04104, and Hafner et al. (2025), [“Mastering diverse control tasks through world models”](https://www.nature.com/articles/s41586-025-08744-2), *Nature* 640:647–653, version of record. The arXiv record and journal article share the same four authors and DreamerV3 work; preserve both original citation labels across the arXiv and journal versions. Dreamer learns world models and improves behavior by imagined trajectories on bounded control tasks, not arbitrary personal-life simulation.

37. **C-R15.** Li et al. (2023), [“BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models”](https://arxiv.org/abs/2301.12597), arXiv:2301.12597. A trained bridge joins frozen vision and language components in vision-language tasks. It is an interface precedent, not evidence that arbitrary NSS latent spaces interoperate.

38. **C-R6.** Bellec et al. (2020), [“A solution to the learning dilemma for recurrent networks of spiking neurons”](https://www.nature.com/articles/s41467-020-17236-y), *Nature Communications* 11, article 3625, version of record. E-prop combines eligibility traces with learning signals in spiking-network tasks. It motivates explicit trace/signal experiments; it is not generic reward-times-activity learning or proof of low-bit traces.

39. **C-R16.** Dettmers et al. (2022), [“8-bit Optimizers via Block-wise Quantization”](https://arxiv.org/abs/2110.02861), arXiv:2110.02861; ICLR 2022. The work reduces optimizer-state storage with block-wise quantization in evaluated training workloads. It supports measuring optimizer-memory savings, not equivalence with eligibility memory.

40. **C-R17.** Li, Chen, and Zhu (2023), [“Memory Efficient Optimizers with 4-bit States”](https://arxiv.org/abs/2309.01507), cited arXiv version 2309.01507; publication status not checked. The study quantizes first and second optimizer moments with tailored schemes. It is a four-bit optimizer-state precedent only; it does not test a recurrent credit trace.

41. **C-R18.** Xu et al. (2025), [“Pushing the Limits of Low-Bit Optimizers: A Focus on EMA Dynamics”](https://arxiv.org/abs/2505.00347v1), cited arXiv version 2505.00347v1; publication status not checked. SOLO studies 4/3/2-bit optimizer states and signal-swamping/noise trade-offs. The cited handoff explicitly reviewed v1; results concern optimizer moving averages, not a general low-bit learner.

42. **C-R19.** Ma et al. (2025), [“BitNet b1.58 2B4T Technical Report”](https://arxiv.org/abs/2504.12285), cited arXiv technical report version; Microsoft’s [official model card](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T) and [BF16 master-weight release](https://huggingface.co/microsoft/bitnet-b1.58-2B-4T-bf16). The report and card distinguish packed ternary serving weights from BF16 training/fine-tuning weights. “1.58-bit” therefore does not mean every training state or activation is stored at that rate.

43. **C-R20.** Gupta et al. (2015), [“Deep Learning with Limited Numerical Precision”](https://arxiv.org/abs/1502.02551), arXiv:1502.02551. The paper studies fixed-point training and emphasizes stochastic rounding, including 16-bit experiments. It is a rounding precedent, not evidence for two-bit eligibility traces.

44. **C-R21.** Shazeer and Stern (2018), [“Adafactor: Adaptive Learning Rates with Sublinear Memory Cost”](https://arxiv.org/abs/1804.04235), arXiv:1804.04235. Factored statistics reduce optimizer memory in tested neural-network training. The analogy motivates measured structure-aware compression; factorization is not automatically exact for arbitrary trace arrays.

45. **C-R22.** Hugging Face, [“GPU memory usage / Model memory anatomy”](https://huggingface.co/docs/transformers/en/model_memory_anatomy) and [“Cache strategies”](https://huggingface.co/docs/transformers/en/kv_cache), official Transformers documentation, accessed 26 September 2026. These pages distinguish parameters, gradients, optimizer state, activations and inference KV cache. They are implementation guidance, not scientific evidence for NSS’s particular runtime budget.

46. **C-R23.** Dettmers et al. (2023), [“QLoRA: Efficient Finetuning of Quantized LLMs”](https://arxiv.org/abs/2305.14314), arXiv:2305.14314. The method fine-tunes quantized models using trainable additions under its evaluated setup. It is relevant to generic Forge workflows; it does not authorize restoring NSS neural overlays or establish safe state migration.

## Verification and transfer boundary

The online check confirmed the identity and limited scope of the selected sources from publisher proceedings, primary journals, arXiv records, PubMed/PMC, eLife, and official project documentation. A small number of primary pages were inaccessible to this fetcher: the Science and Cell pages returned 403, and one PNAS DOI redirected to a cookie-required page. Those are recorded as access limits, not as evidence against the citation. No article was downloaded to the workspace, and no cited model, code, simulation, or benchmark was run.

For the Chat handoff, cite the biology as design inspiration and causal hypotheses, not as architectural authority. Keep exact source observations and prior failures outside model summaries. Preserve the numerical distinction between parameter count, neuron count, synapse count, synaptic state, model memory, and total training footprint. Keep human results separate from macaque and mouse results, and keep study-specific evidence separate from NSS’s own measured outcomes. `NETWORK_ACCESS.json` records the primary URLs, exact search queries, outcomes, and available retrieval-time precision for this verification pass.
