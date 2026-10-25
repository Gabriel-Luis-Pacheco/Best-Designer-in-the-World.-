"""Regressions for audit findings: 22 rubric axes, honest adapter and malformed JSON."""
import copy,importlib.util,json,sys,unittest
from pathlib import Path
from quality_schema import dimensions,load_schema
from review_adapter import to_league,to_paired
from score_review import validate_review
from compare_skill_league import validate_review as validate_league
ROOT=Path(__file__).resolve().parents[1];SK=ROOT/"skills/studio-grade-web-transformation"
sys.path.insert(0,str(SK/"scripts"))
from landing_truth_gate import audit,valid_href
spec=importlib.util.spec_from_file_location("audit_route",SK/"brain/route.py")
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
def paired():
    return {"case_id":1,"variant":"with_skill","run_id":"r1","pair_id":"p1","reviewer":"rater",
            "scores":{"hierarquia_de_atencao":3,"propriedade_fluxos":2,"direcao_arte":2},
            "evidence":["desktop.png"],"assertions":[],"blockers":[]}
def controls():
    return {"model":"m","model_revision":"r","budget_id":"b","tool_profile_id":"t","asset_set_id":"a"}
class AuditFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.template=json.loads((SK/"templates/LANDING_EVIDENCE_PACKET.json").read_text(encoding="utf-8"))
    def test_22_criteria_agree(self):
        self.assertEqual(len(dimensions()),22)
        self.assertEqual([len(x) for x in load_schema()["dimensions"].values()],[11,4,3,4])
        self.assertEqual(validate_review(paired())["scores"]["propriedade_fluxos"],2)
    def test_adapter_roundtrip(self):
        p=paired()
        q=to_league(p,trial_id="t1",task_sha256="a"*64,controls=controls(),system="design-os",blind=True)
        self.assertEqual(validate_league(q)["scores"],p["scores"])
        self.assertEqual(to_paired(q),p)
    def test_adapter_rejects_fake_provenance(self):
        with self.assertRaises(ValueError):
            to_league(paired(),trial_id="t",task_sha256="x",controls=controls(),system="design-os",blind=True)
        with self.assertRaises(ValueError):
            to_league(paired(),trial_id="t",task_sha256="a"*64,controls=controls(),system="design-os",blind=False)
    def test_malformed_claim_ids(self):
        for v in ([{}],[[]],None,10,["abc",{}]):
            x=copy.deepcopy(self.template);x["claims"][0]["evidence_ids"]=v
            self.assertEqual(audit(x)["status"],"BLOCKED")
    def test_malformed_scene_ids(self):
        for v in ([{}],None,7,{"x":"y"}):
            x=copy.deepcopy(self.template);x["scenes"][0]["evidence_ids"]=v
            self.assertEqual(audit(x)["status"],"BLOCKED")
    def test_cta_placeholder_rejected(self):
        self.assertFalse(valid_href("#"))
    def test_new_site_only_html_is_rebuild(self):
        for task in ("Faça um site apenas com HTML", "Faz um site só com CSS"):
            self.assertEqual(rt.route({"task":task})["strategy"]["mode"],"REBUILD")
    def test_colloquial_patch(self):
        self.assertEqual(rt.route({"task":"Só corrige um botão do checkout"})["strategy"]["mode"],"PATCH")
if __name__=="__main__":unittest.main()
