"""Portable static contract engine: positive and adversarial tests."""
import copy
import importlib.util
import json
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills"/"studio-grade-web-transformation"
path=ROOT/"scripts/contract_engine.py"
spec=importlib.util.spec_from_file_location("contract_engine",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ContractEngineTests(unittest.TestCase):
    def setUp(self):
        self.contract=json.loads((ROOT/"templates/PRODUCT_CONTRACT.json").read_text(encoding="utf-8"))
    def test_real_case(self):
        self.assertEqual(module.check(self.contract)["status"],"PASS")
    def test_wrong_href_fails(self):
        bad=copy.deepcopy(self.contract)
        bad["checks"][2]["href"]="#precos"
        self.assertEqual(module.check(bad)["checks"][2]["status"],"FAIL")
    def test_prohibited_contract(self):
        bad=copy.deepcopy(self.contract)
        bad["checks"].append({"id":"forbidden","kind":"prohibited_text","value":"R$ 19,90"})
        self.assertEqual(module.check(bad)["status"],"FAIL")
    def test_path_escape_rejected(self):
        bad=copy.deepcopy(self.contract)
        bad["artifact"]="../README.md"
        with self.assertRaises(ValueError): module.check(bad)
    def test_invalid_unknown_rule_rejected(self):
        bad=copy.deepcopy(self.contract)
        bad["checks"][0]["kind"]="exec"
        with self.assertRaises(ValueError): module.check(bad)
