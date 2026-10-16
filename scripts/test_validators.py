#!/usr/bin/env python3
"""Dependency-free tests of metadata, portability, and review integrity."""
import copy
import json
import pathlib
import tempfile
import unittest
from check_evals import ROOT, SKILL, safe_input_path, validate, validate_case
from score_review import validate_review
from compare_reviews import compare

class ValidationTests(unittest.TestCase):
    def test_repository_structural_validation(self):
        summary = validate()
        self.assertGreaterEqual(summary["cases"], 16)
        self.assertEqual(summary["version"], "8.0.0")
    def test_case_rejects_traversal(self):
        source = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"][0]
        case = copy.deepcopy(source)
        case["files"] = ["../SKILL.md"]
        with self.assertRaises(ValueError):
            validate_case(case, SKILL)
    def test_case_accepts_fixture(self):
        self.assertTrue(safe_input_path(SKILL, "fixtures/landing-generic.html").is_file())
    def test_case_rejects_nonexistent_fixture(self):
        with self.assertRaises(ValueError):
            safe_input_path(SKILL, "fixtures/missing.html")
    def sample_review(self, variant):
        return {"case_id":1,"variant":variant,"run_id":"synthetic-" + variant, "pair_id":"synthetic-pair-001",
                "reviewer":"example-reviewer","scores":{"clareza":2,"mobile":1},
                "evidence":["tests/example-evidence-placeholder"],"blockers":[],
                "assertions":[{"text":"Form is present","result":"PASS","evidence":"example check"}]}
    def test_review_accepts_anchored_scores(self):
        self.assertEqual(validate_review(self.sample_review("with_skill"))["scores"]["clareza"],2)
    def test_review_rejects_unknown_dimension(self):
        r=self.sample_review("with_skill");r["scores"]["looks_magical"]=3
        with self.assertRaises(ValueError):validate_review(r)
    def test_comparison_rejects_mismatched_dimensions(self):
        a=self.sample_review("with_skill");b=self.sample_review("without_skill")
        b["scores"]["composicao"]=2
        result=compare([a,b])
        self.assertEqual(result["paired_cases"],0)
        self.assertEqual(result["excluded"][0]["reason"],"rated dimensions differ")
    def test_comparison_rejects_unpaired_reviewer(self):
        a=self.sample_review("with_skill");b=self.sample_review("without_skill")
        b["reviewer"]="someone-else"
        self.assertEqual(compare([a,b])["paired_cases"],0)
    def test_review_rejects_old_scale(self):
        r=self.sample_review("with_skill");r["scores"]["mobile"]=4
        with self.assertRaises(ValueError):validate_review(r)
    def test_review_requires_evidence(self):
        r=self.sample_review("with_skill");r["evidence"]=[]
        with self.assertRaises(ValueError):validate_review(r)
    def test_review_rejects_bool_score(self):
        r=self.sample_review("with_skill");r["scores"]["mobile"]=True
        with self.assertRaises(ValueError):validate_review(r)
    def test_unpaired_not_counted(self):
        self.assertEqual(compare([self.sample_review("with_skill")])["paired_cases"],0)
    def test_paired_comparison_is_descriptive(self):
        self.assertEqual(compare([self.sample_review("with_skill"),self.sample_review("without_skill")])["paired_cases"],1)

if __name__ == "__main__":
    unittest.main()
