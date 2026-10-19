"""Regression tests for intent vetoes and actual reading-guide injection."""
import importlib.util
from pathlib import Path
import unittest
from run_evals import build_prompt

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("intent_route", ROOT / "skills/studio-grade-web-transformation/brain/route.py")
brain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brain)


class IntentAndReadingTests(unittest.TestCase):
    def route(self, task, **extra):
        return brain.route({"task": task, **extra})

    def test_explicit_implementation_veto_remains_audit(self):
        for task in ("Analise a landing. Não implemente mudanças.",
                     "Review the landing; do not implement changes.",
                     "Analise a página e não faça redesign.",
                     "Não crie do zero; analise a página existente."):
            with self.subTest(task=task):
                self.assertEqual(self.route(task)["strategy"]["mode"], "AUDIT")

    def test_english_compound_request_implements(self):
        self.assertEqual(self.route("Review this landing and implement the improvements")["strategy"]["mode"], "REFINE")

    def test_explicit_mode_wins_over_heuristic(self):
        self.assertEqual(self.route("Analise esta landing", mode="PATCH")["strategy"]["mode"], "PATCH")

    def test_later_positive_surface_is_not_erased_by_earlier_negative(self):
        task = "Não é uma landing page. Mas agora crie uma landing page para o outro produto."
        self.assertIn("landing", self.route(task)["product"]["surfaces"])

    def test_english_negative_surface_does_not_pollute_art(self):
        out = self.route("Create an immersive experience, not a landing page.")
        self.assertNotIn("landing", out["product"]["surfaces"])

    def test_read_uses_information_design_without_marketing_gallery_defaults(self):
        out = self.route("Redesenhe documentação técnica", surface="read")
        refs = out["tool_routing"]["selected_skill_refs"]
        self.assertIn("references/reading-and-information-design.md", refs)
        self.assertNotIn("references/editorial-art-direction-lab.md", refs)
        self.assertTrue(all(x["kind"] != "visual" for x in out["tool_routing"]["research_candidates"]))

    def test_reading_guide_is_actually_injected_for_audit_refine_and_rebuild(self):
        for task in ("Analise documentação", "Melhore documentação", "Crie documentação do zero"):
            case = {"prompt": task, "files": [], "meta": {"surface": "read"}}
            with self.subTest(task=task):
                prompt = build_prompt(case, "with_skill")
                self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/reading-and-information-design.md", prompt)
                self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/marketing-research-and-experiments.md", prompt)
                self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/reading-and-information-design.md", build_prompt(case, "without_skill"))

class PreservationAndNounTests(unittest.TestCase):
    def test_declined_surface_creation_does_not_inject_marketing(self):
        for task in ("Não quero criar uma landing page; crie documentação.",
                     "Não quero fazer uma landing; crie documentação.",
                     "I don't want to build a landing page; create technical documentation."):
            with self.subTest(task=task):
                out = brain.route({"task": task})
                self.assertNotIn("landing", out["product"]["surfaces"])
                self.assertEqual(out["strategy"]["primary_goal"], "comprehension")
                self.assertNotIn("references/landing-page-evidence-and-cro.md", out["tool_routing"]["selected_skill_refs"])

    def test_preserving_behavior_does_not_remove_surface(self):
        for task, surface in (
            ("Improve the layout without changing checkout behavior", "checkout"),
            ("Do not lose data in the dashboard", "dashboard"),
            ("Não quero mudar o checkout, apenas analisar", "checkout")):
            with self.subTest(task=task):
                self.assertIn(surface, brain.route({"task": task})["product"]["surfaces"])

    def test_read_surface_is_inferred_from_common_documentation_terms(self):
        for task in ("Review the build docs only", "Audit the build pipeline documentation"):
            with self.subTest(task=task):
                out = brain.route({"task": task})
                self.assertEqual(out["strategy"]["mode"], "AUDIT")
                self.assertIn("read", out["product"]["surfaces"])
                self.assertEqual(out["strategy"]["primary_goal"], "comprehension")

    def test_audit_of_build_documentation_does_not_implement(self):
        out = brain.route({"task": "Audit the build pipeline documentation", "surface": "read"})
        self.assertEqual(out["strategy"]["mode"], "AUDIT")

    def test_compound_build_verb_is_an_implementation_request(self):
        out = brain.route({"task": "Review the documentation and build the requested interface", "surface": "read"})
        self.assertEqual(out["strategy"]["mode"], "REFINE")


if __name__ == "__main__":
    unittest.main()
