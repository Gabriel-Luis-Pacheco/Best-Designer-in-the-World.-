#!/usr/bin/env python3
"""Conservative twenty-rival readiness gate on declared, blinded human reviews.

This is NOT a taste grader, actual experiment executor, verified blind panel,
statistical significance test, or license to claim that a rival was beaten.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

from compare_skill_league import evaluate

RIVALS = (
    "taste", "impeccable", "frontend-design", "uiux-pro-max", "ui-craft",
    "ms-review", "web-guidelines", "shadcn", "figma", "lottie-motion",
    "gsap", "threejs", "view-transitions", "react-performance",
    "react-composition", "webapp-testing", "marketing-cro",
    "marketing-copy", "marketing-ab", "marketing-seo",
)


def assess(data):
    reviewed = evaluate(data)
    by_rival = defaultdict(list)
    for row in reviewed["comparisons"]:
        by_rival[row["competitor"]].append(row)
    results = {}
    for rival in RIVALS:
        rows = by_rival[rival]
        cases = defaultdict(set)
        for row in rows:
            cases[row["case_id"]].add(row["reviewer"])
        complete_cases = [key for key, reviewers in cases.items() if len(reviewers) >= 2]
        reviewer_ids = {r["reviewer"] for r in rows}
        outcomes = {r["outcome"] for r in rows}
        if not rows:
            status = "UNTESTED"
        elif any(o in ("COMPETITOR_PARETO_BETTER", "COMPETITOR_BETTER_BLOCKER")
                 for o in outcomes):
            status = "COMPETITOR_ADVANTAGE_OBSERVED"
        elif "MIXED_TRADEOFF" in outcomes or "BOTH_BLOCKED_NO_WIN" in outcomes:
            status = "MIXED_OR_BLOCKED"
        elif "TIED" in outcomes:
            status = "TIED_NOT_A_WIN"
        elif len(complete_cases) < 3 or len(reviewer_ids) < 2 or len(rows) < 6:
            status = "INSUFFICIENT_INDEPENDENT_EVIDENCE"
        elif outcomes <= {"OURS_PARETO_BETTER", "OURS_BETTER_BLOCKER"}:
            status = "FAVORABLE_DECLARED_REVIEW_REQUIRES_REPLICATION"
        else:
            status = "INCONCLUSIVE"
        results[rival] = {
            "status": status,
            "reviewed_pairs": len(rows),
            "distinct_cases": len(cases),
            "cases_with_two_or_more_reviewers": len(complete_cases),
            "reviewers": len(reviewer_ids),
            "outcomes": sorted(outcomes),
        }
    unknown_rivals = sorted(set(by_rival) - set(RIVALS))
    return {
        "status": "DECLARED_REVIEWS_ONLY_NO_PROVEN_UNIVERSAL_WINNER",
        "rivals": results,
        "rival_count": len(RIVALS),
        "favorable_declared_count": sum(
            row["status"] == "FAVORABLE_DECLARED_REVIEW_REQUIRES_REPLICATION"
            for row in results.values()
        ),
        "excluded_pairs": reviewed["excluded"],
        "unknown_rivals": unknown_rivals,
        "limitations": [
            "Submitted reviews, reviewer independence, blindness and source artifacts are NOT authenticated",
            "Case count and reviewer count are conservative preflight thresholds, NOT statistical power",
            "Only actual independently evaluated renderings can substantiate individual superiority",
            "No number of self-declared wins proves future or universal superiority",
            "Commercial conversion, accessibility and performance require their own domain measurements",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviews", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.reviews.read_text(encoding="utf-8"))
        print(json.dumps(assess(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, "INVALID REVIEWS: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
