"""Negative and positive tests for the portable creative challenger."""
import importlib.util
import pathlib
import unittest

PATH = (pathlib.Path(__file__).resolve().parents[1] /
        "skills/studio-grade-web-transformation/brain/creative_direction_lab.py")
spec = importlib.util.spec_from_file_location("creative_direction_lab", PATH)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class CreativeDirectionLabTests(unittest.TestCase):
    def test_creative_directions_differ_materially(self):
        output = lab.propose({"task": "Crie landing", "product": "Aprendizado de inglês",
                              "surface": "landing", "real_action": "start a sample lesson"})
        self.assertEqual(output["status"], "PROPOSALS_NOT_RENDERED_NOT_TESTED")
        a, b = output["concepts"]
        self.assertNotEqual(a["composition"], b["composition"])
        self.assertNotEqual(a["signature_gesture"], b["signature_gesture"])
        self.assertNotEqual(a["visual_thesis"], b["visual_thesis"])
        self.assertEqual(set(a["scenes"]), set(lab.SCENE_KEYS))

    def test_no_unrequested_3d(self):
        out = lab.propose({"task": "Site para caixas de som com ótima direção artística",
                           "product": "Caixa de som", "surface": "commerce"})
        self.assertNotIn("webgl", out["requested_technologies_allowed"])
        self.assertNotIn("three.js", out["requested_technologies_allowed"])

    def test_explicit_technology_veto(self):
        out = lab.propose({"task": "Um experimento", "product": "Instrumento",
                           "requested_technologies": ["WebGL", "GSAP", "CSS"],
                           "prohibited_technologies": ["WebGL"]})
        self.assertEqual(out["requested_technologies_allowed"], ["css", "gsap"])

    def test_operations_do_not_become_art_showcase(self):
        out = lab.propose({"task": "Conciliação de registros", "product": "Painel tributário",
                           "surface": "internal", "real_action": "compare record IDs"})
        self.assertEqual(out["concepts"][0]["id"], "task-first")
        self.assertIn("task", out["concepts"][0]["scenes"]["opening"])
        self.assertNotIn("WebGL", out["concepts"][1]["scenes"]["opening"])

    def test_preserves_declared_brand_and_flows(self):
        out = lab.propose({"task": "Redesign", "product": "App",
                           "brand_invariants": ["keep mascot silhouette"],
                           "protected_flows": ["real sign up route"]})
        self.assertEqual(out["concepts"][0]["preserve"],
                         ["keep mascot silhouette", "real sign up route"])

    def test_patch_stays_small(self):
        out = lab.propose({"task": "Fix padding", "product": "App", "mode": "PATCH"})
        self.assertEqual(out["concepts"], [])

    def test_missing_action_is_not_fabricated(self):
        out = lab.propose({"task": "Build site", "product": "App"})
        self.assertIn("UNKNOWN", out["concepts"][0]["product_grounding"])

    def test_invalid_briefs(self):
        for bad in ([], {}, {"task": "hello"}, {"task": "x", "product": "y",
                                                "brand_invariants": "wrong"},
                    {"task": "x", "product": "y", "surface": "unknown"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                lab.propose(bad)


if __name__ == "__main__":
    unittest.main()
