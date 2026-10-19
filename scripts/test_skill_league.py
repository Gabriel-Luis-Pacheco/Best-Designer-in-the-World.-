"""League comparisons never self-generate winners or hide mixed results."""
import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("skill_league",ROOT/"scripts/compare_skill_league.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
H="a"*64
def row(system, scores, *, run="run1", blocked=False):
    return {"trial_id":"trial-1","case_id":"case-1","system":system,
        "reviewer":"blind-reviewer","run_id":run,"task_sha256":H,"blind":True,
        "controls":{"model":"m","model_revision":"r","budget_id":"b","tool_profile_id":"t","asset_set_id":"a"},
        "scores":scores,"evidence":["actual/path/picture.png"],
        "blockers":[{"severity":"P1","evidence":"real issue"}] if blocked else []}
class LeagueTests(unittest.TestCase):
    def test_clear_dominance_descriptive_not_global(self):
        r=m.evaluate({"reviews":[row("design-os",{"mobile":3,"clareza":2}),row("taste",{"mobile":2,"clareza":2},run="run2")]})
        self.assertEqual(r["comparisons"][0]["outcome"],"OURS_PARETO_BETTER")
        self.assertIn("NO_GLOBAL_WINNER",r["status"])
    def test_tradeoff_not_fake_win(self):
        r=m.evaluate({"reviews":[row("design-os",{"mobile":3,"clareza":1}),row("taste",{"mobile":1,"clareza":3},run="run2")]})
        self.assertEqual(r["comparisons"][0]["outcome"],"MIXED_TRADEOFF")
    def test_blockers_dominate(self):
        r=m.evaluate({"reviews":[row("design-os",{"mobile":3},blocked=True),row("taste",{"mobile":1},run="run2")]})
        self.assertEqual(r["comparisons"][0]["outcome"],"COMPETITOR_BETTER_BLOCKER")
    def test_controls_must_match(self):
        a=row("design-os",{"mobile":3});b=row("competitor",{"mobile":1},run="run2");b["controls"]["model"]="different"
        r=m.evaluate({"reviews":[a,b]})
        self.assertEqual(r["valid_pairs"],0)
        self.assertIn("unmatched",r["excluded"][0]["reason"])
    def test_missing_comparison_no_winner(self):
        r=m.evaluate({"reviews":[row("competitor",{"mobile":1})]})
        self.assertEqual(r["valid_pairs"],0)
    def test_optional_evidence_verification(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)
            data={"reviews":[row("design-os",{"mobile":3}),row("taste",{"mobile":2},run="run2")]}
            with self.assertRaises(ValueError):m.evaluate(data,root)
            dest=root/"actual/path/picture.png"
            dest.parent.mkdir(parents=True)
            dest.write_bytes(b"sample")
            result=m.evaluate(data,root)
            self.assertEqual(result["evidence_files_verified"],2)
            data["reviews"][0]["evidence"]=["../../etc/passwd"]
            with self.assertRaises(ValueError):m.evaluate(data,root)
    def test_blind_is_required(self):
        a=row("design-os",{"mobile":2});a["blind"]=False
        with self.assertRaises(ValueError):m.evaluate({"reviews":[a]})
    def test_dimensions_must_match(self):
        r=m.evaluate({"reviews":[row("design-os",{"mobile":3}),row("taste",{"clareza":1},run="run2")]})
        self.assertEqual(r["valid_pairs"],0)
        self.assertIn("dimensions differ",r["excluded"][0]["reason"])
if __name__=="__main__": unittest.main()
