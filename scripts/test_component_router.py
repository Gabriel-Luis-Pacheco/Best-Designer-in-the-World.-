"""Regression tests for component-specific candidate routing (not visual quality)."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1] / "skills" / "studio-grade-web-transformation"
SPEC = importlib.util.spec_from_file_location("component_router", BASE / "scripts" / "component_router.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ComponentRouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles, cls.experts = mod.load()

    def route(self, **overrides):
        return mod.suggest(profiles=self.profiles, experts=self.experts, **overrides)

    def test_at_least_40_profiles_all_guides_and_skills_grounded(self):
        self.assertGreaterEqual(len(self.profiles), 40)
        self.assertGreaterEqual(len(self.experts), 40)
        self.assertEqual(len({p["id"] for p in self.profiles}), len(self.profiles))
        for p in self.profiles:
            self.assertTrue(p["specialist_ids"])
            self.assertTrue(p["reference_guides"])
            for x in p["specialist_ids"]:
                self.assertIn(x, self.experts)
            for g in p["reference_guides"]:
                self.assertTrue((BASE / "references" / g).is_file())

    def test_hero_dispatches_marketing_copy_sales_art_qa(self):
        p = self.route(component_ids=["hero"], surface="marketing", mode="REDESIGN")
        hero = p["components"][0]
        ids = {s["id"] for s in hero["specialists"]}
        for required in ("marketing-research", "marketing-copywriting", "marketing-cro",
                         "anthropic-frontend", "taste-skill", "impeccable", "playwright-browser"):
            self.assertIn(required, ids)
        self.assertIn("human-editorial-and-anti-slop-gates.md", " ".join(hero["reference_guides"]))
        self.assertEqual(hero["benchmark"]["target"], "UP_TO_TEN_RELEVANT_REFERENCES_WHEN_FEASIBLE")
        self.assertTrue(all(s["status"] == "CANDIDATE_NOT_INVOKED" for s in hero["specialists"]))

    def test_pricing_and_checkout_have_different_jobs(self):
        p = self.route(component_ids=["pricing", "checkout"], surface="marketing", mode="REBUILD")
        by = {x["id"]: x for x in p["components"]}
        self.assertIn("cobranca", mod._normalize(by["pricing"]["research_focus"]))
        self.assertIn("transacao", mod._normalize(by["checkout"]["user_job"]))
        self.assertNotEqual(by["pricing"]["editorial_or_ux_gate"], by["checkout"]["editorial_or_ux_gate"])

    def test_internals_do_not_force_marketing_funnel(self):
        p = self.route(component_ids=["data-table", "admin-sensitive"], surface="internal", mode="REFINE")
        ids = {s["id"] for item in p["components"] for s in item["specialists"]}
        self.assertNotIn("marketing-cro", ids)
        self.assertNotIn("marketing-ads", ids)
        self.assertIn("a11y-specialist", ids)

    def test_small_patch_does_not_require_ten_references(self):
        p = self.route(component_ids=["hero"], surface="marketing", mode="PATCH")
        self.assertEqual(p["components"][0]["benchmark"]["target"], "TARGETED_REFERENCES_ONLY_WHEN_NEEDED")

    def test_task_autodetect_portuguese_and_word_boundary(self):
        a = self.route(task="Refazer a primeira dobra e os preços para escolas", surface="marketing")
        ids = {x["id"] for x in a["components"]}
        self.assertIn("hero", ids)
        self.assertIn("pricing", ids)
        b = self.route(task="Meu personagem é heroico", surface="marketing")
        self.assertNotIn("hero", {x["id"] for x in b["components"]})

    def test_no_claim_of_tools_run_or_benchmarked(self):
        p = self.route(component_ids=["hero"], surface="marketing")
        self.assertEqual(p["status"], "CANDIDATE_SELECTION_ONLY_NOT_EXECUTED")
        self.assertEqual(p["components"][0]["benchmark"]["status"], "NOT_RESEARCHED_BY_THIS_TOOL")
        self.assertFalse(any(s["status"] == "EXECUTED" for x in p["components"] for s in x["specialists"]))

    def test_invalid_input_and_unknown_component_fail(self):
        for args in ({"component_ids": ["unknown-component"]},
                     {"task": "x" * 10001},
                     {"surface": "finance"},
                     {"mode": "DO-EVERYTHING"}):
            with self.assertRaises(ValueError):
                self.route(**args)

    def test_empty_task_does_not_invent_expertise(self):
        p = self.route(task="melhore algo", surface="marketing")
        self.assertEqual(p["components"], [])

    def test_profile_categories_include_non_marketing_domains(self):
        labels = {p["id"] for p in self.profiles}
        for expected in ("hero", "dashboard", "charts", "empty-state", "error-state",
                         "checkout", "onboarding", "brand-identity", "motion",
                         "3d-interactive", "design-system", "accessibility",
                         "b2b-landing", "b2c-landing", "seo-geo", "admin-sensitive"):
            self.assertIn(expected, labels)


if __name__ == "__main__":
    unittest.main()
