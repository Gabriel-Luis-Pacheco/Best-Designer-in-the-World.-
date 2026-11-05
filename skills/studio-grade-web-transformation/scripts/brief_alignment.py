#!/usr/bin/env python3
"""Brief compass: detect silent drift, invented compliance and referent substitution.

A declaration is not proof of rendered quality. A reviewer must inspect cited evidence.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

MODES = {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}
STAGES = ("DIRECTION", "FIRST_RENDER", "RELEASE")
PRIORITIES = {"MUST", "SHOULD", "OPTIONAL"}
RESULTS = {"PASS", "FAIL", "UNKNOWN"}
REFERENT_STATES = {"MATCHED", "MISMATCHED", "UNVERIFIED", "NOT_RENDERED"}
RIGHTS = {"AUTHORIZED", "UNKNOWN", "NOT_APPLICABLE"}


def inspect(data: dict) -> dict:
    errors, blockers, unresolved, warnings = [], [], [], []
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["Expected an object"]}
    mode = data.get("mode")
    if mode not in MODES:
        errors.append("mode must be one of " + ", ".join(sorted(MODES)))
    original = data.get("original_brief")
    if not isinstance(original, str) or len(original.strip()) < 20:
        errors.append("Keep the original request verbatim, not a rewritten summary")
    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append("List explicit requirements and priorities")
        requirements = []
    by_id = {}
    for item in requirements:
        if not isinstance(item, dict):
            errors.append("Requirement must be an object")
            continue
        rid = item.get("id")
        if not isinstance(rid, str) or not rid.strip() or rid in by_id:
            errors.append("Requirement ids must be unique nonempty strings")
            continue
        by_id[rid] = item
        if not isinstance(item.get("text"), str) or len(item["text"].strip()) < 8:
            errors.append(rid + ": require recognizable original requirement")
        if item.get("priority") not in PRIORITIES:
            errors.append(rid + ": priority must be MUST/SHOULD/OPTIONAL")
        if item.get("exact_referent"):
            ref = item["exact_referent"]
            if not isinstance(ref, dict):
                errors.append(rid + ": exact_referent must be an object")
                continue
            if not isinstance(ref.get("name"), str) or not ref["name"].strip():
                errors.append(rid + ": exact referent needs an unambiguous name")
            if not isinstance(ref.get("canonical_source"), str) or len(ref["canonical_source"].strip()) < 8:
                errors.append(rid + ": resolve the canonical identity before visual production")
            if not isinstance(ref.get("distinctive_traits"), list) or not ref["distinctive_traits"]:
                errors.append(rid + ": record identity-defining traits; a generic stand-in is forbidden")
            if ref.get("rights") not in RIGHTS:
                errors.append(rid + ": rights must be AUTHORIZED/UNKNOWN/NOT_APPLICABLE")
            elif ref["rights"] == "UNKNOWN":
                unresolved.append(rid + ": reuse/publication permissions unresolved")
    checkpoints = data.get("checkpoints", [])
    if not isinstance(checkpoints, list):
        errors.append("checkpoints must be a list")
        checkpoints = []
    found = set()
    latest = {}
    for cp in checkpoints:
        if not isinstance(cp, dict):
            errors.append("Every checkpoint must be an object")
            continue
        stage = cp.get("stage")
        if stage not in STAGES or stage in found:
            errors.append("Checkpoint stages must be recognized and unique")
            continue
        found.add(stage)
        if cp.get("re_read_original") is not True:
            errors.append(stage + ": re-read the original request, not only the latest plan")
        checks = cp.get("checks", [])
        if not isinstance(checks, list):
            errors.append(stage + ": checks must be a list")
            continue
        seen = set()
        latest[stage] = {}
        for check in checks:
            if not isinstance(check, dict):
                errors.append(stage + ": check must be an object")
                continue
            rid = check.get("requirement_id")
            if rid not in by_id or rid in seen:
                errors.append(stage + ": unknown or repeated requirement id: " + str(rid))
                continue
            seen.add(rid)
            result = check.get("result")
            if result not in RESULTS:
                errors.append(stage + "/" + rid + ": PASS/FAIL/UNKNOWN required")
                continue
            latest[stage][rid] = check
            if result != "PASS":
                why = check.get("observation")
                if not isinstance(why, str) or len(why.strip()) < 12:
                    errors.append(stage + "/" + rid + ": explain FAIL/UNKNOWN")
                if result == "FAIL":
                    blockers.append(stage + "/" + rid + ": observed requirement failure")
                else:
                    unresolved.append(stage + "/" + rid + ": not yet verified")
            else:
                if stage != "DIRECTION" and (not isinstance(check.get("evidence"), list) or
                    not check["evidence"] or not all(isinstance(x, str) and x.strip() for x in check["evidence"])):
                    errors.append(stage + "/" + rid + ": rendered PASS needs inspectable evidence references")
            if by_id[rid].get("exact_referent") and stage != "DIRECTION":
                state = check.get("identity_state")
                if state not in REFERENT_STATES:
                    errors.append(stage + "/" + rid + ": explicit identity_state required")
                elif state == "MISMATCHED":
                    blockers.append(stage + "/" + rid + ": incorrect named identity; never substitute silently")
                elif state in {"UNVERIFIED", "NOT_RENDERED"}:
                    unresolved.append(stage + "/" + rid + ": named identity unverified")
                if state == "MATCHED" and result == "PASS" and not check.get("identity_review"):
                    errors.append(stage + "/" + rid + ": report who compared output to canonical reference")
        if stage == "RELEASE":
            for rid, item in by_id.items():
                if item.get("priority") == "MUST" and rid not in seen:
                    blockers.append("RELEASE/" + rid + ": missing must-have verification")
    if mode in {"REDESIGN", "REBUILD"}:
        for stage in STAGES:
            if stage not in found:
                unresolved.append("Missing " + stage + " checkpoint")
    elif "RELEASE" not in found and mode != "AUDIT":
        unresolved.append("No final original-brief reconciliation")
    for change in data.get("proposed_deviations", []):
        if not isinstance(change, dict) or change.get("requirement_id") not in by_id:
            errors.append("Deviations must cite existing requirements")
            continue
        if not isinstance(change.get("reason"), str) or not change["reason"].strip():
            errors.append("Deviations require reason")
        if change.get("approved_by_user") is not True or not change.get("approval_reference"):
            blockers.append("Unapproved deviation from " + change["requirement_id"])
    release = latest.get("RELEASE", {})
    if release:
        for rid, item in by_id.items():
            if item["priority"] == "MUST" and release.get(rid, {}).get("result") != "PASS":
                blockers.append("RELEASE/" + rid + ": MUST not verified PASS")
    if errors:
        state = "INVALID"
    elif blockers:
        state = "BLOCKED"
    elif unresolved:
        state = "NOT_VERIFIED"
    else:
        state = "READY_FOR_HUMAN_REVIEW"
    warnings.append("Check declarations and identity labels are not automatic visual or legal certification")
    return {"status": state, "errors": errors, "blockers": sorted(set(blockers)),
            "unresolved": sorted(set(unresolved)), "warnings": warnings,
            "limitations": "Manual evidence review and real product rendering remain essential"}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("contract", type=Path)
    args = p.parse_args()
    try:
        if args.contract.stat().st_size > 200_000:
            raise ValueError("Contract exceeds 200 KB")
        report = inspect(json.loads(args.contract.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.exit(2, "INVALID INPUT: " + str(exc) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] != "READY_FOR_HUMAN_REVIEW":
        p.exit(2)


if __name__ == "__main__":
    main()
