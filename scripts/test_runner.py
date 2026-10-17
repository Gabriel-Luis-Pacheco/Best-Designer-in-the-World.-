"""Smoke tests for the opt-in evaluation runner; NOT a model benchmark."""
import json
import pathlib
import sys
import tempfile
import unittest
from run_evals import ROOT, build_prompt, execute, common_task_sha256

class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"][0]
    def test_same_fixtures_both_conditions(self):
        a=build_prompt(self.case, "without_skill")
        b=build_prompt(self.case, "with_skill")
        self.assertIn("=== BEGIN INPUT FILE: fixtures/landing-generic.html ===",a)
        self.assertIn("=== BEGIN INPUT FILE: fixtures/landing-generic.html ===",b)
        self.assertIn("R$ 19,90",a)
        self.assertIn("R$ 19,90",b)
        self.assertNotIn("Design OS Prime v",a)
        self.assertIn("Design OS Prime v",b)
        self.assertIn("TRUSTED ADAPTIVE STRATEGY HYPOTHESIS",b)
        self.assertIn("CANDIDATE_NOT_INSPECTED",b)
        self.assertNotIn("TRUSTED ADAPTIVE STRATEGY HYPOTHESIS",a)
    def test_redesign_loads_applied_design_decisions(self):
        b=build_prompt(self.case,"with_skill")
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/applied-design-decisions.md",b)

    def test_operational_case_prioritizes_data_dense_ui_knowledge(self):
        cases=json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
        case=next(c for c in cases if c["id"]==22)
        b=build_prompt(case,"with_skill")
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/advanced-product-ux-operations.md",b)
        self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/anti-slop-composition.md",b)

    def test_experimental_art_director_is_loaded_not_commercial_playbook(self):
        cases=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))["evals"]
        case=next(c for c in cases if c["id"]==37)
        prompt=build_prompt(case,"with_skill")
        self.assertIn("references/creative-experience-direction.md",prompt)
        self.assertIn('"creative_authority": "ART_DIRECTOR_FIRST"',prompt)

    def test_experiential_commerce_prompt_keeps_art_and_product(self):
        case={"prompt":"Crie landing comercial experimental Awwwards para uma caixa de som de luxo",
              "files":[],"meta":{"surface":["experience","landing"]}}
        prompt=build_prompt(case,"with_skill")
        self.assertIn('"creative_authority": "EXPERIENTIAL_COMMERCE"',prompt)
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/experiential-commerce.md",prompt)
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/product-truth.md",prompt)
        self.assertIn('"conversion"',prompt)

    def test_creative_challenger_loaded_without_polluting_operational_ui(self):
        case={"prompt":"Crie uma landing comercial 3D para uma caixa de som de luxo",
              "files":[],"meta":{"surface":["experience","landing"]}}
        prompt=build_prompt(case,"with_skill")
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/creative-advantage-loop.md",prompt)
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/immersive-3d-product-direction.md",prompt)
        cases=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))["evals"]
        case=next(c for c in cases if c["name"]=="Do not apply immersion rituals to an internal finance dashboard")
        operational=build_prompt(case,"with_skill")
        self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/creative-advantage-loop.md",operational)
        self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/immersive-3d-product-direction.md",operational)

    def test_v11_creative_guides_really_injected(self):
        cases=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))["evals"]
        case=next(c for c in cases if c["id"]==51)
        b=build_prompt(case,"with_skill")
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/creative-signature-and-form.md",b)
        self.assertIn("TRUSTED CONTEXTUAL REFERENCE: references/interaction-dramaturgy-and-payoff.md",b)
        self.assertNotIn("TRUSTED CONTEXTUAL REFERENCE: references/creative-signature-and-form.md",
                         build_prompt(case,"without_skill"))

    def test_isolated_workspaces_do_not_share_mutations(self):
        with tempfile.TemporaryDirectory() as d:
            code = ("import pathlib,sys; p=pathlib.Path('mutation.txt'); "
                    "print('SEEN' if p.exists() else 'CLEAN'); p.write_text('created')")
            command=[sys.executable,"-c",code]
            a=execute(self.case,"without_skill",command,10,pathlib.Path(d))
            b=execute(self.case,"with_skill",command,10,pathlib.Path(d))
            first=json.loads(pathlib.Path(a["path"]).read_text(encoding="utf-8"))
            second=json.loads(pathlib.Path(b["path"]).read_text(encoding="utf-8"))
            self.assertIn("CLEAN",first["stdout"])
            self.assertIn("CLEAN",second["stdout"])
            self.assertEqual(first["fixture_sha256"],second["fixture_sha256"])
            self.assertEqual(first["task_input_sha256"],second["task_input_sha256"])
            self.assertEqual(first["task_input_sha256"],common_task_sha256(self.case))
            self.assertNotEqual(first["assembled_prompt_sha256"],second["assembled_prompt_sha256"])
            self.assertEqual(second["skill_delivery"],"INLINE_IN_AGENT_INPUT_NOT_CONFIRMED_READ")
            self.assertIn("references/applied-design-decisions.md",second["loaded_portable_references"])
            self.assertTrue(first["workspace_isolated"])
            self.assertTrue(second["workspace_isolated"])
    def test_records_outputs_without_grading(self):
        with tempfile.TemporaryDirectory() as d:
            output=execute(self.case,"without_skill",
                [sys.executable,"-c","import sys; print('ACK', len(sys.stdin.read()))"],
                10,pathlib.Path(d))
            saved=json.loads(pathlib.Path(output["path"]).read_text(encoding="utf-8"))
            self.assertEqual(saved["exit_code"],0)
            self.assertIn("ACK",saved["stdout"])
            self.assertEqual(saved["independent_human_review"],"NOT_PERFORMED")

if __name__ == "__main__":
    unittest.main()
