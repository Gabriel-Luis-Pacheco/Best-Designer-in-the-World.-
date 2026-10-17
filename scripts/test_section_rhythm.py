"""Static narrative audit regression tests. No algorithmic quality scores."""
import importlib.util, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("section_rhythm",ROOT/"scripts/section_rhythm.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RhythmTests(unittest.TestCase):
    def test_generic_landing_exposes_card_repetition(self):
        page=(ROOT/"fixtures/landing-generic.html").read_text()
        r=m.inspect(page)
        self.assertEqual(r["status"],"STATIC_HEURISTIC_ONLY_NOT_VISUAL_VERDICT")
        self.assertGreaterEqual(len([s for s in r["sections"] if "REPEATED_CARD_PATTERN_REVIEW" in s["review_flags"]]),1)
    def test_editorial_alternative_produces_sections_without_score(self):
        page=(ROOT/"examples/conversaboa-editorial-alternative.html").read_text()
        r=m.inspect(page)
        self.assertGreaterEqual(r["section_count"],4)
        self.assertNotIn("aesthetic_score",r)
        self.assertIn("Cannot see CSS",r["limitations"][0])
    def test_html_is_not_executed(self):
        r=m.inspect('<section><h2>X</h2><script>throw Error(1)</script><p>Hello</p></section>')
        self.assertEqual(r["section_count"],1)
        self.assertEqual(r["sections"][0]["paragraphs"],1)
        self.assertEqual(r["sections"][0]["text_characters"],7)
if __name__=="__main__": unittest.main()
