"""Tests evidence honesty of competitor screenshot and copy review packets."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec = importlib.util.spec_from_file_location("component_research_gate", BASE / "scripts" / "component_research_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def sample():
    return {
        "schema_version": 1, "component_id": "hero", "mode": "REDESIGN",
        "references": [{
            "url": "https://example.org", "kind": "DIRECT",
            "inspection_status": "NOT_INSPECTED", "observed_mechanism": "",
            "desktop_capture": None, "mobile_capture": None
        }],
        "benchmark": {"target": 10, "limitation_reason": "Browser unavailable"},
        "decisions": {"selected_mechanism": "Original demonstration of the key job",
                      "original_application": "Show actual working product in local brand",
                      "rejected_options": ["Generic cards"]},
        "implementation": {"changed_files": [], "before_capture": None,
                           "after_capture": None, "journey_status": "NOT_TESTED"},
        "editorial": {"status": "SELF_REVIEW_ONLY"}
    }


class ComponentEvidenceTests(unittest.TestCase):
    def test_missing_research_not_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = gate.inspect(sample(), Path(tmp))
            self.assertEqual(p["status"], "NEEDS_EVIDENCE")
            self.assertEqual(p["captured_references"], 0)

    def test_cannot_claim_capture_with_missing_file(self):
        data = sample()
        data["references"][0].update({"inspection_status": "CAPTURED",
                                      "inspection_date": "2026-11-21",
                                      "observed_mechanism": "Strong product proof in a clear hero",
                                      "desktop_capture": "screenshots/no.png"})
        with tempfile.TemporaryDirectory() as tmp:
            p = gate.inspect(data, Path(tmp))
            self.assertEqual(p["status"], "INVALID")
            self.assertIn("CAPTURED without actual image", " ".join(p["errors"]))

    def test_relative_path_traversal_refused(self):
        data = sample()
        data["references"][0].update({"inspection_status": "CAPTURED",
                                      "inspection_date": "2026-11-21",
                                      "observed_mechanism": "Visible product demo and CTA",
                                      "desktop_capture": "../../hidden.png"})
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(gate.inspect(data, Path(tmp))["status"], "INVALID")

    def test_duplicate_sources_and_false_human_approval_refused(self):
        data = sample()
        data["references"].append(dict(data["references"][0]))
        data["editorial"] = {"status": "HUMAN_REVIEWED"}
        with tempfile.TemporaryDirectory() as tmp:
            p = gate.inspect(data, Path(tmp))
            self.assertEqual(p["status"], "INVALID")
            self.assertIn("duplicate", " ".join(p["errors"]))
            self.assertIn("review_evidence", " ".join(p["errors"]))

    def test_existing_png_evidence_is_structurally_detected_not_certified(self):
        data = sample()
        data["references"][0].update({"inspection_status": "CAPTURED",
                                      "inspection_date": "2026-11-21",
                                      "observed_mechanism": "Actual demonstration precedes the next step",
                                      "desktop_capture": "test.png"})
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.png"
            p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 64)
            x = gate.inspect(data, Path(tmp))
            self.assertEqual(x["captured_references"], 1)
            self.assertEqual(x["status"], "NEEDS_EVIDENCE")
            self.assertIn("not proof", " ".join(x["limitations"]))

    def test_bad_schema_or_http_not_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = sample()
            data["schema_version"] = 2
            self.assertEqual(gate.inspect(data, Path(tmp))["status"], "INVALID")
            data = sample()
            data["references"][0]["url"] = "http://example.org"
            self.assertEqual(gate.inspect(data, Path(tmp))["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
