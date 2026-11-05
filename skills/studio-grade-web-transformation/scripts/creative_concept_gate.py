#!/usr/bin/env python3
"""Check whether competing creative directions are grounded and structurally distinct.

This is a falsification gate, NOT a creativity generator or aesthetic judge.
"""
from __future__ import annotations

import argparse
import json
import re
from itertools import combinations
from pathlib import Path

AXES = ("narrative", "spatial_grammar", "proof_mechanism", "interaction", "material")
MIN_DIFFERENCES = 2


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def inspect(data: dict) -> dict:
    errors = []
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["Expected a JSON object"]}
    facts = data.get("facts", [])
    directions = data.get("directions", [])
    if not isinstance(facts, list) or not facts:
        errors.append("Provide at least one grounded fact with id, claim and source")
        facts = []
    fact_ids = set()
    for fact in facts:
        if not isinstance(fact, dict) or not all(isinstance(fact.get(k), str) and fact[k].strip()
                                                   for k in ("id", "claim", "source")):
            errors.append("Each fact needs nonempty id, claim and source")
            continue
        if fact["id"] in fact_ids:
            errors.append("Duplicate fact id: " + fact["id"])
        fact_ids.add(fact["id"])
    if not isinstance(directions, list) or len(directions) < 2:
        errors.append("At least two competing directions are required")
        directions = []
    seen_ids = set()
    for d in directions:
        if not isinstance(d, dict):
            errors.append("Every direction must be an object")
            continue
        did = d.get("id")
        if not isinstance(did, str) or not did.strip() or did in seen_ids:
            errors.append("Every direction needs a distinct nonempty id")
        else:
            seen_ids.add(did)
        for axis in AXES:
            value = d.get(axis)
            if not isinstance(value, str) or len(normalized(value)) < 12:
                errors.append(str(did) + ": missing meaningful " + axis)
        signature = d.get("product_specific_mechanism")
        if not isinstance(signature, str) or len(normalized(signature)) < 20:
            errors.append(str(did) + ": describe the product-specific mechanism")
        evidence = d.get("evidence_ids")
        if not isinstance(evidence, list) or not evidence:
            errors.append(str(did) + ": link at least one supplied fact")
        elif any(not isinstance(x, str) or x not in fact_ids for x in evidence):
            errors.append(str(did) + ": evidence_ids must refer to declared facts")
    pairs = []
    valid = [x for x in directions if isinstance(x, dict)]
    for a, b in combinations(valid, 2):
        differences = [axis for axis in AXES if isinstance(a.get(axis), str) and
                       isinstance(b.get(axis), str) and
                       normalized(a[axis]) != normalized(b[axis])]
        pair = {"a": a.get("id"), "b": b.get("id"),
                "different_axes": differences, "count": len(differences)}
        pairs.append(pair)
        if len(differences) < MIN_DIFFERENCES:
            errors.append(f"Directions {a.get('id')} and {b.get('id')} vary on fewer than two structural axes")
        if normalized(str(a.get("product_specific_mechanism", ""))) == normalized(
                str(b.get("product_specific_mechanism", ""))):
            errors.append(f"Directions {a.get('id')} and {b.get('id')} reuse the same product-specific mechanism")
    return {
        "status": "REVIEW_REQUIRED" if not errors else "INVALID",
        "structural_pairs": pairs,
        "errors": errors,
        "limitations": [
            "Different words do not prove meaningfully different concepts",
            "Facts and references are supplied, not independently verified",
            "No visual quality, user research or successful implementation is certified",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Creative comparison JSON")
    args = parser.parse_args()
    try:
        if args.brief.stat().st_size > 100_000:
            raise ValueError("Brief exceeds 100 KB")
        result = inspect(json.loads(args.brief.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"INVALID INPUT: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["errors"]:
        parser.exit(2)


if __name__ == "__main__":
    main()
