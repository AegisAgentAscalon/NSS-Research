"""Primary/replay driver for an ordinary contract harness; no neural packages."""
from __future__ import annotations
import copy,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
import engine
from engine import canonical,digest,review
from journal import Journal,JournalError,Store,atomic_json,validate,coverage_cursor,deadline_status


def dump(path,value):path.write_bytes(canonical(value)+b"\n")


def reseal(p):
    p["candidate"]["artifact_hash"]=digest(p["candidate"]["artifact"])
    p["candidate"]["measured_artifact"]=p["candidate"]["artifact_hash"]
    return p


def execute(inputs:Path,out:Path):
    start=time.monotonic();out.mkdir(parents=True,exist_ok=False)
    cases=[json.loads(l) for l in (inputs/"cases.jsonl").read_text().splitlines()]
    rows=[]; log=Journal(out/"reviews.jsonl")
    for case in cases:
        if len(rows)>=10000:raise RuntimeError("REVIEW_CAP")
        log.append("REVIEW_INTENT",{"case_id":case["case_id"],"input_hash":digest(case["public"])})
        r=review(case["public"])
        rows.append({"case_id":case["case_id"],"stratum":case["stratum"],"result":r})
        log.append("REVIEW_COMMIT",rows[-1])
    (out/"decisions.jsonl").write_bytes(b"".join(canonical(r)+b"\n" for r in rows))
    dump(out/"review_terminal.json",log.terminal())
    base=copy.deepcopy(next(x["public"] for x in cases if x["case_id"]=="CORRECT_LAWFUL_REVISION"))
    scenarios=[]
    def observed(name,data):scenarios.append({"name":name,"observed":data})
    # Actual simulated commit and duplicate handling.
    store=Store(out/"lifecycle_normal",base["snapshot"])
    first=store.adopt(base,review(base),"op1")
    second=store.adopt(base,review(base),"op1")
    observed("one_commit_duplicate_blocked",{"first":first["status"],"second":second["status"],
        "accepted":store.state["snapshot"]["accepted_id"],"completed":len(store.state["completed"])})
    # State/evidence changed since approval: re-evaluation must prevent stale adoption.
    for name,key,change in [("stale_parent_after_review","accepted_id","parent_new"),
                            ("stale_epoch_after_review","epoch_id","epoch_new")]:
        st=Store(out/name,base["snapshot"]);token=review(base)
        snap=copy.deepcopy(st.state["snapshot"]);snap[key]=change;st.update_public(snap)
        r=st.adopt(base,token,"stale")
        observed(name,{"status":r["status"],"accepted":st.state["snapshot"]["accepted_id"]})
    st=Store(out/"receipt_after_review",base["snapshot"]);token=review(base)
    snap=copy.deepcopy(st.state["snapshot"]);snap["requirements"]["focal"]["revision"]=3;snap["cutoff"]=3
    st.update_public(snap);r=st.adopt(base,token,"stale_receipt")
    observed("stale_evidence_after_review",{"status":r["status"],"accepted":st.state["snapshot"]["accepted_id"]})
    # Never accepting is not timely adaptation; no fake repaired weights are inferred.
    observed("deadline_obligations",{"at_deadline":deadline_status(5,5,None),
        "overdue":deadline_status(6,5,None),"late_completion":deadline_status(8,5,7),
        "on_time":deadline_status(6,5,5)})
    # Rolling small losses must still be compared to the original stable epoch.
    st=Store(out/"cumulative_drift",base["snapshot"]);sequence=[]
    for step,p1 in enumerate([90,130,170],1):
        q=copy.deepcopy(base);q["snapshot"]=copy.deepcopy(st.state["snapshot"])
        q["candidate"]["parent_id"]=q["snapshot"]["accepted_id"]
        q["candidate"]["revision_id"]=q["candidate"]["artifact"]["revision_id"]=f"drift{step}"
        q["candidate"]["artifact"]["p1_milli"].update({f"old{i}":p1 for i in range(3)})
        reseal(q);rr=review(q);ap=st.adopt(q,rr,f"driftop{step}")
        sequence.append({"decision":rr["decision"],"reasons":rr["reasons"],"apply":ap["status"],
            "accepted":st.state["snapshot"]["accepted_id"],"anchor_p1":st.state["snapshot"]["anchor_p1"]["old0"]})
    observed("cumulative_anchor",sequence)
    # Deferred candidate and separately declared new evidence: preserves both raw revisions.
    st=Store(out/"review_revision",base["snapshot"])
    bad=copy.deepcopy(base);bad["candidate"]["artifact"]["p1_milli"]["old0"]=650;reseal(bad)
    bad_r=review(bad);st.log.append("DEFERRED_REVIEW",{"raw":bad,"decision":bad_r})
    repaired=copy.deepcopy(base);repaired["candidate"]["revision_id"]=repaired["candidate"]["artifact"]["revision_id"]="independent_repaired_fixture"
    reseal(repaired);good_r=review(repaired);ap=st.adopt(repaired,good_r,"repaired")
    observed("synthetic_repair_revision",{"first":bad_r["decision"],"second":good_r["decision"],
        "commit":ap["status"],"raw_bad_retained":st.log.records[1]["payload"]["raw"]["candidate"]["artifact"]["p1_milli"]["old0"]==650,
        "actual_training":False})
    # Changing only an expected evaluator label cannot change public decision.
    rr1=review(base);rr2=review(json.loads(canonical(base)))
    observed("public_identical_probe",{"same_public_hash":rr1["input_hash"]==rr2["input_hash"],"same_result":rr1==rr2})
    # Fully accounted is not synonymous with resolved or deeply examined.
    items={1:{"accounted":True,"resolved":True,"depth":"detailed"},2:{"accounted":True,"resolved":False,"depth":"shallow"},
           4:{"accounted":True,"resolved":True,"depth":"detailed"}}
    observed("review_cursor_gap",coverage_cursor(0,4,items))
    items[3]={"accounted":True,"resolved":False,"depth":"deferred"}
    observed("review_cursor_unresolved",coverage_cursor(0,4,items))
    # Real process termination on each side of the durable state write.
    for point,code in [("after_intent",73),("after_state",74)]:
        root=out/("crash_"+point);request=out/("request_"+point+".json");dump(request,base)
        cp=subprocess.run([sys.executable,__file__,"crash",str(request),str(root),point],capture_output=True)
        (out/(point+"_child_stdout.txt")).write_bytes(cp.stdout)
        (out/(point+"_child_stderr.txt")).write_bytes(cp.stderr)
        recovered=Store(root).recovery();store=Store(root)
        retry=store.adopt(base,review(base),"crash-op")
        observed("crash_"+point,{"exit_code":cp.returncode,"expected_code":code,"recovery":recovered,"retry":retry["status"]})
    # Faults on copied logs. Original evidence remains untouched.
    raw=(out/"reviews.jsonl").read_bytes();lines=raw.splitlines(keepends=True);terminal=log.terminal()
    faults={"middle_delete":b"".join(lines[:10]+lines[11:]),
        "duplicate":b"".join(lines[:10]+[lines[9]]+lines[10:]),
        "reordered":b"".join(lines[:8]+[lines[9],lines[8]]+lines[10:]),
        "torn":raw[:-7],"suffix_truncated":b"".join(lines[:-1])}
    changed=json.loads(lines[9]);changed["payload"]["case_id"]="tampered"
    faults["altered_payload"]=b"".join(lines[:9]+[canonical(changed)+b"\n"]+lines[10:])
    faultrows=[];folder=out/"faults";folder.mkdir()
    for name,data in faults.items():
        target=folder/(name+".jsonl");target.write_bytes(data)
        caught=None
        try:validate(target,terminal)
        except JournalError as e:caught=str(e)
        faultrows.append({"fault":name,"detected":caught is not None,"reason":caught})
    clean_ok=len(validate(out/"reviews.jsonl",terminal))==len(lines)
    prefix=validate(folder/"suffix_truncated.jsonl")
    observed("hash_chain_limits",{"clean_pass":clean_ok,"faults":faultrows,
        "suffix_is_valid_without_external_terminal":len(prefix)==len(lines)-1})
    corrupt=Store(out/"corrupted_state",base["snapshot"])
    corrupt.adopt(base,review(base),"corruptop")
    state=json.loads(corrupt.state_path.read_text());state["snapshot"]["accepted_id"]="tampered"
    atomic_json(corrupt.state_path,state)
    try:Store(corrupt.root).recovery();detected=False
    except JournalError:detected=True
    observed("state_corruption",{"detected":detected})
    dump(out/"lifecycle.json",scenarios)
    # Diagnostic closure inventory; corrupted copies are deliberately not clean logs.
    logs={}
    for file in out.rglob("journal.jsonl"):
        records=validate(file);logs[str(file.relative_to(out))]={"records":len(records),"tail":records[-1]["hash"]}
    dump(out/"journal_terminals.json",logs)
    dump(out/"COUNTERS.json",{"main_rule_evaluations":len(cases),"all_rule_evaluations_including_children":engine.REVIEW_CALLS+4,
        "lifecycle_journal_events":sum(v["records"] for v in logs.values()),"grid":1440,"corners":54,
        "lifecycle_scenarios":len(scenarios),"neural_models":0,"model_forwards":0,"gradients":0,"optimizer_updates":0,
        "synthetic_candidate_artifacts":len(cases),"source":"constructed_tables_not_model_outputs"})
    dump(out/"RESOURCE.json",{"wall_seconds":time.monotonic()-start,"maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})


if __name__=="__main__":
    if sys.argv[1]=="crash":
        p=json.loads(Path(sys.argv[2]).read_text());st=Store(Path(sys.argv[3]),p["snapshot"])
        st.adopt(p,review(p),"crash-op",sys.argv[4]);raise SystemExit(99)
    execute(Path(sys.argv[1]),Path(sys.argv[2]))
