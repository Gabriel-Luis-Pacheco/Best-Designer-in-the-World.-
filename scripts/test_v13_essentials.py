"""V13 regressions: intent fidelity, grounded persuasion, public SEO, and review council."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "skills" / "studio-grade-web-transformation" / "scripts"


def module(name):
    spec = importlib.util.spec_from_file_location("v13_" + name, ROOT / (name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


brief = module("brief_alignment")
copy = module("positioning_copy_contract")
seo = module("search_presence_audit")
council = module("review_council")


def briefing():
    items = [
        {"id": "identity", "text": "The animated introduction must feature exactly the named fictional hero.",
         "priority": "MUST",
         "exact_referent": {"name": "Captain Aurora", "canonical_source": "official fictional source bible",
                            "distinctive_traits": ["scar above eyebrow", "navy coat", "gold emblem"],
                            "rights": "AUTHORIZED"}},
        {"id": "contact", "text": "Visitors must be able to contact the artist.",
         "priority": "MUST"}
    ]
    checkpoints = []
    for stage in brief.STAGES:
        checks = []
        for item in items:
            check = {"requirement_id": item["id"], "result": "PASS",
                     "evidence": ["review/scene.png"] if stage != "DIRECTION" else []}
            if item["id"] == "identity" and stage != "DIRECTION":
                check["identity_state"] = "MATCHED"
                check["identity_review"] = "Compared to canonical art guide"
            checks.append(check)
        checkpoints.append({"stage": stage, "re_read_original": True, "checks": checks})
    return {"mode": "REBUILD", "original_brief": "Build a cinematic portfolio showing Captain Aurora and a real contact flow.",
            "requirements": items, "checkpoints": checkpoints, "proposed_deviations": []}


def positioning():
    return {
        "audience": {"segment": "independent video editors", "job": "present a credible body of work",
                     "trigger": "receiving client enquiries for editing work"},
        "competitive_alternatives": ["emailing scattered video files and a generic template"],
        "market_category": "video editing portfolio",
        "proofs": [{"id": "proof-1", "status": "VERIFIED", "source": "source clip and approved final clip"}],
        "differentiators": [{"capability": "Show real source-to-final editing decisions",
                             "alternative_gap": "Static galleries do not reveal technique",
                             "customer_outcome": "Clients can judge the editor's work",
                             "proof_ids": ["proof-1"]}],
        "message": {"headline": "See the cut before and after",
                    "subheadline": "Explore original footage and final edited projects",
                    "primary_cta": "View projects",
                    "cta_destination": "/projects",
                    "claims": [{"text": "Compare original and final projects", "proof_ids": ["proof-1"]}],
                    "objections": [{"question": "Is this the editor's own work?",
                                    "answer": "Yes, credits are displayed alongside each project",
                                    "proof_ids": ["proof-1"]}]},
    }


def html(title="Studio editing portfolio", noindex=False):
    return ('<!doctype html><html lang="en"><head><title>' + title +
            '</title><meta name="description" content="Genuine video editing cases, clips and booking information.">' +
            ('<meta name="robots" content="noindex">' if noindex else '') +
            '<link rel="canonical" href="https://example.test/projects">' +
            '<meta property="og:title" content="Projects"><meta property="og:description" content="Cases">' +
            '</head><body><h1>Selected editing cases</h1><a href="/contact">Contact</a>' +
            '<img src="/real-clip.webp" alt="Before and after editing timeline"></body></html>')


class OriginalBriefTests(unittest.TestCase):
    def test_original_requirements_match(self):
        self.assertEqual(brief.inspect(briefing())["status"], "READY_FOR_HUMAN_REVIEW")

    def test_generic_substitution_blocks_release(self):
        record = briefing()
        record["checkpoints"][-1]["checks"][0]["identity_state"] = "MISMATCHED"
        report = brief.inspect(record)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(any("incorrect named identity" in x for x in report["blockers"]))

    def test_missing_required_flow_blocks(self):
        record = briefing()
        record["checkpoints"][-1]["checks"].pop(1)
        self.assertEqual(brief.inspect(record)["status"], "BLOCKED")

    def test_cannot_silently_override_brief(self):
        record = briefing()
        record["proposed_deviations"] = [{"requirement_id": "identity",
                                          "reason": "Generic replacement is cheaper",
                                          "approved_by_user": False}]
        self.assertEqual(brief.inspect(record)["status"], "BLOCKED")

    def test_missing_reference_source_invalid(self):
        record = briefing()
        record["requirements"][0]["exact_referent"]["canonical_source"] = ""
        self.assertEqual(brief.inspect(record)["status"], "INVALID")

    def test_unknown_critical_requirement_is_not_pass(self):
        record = briefing()
        record["checkpoints"][-1]["checks"][1] = {
            "requirement_id": "contact", "result": "UNKNOWN",
            "observation": "No usable browser runtime to verify forms"}
        self.assertEqual(brief.inspect(record)["status"], "BLOCKED")

    def test_missing_checkpoint_requires_review(self):
        record = briefing()
        record["checkpoints"].pop(1)
        self.assertEqual(brief.inspect(record)["status"], "NOT_VERIFIED")

    def test_short_vague_original_is_not_rejected(self):
        record = briefing()
        record["original_brief"] = "site foda"
        self.assertEqual(brief.inspect(record)["status"], "READY_FOR_HUMAN_REVIEW")

    def test_correcting_initial_bad_identity_is_allowed(self):
        record = briefing()
        old = record["checkpoints"][1]["checks"][0]
        old["result"] = "FAIL"
        old["identity_state"] = "MISMATCHED"
        old["observation"] = "The first rendering used a generic substitute"
        report = brief.inspect(record)
        self.assertEqual(report["status"], "READY_FOR_HUMAN_REVIEW")
        self.assertTrue(report["historical_checks"])
        record["checkpoints"][-1]["checks"][0]["identity_state"] = "MISMATCHED"
        self.assertEqual(brief.inspect(record)["status"], "BLOCKED")

    def test_correction_reconciles_unverified_first_render(self):
        record = briefing()
        old = record["checkpoints"][1]["checks"][1]
        old["result"] = "UNKNOWN"
        old["observation"] = "The form could not be tested in the first preview"
        self.assertEqual(brief.inspect(record)["status"], "READY_FOR_HUMAN_REVIEW")

    def test_malformed_check_and_referent_types_are_invalid(self):
        record = briefing()
        record["checkpoints"][0]["checks"][0]["requirement_id"] = []
        self.assertEqual(brief.inspect(record)["status"], "INVALID")
        record = briefing()
        record["requirements"][0]["exact_referent"]["rights"] = {}
        self.assertEqual(brief.inspect(record)["status"], "INVALID")
        record = briefing()
        record["checkpoints"][1]["checks"][0]["identity_state"] = []
        self.assertEqual(brief.inspect(record)["status"], "INVALID")

    def test_malformed_deviations_and_missing_priority_do_not_crash(self):
        record = briefing()
        record["proposed_deviations"] = "invalid"
        record["requirements"][0].pop("priority")
        self.assertEqual(brief.inspect(record)["status"], "INVALID")


class PositioningTests(unittest.TestCase):
    def test_claims_linked_to_real_proof(self):
        self.assertEqual(copy.inspect(positioning())["status"], "READY_FOR_HUMAN_COPY_TEST")

    def test_unverified_claim_proof_detected(self):
        record = positioning()
        record["proofs"][0]["status"] = "PROPOSED"
        self.assertEqual(copy.inspect(record)["status"], "PROOF_GAPS")

    def test_invented_reference_detected(self):
        record = positioning()
        record["message"]["claims"][0]["proof_ids"] = ["invented"]
        self.assertEqual(copy.inspect(record)["status"], "INVALID")

    def test_no_competitive_alternative_is_invalid(self):
        record = positioning()
        record["competitive_alternatives"] = []
        self.assertEqual(copy.inspect(record)["status"], "INVALID")

    def test_placeholder_primary_cta_is_rejected(self):
        record = positioning()
        record["message"]["cta_destination"] = "#"
        self.assertEqual(copy.inspect(record)["status"], "INVALID")

    def test_superlatives_get_review_not_auto_pass(self):
        record = positioning()
        record["message"]["headline"] = "Guaranteed 100% perfect edits"
        self.assertTrue(any("superlative" in s for s in copy.inspect(record)["review"]))


class SearchPresenceTests(unittest.TestCase):
    def test_public_metadata_audit(self):
        row = seo.inspect({"good.html": html()})
        self.assertEqual(row["counts"]["P0"], 0)
        self.assertEqual(row["counts"]["P1"], 0)

    def test_noindex_public_is_critical(self):
        row = seo.inspect({"hidden.html": html(noindex=True)})
        self.assertIn("NOINDEX_PUBLIC", [issue["code"] for issue in row["pages"][0]["issues"]])

    def test_duplicate_titles_and_descs_are_reviewed(self):
        row = seo.inspect({"one.html": html(), "two.html": html()})
        self.assertIn("DUPLICATE_TITLE", [i["code"] for i in row["pages"][0]["issues"]])
        self.assertIn("DUPLICATE_DESCRIPTION", [i["code"] for i in row["pages"][1]["issues"]])

    def test_internal_sites_do_not_require_seo(self):
        row = seo.inspect({"internal.html": "<html><body>Private app</body></html>"}, public=False)
        self.assertEqual(row["status"], "NOT_APPLICABLE")

    def test_broken_placeholder_link_detected(self):
        source = html().replace('href="/contact"', 'href="#"')
        row = seo.inspect({"page.html": source})
        self.assertIn("NONCRAWLABLE_NAVIGATION", [i["code"] for i in row["pages"][0]["issues"]])


class CouncilTests(unittest.TestCase):
    def test_role_assignment_is_surface_specific(self):
        selected = {x["role"] for x in council.plan("landing", "REBUILD")}
        self.assertIn("search_discovery", selected)
        self.assertIn("prospective_customer", selected)
        self.assertNotIn("task_operator", selected)

    def test_small_patch_avoids_ritual(self):
        self.assertLessEqual(len(council.plan("landing", "PATCH")), 3)

    def test_no_fake_customer_claim(self):
        packet = {"surface": "landing", "mode": "REBUILD",
                  "reviews": [{"role": "prospective_customer", "review_mode": "REAL_USER",
                               "findings": []}]}
        self.assertEqual(council.inspect(packet)["status"], "INVALID")

    def test_critical_observed_problem_blocks(self):
        packet = {"surface": "landing", "mode": "REBUILD",
                  "reviews": [{"role": "brief_guardian", "review_mode": "SEQUENTIAL_SELF_REVIEW",
                               "task_observed": "Check the brief against the actual captured hero",
                               "inspected_evidence": ["captures/hero.png"],
                               "verdict": "ISSUES_FOUND",
                               "findings": [{"severity": "P1",
                                             "observation": "A central promised interaction is missing in the hero",
                                             "evidence": ["captures/hero.png"],
                                             "recommendation": "Implement the real interaction, recapture and verify"}]}]}
        self.assertEqual(council.inspect(packet)["status"], "BLOCKED")

    def test_unrun_roles_are_only_assignments(self):
        packet = {"surface": "landing", "mode": "REBUILD"}
        self.assertEqual(council.inspect(packet)["status"], "ASSIGNMENTS_ONLY")

    def test_empty_signoff_must_prove_it_inspected_something(self):
        role = {"role": "brief_guardian", "review_mode": "SEQUENTIAL_SELF_REVIEW",
                "verdict": "NO_ISSUES_OBSERVED", "findings": []}
        packet = {"surface": "landing", "mode": "REBUILD", "reviews": [role]}
        self.assertEqual(council.inspect(packet)["status"], "INVALID")
        role["task_observed"] = "I checked the hero and working CTA in a real browser"
        role["inspected_evidence"] = ["captures/hero.png", "traces/cta.json"]
        self.assertEqual(council.inspect(packet)["status"], "INCOMPLETE")

    def test_verified_correction_can_close_critical_issue(self):
        role = {"role": "brief_guardian", "review_mode": "SEQUENTIAL_SELF_REVIEW",
                "task_observed": "Check exact request and post-fix opening",
                "inspected_evidence": ["captures/hero.png"],
                "verdict": "ISSUES_FOUND",
                "findings": [{"severity": "P1",
                              "observation": "The requested hero subject is absent from the opening",
                              "evidence": ["captures/hero-before.png"],
                              "recommendation": "Use the canonical approved subject in the opening",
                              "resolution": "VERIFIED_FIXED",
                              "fix_evidence": ["captures/hero-after.png"]}]}
        packet = {"surface": "landing", "mode": "REBUILD", "reviews": [role]}
        self.assertEqual(council.inspect(packet)["status"], "INCOMPLETE")
        role["findings"][0]["fix_evidence"] = []
        self.assertEqual(council.inspect(packet)["status"], "INVALID")

    def test_weird_role_or_severity_is_invalid_not_exception(self):
        packet = {"surface": "landing", "mode": "REBUILD",
                  "reviews": [{"role": ["brief_guardian"], "verdict": {}, "findings": []}]}
        self.assertEqual(council.inspect(packet)["status"], "INVALID")
        packet["reviews"][0] = {"role": "brief_guardian", "review_mode": "SEQUENTIAL_SELF_REVIEW",
                                "task_observed": "Tried a real interaction and checked a screenshot",
                                "inspected_evidence": ["hero.png"], "verdict": "ISSUES_FOUND",
                                "findings": [{"severity": [], "evidence": ["hero.png"]}]}
        self.assertEqual(council.inspect(packet)["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
