import importlib.util
import pathlib
import unittest
root=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
spec=importlib.util.spec_from_file_location("inspect_html",root/"inspect_html.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class StaticHTMLTests(unittest.TestCase):
    def test_clean_source(self):
        page='<html lang="pt-BR"><main><h1>A</h1><button>Salvar</button><a href="#alvo">Ir</a><section id="alvo"></section><img alt=""></main></html>'
        self.assertEqual(mod.inspect(page)["status"],"PASS")
    def test_duplicate_id_is_error(self):
        page='<html lang="en"><main><p id="a"></p><p id="a"></p></main></html>'
        self.assertIn("DUPLICATE_ID",[x["code"] for x in mod.inspect(page)["issues"]])
        self.assertEqual(mod.inspect(page)["status"],"FAIL")
    def test_broken_anchor_is_error(self):
        page='<html lang="en"><main><a href="#missing">A</a></main></html>'
        self.assertEqual(mod.inspect(page)["status"],"FAIL")
    def test_unnamed_button_warning(self):
        page='<html lang="en"><main><button><svg></svg></button></main></html>'
        result=mod.inspect(page)
        self.assertEqual(result["status"],"WARN")
        self.assertIn("BUTTON_NAME_MAY_BE_MISSING",[x["code"] for x in result["issues"]])

    def test_broken_aria_reference(self):
        page='<html lang="en"><main><button aria-describedby="not-there">Go</button></main></html>'
        self.assertEqual(mod.inspect(page)["status"],"FAIL")
        self.assertIn("BROKEN_ARIA_REFERENCE",[x["code"] for x in mod.inspect(page)["issues"]])
    def test_unlabelled_input_warning(self):
        page='<html lang="en"><main><input id="email"></main></html>'
        self.assertIn("INPUT_LABEL_MAY_BE_MISSING",[x["code"] for x in mod.inspect(page)["issues"]])
    def test_labelled_input_clean(self):
        page='<html lang="en"><main><label for="email">Email</label><input id="email"></main></html>'
        self.assertEqual(mod.inspect(page)["status"],"PASS")
