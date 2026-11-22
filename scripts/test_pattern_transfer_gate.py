"""Benchmark-first patterns must be observed, applied with fit, and not called validated without data."""
from __future__ import annotations

import importlib.util
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec = importlib.util.spec_from_file_location("pattern_transfer_gate", BASE / "scripts/pattern_transfer_gate.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def valid_png() -> bytes:
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00\xff")) + chunk(b"IEND", b""))


def research(*, status="CAPTURED", component="onboarding", kind="DIRECT"):
    return {
        "schema_version": 1, "component_id": component, "mode": "REDESIGN",
        "references": [{
            "url": "https://sample.org/onboarding", "kind": kind,
            "inspection_status": status,
            "inspection_date": "2026-11-22",
            "observed_mechanism": "A user completes a real guided task on the first session",
            "desktop_capture": "screens/first.png" if status == "CAPTURED" else None
        }]
    }


def transfer(*, component="onboarding"):
    return {
        "schema_version": 1, "component_id": component, "mode": "REDESIGN",
        "audience_job": "New user completing one real task after the first account registration.",
        "research_packet": "research.json",
        "baseline_choice": "Use a familiar low-friction first-value path, preserving safe skip and recovery.",
        "own_validation_plan": "Test authentic first-task completion, user understanding and errors on mobile.",
        "benchmark_access_limitation": "Only one comparable public flow was capturable using authorized access.",
        "candidate_patterns": [{
            "source_url": "https://sample.org/onboarding",
            "source_step": "After signup, before first guided task",
            "mechanism": "Allow the visitor to start the real core task without optional setup first.",
            "evidence_level": "OBSERVED_ONLY",
            "decision": "ADAPT",
            "fit_rationale": "Our new user has the same primary job, but fewer required profile inputs.",
            "original_implementation": "Apply our own interaction and brand with the equivalent first-task logic.",
            "known_risk": "Incomplete preferences could affect later personalization quality.",
            "test_plan": "Measure the first meaningful task and recovery without fabricating any lift."
        }]
    }


class PatternTransferTests(unittest.TestCase):
    def test_observed_copy_is_not_verified_conversion(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            result = mod.inspect(transfer(), root, research())
            self.assertEqual(result["status"], "READY_FOR_HUMAN_REVIEW")
            self.assertEqual(result["captured_direct_or_substitute"], 1)
            self.assertEqual(result["evidence_levels_declared"], {"OBSERVED_ONLY": 1})
            self.assertIn("not proof", " ".join(result["limitations"]).lower())

    def test_fake_success_lift_with_observed_only_is_invalid(self):
        obj = transfer()
        obj["candidate_patterns"][0]["conversion_lift"] = "80% uplift"
        with tempfile.TemporaryDirectory() as d:
            result = mod.inspect(obj, Path(d), research())
            self.assertEqual(result["status"], "INVALID")
            self.assertIn("cannot claim validated conversion", " ".join(result["errors"]))

    def test_competitor_url_must_be_in_research_packet(self):
        obj = transfer()
        obj["candidate_patterns"][0]["source_url"] = "https://not-inspected.org"
        with tempfile.TemporaryDirectory() as d:
            result = mod.inspect(obj, Path(d), research())
            self.assertEqual(result["status"], "INVALID")
            self.assertIn("absent from actual research", " ".join(result["errors"]))

    def test_uninspected_url_cannot_be_reported_as_observed(self):
        with tempfile.TemporaryDirectory() as d:
            result = mod.inspect(transfer(), Path(d), research(status="NOT_INSPECTED"))
            self.assertEqual(result["status"], "INVALID")
            self.assertIn("uninspected", " ".join(result["errors"]))

    def test_missing_capture_discloses_unvalidated_baseline(self):
        obj = transfer()
        obj["benchmark_access_limitation"] = "Public onboarding screens were unavailable and no account was authorized."
        with tempfile.TemporaryDirectory() as d:
            result = mod.inspect(obj, Path(d), research(status="INSPECTED_NO_CAPTURE"))
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertEqual(result["captured_sources"], 0)
            self.assertTrue(any("screenshot" in x for x in result["missing_evidence"]))

    def test_benchmark_shortfall_needs_explanation(self):
        obj = transfer()
        obj.pop("benchmark_access_limitation")
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            result = mod.inspect(obj, root, research())
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertIn("target benchmarks", " ".join(result["missing_evidence"]))

    def test_independent_evidence_requires_publication_and_scope(self):
        obj = transfer()
        obj["candidate_patterns"][0]["evidence_level"] = "INDEPENDENT_RESEARCH"
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            result = mod.inspect(obj, root, research())
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertIn("study URL", " ".join(result["missing_evidence"]))

    def test_published_numeric_result_must_have_population_and_period(self):
        obj = transfer()
        obj["candidate_patterns"][0].update({
            "evidence_level": "PUBLISHED_RESULT",
            "study_url": "https://journal.example.org/article",
            "reported_scope": "Equivalent digital onboarding with a documented task and participant group.",
            "reported_result": "Published effect on signup-to-first-value completion rate."
        })
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            result = mod.inspect(obj, root, research())
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertIn("population and period", " ".join(result["missing_evidence"]))

    def test_claiming_own_test_requires_real_artifact(self):
        obj = transfer()
        obj["candidate_patterns"][0].update({
            "evidence_level": "OWN_VERIFIED_TEST",
            "reported_population_and_period": "New first-time adult visitors during a documented launch period."
        })
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            result = mod.inspect(obj, root, research())
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertIn("own measured test", " ".join(result["missing_evidence"]))

    def test_no_adopt_or_adapt_requires_fallback_plan(self):
        obj = transfer()
        obj["candidate_patterns"][0]["decision"] = "REJECT"
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            result = mod.inspect(obj, root, research())
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertIn("No candidate pattern selected", " ".join(result["missing_evidence"]))

    def test_component_and_research_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(
                mod.inspect(transfer(component="checkout"), Path(d), research())["status"],
                "INVALID"
            )
            self.assertEqual(
                mod.inspect(transfer(component="dashboard"), Path(d), research())["status"],
                "INVALID"
            )

    def test_broken_png_cannot_count_as_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 110)
            result = mod.inspect(transfer(), root, research())
            self.assertEqual(result["status"], "NEEDS_EVIDENCE")
            self.assertEqual(result["captured_sources"], 0)

    def test_read_packet_from_real_document_path(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "screens").mkdir()
            (root / "screens/first.png").write_bytes(valid_png())
            (root / "research.json").write_text(json.dumps(research()), encoding="utf-8")
            result = mod.inspect(transfer(), root)
            self.assertEqual(result["status"], "READY_FOR_HUMAN_REVIEW")

    def test_no_url_based_sources_without_real_research(self):
        with tempfile.TemporaryDirectory() as d:
            result = mod.inspect(transfer(), Path(d))
            self.assertEqual(result["status"], "INVALID")
            self.assertIn("real existing research_packet", " ".join(result["missing_evidence"]))


if __name__ == "__main__":
    unittest.main()
