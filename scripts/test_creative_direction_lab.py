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

class GroundedDirectionTests(unittest.TestCase):
    def brief(self, **extra):
        return {"task": "Build the requested surface", "product": "Atlas", **extra}

    def test_read_product_checkout_and_art_have_distinct_structures(self):
        pairs = [tuple(c["id"] for c in lab.propose(self.brief(surface=s))["concepts"])
                 for s in ("read", "product", "checkout", "experience", "commerce", "internal")]
        self.assertEqual(len(set(pairs)), 6)

    def test_reading_has_navigation_not_a_sales_funnel(self):
        out = lab.propose(self.brief(surface="read"))
        for c in out["concepts"]:
            self.assertIn("do not add a sales funnel", c["scenes"]["closure"])

    def test_declared_evidence_changes_the_structure_not_just_product_name(self):
        demo = lab.propose(self.brief(evidence_types=["demo"]))
        photo = lab.propose(self.brief(evidence_types=["photography"]))
        self.assertNotEqual(demo["concepts"][0]["composition"], photo["concepts"][0]["composition"])
        self.assertIn("declared evidence=photography", photo["concepts"][0]["fit_basis"])

    def test_scope_overrules_irrelevant_photographic_evidence(self):
        out = lab.propose(self.brief(surface="checkout", evidence_types=["photography", "narrative"]))
        self.assertEqual([c["id"] for c in out["concepts"]], ["review-first", "recovery-first"])

    def test_declared_facts_jobs_and_assets_are_traceable_and_unverified(self):
        out = lab.propose(self.brief(product_facts=["Data stays on the device"],
            user_jobs=["Compare two source records"], available_assets=["original-mark.svg"],
            objective="Complete a comparison", audience="Auditors"))
        c = out["concepts"][0]
        self.assertIn("Data stays on the device", c["scenes"]["middle"])
        self.assertIn("Compare two source records", c["scenes"]["opening"])
        self.assertIn("original-mark.svg", c["scenes"]["recognition"])
        self.assertEqual(c["declared_grounding"]["audience_supplied_unverified"], "Auditors")
        self.assertIn("unverified", out["limits"])

    def test_missing_context_remains_unknown(self):
        out = lab.propose(self.brief())
        self.assertIn("product_facts", out["context_gaps"])
        self.assertIn("UNKNOWN", out["concepts"][0]["scenes"]["middle"])

    def test_locked_direction_and_default_refine_do_not_reopen_concepts(self):
        for fields in ({"direction_locked": True, "existing_direction": "Quiet reference"}, {"mode": "REFINE"}):
            out = lab.propose(self.brief(**fields))
            self.assertEqual(out["concepts"], [])
        out = lab.propose(self.brief(mode="REFINE", explore_directions=True))
        self.assertEqual(len(out["concepts"]), 2)

    def test_audit_never_builds_even_with_exploration_opt_in(self):
        out = lab.propose(self.brief(mode="AUDIT", explore_directions=True))
        self.assertEqual(out["concepts"], [])

    def test_constraints_survive_non_exploration_routes(self):
        out = lab.propose(self.brief(mode="PATCH", requested_technologies=["CSS", "GSAP"],
            prohibited_technologies=["gsap"], protected_flows=["payment.total"]))
        self.assertEqual(out["requested_technologies_allowed"], ["css"])
        self.assertEqual(out["preserve"], ["payment.total"])

    def test_all_surface_evidence_pairs_remain_distinct_and_valid(self):
        for surface in lab.SURFACES:
            for evidence in lab.EVIDENCE_TYPES:
                with self.subTest(surface=surface, evidence=evidence):
                    out = lab.propose(self.brief(surface=surface, evidence_types=[evidence]))
                    a, b = out["concepts"]
                    self.assertNotEqual(a["id"], b["id"])
                    self.assertNotEqual(a["composition"], b["composition"])
                    self.assertNotEqual(a["signature_gesture"], b["signature_gesture"])

    def test_bad_evidence_and_boolean_inputs_rejected(self):
        for fields in ({"evidence_types": ["invented"]}, {"direction_locked": "false"},
                       {"explore_directions": 1}, {"product_facts": "not a list"}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                lab.propose(self.brief(**fields))


if __name__ == "__main__":
    unittest.main()
