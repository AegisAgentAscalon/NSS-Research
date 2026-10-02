# NSS — Current Research Checklist
**Version 0.28 · 1 October 2026 (America/Detroit) · Running status ledger**

## Where we are — ELI5

**Goal:** A useful, controllable local companion, not a frontier/RSI program or mandatory tri-core system.

**Current phase:** Model quantization/compression. Training efficiency and post-learning repair remain later, separate phases.

**Question just tested:** Can the useful two-bit weights be stored more tightly without changing a single value or answer?

**Finding:** Yes. Huffman coding stores matrix codes at **1.79–1.83 bits/entry**, with complete matched files **4.46–5.53% smaller**. Every tested result stays exact. The simple decoder runs **7.56–8.23 times slower**, so it is not adopted. Whole-file compression saves about13% for archiving, not a demonstrated runtime-memory gain.

**Decision:** Keep direct Q2 as the default. Preserve this positive representation result and negative decoder result. A more efficient decoder is a possible later, bounded question—not an automatic experiment. Ternary remains the long-term candidate; two-bit is already the useful interim reference.

**On hold:** Training acceleration, further training-state compression, post-learning repair, CYCLE01-B, new English readers, HSA/segmented extensions, DARP, DIRECT01, malleable architectures and expanded integration.

**Publication:** A self-contained research package is prepared; no GitHub repository or license has been created/changed. Human rights/privacy review and independent reproduction remain outstanding.

