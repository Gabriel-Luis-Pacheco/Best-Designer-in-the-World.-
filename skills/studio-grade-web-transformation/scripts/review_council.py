#!/usr/bin/env python3
"""Plan scoped critique roles and reject empty/fake review evidence.

Never treats model role-play as user research or an invocation ID as an
authenticated subagent trace. Inspect underlying evidence before release.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROLES = {
    "brief_guardian": ("Original intent fidelity", "Re-read original wording and amendments; compare exact subjects, behaviors, core assets and protected routes against the actual output."),
    "first_time_viewer": ("First-visit comprehension", "See the rendered first viewport without the builder's rationale. Is the real offering legible? Identify observed evidence, not fabricated reactions."),
    "prospective_customer": ("Buyer objections", "Inspect price/terms, value, trust and actual proof from a hypothetical buyer lens; never claim customer interviews."),
    "positioning_copy_editor": ("Copy and positioning", "Review true alternatives, qualified value, claims, tone, proof, CTA and exact confusing strings."),
    "search_discovery": ("Search and discovery", "Review public page intent, indexability, metadata and crawlable links; leave live rankings and Search Console UNKNOWN if not checked."),
    "art_director": ("Visual authorship", "Inspect opening, middle, ending, original subject and mobile; critique context-specific visual and motion craft."),
    "accessibility_mobile": ("Inclusive usability", "Inspect keyboard, focus, labels, reflow, touch, contrast, reduced motion, errors and recovery."),
    "functional_reviewer": ("Real functionality", "Exercise actual routes, navigation, forms, error paths, data contracts and regressions."),
    "task_operator": ("End-user task", "Complete the real user job; reject decorated mockups that cannot perform the task."),
    "motion_story_editor": ("Interactive dramaturgy", "Review motion cues, input consequences, skip/replay and fallbacks across real states."),
    "reference_identity": ("Exact named reference", "Compare output to canonical supplied/authoritative identity; generic stand-ins do not pass."),
}
MODES = {"INDEPENDENT_AGENT", "SEQUENTIAL_SELF_REVIEW", "REAL_USER"}
WORKFLOW_MODES = {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}
SEVERITIES = {"P0", "P1", "P2", "NOTE"}
VERDICTS = {"NO_ISSUES_OBSERVED", "ISSUES_FOUND", "UNKNOWN"}


def substantial(value: object, minimum: int = 12) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum


def references(value: object) -> bool:
    return (isinstance(value, list) and bool(value) and
            all(isinstance(x, str) and bool(x.strip()) for x in value))


def plan(surface: str, mode: str) -> list[dict]:
    surface = surface.casefold()
    chosen = ["brief_guardian", "first_time_viewer", "art_director", "functional_reviewer"]
    if surface in {"landing", "marketing", "commerce", "experiential_commerce"}:
        chosen += ["prospective_customer", "positioning_copy_editor", "search_discovery"]
    elif surface in {"product", "mobile", "dashboard", "internal", "checkout"}:
        chosen += ["task_operator", "accessibility_mobile"]
    elif surface in {"art", "experience"}:
        chosen += ["motion_story_editor", "reference_identity"]
    elif surface in {"read", "docs"}:
        chosen += ["search_discovery", "accessibility_mobile"]
    if mode in {"PATCH", "AUDIT"}:
        chosen = [x for x in chosen if x in
                  {"brief_guardian", "first_time_viewer", "functional_reviewer", "accessibility_mobile"}]
    return [{"role": name, "lens": ROLES[name][0], "task": ROLES[name][1]}
            for name in chosen]


def inspect(data: dict) -> dict:
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["Expected an object"]}
    surface, mode = data.get("surface"), data.get("mode")
    errors, blockers, limitations, incomplete = [], [], [], []
    if not isinstance(surface, str) or not surface.strip():
        errors.append("A nonempty surface is required")
        surface = "product"
    if not isinstance(mode, str) or mode not in WORKFLOW_MODES:
        errors.append("Workflow mode must be PATCH/AUDIT/REFINE/REDESIGN/REBUILD")
        mode = "AUDIT"
    assignments = plan(surface, mode)
    expected = {r["role"] for r in assignments}
    reviews = data.get("reviews", [])
    if not isinstance(reviews, list):
        errors.append("reviews must be an array")
        reviews = []
    received, invocation_ids = set(), set()
    for entry in reviews:
        if not isinstance(entry, dict) or not isinstance(entry.get("role"), str) or entry["role"] not in ROLES:
            errors.append("Review must declare a known string role")
            continue
        role = entry["role"]
        if role not in expected:
            errors.append(role + ": role outside selected scope")
        if role in received:
            errors.append(role + ": repeated reviewer role")
        received.add(role)
        review_mode = entry.get("review_mode")
        if not isinstance(review_mode, str) or review_mode not in MODES:
            errors.append(role + ": disclose real-agent, self-review or real-user mode")
        if review_mode == "INDEPENDENT_AGENT":
            trace = entry.get("agent_invocation_id")
            if not substantial(trace, 6) or trace in invocation_ids:
                errors.append(role + ": unique real agent invocation trace required")
            else:
                invocation_ids.add(trace)
        if review_mode == "REAL_USER" and not substantial(entry.get("recruitment_record"), 6):
            errors.append(role + ": real-user claim needs a session/recruitment trace")
        if entry.get("saw_builder_rationale") is True and role == "first_time_viewer":
            limitations.append("First-time viewer saw builder rationale; do not call blind")
        if not substantial(entry.get("task_observed")):
            errors.append(role + ": describe the concrete task/state inspected")
        if not references(entry.get("inspected_evidence")):
            errors.append(role + ": list actual inspected screenshots/routes/traces")
        verdict = entry.get("verdict")
        if not isinstance(verdict, str) or verdict not in VERDICTS:
            errors.append(role + ": verdict must be NO_ISSUES_OBSERVED/ISSUES_FOUND/UNKNOWN")
            verdict = "UNKNOWN"
        findings = entry.get("findings", [])
        if not isinstance(findings, list):
            errors.append(role + ": findings must be a list")
            findings = []
        if verdict == "NO_ISSUES_OBSERVED" and findings:
            errors.append(role + ": no-issues verdict contradicts supplied findings")
        if verdict == "ISSUES_FOUND" and not findings:
            errors.append(role + ": issues-found verdict requires specific findings")
        if verdict == "UNKNOWN":
            if not substantial(entry.get("reason")):
                errors.append(role + ": UNKNOWN needs a concrete unverified reason")
            incomplete.append(role + ": review not verified")
        for issue in findings:
            if not isinstance(issue, dict):
                errors.append(role + ": finding must be an object")
                continue
            severity = issue.get("severity")
            if not isinstance(severity, str) or severity not in SEVERITIES:
                errors.append(role + ": P0/P1/P2/NOTE severity required")
                continue
            if not substantial(issue.get("observation"), 15):
                errors.append(role + ": state a precise observed failure")
            if not references(issue.get("evidence")):
                errors.append(role + ": finding must cite an inspected artifact/route/trace")
            if not substantial(issue.get("recommendation")):
                errors.append(role + ": recommend a causal fix")
            resolution = issue.get("resolution", "OPEN")
            if resolution not in {"OPEN", "VERIFIED_FIXED"}:
                errors.append(role + ": finding resolution must be OPEN/VERIFIED_FIXED")
            if severity in {"P0", "P1"}:
                if resolution == "VERIFIED_FIXED":
                    if not references(issue.get("fix_evidence")):
                        errors.append(role + ": resolved major finding requires post-fix evidence")
                else:
                    blockers.append(role + ": " + str(issue.get("observation", "major issue")))
    missing = sorted(expected - received)
    if not reviews and not errors:
        state = "ASSIGNMENTS_ONLY"
    elif errors:
        state = "INVALID"
    elif blockers:
        state = "BLOCKED"
    elif missing or incomplete:
        state = "INCOMPLETE"
    else:
        state = "REVIEWED_NOT_CERTIFIED"
    limitations.extend([
        "References are declarations; inspect the actual files/routes and source traces",
        "A self-reviewed buyer role is not an actual customer's response",
        "Agent invocation IDs do not authenticate independent execution",
        "No automatic certification of visual quality, conversion or accessibility",
    ])
    return {"status": state, "assignments": assignments, "missing_roles": missing,
            "incomplete_reviews": incomplete, "errors": errors,
            "blockers": blockers, "limitations": limitations}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    args = p.parse_args()
    try:
        if args.packet.stat().st_size > 200_000:
            raise ValueError("Packet exceeds 200 KB")
        report = inspect(json.loads(args.packet.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        p.exit(2, "INVALID INPUT: " + str(exc) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] not in {"ASSIGNMENTS_ONLY", "REVIEWED_NOT_CERTIFIED"}:
        p.exit(2)


if __name__ == "__main__":
    main()
