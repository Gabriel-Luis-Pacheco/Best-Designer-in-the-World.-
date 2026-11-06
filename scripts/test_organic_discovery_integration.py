"""Offline structural tests: optional organic evidence validator and skill reference wiring."""
import json
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "skills" / "studio-grade-web-transformation"
SCRIPT = SK / "scripts/organic_opportunity_audit.py"
spec = importlib.util.spec_from_file_location("organic_opportunity_audit", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
GUIDES = [
    "organic-discovery-operating-system.md",
    "ai-answer-and-entity-visibility.md",
    "search-content-and-authority-engine.md",
    "search-intelligence-measurement-loop.md",
]


def example():
    return {
        "mode": "REDESIGN", "scope": "public",
        "business_goal": "Legitimate activated trial", "audience": "Learners",
        "intents": [{
            "id": "speaking-practice", "market": "pt-BR Brazil",
            "user_job": "Try a real speaking exercise",
            "query_family": "praticar ingles conversacao",
            "reason_to_win": "Genuine interactive speaking feedback",
            "research_status": "HYPOTHESIS", "target_url": None,
            "original_proof": "Observed working first exercise",
            "next_user_action": "Try speaking"
        }],
        "measurement": {"baseline_status": "UNKNOWN",
                        "qualified_outcome": "activated trials per eligible organic session"}
    }


class OrganicIntegrationTests(unittest.TestCase):
    def test_guides_are_reachable_and_indexed(self):
        core = (SK / "SKILL.md").read_text(encoding="utf-8")
        index = (SK / "references/resource-index.md").read_text(encoding="utf-8")
        for name in GUIDES:
            with self.subTest(name=name):
                self.assertTrue((SK / "references" / name).is_file())
                self.assertIn("references/" + name, core)
                self.assertEqual(index.count("references/" + name), 1)

    def test_packet_accepts_honest_unknowns(self):
        self.assertEqual(module.inspect(example())["status"], "DECLARED_READY_FOR_REVIEW")

    def test_observed_serp_without_source_is_error(self):
        packet = example()
        packet["intents"][0]["research_status"] = "OBSERVED"
        result = module.inspect(packet)
        self.assertIn("OBSERVED_WITHOUT_SOURCE", {x["code"] for x in result["findings"]})
        self.assertEqual(result["status"], "INVALID")

    def test_observed_source_is_traceable(self):
        packet = example()
        packet["intents"][0]["research_status"] = "OBSERVED"
        packet["intents"][0]["research_source"] = {
            "date": "2026-11-06", "url": "https://example.com/a-serp-snapshot"}
        self.assertEqual(module.inspect(packet)["status"], "DECLARED_READY_FOR_REVIEW")

    def test_rank_claim_and_missing_proof(self):
        packet = example()
        packet["intents"][0]["ranking_claim"] = True
        packet["intents"][0]["original_proof"] = ""
        packet["intents"][0]["publish"] = True
        codes = {x["code"] for x in module.inspect(packet)["findings"]}
        self.assertIn("UNSUPPORTED_RANKING", codes)
        self.assertIn("NO_ORIGINAL_ADVANTAGE", codes)
        self.assertIn("PUBLISH_WITHOUT_PROOF", codes)

    def test_private_context_is_not_forced_into_marketing(self):
        packet = example()
        packet["scope"] = "private"
        self.assertEqual(module.inspect(packet)["status"], "NOT_APPLICABLE")

    def test_invalid_input_is_nonfatal(self):
        for value in [None, [], 42, "x", {}]:
            with self.subTest(value=value):
                self.assertEqual(module.inspect(value)["status"], "INVALID")
        packet = example()
        packet["intents"] = [None]
        self.assertEqual(module.inspect(packet)["status"], "INVALID")

    def test_supplemental_scenarios_are_unexecuted(self):
        cases = json.loads((SK / "evals/organic_discovery_scenarios.json").read_text(encoding="utf-8"))
        self.assertEqual(cases["status"], "NOT_RUN")
        self.assertGreaterEqual(len(cases["scenarios"]), 6)
        self.assertEqual(len({x["id"] for x in cases["scenarios"]}), len(cases["scenarios"]))


if __name__ == "__main__":
    unittest.main()
