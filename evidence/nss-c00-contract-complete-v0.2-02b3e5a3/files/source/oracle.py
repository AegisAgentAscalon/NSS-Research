"""Independent reference: declarative requirement tables, no production imports."""
import hashlib,json


def h(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()


def reference(pub):
    def result(d,r,metrics=None):
        return {"decision":d,"reasons":sorted(set(r)),"input_hash":h(pub),
                "metrics":metrics or {},"review_version":"C00_RULE_V2"}
    try:
        st=pub["snapshot"]; cand=pub["candidate"]; policy=pub["policy"]
        if any(type(policy[k])!=int or not 0<=policy[k]<=1000 for k in ("min_focal","min_old","parent_drop","epoch_drop")):
            return result("REJECT",["BAD_POLICY"])
        if any(type(v)!=int or v<0 for v in (pub["tick"],cand["deadline"])):
            return result("REJECT",["BAD_CLOCK"])
        if any(type(cand[k])!=bool for k in ("permitted","authority_valid","state_compatible","pending_trace")):
            return result("REJECT",["BAD_BOOLEAN_FIELD"])
        checks=[(cand["domain"]=="parameter_candidate","WRONG_DOMAIN"),
                (bool(cand["permitted"]),"NO_PERMISSION"),
                (cand["evidence_origin"]=="verified_fixture","UNSUPPORTED_ORIGIN"),
                (bool(cand["authority_valid"]),"INVALID_AUTHORITY"),
                (h(cand["artifact"])==cand["artifact_hash"],"ARTIFACT_HASH"),
                (cand["measured_artifact"]==cand["artifact_hash"],"MEASUREMENT_BINDING"),
                (cand["revision_id"]==cand["artifact"]["revision_id"],"CANDIDATE_ID")]
        probs=cand["artifact"]["p1_milli"]; specs=st["requirements"]
        checks += [(type(v)==int and 0<=v<=1000,"BAD_PROBABILITY") for v in probs.values()]
        checks += [(type(v["target"])==int and v["target"] in (0,1),"BAD_TARGET") for v in specs.values()]
        failed=[name for ok,name in checks if not ok]
        if failed:return result("REJECT",failed)
        ready=[(cand["parent_id"]==st["accepted_id"],"STALE_PARENT"),
            (cand["epoch_id"]==st["epoch_id"],"STALE_EPOCH"),
            (cand["schema_id"]==st["schema_id"],"SCHEMA_MISMATCH"),
            (cand["completion"]=="committed","UNKNOWN_COMPLETION"),
            (cand["state_compatible"] is True,"STATE_UNRESOLVED"),
            (cand["pending_trace"] is False,"PENDING_TRACE"),
            (cand["receipt_cutoff"]<=st["cutoff"],"FUTURE_EVIDENCE"),
            (set(probs)==set(specs),"INCOMPLETE_PANEL"),
            (set(cand["receipt_revisions"])==set(specs),"RECEIPT_COVERAGE")]
        for key,value in specs.items():
            ready.extend([(cand["receipt_revisions"].get(key)==value["revision"],"STALE_RECEIPT"),
                          (value["released_at"]<=st["cutoff"],"UNRELEASED_TARGET")])
            if value["kind"]=="old":
                ready.append((value["revision"]==st["epoch_target_revisions"].get(key),"REQUALIFICATION_REQUIRED"))
        failed=[name for ok,name in ready if not ok]
        if failed:return result("DEFER",failed)
        observed={}; clauses=[]
        # Enumerate the two possible labels by lookup, rather than producer helper.
        for key,r in specs.items():
            score=(1000-probs[key],probs[key])[r["target"]]
            cls=int(probs[key]>500)
            obs={"prob_milli":score,"class_correct":cls==r["target"]}
            if r["kind"]=="old":
                par=(1000-st["parent_p1"][key],st["parent_p1"][key])[r["target"]]
                anc=(1000-st["anchor_p1"][key],st["anchor_p1"][key])[r["target"]]
                obs.update(parent_drop=par-score,epoch_drop=anc-score)
                clauses.extend([(cls==r["target"],"OLD_CLASS"),
                    (score>=policy["min_old"],"OLD_FLOOR"),
                    (score>=par-policy["parent_drop"],"PARENT_BUDGET"),
                    (score>=anc-policy["epoch_drop"],"EPOCH_BUDGET")])
            else:
                clauses.extend([(cls==r["target"],"FOCAL_CLASS"),(score>=policy["min_focal"],"FOCAL_FLOOR")])
            observed[key]=obs
        failed=[name for ok,name in clauses if not ok]
        return result("DEFER" if failed else "ADOPT_ELIGIBLE",failed or ["CONTRACT_SATISFIED"],
            {"late":pub["tick"]>cand["deadline"],"by_capability":observed})
    except (KeyError,TypeError,AttributeError,ValueError):
        return result("REJECT",["MALFORMED_RECORD"])
