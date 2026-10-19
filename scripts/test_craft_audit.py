"""Negative and positive coverage for the static craft review. Not aesthetic scoring."""
import importlib.util, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
spec=importlib.util.spec_from_file_location("craft_audit",ROOT/"craft_audit.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CraftAuditTests(unittest.TestCase):
    def test_clean_editorial_not_forced_into_cards(self):
        p='<html><main><section><h1>Oficina do Norte</h1><p>Peças e histórias.</p></section></main></html>'
        self.assertEqual(m.inspect(p)["status"],"NO_SOURCE_HEURISTIC_FLAGS")
    def test_generic_copy_review_only(self):
        x=m.inspect('<section>Unlock your potential</section>')
        self.assertEqual(x["status"],"REVIEW_REQUIRED")
        self.assertEqual(x["findings"][0]["severity"],"REVIEW")
        self.assertNotIn("score",x)
    def test_adjacent_cards(self):
        page="".join("<section>"+("<article><p>Texto</p></article>"*3)+"</section>" for _ in range(2))
        self.assertIn("ADJACENT_CARD_SECTIONS_REVIEW",[x["code"] for x in m.inspect(page)["findings"]])
    def test_emoji_standins_need_review_only(self):
        page='<section><h2>Trilha</h2><p>🏁 Primeira aula</p><p>📍 Segunda aula</p><p>🏆 Última aula</p></section>'
        findings=m.inspect(page)["findings"]
        self.assertIn("EMOJI_AS_VISUAL_PLACEHOLDER_REVIEW",[x["code"] for x in findings])
        self.assertTrue(all(x["severity"]=="REVIEW" for x in findings))
    def test_copy_wall_with_cta_still_seen(self):
        page="<section><h2>Sobre o curso</h2>"+("<p>"+"Repetição e explicação sem demonstração real. "*8+"</p>")*4+"<a href='/aula'>Começar</a></section>"
        self.assertIn("TEXT_DOMINATED_SECTION_REVIEW",[x["code"] for x in m.inspect(page)["findings"]])
    def test_script_text_not_counted(self):
        self.assertEqual(m.inspect('<section><script>Unlock your potential</script><h2>Olá</h2></section>')["findings"],[])
    def test_autoplay_needs_review_not_auto_reject(self):
        self.assertIn("AUTOPLAY_WITHOUT_CONTROLS_REVIEW",[x["code"] for x in m.inspect('<section><video muted autoplay></video></section>')["findings"]])
    def test_size_limit(self):
        with self.assertRaises(ValueError):m.inspect("x"*4_100_000)
if __name__=="__main__":unittest.main()
