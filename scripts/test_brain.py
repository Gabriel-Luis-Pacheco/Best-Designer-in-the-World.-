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
    def test_unverified_inference_is_explicitly_not_authorized(self):
        d=brain.route({"task":"Faça um site bonito e útil"})
        self.assertEqual(d["triage_review"]["interpretation"],"HYPOTHESIS_ONLY")
        self.assertIn("surface",d["triage_review"]["inferred_fields"])
        self.assertIn("verified_product_facts",d["triage_review"]["context_gaps"])
        self.assertEqual(d["triage_review"]["approval"],"NOT_AUTHORIZED_TO_EDIT_FROM_THIS_OUTPUT")
    def test_explicit_context_reduces_but_does_not_eliminate_review(self):
        d=brain.route({"task":"Redesenhe esta landing comercial",
                       "surface":"landing","vertical":"commerce","mode":"REDESIGN",
                       "goals":["conversion"],"audience":"Compradores",
                       "facts":["Preço confirmado pelo responsável"]})
        self.assertEqual(d["triage_review"]["inferred_fields"],[])
        self.assertEqual(d["triage_review"]["context_gaps"],[])
        self.assertEqual(d["triage_review"]["interpretation"],"HYPOTHESIS_ONLY")

    def test_luxury_experiential_landing_preserves_both_goals(self):
        d=brain.route({"task":"Crie uma landing page comercial experimental nível Awwwards para "
                       "caixa de som escultural de luxo. A experiência visual é o diferencial."})
        self.assertEqual(d["strategy"]["mode"],"REBUILD")
        self.assertEqual(d["strategy"]["creative_authority"],"EXPERIENTIAL_COMMERCE")
        self.assertEqual(d["strategy"]["primary_goal"],"artistic_impact")
        self.assertIn("conversion",d["strategy"]["secondary_goals"])
        self.assertIn("references/experiential-commerce.md",d["tool_routing"]["selected_skill_refs"])

    def test_fresh_commercial_landing_not_refine(self):
        d=brain.route({"task":"Crie uma landing page para um produto novo"})
        self.assertEqual(d["strategy"]["mode"],"REBUILD")
        self.assertEqual(d["product"]["surfaces"],["landing"])

    def test_existing_landing_refinement_preserved(self):
        d=brain.route({"task":"Melhore a landing existente e crie um menu melhor"})
        self.assertEqual(d["strategy"]["mode"],"REFINE")

    def test_experimental_operations_cannot_override_accuracy(self):
        d=brain.route({"task":"Crie dashboard para sistema interno de fintech Awwwards com dados auditáveis"})
        self.assertEqual(d["strategy"]["creative_authority"],"OPERATIONAL_FIRST_ART_SUPPORT")
        self.assertEqual(d["strategy"]["primary_goal"],"accuracy")

    def test_awwwards_checkout_never_becomes_an_art_exhibition(self):
        d=brain.route({"task":"Crie checkout Awwwards de uma loja com preço e pagamentos reais"})
        self.assertEqual(d["strategy"]["creative_authority"],"COMMERCE_FIRST_ART_SUPPORT")
        self.assertEqual(d["strategy"]["primary_goal"],"conversion")

    def test_awwwards_product_preserves_product_activation(self):
        d=brain.route({"task":"Crie um app Awwwards para onboarding de novos usuários"})
        self.assertEqual(d["strategy"]["creative_authority"],"PRODUCT_FIRST_ART_SUPPORT")
        self.assertEqual(d["strategy"]["primary_goal"],"activation")

    def test_explicit_goal_hybrid_still_overrides_defaults(self):
        d=brain.route({"task":"Crie landing comercial experimental Awwwards",
                       "goals":["trust","artistic_impact"]})
        self.assertEqual(d["strategy"]["primary_goal"],"trust")

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

    def test_compound_analysis_and_implementation_routes_to_execution(self):
        d=brain.route({"task":"Analise esta landing e implemente todas as melhorias necessárias",
                       "surface":"landing"})
        self.assertEqual(d["strategy"]["mode"],"REFINE")
        self.assertEqual(d["triage_review"]["execution_intent"],"ANALYZE_AND_IMPLEMENT")
    def test_inspection_only_remains_audit(self):
        d=brain.route({"task":"Analise esta landing e descreva as melhorias",
                       "surface":"landing"})
        self.assertEqual(d["strategy"]["mode"],"AUDIT")
    def test_compound_small_patch_remains_patch(self):
        d=brain.route({"task":"Analise e corrija apenas o botão de feedback",
                       "surface":"product"})
        self.assertEqual(d["strategy"]["mode"],"PATCH")
    def test_operational_redesign_avoids_editorial_reference(self):
        d=brain.route({"task":"Redesenhe sistema interno de conciliação",
                       "surface":"internal","mode":"REDESIGN"})
        self.assertNotIn("references/editorial-art-direction-lab.md",
                         d["tool_routing"]["selected_skill_refs"])
    def test_analyze_and_fix_broadly_is_not_a_small_patch(self):
        d=brain.route({"task":"Analise tudo e corrija todos os problemas","surface":"landing"})
        self.assertEqual(d["strategy"]["mode"],"REFINE")
    def test_normal_internal_is_operational_without_awwwards_cue(self):
        d=brain.route({"task":"Redesenhe sistema interno de conciliação","surface":"internal"})
        self.assertEqual(d["strategy"]["creative_authority"],"OPERATIONAL_FIRST_ART_SUPPORT")
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

    def test_awwwards_experience_routes_to_real_studio_process(self):
        d=brain.route({"task":"Crie um museu digital experimental Awwwards","surface":"experience"})
        refs=d["tool_routing"]["selected_skill_refs"]
        self.assertIn("references/awwwards-studio-production.md",refs)
        self.assertIn("references/award-readiness-and-qa.md",refs)
        self.assertNotIn("references/landing-page-evidence-and-cro.md",refs)

    def test_commercial_landing_routes_to_cro_not_3d_by_default(self):
        d=brain.route({"task":"Crie uma landing comercial de SaaS","surface":"landing"})
        refs=d["tool_routing"]["selected_skill_refs"]
        self.assertIn("references/landing-page-evidence-and-cro.md",refs)
        self.assertNotIn("references/creative-technology-playbook.md",refs)

    def test_explicit_threejs_landing_routes_to_creative_tech(self):
        d=brain.route({"task":"Landing comercial com Three.js e WebGL","surface":"landing"})
        self.assertIn("references/creative-technology-playbook.md",
                      d["tool_routing"]["selected_skill_refs"])

    def test_skill_research_is_conditional(self):
        d=brain.route({"task":"Faça seleção de skills externas para redesign","surface":"landing"})
        self.assertIn("references/specialist-skills-orchestration.md",
                      d["tool_routing"]["selected_skill_refs"])

    def test_internal_fintech_never_receives_awards_pack_by_default(self):
        d=brain.route({"task":"Corrija apenas filtro de tabela","surface":"internal","vertical":"fintech"})
        self.assertNotIn("references/awwwards-studio-production.md",
                         d["tool_routing"]["selected_skill_refs"])

    def test_experience_design_evidence_pack(self):
        d=brain.route({"task":"Crie um museu Awwwards imersivo","surface":"experience","mode":"REBUILD"})
        refs=d["tool_routing"]["selected_skill_refs"]
        self.assertIn("references/persistent-design-knowledge.md",refs)
        self.assertNotIn("references/marketing-research-and-experiments.md",refs)
    def test_landing_cro_research_selected(self):
        d=brain.route({"task":"Refaça landing que precisa de conversão","surface":"landing","mode":"REDESIGN","goals":["conversion"]})
        self.assertIn("references/marketing-research-and-experiments.md",d["tool_routing"]["selected_skill_refs"])
    def test_internal_patch_no_new_arts_packs(self):
        d=brain.route({"task":"Corrija só filtro no painel","surface":"internal","mode":"PATCH"})
        paths=d["tool_routing"]["selected_skill_refs"]
        self.assertNotIn("references/design-audit-execution.md",paths)
        self.assertNotIn("references/persistent-design-knowledge.md",paths)
        self.assertNotIn("references/motion-3d-engineering-cookbook.md",paths)

    def test_no_3d_if_user_explicitly_refuses_webgl(self):
        d=brain.route({"task":"Crie uma experiência artística sem WebGL e sem GSAP usando SVG",
                       "surface":"experience"})
        refs=d["tool_routing"]["selected_skill_refs"]
        self.assertNotIn("references/creative-technology-playbook.md",refs)
        self.assertNotIn("references/motion-3d-engineering-cookbook.md",refs)

    def test_positive_3d_after_negation_is_kept(self):
        d=brain.route({"task":"Sem WebGL, mas quero Three.js com WebGPU",
                       "surface":"experience"})
        self.assertIn("references/creative-technology-playbook.md",
                      d["tool_routing"]["selected_skill_refs"])

    def test_no_heavy_stack_for_simple_photo_product(self):
        d=brain.route({"task":"Crie landing de caixa de som com fotografias e CSS",
                       "surface":"landing"})
        self.assertNotIn("references/motion-3d-engineering-cookbook.md",
                         d["tool_routing"]["selected_skill_refs"])

    def test_portuguese_preposition_no_webgl_is_positive(self):
        d=brain.route({"task":"Crie uma experiência no WebGL com animação",
                       "surface":"experience"})
        self.assertIn("references/creative-technology-playbook.md",
                      d["tool_routing"]["selected_skill_refs"])
