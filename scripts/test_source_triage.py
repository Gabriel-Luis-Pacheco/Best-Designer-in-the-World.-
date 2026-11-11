"""Source lint should be review-only and guard against accidental overconfidence."""
import importlib.util
import pathlib
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
spec=importlib.util.spec_from_file_location("source_triage",ROOT/"source_triage.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SourceTriageTests(unittest.TestCase):
    def test_risk_patterns(self):
        css="a {outline:none; transition: all 1s; height:100vh; font-size:10px; animation: spin 1s infinite;}"
        codes={x["code"] for x in mod.inspect(css,"screen.css")}
        self.assertTrue({"OUTLINE_REMOVAL_REVIEW","BROAD_TRANSITION_REVIEW","FIXED_MOBILE_VH_REVIEW","SMALL_TEXT_REVIEW","LOOP_MOTION_FALLBACK_REVIEW"}<=codes)
        self.assertTrue(all(x["certainty"]=="STATIC_SOURCE_HEURISTIC" for x in mod.inspect(css,"screen.css")))
    def test_context_does_not_claim_no_motion_support(self):
        css="div {animation: spin 2s infinite;} @media (prefers-reduced-motion: reduce){div{animation:none;}}"
        codes={x["code"] for x in mod.inspect(css,"test.css")}
        self.assertNotIn("LOOP_MOTION_FALLBACK_REVIEW",codes)
    def test_jsx_accessibility_and_false_positive(self):
        self.assertIn("NONSEMANTIC_CLICK_TARGET_REVIEW",
                      {x["code"] for x in mod.inspect("<div onClick={run}>Go</div>","x.tsx")})
        self.assertNotIn("NONSEMANTIC_CLICK_TARGET_REVIEW",
                      {x["code"] for x in mod.inspect("<div role='button' tabIndex={0} onKeyDown={handle} onClick={run}>Go</div>","x.tsx")})
    def test_reasoned_exception(self):
        x="/* design-os-ignore OUTLINE_REMOVAL_REVIEW: focus-visible ring added in global CSS */\na{outline:0;}"
        self.assertNotIn("OUTLINE_REMOVAL_REVIEW",{y["code"] for y in mod.inspect(x,"x.css")})
    def test_directory_skips_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=pathlib.Path(tmp)
            (r/"main.css").write_text("button { transition: all 1s; }")
            (r/"node_modules").mkdir()
            (r/"node_modules"/"dependency.css").write_text("a{outline:0}")
            result=mod.scan(r)
            self.assertEqual(result["files_scanned"],1)
            self.assertEqual(len(result["findings"]),1)
            self.assertEqual(result["status"],"REVIEW_CANDIDATES")
    def test_clean_not_grade(self):
        result=mod.inspect(".button { outline: 2px solid currentColor; transition: opacity .2s }","a.css")
        self.assertEqual(result,[])
if __name__=="__main__":
    unittest.main()
