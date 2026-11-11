"""Context helper must preserve approved content and never self-certify."""
import importlib.util
import pathlib
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
spec=importlib.util.spec_from_file_location("design_context",ROOT/"design_context.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class DesignContextTests(unittest.TestCase):
    def test_create_only_preserve_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp)
            (root/"DESIGN.md").write_text("# APPROVED identity\nUser approved character",encoding="utf-8")
            result=mod.init(root)
            self.assertEqual(result["created"],["PRODUCT.md"])
            self.assertEqual(result["preserved"],["DESIGN.md"])
            self.assertIn("User approved character",(root/"DESIGN.md").read_text())
            self.assertEqual(mod.init(root)["created"],[])
    def test_missing_context_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            report=mod.status(pathlib.Path(tmp))
            self.assertEqual(report["documents"]["PRODUCT.md"]["status"],"MISSING")
            self.assertEqual(report["status"],"CONTEXT_INVENTORY_ONLY")
    def test_unverified_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            report=mod.init(pathlib.Path(tmp))
            self.assertGreater(report["documents"]["PRODUCT.md"]["unknown_count"],0)
            self.assertEqual(report["documents"]["DESIGN.md"]["status"],"PRESENT_UNVERIFIED")
if __name__=="__main__":
    unittest.main()
