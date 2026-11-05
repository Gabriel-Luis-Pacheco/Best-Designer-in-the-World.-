"""Verify v13 guidance is actually injected by the evaluation runner when needed."""
import unittest
from run_evals import _route_case, selected_contextual_references, build_prompt

CASES = [
    ("Crie experiência artística com um personagem canônico específico, fiel ao pedido inicial",
     ["experience"], "original-brief-and-referent-fidelity.md"),
    ("Crie landing com posicionamento e copywriting para compradores reais",
     ["landing"], "positioning-and-copywriting.md"),
    ("Crie landing pública e otimize SEO e indexação com evidência",
     ["landing"], "seo-discovery-and-search-experience.md"),
    ("Redesign completo e use subagentes críticos com evidência visual",
     ["landing"], "review-council-and-course-correction.md"),
    ("Me surpreenda com um site incrível do zero, briefing ruim",
     ["landing"], "proactive-completeness-and-launch.md"),
]


class V13ReferenceReachabilityTests(unittest.TestCase):
    def test_injected_in_real_with_skill_prompt(self):
        for prompt, surfaces, filename in CASES:
            with self.subTest(filename=filename):
                case = {"prompt": prompt, "files": [], "meta": {"surface": surfaces}}
                refs = selected_contextual_references(case, _route_case(case))
                ref = "references/" + filename
                self.assertIn(ref, refs)
                self.assertIn("TRUSTED CONTEXTUAL REFERENCE: " + ref, build_prompt(case, "with_skill"))
                self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: " + ref, build_prompt(case, "without_skill"))

    def test_small_patch_does_not_load_design_council_and_seo_stack(self):
        case = {"prompt": "Só corrige o tamanho de um botão de SEO em uma landing",
                "files": [], "meta": {"surface": ["landing"]}}
        refs = selected_contextual_references(case, _route_case(case))
        self.assertLessEqual(len(refs), 2)
        self.assertNotIn("references/review-council-and-course-correction.md", refs)
        self.assertNotIn("references/seo-discovery-and-search-experience.md", refs)


if __name__ == "__main__":
    unittest.main()
