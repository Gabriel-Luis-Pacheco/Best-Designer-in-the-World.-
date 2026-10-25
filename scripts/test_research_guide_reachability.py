"""Research guides must reach the model in relevant tasks, not merely a catalog."""
import unittest
from run_evals import _route_case,selected_contextual_references,build_prompt
CASES=[
("Crie landing completa com evidência e prova visual",["landing"],"evidence-to-scene-protocol.md"),
("Crie landing para lançamento com SEO",["landing"],"commercial-launch-evidence.md"),
("Crie landing de inteligência artificial com AI UX responsável",["landing"],"ai-creative-integrity-and-ux.md"),
("Crie experiência artística Awwwards para um museu virtual",["experience"],"award-business-reference-atlas.md"),
]
class ResearchReachabilityTests(unittest.TestCase):
    def test_real_context_injection(self):
        for task,surfaces,name in CASES:
            with self.subTest(name=name):
                case={"prompt":task,"files":[],"meta":{"surface":surfaces}}
                refs=selected_contextual_references(case,_route_case(case))
                self.assertIn("references/"+name,refs)
                self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/"+name,build_prompt(case,"with_skill"))
                self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/"+name,build_prompt(case,"without_skill"))
    def test_patch_is_small(self):
        case={"prompt":"Só corrija o link SEO na landing","files":[],"meta":{"surface":["landing"]}}
        refs=selected_contextual_references(case,_route_case(case))
        self.assertLessEqual(len(refs),2)
        self.assertNotIn("references/commercial-launch-evidence.md",refs)
if __name__=="__main__":unittest.main()
