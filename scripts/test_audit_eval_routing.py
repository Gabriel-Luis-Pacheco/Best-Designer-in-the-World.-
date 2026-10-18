"""Prevent silent loss of actual reference injection, not a visual benchmark."""
import json
import unittest
from audit_eval_routing import audit
from run_evals import ROOT

class RoutingCoverageTests(unittest.TestCase):
    def test_every_synthetic_brief_has_consistent_treatment(self):
        cases=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))["evals"]
        result=audit(cases)
        self.assertEqual(result["checked"],len(cases))
        self.assertEqual(result["failures"],[],result["failures"])
        self.assertGreaterEqual(len(result["cases"]),61)
        self.assertIn("SOURCE_ONLY",result["status"])
    def test_negative_contract_shows_no_art_stuff_in_dashboard(self):
        case={"id":999,"name":"Dashboard","prompt":"Corrija um filtro no dashboard financeiro",
              "files":[],"meta":{"surface":"internal"}}
        x=audit([case])
        self.assertEqual(x["failures"],[])
        self.assertNotIn("references/creative-advantage-loop.md",x["cases"][0]["selected_refs"])
if __name__=="__main__":
    unittest.main()
