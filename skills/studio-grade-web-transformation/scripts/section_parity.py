#!/usr/bin/env python3
"""Audit section-by-section visual evidence for a real redesign.

This checks coverage and existence of comparable artifacts. It never scores
beauty, reads screenshot pixels, tests users, or certifies conversion.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from functools import lru_cache
from pathlib import Path

MODES = {"REFINE", "REDESIGN", "REBUILD"}
CHANGES = {"KEEP", "REWORK", "ADD", "REMOVE"}
VERDICTS = {"BETTER", "WORSE", "MIXED", "SAME", "UNKNOWN"}
REVIEWERS = {"HUMAN", "INDEPENDENT_AGENT", "AGENT_SELF_REVIEW", "NOT_REVIEWED"}
VIEWPORTS = ("desktop", "mobile")
@lru_cache(maxsize=1)
def _validate_png():
    """Reuse the existing CRC/chunk validator rather than trusting PNG headers."""
    path = Path(__file__).with_name("production_evidence.py")
    spec = importlib.util.spec_from_file_location("section_parity_png", path)
    if spec is None or spec.loader is None:
        raise ValueError("Missing installed PNG validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.png_dimensions


def _artifact(root: Path, relative: object, *, png: bool) -> str:
    """Return PASS/MISSING/INVALID for a local file; reject escaping paths."""
    if relative is None or relative == "":
        return "MISSING"
    if not isinstance(relative, str) or "\\" in relative:
        return "INVALID"
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts or not relative.strip():
        return "INVALID"
    target = (root / rel).resolve()
    if not target.is_relative_to(root) or target.is_symlink():
        return "INVALID"
    if not target.is_file():
        return "MISSING"
    size = target.stat().st_size
    if not 0 < size <= 50_000_000:
        return "INVALID"
    if png:
        try:
            _validate_png()(target.read_bytes())
        except (ValueError, OSError):
            return "INVALID"
    return "PASS"


def inspect(packet: object, root: Path) -> dict:
    """Structural and evidence coverage audit, not a visual quality rating."""
    errors: list[str] = []
    blockers: list[str] = []
    missing: list[str] = []
    warnings: list[str] = []
    if not isinstance(packet, dict):
        return {"status": "INVALID", "errors": ["Expected JSON object"]}
    root = root.resolve(strict=True)

    if not isinstance(packet.get("mode"), str) or packet["mode"] not in MODES:
        errors.append("mode must be REFINE/REDESIGN/REBUILD")
    if not isinstance(packet.get("route"), str) or not packet["route"].startswith("/"):
        errors.append("route must start with /")

    inventory = packet.get("inventory")
    sections = packet.get("sections")
    if not isinstance(inventory, list) or not inventory or any(
        not isinstance(s, str) or not s.strip() for s in inventory
    ) or len(set(inventory)) != len(inventory):
        errors.append("inventory must contain unique nonempty section ids from the actual page")
        inventory = []
    if not isinstance(sections, list):
        errors.append("sections must be an array")
        sections = []

    seen: set[str] = set()
    reviewed = 0
    for index, section in enumerate(sections):
        where = f"sections[{index}]"
        if not isinstance(section, dict):
            errors.append(f"{where}: expected object")
            continue
        sid = section.get("id")
        if not isinstance(sid, str) or not sid.strip() or sid in seen:
            errors.append(f"{where}: missing/duplicate section id")
            continue
        seen.add(sid)
        where = sid
        change = section.get("change")
        if not isinstance(change, str) or change not in CHANGES:
            errors.append(f"{where}: change must be KEEP/REWORK/ADD/REMOVE")
            continue
        for name, min_length in (("purpose", 12), ("diagnosis", 20)):
            value = section.get(name)
            if not isinstance(value, str) or len(value.strip()) < min_length:
                errors.append(f"{where}: concrete {name} is required")

        if change == "REMOVE":
            reason = section.get("removal_reason")
            if not isinstance(reason, str) or len(reason.strip()) < 20:
                errors.append(f"{where}: explain why removal does not lose essential value")

        before, after = section.get("before", {}), section.get("after", {})
        if not isinstance(before, dict) or not isinstance(after, dict):
            errors.append(f"{where}: before/after must be viewport objects")
            continue
        for stage, required in (("before", change != "ADD"), ("after", change != "REMOVE")):
            if not required:
                continue
            shots = before if stage == "before" else after
            for viewport in VIEWPORTS:
                result = _artifact(root, shots.get(viewport), png=True)
                if result == "INVALID":
                    errors.append(f"{where}: {stage}.{viewport} invalid or unsafe PNG")
                elif result == "MISSING":
                    missing.append(f"{where}: {stage}.{viewport} screenshot missing")

        assessment = section.get("assessment")
        if not isinstance(assessment, dict):
            errors.append(f"{where}: assessment object required")
            continue
        verdict = assessment.get("verdict")
        reviewer = assessment.get("reviewer_type")
        if not isinstance(verdict, str) or verdict not in VERDICTS or not isinstance(reviewer, str) or reviewer not in REVIEWERS:
            errors.append(f"{where}: invalid verdict or reviewer_type")
            continue
        if verdict == "UNKNOWN":
            missing.append(f"{where}: visual comparison not reviewed")
        else:
            if reviewer == "NOT_REVIEWED":
                errors.append(f"{where}: a verdict requires a named review type")
            reason = assessment.get("reason")
            if not isinstance(reason, str) or len(reason.strip()) < 24:
                errors.append(f"{where}: justify the review with concrete pixel observations")
            else:
                reviewed += 1
        if reviewer != "HUMAN":
            warnings.append(f"{where}: no representative human preference or comprehension test")
        if verdict == "WORSE" and change != "REMOVE":
            blockers.append(f"{where}: the redesign was judged worse and needs repair")

    if set(inventory) != seen:
        errors.append(
            f"inventory coverage mismatch: missing={sorted(set(inventory)-seen)} "
            f"unlisted={sorted(seen-set(inventory))}"
        )

    journey = packet.get("primary_journey")
    if not isinstance(journey, dict):
        errors.append("primary_journey must describe a tested CTA/core task to first value")
    else:
        state = journey.get("status")
        if not isinstance(state, str) or state not in {"PASS", "FAIL", "UNKNOWN"}:
            errors.append("primary_journey.status must be PASS/FAIL/UNKNOWN")
        for field in ("entry", "first_value"):
            if not isinstance(journey.get(field), str) or len(journey[field].strip()) < 8:
                errors.append("primary_journey." + field + " must describe a real task")
        if state == "FAIL":
            blockers.append("primary_journey: core action failed")
        elif state == "UNKNOWN":
            missing.append("primary_journey: not tested")
        else:
            evidence = journey.get("evidence", [])
            if not isinstance(evidence, list) or not evidence:
                missing.append("primary_journey: PASS lacks local evidence")
            else:
                for file in evidence:
                    result = _artifact(root, file, png=False)
                    if result == "INVALID":
                        errors.append("primary_journey: invalid/unsafe evidence path")
                    elif result == "MISSING":
                        missing.append("primary_journey: evidence file missing")

    findings = packet.get("critical_findings", [])
    if not isinstance(findings, list):
        errors.append("critical_findings must be an array")
        findings = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict) or not isinstance(finding.get("severity"), str) or finding["severity"] not in {"P0", "P1", "P2"} or not isinstance(finding.get("state"), str) or finding["state"] not in {"OPEN", "FIXED"}:
            errors.append(f"critical_findings[{index}]: invalid severity/state")
        elif finding["severity"] in {"P0", "P1"} and finding["state"] != "FIXED":
            blockers.append(f"critical_findings[{index}]: unresolved {finding['severity']}")

    status = (
        "INVALID" if errors else
        "BLOCKED" if blockers else
        "NEEDS_EVIDENCE" if missing else
        "READY_FOR_HUMAN_REVIEW"
    )
    return {
        "status": status,
        "inventory_count": len(inventory),
        "sections_recorded": len(seen),
        "sections_with_recorded_visual_judgment": reviewed,
        "errors": errors,
        "blockers": blockers,
        "missing_evidence": missing,
        "warnings": warnings,
        "limitations": [
            "The inventory is user/agent-declared; this script cannot detect omitted DOM sections.",
            "PNG signature/end checks do not decode or visually judge screenshots.",
            "Recorded PASS/verdicts are assertions, not independently executed tests.",
            "READY_FOR_HUMAN_REVIEW is not proof of aesthetics, preference, accessibility or conversion.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="Section matrix JSON")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root containing screenshots")
    args = parser.parse_args()
    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        report = inspect(packet, args.root)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        report = {"status": "INVALID", "errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "READY_FOR_HUMAN_REVIEW":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
