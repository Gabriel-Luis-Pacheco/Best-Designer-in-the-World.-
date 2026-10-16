"""Read-only project intake regression tests. No network or JS execution."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("design_intake",ROOT/"brain/project_intake.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class IntakeTests(unittest.TestCase):
    def test_inventory_detects_routes_assets_and_scripts_without_secret_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"src/app").mkdir(parents=True)
            (root/"public").mkdir()
            (root/"node_modules/ignored").mkdir(parents=True)
            (root/"src/app/page.tsx").write_text("export default function Page(){}",encoding="utf-8")
            (root/"public/logo.svg").write_text("<svg/>",encoding="utf-8")
            (root/".env").write_text("SECRET=do-not-print",encoding="utf-8")
            (root/"node_modules/ignored/page.tsx").write_text("bad",encoding="utf-8")
            (root/"package.json").write_text(json.dumps({
                "dependencies":{"next":"15.0.0","react":"19.0.0"},
                "scripts":{"dev":"next dev","test":"jest"}
            }),encoding="utf-8")
            result=mod.inspect_project(root)
            self.assertIn("Next.js",result["framework_hints"])
            self.assertIn("src/app/page.tsx",result["route_file_candidates"])
            self.assertIn("public/logo.svg",result["brand_asset_candidates"])
            self.assertIn("test",result["package_script_names"])
            self.assertNotIn("do-not-print",str(result))
            self.assertNotIn("ignored",str(result))
            self.assertEqual(result["evidence_level"],"FILE_INVENTORY_ONLY")
    def test_empty_workspace_is_not_misrepresented_as_ui_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=mod.build_plan({"task":"Melhore a landing comercial","surface":"landing"},tmp)
            self.assertEqual(r["project_inventory"]["file_count_sampled"],0)
            self.assertEqual(r["strategy"]["measurement_status"],"NOT_MEASURED")
            self.assertTrue(any("No rendered UI" in s for s in r["project_inventory"]["limits"]))
    def test_not_directory_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"file"
            path.write_text("x")
            with self.assertRaises(ValueError):mod.inspect_project(path)
