"""Regression tests for experiment integrity; no false causal wins."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ab_guard",ROOT/"scripts/validate_experiment.py")
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
NAME=guard.NAME

class ABEvaluationTests(unittest.TestCase):
    def setup_pair(self,sha):
        common={"model":"Muse Spark","model_revision":"fixed","thinking_effort":"high",
                "settings":{"temperature":"default"},"prompt_sha256":"9"*64,
                "tool_profile":["editor","terminal","browser"],"budget":{"tokens":50000}}
        treatment={**common,"workspace_id":"a","skill_name":NAME,"skill_loaded":True,
                   "skill_sha256":sha,"other_design_skills":[],
                   "read_trace":[{"operation":"read_skill","skill_name":NAME,"content_sha256":sha}]}
        baseline={**common,"workspace_id":"b","skill_loaded":False,"loaded_design_skills":[]}
        return {"with_skill":treatment,"without_skill":baseline}
    def test_mirage_missing_skill_and_substitution_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"SKILL.md";path.write_text("real v9.7",encoding="utf-8")
            sha=hashlib.sha256(path.read_bytes()).hexdigest()
            pair=self.setup_pair(sha)
            pair["with_skill"]["skill_loaded"]=False
            pair["with_skill"]["other_design_skills"]=["frontend-design"]
            self.assertEqual(guard.check_pair(pair,path)["status"],"INVALID_COMPARISON")
    def test_claim_without_trace_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"SKILL.md";path.write_text("real v9.7",encoding="utf-8")
            pair=self.setup_pair(hashlib.sha256(path.read_bytes()).hexdigest())
            pair["with_skill"]["read_trace"]=[]
            self.assertEqual(guard.check_pair(pair,path)["status"],"INVALID_COMPARISON")
    def test_unmatched_context_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"SKILL.md";path.write_text("real v9.7",encoding="utf-8")
            pair=self.setup_pair(hashlib.sha256(path.read_bytes()).hexdigest())
            pair["without_skill"]["budget"]={"tokens":1000}
            self.assertEqual(guard.check_pair(pair,path)["status"],"INVALID_COMPARISON")
    def test_claimed_provenance_does_not_become_proven_outcome(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"SKILL.md";path.write_text("real v9.7",encoding="utf-8")
            pair=self.setup_pair(hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(guard.check_pair(pair,path)["status"],"READY_FOR_BLIND_REVIEW_NOT_PROVEN")
    def test_missing_skill_file_invalid(self):
        pair=self.setup_pair("a"*64)
        self.assertEqual(guard.check_pair(pair,"/does/not/exist")["status"],"INVALID_COMPARISON")

if __name__=="__main__":
    unittest.main()
