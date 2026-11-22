"""Tests for the 47-component execution atlas and staged specialist workplans."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("component_workplan",ROOT/"scripts/component_workplan.py")
plan_mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan_mod)


class WorkplanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas,cls.experts=plan_mod.load_atlas()

    def go(self,component,mode="REDESIGN",surface="marketing"):
        return plan_mod.plan(component_ids=[component],mode=mode,surface=surface,
                             atlas=self.atlas,experts=self.experts)["components"][0]

    def test_all_47_have_distinct_jobs_and_review_questions(self):
        self.assertEqual(len(self.atlas["profiles"]),47)
        self.assertEqual(len(self.atlas["phase_definitions"]),15)
        jobs={x["id"]:x["review_questions"] for x in self.atlas["profiles"]}
        self.assertNotEqual(jobs["hero"],jobs["checkout"])
        self.assertNotEqual(jobs["pricing"],jobs["dashboard"])
        for id_,questions in jobs.items():
            self.assertGreaterEqual(len(questions),2,id_)

    def test_hero_has_copy_market_art_and_proof_handoffs(self):
        result=self.go("hero")
        steps={x["id"]:x for x in result["phases"]}
        for id_ in ("truth","market","position","editorial","proof","art","ux","engineering","accessibility","render","measurement"):
            self.assertIn(id_,steps)
        sources={r["id"] for x in result["phases"]
                 for r in x["lead_candidates"]+x["alternative_candidates"]}
        for id_ in ("marketing-copywriting","marketing-cro","taste-skill","anthropic-frontend","impeccable"):
            self.assertIn(id_,sources)
        self.assertTrue(all(x["status"]=="NOT_STARTED" for x in result["phases"]))
        self.assertTrue(all(v["status"]=="CANDIDATE_UNVERIFIED_NOT_INVOKED"
                            for x in result["phases"]
                            for v in x["lead_candidates"]+x["alternative_candidates"]))
        self.assertTrue(all(v["source"].startswith("https://github.com/") and v["skill_file"]
                            for x in result["phases"]
                            for v in x["lead_candidates"]+x["alternative_candidates"]))

    def test_dashboard_focused_on_operational_data_not_sales(self):
        result=self.go("dashboard",surface="internal")
        steps={x["id"] for x in result["phases"]}
        self.assertIn("data",steps)
        self.assertNotIn("market",steps)
        self.assertNotIn("position",steps)
        self.assertNotIn("editorial",steps)
        all_ids={r["id"] for x in result["phases"]
                 for r in x["lead_candidates"]+x["alternative_candidates"]}
        self.assertNotIn("marketing-sales",all_ids)
        self.assertNotIn("marketing-cro",all_ids)

    def test_checkout_includes_price_truth_and_recovery(self):
        checkout=self.go("checkout")
        steps={x["id"] for x in checkout["phases"]}
        self.assertIn("commerce",steps)
        self.assertIn("editorial",steps)
        self.assertIn("proof",steps)
        self.assertIn("render",steps)
        self.assertIn("preco",str(checkout["review_questions"]).casefold() +
                      str(checkout["red_flags"]).casefold())

    def test_approved_patch_skips_research_and_creative_ceremony(self):
        hero=self.go("hero",mode="PATCH")
        ids={x["id"] for x in hero["phases"]}
        self.assertNotIn("market",ids)
        self.assertNotIn("editorial",ids)
        self.assertNotIn("position",ids)
        self.assertIn("render",ids)

    def test_all_profile_phase_guides_exist(self):
        for phase in self.atlas["phase_definitions"].values():
            for name in phase["guides"]:
                self.assertTrue((ROOT/"references"/name).is_file(),name)

    def test_unknown_component_or_surface_rejected(self):
        with self.assertRaises(ValueError):
            self.go("nonexistent")
        with self.assertRaises(ValueError):
            self.go("hero",surface="internal")
        with self.assertRaises(ValueError):
            self.go("hero",surface="unrecognized")

    def test_status_is_planning_not_action(self):
        result=plan_mod.plan(component_ids=["hero"],surface="marketing",mode="REBUILD",
                            atlas=self.atlas,experts=self.experts)
        self.assertEqual(result["status"],"PLANNED_NOT_EXECUTED")
        self.assertEqual(result["components"][0]["final_status"],"NOT_EXECUTED_NEEDS_REAL_ARTIFACTS")


if __name__=="__main__":
    unittest.main()
