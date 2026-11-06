"""Quality controller integration tests; real artifacts, no invented site claims."""
from __future__ import annotations
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "skills" / "studio-grade-web-transformation" / "scripts"
spec = importlib.util.spec_from_file_location("quality_controller_v14", ROOT / "quality_controller.py")
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class UnifiedQualityTests(unittest.TestCase):
    def test_significant_rebuild_cannot_pass_without_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            data = {"mode": "REBUILD", "surface": "landing", "public": True}
            result = controller.inspect(data, Path(directory))
            self.assertEqual(result["status"], "INCOMPLETE")
            self.assertEqual({g["gate"] for g in result["gates"]},
                {"brief", "production", "reviews", "positioning", "public_seo"})

    def test_empty_patch_not_misrepresented_as_qa(self):
        with tempfile.TemporaryDirectory() as directory:
            data = {"mode": "PATCH", "surface": "product", "public": False}
            result = controller.inspect(data, Path(directory))
            self.assertEqual(result["status"], "INCOMPLETE")
            self.assertIn("No gate executed", result["unverified_or_missing"][0])

    def test_public_noindex_is_blocking_not_an_seo_score(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text(
                '<html lang="en"><head><title>Public landing</title>'
                '<meta name="robots" content="noindex"></head>'
                '<body><h1>Public landing</h1></body></html>',
                encoding="utf-8")
            result = controller.inspect({
                "mode": "PATCH", "surface": "landing", "public": True,
                "html_pages": ["index.html"],
            }, root)
            self.assertEqual(result["status"], "BLOCKED")

    def test_unsafe_path_cannot_escape_project(self):
        with tempfile.TemporaryDirectory() as directory:
            result = controller.inspect({
                "mode": "PATCH", "surface": "landing", "public": True,
                "html_pages": ["../missing.html"],
            }, Path(directory))
            self.assertEqual(result["status"], "INVALID")

    def test_wrong_config_types_fail_as_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            result = controller.inspect({"mode": [], "surface": "landing",
                                         "public": "yes"}, Path(directory))
            self.assertEqual(result["status"], "INVALID")

    def test_structural_packet_is_not_a_certification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            brief = {"mode": "REFINE", "original_brief": "Make the contact button easier to use.",
                     "requirements": [{"id": "button", "text": "Improve the contact button",
                                       "priority": "MUST"}],
                     "checkpoints": [{"stage": "RELEASE", "re_read_original": True,
                                      "checks": [{"requirement_id": "button", "result": "PASS",
                                                  "evidence": ["captures/button.png"]}]}]}
            (root / "brief.json").write_text(json.dumps(brief), encoding="utf-8")
            result = controller.inspect({"mode": "REFINE", "surface": "product",
                                         "public": False, "brief": "brief.json"}, root)
            self.assertEqual(result["status"], "EVIDENCE_PACKET_FOR_HUMAN_REVIEW")
            self.assertIn("brief", result["human_review_required"])
            self.assertIn("No visual aesthetics", result["limitations"][-1])


if __name__ == "__main__":
    unittest.main()
