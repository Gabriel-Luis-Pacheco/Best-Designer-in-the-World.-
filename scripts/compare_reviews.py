#!/usr/bin/env python3
"""Paired descriptive A/B reporting. No fabricated data or significance claims."""
from __future__ import annotations
import argparse
import collections
import json
import pathlib
from score_review import load_review

def compare(reviews: list[dict]) -> dict:
    buckets = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in reviews:
        buckets[r["case_id"]][r["variant"]].append(r)
    paired = []
    for case_id, variants in sorted(buckets.items()):
        if not all(variants[v] for v in ("with_skill", "without_skill")):
            continue
        def stats(items):
            values = [v for r in items for v in r["scores"].values()]
            return {"runs_reviewed": len(items), "dimensions_rated": len(values),
                    "mean_human_rating": round(sum(values) / len(values), 3),
                    "blocked_reviews": sum(any(b["severity"] in ("P0", "P1") for b in r.get("blockers", [])) for r in items)}
        before, after = stats(variants["without_skill"]), stats(variants["with_skill"])
        paired.append({"case_id": case_id, "without_skill": before, "with_skill": after,
                       "descriptive_rating_difference": round(after["mean_human_rating"] - before["mean_human_rating"], 3)})
    return {"paired_cases": len(paired), "case_summaries": paired,
            "warning": "Descriptive human review only; different rated dimensions or reviewers confound averages. No causality or statistical claim."}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", type=pathlib.Path, help="human review JSON files")
    args = p.parse_args()
    reviews = [load_review(x) for x in args.paths]
    print(json.dumps(compare(reviews), ensure_ascii=False, indent=2))
