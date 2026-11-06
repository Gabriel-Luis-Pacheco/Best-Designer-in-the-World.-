#!/usr/bin/env python3
"""Review proposed learning rules without automatically promoting self-reported wins."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

OUTCOMES = {"WITH_SKILL", "BASELINE", "TIE", "MIXED", "INCONCLUSIVE"}


def inspect(data: dict) -> dict:
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["Expected object"]}
    errors, warnings, runs = [], [], []
    hypothesis = data.get("hypothesis")
    if not isinstance(hypothesis, str) or len(hypothesis.strip()) < 20:
        errors.append("State a falsifiable, scoped rule hypothesis")
    tests = data.get("tests")
    if not isinstance(tests, list) or not tests:
        errors.append("Provide paired experiment records")
        tests = []
    seen = set()
    for i, test in enumerate(tests):
        if not isinstance(test, dict):
            errors.append(f"Test {i}: expected an object")
            continue
        key = (test.get("project_id"), test.get("task_hash"), test.get("run_id"))
        if not all(isinstance(k, str) and k.strip() for k in key) or key in seen:
            errors.append(f"Test {i}: unique project_id/task_hash/run_id required")
            continue
        seen.add(key)
        outcome = test.get("outcome")
        if not isinstance(outcome, str) or outcome not in OUTCOMES:
            errors.append(f"Test {i}: unknown outcome")
        if test.get("matched_conditions") is not True or test.get("skill_read_confirmed") is not True:
            errors.append(f"Test {i}: no verified matched baseline and actual skill read")
        if test.get("rendered_artifacts") is not True or test.get("independent_blind_reviews") is not True:
            errors.append(f"Test {i}: require rendered artifacts and independent blinded reviews")
        if not isinstance(test.get("evidence"), list) or not test["evidence"] or any(
                not isinstance(e, str) or not e.strip() for e in test["evidence"]):
            errors.append(f"Test {i}: missing traceable evidence references")
        runs.append({"project_id": key[0], "outcome": outcome})
    projects = {r["project_id"] for r in runs}
    wins = sum(r["outcome"] == "WITH_SKILL" for r in runs)
    losses = sum(r["outcome"] == "BASELINE" for r in runs)
    mixed = sum(isinstance(r["outcome"], str) and r["outcome"] in {"MIXED", "TIE", "INCONCLUSIVE"} for r in runs)
    if len(projects) < 2:
        warnings.append("Evidence covers fewer than two distinct projects: no general rule justified")
    if wins < 2:
        warnings.append("Insufficient independently reviewed with-skill wins to consider generalization")
    if losses or mixed:
        warnings.append("Counterevidence or uncertainty exists; report it explicitly and narrow hypothesis")
    if not errors:
        warnings.append("Self-reported evidence references are not authenticated by this tool")
    return {
        "status": "INVALID" if errors else "HUMAN_REVIEW_CANDIDATE" if len(projects) >= 2 and wins >= 2 and not (losses or mixed)
                  else "PROJECT_LEVEL_HYPOTHESIS_ONLY",
        "errors": errors, "warnings": warnings,
        "summary": {"projects": len(projects), "matched_runs": len(runs),
                    "with_skill_wins": wins, "baseline_wins": losses, "mixed_or_unresolved": mixed},
        "limitations": "Never automatically promote rules: review evidence authenticity, costs, other surfaces and holdout replication",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger", type=Path)
    args = p.parse_args()
    try:
        if args.ledger.stat().st_size > 200_000:
            raise ValueError("Ledger exceeds 200 KB")
        report = inspect(json.loads(args.ledger.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        p.exit(2, f"INVALID INPUT: {exc}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["errors"]:
        p.exit(2)


if __name__ == "__main__":
    main()
