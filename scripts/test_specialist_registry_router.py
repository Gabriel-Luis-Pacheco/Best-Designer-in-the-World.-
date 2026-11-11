"""Specialist recommendation is proportional, permission-aware and not executable."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
BASE=Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("new_specialist_router",BASE/"scripts/specialist_router.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SpecialistRouterTests(unittest.TestCase):
    def test_catalog_is_valid_and_has_all_source_references(self):
        rows=mod.read_registry()
        self.assertGreaterEqual(len(rows),38)
        self.assertEqual(len(set(x["id"] for x in rows)),len(rows))
        for row in rows:
            self.assertTrue(row["source"]["url"].startswith("https://github.com/"))
            self.assertTrue(row["source"]["verification"]=="SOURCE_EXISTS_ONLY")
    def test_global_prompt_does_not_load_every_specialist(self):
        x=mod.recommend("marketing","build","landing de produto novo")
        self.assertTrue(x["design_os_is_primary"])
        self.assertTrue(len(x["candidates"])>=2)
        self.assertTrue(len(x["candidates"])<12)
        self.assertEqual(x["status"],"CANDIDATE_SELECTION_ONLY_NOT_EXECUTED")
    def test_geo_and_seo_are_distinct_specialists(self):
        x=mod.recommend("marketing","audit","auditar SEO GEO AI Search e indexação")
        names={r["id"] for r in x["candidates"]}
        self.assertIn("marketing-ai-seo",names)
        self.assertIn("marketing-seo",names)
        self.assertNotIn("ceo-operator",names)
    def test_great_leads_and_psychology_trigger_original_guides(self):
        x=mod.recommend("marketing","clarify","Great Leads copy e psicologia do usuário no hero")
        self.assertIn("references/great-leads-ethical-copy-framework.md",x["internal_guides"])
        self.assertIn("references/ethical-user-psychology.md",x["internal_guides"])
        self.assertIn("marketing-psychology",{r["id"] for r in x["candidates"]})
    def test_owner_specific_ceo_guard(self):
        a=mod.recommend("marketing","shape","CEO, CMO e growth para minha empresa")
        b=mod.recommend("marketing","shape","CEO, CMO e growth para BataTalk",product="BataTalk")
        self.assertNotIn("ceo-operator",{r["id"] for r in a["candidates"]})
        self.assertNotIn("ceo-operator",{r["id"] for r in b["candidates"]})
        c=mod.recommend("marketing","shape","CEO, CMO e growth para BataTalk",product="BataTalk",allow_project_ceo=True)
        self.assertIn("ceo-operator",{r["id"] for r in c["candidates"]})
    def test_host_local_detection_not_claim_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            target=root/".agent/skills/impeccable"
            target.mkdir(parents=True)
            (target/"SKILL.md").write_text("---\nname: impeccable\n---\n# Skill\n",encoding="utf-8")
            x=mod.recommend("product","polish","impeccable polish de tela",project=root)
            detected=next(v for v in x["candidates"] if v["id"]=="impeccable")
            self.assertEqual(detected["availability"],"LOCAL_SKILL_FILE_DETECTED_NOT_LOADED")
            self.assertFalse(any("INVOKED" in k for k in detected.values() if isinstance(k,str)))
    def test_symlink_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            target=root/"foreign"
            target.mkdir()
            (target/"SKILL.md").write_text("---\nname: impeccable\n---\n",encoding="utf-8")
            base=root/".agent/skills"
            base.mkdir(parents=True)
            (base/"faux").symlink_to(target,target_is_directory=True)
            self.assertEqual(mod.detect_local(root,{"impeccable"}),{})
    def test_unrelated_art_does_not_force_sales_funnel(self):
        x=mod.recommend("art","build","experiência abstrata animada")
        self.assertNotIn("references/full-funnel-commercial-orchestration.md",x["internal_guides"])
        self.assertTrue(all(not r["lane"].startswith("sales") for r in x["candidates"]))
    def test_negated_technology_and_skill_is_not_recommended(self):
        a=mod.recommend("art","build","Experiência sem WebGL e GSAP, com ilustrações")
        names={r["id"] for r in a["candidates"]}
        self.assertNotIn("threejs-engineering",names)
        self.assertNotIn("gsap-scrolltrigger",names)
        b=mod.recommend("product","polish","Refine a interface sem Impeccable")
        self.assertNotIn("impeccable",{r["id"] for r in b["candidates"]})

    def test_contrast_clause_releases_veto(self):
        x=mod.recommend("art","build","Sem WebGL, mas usar GSAP para scroll")
        ids={r["id"] for r in x["candidates"]}
        self.assertNotIn("threejs-engineering",ids)
        self.assertIn("gsap-scrolltrigger",ids)

    def test_ceo_authorization_is_boolean_not_project_name(self):
        x=mod.recommend("marketing","shape","CEO para BataTalk",product="BataTalk")
        self.assertEqual(x["project_ceo_gate"],"CLOSED")
        y=mod.recommend("marketing","shape","CEO para BataTalk",product="BataTalk",allow_project_ceo=True)
        self.assertEqual(y["project_ceo_gate"],"OPEN_ONLY_IF_TARGET_CONFIRMED_AND_AUTHORIZED")

    def test_figma_dependency(self):
        x=mod.recommend("product","build","implementar figma pixel-perfect design to code")
        self.assertIn("figma-use",{d["id"] for d in x["prerequisites"]})
    def test_no_tool_execution_and_limit_text(self):
        with self.assertRaises(ValueError):
            mod.recommend("product","build","x"*11000)
        x=mod.recommend("internal","audit","formulário")
        self.assertNotIn("score_of_design",x)
        self.assertFalse(any(r["availability"]=="EXECUTED" for r in x["candidates"]))
if __name__=="__main__":
    unittest.main()