## Priority queue
| Priority | Task | Status | ELI5 | Next action |
|---|---|---|---|---|
| 1 | LOW-BIT-MODEL | MODEL_QUANTIZATION_Q2_INTERIM_RETAINED_TERNARY_TARGET_OPEN | First get the model itself working well with the target few weight settings. | Retain direct Q2 as the useful interim runtime. Lossless HUF16 storage works but this decoder is not adopted. One later fixed-format decoder optimization may test whether table decoding or bounded block reuse removes the measured bottleneck; it is not automatically authorized. Training efficiency and repair remain deferred. |
| 0 | LB01-Q2-PACK | COMPLETE_LOSSLESS_STORAGE_GAIN_NO_RUNTIME_ADOPTION | Pack the same four weight settings with shorter labels, without changing the learner. Less storage works; the simple decoder costs too much time. | Retain direct Q2 as the useful interim runtime. Lossless HUF16 storage works but this decoder is not adopted. One later fixed-format decoder optimization may test whether table decoding or bounded block reuse removes the measured bottleneck; it is not automatically authorized. Training efficiency and repair remain deferred. |
| 0 | LB01-T3-TARGET | COMPLETE_BOUNDED_COMPARISON_NO_TERNARY_WORKING_POINT_Q2_RETAINED | Try switching four-setting weights to three settings immediately or gradually; see whether the small model still finishes its checklists correctly. | Retain two-bit as the useful interim model. Review the residual ternary representation/quality tradeoff; no automatic further fitting or ramp tuning. Any next model-only calibration or from-start ternary test needs a separately fixed protocol. Training efficiency and post-learning repair remain deferred until the user moves phases. |
| 0 | LB02-MASTER16 | COMPLETE_BOUNDED_SAME_TASK_CONTINUATION_MASTER_ARRAY_SAVING | Keep the useful two-bit learner practicing the same task while halving its matrix working copies; compare ordinary and stochastic rounding. | Retain this completed training-state precision result. It did not further reduce the two-bit inference representation. No follow-up until the training phase. |
| 0 | LB02-Q2-TRAIN | COMPLETE_LOGICAL_COMPARISON_MEMORY_GAIN_LEARNING_GATE_OPEN_OPERATIONAL_CAP_EXCEEDED | Teach a four-setting-weight model while storing smaller optimizer notes; check whether it can keep old work and learn something new. | Preserve the quantization/preparation and learning-array gains separately from the later repair findings. Reuse the prepared checkpoints; no automatic retention experiment or change to original gates. |
| later: training | LB02 | ON_HOLD_UNTIL_MODEL_QUANTIZATION_DECISION | Make training cheaper or faster after the model-quantization working point is established. | Hold further training efficiency studies. Preserve completed Q2_M8 and MASTER16 evidence. Resume only when the user moves into training research. |
| later: training | LB02-ACCUM | MASTER16_RESULT_RETAINED_FOLLOWUP_DEFERRED | Shrink the remaining wide working copies without losing the little updates that make learning possible. | Do not run the proposed earlier-preparation FP16-master comparison now. Revisit small-update accumulation in the later training phase. |
| conditional: model quantization | LB01-T2 | CONDITIONAL_TERNARY_PREPARATION_NOT_RUN | Can learning with ternary weights from the beginning avoid damage caused by rounding an already-trained model? | From-start ternary remains unrun. LB01-T3-TARGET tested immediate and gradual conversion of existing Q2 parents, not new ternary initialization. No automatic from-start experiment or training-optimization phase. |
| later: repair | LB02-RETENTION | ON_HOLD_SEPARATE_POST_LEARNING_REPAIR | Keep the two-bit model from forgetting old checklist details while it learns the corrected answer. | Hold; post-learning repair is separate from model quantization and later training-efficiency research. |
| 0 | LB01-TERNARY | COMPLETE_BOUNDED_DIAGNOSTIC_TERNARY_WORKING_POINT_NOT_ESTABLISHED | Shrink checklist weights to minus, zero and plus, then teach the learner to work with that restriction. Compact storage works; quality and training-memory goals remain open. | Preserve original result; ternary remainslong-termtarget,notdisprovenbyQ2results. Revisitonlyundernewdispatch. |
| parked | LB01-Q4 | PARKED_UNRUN_AFTER_USER_RESTORED_TERNARY_Q2_TARGET | Give weights more usable levels than ternary, then check whether the small model keeps its skills and can still learn. | Four-bit remains an optional comparison, not the current primary target. No four-bit scientific run occurred. |
| 0 | BRIDGE01 | COMPLETE_BOUNDED_DUMMY_PROTOTYPE_PARKED_FOR_LOW_BIT | Connect a pretend language model to a real small checklist network, saved records and an action checker; see whether work survives interruption. | Preserve runnable prototype, do not expand until low-bit priority is resolved or user directs otherwise. |
| 0 | LB01 | COMPLETE_FIRST_TERNARY_TRIAL_WORKING_POINT_OPEN | A three-choice weight format runs and shrinks storage; ternary-aware training restores much of the old skill but not reliable complete tasks. | Use LB01-TERNARY evidence; no claim that all learning state is low-bit. |
| conditional: model execution | LB03 | SCOPE_DEPENDENT_NOT_RUN | Measure an additional precision or execution improvement only after it addresses a specific need; no mandatory four-bit stage. | Only model representation/execution checks can belong to the current phase. Training-state and training-kernel optimization stay deferred; no automatic sweep. |
| 0 | MEM01 | COMPLETE_BOUNDED_HANDOFF_DIAGNOSTIC_READER_LIMITED | Save the work, restart later, and check that the right unfinished tasks and current facts survive. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| 0 | COMP01-A | COMPLETE_ENGINEERING_ONLY | Build the exam and check that its marking works before testing the companion. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| 0 | LAB01 | COMPLETE_BOUNDED_DIAGNOSTIC_REFERENCE_NOT_READY | Extend our own small reader so it can use simple evidence and corrections, then test it on unseen histories. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| 0 | LAB02-SIZE | COMPLETE_BOUNDED_DIAGNOSTIC_NO_CONSISTENT_WIDTH_GAIN | Give the same reader a little more room and see whether better answers justify the added cost. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| 0 | LAB02-BIND | COMPLETE_BOUNDED_DIAGNOSTIC_NO_CURRICULUM_GAIN | Teach the reader which fact belongs to which project and time before relying on it for memory. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| 0 | LAB-READER-DECISION | ROUTE_SELECTED_READER_PREPARATION_PARKED | Decide how to get an informative research reader without repeatedly training the same weak one. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| standing | LAB-SEMANTIC-REVIEW | NEW_CORPUS_REVIEW_COMPLETE_RETROSPECTIVE_REVIEW_PENDING | Check whether the exam is fair as well as whether each answer follows what the exam actually says. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| on hold | COMP01-B | ON_HOLD_PENDING_LOW_BIT_WORKING_POINT | Can an actual language model answer with the right page in front of it, then find that page in a notebook? | Hold. Resume only after low-bit decision or explicit owner reprioritization. |
| 0 | PREP01 | COMPLETE_BOUNDED_DIAGNOSTIC_WORKSHEET_TRADEOFF_NO_ADVANCE_GAIN | Try preparing a source-linked task sheet before questions arrive, then check whether that helps more than ordinary retrieval or making/caching the same sheet when asked. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| on hold | CYCLE01-B | ON_HOLD_PENDING_LOW_BIT_WORKING_POINT | Test whether learning keeps accumulating over several nights instead of proving only one successful update. | Hold. Resume only after low-bit decision or explicit owner reprioritization. |
| on hold | ADAPT01 | ON_HOLD_PENDING_LOW_BIT_WORKING_POINT | Try one way to make learning less disruptive without stopping useful learning. | Hold. Resume only after low-bit decision or explicit owner reprioritization. |
| umbrella | BUDGET01 | MODEL_QUANTIZATION_FOCUS_TRAINING_LATER | Make a useful learner fit the available memory and compute instead of shrinking numbers blindly. | Keep honest model storage, execution and preparation cost records. Do not optimize training speed or memory before the training phase. |
| on hold | INT01 | ON_HOLD_PENDING_LOW_BIT_WORKING_POINT | Combine only the pieces that actually make the companion better. | Hold. Resume only after low-bit decision or explicit owner reprioritization. |
| 0 | READER-SUPPORT01 | COMPLETE_BOUNDED_DIAGNOSTIC_NO_PRIMARY_GAIN_OUTPUT_CONTRACT_LIMIT | Teach one small reader which notes support its answer; compare it with answer-only practice and an ordinary question-aware index. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |
| 0 | CYCLE01-A | COMPLETE_DEVELOPMENT_FEASIBILITY_PROMISING_SIGNAL | Let a copy learn at night, check it, then use the accepted version and its unfinished work the next day. | Retain result and any unresolved limits. No follow-on outside low-bit unless explicitly authorized. |

