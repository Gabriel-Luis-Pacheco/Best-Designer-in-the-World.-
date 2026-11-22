#!/usr/bin/env python3
"""Hero art-direction evidence gate. It NEVER judges pixels or certifies taste.

Status is a workflow/evidence check, not a beauty score. Do not waive
unresolved P0/P1 issues by adding screenshots or declaring self-approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

MODES = {"REDESIGN", "REBUILD", "REFINE"}
VERDICTS = {"PASS", "REWORK", "BLOCKED_WITH_EVIDENCE", "NOT_REVIEWED"}
REVIEWERS = {"SELF_REVIEW", "INDEPENDENT_AGENT", "HUMAN", "NOT_REVIEWED"}
DECISIONS = {"ADOPT", "ADAPT", "REJECT"}
MAX_BYTES = 30_000_000


def _meaningful(value: object, n: int = 20) -> bool:
    return isinstance(value, str) and len(value.strip()) >= n


def _image(root: Path, value: object) -> bool:
    """Check actual local PNG existence and safe path; not aesthetic content."""
    if not isinstance(value, str) or not value or "\\" in value or len(value) > 500:
        return False
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.suffix.lower() != ".png":
        return False
    full = (root / path).resolve()
    if not full.is_relative_to(root) or not full.is_file() or full.is_symlink():
        return False
    size = full.stat().st_size
    if not 64 <= size <= MAX_BYTES:
        return False
    with full.open("rb") as f:
        return f.read(8) == b"\x89PNG\r\n\x1a\n"


def _valid_url(value: object) -> bool:
    if not isinstance(value, str) or len(value) > 1024:
        return False
    u = urlparse(value)
    return u.scheme in ("https", "http") and bool(u.netloc)


def inspect(packet: object, root: Path) -> dict:
    if not isinstance(packet, dict):
        return {"status": "INVALID", "errors": ["root must be a JSON object"]}
    errors: list[str] = []
    missing: list[str] = []
    blockers: list[str] = []
    warnings: list[str] = []

    if packet.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if packet.get("mode") not in MODES:
        errors.append("mode must be REDESIGN / REBUILD / REFINE")
    if packet.get("surface") not in {"marketing", "product", "content"}:
        errors.append("surface invalid")
    if not isinstance(packet.get("route"), str) or not packet["route"].startswith("/"):
        errors.append("route must begin with /")

    brief = packet.get("brief")
    if not isinstance(brief, dict):
        errors.append("brief object required")
        brief = {}
    for key in ("audience", "offer", "primary_cta", "first_value", "brand_constraints"):
        if not _meaningful(brief.get(key), 10):
            missing.append(f"brief.{key}: real project context required")

    research = packet.get("research")
    if not isinstance(research, dict):
        errors.append("research object required")
        research = {}
    competitors = research.get("direct_competitors", [])
    adjacent = research.get("cross_category", [])
    if not isinstance(competitors, list) or not isinstance(adjacent, list):
        errors.append("research arrays invalid")
        competitors, adjacent = [], []
    if len(competitors) > 10 or len(adjacent) > 6:
        errors.append("maximum 10 direct / 6 cross-category references")
    if len(competitors) < 8 and not _meaningful(research.get("shortfall_reason"), 20):
        missing.append("research: 8–10 live direct references OR reason for smaller set")
    if len(adjacent) < 2 and not _meaningful(research.get("cross_category_shortfall_reason"), 20):
        missing.append("research: 2–4 cross-category references OR reason for smaller set")
    for lane, refs in (("direct", competitors), ("adjacent", adjacent)):
        seen: set[str] = set()
        for n, record in enumerate(refs):
            p = f"research.{lane}[{n}]"
            if not isinstance(record, dict):
                errors.append(f"{p}: record must be object")
                continue
            url = record.get("url")
            if not _valid_url(url):
                errors.append(f"{p}: valid source URL required")
            elif url in seen:
                errors.append(f"{p}: duplicate URL")
            else:
                seen.add(url)
            if record.get("decision") not in DECISIONS:
                missing.append(f"{p}: ADOPT / ADAPT / REJECT decision")
            for field in ("observed_mechanism", "original_application", "caveat"):
                if not _meaningful(record.get(field)):
                    missing.append(f"{p}.{field}: specific observation required")
            if not _meaningful(record.get("observed_date"), 8):
                missing.append(f"{p}: observation date required")
            for view in ("desktop", "mobile"):
                if not _image(root, record.get(view)):
                    missing.append(f"{p}.{view}: real PNG capture missing")

    concepts = packet.get("concepts", [])
    if not isinstance(concepts, list):
        errors.append("concepts must be array")
        concepts = []
    if len(concepts) < 2 and packet.get("mode") in {"REDESIGN", "REBUILD"}:
        missing.append("concepts: at least 2 genuinely distinct visual directions")
    ids: set[str] = set()
    for n, concept in enumerate(concepts):
        if not isinstance(concept, dict):
            errors.append(f"concepts[{n}] must be an object")
            continue
        ident = concept.get("id")
        if not isinstance(ident, str) or not ident or ident in ids:
            errors.append(f"concepts[{n}]: unique id required")
        else:
            ids.add(ident)
        for field in ("visual_thesis", "primary_focus", "removed_or_deferred", "mobile_recomposition"):
            if not _meaningful(concept.get(field)):
                missing.append(f"concepts[{n}].{field} required")
    if packet.get("chosen_concept") not in ids:
        missing.append("chosen_concept must match a concept id")

    render = packet.get("render", {})
    if not isinstance(render, dict):
        errors.append("render must be object")
        render = {}
    for phase in ("before", "after"):
        shots = render.get(phase, {})
        if not isinstance(shots, dict):
            errors.append(f"render.{phase} must be object")
            continue
        for view in ("desktop", "mobile"):
            if not _image(root, shots.get(view)):
                missing.append(f"render.{phase}.{view}: actual rendered PNG required")

    review = packet.get("review", {})
    if not isinstance(review, dict):
        errors.append("review must be object")
        review = {}
    verdict = review.get("verdict")
    if verdict not in VERDICTS:
        errors.append("review.verdict invalid")
    reviewer = review.get("reviewer_type")
    if reviewer not in REVIEWERS:
        errors.append("review.reviewer_type invalid")
    if verdict == "PASS" and reviewer == "NOT_REVIEWED":
        errors.append("PASS requires a reviewer, SELF_REVIEW is allowed but not human approval")
    for field in ("squint_focal_order", "signal_noise_review", "reference_contrast", "mobile_review", "decision_reason"):
        if not _meaningful(review.get(field)):
            missing.append(f"review.{field}: concrete visual assessment missing")
    removal_log = review.get("removal_log")
    if not isinstance(removal_log, list) or not removal_log or not all(_meaningful(x, 8) for x in removal_log):
        missing.append("review.removal_log: actual deletions/merges/defer decisions required")

    findings = review.get("critical_findings", [])
    if not isinstance(findings, list):
        errors.append("critical_findings must be array")
        findings = []
    for i, issue in enumerate(findings):
        if not isinstance(issue, dict) or issue.get("severity") not in {"P0", "P1", "P2"}:
            errors.append(f"critical_findings[{i}] invalid")
            continue
        if not _meaningful(issue.get("description")):
            missing.append(f"critical_findings[{i}].description required")
        if not isinstance(issue.get("resolved"), bool):
            errors.append(f"critical_findings[{i}].resolved must be bool")
        elif not issue["resolved"] and issue["severity"] in {"P0", "P1"}:
            blockers.append(f"unresolved {issue['severity']}: {issue.get('description', 'unnamed')}")
    if verdict in {"REWORK", "BLOCKED_WITH_EVIDENCE"}:
        blockers.append(f"visual reviewer said {verdict}; do not ship as premium")
    if reviewer != "HUMAN":
        warnings.append("Not human art-directed or user-tested; reviewer provenance must be honest")

    journey = packet.get("journey")
    if not isinstance(journey, dict):
        errors.append("journey must be object")
        journey = {}
    if journey.get("status") not in {"PASS", "FAIL", "NOT_TESTED"}:
        errors.append("journey.status invalid")
    if journey.get("status") == "FAIL":
        blockers.append("primary CTA-to-first-value journey FAIL")
    if journey.get("status") != "PASS":
        missing.append("primary journey not tested to actual first value")
    elif not _meaningful(journey.get("evidence_path"), 4):
        missing.append("journey PASS needs evidence_path")

    status = ("INVALID" if errors else
              "ART_DIRECTION_BLOCKED" if blockers else
              "NEEDS_EVIDENCE" if missing else
              "READY_FOR_HUMAN_REVIEW")
    return {
        "status": status,
        "errors": errors, "blockers": blockers, "missing": missing,
        "warnings": warnings,
        "notice": "Structural evidence gate only. No pixel understanding, quality certificate or conversion measurement."
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    p.add_argument("--root", type=Path, default=Path("."))
    args = p.parse_args()
    try:
        root = args.root.resolve(strict=True)
        data = json.loads(args.packet.read_text(encoding="utf-8"))
        result = inspect(data, root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "INVALID", "errors": [str(exc)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "READY_FOR_HUMAN_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
