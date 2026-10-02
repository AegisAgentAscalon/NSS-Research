from .runtime import Catalog, Overlay, Profile, Transition, State, transition, action_disposition

def example():
    return Catalog("synthetic-core-hash", "gen-1", "tok-1", "ctx-1", "ov-1", "sim-1",
        (Overlay("A", "synthetic-A-hash"), Overlay("B", "synthetic-B-hash", ("A",))),
        (Profile("core", (), "fixture:core"), Profile("A", ("A",), "fixture:A"),
         Profile("AB", ("A", "B"), "fixture:AB")),
        (Transition("AB", "A", "replay", "fixture:AB-to-A"),
         Transition("A", "core", "replay", "fixture:A-to-core"),
         Transition("A", "A", "reuse", "fixture:A-reuse")))

def main():
    c = example()
    s = State("demo-task", "AB", c.ecid("AB"), ("fixture:original-input",),
              ("stale-cache",), "unfinished output", ("mock-write-1",))
    result = transition(c, s, "A", authorized=True)
    print("Synthetic contract simulation; qualification evidence is fixture metadata.")
    print("Status:", result.status, "Replay required:", result.replay_required)
    print("Cache cleared:", not result.state.cache, "Draft cleared:", not result.state.draft)
    print("Previously committed action:", action_disposition(result.state, "mock-write-1"))

if __name__ == "__main__":
    main()
