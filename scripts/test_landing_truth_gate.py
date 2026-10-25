"""Unit tests for optional evidence-to-scene contract gate."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SK=ROOT/"skills/studio-grade-web-transformation"
sys.path.insert(0,str(SK/"scripts"))
from landing_truth_gate import audit,valid_href

class TestLandingTruthGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=json.loads((SK/"templates/LANDING_EVIDENCE_PACKET.json").read_text(encoding="utf-8"))
    def test_synthetic_fixture(self):
        r=audit(self.template)
        self.assertEqual(r["status"],"DECLARATIONS_CHECKED",r)
    def test_prod_claim_unverified(self):
        x=copy.deepcopy(self.template);x["mode"]="production"
        self.assertEqual(audit(x)["status"],"BLOCKED")
    def test_unsafe_cta(self):
        self.assertFalse(valid_href("javascript:alert(1)"))
        self.assertFalse(valid_href("//evil.example"))
        x=copy.deepcopy(self.template);x["primary_cta"]["href"]="javascript:alert(1)"
        self.assertEqual(audit(x)["status"],"BLOCKED")
    def test_repeated_scene(self):
        x=copy.deepcopy(self.template)
        x["scenes"][1]["new_information"]=x["scenes"][0]["new_information"]
        r=audit(x)
        self.assertEqual(r["status"],"REVIEW_REQUIRED")
        self.assertTrue(any("CUT/MERGE" in q for q in r["warnings"]))
    def test_webgl_fallback(self):
        x=copy.deepcopy(self.template);x["mode"]="production"
        x["evidence"][0]["status"]="verified";x["scenes"][0]["medium"]="webgl"
        self.assertTrue(any("fallback" in q for q in audit(x)["errors"]))
    def test_missing_source_id(self):
        x=copy.deepcopy(self.template);x["claims"][0]["evidence_ids"]=["not-found"]
        self.assertEqual(audit(x)["status"],"BLOCKED")
if __name__=="__main__": unittest.main()
