"""The lightweight operational router should load only relevant existing guides."""
import importlib.util
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
spec=importlib.util.spec_from_file_location("design_workflow", ROOT/"design_workflow.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class DesignWorkflowTests(unittest.TestCase):
    def test_scope_and_action(self):
        report=mod.route("distill","marketing","PATCH")
        self.assertEqual(report["action"],"distill")
        self.assertEqual(report["mode"],"PATCH")
        self.assertFalse(report["missing_references"])
        self.assertLessEqual(len(report["guides"]),3)
    def test_alias_native(self):
        report=mod.route("responsive","native")
        self.assertEqual(report["action"],"adapt")
        self.assertIn("references/native-interface-discipline.md", report["guides"])
        self.assertEqual(report["status"],"ROUTING_ONLY_NOT_EXECUTED")
    def test_all_paths_exist(self):
        for operation in mod.OPERATIONS:
            for surface in mod.SURFACES:
                self.assertFalse(mod.route(operation,surface)["missing_references"],(operation,surface))
    def test_invalid_scope(self):
        with self.assertRaises(ValueError):
            mod.route("polish","product","WRITE_EVERYTHING")
    def test_no_fake_evaluation(self):
        self.assertNotIn("score",mod.route("critique","product"))
if __name__=="__main__":
    unittest.main()
