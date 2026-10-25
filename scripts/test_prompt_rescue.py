"""Proactive prompt-rescue routing/context regressions; NOT visual quality tests."""
import importlib.util
import json
from pathlib import Path
import unittest
from run_evals import build_prompt, _route_case, selected_contextual_references
ROOT=Path(__file__).resolve().parents[1]
SK=ROOT/"skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("prompt_rescue_router",SK/"brain/route.py")
brain=importlib.util.module_from_spec(spec);spec.loader.exec_module(brain)

class RescueTests(unittest.TestCase):
    def route(self, task, **extra):
        return brain.route({"task":task,**extra})
    def test_short_new_website_requests_become_rebuild(self):
        for task in ("Faz um site foda para o produto", "Faça uma landing para um produto novo", "Make me a beautiful website"):
            with self.subTest(task=task):
                r=self.route(task)
                self.assertEqual(r["strategy"]["mode"],"REBUILD")
                self.assertEqual(r["autonomy_guidance"]["status"],"ADVICE_ONLY_NOT_PERMISSION")
                self.assertIn("real capabilities",r["autonomy_guidance"]["must_not_infer"])
    def test_existing_site_not_rebuilt_by_noun(self):
        self.assertEqual(self.route("Melhore a landing existente e faça um menu novo")["strategy"]["mode"],"REFINE")
    def test_audit_stays_audit(self):
        r=self.route("Analise a landing, mas não implemente mudanças")
        self.assertEqual(r["strategy"]["mode"],"AUDIT")
        self.assertIn("without implementing",r["autonomy_guidance"]["agent_owned_next_actions"][1])
    def test_patch_stays_narrow(self):
        r=self.route("Só corrija o botão",mode="PATCH")
        self.assertEqual(r["strategy"]["mode"],"PATCH")
        self.assertIn("smallest",r["autonomy_guidance"]["agent_owned_next_actions"][1])
    def test_injected_guide_only_in_treatment(self):
        case={"prompt":"Crie uma landing muito bonita para meu produto", "files":[], "meta":{"surface":["landing"]}}
        refs=selected_contextual_references(case,_route_case(case))
        guide="TRUSTED CONTEXTUAL REFERENCE: references/prompt-rescue-and-autonomous-direction.md"
        self.assertIn("references/prompt-rescue-and-autonomous-direction.md",refs)
        self.assertIn(guide,build_prompt(case,"with_skill"))
        self.assertNotIn(guide,build_prompt(case,"without_skill"))
    def test_patch_not_overloaded(self):
        case={"prompt":"Só corrija um bug pontual do checkout", "files":[], "meta":{"surface":["checkout"]}}
        refs=selected_contextual_references(case,_route_case(case))
        self.assertNotIn("references/prompt-rescue-and-autonomous-direction.md",refs)
    def test_evals_present_and_paths_exist(self):
        manifest=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))
        cases=[x for x in manifest["evals"] if 66<=x["id"]<=73]
        self.assertEqual(len(cases),8)
        for case in cases:
            for f in case["files"]:
                self.assertTrue((SK/f).is_file(),f)
if __name__=="__main__":unittest.main()
