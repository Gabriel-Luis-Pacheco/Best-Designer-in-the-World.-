#!/usr/bin/env python3
"""Static regression guard for research-to-skill reachability and scenario integrity.

This test checks wiring and data shape only. It does not execute LLM evaluations,
render pages, prove conversion improvement or certify accessibility/aesthetics.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "skills" / "studio-grade-web-transformation"
GUIDES = (
    "landing-strategy-and-decision-architecture.md",
    "copy-lab-and-ethical-psychology.md",
    "visual-direction-and-anti-slop-atelier.md",
    "funnel-measurement-experiments-and-release.md",
)


class LandingResearchIntegrationTests(unittest.TestCase):
    def test_all_research_guides_are_reachable(self):
        core = (SK / "SKILL.md").read_text(encoding="utf-8")
        index = (SK / "references" / "resource-index.md").read_text(encoding="utf-8")
        for name in GUIDES:
            with self.subTest(guide=name):
                path = SK / "references" / name
                self.assertTrue(path.is_file())
                self.assertGreater(len(path.read_text(encoding="utf-8")), 2500)
                self.assertIn("references/" + name, core)
                self.assertEqual(index.count("references/" + name), 1)

    def test_original_qa_scope_remains_preserved(self):
        core = (SK / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "Original-brief compass",
            "Course correction",
            "NOT VERIFIED",
            "Independent critique",
            "LANDING / MARKETING",
            "CUT",
            "render",
        ):
            self.assertIn(required.casefold(), core.casefold())

    def test_optional_templates_and_sources_exist(self):
        for path in (
            SK / "templates/LANDING_DECISION_CARD.md",
            SK / "templates/LANDING_REVIEW_CARD.md",
            ROOT / "docs/RESEARCH_LANDING_PAGE_SYSTEM_2026-11-06.md",
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 1000)
        source_map = (ROOT / "docs/RESEARCH_LANDING_PAGE_SYSTEM_2026-11-06.md").read_text(encoding="utf-8")
        self.assertIn("https://www.w3.org/TR/WCAG22/", source_map)
        self.assertIn("https://web.dev/articles/vitals", source_map)

    def test_research_scenarios_are_explicitly_unexecuted(self):
        path = SK / "evals/landing_research_scenarios.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "NOT_RUN")
        scenarios = data["scenarios"]
        self.assertGreaterEqual(len(scenarios), 6)
        self.assertEqual(len({case["id"] for case in scenarios}), len(scenarios))
        for case in scenarios:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["surface"])
                self.assertGreater(len(case["prompt"]), 50)
                self.assertGreaterEqual(len(case["expected"]), 3)
                self.assertGreaterEqual(len(case["anti_patterns"]), 2)


if __name__ == "__main__":
    unittest.main()