## Previous research — original entries preserved
All59 earlier historical JSON entries remain unchanged; LB01-Q2-PACK is entry60. Historical next actions do not override the current scope.
| Task | Status | ELI5 | Result |
|---|---|---|---|
| Q001 | COMPLETED_DIAGNOSTIC | Can a tiny memory keep a symbol while distractions arrive? | Short tasks worked; long distraction exposed decay. Exact memory remained a strong control. |
| Q002 | COMPLETED_DIAGNOSTIC | Can addressed memory know both a value and when nothing is known? | Prepared/gated versions could retain records; short preparation and poorly calibrated admission failed. |
| Q003 | COMPLETED_MIXED | Can noisy memories be repaired without inventing missing ones? | Denoising improved known values but could destroy UNKNOWN. Simple exact controls were stronger. |
| Q004 | COMPLETED_MIXED | Can memory remain empty, then be written, corrected, cleared and rewritten? | Protected presence worked narrowly; neural alternatives retained failures. |
| Q005 | COMPLETED_NO_UNIQUE_GAIN | Should knowing that a memory exists be separate from its contents? | Separate presence lanes worked, but did not beat simple controls. |
| Q006 | COMPLETED_BOUNDED | Can a reader follow links through records with more thinking steps? | Structured readers followed longer clean chains with more rounds; noise broke binding. |
| Q007 | COMPLETED_MIXED | Can stored reference codes repair damaged records? | Registered records recovered; unfamiliar identities could be forced into false familiar answers. |
| Q008 | COMPLETED_GATE_FAILED | Can a gate reject unfamiliar identities without rejecting recoverable memories? | False acceptance fell, but valid known coverage suffered; joint gates failed. |
| Q009 | COMPLETED_BOUNDED_REFERENCE | Can almost-identical people or records be kept from overwriting each other? | Exact ownership worked; learned close-identity readers/binders remained weak. |
| Q010-ORIGINAL | REPORT_ONLY_ORIGINAL_PAYLOAD_GAP | Was the original broader qualification reproducible from retained evidence? | Original report remains historical; essential original training/code/checkpoint bytes were missing in the documented inventory. |
| Q010-RECOVERY-v1.6 | CLOSED_BOUNDED_RECOVERED_EVIDENCE | Can the recovered reference at least be evaluated at fixed weights? | Bounded reconstructed inference/state evidence accepted; close-identity and novel-query limitations remained. |
| CM01 | COMPLETED_BOUNDED | Can a small explicit reference packet help the reader identify the right record? | Reference assistance helped noisy cases; exact lookup stayed a strong control. |
| CM02 | COMPLETED_NO_FORMAT_ADVANTAGE | Is a little context packet better than an ordinary index with the same information? | Packet and index tied; retaining selection information mattered more than its format. |
| TS01 | COMPLETED_BOUNDED | Can a recurrent state track two checklists? | Yes on a narrow fixed-weight task with supplied routing/no-op handling; exact tracking also worked. |
| TS02-MW01 | COMPLETED_GATE_FAILED | Do small metadata tokens improve revision-aware progress tracking? | Some pooled gains, but reliability and stale/false-completion gates failed. |
| TS03-CR01 | COMPLETED_GATE_FAILED | Does a revised curriculum fix the workspace learner? | Coverage, interaction, reliability and final-advantage screens failed despite correct bindings in some cases. |
| CKA01 | RETAINED_DATA_ANALYSIS_COMPLETE | Did the task learner forget later, or never learn adequately? | Saved-checkpoint analysis found substantial fitting/transfer weakness, not an early-stop rescue. |
| DC01-v0.4 | TECHNICAL_PREFLIGHT_STOP | Can the delayed-feedback experiment fit its evidence budget? | Storage forecast stopped main work before learning evaluation. |
| DC01-v0.5 | COMPLETED_BOUNDED_REPORT_LEVEL | Can a correctly identified delayed signal teach a new association? | Bounded identified delayed updates worked; general temporal credit and total cost remain open. |
| REV01 | COMPLETED_TRADEOFF_GATE_FAILED | Does a stronger correction teach faster? | Faster first correction, but old-confidence damage and some old-label errors prevented complete qualification. |
| PROTECT01 | STOPPED_AT_DEVELOPMENT_ADMISSION | Can a projected update protect old answers while learning? | Projection had a development tradeoff; acquisition admission stopped held-out work. |
| REHEARSE01 | STOPPED_AT_DEVELOPMENT_ADMISSION | Can old-example practice repair damage from a strong correction? | Stopped at development admission; useful old-loss effects did not qualify the whole rule. |
| ANA-REHEARSE01 | RETAINED_DATA_ANALYSIS_COMPLETE | What do the saved rehearsal gradients and losses explain? | Retained-data analysis supported old/new competition; it did not run another repair policy. |
| TIMING01 | COMPLETED_TRADEOFF_GATE_FAILED | Should replay happen early or after later feedback? | Endpoints improved in many cases, but full-trajectory confidence requirements failed. |
| ANA-TIMING01 | RETAINED_DATA_ANALYSIS_COMPLETE | Did favorable endpoints hide damage during the update sequence? | Retained analysis preserved the original failures and exposed worse peaks. |
| MICROMACRO01 | COMPLETED_BOUNDED_CYCLE | Can one bounded learn-and-repair cycle retain a gain through later feedback? | A narrow cycle contract passed; stricter criteria failed. Not indefinite successive generations. |
| TEACH01 | COMPLETED_BOUNDED_REPORT_LEVEL | Does a stable teacher help when direct replay misses old examples? | Modest report-level benefit; complete old records and ordinary controls were strong. |
| C00-CONTRACT01 | COMPLETED_SOFTWARE_CONTRACT | Can the software safely review and record a proposed change? | Authored transaction/contract checks worked after a preserved bug fix; no neural reviewer tested. |
| EVAL01 | RETAINED_DATA_ANALYSIS_COMPLETE | Does stricter checking reject bad changes without rejecting too many useful ones? | Retrospective snapshots showed an admission/deferral tradeoff, not a universal evaluator winner. |
| STATEBRIDGE01 | COMPLETED_DIAGNOSTIC_UNQUALIFIED | Can unfinished internal state continue after weights change? | Initial reading could work while subsequent computation failed; numerical gate also failed. |
| SURFACE01 | STOP_BASELINE_COMPETENCE | Can we isolate which changed weights break old work? | Four parents trained; one false-DONE history stopped the planned surface comparison before B corrections. |
| TRACE01 | TECHNICAL_STOP_PARTIAL_CONFIRMATION | Can observed degradation guide what to rehearse? | Tracked onset; guided replay had mixed development tradeoffs. Numerical failure and storage stop left 3/32 confirmation contexts. |
| RECOVER01-v0.2 | COMPLETED_DIAGNOSTIC_STRONG_RECOVERY | Can ordinary replay recover old work after new learning? | Very large observed repair; corrected classes survived. Residual errors and strict numerical failure remain. |
| SH01 | COMPLETED_PARTIAL_COHORT | Does a hierarchy help a small maintenance reader? | HSA learned the bounded rule better than paired dense models; initial sparse execution was slower. One fit incomplete. |
| SH02 | WORKING_COMPONENT_PARKED | Can we clean the same hierarchy without changing its decisions? | Packed execution improved larger cases; small/batched costs and historical bitwise mismatch remain. |
| SC01 | WORKING_COMPONENT_PARKED | Can bounded segments track revisions and interrupted maintenance? | Exact integration worked; ordinary caching supplied most savings and some jobs were slower. |
| SC02 | WORKING_COMPONENT_PARKED | Can incremental work make the segmented implementation better? | Incremental publication/plans helped; intermediate neural caching was slower in all tested cells. |
| CAP01 | WORKING_COMPONENT_PARKED | Can the computation finish when all its evidence cannot fit at once? | Exact multipass attention extended input reach; ordinary streaming matched custom grouping. Larger-layout learned errors persisted. |
| CAP02 | BOUNDED_CLOSEOUT_PARKED_FOR_INTEGRATION | Can broader practice help use the expanded input reach without losing the small task? | Mixed-size preparation improved larger layouts and retained small-task skill; remaining errors preserved. |
| DARP01 | COMPLETED_OUTPUT_COMPETENCE_NOT_ESTABLISHED | Can segmented diffusion plan, check and repair maintenance output blocks? | Mechanism ran; initial writers were weak. Copying and missing replanning preparation limited comparison. |
| DARP02 | COMPLETED_PREPARATION_GAIN | Does better creation/edit/revision preparation help? | Large preparation gain; richer feedback had no broad advantage; natural errors remained hard to repair. |
| DARP03 | PARK_CURRENT_DARP_IMPLEMENTATION | Does learning from real mistakes give diffusion a clear advantage over AR? | Useful supported DARP approached AR, but no clear quality/speed win; more false completion and slower sample. |
| HSA-CONSOLIDATION | DOCUMENTATION_COMPLETE | Can we preserve the whole HSA/context record and its boundaries? | Six studies consolidated and evidence indexed; result remains a bounded component. |
| DARP-CONSOLIDATION | DOCUMENTATION_COMPLETE | Can we preserve DARP findings and a clear stop decision? | Three studies consolidated; viable supported alternative without established practical superiority or general equivalence. |
| EVIDENCE-LED-PLAN | PLAN_CURRENT | What should we do next without repeating old experiments? | Stepwise main path and conditional literature queue established. |
| DIRECT01-SPEC | DOCUMENTATION_COMPLETE_EXPERIMENT_NOT_RUN | Can we specify a fair direct-parallel versus AR output comparison? | Conditional protocol ready; no selected model, trained heads or execution. |
| COMP01-B-SETUP | ENGINEERING_ONLY_MODEL_ACQUISITION_BLOCKED | Choose a small test reader and wire it to the exam. | Official135M selected with a single conditional360M fallback. Model acquisition failed before inference;18 offline runner contract tests passed. |
| LAB01 | COMPLETE_BOUNDED_DIAGNOSTIC_REFERENCE_NOT_READY | Can our own small reader answer from simple English evidence without a pretrained download? | 3new92837parameterARfits;5400main+6preflightupdates. Familiar supported833/1536,withheld768/768,paraphrase251/768;nofamilypasses.21preflightgroups;5376recounts;384freshreplays;24checkpointhashes;48480sampledprecisionvaluesallpass. |
| LAB02-SIZE | COMPLETE_BOUNDED_DIAGNOSTIC_NO_CONSISTENT_WIDTH_GAIN | Giving the same reader about22%or47%more room did not consistently help it choose the right project/date record. | Nine fresh fits: supported whole answers833/1536,825/1536,844/1536; largest+0.72pp, wording31.12%→35.81%with mixed seed changes. No family working point.16,218total optimizer applications;40engineering groups;no main interruptions. |
| LAB02-BIND | COMPLETE_BOUNDED_DIAGNOSTIC_NO_CURRICULUM_GAIN | Give two identical readers the same exercises in different orders and check which learns to use the evidence better. | Six fresh paired readers; mixed757/1536(49.28%),staged734/1536(47.79%) supported answers. Staged lower in all3pairs. No family working point. Explicit new rules and full raw test/answer traces; finite-grammar review of9984outputs and manual64items/384responses. No old scores changed. |
| MEM01 | COMPLETE_BOUNDED_HANDOFF_DIAGNOSTIC_READER_LIMITED | Save unfinished work, reopen it with current records, and distinguish missing memories from a reader misunderstanding correct notes. | Frozen3LAB02-BINDmixed readers;3888responseobservations,0updates. DIRECT/FULL413/864post-break completeanswers,COMPACT504/864(+10.53pp);150gain/59loss;allthreeparentsgain. Wholefour-answerresume8/216allpolicies.1944recordchecks0loss;2592packetreplaysand432snapshotrestores exact. Current-status errors remain;ordinary scoped lookup supplies benefit,not newreaderlearning.23preflightgroups;3888recounts/fullreplays;41580sample precisionvaluespass. One audit-calltimeout, maincomplete; partialauditworkunknown. |
| PREP01 | COMPLETE_BOUNDED_DIAGNOSTIC_WORKSHEET_TRADEOFF_NO_ADVANCE_GAIN | Try preparing a source-linked task sheet before questions arrive, then check whether that helps more than ordinary retrieval or making/caching the same sheet when asked. | Three unchanged99674parameterreaders;5472main responses. RAW818/1368(59.80%) vsall3sheetpolicies790/1368(57.75%);all3readersdecline,163gains191losses. Falsecompletion54→14butdone-worksuggestions330→384. Identicalsheetqualitybefore/afterquery;ADVANCEslowerthanCACHEinall9timingmedians,highreuseratio1.043. Exposedgold-supportdiagnostic41/72→58/72(mainlystatus22/36→36/36,work19/36→22/36);notdeployable.0updates.5472main+288diagnosticrecounts,5472freshreplays,576restores,73920sampleprecisionvaluespass.21preflightgroupsafterpreservedcopybug;postresultaudittypemismatchcorrectedseparately. |
| READER-SUPPORT01 | COMPLETE_BOUNDED_DIAGNOSTIC_NO_PRIMARY_GAIN_OUTPUT_CONTRACT_LIMIT | Teach one small reader which notes support its answer; compare it with answer-only practice and an ordinary question-aware index. | Six fresh106615parameter readers; A answer-only vs S answer+source loss. Supported five-field A586/1536(38.15%),S521/1536(33.92%); no primary gain, parent differences−11.91/−3.91/+3.13pp. A keepsall, S exactsupport808/1536 but answers287/808ofthosecorrect. PublicLOOKUPA769/1536,S692/1536; retrospective namedstatusfactAlookup768/768 is notcompletehandoff. Positivecompletion136→89,done-worksuggestions235→341; wholefouranswers0→9/384. Publicstatusancillaryfieldscopeunderspecified; rawkeyandsynonym/reviewkeptseparate.29952recounts,576freshreplays,42912sampleprecisionvaluespass,30maincheckpointsverified.9600logicalmain;9808–9809actualmain+12preflight afterrecorded208steptailreplay. No follow-up fitting. |
| CYCLE01-A | COMPLETE_DEVELOPMENT_FEASIBILITY_PROMISING_SIGNAL | Let a copy learn at night, check it, then use the accepted version and its unfinished work the next day. | Four source parents, two nights, FIXED/LEARN/REPLAY/BALANCED.2048development+7disposableupdates;0newfits. Balanced5/8adoptions,allfourend32/32currentcueanswers,4087/4096guardanswers,2046/2048liveanswers,30/32entiretwo-dayhistories,0livefalseDONE.Only4103acceptedbothnights. ExtraBexposureconfounded;allmaterialdevelopment.232savedoutputsreplayedexact,160checkpointfilesverified;9,304,960evaluationnumericcomparisons0violationsinnewfloat64contract. Onecallerinterruption,resume32missingupdatesatprovenphasebarrier,0repeatedupdates;discardedinference/time/RSSunknown. |
| BRIDGE01 | COMPLETE_BOUNDED_DUMMY_PROTOTYPE_PARKED_FOR_LOW_BIT | Connect a pretend language model to a real small checklist network, saved records and an action checker; see whether work survives interruption. | 216scripted sessions,3474simulatedeffects,558rejections,0contractviolations;4144/4144learnednext-itemobservations. Exactrulealsocompletesall.41preflightchecks;216freshreplays;302512NumPy/Torchfloat64scalars0violations.0training/downloads/realLLMinference. Main6.331score99.15MBRSS; notcompletebill. Overallcapscheckedposthoc,roundcapenforced. |
| LB01-TERNARY | COMPLETE_BOUNDED_DIAGNOSTIC_TERNARY_WORKING_POINT_NOT_ESTABLISHED | Shrink checklist weights to minus, zero and plus, then teach the learner to work with that restriction. Compact storage works; quality and training-memory goals remain open. | Four exact18249parameterparents; matrices17856ternary,biases393FP32. Directconversion6361/32768(19.41%),QAT51231615/32768(96.48%),610/1024whole,342falseDONE;FPparent32733/32768. Workingpoint0/4. All8oldcueclassesretained;64jointnewcuephasefailsflipinbothFLOATandTERNARY. Packednumeric6717bytesvs72996FP32;five-tritcodes~1.6bits,scales/biasesextra. ScalarpackedC~5xslower;FP32master/grad/Adam292008bytesbeforeactivations,notlowmemorytraining.4608main+6preflight=4614actualupdates,norepeats.24preflightchecks,200recounts/replays,40checkpoints,20packedexports,79907552evaluationnumericalscalarcomparisons0violations. Nootherresearchreopened. |
| LB02-Q2-TRAIN | COMPLETE_LOGICAL_COMPARISON_MEMORY_GAIN_LEARNING_GATE_OPEN_OPERATIONAL_CAP_EXCEEDED | Teach a four-setting-weight model while storing smaller optimizer notes; check whether it can keep old work and learn something new. | Four exact18,249parameterparents;Q2four-codeaffinematricesandcustom8bitmomentstorage. After1024preparation:Q2M8 32766/32768answers,1022/1024whole,1falseDONE;Q2M32 32765,1022whole,1falseDONE;F32 32763,1023whole,0falseDONE. AfterB64+AB32 all12pathsretain32/32currentcueclasses/arm;Q2M8oldwork32521/32768(99.246%),952whole,11falseDONE;Q2M3232607,959whole,19falseDONE;F3232540,941whole,16falseDONE. Q2preparationworking3/4peroptimizer,fulllearningQ2M8only1/4;compressedqualityequivalencenotqualified. Master+gradient+momentarrays291984→183650bytes(-37.10%),moments145992→37658(-74.21%);wideactivations/copiesremain. PackedQ2numeric8001bytes/file8703;scalarC2.50–2.64xslower,compressedtrainingdescriptively3.55%slowerthanQ2M32. 13440logicalmain,13645–13647actualmain+43preflight=13688–13690;205–207replayedafter2callerinterruptions,originalactualcapNOTmet. 264outputarrays/1019904Aobservationsrecountedandfreshreplayedexact;72checkpoints,48packedexports,72Bchecks,3fixturefilesbyteexact;main166323200numericcomparisons0violations. NoBitNetTransformer,fromscratchfits,all2bittraining,deployedorwholeNSSqualification. |
| LB02-MASTER16 | COMPLETE_BOUNDED_SAME_TASK_CONTINUATION_MASTER_ARRAY_SAVING | Keep the useful two-bit learner practicing the same task while halving its matrix working copies; compare ordinary and stochastic rounding. | Four exact LB02 Q2_M8 preparation parents; 12x256 same-task updates, no new cue or repair. M32 final32764/32768 (1022whole,0falseDONE),M16nearest32767 (1023whole,0FD),M16stochastic32766 (1022whole,1FD). BothM16 pass NEW practical continuation/storage screen4/4; not retroactive oldgate pass. All3arms8192/8192stress and32/32originalB. Master+gradient+moment arrays183650→147938bytes (-19.45%); actualbatch saved-tensor union broader2.534MB→2.499MB (~1.41%), not19.45%wholememory. FP16nearest rounds93.72%of proposedupdates away,SR89.84%; near-mastered startingpoint, no newskill/plasticity qualification. Descriptivecores+6.69%/+11.08%;nospeedclaim.3072main+18preflight=3090updates;12backwardmemoryprobes,noauditupdates;no interruptions.84rawarrays264192suffixscoresrecounted/all84freshreplays exact,108checkpoints,3fixturefilesexact;63912960numericcomparisons0breaches. |
| LB01-T3-TARGET | COMPLETE_BOUNDED_COMPARISON_NO_TERNARY_WORKING_POINT_Q2_RETAINED | Try switching four-setting weights to three settings immediately or gradually; see whether the small model still finishes its checklists correctly. | Four exact prepared Q2_M32 parents; 12x1024 same-task QAT, all original associations unchanged. Q2 final32764/32768,1023/1024whole,0FD; immediateT3 32283/32768(98.52%),863whole,65FD; gradualT3 32108(97.99%),774whole,211FD. Ternary working0/4 each; Q2 nominal4/4, strict long-stress2/4 despite99.99%answers/253of256whole. T3 stresswhole94/256direct,53/256ramp. Ramp mixed early,513pure updates vs1024direct; not a universal comparison of all gradual methods. ActualpackedT3 body6717B/file7604B vsQ2 8001/8703;FP32scales/biases,FP64inference.12300actualupdates(12288main+12preflight),nointerruptions/repeats.168arrays522240suffixanswersfullfreshreplayexact,52exports72checkpoints,3fixturesbyteexact,106006400numericcomparisons0breaches. No training-efficiency or post-learning-repair study. |
| LB01-Q2-PACK | COMPLETE_LOSSLESS_STORAGE_GAIN_NO_RUNTIME_ADOPTION | Pack the same four weight settings with shorter labels, without changing the learner. Less storage works; the simple decoder costs too much time. | Four exact Q2_CONTROL1024 exports; RAW/HUF16/DEF16 fixed 16-row blocks, no learning. Huffman codes1.7890–1.8297bits/entry versus2; matched files8137/8088/8046/8058B versus8517B (4.46–5.53% saving); all12canonical models exact. HUF16 7.56–8.23x slower, not adopted. DEF16 saves0.31–0.74%, adds7168B zlib allocations. Whole legacy-file zlib12.59–12.92% smaller, archive-only. All36rawarrays245856scoredobservations independently recounted/replayed exact;12snapshot restores48badbindings rejected. Primary32764/32768 andlong49147/49152 retained, including old failures.11preflightgroups,37mainlock objects intact,476sourcepayloads verified. No newfit/update. Extra public-wrapper reproduction interrupted in4104; missing inference finished separately, partial outputs exact; primary main/audit uninterrupted. Eight illustrative indices allmixed despite protocolexpectation, disclosed without changingindices. Current result is code-storage compression, not ternary arithmetic, universal speed/RAM/20B scaling. |

