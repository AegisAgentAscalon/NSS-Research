import json
import tempfile
import unittest
from pathlib import Path

from nss_base.logic_atlas import SPEC_PATH, get_flow, load_atlas, metrics_table, validate_atlas, flow_metrics
from nss_base.runtime import ContractError


class LogicAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = load_atlas()

    def test_all_flows_validate_and_are_reachable(self):
        validate_atlas(self.atlas)
        self.assertGreaterEqual(len(self.atlas["flows"]), 20)

    def test_every_flow_has_explicit_failure_and_forbidden_edges(self):
        for flow in self.atlas["flows"]:
            self.assertTrue(flow["failure_codes"], flow["id"])
            self.assertTrue(flow["forbidden_edges"], flow["id"])
            self.assertTrue(flow["invariants"], flow["id"])

    def test_research_mechanisms_are_not_canonical_prerequisites(self):
        for flow_id in ("context_manager", "recurrent_depth", "directional_guidance", "darp"):
            self.assertIn("research", get_flow(self.atlas, flow_id)["status"])

    def test_core_only_rule_is_explicit(self):
        core = get_flow(self.atlas, "core")
        self.assertTrue(any("Core-only" in x for x in core["invariants"]))
        runtime = get_flow(self.atlas, "overlay_runtime")
        self.assertIn("Failed transition preserves source configuration.", runtime["invariants"])

    def test_recovery_and_action_flows_separate_replay_from_side_effects(self):
        recovery = get_flow(self.atlas, "checkpoint_recovery")
        action = get_flow(self.atlas, "action_boundary")
        joined = "\n".join(recovery["pseudocode"] + action["pseudocode"] + recovery["forbidden_edges"] + action["forbidden_edges"])
        self.assertIn("REPLAY_SAFE", joined)
        self.assertIn("idempotency", joined.lower())
        self.assertIn("Replay -> Repeat committed side effect", joined)

    def test_overlay_runtime_requires_profile_and_transition_qualification(self):
        runtime = get_flow(self.atlas, "overlay_runtime")
        pseudo = "\n".join(runtime["pseudocode"])
        self.assertIn("QUALIFIED(target.qap)", pseudo)
        self.assertIn("QUALIFIED(state.profile -> target.qap)", pseudo)

    def test_qualification_is_claim_scoped(self):
        q = get_flow(self.atlas, "qualification")
        self.assertIn("Qualification is claim-scoped.", q["invariants"])
        self.assertTrue(any("exact hashes" in x for x in q["invariants"]))

    def test_no_terminal_has_outgoing_edge(self):
        for flow in self.atlas["flows"]:
            terminal_ids = set(flow["terminals"])
            self.assertFalse(any(e["from"] in terminal_ids for e in flow["transitions"]), flow["id"])

    def test_metrics_are_bounded_and_nonzero(self):
        for flow_id, metrics in metrics_table(self.atlas):
            self.assertGreaterEqual(metrics.nodes, 5, flow_id)
            self.assertGreaterEqual(metrics.cyclomatic_complexity, 1, flow_id)
            self.assertLess(metrics.cyclomatic_complexity, 12, flow_id)

    def test_unknown_outcome_fails_validation(self):
        bad = json.loads(json.dumps(self.atlas))
        bad["flows"][0]["failure_codes"].append("NOT_A_REAL_OUTCOME")
        with self.assertRaises(ContractError):
            validate_atlas(bad)

    def test_unreachable_node_fails_validation(self):
        bad = json.loads(json.dumps(self.atlas))
        bad["flows"][0]["nodes"].append({"id":"orphan","label":"orphan","kind":"process"})
        with self.assertRaises(ContractError):
            validate_atlas(bad)

    def test_malformed_values_are_typed_failures(self):
        changes = [lambda a: a.update(schema_version=True),
                   lambda a: a.update(global_outcomes=[{}]),
                   lambda a: a.update(flows=[None]),
                   lambda a: a["flows"][0].update(nodes=[None]),
                   lambda a: a["flows"][0].update(transitions=None),
                   lambda a: a["flows"][0].update(failure_codes=[{}]),
                   lambda a: a["flows"][0].update(terminals={"done": ["SUCCESS"], "fail": [{}]}),
                   lambda a: a["shared_primitives"].update(TRY=None)]
        for i, change in enumerate(changes):
            with self.subTest(case=i):
                bad = json.loads(json.dumps(self.atlas)); change(bad)
                with self.assertRaises(ContractError): validate_atlas(bad)

    def test_duplicate_edge_cannot_satisfy_decision_branches(self):
        bad = json.loads(json.dumps(self.atlas))
        bad["flows"][0]["transitions"].append(dict(bad["flows"][0]["transitions"][0]))
        with self.assertRaises(ContractError): validate_atlas(bad)

    def test_unmapped_terminal_and_failure_success_are_rejected(self):
        for mode in ("unmapped", "false_success"):
            bad = json.loads(json.dumps(self.atlas)); f = bad["flows"][0]
            if mode == "unmapped": del f["terminals"]["done"]
            else: f["terminals"]["fail"] = ["SUCCESS"]
            with self.assertRaises(ContractError): validate_atlas(bad)

    def test_reachable_closed_cycle_is_rejected(self):
        bad = json.loads(json.dumps(self.atlas)); f = bad["flows"][0]
        f["nodes"].append({"id":"trap", "kind":"process", "label":"trap"})
        f["transitions"].extend([{"from":"auth", "to":"trap", "when":"trap"},
                                  {"from":"trap", "to":"trap", "when":"always"}])
        with self.assertRaises(ContractError): validate_atlas(bad)

    def test_strict_json_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/"bad.json"
            for text in ('{"schema_version":2,"schema_version":2}', '{"x":NaN}'):
                p.write_text(text, encoding="utf-8")
                with self.assertRaises(ContractError): load_atlas(p)

    def test_normalized_complexity_two_exits(self):
        f = {"nodes":[{"kind":"start"},{"kind":"decision"},{"kind":"success"},{"kind":"failure"}],
             "transitions":[{}, {}, {}], "terminals":{"ok":["SUCCESS"],"bad":["VALIDATION_FAILED"]}}
        self.assertEqual(flow_metrics(f).cyclomatic_complexity, 2)

    def test_terminal_envelopes_preserve_declared_codes(self):
        for f in self.atlas["flows"]:
            for codes in f["terminals"].values():
                self.assertIsInstance(codes, list)
                self.assertTrue(set(codes) <= set(f["failure_codes"]) | {"SUCCESS"})

    def test_refinement_consumes_budget_and_profile_selection_is_exact(self):
        for fid in ("recurrent_depth", "darp"):
            code = "\n".join(get_flow(self.atlas, fid)["pseudocode"])
            self.assertIn("BUDGET.claim(", code)
            self.assertNotIn("BUDGET.can_claim", code)
        self.assertIn("SELECT_ONE_QUALIFIED_PROFILE", "\n".join(get_flow(self.atlas,"overlay_index")["pseudocode"]))


if __name__ == "__main__":
    unittest.main()
