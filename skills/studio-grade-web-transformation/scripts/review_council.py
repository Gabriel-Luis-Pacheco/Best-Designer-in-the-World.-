#!/usr/bin/env python3
"""Select focused critique roles; validate traceable findings without pretending users exist."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROLES = {
    "brief_guardian": ("Original intent fidelity", "Compare original request with what was built; check exact names, promised behaviors, required assets and silent scope changes."),
    "first_time_viewer": ("Five-second comprehension", "Review a rendered first visit without the builder rationale: what is this, why care, what can I do? Identify evidence, not a fabricated user reaction."),
    "prospective_customer": ("Buyer objections", "Assess value, price/terms truth, proof, trust and whether the next action is worth taking from a hypothetical buyer lens. Never claim real customer research."),
    "positioning_copy_editor": ("Copy and positioning", "Compare copy to real alternatives, audience language, differentiated value, credible proof, CTA and brand tone; show exact confusing text."),
    "search_discovery": ("Search/metadata", "Inspect relevant public URLs, titles, query intent, crawlable links, technical indexability, JS rendering and Search Console gaps; do not promise rank."),
    "art_director": ("Visual authorship", "Inspect opening, middle, ending and mobile; criticize generic grammar, weak signature, pacing, legibility and actual assets."),
    "accessibility_mobile": ("Inclusive usability", "Check narrow viewports, touch/keyboard/focus, text, contrast, reduced motion and recovery states with actual evidence."),
    "functional_reviewer": ("Real functionality", "Run real navigation, forms, routes, critical product states, errors, data/price safety and regressions."),
    "task_operator": ("Product task", "Attempt the true end-user job; flag any decorative replacement for genuine workflow, context loss, duplication or dead end."),
    "motion_story_editor": ("Interactive narrative", "Inspect actual timed/interactive states, gesture consequences, climax and skip/replay; test reduced motion and no-GPU fallback."),
    "reference_identity": ("Named visual fidelity", "Match each explicitly named entity to confirmed canonical references and the rendered subject; do not accept generic substitutes."),
}
MODES = {"INDEPENDENT_AGENT", "SEQUENTIAL_SELF_REVIEW", "REAL_USER"}


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
        chosen = [x for x in chosen if x in {"brief_guardian", "first_time_viewer", "functional_reviewer", "accessibility_mobile"}]
    return [{"role": x, "lens": ROLES[x][0], "task": ROLES[x][1]} for x in chosen]


def inspect(data: dict) -> dict:
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["Expected object"]}
    surface, mode = data.get("surface"), data.get("mode")
    errors, blockers, limitations = [], [], []
    if not isinstance(surface, str) or not surface.strip():
        errors.append("surface required")
        surface = "product"
    if mode not in {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}:
        errors.append("Valid workflow mode required")
        mode = "AUDIT"
    assignments = plan(surface, mode)
    expected = {r["role"] for r in assignments}
    reviews = data.get("reviews", [])
    if not isinstance(reviews, list):
        errors.append("reviews must be an array")
        reviews = []
    received, invocation_ids = set(), set()
    for entry in reviews:
        if not isinstance(entry, dict) or entry.get("role") not in ROLES:
            errors.append("Review must declare a recognized role")
            continue
        role = entry["role"]
        if role not in expected:
            errors.append(role + ": role outside selected scope")
        if role in received:
            errors.append(role + ": duplicate review")
        received.add(role)
        review_mode = entry.get("review_mode")
        if review_mode not in MODES:
            errors.append(role + ": must disclose independent agent, sequential self-review, or real user")
        if review_mode == "INDEPENDENT_AGENT":
            trace = entry.get("agent_invocation_id")
            if not isinstance(trace, str) or len(trace.strip()) < 6 or trace in invocation_ids:
                errors.append(role + ": independent agent claim needs unique invocation trace")
            else:
                invocation_ids.add(trace)
        if review_mode == "REAL_USER":
            if not entry.get("recruitment_record"):
                errors.append(role + ": cannot claim real user without recruitment/session trace")
        if entry.get("saw_builder_rationale") is True and role == "first_time_viewer":
            limitations.append("First-time critique was not blind to builder rationale")
        observations = entry.get("findings", [])
        if not isinstance(observations, list):
            errors.append(role + ": findings must be a list")
            continue
        for issue in observations:
            if not isinstance(issue, dict):
                errors.append(role + ": issue must be an object")
                continue
            if issue.get("severity") not in {"P0", "P1", "P2", "NOTE"}:
                errors.append(role + ": issue severity P0/P1/P2/NOTE required")
            if not isinstance(issue.get("observation"), str) or len(issue["observation"].strip()) < 15:
                errors.append(role + ": describe precisely what was observed")
            if not isinstance(issue.get("evidence"), list) or not issue["evidence"]:
                errors.append(role + ": show a screenshot, exact route, interaction trace or other verifiable evidence")
            if not isinstance(issue.get("recommendation"), str) or len(issue["recommendation"].strip()) < 12:
                errors.append(role + ": give actionable causal recommendation")
            if issue.get("severity") in {"P0", "P1"}:
                blockers.append(role + ": " + issue.get("observation", "major failure"))
    missing = sorted(expected - received)
    if not reviews:
        state = "ASSIGNMENTS_ONLY"
    elif errors:
        state = "INVALID"
    elif blockers:
        state = "BLOCKED"
    elif missing:
        state = "INCOMPLETE"
    else:
        state = "REVIEWED_NOT_CERTIFIED"
    limitations.extend(["Model role-play is not observed customer behavior",
                        "Independent invocation IDs are declarations; inspect actual agent/tool traces",
                        "Agreement among simulated reviewers is not independent user evidence",
                        "No automatic aesthetic pass, conversion claim or accessibility certification"])
    return {"status": state, "assignments": assignments, "missing_roles": missing,
            "errors": errors, "blockers": blockers, "limitations": limitations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    try:
        if args.packet.stat().st_size > 200_000:
            raise ValueError("Packet exceeds 200 KB")
        result = inspect(json.loads(args.packet.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, "INVALID INPUT: " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] not in {"ASSIGNMENTS_ONLY", "REVIEWED_NOT_CERTIFIED"}:
        parser.exit(2)


if __name__ == "__main__":
    main()