## Standing evaluation and continuity rules
A completed feasibility is not a confirmed lifecycle. Keep adopted learning, deferred learning and old-task retention separate; preserve historical failed gates.
Update this ledger and regenerate Markdown after each authorized research step. Preserve immutable versioned snapshots and link latest via NSS_Research_Checklist_CURRENT.*. No scheduled or background updates implied. Include review coverage and public-answer-support findings. Never turn a policy/documentation update into a completed experiment.

The exact tests and raw answers remain linked. Finite-rule/scorer checks are distinct from semantic review, and author review is not independent replication. No background work is implied.

## Optional tasks and returns — preserved
```json
[
  {
    "id": "DIRECT01",
    "priority": "optional after COMP01",
    "status": "SPEC_READY_CONDITIONAL_NOT_RUN",
    "eli5": "Can the model write a whole structured block at once instead of one field at a time?",
    "next_action": "Train matched new AR and parallel heads only when a capable shared representation and output question are bound.",
    "sources": [
      "CODEX",
      "DIRECT"
    ],
    "dependency": "COMP01 competence or separately authorized mechanism-only route"
  },
  {
    "id": "BALANCE01",
    "priority": "optional before/within CYCLE01",
    "status": "PROPOSAL_ONLY_NOT_RUN",
    "eli5": "While rehearsing old skills, also practice the new correct answer, possibly with gentler updates.",
    "next_action": "Use the original bounded comparison or explicitly adapt it into CYCLE01; do not do both just to duplicate evidence.",
    "sources": [
      "BALANCE",
      "PLAN"
    ],
    "dependency": null
  },
  {
    "id": "SURFACE01-FACTORIAL",
    "priority": "conditional diagnostic",
    "status": "NOT_RUN_AFTER_BASELINE_STOP",
    "eli5": "Which part of a weight update breaks an unfinished task: the reader or the state updater?",
    "next_action": "Reopen only when update location is decision-relevant; the original parent admission stopped the comparison.",
    "sources": [
      "SURFACE",
      "PLAN"
    ],
    "dependency": null
  },
  {
    "id": "NUM-STATEBRIDGE-RECOVER",
    "priority": "conditional prerequisite",
    "status": "OPEN_HISTORICAL_GATE_FAILURE",
    "eli5": "Do two implementations agree well enough to trust this old learning path?",
    "next_action": "Diagnose exposed cases and prospectively justify verification before qualifying reused paths; do not erase old failures.",
    "sources": [
      "HISTORY",
      "RECOVER",
      "PLAN"
    ],
    "dependency": null
  },
  {
    "id": "RET-MW01-FIT-001",
    "priority": "parked return",
    "status": "OPEN_PARKED",
    "eli5": "Why did the older workspace learner fail to learn and transfer its task?",
    "next_action": "Revisit only for a named dependency or the foundation checkpoint.",
    "sources": [
      "HISTORY",
      "PLAN"
    ],
    "dependency": null
  },
  {
    "id": "FCR-0103-001",
    "priority": "after NBR-03 / before NBR-04",
    "status": "REQUIRED_RETURN_NOT_YET_DUE",
    "eli5": "Review what the foundation still needs before moving to the next major research area.",
    "next_action": "Preserve the named checkpoint and explicitly defer nonblocking old issues; not a demand for perfect old prototypes.",
    "sources": [
      "HISTORY",
      "PLAN"
    ],
    "dependency": null
  }
]
```

