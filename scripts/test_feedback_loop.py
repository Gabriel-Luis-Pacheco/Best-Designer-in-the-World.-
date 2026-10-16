import importlib.util
import pathlib
import unittest
p=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/brain/feedback_loop.py"
spec=importlib.util.spec_from_file_location("brain_feedback",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class FeedbackTests(unittest.TestCase):
    def event(self,base,after,role="primary",evidence="tests/local-measurement.csv"):
        return {"metric":"rate","direction":"up","role":role,"baseline":base,"after":after,"sample":100,"evidence":evidence}
    def test_missing_measurement_stays_unknown(self):
        r=m.summarize({"version":1,"goal":"activation","observations":[self.event(None,None)]})
        self.assertEqual(r["decision"],"INSUFFICIENT_EVIDENCE")
    def test_observed_gain_not_called_causal(self):
        r=m.summarize({"version":1,"goal":"activation","observations":[self.event(4,6)]})
        self.assertEqual(r["observed"][0]["status"],"IMPROVED_OBSERVED")
        self.assertIn("not causal",r["limitations"])
    def test_guardrail_regression_blocks_optimism(self):
        r=m.summarize({"version":1,"goal":"activation","observations":[self.event(5,3,"guardrail")]})
        self.assertEqual(r["decision"],"INVESTIGATE_GUARDRAIL_REGRESSION")
    def test_unproven_evidence_stays_unknown(self):
        r=m.summarize({"version":1,"goal":"retention","observations":[self.event(1,2,evidence="")]})
        self.assertEqual(r["decision"],"INSUFFICIENT_EVIDENCE")
