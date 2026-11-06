"""Regression tests for v12 creative production contracts. No aesthetic claims."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "studio-grade-web-transformation" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location("v12_" + name, ROOT / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


concept = load("creative_concept_gate")
evidence = load("production_evidence")
assets = load("asset_provenance")
cinematic = load("cinematic_timeline")
learning = load("learning_ledger")


def png(color):
    def chunk(tag, body):
        return struct.pack(">I", len(body)) + tag + body + struct.pack(">I", zlib.crc32(tag + body))
    scan = b"\x00" + bytes(color)
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(scan)) + chunk(b"IEND", b""))


class ConceptTests(unittest.TestCase):
    def brief(self):
        return {"facts": [{"id": "f1", "claim": "A real supplied artifact", "source": "user brief"}],
                "directions": [
                    {"id": "a", "narrative": "A story of revealing the work", "spatial_grammar": "single immersive room",
                     "proof_mechanism": "interactive working sample", "interaction": "drag and reveal timeline",
                     "material": "soft volumetric material", "product_specific_mechanism": "Manipulate the actual editing timeline",
                     "evidence_ids": ["f1"]},
                    {"id": "b", "narrative": "A story through editorial case notes", "spatial_grammar": "structured reading columns",
                     "proof_mechanism": "before and after real samples", "interaction": "click to inspect cuts",
                     "material": "fine typographic grid", "product_specific_mechanism": "Compare original and edited scene",
                     "evidence_ids": ["f1"]}
                ]}

    def test_grounded_distinct_concepts(self):
        result = concept.inspect(self.brief())
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["errors"], [])

    def test_repeated_concept_does_not_pass(self):
        b = self.brief()
        for axis in concept.AXES:
            b["directions"][1][axis] = b["directions"][0][axis]
        self.assertEqual(concept.inspect(b)["status"], "INVALID")

    def test_unreferenced_fact_fails(self):
        b = self.brief()
        b["directions"][0]["evidence_ids"] = ["invented"]
        self.assertEqual(concept.inspect(b)["status"], "INVALID")

    def test_word_order_change_is_not_new_creative_direction(self):
        b = self.brief()
        a = b["directions"][0]
        c = b["directions"][1]
        for axis in concept.AXES:
            c[axis] = " ".join(reversed(a[axis].split()))
        c["product_specific_mechanism"] = " ".join(
            reversed(a["product_specific_mechanism"].split()))
        self.assertEqual(concept.inspect(b)["status"], "INVALID")


class EvidenceTests(unittest.TestCase):
    def test_production_packet_requires_actual_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "first.png").write_bytes(png((255, 0, 0, 255)))
            (root / "second.png").write_bytes(png((0, 0, 255, 255)))
            (root / "check.txt").write_text("Example check output")
            packet = {
                "mode": "REBUILD", "surface": "experience", "motion_fallback": "Provide accessible readable DOM content",
                "scenes": [{"id": s, "purpose": "Meaningful scene about authentic product",
                            "desktop": "first.png", "mobile": "second.png"}
                           for s in ("opening", "middle", "closing")],
                "checks": [{"id": c, "status": "PASS", "evidence": ["check.txt"]}
                           for c in evidence.CORE_CHECKS | evidence.EXPERIENCE_CHECKS],
                "iteration": {"scene_id": "middle", "cause": "Visual emphasis hid the actual product",
                              "change": "Replace decoration with real product imagery",
                              "before": "first.png", "after": "second.png"}
            }
            ok = evidence.inspect(packet, root)
            self.assertEqual(ok["status"], "EVIDENCE_READY_FOR_HUMAN_REVIEW")
            packet["iteration"]["after"] = "first.png"
            self.assertEqual(evidence.inspect(packet, root)["status"], "INVALID")
            packet["iteration"]["after"] = "second.png"
            (root / "check.txt").unlink()
            self.assertEqual(evidence.inspect(packet, root)["status"], "INVALID")

    def test_unknown_never_becomes_pass(self):
        with tempfile.TemporaryDirectory() as d:
            packet = {"mode": "PATCH", "surface": "product", "checks": [
                {"id": "keyboard", "status": "UNKNOWN", "reason": "No runtime was available"}]}
            self.assertEqual(evidence.inspect(packet, Path(d))["status"], "INCOMPLETE_UNKNOWN")

    def test_crc_corrupt_png_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "corrupt.png"
            good = bytearray(png((10, 10, 10, 255)))
            good[30] ^= 1
            p.write_bytes(good)
            with self.assertRaisesRegex(ValueError, "CRC"):
                evidence.artifact(Path(d), "corrupt.png", png=True)

    def test_evidenced_preservation_does_not_force_fake_rework(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "real.png").write_bytes(png((255, 0, 0, 255)))
            (root / "check.log").write_text("Existing scene already passed inspection")
            packet = {
                "mode": "REDESIGN", "surface": "landing",
                "scenes": [{"id": s, "purpose": "Show the genuine product and working action",
                            "desktop": "real.png", "mobile": "real.png"}
                           for s in ("opening", "middle", "closing")],
                "checks": [{"id": c, "status": "PASS", "evidence": ["check.log"]}
                           for c in evidence.CORE_CHECKS],
                "preserve_decision": {"decision": "PRESERVE",
                                      "reason": "Human reviewer inspected the complete useful site and found no material problem",
                                      "review_evidence": ["real.png", "check.log"]},
            }
            self.assertEqual(evidence.inspect(packet, root)["status"], "EVIDENCE_READY_FOR_HUMAN_REVIEW")
            packet["preserve_decision"]["review_evidence"] = ["missing.png"]
            self.assertEqual(evidence.inspect(packet, root)["status"], "INVALID")

    def test_wrong_types_report_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            packet = {"mode": "PATCH", "surface": "product", "checks": [
                {"id": "keyboard", "status": ["PASS"]}], "blockers": "bad"}
            self.assertEqual(evidence.inspect(packet, Path(d))["status"], "INVALID")


class AssetTests(unittest.TestCase):
    def test_canonical_byte_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "logo.svg").write_text("<svg>original</svg>")
            digest = hashlib.sha256((root / "logo.svg").read_bytes()).hexdigest()
            manifest = {"assets": [{"id": "logo", "role": "logo", "rights": "owned",
                "source": "supplied by owner", "canonical": True, "canonical_sha256": digest,
                "paths": ["logo.svg"]}]}
            self.assertEqual(assets.inspect(manifest, root)["status"], "INVENTORY_READY_FOR_RIGHTS_REVIEW")
            manifest["assets"][0]["canonical_sha256"] = "0" * 64
            self.assertEqual(assets.inspect(manifest, root)["status"], "INVALID")


class CinematicTests(unittest.TestCase):
    def test_cinematic_accessibility_contract(self):
        plan = {"scenes": [{"id": b, "beat": b, "engine": "css", "trigger": "scroll",
                            "duration_ms": 650, "payoff": "The real artwork changes context"}
                           for b in cinematic.BEATS],
                "runtime": {"time_owner": "Single scroll timeline owner",
                            "reduced_motion": "Static representative scene with identical content",
                            "no_gpu_fallback": "Provide semantic HTML with functional portfolio",
                            "mobile_direction": "Author mobile camera and crop independently",
                            "skip_or_replay": "Visible skip and replay controls",
                            "autoplay_audio": False, "audio_control": "No audio required"}}
        self.assertEqual(cinematic.inspect(plan)["status"], "PLAN_READY_FOR_PROTOTYPE")
        plan["runtime"]["autoplay_audio"] = True
        self.assertEqual(cinematic.inspect(plan)["status"], "INVALID")


class LearningTests(unittest.TestCase):
    def test_no_generalization_from_single_project(self):
        sample = {"hypothesis": "Opening with a real live demo improves product comprehension",
                  "tests": [{"project_id": "p1", "task_hash": "abc", "run_id": "r1",
                             "outcome": "WITH_SKILL", "matched_conditions": True,
                             "skill_read_confirmed": True, "rendered_artifacts": True,
                             "independent_blind_reviews": True, "evidence": ["path/to/proof"]}]}
        self.assertEqual(learning.inspect(sample)["status"], "PROJECT_LEVEL_HYPOTHESIS_ONLY")
        second = dict(sample["tests"][0], project_id="p2", task_hash="def", run_id="r2")
        sample["tests"].append(second)
        self.assertEqual(learning.inspect(sample)["status"], "HUMAN_REVIEW_CANDIDATE")
        sample["tests"][0]["matched_conditions"] = False
        self.assertEqual(learning.inspect(sample)["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
