"""Adversarial JSON-shaped input coverage for portable V12/V13 validators.

A malformed external packet should produce INVALID/REVIEW, never crash with an
unhandled TypeError. Tests are deliberately independent of a real website.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "studio-grade-web-transformation" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location("v14_" + name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {name: load(name) for name in (
    "brief_alignment", "review_council", "positioning_copy_contract",
    "creative_concept_gate", "cinematic_timeline", "learning_ledger",
    "production_evidence", "asset_provenance", "search_presence_audit",
)}


class InvalidInputSafety(unittest.TestCase):
    def test_nonobject_top_level_never_crashes(self):
        bad = (None, [], "", 0, 1, True, False)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name, module in MODULES.items():
                if name == "search_presence_audit":
                    continue
                for x in bad:
                    with self.subTest(name=name, value=x):
                        report = module.inspect(x, root) if name in (
                            "production_evidence", "asset_provenance") else module.inspect(x)
                        self.assertEqual(report["status"], "INVALID")

    def test_malformed_fields_never_raise(self):
        items = [
            ("brief_alignment", {"mode": [], "original_brief": "x",
                 "requirements": [{"id": "one", "text": "Some original requested feature",
                                   "priority": [], "exact_referent": {"name": "Thing", "canonical_source": "source",
                                   "distinctive_traits": ["g"], "rights": []}}],
                 "checkpoints": [{"stage": "RELEASE", "re_read_original": True,
                                  "checks": [{"requirement_id": [], "result": ["PASS"]}]}],
                 "proposed_deviations": [{"requirement_id": []}]}),
            ("positioning_copy_contract", {"audience": {}, "competitive_alternatives": [],
                  "market_category": "category", "proofs": [{"id": "p", "status": [], "source": "source file"}],
                  "differentiators": [{"capability": "real capability", "alternative_gap": "actual difference",
                                      "customer_outcome": "meaningful result", "proof_ids": [[]]}],
                  "message": {"headline": "some text", "subheadline": "some text",
                              "primary_cta": "Continue", "cta_destination": "/go",
                              "claims": [{"text": "An asserted claim", "proof_ids": [[]]}]}}),
            ("review_council", {"surface": "landing", "mode": "REBUILD",
                               "reviews": [{"role": [], "review_mode": [], "findings": []}]}),
            ("creative_concept_gate", {"facts": [{"id": [], "claim": "claim", "source": "source"}],
                                       "directions": [{"id": [], "evidence_ids": [[]]}]}),
            ("cinematic_timeline", {"scenes": [{"id": [], "beat": [], "engine": [],
                                                "trigger": [], "duration_ms": 0}],
                                    "runtime": {}}),
            ("learning_ledger", {"hypothesis": "An explicit and falsifiable product hypothesis",
                                 "tests": [{"project_id": "p", "task_hash": "h", "run_id": "r",
                                            "outcome": [], "matched_conditions": True}]}),
            ("production_evidence", {"mode": [], "surface": [], "scenes": [],
                                     "checks": [{"id": "x", "status": []}], "blockers": []}),
            ("asset_provenance", {"assets": [{"id": "x", "role": [], "rights": [],
                                            "source": "source", "paths": []}]}),
        ]
        with tempfile.TemporaryDirectory() as d:
            for name, value in items:
                with self.subTest(name=name):
                    module = MODULES[name]
                    result = module.inspect(value, Path(d)) if name in (
                        "asset_provenance", "production_evidence") else module.inspect(value)
                    self.assertEqual(result["status"], "INVALID", result)

    def test_html_parser_accepts_boolean_attrs_without_crashing(self):
        seo = MODULES["search_presence_audit"]
        source = '<head><meta name=description content><link rel></head><body><a href>Link</a></body>'
        report = seo.inspect({"test.html": source})
        self.assertEqual(report["status"], "STATIC_REVIEW_ONLY")

    def test_superlative_100_percent_without_extra_words_flagged(self):
        copy = MODULES["positioning_copy_contract"]
        pattern = copy.ABSOLUTE
        self.assertTrue(pattern.search("100% satisfied"))
        self.assertTrue(pattern.search("#1 worldwide"))


if __name__ == "__main__":
    unittest.main()
