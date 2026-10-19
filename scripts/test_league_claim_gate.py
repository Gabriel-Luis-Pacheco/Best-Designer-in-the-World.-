"""No automatic wins from absent, thin, tied or cherry-picked comparisons."""
import unittest
import tempfile
from pathlib import Path
from league_claim_gate import assess, RIVALS


def make_review(rival, case, reviewer, system, score):
    return {
        "trial_id": "t-" + case,
        "case_id": case,
        "reviewer": reviewer,
        "system": system,
        "run_id": case + "-" + reviewer + "-" + system,
        "task_sha256": "a" * 64,
        "blind": True,
        "controls": {
            "model": "declared-model", "model_revision": "rev",
            "budget_id": "same-budget", "tool_profile_id": "same-tools",
            "asset_set_id": "same-assets"
        },
        "scores": {"direcao_arte": score, "mobile": 2},
        "evidence": ["artifact path to verify separately"],
        "blockers": []
    }


class LeagueClaimGateTests(unittest.TestCase):
    def test_twenty_named_rivals_without_reviews_are_untested(self):
        result = assess({"reviews": []})
        self.assertEqual(len(result["rivals"]), 20)
        self.assertEqual(result["favorable_declared_count"], 0)
        self.assertTrue(all(x["status"] == "UNTESTED" for x in result["rivals"].values()))

    def test_one_declared_win_is_insufficient(self):
        result = assess({"reviews": [
            make_review("taste", "c1", "r1", "design-os", 3),
            make_review("taste", "c1", "r1", "taste", 1),
        ]})
        self.assertEqual(result["rivals"]["taste"]["status"],
                         "INSUFFICIENT_INDEPENDENT_EVIDENCE")

    def test_multiple_blind_declarations_only_create_favorable_candidate(self):
        rows = []
        for case in ("c1", "c2", "c3"):
            for reviewer in ("r1", "r2"):
                rows.extend((make_review("taste", case, reviewer, "design-os", 3),
                             make_review("taste", case, reviewer, "taste", 1)))
        result = assess({"reviews": rows})
        self.assertEqual(result["rivals"]["taste"]["status"],
                         "FAVORABLE_DECLARED_REVIEW_REQUIRES_REPLICATION")
        self.assertEqual(result["favorable_declared_count"], 1)
        self.assertEqual(result["rivals"]["gsap"]["status"], "UNTESTED")

    def test_single_competitor_advantage_is_recorded(self):
        rows = []
        for case in ("c1", "c2", "c3"):
            for reviewer in ("r1", "r2"):
                rows.extend((make_review("taste", case, reviewer, "design-os",
                                         1 if case == "c2" else 3),
                             make_review("taste", case, reviewer, "taste", 2)))
        result = assess({"reviews": rows})
        self.assertEqual(result["rivals"]["taste"]["status"],
                         "COMPETITOR_ADVANTAGE_OBSERVED")

    def test_invalid_unblinded_is_rejected(self):
        row = make_review("taste", "c1", "r1", "design-os", 3)
        row["blind"] = False
        with self.assertRaises(ValueError):
            assess({"reviews": [row]})

    def test_missing_declared_evidence_is_rejected_with_root(self):
        rows = [make_review("taste", "c1", "r1", "design-os", 3),
                make_review("taste", "c1", "r1", "taste", 2)]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "evidence"):
                assess({"reviews": rows}, tmp)

    def test_real_nonempty_local_evidence_is_counted_not_certified(self):
        rows = [make_review("taste", "c1", "r1", "design-os", 3),
                make_review("taste", "c1", "r1", "taste", 2)]
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "artifact path to verify separately").write_text("sample bytes")
            result = assess({"reviews": rows}, tmp)
            self.assertEqual(result["evidence_files_verified"], 2)
            self.assertEqual(result["rivals"]["taste"]["status"],
                             "INSUFFICIENT_INDEPENDENT_EVIDENCE")

    def test_rival_names_unique(self):
        self.assertEqual(len(set(RIVALS)), 20)


if __name__ == "__main__":
    unittest.main()
