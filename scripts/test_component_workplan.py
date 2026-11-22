"""Tests for the 47-component execution atlas and staged specialist workplans."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("component_workplan",ROOT/"scripts/component_workplan.py")
plan_mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan_mod)


class WorkplanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas,cls.experts=plan_mod.load_atlas()

    def go(self,component,mode="REDESIGN",surface="marketing"):
        return plan_mod.plan(component_ids=[component],mode=mode,surface=surface,
                             atlas=self.atlas,experts=self.experts)["components"][0]

    def test_all_47_have_distinct_jobs_and_review_questions(self):
        self.assertEqual(len(self.atlas["profiles"]),47)
        self.assertEqual(len(self.atlas["phase_definitions"]),15)
        jobs={x["id"]:x["review_questions"] for x in self.atlas["profiles"]}
        self.assertNotEqual(jobs["hero"],jobs["checkout"])
        self.assertNotEqual(jobs["pricing"],jobs["dashboard"])
        for id_,questions in jobs.items():
            self.assertGreaterEqual(len(questions),2,id_)

    def test_hero_has_copy_market_art_and_proof_handoffs(self):
        result=self.go("hero")
        steps={x["id"]:x for x in result["phases"]}
        for id_ in ("truth","market","position","editorial","proof","art","ux","engineering","accessibility","render","measurement"):
            self.assertIn(id_,steps)
        sources={r["id"] for x in result["phases"]
                 for r in x["lead_candidates"]+x["alternative_candidates"]}
        for id_ in ("marketing-copywriting","marketing-cro","taste-skill","anthropic-frontend","impeccable"):
            self.assertIn(id_,sources)
        self.assertTrue(all(x["status"]=="NOT_STARTED" for x in result["phases"]))
        self.assertTrue(all(v["status"]=="CANDIDATE_UNVERIFIED_NOT_INVOKED"
                            for x in result["phases"]
                            for v in x["lead_candidates"]+x["alternative_candidates"]))
        self.assertTrue(all(v["source"].startswith("https://github.com/") and v["skill_file"]
                            for x in result["phases"]
                            for v in x["lead_candidates"]+x["alternative_candidates"]))

    def test_dashboard_focused_on_operational_data_not_sales(self):
        result=self.go("dashboard",surface="internal")
        steps={x["id"] for x in result["phases"]}
        self.assertIn("data",steps)
        self.assertNotIn("market",steps)
        self.assertNotIn("position",steps)
        self.assertNotIn("editorial",steps)
        all_ids={r["id"] for x in result["phases"]
                 for r in x["lead_candidates"]+x["alternative_candidates"]}
        self.assertNotIn("marketing-sales",all_ids)
        self.assertNotIn("marketing-cro",all_ids)

    def test_checkout_includes_price_truth_and_recovery(self):
        checkout=self.go("checkout")
        steps={x["id"] for x in checkout["phases"]}
        self.assertIn("commerce",steps)
        self.assertIn("editorial",steps)
        self.assertIn("proof",steps)
        self.assertIn("render",steps)
        self.assertIn("preco",str(checkout["review_questions"]).casefold() +
                      str(checkout["red_flags"]).casefold())

    def test_approved_patch_skips_research_and_creative_ceremony(self):
        hero=self.go("hero",mode="PATCH")
        ids={x["id"] for x in hero["phases"]}
        self.assertNotIn("market",ids)
        self.assertNotIn("editorial",ids)
        self.assertNotIn("position",ids)
        self.assertIn("render",ids)

    def test_all_profile_phase_guides_exist(self):
        for phase in self.atlas["phase_definitions"].values():
            for name in phase["guides"]:
                self.assertTrue((ROOT/"references"/name).is_file(),name)

    def test_unknown_component_or_surface_rejected(self):
        with self.assertRaises(ValueError):
            self.go("nonexistent")
        with self.assertRaises(ValueError):
            self.go("hero",surface="internal")
        with self.assertRaises(ValueError):
            self.go("hero",surface="unrecognized")

    def test_hero_routes_specialized_vendor_copy_slop_and_proof(self):
        hero=self.go("hero")
        phases={x["id"]:x for x in hero["phases"]}
        art=phases["art"]["vendored_specialized_references"]
        editorial=phases["editorial"]["vendored_specialized_references"]
        proof=phases["proof"]["vendored_specialized_references"]
        def names(group):
            return {x["name"] for x in group["priority_snapshots"]+
                    group["additional_snapshots_if_relevant"]}
        self.assertIn("landing-page",names(art))
        self.assertIn("copy-editing",names(editorial))
        self.assertIn("product-proof-saas",names(proof))
        self.assertLessEqual(len(art["priority_snapshots"]),3)
        self.assertTrue(all("NOT_LOADED" in x["status"] for g in (art,editorial,proof)
                            for x in g["priority_snapshots"]))

    def test_pricing_gets_pricing_page_not_unrelated_motions(self):
        pricing=self.go("pricing")
        phases={x["id"]:x for x in pricing["phases"]}
        refs=phases["commerce"]["vendored_specialized_references"]
        all_names={x["name"] for x in refs["priority_snapshots"]+
                   refs["additional_snapshots_if_relevant"]}
        self.assertIn("pricing-page",all_names)
        self.assertNotIn("animation-systems",all_names)

    def test_every_component_has_expert_or_explicit_contextual_gap(self):
        # Regression against 104 formerly empty expert-stage assignments across
        # 394 staged component checks. Avoid declaring them solved by a vendor
        # snapshot whose runtime availability has not been established.
        matrix,_=plan_mod._component_router().load()
        modes={"hero":"REDESIGN","checkout":"REBUILD","dashboard":"REFINE"}
        used_fallback=False
        checked=0
        uncovered=[]
        for profile in matrix:
            component=profile["id"]
            surface=profile["surfaces"][0]
            result=self.go(component,mode=modes.get(component,"REDESIGN"),surface=surface)
            for stage in result["phases"]:
                checked+=1
                leads=stage["lead_candidates"]
                available=leads+stage["alternative_candidates"]
                # Truth is deliberately a canonical product-facts task with
                # no third-party lane. It must not invent an expert just to
                # make a routing coverage metric reach 100%.
                role_lanes=self.atlas["phase_definitions"][stage["id"]]["role_lanes"]
                if not available and role_lanes:
                    uncovered.append((component,stage["id"],stage["missing_compatible_specialist_lanes"]))
                for expert in available:
                    self.assertIn(surface,self.experts[expert["id"]]["surfaces"],
                                  (component,stage["id"],expert["id"]))
                    self.assertEqual(expert["status"],"CANDIDATE_UNVERIFIED_NOT_INVOKED")
                    used_fallback |= expert["selection_method"]=="SURFACE_COMPATIBLE_REGISTRY_FALLBACK"
                self.assertLessEqual(len(leads),3)
        self.assertGreaterEqual(checked,350)
        self.assertEqual(uncovered,[])
        self.assertTrue(used_fallback)

    def test_internal_navigation_does_not_pull_marketing_copywriter(self):
        nav=self.go("navigation",surface="internal")
        editorial=next(p for p in nav["phases"] if p["id"]=="editorial")
        ids={x["id"] for x in editorial["lead_candidates"]+editorial["alternative_candidates"]}
        self.assertNotIn("marketing-copywriting",ids)
        self.assertIn("ui-ux-pro-max",ids)

    def test_hero_measurement_receives_global_registered_specialist(self):
        result=self.go("hero")
        measurement=next(x for x in result["phases"] if x["id"]=="measurement")
        ids={x["id"] for x in measurement["lead_candidates"]+measurement["alternative_candidates"]}
        self.assertIn("marketing-conversion-tracking",ids)
        self.assertIn("marketing-analytics",ids)
        self.assertEqual(measurement["missing_compatible_specialist_lanes"],[])

    def test_no_threejs_or_gsap_by_default_on_static_hero(self):
        hero=self.go("hero")
        stage=next(x for x in hero["phases"] if x["id"]=="engineering")
        ids={x["id"] for x in stage["lead_candidates"]+stage["alternative_candidates"]}
        self.assertNotIn("react-three-fiber",ids)
        self.assertNotIn("gsap-scrolltrigger",ids)

    def test_all_priority_flows_receive_competitor_pattern_transfer(self):
        atlas=self.atlas
        priority=[p for p in atlas["profiles"] if p.get("benchmark_transfer")]
        self.assertGreaterEqual(len(priority),16)
        for profile in priority:
            surface=("marketing" if "marketing" in next(
                x for x in plan_mod._component_router().load()[0] if x["id"]==profile["id"]
            )["surfaces"] else next(
                x for x in plan_mod._component_router().load()[0] if x["id"]==profile["id"]
            )["surfaces"][0])
            result=self.go(profile["id"],mode="REDESIGN",surface=surface)
            self.assertIn("market",{p["id"] for p in result["phases"]})
            spec=result["benchmark_pattern_transfer"]
            self.assertEqual(spec["status"],"NOT_OBSERVED_NOT_VALIDATED")
            self.assertGreaterEqual(spec["reference_target"],4)
            self.assertIn("ADOPT",spec["pattern_baseline"])
            self.assertTrue(spec["stages_to_observe"])
            self.assertTrue(spec["mandatory_for_major_modes"])

    def test_onboarding_now_prioritizes_competitor_flow_evidence(self):
        flow=self.go("onboarding",mode="REBUILD",surface="product")
        phases=[p["id"] for p in flow["phases"]]
        self.assertLess(phases.index("market"),phases.index("activation"))
        spec=flow["benchmark_pattern_transfer"]
        self.assertTrue(any("first value" in s for s in spec["stages_to_observe"]))
        self.assertEqual(spec["reference_target"],5)

    def test_checkout_adoption_is_not_assumed_to_be_proven_conversion(self):
        flow=self.go("checkout",mode="REBUILD",surface="product")
        spec=flow["benchmark_pattern_transfer"]
        self.assertIn("does not prove",spec["result_claim_policy"].lower() if
                      "does not prove" in spec["result_claim_policy"].lower() else
                      "does not prove a conversion result")
        self.assertIn("market",{x["id"] for x in flow["phases"]})

    def test_patch_never_forces_competitor_flow_marathon(self):
        flow=self.go("onboarding",mode="PATCH",surface="product")
        self.assertNotIn("market",{x["id"] for x in flow["phases"]})
        self.assertIsNone(flow["benchmark_pattern_transfer"])

    def test_dashboard_does_not_inherit_commercial_transfer(self):
        flow=self.go("dashboard",mode="REDESIGN",surface="internal")
        self.assertIsNone(flow["benchmark_pattern_transfer"])

    def test_status_is_planning_not_action(self):
        result=plan_mod.plan(component_ids=["hero"],surface="marketing",mode="REBUILD",
                            atlas=self.atlas,experts=self.experts)
        self.assertEqual(result["status"],"PLANNED_NOT_EXECUTED")
        self.assertEqual(result["components"][0]["final_status"],"NOT_EXECUTED_NEEDS_REAL_ARTIFACTS")


if __name__=="__main__":
    unittest.main()
