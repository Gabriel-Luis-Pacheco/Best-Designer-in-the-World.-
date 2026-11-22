"""Integrated product-plan, inventory and permission boundary checks."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/brain"
spec=importlib.util.spec_from_file_location("design_pipeline",HERE/"pipeline.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class PipelineTests(unittest.TestCase):
    def test_protected_contract_parent_change_blocks(self):
        result=p.compose({"context":{"task":"Ajuste checkout","surface":"checkout",
           "authorized_change_types":["visual"],"protected_contract_ids":["checkout.total"]},
           "proposals":[{"id":"a","kind":"visual","target":"checkout"}]})
        self.assertEqual(result["execution_state"],"STOP_PROTECTED_CONTRACT")

    def test_unauthorized_backend_needs_review(self):
        result=p.compose({"context":{"task":"Corrija só botão","surface":"product",
              "authorized_change_types":["visual"]},
              "proposals":[{"id":"b","kind":"backend","target":"api.billing"}]})
        self.assertEqual(result["execution_state"],"REQUIRES_SCOPE_OR_DOMAIN_REVIEW")

    def test_allowed_change_is_not_declared_implemented(self):
        result=p.compose({"context":{"task":"Corrija só botão","surface":"product",
              "authorized_change_types":["visual"]},
              "proposals":[{"id":"c","kind":"visual","target":"button.feedback"}]})
        self.assertEqual(result["execution_state"],"IN_SCOPE_BUT_NOT_EXECUTED")
        self.assertEqual(result["research_state"],"CANDIDATES_NOT_VISITED")

    def test_project_inventory_is_read_only_and_not_ui_certification(self):
        with tempfile.TemporaryDirectory() as root:
            result=p.compose({"context":{"task":"Melhore landing","surface":"landing"}},root)
            self.assertEqual(result["strategy"]["project_inventory"]["evidence_level"],"FILE_INVENTORY_ONLY")
            self.assertEqual(result["execution_state"],"PLAN_ONLY_NOT_EXECUTED")

    def test_onboarding_rebuild_reaches_real_specialists_and_benchmark_baseline(self):
        result=p.compose({"context":{
            "task":"Reconstrua o onboarding: primeira tarefa e ativação",
            "surface":"product", "mode":"REBUILD",
            "audience":"New users of a guided learning product"
        }})
        pipeline=result["component_orchestration"]
        self.assertEqual(pipeline["status"],"COMPONENT_PLANNED_NOT_EXECUTED")
        self.assertEqual(pipeline["selection"],"PROVISIONAL_TASK_ALIAS_MATCH")
        flows=[c for scope in pipeline["workplans"] for c in scope["components"]]
        onboarding=next(x for x in flows if x["component_id"]=="onboarding")
        self.assertIsNotNone(onboarding["benchmark_pattern_transfer"])
        self.assertGreaterEqual(onboarding["benchmark_pattern_transfer"]["reference_target"],4)
        ids={ph["id"] for ph in onboarding["phases"]}
        self.assertIn("market",ids)
        self.assertIn("activation",ids)
        self.assertEqual(result["execution_state"],"PLAN_ONLY_NOT_EXECUTED")

    def test_hero_gets_marketing_copy_and_market_reference(self):
        result=p.compose({"context":{
            "task":"Refaça a hero da landing com provas reais","surface":"landing","mode":"REDESIGN"
        }})
        scope=result["component_orchestration"]
        hero=next(c for x in scope["workplans"] for c in x["components"] if c["component_id"]=="hero")
        lead={e["id"] for ph in hero["phases"] for e in ph["lead_experts"]}
        self.assertIn("marketing-copywriting",lead)
        self.assertIn("market",{ph["id"] for ph in hero["phases"]})
        self.assertEqual(scope["evidence"],"NO_EXTERNAL_SKILLS_OR_BROWSING_OR_IMPLEMENTATION_EXECUTED")

    def test_checkout_patch_is_scoped_without_competitor_marathon(self):
        out=p.compose({"context":{"task":"Corrija o checkout","surface":"checkout","mode":"PATCH"}})
        selected=out["component_orchestration"]["workplans"][0]["components"]
        checkout=next(p for p in selected if p["component_id"]=="checkout")
        self.assertNotIn("market",{ph["id"] for ph in checkout["phases"]})
        self.assertIsNone(checkout["benchmark_pattern_transfer"])

    def test_generic_redesign_requires_real_inventory_instead_of_hallucinated_sections(self):
        out=p.compose({"context":{"task":"Melhore tudo", "surface":"landing", "mode":"REDESIGN"}})
        plan=out["component_orchestration"]
        self.assertEqual(plan["status"],"COMPONENT_INVENTORY_REQUIRED")
        self.assertEqual(plan["workplans"],[])
        self.assertIn("Inventory",plan["next_step"])

    def test_explicit_components_have_precedence_and_are_validated(self):
        out=p.compose({"context":{"task":"Refaça todo produto","surface":"product","mode":"REBUILD"},
                       "components":["onboarding","activation"]})
        self.assertEqual(out["component_orchestration"]["selection"],"EXPLICIT_USER_IDS")
        ids=[c["component_id"] for x in out["component_orchestration"]["workplans"] for c in x["components"]]
        self.assertEqual(ids,["onboarding","activation"])
        with self.assertRaises(ValueError):
            p.compose({"context":{"task":"Novo design","surface":"product"},"components":["invented"]})
        with self.assertRaises(ValueError):
            p.compose({"context":{"task":"Novo design","surface":"internal"},"components":["hero"]})

    def test_bounded_component_input_rejects_bad_shape(self):
        with self.assertRaises(ValueError):
            p.compose({"context":{"task":"Melhore","surface":"landing"},"components":"hero"})
        with self.assertRaises(ValueError):
            p.compose({"context":{"task":"Melhore","surface":"landing"},"components":["hero"]*13})

    def test_invalid_scope_payload_fails_closed(self):
        with self.assertRaises(ValueError):
            p.compose({"context":{"task":"foo"},"proposals":"run the code"})
