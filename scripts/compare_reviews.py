#!/usr/bin/env python3
"""Evidence-first paired A/B reports. Never compare different rubric dimensions."""
from __future__ import annotations
import argparse
import collections
import json
import pathlib
from score_review import load_review


def compare(reviews: list[dict]) -> dict:
    groups = collections.defaultdict(lambda: collections.defaultdict(list))
    unpaired = []
    for r in reviews:
        if not r.get("pair_id"):
            unpaired.append({"case_id": r["case_id"], "reason": "missing pair_id"})
            continue
        groups[(r["case_id"], r["pair_id"])][r["variant"]].append(r)
    paired = []
    for (case_id, pair_id), variants in sorted(groups.items()):
        left, right = variants["without_skill"], variants["with_skill"]
        if len(left) != 1 or len(right) != 1:
            unpaired.append({"case_id": case_id, "pair_id": pair_id,
                             "reason": "requires exactly one human review per condition"})
            continue
        a, b = left[0], right[0]
        if a["reviewer"] != b["reviewer"]:
            unpaired.append({"case_id": case_id, "pair_id": pair_id,
                             "reason": "different reviewers; cannot make within-reviewer comparison"})
            continue
        if set(a["scores"]) != set(b["scores"]):
            unpaired.append({"case_id": case_id, "pair_id": pair_id,
                             "reason": "rated dimensions differ"})
            continue
        if a["run_id"] == b["run_id"]:
            unpaired.append({"case_id": case_id, "pair_id": pair_id,
                             "reason": "same run ID in both conditions"})
            continue
        deltas = {dim: b["scores"][dim] - a["scores"][dim]
                  for dim in sorted(a["scores"])}
        blocked = lambda r: any(x["severity"] in ("P0", "P1")
                                for x in r.get("blockers", []))
        paired.append({
            "case_id": case_id, "pair_id": pair_id, "reviewer": a["reviewer"],
            "without_skill_run": a["run_id"], "with_skill_run": b["run_id"],
            "dimension_deltas": deltas,
            "mean_paired_delta": round(sum(deltas.values()) / len(deltas), 3),
            "without_skill_blocked": blocked(a), "with_skill_blocked": blocked(b)
        })
    return {"paired_cases": len(paired), "paired_reviews": paired,
            "excluded": unpaired, "status": "DESCRIPTIVE_ONLY",
            "warning": "Comparisons are descriptive, not proof of causality, conversion, or statistical significance."}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", type=pathlib.Path)
    args = p.parse_args()
    reviews = [load_review(x) for x in args.paths]
    print(json.dumps(compare(reviews), ensure_ascii=False, indent=2))
