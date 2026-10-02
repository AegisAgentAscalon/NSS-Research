"""Fixed synthetic engineering inputs. No model-generated data or RNG."""
from __future__ import annotations
import copy, hashlib, itertools, json
from pathlib import Path


def hash_obj(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()


def seal(public):
    c=public["candidate"];c["artifact_hash"]=hash_obj(c["artifact"]);c["measured_artifact"]=c["artifact_hash"]
    return public


def base():
    requirements={f"old{i}":{"kind":"old","target":0,"revision":1,"released_at":1} for i in range(3)}
    requirements["focal"]={"kind":"focal","target":1,"revision":2,"released_at":2}
    s={"accepted_id":"parent0","epoch_id":"epoch0","schema_id":"schema0","cutoff":2,
       "requirements":requirements,"epoch_target_revisions":{f"old{i}":1 for i in range(3)},
       "parent_p1":{**{f"old{i}":50 for i in range(3)},"focal":50},
       "anchor_p1":{f"old{i}":50 for i in range(3)}}
    c={"domain":"parameter_candidate","revision_id":"candidate0","parent_id":"parent0",
       "epoch_id":"epoch0","schema_id":"schema0","completion":"committed",
       "evidence_origin":"verified_fixture","authority_valid":True,"permitted":True,
       "state_compatible":True,"pending_trace":False,"receipt_cutoff":2,"deadline":5,
       "receipt_revisions":{**{f"old{i}":1 for i in range(3)},"focal":2},
       "artifact":{"revision_id":"candidate0","p1_milli":{**{f"old{i}":50 for i in range(3)},"focal":950}}}
    return seal({"snapshot":s,"candidate":c,"policy":{"min_focal":850,"min_old":600,"parent_drop":50,"epoch_drop":100},"tick":3})


def write_inputs(dest:Path):
    dest.mkdir(parents=True,exist_ok=True)
    cases=[]
    grid=itertools.product([0,50,100],[50,100],[600,850,950],[-25,0,25,75,150],[0,50],[0,1],[0,1],["committed","unknown"])
    for n,(pd,ed,fq,drop,gap,oy,fy,completion) in enumerate(grid):
        p=base();s,c=p["snapshot"],p["candidate"]
        p["policy"].update(parent_drop=pd,epoch_drop=ed)
        for i in range(3):
            key=f"old{i}"; s["requirements"][key]["target"]=oy
            s["anchor_p1"][key]=950 if oy else 50
            s["parent_p1"][key]=(950-gap) if oy else (50+gap)
            q=950-gap-drop; c["artifact"]["p1_milli"][key]=q if oy else 1000-q
        s["requirements"]["focal"]["target"]=fy
        s["parent_p1"]["focal"]=50 if fy else 950  # obsolete focal class must be allowed to change
        c["artifact"]["p1_milli"]["focal"]=fq if fy else 1000-fq
        c["completion"]=completion
        c["revision_id"]=c["artifact"]["revision_id"]=f"grid-candidate-{n:04d}"
        cases.append({"case_id":f"GRID-{n:04d}","stratum":"factorial_contract","public":seal(p)})
    assert len(cases)==1440
    corners=[]
    def add(name, mutate, reseal=True):
        p=base(); mutate(p)
        if reseal: seal(p)
        corners.append({"case_id":name,"stratum":"literal_corner","public":p})
    add("CORRECT_LAWFUL_REVISION",lambda p:None)
    add("LENIENT_ACCEPTABLE_DROP",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=90))
    add("PER_RECORD_NOT_AVERAGE",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=250,old1=0,old2=0))
    add("FOCAL_ALREADY_GOOD_BUT_OLD_WRONG",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=650))
    add("NO_NEW_LEARNING",lambda p:p["candidate"]["artifact"]["p1_milli"].update(focal=50))
    add("FOCAL_EQUAL_THRESHOLD",lambda p:p["candidate"]["artifact"]["p1_milli"].update(focal=850))
    add("FOCAL_BELOW_THRESHOLD",lambda p:p["candidate"]["artifact"]["p1_milli"].update(focal=849))
    add("PARENT_EQUAL_BOUNDARY",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=100))
    add("PARENT_OVER_BOUNDARY",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=101))
    def epoch(p,over=0):
        p["snapshot"]["parent_p1"]["old0"]=100;p["candidate"]["artifact"]["p1_milli"]["old0"]=150+over
        p["policy"]["parent_drop"]=100
    add("EPOCH_EQUAL_BOUNDARY",lambda p:epoch(p))
    add("EPOCH_OVER_BOUNDARY",lambda p:epoch(p,1))
    def tie(p,y):
        p["snapshot"]["requirements"]["old0"]["target"]=y
        p["candidate"]["artifact"]["p1_milli"]["old0"]=500
        p["policy"].update(min_old=500,parent_drop=1000,epoch_drop=1000)
    add("CLASS_TIE_TARGET_ZERO",lambda p:tie(p,0));add("CLASS_TIE_TARGET_ONE",lambda p:tie(p,1))
    add("UNKNOWN_UPDATE",lambda p:p["candidate"].update(completion="unknown"))
    add("STALE_PARENT",lambda p:p["candidate"].update(parent_id="obsolete"))
    add("STALE_EPOCH",lambda p:p["candidate"].update(epoch_id="obsolete"))
    add("STATE_SCHEMA",lambda p:p["candidate"].update(schema_id="other"))
    add("NO_STATE_MIGRATION",lambda p:p["candidate"].update(state_compatible=False))
    add("PENDING_CREDIT",lambda p:p["candidate"].update(pending_trace=True))
    add("NO_PERMISSION",lambda p:p["candidate"].update(permitted=False))
    add("BAD_AUTHORITY",lambda p:p["candidate"].update(authority_valid=False))
    add("HYPOTHESIS_AS_OBSERVATION",lambda p:p["candidate"].update(evidence_origin="dream_hypothesis"))
    add("UNSUPPORTED_STATE_DOMAIN",lambda p:p["candidate"].update(domain="state_repair"))
    add("FUTURE_RECEIPT",lambda p:p["candidate"].update(receipt_cutoff=3))
    add("REQUIRED_TARGET_NOT_RELEASED",lambda p:p["snapshot"]["requirements"]["focal"].update(released_at=3))
    add("STALE_TARGET_REVISION",lambda p:p["candidate"]["receipt_revisions"].update(focal=1))
    add("OLD_TARGET_CHANGED",lambda p:p["snapshot"]["requirements"]["old0"].update(revision=2))
    add("MISSING_PANEL_ITEM",lambda p:p["candidate"]["artifact"]["p1_milli"].pop("old0"))
    add("EXTRA_UNDECLARED_MEASUREMENT",lambda p:p["candidate"]["artifact"]["p1_milli"].update(extra=950))
    add("MISSING_RECEIPT",lambda p:p["candidate"]["receipt_revisions"].pop("old0"))
    add("BAD_ARTIFACT_HASH",lambda p:p["candidate"].update(artifact_hash="0"*64),False)
    add("MEASUREMENT_WRONG_ARTIFACT",lambda p:p["candidate"].update(measured_artifact="1"*64),False)
    add("WRONG_CANDIDATE_ID",lambda p:p["candidate"].update(revision_id="wrong"))
    add("OUT_OF_RANGE_PROBABILITY",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=1001))
    add("NON_INTEGER_PROBABILITY",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=50.0))
    add("BOOL_IS_NOT_PROBABILITY",lambda p:p["candidate"]["artifact"]["p1_milli"].update(old0=True))
    add("BAD_TARGET",lambda p:p["snapshot"]["requirements"]["old0"].update(target=2))
    add("MISSING_FIELD",lambda p:p["candidate"].pop("domain"))
    add("BAD_POLICY",lambda p:p["policy"].update(min_old=-1))
    add("BOOL_POLICY",lambda p:p["policy"].update(parent_drop=True))
    add("NEGATIVE_CLOCK",lambda p:p.update(tick=-1))
    add("FLOAT_CLOCK",lambda p:p.update(tick=1.5))
    add("ON_DEADLINE",lambda p:p.update(tick=5))
    add("PAST_DEADLINE_STILL_REVIEWABLE",lambda p:p.update(tick=6))
    for field,value,name in [
        ("permitted","false","TEXT_FALSE_PERMISSION"),
        ("authority_valid","false","TEXT_FALSE_AUTHORITY"),
        ("permitted",1,"INTEGER_PERMISSION"),
        ("authority_valid",1,"INTEGER_AUTHORITY"),
        ("state_compatible",1,"INTEGER_COMPATIBILITY"),
        ("state_compatible","true","TEXT_COMPATIBILITY"),
        ("pending_trace",0,"INTEGER_PENDING"),
        ("pending_trace","","TEXT_PENDING"),
        ("permitted",None,"NULL_PERMISSION"),
        ("authority_valid",[],"LIST_AUTHORITY")]:
        add(name,lambda p,field=field,value=value:p["candidate"].update({field:value}))
    assert len(corners)==54
    cases+=corners
    with (dest/"cases.jsonl").open("w") as f:
        for x in cases:f.write(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n")
    overlays=[{"pair_id":"INVISIBLE-CAPABILITY", "case_id":"CORRECT_LAWFUL_REVISION",
        "public_hash":hash_obj(corners[0]["public"]),"hidden_extra_capability":state,
        "full_scope_acceptable":ok} for state,ok in [("unchanged",True),("broken",False)]]
    (dest/"private_overlays.json").write_text(json.dumps(overlays,indent=2)+"\n")
    (dest/"INVENTORY.json").write_text(json.dumps({"grid":1440,"corners":54,"total":1494,
        "identical_public_opposite_full_scope_pairs":1,"origin":"AUTHOR_CONSTRUCTED_SYNTHETIC_CONTRACT_FIXTURES",
        "rng_draws":0},indent=2)+"\n")


if __name__=="__main__":
    import sys
    write_inputs(Path(sys.argv[1]))
