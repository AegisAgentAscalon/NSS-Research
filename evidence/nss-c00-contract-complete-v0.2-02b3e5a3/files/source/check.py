"""Independent retained-evidence check; imports reference only, never production code."""
from __future__ import annotations
import collections,csv,hashlib,json,sys
from pathlib import Path
from oracle import reference


def c(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def h(x):return hashlib.sha256(c(x)).hexdigest()
def dump(p,x):p.write_bytes(c(x)+b"\n")


def read_chain(path,terminal=None):
    out=[];previous="0"*64
    for i,raw in enumerate(path.read_bytes().splitlines(keepends=True),1):
        assert raw.endswith(b"\n"),"torn"
        r=json.loads(raw);assert r["seq"]==i and r["prev"]==previous
        assert r["hash"]==h({k:r[k] for k in ("seq","prev","kind","payload")})
        out.append(r);previous=r["hash"]
    if terminal:assert len(out)==terminal["records"] and previous==terminal["tail"]
    return out


def main(inputs,run,out):
    out.mkdir(parents=True,exist_ok=False)
    cases=[json.loads(l) for l in (inputs/"cases.jsonl").read_text().splitlines()]
    decisions=[json.loads(l) for l in (run/"decisions.jsonl").read_text().splitlines()]
    assert len(cases)==len(decisions)==1494
    counts=collections.Counter();reason_counts=collections.Counter(); rows=[]; mismatches=[]
    expected={};byid={}
    for case,row in zip(cases,decisions,strict=True):
        assert case["case_id"]==row["case_id"]
        exp=reference(case["public"]);expected[case["case_id"]]=exp;byid[case["case_id"]]=row
        if row["result"]!=exp:mismatches.append({"case_id":case["case_id"],"expected":exp,"actual":row["result"]})
        counts[exp["decision"]]+=1;reason_counts.update(exp["reasons"])
        rows.append({"case_id":case["case_id"],"stratum":case["stratum"],"expected":exp["decision"],
            "actual":row["result"]["decision"],"match":row["result"]==exp,
            "reasons":"|".join(exp["reasons"]),"focal_probability":exp["metrics"].get("by_capability",{}).get("focal",{}).get("prob_milli"),
            "late":exp["metrics"].get("late",False)})
    dump(out/"MISMATCHES.json",mismatches)
    assert not mismatches,"DECISION_ORACLE_MISMATCH"
    adversarial = [r for r in rows if r["case_id"] in {
        "TEXT_FALSE_PERMISSION","TEXT_FALSE_AUTHORITY","INTEGER_PERMISSION","INTEGER_AUTHORITY",
        "INTEGER_COMPATIBILITY","TEXT_COMPATIBILITY","INTEGER_PENDING","TEXT_PENDING","NULL_PERMISSION","LIST_AUTHORITY"}]
    assert len(adversarial)==10 and all(r["actual"]=="REJECT" and r["reasons"]=="BAD_BOOLEAN_FIELD" for r in adversarial)
    journal=read_chain(run/"reviews.jsonl",json.loads((run/"review_terminal.json").read_text()))
    assert len(journal)==2*len(cases)
    for i,(case,row) in enumerate(zip(cases,decisions,strict=True)):
        intent,commit=journal[2*i:2*i+2]
        assert intent["kind"]=="REVIEW_INTENT" and commit["kind"]=="REVIEW_COMMIT"
        assert intent["payload"]=={"case_id":case["case_id"],"input_hash":h(case["public"])}
        assert commit["payload"]==row
    obs={r["name"]:r["observed"] for r in json.loads((run/"lifecycle.json").read_text())}
    checks={}
    def chk(name,condition):
        checks[name]=bool(condition)
        assert condition,name
    a=obs["one_commit_duplicate_blocked"]
    chk("commit_then_duplicate",a=={"first":"COMMITTED","second":"DUPLICATE","accepted":"candidate0","completed":1})
    chk("stale_parent_recheck",obs["stale_parent_after_review"]=={"status":"BLOCKED_RECHECK","accepted":"parent_new"})
    chk("stale_epoch_recheck",obs["stale_epoch_after_review"]=={"status":"BLOCKED_RECHECK","accepted":"parent0"})
    chk("stale_receipt_recheck",obs["stale_evidence_after_review"]=={"status":"BLOCKED_RECHECK","accepted":"parent0"})
    chk("deadline_report",obs["deadline_obligations"]=={"at_deadline":"PENDING","overdue":"OVERDUE","late_completion":"COMPLETED_LATE","on_time":"ON_TIME"})
    q=obs["cumulative_anchor"]
    chk("drift_first_two",[r["decision"] for r in q]==["ADOPT_ELIGIBLE","ADOPT_ELIGIBLE","DEFER"])
    chk("drift_not_reset",all(r["anchor_p1"]==50 for r in q) and q[-1]["accepted"]=="drift2" and q[-1]["reasons"]==["EPOCH_BUDGET"])
    q=obs["synthetic_repair_revision"]
    chk("defer_then_new_fixture",q=={"first":"DEFER","second":"ADOPT_ELIGIBLE","commit":"COMMITTED","raw_bad_retained":True,"actual_training":False})
    chk("public_pair",obs["public_identical_probe"]=={"same_public_hash":True,"same_result":True})
    q=obs["review_cursor_gap"]
    chk("cursor_no_gap_jump",q["accounted_through"]==2 and q["missing"]==[3] and q["unresolved"]==[2])
    q=obs["review_cursor_unresolved"]
    chk("accounted_not_resolved",q["accounted_through"]==4 and q["missing"]==[] and q["unresolved"]==[2,3])
    for point,code,accepted in [("after_intent",73,"parent0"),("after_state",74,"candidate0")]:
        q=obs["crash_"+point];root=run/("crash_"+point)
        records=read_chain(root/"journal.jsonl");state=json.loads((root/"state.json").read_text())
        chk("child_exit_"+point,q["exit_code"]==code)
        chk("unknown_not_retried_"+point,q["recovery"]["status"]=="UNKNOWN_COMPLETION" and q["retry"]=="BLOCKED_UNKNOWN")
        chk("crash_commit_count_"+point,sum(r["kind"]=="ADOPTION_COMMIT" for r in records)==0 and sum(r["kind"]=="ADOPTION_INTENT" for r in records)==1)
        chk("crash_actual_state_"+point,state["snapshot"]["accepted_id"]==accepted==q["recovery"]["accepted_id"])
    q=obs["hash_chain_limits"]
    chk("clean_chain",q["clean_pass"])
    chk("detected_six_copy_faults",len(q["faults"])==6 and all(r["detected"] for r in q["faults"]))
    independent_faults=[]
    terminal=json.loads((run/"review_terminal.json").read_text())
    for p in sorted((run/"faults").glob("*.jsonl")):
        try:read_chain(p,terminal);caught=False
        except (AssertionError,ValueError,KeyError):caught=True
        independent_faults.append(caught)
    chk("independent_fault_rejection",len(independent_faults)==6 and all(independent_faults))
    prefix=read_chain(run/"faults/suffix_truncated.jsonl")
    chk("terminal_anchor_needed",len(prefix)==terminal["records"]-1 and q["suffix_is_valid_without_external_terminal"])
    root=run/"corrupted_state";state=json.loads((root/"state.json").read_text());records=read_chain(root/"journal.jsonl")
    last=[r["payload"]["state_hash"] for r in records if "state_hash"in r["payload"]][-1]
    chk("state_corruption_detected",h(state)!=last and obs["state_corruption"]["detected"])
    for path,terminal in json.loads((run/"journal_terminals.json").read_text()).items():
        read_chain(run/path,terminal)
    overlays=json.loads((inputs/"private_overlays.json").read_text())
    assert len(overlays)==2 and overlays[0]["public_hash"]==overlays[1]["public_hash"]
    actions=[byid[r["case_id"]]["result"]["decision"]=="ADOPT_ELIGIBLE" for r in overlays]
    hidden_errors=sum(a != r["full_scope_acceptable"] for a,r in zip(actions,overlays,strict=True))
    chk("invisible_harm_not_resolved",hidden_errors==1 and actions==[True,True])
    # Controls have identical fixed proposal observations, not reconstructed neural trajectories.
    behavioral={"OLD_CLASS","OLD_FLOOR","PARENT_BUDGET","EPOCH_BUDGET","FOCAL_CLASS","FOCAL_FLOOR"}
    behavior_deferrals=sum(bool(set(e["reasons"])&behavioral) for e in expected.values())
    unresolved=sum(e["decision"]=="DEFER" and not(set(e["reasons"])&behavioral) for e in expected.values())
    controls=[{"policy":"CONTRACT_RULE","eligible_missed":0,"behavioral_violations_adopted":0,"integrity_rejections_adopted":0,"unresolved_adopted":0},
        {"policy":"ACCEPT_ALL","eligible_missed":0,"behavioral_violations_adopted":behavior_deferrals,"integrity_rejections_adopted":counts["REJECT"],"unresolved_adopted":unresolved},
        {"policy":"NEVER_ADOPT","eligible_missed":counts["ADOPT_ELIGIBLE"],"behavioral_violations_adopted":0,"integrity_rejections_adopted":0,"unresolved_adopted":0}]
    def table(name,rr):
        with (out/name).open("w",newline="")as f:
            w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
    table("DECISIONS.csv",rows);table("CONTROLS.csv",controls)
    table("REASONS.csv",[{"reason":k,"count":v}for k,v in sorted(reason_counts.items())])
    table("CONFORMANCE.csv",[{"check":k,"passed":v}for k,v in checks.items()])
    table("NON_ADOPTED_CASES.csv",[r for r in rows if r["actual"]!="ADOPT_ELIGIBLE"])
    summary={"scope":"SYNTHETIC_CONTRACT_CONFORMANCE_NOT_LEARNED_REVIEW","cases":len(cases),"dispositions":dict(counts),
        "exact_decision_reason_metric_matches":len(rows)-len(mismatches),"lifecycle_independent_assertions":len(checks),
        "lifecycle_scenarios":len(obs),"behavioral_deferrals":behavior_deferrals,"unresolved_deferrals":unresolved,
        "hidden_extra_capability_pair":{"public_identical":True,"same_decision":True,"full_scope_misses":hidden_errors,"cases":2},
        "model_forwards":0,"optimizer_updates":0,"fit_or_holdout_claim":False,"controls":controls}
    dump(out/"SUMMARY.json",summary)
    print(json.dumps(summary,indent=2))


if __name__=="__main__":main(*map(Path,sys.argv[1:4]))
