"""Specialist routing is a bounded proposal, never an installer."""
import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
s=importlib.util.spec_from_file_location("specialist_router",ROOT/"brain/specialist_router.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class SpecialistRouterTests(unittest.TestCase):
    def test_cinematic_webgl(self):
        d=m.suggest({"task":"Crie experiência WebGL Three.js e GSAP","surface":"experience"})
        ids={x["id"] for x in d["specialists"]}
        self.assertIn("threejs",ids)
        self.assertIn("gsap",ids)
        self.assertLessEqual(len(ids),3)
    def test_landing_cro(self):
        d=m.suggest({"task":"Melhorar conversão de landing page","surface":"landing"})
        ids={x["id"] for x in d["specialists"]}
        self.assertIn("marketing-cro",ids)
        self.assertTrue(all(x["status"]=="CANDIDATE_NOT_INSTALLED_NOT_INSPECTED" for x in d["specialists"]))
    def test_patch_short_circuits(self):
        x=m.suggest({"task":"Corrija só padding do botão","mode":"PATCH","surface":"product"})
        self.assertEqual(x["specialists"],[])
    def test_internal_not_marketing(self):
        x=m.suggest({"task":"Melhore dashboard de dados","surface":"internal"})
        self.assertFalse(any(v["id"].startswith("marketing") for v in x["specialists"]))
    def test_negated_3d_request_not_a_positive_signal(self):
        d=m.suggest({"task":"Faça uma landing sem WebGL","max_specialists":3})
        self.assertNotIn("threejs",{x["id"] for x in d["specialists"]})
    def test_negated_gsap_not_a_positive_signal(self):
        d=m.suggest({"task":"Quero interface sem GSAP","max_specialists":3})
        self.assertNotIn("gsap",{x["id"] for x in d["specialists"]})
    def test_max_zero(self):
        x=m.suggest({"task":"GSAP","max_specialists":0})
        self.assertEqual(x["specialists"],[])
    def test_cannot_run_unbounded(self):
        with self.assertRaises(ValueError):m.suggest({"task":"GSAP","max_specialists":99})
if __name__=="__main__":unittest.main()
