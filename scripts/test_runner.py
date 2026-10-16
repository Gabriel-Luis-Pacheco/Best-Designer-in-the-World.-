"""Smoke tests for the opt-in evaluation runner; NOT a model benchmark."""
import json
import pathlib
import sys
import tempfile
import unittest
from run_evals import ROOT, build_prompt, execute

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
        self.assertNotIn("Design OS Prime v8",a)
        self.assertIn("Design OS Prime v8",b)
        self.assertIn("anti-slop-composition.md",b)
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
