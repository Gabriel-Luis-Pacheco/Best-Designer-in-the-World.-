#!/usr/bin/env python3
"""Validate and summarize actual human reviews; never generates aesthetic scores."""
from __future__ import annotations
import json
import pathlib
import sys
from quality_schema import dimensions

VALID_VARIANTS = {"with_skill", "without_skill"}
VALID_RESULTS = {"PASS", "FAIL", "UNKNOWN"}
VALID_SEVERITIES = {"P0", "P1", "P2"}
VALID_DIMENSIONS = dimensions()

def validate_review(d: dict) -> dict:
    if not isinstance(d, dict):
        raise ValueError("review must be object")
    for key in ("reviewer", "run_id"):
        if not isinstance(d.get(key), str) or not d[key].strip():
            raise ValueError(f"missing {key}")
    if type(d.get("case_id")) is not int or d.get("variant") not in VALID_VARIANTS:
        raise ValueError("invalid case_id / variant")
    if not isinstance(d.get("pair_id"), str) or not d["pair_id"].strip():
        raise ValueError("pair_id required for paired analysis")
    scores = d.get("scores")
    if not isinstance(scores, dict) or not scores:
        raise ValueError("scores required")
    if any(type(v) is not int or v not in (0, 1, 2, 3) for v in scores.values()):
        raise ValueError("human ratings use 0..3; omit UNKNOWN dimensions")
    if not set(scores).issubset(VALID_DIMENSIONS):
        raise ValueError("unknown rubric dimension")
    evidence = d.get("evidence")
    if not isinstance(evidence, list) or not evidence or any(not isinstance(x, str) or not x.strip() for x in evidence):
        raise ValueError("evidence references required (not self-assigned grades)")
    blockers = d.get("blockers", [])
    if not isinstance(blockers, list) or any(not isinstance(b, dict) or b.get("severity") not in VALID_SEVERITIES or not b.get("evidence") for b in blockers):
        raise ValueError("blockers require severity and evidence")
    assertions = d.get("assertions", [])
    if not isinstance(assertions, list) or any(not isinstance(a, dict) or a.get("result") not in VALID_RESULTS or not a.get("text") or (a["result"] != "UNKNOWN" and not a.get("evidence")) for a in assertions):
        raise ValueError("assertions require result and evidence for PASS/FAIL")
    return d

def load_review(path: str | pathlib.Path) -> dict:
    return validate_review(json.loads(pathlib.Path(path).read_text(encoding="utf-8")))

def describe(d: dict) -> dict:
    return {"case_id": d["case_id"], "pair_id": d["pair_id"], "variant": d["variant"], "run_id": d["run_id"], "reviewer": d["reviewer"],
            "min_rating": min(d["scores"].values()), "rated_dimensions": len(d["scores"]),
            "blocked": any(b["severity"] in ("P0", "P1") for b in d.get("blockers", [])),
            "assertions": {v: sum(a["result"] == v for a in d.get("assertions", [])) for v in ("PASS", "FAIL", "UNKNOWN")},
            "status": "HUMAN_REVIEW_BLOCKED" if any(b["severity"] in ("P0", "P1") for b in d.get("blockers", [])) else "HUMAN_REVIEW_ONLY"}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/score_review.py path/to/review.json")
    try:
        print(json.dumps(describe(load_review(sys.argv[1])), ensure_ascii=False, indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: {exc}")
