"""DTCG subset negative tests. Do not claim conformance or visual checks."""
import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
s=importlib.util.spec_from_file_location("validate_tokens",ROOT/"validate_tokens.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class DTCGTests(unittest.TestCase):
    def test_aliases(self):
        x=m.validate({"color":{"primary":{"$type":"color","$value":"#224466"},
                                 "hover":{"$type":"color","$value":"{color.primary}"}}})
        self.assertEqual(x["tokens"],2)
        self.assertEqual(x["aliases"],1)
    def test_inherited_type(self):
        x=m.validate({"dimension":{"$type":"dimension","base":{"$value":"1rem"}}})
        self.assertEqual(x["tokens"],1)
    def test_missing_alias(self):
        with self.assertRaisesRegex(ValueError,"unresolved"):
            m.validate({"foo":{"$value":"{bar}"}})
    def test_cycle(self):
        with self.assertRaisesRegex(ValueError,"Circular"):
            m.validate({"a":{"$value":"{b}"},"b":{"$value":"{a}"}})
    def test_reject_unsupported_type(self):
        with self.assertRaisesRegex(ValueError,"Unknown"):
            m.validate({"a":{"$type":"notReal","$value":"x"}})
    def test_no_false_compliance(self):
        self.assertIn("subset",m.validate({"a":{"$value":"x"}})["limitations"][0])
if __name__=="__main__":unittest.main()
