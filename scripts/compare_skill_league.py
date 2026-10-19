#!/usr/bin/env python3
"""Conservative cross-skill design trial review. Does NOT score designs or run agents.

Consumes blinded HUMAN ratings linked to real captures. A 'dominates' decision
requires no losses on any jointly rated dimension, not a weighted average.
All outputs are DESCRIPTIVE; one test can't show global superiority.
"""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path

ALLOWED_DIMENSIONS = frozenset({
    "clareza", "direcao_arte", "narrativa", "identidade", "composicao",
    "microcraft", "mobile", "funcionalidade", "acessibilidade",
    "conteudo_credibilidade", "performance", "reconhecimento_produto",
    "continuidade_cenas", "agencia_interativa", "climax_encerramento"
})
HEX = frozenset("0123456789abcdef")

def _valid_sha(value):
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX

def validate_review(review):
    if not isinstance(review, dict):
        raise ValueError("review must be an object")
    required = ("trial_id", "case_id", "system", "reviewer", "run_id")
    for name in required:
        if not isinstance(review.get(name), str) or not review[name].strip():
            raise ValueError("invalid " + name)
    if not _valid_sha(review.get("task_sha256")):
        raise ValueError("invalid shared task digest")
    if review.get("blind") is not True:
        raise ValueError("reviews must be explicitly blinded before comparison")
    controls = review.get("controls")
    if not isinstance(controls, dict) or not all(
        isinstance(controls.get(k), str) and controls[k]
        for k in ("model", "model_revision", "budget_id", "tool_profile_id", "asset_set_id")
    ):
        raise ValueError("missing comparable execution controls")
    scores = review.get("scores")
    if (not isinstance(scores, dict) or not scores or not set(scores) <= ALLOWED_DIMENSIONS
        or any(type(n) is not int or n not in range(4) for n in scores.values())):
        raise ValueError("scores must use known dimensions with integer 0..3")
    evidence = review.get("evidence")
    if not isinstance(evidence, list) or not evidence or any(not isinstance(e, str) or not e.strip() for e in evidence):
        raise ValueError("artifact references required for each review")
    blockers = review.get("blockers", [])
    if not isinstance(blockers, list) or any(
        not isinstance(item, dict) or item.get("severity") not in ("P0", "P1", "P2")
        or not isinstance(item.get("evidence"), str) or not item["evidence"].strip()
        for item in blockers
    ):
        raise ValueError("blockers must have valid severity and evidence")
    return review

def _blocked(r):
    return any(b["severity"] in ("P0", "P1") for b in r.get("blockers", []))

def _compare(ours, theirs):
    if ours["run_id"] == theirs["run_id"]:
        return None, "same run identifier"
    if ours["task_sha256"] != theirs["task_sha256"] or ours["controls"] != theirs["controls"]:
        return None, "unmatched task input or execution controls"
    if set(ours["scores"]) != set(theirs["scores"]):
        return None, "rated dimensions differ"
    a, b = _blocked(ours), _blocked(theirs)
    if a != b:
        outcome = "OURS_BETTER_BLOCKER" if not a else "COMPETITOR_BETTER_BLOCKER"
    elif a:
        outcome = "BOTH_BLOCKED_NO_WIN"
    else:
        wins = sum(ours["scores"][x] > theirs["scores"][x] for x in ours["scores"])
        losses = sum(ours["scores"][x] < theirs["scores"][x] for x in ours["scores"])
        outcome = ("OURS_PARETO_BETTER" if wins > 0 and losses == 0 else
                   "COMPETITOR_PARETO_BETTER" if losses > 0 and wins == 0 else
                   "TIED" if wins == 0 and losses == 0 else
                   "MIXED_TRADEOFF")
    return {
        "outcome": outcome,
        "positive_axes": sorted(k for k in ours["scores"] if ours["scores"][k] > theirs["scores"][k]),
        "negative_axes": sorted(k for k in ours["scores"] if ours["scores"][k] < theirs["scores"][k]),
        "blocked": {"ours": a, "competitor": b},
        "evidence": {"ours": ours["evidence"], "competitor": theirs["evidence"]}
    }, None

def evaluate(data, evidence_root=None):
    if not isinstance(data, dict) or not isinstance(data.get("reviews"), list):
        raise ValueError("expected object containing reviews array")
    rows = [validate_review(r) for r in data["reviews"]]
    verified_files=0
    if evidence_root is not None:
        root=Path(evidence_root).resolve()
        for row in rows:
            for evidence in row["evidence"]:
                rel=Path(evidence)
                dest=(root/rel).resolve()
                if rel.is_absolute() or not dest.is_relative_to(root) or not dest.is_file() or dest.stat().st_size==0:
                    raise ValueError("missing/unsafe/empty review evidence: "+evidence)
                verified_files+=1
    buckets = collections.defaultdict(list)
    for row in rows:
        key = (row["trial_id"], row["case_id"], row["reviewer"], row["system"])
        buckets[key].append(row)
    result, excluded = [], []
    groups = {(t,c,r) for t,c,r,_ in buckets}
    for trial, case, reviewer in sorted(groups):
        ours = buckets.get((trial, case, reviewer, "design-os"), [])
        candidates = sorted(s for t,c,r,s in buckets if (t,c,r)==(trial,case,reviewer) and s!="design-os")
        for system in candidates:
            competitors = buckets[(trial,case,reviewer,system)]
            if len(ours)!=1 or len(competitors)!=1:
                excluded.append({"trial_id":trial,"case_id":case,"reviewer":reviewer,"competitor":system,"reason":"missing or duplicate review for a condition"})
                continue
            comparison, issue = _compare(ours[0], competitors[0])
            if issue:
                excluded.append({"trial_id":trial,"case_id":case,"reviewer":reviewer,"competitor":system,"reason":issue})
                continue
            result.append({"trial_id":trial,"case_id":case,"reviewer":reviewer,
                           "competitor":system,**comparison})
    totals = collections.defaultdict(collections.Counter)
    for r in result:
        totals[r["competitor"]][r["outcome"]] += 1
    return {
        "status":"DESCRIPTIVE_HUMAN_REVIEWS_ONLY_NO_GLOBAL_WINNER",
        "evidence_files_verified":verified_files if evidence_root is not None else None,
        "comparisons":result,
        "excluded":excluded,
        "by_competitor":{k:dict(v) for k,v in sorted(totals.items())},
        "valid_pairs":len(result),
        "limits":[
          ("Evidence paths and nonempty files validated, NOT contents/blindness"
           if evidence_root is not None else
           "All controls/evidence and blind status are declared by submitter, not independently verified"),
          "Scores are subjective human observations, not award judgment or randomized user trials",
          "Pareto comparison avoids hiding regressions; MIXED_TRADEOFF is not a win",
          "Repeated reviewer judgments or cases are not statistically independent",
          "No league winner claim without repetitions, real render captures, reliability and separate human analysis"
        ]
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("reviews", type=Path)
    p.add_argument("--evidence-root",type=Path,help="Reject missing or unsafe local review evidence")
    args=p.parse_args()
    try:
        d=json.loads(args.reviews.read_text(encoding="utf-8"))
        print(json.dumps(evaluate(d,args.evidence_root),ensure_ascii=False,indent=2))
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        p.exit(2,"INVALID REVIEW INPUT: "+str(exc)+"\n")
if __name__=="__main__":
    main()
