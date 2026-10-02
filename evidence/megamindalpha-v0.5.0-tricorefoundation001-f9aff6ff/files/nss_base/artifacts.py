"""Local manifest loading, byte hashing, and semantic qualification-fixture checks."""
from hashlib import sha256
from pathlib import Path

from .runtime import Catalog, Overlay, Profile, Transition, digest, fail
from .serialization import decode, read_json, validate


class Bundle:
    def __init__(self, manifest):
        self.root = Path(manifest).resolve().parent
        self.document = validate(read_json(manifest), "manifest.schema.json")
        d = self.document
        self.catalog = Catalog(d["core"]["sha256"], d["generation"], d["tokenizer"],
            d["context_abi"], d["overlay_abi"], d["runtime_version"],
            tuple(Overlay(o["id"], o["artifact"]["sha256"], tuple(o["requires"]), tuple(o["excludes"])) for o in d["overlays"]),
            tuple(Profile(p["id"], tuple(p["overlays"]), p["evidence_ref"]) for p in d["profiles"]),
            tuple(Transition(t["source"], t["destination"], t["state_reuse_policy"], t["evidence_ref"]) for t in d["transitions"]))
        profiles = {p["id"]: p for p in d["profiles"]}
        overlays = {o["id"]: o for o in d["overlays"]}
        for p in d["profiles"]:
            before = set()
            for name in p["overlays"]:
                if not set(overlays[name]["requires"]) <= before:
                    fail("INCOMPATIBLE_CONFIGURATION", "Dependencies must precede dependents in execution order")
                before.add(name)
        for t in d["transitions"]:
            replay = t["state_reuse_policy"] == "replay"
            if t["failure_destination"] != t["source"]:
                fail("VALIDATION_FAILED", "001A failure destination must retain source")
            if t["replay_required"] != replay or t["invalidate"] != (["cache", "draft"] if replay else []):
                fail("VALIDATION_FAILED", "Transition policy and invalidation disagree")
            if not replay and profiles[t["source"]]["overlays"] != profiles[t["destination"]]["overlays"]:
                fail("INCOMPATIBLE_CONFIGURATION", "Reuse requires identical ordered computation")
        self.verify()

    def artifact(self, descriptor, schema="operation.schema.json"):
        relative = Path(descriptor["path"])
        path = (self.root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(self.root):
            fail("VALIDATION_FAILED", "Artifact path escapes fixture root")
        try:
            raw = path.read_bytes()
        except OSError as e:
            fail("VALIDATION_FAILED", f"Artifact unavailable: {e}")
        if sha256(raw).hexdigest() != descriptor["sha256"]:
            fail("INCOMPATIBLE_CONFIGURATION", "Artifact bytes differ from manifest hash")
        try:
            return validate(decode(raw.decode("utf-8")), schema)
        except UnicodeError:
            fail("VALIDATION_FAILED", "Artifact is not UTF-8")

    def verify(self):
        self.artifact(self.document["core"])
        for overlay in self.document["overlays"]:
            self.artifact(overlay["artifact"])

    def ecid(self, profile_id):
        self.catalog.profile(profile_id)
        # Bind ordering and full declared contract as well as actual artifact hashes.
        return digest({"ecid_schema": "001A-1", "manifest": self.document,
                       "active_profile": profile_id})

    def edge(self, source, target):
        self.catalog.profile(source)
        self.catalog.profile(target)
        for t in self.document["transitions"]:
            if (t["source"], t["destination"]) == (source, target):
                return t
        fail("INCOMPATIBLE_CONFIGURATION", "No qualified directed transition")

    def operations(self, profile_id):
        p = self.catalog.profile(profile_id)
        overlays = {o["id"]: o for o in self.document["overlays"]}
        return [self.artifact(self.document["core"])] + [self.artifact(overlays[n]["artifact"]) for n in p.overlays]
