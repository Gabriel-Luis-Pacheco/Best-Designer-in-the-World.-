"""Tests for structural art-direction gate. Run: python -m unittest tests.test_hero_taste_gate"""
import copy
import importlib.util
import struct
import tempfile
import zlib
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation/scripts/hero_taste_gate.py"
spec = importlib.util.spec_from_file_location("hero_taste_gate", MODULE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def packet():
    def ref(i, lane):
        return {
            "url": f"https://example.org/{lane}/{i}",
            "observed_date": "2026-11-22",
            "desktop": "evidence/desktop.png",
            "mobile": "evidence/mobile.png",
            "decision": "ADAPT",
            "observed_mechanism": "Strong single proof scene supported by a short category headline",
            "original_application": "Feature an authentic focused product scene, not their brand assets",
            "caveat": "No published conversion result was inspected or verified"
        }
    return {
        "schema_version": 1, "mode": "REDESIGN", "surface": "marketing", "route": "/schools",
        "brief": {"audience": "School owners who purchase a speaking practice pilot",
                  "offer": "A real pilot proposal with verified written terms",
                  "primary_cta": "Request a real classroom pilot through contact form",
                  "first_value": "Teacher and students complete a real voice conversation",
                  "brand_constraints": "Keep factual prices, identity and authorized assets"},
        "research": {"direct_competitors": [ref(i, "direct") for i in range(8)],
                     "cross_category": [ref(i, "adjacent") for i in range(2)],
                     "shortfall_reason": "", "cross_category_shortfall_reason": ""},
        "concepts": [
            {"id": "focus", "visual_thesis": "Single large genuine speaking turn contrasted against a quiet copy block",
             "primary_focus": "One large real voice conversation rather than a dashboard collage",
             "removed_or_deferred": "Defer extra stats and tiny annotations below the first fold",
             "mobile_recomposition": "Crop conversation to one legible turn and keep the CTA next"},
            {"id": "editorial", "visual_thesis": "Large human classroom context with restrained conversation inset",
             "primary_focus": "An authentic moment from a student learning context and clear category copy",
             "removed_or_deferred": "Remove competing floating labels and three mini KPI cards",
             "mobile_recomposition": "Place the scene after the promise, with full text sizing"}],
        "chosen_concept": "focus",
        "render": {"before": {"desktop": "evidence/desktop.png", "mobile": "evidence/mobile.png"},
                   "after": {"desktop": "evidence/desktop.png", "mobile": "evidence/mobile.png"}},
        "review": {"reviewer_type": "SELF_REVIEW", "verdict": "PASS",
                   "squint_focal_order": "Dominant conversation followed by one offer and one visible primary action",
                   "signal_noise_review": "The KPI chips and decorative annotations were removed or deferred",
                   "reference_contrast": "Compared product-led and editorial hero mechanisms and rejected generic cards",
                   "mobile_review": "Real reflow and primary action were checked at phone viewport",
                   "decision_reason": "This is an agent judgment; no blinded reviewer approved the design",
                   "removal_log": ["Removed distracting three-stat block from first viewport"],
                   "critical_findings": []},
        "journey": {"status": "PASS", "evidence_path": "evidence/journey.txt"}
    }


class GateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "evidence").mkdir()
        # Valid 1x1 RGBA PNG with real IHDR/IDAT/IEND chunks and CRC.
        def chunk(kind, body):
            data = kind + body
            return struct.pack(">I", len(body)) + data + struct.pack(">I", zlib.crc32(data))
        ihdr = struct.pack(">2I5B", 1, 1, 8, 6, 0, 0, 0)
        png = (bytes.fromhex("89504e470d0a1a0a")
               + chunk(b"IHDR", ihdr)
               + chunk(b"IDAT", zlib.compress(b"\\x00\\x00\\x00\\x00\\xff"))
               + chunk(b"IEND", b""))
        for name in ("desktop.png", "mobile.png"):
            (self.root / "evidence" / name).write_bytes(png)
        (self.root / "evidence/journey.txt").write_text("Manually executed actual real CTA flow")

    def tearDown(self):
        self.temp.cleanup()

    def test_a_complete_self_review_is_not_human_approval(self):
        result = gate.inspect(packet(), self.root)
        self.assertEqual(result["status"], "READY_FOR_HUMAN_REVIEW")
        self.assertTrue(any("Not human" in w for w in result["warnings"]))

    def test_critical_visual_issue_blocks_shipping(self):
        p = packet()
        p["review"]["critical_findings"] = [
            {"severity": "P1", "description": "Three equally prominent competing focal regions remain", "resolved": False}
        ]
        self.assertEqual(gate.inspect(p, self.root)["status"], "ART_DIRECTION_BLOCKED")

    def test_missing_captures_are_not_approved(self):
        p = packet()
        p["render"]["after"]["mobile"] = "missing.png"
        self.assertEqual(gate.inspect(p, self.root)["status"], "NEEDS_EVIDENCE")

    def test_wrong_research_cannot_be_passed_with_a_url_only(self):
        p = packet()
        p["research"]["direct_competitors"][0]["observed_mechanism"] = ""
        self.assertEqual(gate.inspect(p, self.root)["status"], "NEEDS_EVIDENCE")

    def test_reported_rework_blocks(self):
        p = packet()
        p["review"]["verdict"] = "REWORK"
        self.assertEqual(gate.inspect(p, self.root)["status"], "ART_DIRECTION_BLOCKED")

    def test_journey_failure_blocks(self):
        p = packet()
        p["journey"]["status"] = "FAIL"
        self.assertEqual(gate.inspect(p, self.root)["status"], "ART_DIRECTION_BLOCKED")


if __name__ == "__main__":
    unittest.main()