## Later literature leads — preserved
```json
[
  {
    "lead": "Computation-preserving recurrent updates",
    "when": "ADAPT01 first lead",
    "eli5": "Protect useful old computations while allowing new ones. Distinct from PROTECT01 output-margin projection."
  },
  {
    "lead": "OML / meta-experience replay",
    "when": "Conditional after measured adaptation weakness",
    "eli5": "Prepare representations to learn later with less interference; charge the preparation."
  },
  {
    "lead": "Plasticity renewal",
    "when": "Conditional on loss of future learnability",
    "eli5": "Refresh capacity only if it actually becomes harder to learn; protect rare skills."
  },
  {
    "lead": "RIM / compositional state",
    "when": "Conditional on state interference or binding failures",
    "eli5": "Keep separate concerns in interacting state parts, not a restored tri-core."
  },
  {
    "lead": "Differentiable plasticity / Backpropamine",
    "when": "Separate later update-rule lane",
    "eli5": "Learn how adaptation responds to experience; define temporary versus accepted changes."
  },
  {
    "lead": "TTT / Titans adaptive working memory",
    "when": "Separate later state-contract lane",
    "eli5": "Test a learnable working-memory mechanism without renaming hidden daytime weight updates."
  },
  {
    "lead": "Griffin / Mamba / dense-local attention",
    "when": "COMP01 feasibility or BUDGET01",
    "eli5": "Choose an adequate prepared language backbone if efficiency is blocking; do not assume memory reliability."
  },
  {
    "lead": "Adafactor / low-bit optimizer states",
    "when": "BUDGET01 when optimizer memory matters",
    "eli5": "Reduce a measured storage burden, not every value indiscriminately."
  },
  {
    "lead": "Eligibility traces / e-prop / G08-G12",
    "when": "Scoped learning-rule and precision lane",
    "eli5": "Identify past activity deserving a later update; test float behavior before compression."
  },
  {
    "lead": "Learned optimizers",
    "when": "Later after repeatable repair tasks",
    "eli5": "Test learned update policies against strong conventional optimization."
  },
  {
    "lead": "Net2Net / structural growth",
    "when": "Conditional on capacity bottleneck",
    "eli5": "Add bounded capacity while preserving initial function; then test specialization and continuation."
  },
  {
    "lead": "HyperNetworks / KAN-style functions",
    "when": "Theoretical shelf",
    "eli5": "Investigate a concrete representation limitation, not flexible-looking machinery for its own sake."
  },
  {
    "lead": "Generative replay / distillation / self-play / world models",
    "when": "Later, after relevant foundation return",
    "eli5": "Test useful generated practice against exact replay and extra-compute controls; generated history is not evidence."
  },
  {
    "lead": "Biological inspiration / appraisal / multimodal bridges",
    "when": "Later function-specific hypotheses",
    "eli5": "Tie each idea to a useful companion behavior; affect is not fact or permission."
  }
]
```
