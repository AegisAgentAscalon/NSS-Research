# Concrete acceptance cases

| Stimulus | Expected observation |
|---|---|
| Known exact fixture label | Selects the single matching released profile and emits no permit |
| Unknown or labels split across two profiles | CAPABILITY_UNAVAILABLE, no implicit union |
| Two tied acceptable profiles | NEEDS_CLARIFICATION unless the current profile is tied for best |
| Same-profile selection | No load units; unchanged weights do not permit old stage-cache reuse |
| CORE missing or B-only added to current family descriptor | Registration rejected |
| Old epoch, changed generation, unregistered descriptor or corrupted size | Selection/admission rejected |
| Current child/source permission withdrawn | New selection/read/handoff blocked; history remains inspectable |
| Unfinished source or unqualified AB->CORE/A->AB edge | Source task/ticket unchanged; no transition synthesized |
| AB->A with missing speed unit | Exact source supplies m/s; facts/assumptions/receipts retained |
| Original source disagrees or omits required property | Conflict/clarification outcome, no guessed completion |
| Control/evaluation request | Only CORE eligible; selected artifact set contains core only |
| New managed stage while another is open or generation publication while busy | RECOVERY_REQUIRED |
| Source record hash, task id, pairs, owner path, descriptor or ticket substituted | Rejected before publication |
| Finish/close/cancel with omitted or uncertain effect receipts | Blocked until explicit reconciliation |
| Explicit cancel after withdrawal | Record/reason/verified receipts preserved; no new execution |
| Crash before/after START, FINISH, MOVE, CLOSE or CANCEL commit | Old state or one complete committed state; exact retry is idempotent history |
| Old command replayed after generation epoch changes | Historical receipt only; current pointer/ticket does not change |
| Raw journal edit or semantically forged task event | Audit/reducer fails closed |
| Live selected-profile artifacts used in toy forward pass | Cache identity changes on handoff; rebuilt A equals fresh A under fixed backend |

Tests are specifications of local software behavior. They are not proof of safe
untrusted tools, learned semantic routing, general neural composition or native paging.
