import importlib.util
import json
import pathlib
import copy
import unittest
root=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
path=root/"research/validate_catalog.py"
spec=importlib.util.spec_from_file_location("validate_catalog",path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
catalog=json.loads((root/"research/source_catalog.json").read_text(encoding="utf-8"))
class CatalogTests(unittest.TestCase):
    def test_catalog_is_well_formed(self):
        self.assertGreaterEqual(mod.validate_catalog(catalog)["entries"],10)
    def test_duplicate_id_rejected(self):
        bad=copy.deepcopy(catalog);bad["sources"][1]["id"]=bad["sources"][0]["id"]
        with self.assertRaises(ValueError):mod.validate_catalog(bad)
    def test_http_and_embedded_secrets_rejected(self):
        bad=copy.deepcopy(catalog);bad["sources"][0]["url"]="http://unsafe.com"
        with self.assertRaises(ValueError):mod.validate_catalog(bad)
