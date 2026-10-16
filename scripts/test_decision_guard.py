import importlib.util
import pathlib
import unittest
r=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/brain"
spec=importlib.util.spec_from_file_location("decision_guard",r/"decision_guard.py")
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
class DecisionGuardTests(unittest.TestCase):
    def test_nested_contracts_are_protected(self):
        p={"version":1,"allowed_kinds":["visual"],"protected_targets":["checkout","product/brand"],
           "proposals":[{"id":"1","kind":"visual","target":"checkout.total"},
                        {"id":"2","kind":"visual","target":"product/brand/logo"},
                        {"id":"3","kind":"visual","target":"checkout-help"},
                        {"id":"4","kind":"visual","target":"product"}]}
        result=guard.evaluate(p)
        self.assertEqual([x["decision"] for x in result["changes"]],
            ["BLOCK_PROTECTED_CONTRACT","BLOCK_PROTECTED_CONTRACT","IN_SCOPE_FOR_TESTING","BLOCK_PROTECTED_CONTRACT"])

    def test_protected_price_blocks_even_when_kind_allowed(self):
        p={"version":1,"allowed_kinds":["pricing"],"protected_targets":["plan.price"],
           "proposals":[{"id":"1","kind":"pricing","target":"plan.price"}]}
        self.assertEqual(guard.evaluate(p)["status"],"BLOCKED")
    def test_outside_scope_requires_approval(self):
        p={"version":1,"allowed_kinds":["visual"],"protected_targets":[],
           "proposals":[{"id":"2","kind":"backend","target":"api.delete"}]}
        self.assertEqual(guard.evaluate(p)["changes"][0]["decision"],"NEEDS_AUTHORIZATION")
    def test_authorized_high_risk_needs_verification(self):
        p={"version":1,"allowed_kinds":["payments"],"protected_targets":[],
           "proposals":[{"id":"3","kind":"payments","target":"checkout.flow"}]}
        self.assertEqual(guard.evaluate(p)["changes"][0]["decision"],"REQUIRES_DOMAIN_VERIFICATION")
    def test_safe_visual_change_is_not_claimed_executed(self):
        p={"version":1,"allowed_kinds":["visual"],"protected_targets":[],
           "proposals":[{"id":"4","kind":"visual","target":"hero.spacing"}]}
        self.assertEqual(guard.evaluate(p)["status"],"IN_SCOPE_NOT_EXECUTED")
    def test_duplicate_id_rejected(self):
        p={"version":1,"allowed_kinds":["visual"],"protected_targets":[],
           "proposals":[{"id":"4","kind":"visual","target":"x"},{"id":"4","kind":"visual","target":"y"}]}
        with self.assertRaises(ValueError):guard.evaluate(p)
