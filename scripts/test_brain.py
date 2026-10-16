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
    def test_creative_mirage_explicit_negative_landing(self):
        task=("Crie um site experimental de nível Awwwards, museu digital de mundos impossíveis. "
              "Não estamos criando um produto comercial, um MVP, uma landing page de vendas ou um site corporativo.")
        d=brain.route({"task":task})
        self.assertEqual(d["product"]["surfaces"],["experience"])
        self.assertEqual(d["strategy"]["primary_goal"],"artistic_impact")
        self.assertEqual(d["strategy"]["mode"],"REBUILD")
        self.assertEqual(d["strategy"]["creative_authority"],"ART_DIRECTOR_FIRST")
        self.assertIn("references/creative-experience-direction.md",d["tool_routing"]["selected_skill_refs"])
        self.assertNotIn("conversion",d["strategy"]["secondary_goals"])

    def test_negative_surface_does_not_trigger_commercial(self):
        d=brain.route({"task":"Não é uma landing page, é uma experiência imersiva artística. Crie o site."})
        self.assertNotIn("landing",d["product"]["surfaces"])
        self.assertEqual(d["strategy"]["primary_goal"],"artistic_impact")

    def test_experience_explicit_goal_can_override_creative_default(self):
        d=brain.route({"task":"Experiência imersiva para ensinar", "surface":"experience", "goals":["learning"]})
        self.assertEqual(d["strategy"]["primary_goal"],"learning")
        self.assertEqual(d["strategy"]["goal_source"],"explicit")

    def test_creative_sources_are_candidates_not_visited(self):
        d=brain.route({"task":"Crie website experimental Awwwards"})
        self.assertEqual(d["tool_routing"]["research_candidates"][0]["kind"],"visual")
        self.assertTrue(all(x["status"]=="CANDIDATE_NOT_INSPECTED" for x in d["tool_routing"]["research_candidates"]))

    def test_critical_phrase_not_substring(self):
        self.assertFalse(brain.contains_phrase("hospitalidade","hospital"))
        self.assertTrue(brain.contains_phrase("hospital clínico","hospital"))

    def test_redesign_after_analysis_not_audit(self):
        d=brain.route({"task":"Analise a landing e proponha um redesign completo","surface":"landing"})
        self.assertEqual(d["strategy"]["mode"],"REDESIGN")

    def test_only_fix_is_patch(self):
        d=brain.route({"task":"Corrija só o botão de feedback","surface":"product"})
        self.assertEqual(d["strategy"]["mode"],"PATCH")

    def test_education_landing_not_forced_into_learning(self):
        d=brain.route({"task":"Melhore esta landing de inglês","surface":"landing","vertical":"education"})
        self.assertEqual(d["strategy"]["primary_goal"],"conversion")

    def test_natural_language_trust_over_clicks(self):
        d=brain.route({"task":"Quero melhorar confiabilidade e transparência desta landing, não preciso aumentar cliques agora"})
        self.assertEqual(d["strategy"]["primary_goal"],"trust")

    def test_research_gallery_is_reachable_for_landing(self):
        d=brain.route({"task":"Redesenhe uma landing comercial","surface":"landing","mode":"REDESIGN"})
        ids={x["id"] for x in d["tool_routing"]["research_candidates"]}
        self.assertTrue(ids.intersection({"awwwards","siteinspire"}),ids)

    def test_explicit_governing_goal_survives_multisurface(self):
        d=brain.route({"task":"Melhore landing e sistema interno de fintech",
                       "surface":["landing","internal"],"goals":["trust","conversion"]})
        self.assertTrue(all(x["governing_goal"]=="trust" for x in d["strategy"]["surface_plans"]))
        self.assertTrue(all(x["explicit_goals_not_overridden"] for x in d["strategy"]["surface_plans"]))

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

    def test_internal_fintech_avoids_marketing_gallery(self):
        d=brain.route(self.sample("fintech-internal"))
        ids={x["id"] for x in d["tool_routing"]["research_candidates"]}
        self.assertFalse(ids.intersection({"awwwards","siteinspire","landbook","godly"}))
    def test_research_questions_include_mechanisms(self):
        d=brain.route(self.sample("fintech-internal"))
        layers={x["layer"] for x in d["tool_routing"]["research_questions"]}
        self.assertEqual(layers,{"domain","mechanism","expression"})
        self.assertTrue(all(x["status"]=="NOT_EXECUTED" for x in d["tool_routing"]["research_questions"]))
    def test_patch_no_research_questions(self):
        d=brain.route({"task":"Corrija apenas bug","mode":"PATCH","surface":"internal"})
        self.assertEqual(d["tool_routing"]["research_questions"],[])
