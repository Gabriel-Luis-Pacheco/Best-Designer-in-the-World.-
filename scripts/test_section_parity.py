"""Regression tests for section-by-section redesign evidence coverage."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import struct
import unittest
import zlib
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation/scripts/section_parity.py"
spec = importlib.util.spec_from_file_location("section_parity", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SectionParityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "images").mkdir()
        # Construct a valid one-pixel RGBA PNG with CRC-correct chunks.
        def chunk(tag, data):
            return (struct.pack(">I", len(data)) + tag + data +
                    struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
        ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
        png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
               chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00\xff")) +
               chunk(b"IEND", b""))
        for name in ("before-desktop.png", "before-mobile.png", "after-desktop.png", "after-mobile.png"):
            (self.root / "images" / name).write_bytes(png)
        (self.root / "flow.txt").write_text("Clicked CTA, visited first value, recorded result.", encoding="utf-8")
        self.packet = {
            "mode": "REDESIGN",
            "route": "/",
            "inventory": ["hero"],
            "sections": [{
                "id": "hero",
                "change": "REWORK",
                "purpose": "Show the real product and its essential action",
                "diagnosis": "The original hero did not demonstrate the core product.",
                "before": {
                    "desktop": "images/before-desktop.png",
                    "mobile": "images/before-mobile.png",
                },
                "after": {
                    "desktop": "images/after-desktop.png",
                    "mobile": "images/after-mobile.png",
                },
                "assessment": {
                    "verdict": "MIXED",
                    "reviewer_type": "AGENT_SELF_REVIEW",
                    "reason": "The proof is clearer but headline contrast needs review.",
                },
            }],
            "primary_journey": {
                "status": "PASS",
                "entry": "Click the practice button",
                "first_value": "Complete the first spoken interaction",
                "evidence": ["flow.txt"],
            },
            "critical_findings": [],
        }

    def test_complete_packet_is_only_ready_for_human_review(self):
        r = module.inspect(self.packet, self.root)
        self.assertEqual(r["status"], "READY_FOR_HUMAN_REVIEW")
        self.assertIn("no representative human", " ".join(r["warnings"]))
        self.assertEqual(r["sections_recorded"], 1)

    def test_unlisted_sections_are_invalid(self):
        p = copy.deepcopy(self.packet)
        p["inventory"] = ["hero", "pricing"]
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")

    def test_missing_mobile_capture_needs_evidence(self):
        p = copy.deepcopy(self.packet)
        del p["sections"][0]["after"]["mobile"]
        r = module.inspect(p, self.root)
        self.assertEqual(r["status"], "NEEDS_EVIDENCE")
        self.assertIn("after.mobile", " ".join(r["missing_evidence"]))

    def test_directory_traversal_is_rejected(self):
        p = copy.deepcopy(self.packet)
        p["sections"][0]["before"]["desktop"] = "../private.png"
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")

    def test_unreviewed_visual_better_claim_is_invalid(self):
        p = copy.deepcopy(self.packet)
        p["sections"][0]["assessment"]["verdict"] = "BETTER"
        p["sections"][0]["assessment"]["reviewer_type"] = "NOT_REVIEWED"
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")

    def test_unknown_verdict_needs_evidence(self):
        p = copy.deepcopy(self.packet)
        p["sections"][0]["assessment"]["verdict"] = "UNKNOWN"
        self.assertEqual(module.inspect(p, self.root)["status"], "NEEDS_EVIDENCE")

    def test_unresolved_critical_finding_blocks(self):
        p = copy.deepcopy(self.packet)
        p["critical_findings"] = [{"severity": "P1", "state": "OPEN"}]
        self.assertEqual(module.inspect(p, self.root)["status"], "BLOCKED")

    def test_failed_first_value_blocks(self):
        p = copy.deepcopy(self.packet)
        p["primary_journey"]["status"] = "FAIL"
        self.assertEqual(module.inspect(p, self.root)["status"], "BLOCKED")

    def test_removed_section_requires_why(self):
        p = copy.deepcopy(self.packet)
        p["sections"][0]["change"] = "REMOVE"
        p["sections"][0]["assessment"]["verdict"] = "SAME"
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")
        p["sections"][0]["removal_reason"] = "This block repeats the same verified proof as the hero."
        self.assertEqual(module.inspect(p, self.root)["status"], "READY_FOR_HUMAN_REVIEW")

    def test_invalid_screenshot_is_not_a_visual_review(self):
        p = copy.deepcopy(self.packet)
        (self.root / "images" / "after-mobile.png").write_text("not a screenshot")
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")

    def test_crc_invalid_png_is_rejected(self):
        p = copy.deepcopy(self.packet)
        target = self.root / "images" / "after-mobile.png"
        raw = bytearray(target.read_bytes())
        raw[25] ^= 1
        target.write_bytes(raw)
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")

    def test_malformed_json_types_do_not_crash(self):
        for key, value in (("mode", []), ("route", 7)):
            p = copy.deepcopy(self.packet)
            p[key] = value
            self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")
        p = copy.deepcopy(self.packet)
        p["sections"][0]["change"] = {}
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")
        p = copy.deepcopy(self.packet)
        p["sections"][0]["assessment"]["verdict"] = []
        self.assertEqual(module.inspect(p, self.root)["status"], "INVALID")

    def test_nonobject_packet_does_not_crash(self):
        self.assertEqual(module.inspect([], self.root)["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
