"""Canonical hash-chained append log plus simulated adoption; no neural state."""
from __future__ import annotations
import copy
import hashlib
import json
import os
from pathlib import Path
from engine import canonical, digest, review


class JournalError(RuntimeError):
    pass


class Journal:
    def __init__(self, path: Path):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.records=[]
        if self.path.exists():
            self.records=validate(self.path)
        self.tail=self.records[-1]["hash"] if self.records else "0"*64

    def append(self, kind: str, payload: dict):
        body={"seq":len(self.records)+1,"prev":self.tail,"kind":kind,"payload":payload}
        rec={**body,"hash":digest(body)}
        with self.path.open("ab") as f:
            f.write(canonical(rec)+b"\n"); f.flush(); os.fsync(f.fileno())
        self.records.append(rec); self.tail=rec["hash"]
        return rec

    def terminal(self):
        return {"records":len(self.records),"tail":self.tail}


def validate(path: Path, terminal: dict|None=None):
    out=[]; prev="0"*64
    with Path(path).open("rb") as f:
        for line in f:
            if not line.endswith(b"\n"): raise JournalError("TORN_RECORD")
            try: rec=json.loads(line)
            except (json.JSONDecodeError,UnicodeDecodeError) as e: raise JournalError("BAD_JSON") from e
            if set(rec)!={"seq","prev","kind","payload","hash"}: raise JournalError("BAD_RECORD")
            if rec["seq"]!=len(out)+1 or rec["prev"]!=prev: raise JournalError("CHAIN_GAP")
            body={k:v for k,v in rec.items() if k!="hash"}
            if digest(body)!=rec["hash"]: raise JournalError("HASH_MISMATCH")
            out.append(rec); prev=rec["hash"]
    if terminal is not None and (len(out)!=terminal["records"] or prev!=terminal["tail"]):
        raise JournalError("TERMINAL_MISMATCH")
    return out


def atomic_json(path: Path, value: dict):
    path=Path(path); temp=path.with_suffix(path.suffix+".tmp")
    with temp.open("wb") as f:
        f.write(canonical(value)+b"\n");f.flush();os.fsync(f.fileno())
    os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


class Store:
    def __init__(self, root: Path, initial: dict|None=None):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.state_path=self.root/"state.json"
        self.log=Journal(self.root/"journal.jsonl")
        if not self.state_path.exists():
            if initial is None: raise JournalError("NO_STATE")
            atomic_json(self.state_path, {"snapshot":initial,"completed":[]})
            self.log.append("INITIALIZE",{"accepted_id":initial["accepted_id"],"snapshot_hash":digest(initial),"state_hash":digest({"snapshot":initial,"completed":[]})})
        self.state=json.loads(self.state_path.read_bytes())

    def update_public(self,snapshot: dict):
        self.state["snapshot"]=copy.deepcopy(snapshot)
        atomic_json(self.state_path,self.state)
        self.log.append("PUBLIC_VERSION",{"snapshot_hash":digest(snapshot),"state_hash":digest(self.state)})

    def recovery(self):
        intents={}; commits=set()
        for r in self.log.records:
            if r["kind"]=="ADOPTION_INTENT": intents[r["payload"]["operation_id"]]=r
            if r["kind"]=="ADOPTION_COMMIT": commits.add(r["payload"]["operation_id"])
        pending=sorted(set(intents)-commits)
        stable=[r["payload"]["state_hash"] for r in self.log.records if "state_hash" in r["payload"]]
        if not pending and stable and stable[-1] != digest(self.state):
            raise JournalError("STATE_HASH_MISMATCH")
        return {"status":"UNKNOWN_COMPLETION" if pending else "CLEAN", "pending":pending,
                "accepted_id":self.state["snapshot"]["accepted_id"],
                "applied_markers":self.state["completed"]}

    def adopt(self, public:dict, token:dict, operation_id:str, crash_at:str|None=None):
        if self.recovery()["pending"]:
            self.log.append("ADOPTION_BLOCKED",{"operation_id":operation_id,"reason":"UNKNOWN_COMPLETION"})
            return {"status":"BLOCKED_UNKNOWN"}
        if operation_id in self.state["completed"]:
            self.log.append("DUPLICATE_REJECTED",{"operation_id":operation_id})
            return {"status":"DUPLICATE"}
        # Re-evaluate against currently accepted public evidence, never trust the old token alone.
        current=copy.deepcopy(public);current["snapshot"]=self.state["snapshot"]
        current_review=review(current)
        if token!=current_review or current_review["decision"]!="ADOPT_ELIGIBLE":
            self.log.append("ADOPTION_BLOCKED",{"operation_id":operation_id,"reason":"RECHECK_FAILED",
                "current_decision":current_review})
            return {"status":"BLOCKED_RECHECK","current_decision":current_review}
        cand=current["candidate"]
        self.log.append("ADOPTION_INTENT",{"operation_id":operation_id,"candidate_id":cand["revision_id"],
            "before":digest(self.state),"review_hash":digest(current_review),"artifact_hash":cand["artifact_hash"]})
        if crash_at=="after_intent": os._exit(73)
        after=copy.deepcopy(self.state)
        after["snapshot"]["accepted_id"]=cand["revision_id"]
        after["snapshot"]["parent_p1"]=cand["artifact"]["p1_milli"]
        after["completed"].append(operation_id)
        atomic_json(self.state_path,after); self.state=after
        if crash_at=="after_state": os._exit(74)
        self.log.append("ADOPTION_COMMIT",{"operation_id":operation_id,"accepted_id":cand["revision_id"],
            "after":digest(after),"state_hash":digest(after),"late":current_review["metrics"].get("late",False)})
        return {"status":"COMMITTED","accepted_id":cand["revision_id"],"late":current_review["metrics"].get("late",False)}


def coverage_cursor(previous:int, cutoff:int, items:dict[int,dict]):
    cursor=previous
    for i in range(previous+1,cutoff+1):
        if i not in items or not items[i].get("accounted",False): break
        cursor=i
    unresolved=[i for i in range(previous+1,cutoff+1) if i in items and not items[i].get("resolved",False)]
    return {"accounted_through":cursor,"unresolved":unresolved,
            "missing":[i for i in range(previous+1,cutoff+1) if i not in items],
            "depth":{str(i):v.get("depth","none") for i,v in items.items() if previous<i<=cutoff}}


def deadline_status(now:int, deadline:int, completed_at:int|None):
    if completed_at is None: return "PENDING" if now<=deadline else "OVERDUE"
    return "ON_TIME" if completed_at<=deadline else "COMPLETED_LATE"
