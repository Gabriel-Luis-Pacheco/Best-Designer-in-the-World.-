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
            "desktop": f"evidence/{lane}-{i}-desktop.png",
            "mobile": f"evidence/{lane}-{i}-mobile.png",
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
        "visual_transfer": {
            "source_url": "https://example.org/direct/0",
            "source_composition": "One dominant product frame set against a simple and short offer column",
            "target_composition": "Large real conversation frame, legible task and an unambiguous CTA",
            "originality_boundaries": "All colors, interface elements, characters and copy come from our own product",
            "side_by_side_observation": "Compared actual hierarchy, cropping, optical spacing and CTA prominence"
        },
        "render": {"before": {"desktop": "evidence/before-desktop.png", "mobile": "evidence/before-mobile.png"},
                   "after": {"desktop": "evidence/after-desktop.png", "mobile": "evidence/after-mobile.png"}},
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
        # Structurally valid, viewport-sized, individually distinct PNG fixtures.
        # This does NOT simulate a browser or certify the appearance of the image.
        def chunk(kind, body):
            data = kind + body
            return struct.pack(">I", len(body)) + data + struct.pack(">I", zlib.crc32(data))
        def png(width, height, seed):
            ihdr = struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0)
            rgba = bytes(((seed * 17) % 256, (seed * 31) % 256,
                          (seed * 43) % 256, 255))
            scanline = bytes([0]) + rgba * width
            return (bytes.fromhex("89504e470d0a1a0a")
                    + chunk(b"IHDR", ihdr)
                    + chunk(b"IDAT", zlib.compress(scanline * height))
                    + chunk(b"IEND", b""))
        paths = []
        for lane, count in (("direct", 8), ("adjacent", 2)):
            for i in range(count):
                for viewport in ("desktop", "mobile"):
                    paths.append(f"{lane}-{i}-{viewport}.png")
        for phase in ("before", "after"):
            for viewport in ("desktop", "mobile"):
                paths.append(f"{phase}-{viewport}.png")
        for seed, name in enumerate(paths, start=1):
            width, height = (900, 600) if "desktop" in name else (390, 700)
            (self.root / "evidence" / name).write_bytes(png(width, height, seed))
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

    def test_recycled_competitor_screenshots_cannot_pass_as_distinct_evidence(self):
        p = packet()
        p["research"]["direct_competitors"][1]["desktop"] = p["research"]["direct_competitors"][0]["desktop"]
        result = gate.inspect(p, self.root)
        self.assertEqual(result["status"], "NEEDS_EVIDENCE")
        self.assertTrue(any("identical" in x for x in result["missing"]))

    def test_same_before_and_after_pixels_cannot_support_a_redesign(self):
        p = packet()
        p["render"]["after"]["desktop"] = p["render"]["before"]["desktop"]
        result = gate.inspect(p, self.root)
        self.assertEqual(result["status"], "NEEDS_EVIDENCE")
        self.assertTrue(any("reused before/after" in x for x in result["missing"]))

    def test_tiny_artifacts_are_not_real_viewport_captures(self):
        p = packet()
        small = self.root / "evidence" / "tiny.png"
        original = (self.root / p["render"]["after"]["desktop"]).read_bytes()
        # Retain a valid PNG, but mark it as too narrow to represent desktop.
        small.write_bytes(original)
        p["render"]["after"]["mobile"] = "evidence/tiny.png"
        self.assertEqual(gate.inspect(p, self.root)["status"], "NEEDS_EVIDENCE")

    def test_reference_transfer_must_point_to_an_inspected_source(self):
        p = packet()
        p["visual_transfer"]["source_url"] = "https://unexamined.invalid"
        result = gate.inspect(p, self.root)
        self.assertEqual(result["status"], "NEEDS_EVIDENCE")
        self.assertTrue(any("source_url" in x for x in result["missing"]))


if __name__ == "__main__":
    unittest.main()
