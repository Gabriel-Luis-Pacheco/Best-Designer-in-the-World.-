import importlib.util
import pathlib
import unittest
path=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts/release_gate.py"
spec=importlib.util.spec_from_file_location("release_gate",path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class GateTests(unittest.TestCase):
    def base(self,status="PASS"):
        return {"version":1,"checks":[{"id":"flow","severity":"P0","result":status,"evidence":["proof/test-log.txt"]}]}
    def test_missing_critical_flow_blocks(self):
        self.assertEqual(mod.assess(self.base("UNKNOWN"))["decision"],"BLOCK")
    def test_failed_p1_blocks(self):
        a=self.base();a["checks"].append({"id":"focus","severity":"P1","result":"FAIL"})
        self.assertEqual(mod.assess(a)["decision"],"BLOCK")
    def test_pass_requires_evidence(self):
        a=self.base();a["checks"][0]["evidence"]=[]
        with self.assertRaises(ValueError):mod.assess(a)
    def test_all_pass_is_human_review_only(self):
        self.assertEqual(mod.assess(self.base())["decision"],"READY_FOR_HUMAN_REVIEW")
    def test_p2_unknown_warning(self):
        a=self.base();a["checks"].append({"id":"craft","severity":"P2","result":"UNKNOWN"})
        self.assertEqual(mod.assess(a)["decision"],"REVIEW_WITH_WARNINGS")
