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

    def test_invalid_scope_payload_fails_closed(self):
        with self.assertRaises(ValueError):
            p.compose({"context":{"task":"foo"},"proposals":"run the code"})
