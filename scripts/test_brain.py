"""Adversarial strategy routing tests. They don't grade designs or research."""
import importlib.util
import pathlib
import json
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("design_brain",ROOT/"brain/route.py")
brain=importlib.util.module_from_spec(spec);spec.loader.exec_module(brain)

class BrainTests(unittest.TestCase):
    def sample(self,name):
        return json.loads((ROOT/"brain/examples"/(name+".json")).read_text(encoding="utf-8"))
    def test_fintech_same_vertical_different_surfaces(self):
        landing=brain.route(self.sample("fintech-landing"))
        internal=brain.route(self.sample("fintech-internal"))
        self.assertEqual(landing["product"]["vertical"],"fintech")
        self.assertEqual(internal["product"]["vertical"],"fintech")
        self.assertEqual(landing["strategy"]["primary_goal"],"conversion")
        self.assertEqual(internal["strategy"]["primary_goal"],"accuracy")
        self.assertNotEqual(landing["strategy"]["surface_plans"][0]["reference_packs"],
                            internal["strategy"]["surface_plans"][0]["reference_packs"])
    def test_edtech_retention_is_secondary(self):
        d=brain.route(self.sample("edtech-product"))
        self.assertEqual(d["strategy"]["primary_goal"],"learning")
        self.assertIn("retention",d["strategy"]["secondary_goals"])
        self.assertEqual(d["strategy"]["measurement_status"],"NOT_MEASURED")
    def test_implicit_multisurface_not_collapsed(self):
        d=brain.route({"task":"Redesenhe landing e sistema interno de fintech"})
        self.assertIn("landing",d["product"]["surfaces"])
        self.assertIn("internal",d["product"]["surfaces"])
        self.assertEqual(len(d["strategy"]["surface_plans"]),2)
    def test_explicit_goal_takes_precedence(self):
        d=brain.route({"task":"Melhore site de educação","surface":"landing","vertical":"education","goals":["trust","conversion"]})
        self.assertEqual(d["strategy"]["primary_goal"],"trust")
        self.assertEqual(d["strategy"]["goal_source"],"explicit")
    def test_patch_minimum_research(self):
        d=brain.route({"task":"Corrija apenas bug no menu","mode":"PATCH","surface":"product"})
        self.assertEqual(d["tool_routing"]["research_candidates"],[])
    def test_sources_are_never_claimed_inspected(self):
        d=brain.route(self.sample("fintech-landing"))
        self.assertTrue(d["tool_routing"]["research_candidates"])
        self.assertTrue(all(r["status"]=="CANDIDATE_NOT_INSPECTED" for r in d["tool_routing"]["research_candidates"]))
    def test_no_fake_verified_facts(self):
        d=brain.route(self.sample("fintech-internal"))
        self.assertIn("facts_provided_unverified",d["product"])
        self.assertNotIn("VERIFIED",d["strategy"]["measurement_status"])
    def test_all_skills_resolve_inside_portable_package(self):
        d=brain.route(self.sample("fintech-landing"))
        for name in d["tool_routing"]["selected_skill_refs"]:
            self.assertTrue((ROOT/name).is_file(),name)
    def test_invalid_surface_fails_closed(self):
        with self.assertRaises(ValueError):brain.route({"task":"Melhore","surface":"astro"})
    def test_invalid_tool_payload_fails_closed(self):
        with self.assertRaises(ValueError):brain.route({"task":"Melhore","tools":"run shell"})
    def test_missing_task_errors(self):
        with self.assertRaises(ValueError):brain.route({"surface":"landing"})
    def test_mode_recognizes_audit(self):
        d=brain.route({"task":"Analise criticamente o dashboard","surface":"dashboard"})
        self.assertEqual(d["strategy"]["mode"],"AUDIT")
