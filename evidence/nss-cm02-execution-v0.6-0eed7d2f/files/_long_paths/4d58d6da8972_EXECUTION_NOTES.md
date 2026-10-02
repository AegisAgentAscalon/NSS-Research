# CM-02 execution specification v0.3

User execution authorization: “Okay, let's do it.” This accepts the reviewed v0.2 scientific design and its X_latest control. The new execution version records implementation completions before any generated stimulus; the historical proposal is retained verbatim.

Execution specification v0.3 pins the byte-level/public message representation below before generation; it does not change v0.2 sequence counts, noise, targets, policies, seeds or criteria.

Prelude activation includes a public two-entry task/scope registry of opaque IDs. Both slots start U at activation; earlier state is empty. This registry supplies no record binding or answer. W retains exactly two ASCII packets; I two immutable tuples.

Each registration exposes its allocated physical row, as required for the public-key-to-row map. Codebook/resolver catalogue is public numerical scaffolding, unchanged at deletion. It is not hidden identity evidence.

The six semantic tuple fields are (1, scope, handle, revision, binding_event, operation); U reserves four zero fields, H uses scope/nonzero conflict event with zero handle/revision. R requires all reference fields nonzero. H encodings are narrower than the general CM01 codec but represent this protocol's conflict state exactly.

Selection/correction/conflict closes the previously current binding in the historical binding archive. No W shadow latest-selection table is retained. Queries are read-only; revision/deletion never rewrites W/I entries.

X_latest has an explicitly costed historical revision index to check consecutive observed revisions; W/I do not retain that extra index. All arms retain the specified original public history and current record archive; X_S reconstructs them afresh from its observed prefix.

The worker receives a begin message, one committed event at a time, and one current query. Only the coordinator can read future public files; generator/scorer alone read templates/seeds/intent. Worker file-audit hooks block new raw/protocol and producer/scorer access except its own forward-attempt write receipt.

One controller trajectory is captured per sequence and read by all five fixed near seeds. Repeating model seeds is not repeating independent trajectories. I/W numerical requirements are equal; a full input/model identity cache avoids shared physical forwards. Cache memory is audit machinery, separately counted.

Cache keys include dtype/shape/bytes for K,V,valid,Q,book,active,symbols, stage 0 and the frozen model hash; exact replay starts an empty worker, controller state and cache.

Inference uses CPU float32, one stage, one request per physical forward. All original resolver thresholds and the retained amended pointer-math verifier remain unchanged. Source import of historical training definitions for hash checks never invokes a training procedure.

Queries rotate W/I/O ordering by global public query ordinal. Timing is separately recorded and excluded from exact semantic replay. No best timing selection or cross-arm cache-hit speedup claim is permitted.

Resident memory is the unique Python object graph rooted at the controller, query and one near model, with tensor storage counted once. Shared object aliases are traversed once; separate component inventories are never summed. Canonical JSON inventory sizes, numerical array bytes, 26-byte semantic-field lower bounds and 56-byte packet rewrites are reported separately.

Initial activation and every event are charged; event telemetry records map writes, tuple/string allocations, packet encode/decode, archive bytes and row updates. Query telemetry adds all indexed reads, exact payload traffic, scan visits, reconstruction peak and experimental cache size. Python object counts describe this implementation, not a deployment-level compression theorem.

Eighteen deterministic toy contract methods precede source lock. No random CM02 stimulus or model forward is used in these tests. Fixture and main generation must follow this lock. All unexpected gate failures stop the study with evidence retained.

The global attempted-forward ledger is claimed before each model call and refuses a 6001st attempt; all fixture/main/replay calls share it. Baseline verifier arithmetic replay is not a learned-model forward and is reported separately.

No Q010 weight change, optimizer update, new neural interface or native recurrent-state experiment is authorized or executed by this protocol.
