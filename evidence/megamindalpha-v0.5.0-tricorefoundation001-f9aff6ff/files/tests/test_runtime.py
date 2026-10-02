import unittest
from dataclasses import replace
from nss_base.demo import example
from nss_base.runtime import State, Profile, Overlay, Transition, ContractError, transition, action_disposition

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.c = example()
        self.s = State("t", "AB", self.c.ecid("AB"), ("original-input",), ("cache",), "draft", ("write-1",))

    def test_core_only_required(self):
        with self.assertRaises(ContractError):
            replace(self.c, profiles=self.c.profiles[1:])

    def test_dependency_closure(self):
        with self.assertRaises(ContractError):
            replace(self.c, profiles=self.c.profiles + (Profile("B", ("B",), "test"),))

    def test_exclusion(self):
        with self.assertRaises(ContractError):
            replace(self.c, overlays=(Overlay("A", "a", excludes=("B",)), self.c.overlays[1]))

    def test_unknown_profile(self):
        self.assertEqual(transition(self.c, self.s, "B", authorized=True).status, "INCOMPATIBLE_CONFIGURATION")

    def test_transition_is_directed(self):
        s = replace(self.s, profile="A", ecid=self.c.ecid("A"))
        self.assertEqual(transition(self.c, s, "AB", authorized=True).status, "INCOMPATIBLE_CONFIGURATION")

    def test_reject_reuse_across_weights(self):
        with self.assertRaises(ContractError):
            replace(self.c, transitions=(Transition("AB", "A", "reuse", "test"),))

    def test_replay_clears_stale_state_preserves_commit(self):
        out = transition(self.c, self.s, "A", authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        self.assertTrue(out.replay_required)
        self.assertEqual(out.state.cache, ())
        self.assertEqual(out.state.draft, "")
        self.assertEqual(out.state.ecid, self.c.ecid("A"))
        self.assertEqual(out.state.input_refs, self.s.input_refs)
        self.assertEqual(action_disposition(out.state, "write-1"), "SKIP_COMMITTED")
        self.assertEqual(self.s.cache, ("cache",))

    def test_uncertain_action_blocks_replay(self):
        s = replace(self.s, uncertain_action_ids=("write-2",))
        out = transition(self.c, s, "A", authorized=True)
        self.assertEqual(out.status, "RECOVERY_REQUIRED")
        self.assertIs(out.state, s)
        self.assertEqual(action_disposition(s, "write-2"), "RECONCILE")

    def test_failure_and_denial_preserve_state(self):
        for kwargs, code in [({}, "AUTHORIZATION_DENIED"), ({"authorized": True, "load_ok": False}, "INTERNAL_FAILURE")]:
            out = transition(self.c, self.s, "A", **kwargs)
            self.assertEqual(out.status, code)
            self.assertIs(out.state, self.s)

    def test_missing_replay_inputs(self):
        s = replace(self.s, input_refs=())
        self.assertEqual(transition(self.c, s, "A", authorized=True).status, "RECOVERY_REQUIRED")

    def test_stale_ecid(self):
        s = replace(self.s, ecid="stale")
        self.assertEqual(transition(self.c, s, "A", authorized=True).status, "INCOMPATIBLE_CONFIGURATION")

    def test_identity_changes_with_artifact(self):
        changed = replace(self.c, overlays=(Overlay("A", "new-A"), self.c.overlays[1]))
        self.assertNotEqual(changed.ecid("A"), self.c.ecid("A"))
        self.assertEqual(self.c.ecid("AB"), example().ecid("AB"))

    def test_same_profile_reuse(self):
        s = replace(self.s, profile="A", ecid=self.c.ecid("A"))
        out = transition(self.c, s, "A", authorized=True)
        self.assertEqual(out.status, "SUCCESS")
        self.assertFalse(out.replay_required)
        self.assertEqual(out.state.cache, s.cache)

if __name__ == "__main__":
    unittest.main()
