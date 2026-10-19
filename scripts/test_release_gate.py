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

    def test_optional_real_evidence_verification(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            self.assertEqual(mod.assess(self.base(),root)["decision"],"BLOCK")
            (root/"proof").mkdir()
            (root/"proof/test-log.txt").write_text("PASS",encoding="utf-8")
            result=mod.assess(self.base(),root)
            self.assertEqual(result["decision"],"READY_FOR_HUMAN_REVIEW")
            self.assertEqual(result["file_evidence_verified"],1)
            bad=self.base();bad["checks"][0]["evidence"]=["../../etc/passwd"]
            self.assertEqual(mod.assess(bad,root)["decision"],"BLOCK")
            (root/"proof/test-log.txt").write_text("",encoding="utf-8")
            self.assertEqual(mod.assess(self.base(),root)["decision"],"BLOCK")
