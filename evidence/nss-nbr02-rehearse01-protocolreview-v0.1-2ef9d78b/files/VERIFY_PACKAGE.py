#!/usr/bin/env python3
"""Verify documentation bytes and symbolic workload; never import scientific source."""
from pathlib import Path
import hashlib, json, sys

def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/"MANIFEST.json").read_text())
    failures=[];checks=0
    def check(ok,label):
        nonlocal checks
        checks+=1
        if not ok:failures.append(label)
    for item in manifest["files"]:
        p=root/item["path"]
        check(p.is_file() and p.stat().st_size==item["bytes"] and
              hashlib.sha256(p.read_bytes()).hexdigest()==item["sha256"], "payload:"+item["path"])
    ledger=json.loads((root/"WORK_LEDGER.json").read_text())
    p=ledger["one_pass"];full=ledger["capture_plus_full_adaptive_replay"];caps=ledger["caps_global"]
    check(sum(ledger["applications_by_phase_per_pass"].values())==3068,"phase-applications")
    check(800+96*(2+4*4+2)+2*(10+2*20)+12*20+8==3068,"independent-application-expansion")
    check(p["contexts"]==96+4+12==112,"contexts")
    check(ledger["context"]["all_prefixes"]==18+16+180+60==274,"context-prefixes")
    for key in p:check(full[key]==2*p[key],"full-adaptive-replay:"+key)
    check(p["regular_online_applications"]==800+20+112*18==2836,"ordinary-applications")
    check(p["batch_applications"]==112*2+8==232,"batch-applications")
    check(p["parameter_applications"]==p["regular_online_applications"]+p["batch_applications"],"application-types")
    check(p["gradient_examples_including_derivative_fixtures"]==2836+232*8+8==4700,"gradient-examples")
    check(p["g_backwards"]==p["l_gradient_examples"]==2350,"gradient-methods")
    check(p["three_event_prefixes"]==112*274+800+128+20+16+8+64+8==31732,"independent-prefix-expansion")
    check(p["cells"]==3*31732+2*2*(0+8+32)*21==98556,"cells-and-delays")
    check(p["heads"]==31732,"heads")
    check(p["rehearsal_example_retrievals"]==8*232==1856,"replay-retrievals")
    check(p["exact_control_query_rows"]==(12+6+2)*60==1200,"exact-control-rows")
    for key in ("parameter_applications","cells","heads","g_backwards","l_gradient_examples"):
        check(full[key]<=caps[key],"cap:"+key)
    check(9400*2696==25342400,"gradient-byte-component")
    check(464*5392==2501888,"accumulator-byte-component")
    check(6136*2696==16542656,"post-state-byte-component")
    check(63464*256==16246784,"hidden-trajectory-byte-component")
    seeds=json.loads((root/"SEEDS.json").read_text())
    rows=seeds["allocations"]
    check(len(rows)==33 and len({r["seed_uint64"] for r in rows})==33,"seed-count-unique")
    check(all(r["seed_uint64"]==int.from_bytes(hashlib.sha256(
          ("NSS-NBR02-REHEARSE01-REVIEW-v0.1/"+r["label"]).encode("ascii")).digest()[:8],"big")
          for r in rows),"seed-derivation-only")
    status=json.loads((root/"STATUS.json").read_text())
    check(status["state"]=="PROPOSED_NOT_DISPATCHED","proposal-not-execution")
    for key in ("models_loaded","gradient_calculations","parameter_updates","new_task_or_label_draws","new_numerical_fixtures","scientific_replays"):
        check(status[key]==0,"no-execution:"+key)
    # Scope checks; not mathematical/empirical validation of the proposed learner.
    text=" ".join((root/"PROTOCOL.md").read_text().split())
    for term in ("H=0","POST_EXTRA","PRE_EXTRA","CONTROL_SATURATION","B1","N_G/N_L","extra computation",
                 "3/4","6,136","FCR-0103-001","not a discovered optimal threshold","No QP"):
        check(term in text,"required-boundary:"+term)
    audit=json.loads((root/"audit/SOURCE_AUDIT.json").read_text())
    check([a["direct_payloads_hashed"] for a in audit["archives"]]==[10,183,44],"source-audit-scope")
    check(len(audit["archives"][1]["logical_paths_not_restored"])==2,"logical-restoration-not-claimed")
    check(audit["scientific_execution"] is False,"source-audit-not-replication")
    result={"status":"PASS" if not failures else "FAIL","checks":checks,
            "manifest_payloads":len(manifest["files"]),"failures":failures,
            "scope":"document identity and static arithmetic only; zero scientific execution"}
    print(json.dumps(result,indent=2))
    return 0 if not failures else 1
if __name__=="__main__":raise SystemExit(main())
