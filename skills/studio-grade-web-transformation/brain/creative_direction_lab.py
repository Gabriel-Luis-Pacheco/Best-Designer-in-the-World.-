#!/usr/bin/env python3
"""Propose surface-aware structural hypotheses from declared evidence, without I/O.

This bounded pattern selector is NOT a creative intelligence, source verifier,
site builder or aesthetic evaluator. An agent must inspect and override it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SURFACES = {"landing", "product", "dashboard", "internal", "experience", "commerce",
            "read", "mobile", "checkout", "experiential_commerce"}
TECHNOLOGIES = {"gsap", "webgl", "webgpu", "three.js", "rive", "css", "svg"}
EVIDENCE_TYPES = {"demo", "photography", "records", "process", "collection",
                  "narrative", "comparison", "documentation"}
SCENE_KEYS = ("opening", "recognition", "middle", "interaction", "closure")

# Different structures, not random palette/brand-name substitutions. Evidence
# requirements are declared availability, never independent source verification.
PATTERNS = {
    "task-first": ("Task-first density", "Organize around the next costly operation.",
                   "compact task-oriented grid", "Move through real task states with context retained."),
    "evidence-first": ("Evidence-first workbench", "Organize source evidence before decisions.",
                       "document-led split workbench", "Inspect a source and return to the same record."),
    "search-first": ("Question-led reference", "Organize by the reader's question and stable topic paths.",
                     "search and topic index with readable article rail", "Find an answer and preserve the return path."),
    "guided-reading": ("Guided explanation", "Sequence prerequisite knowledge before advanced detail.",
                       "progressive reading path with contextual examples", "Follow an example and navigate back without losing place."),
    "guided-task": ("Progressive task", "Expose the minimum useful next decision and its consequences.",
                    "sequential task canvas with persistent summary", "Complete a real step and recover without restarting."),
    "workspace": ("Direct workspace", "Keep the working object and its controls in one context.",
                  "object-centered workspace with adjacent tools", "Edit a permitted state with visible feedback and recovery."),
    "review-first": ("Review and confirm", "Make selected items, totals and terms inspectable before commitment.",
                     "order summary beside the transaction form", "Correct a choice before a real confirmation."),
    "recovery-first": ("Resilient purchase path", "Order purchase decisions around continuity and error recovery.",
                        "progressive transaction steps with persistent total", "Recover a failed step without losing valid choices."),
    "catalog-first": ("Browse and narrow", "Organize verified items around meaningful selection criteria.",
                      "browsable catalog followed by focused item detail", "Narrow real items and inspect a preserved selection."),
    "product-proof": ("Product demonstration", "Make actual behavior the main explanation of value.",
                      "demonstration stage with adjacent evidence and next action", "Try only the behavior the real product supports."),
    "editorial-proof": ("Editorial demonstration", "Explain a distinctive product property through type, crop and pacing.",
                        "editorial chapters organized around a real product property", "Reveal the evidence supporting one concrete claim."),
    "living-artifact": ("Evolving artifact", "Explore a supplied object or concept through connected states.",
                        "continuous spatial sequence centered on a supplied artifact", "Propose a reversible transformation only if the runtime supports it."),
    "process-led": ("Visible process", "Use a declared sequence to explain cause and consequence.",
                    "connected process stages with progressive evidence", "Inspect a real stage and its inputs or outputs."),
    "comparison-led": ("Decision through comparison", "Organize around supplied differences and decision criteria.",
                       "aligned comparison followed by a focused recommendation space", "Compare verified alternatives without concealing conditions."),
    "collection-led": ("Curated collection", "Use relationships between supplied items as the narrative.",
                       "collection index linked to focused object studies", "Explore an item and retain collection context."),
    "narrative-led": ("Authored narrative", "Compose a supplied story as connected reveals and resolution.",
                      "paced narrative scenes with a contextual ending", "Offer agency that changes understanding of the supplied story."),
    "image-led": ("Material close study", "Let authorized photography demonstrate a tangible property.",
                  "large image studies with precise product annotations", "Inspect real details without substituting invented product imagery."),
}
DEFAULTS = {
    "internal": ("task-first", "evidence-first"),
    "dashboard": ("task-first", "evidence-first"),
    "read": ("search-first", "guided-reading"),
    "product": ("guided-task", "workspace"),
    "mobile": ("guided-task", "workspace"),
    "checkout": ("review-first", "recovery-first"),
    "commerce": ("product-proof", "catalog-first"),
    "landing": ("editorial-proof", "product-proof"),
    "experience": ("editorial-proof", "living-artifact"),
    "experiential_commerce": ("product-proof", "living-artifact"),
}
EVIDENCE_PATTERNS = {
    "demo": "product-proof", "photography": "image-led", "records": "evidence-first",
    "process": "process-led", "collection": "collection-led", "narrative": "narrative-led",
    "comparison": "comparison-led", "documentation": "guided-reading",
}
# Scope beats an exciting but irrelevant evidence type: do not suggest a
# photographic art showcase for a checkout or operational record task.
ELIGIBLE_EVIDENCE = {
    "internal": ("records", "process", "comparison"),
    "dashboard": ("records", "comparison", "process"),
    "read": ("documentation", "process", "comparison"),
    "product": ("process", "records", "comparison"),
    "mobile": ("process", "records", "comparison"),
    "checkout": (),
    "commerce": ("photography", "comparison", "demo", "collection", "process"),
    "landing": ("demo", "photography", "process", "comparison", "collection", "narrative"),
    "experience": ("collection", "narrative", "photography", "process", "demo"),
    "experiential_commerce": ("photography", "demo", "narrative", "collection", "process", "comparison"),
}


def _string(value, name, required=False):
    if not isinstance(value, str) or len(value) > 1000:
        raise ValueError(name + " must be a string <= 1000 characters")
    value = value.strip()
    if required and not value:
        raise ValueError(name + " is required")
    return value


def _strings(value, name, limit=20):
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > limit:
        raise ValueError(name + " must be an array of at most " + str(limit))
    return list(dict.fromkeys(_string(x, name + " item", True) for x in value))


def _boolean(data, name):
    value = data.get(name, False)
    if not isinstance(value, bool):
        raise ValueError(name + " must be a boolean")
    return value


def _make_concept(key, brief, surface, evidence):
    label, thesis, layout, gesture = PATTERNS[key]
    product = brief["product"]
    action = brief["real_action"] or "UNKNOWN — verify the actual user action before implementation"
    facts = brief["product_facts"]
    jobs = brief["user_jobs"]
    assets = brief["available_assets"]
    grounding = {"product_facts_supplied_unverified": facts,
                 "user_jobs_supplied_unverified": jobs,
                 "assets_supplied_unverified": assets,
                 "objective_supplied_unverified": brief["objective"] or "UNKNOWN",
                 "audience_supplied_unverified": brief["audience"] or "UNKNOWN"}
    focus = facts[0] if facts else "UNKNOWN — inspect a distinctive product fact"
    need = jobs[0] if jobs else "UNKNOWN — inspect the actual user job"
    asset = assets[0] if assets else "UNKNOWN — inspect authorized original assets"
    opening = "Introduce " + product + " around: " + need + ". Proposed structure: " + layout + "."
    middle = "Develop this supplied fact: " + focus + ". Proposed evidence mechanism: " + thesis
    closure = "Resolve the opening and present only the verified next action: " + action
    if surface in {"internal", "dashboard"}:
        opening = "Show the actual task and current state for " + product + ": " + need
        middle = "Inspect real records and source evidence for: " + focus + ". " + thesis
        closure = "Confirm real outcome, recovery and source trace; never invent success: " + action
    elif surface == "read":
        opening = "Orient the reader of " + product + " to: " + need + ". " + layout
        closure = "Provide a stable related topic or return path; do not add a sales funnel."
    elif surface == "checkout":
        opening = "Show actual selection, price and terms for " + product + ". " + layout
        closure = "Confirm only a real transaction outcome and recovery path; never simulate payment success."
    return {
        "id": key, "title": label, "visual_thesis": thesis,
        "composition": layout, "signature_gesture": gesture,
        "product_grounding": action, "declared_grounding": grounding,
        "fit_basis": ["surface=" + surface] + ["declared evidence=" + e for e in evidence
                                                  if EVIDENCE_PATTERNS[e] == key],
        "scenes": dict(zip(SCENE_KEYS, (
            opening, "Keep " + product + " recognizable using: " + asset,
            middle, "Only if verified: " + action + ". Proposed behavior: " + gesture, closure))),
        "mobile_direction": "Recompose at 320/390px around the same user job; retain context, keyboard/zoom and recovery.",
        "preserve": brief["brand_invariants"] + brief["protected_flows"],
        "proof_required": ["Inspect supplied facts, original assets and real capability before implementation",
                           "Render representative opening, middle, ending and mobile states",
                           "Test the real task, error recovery and reduced motion where applicable"],
        "risk": "A reusable pattern can still be generic or wrong; verify the actual product and replace it when needed.",
    }


def propose(input_data):
    if not isinstance(input_data, dict):
        raise ValueError("brief must be a JSON object")
    if len(json.dumps(input_data, ensure_ascii=False)) > 20000:
        raise ValueError("brief too large")
    brief = {name: _string(input_data.get(name, ""), name, name in {"task", "product"})
             for name in ("task", "product", "objective", "audience", "real_action", "existing_direction")}
    for name in ("brand_invariants", "protected_flows", "product_facts", "user_jobs", "available_assets"):
        brief[name] = _strings(input_data.get(name), name)
    surface = _string(input_data.get("surface", "landing"), "surface").lower() or "landing"
    if surface not in SURFACES:
        raise ValueError("surface must be one of " + ", ".join(sorted(SURFACES)))
    mode = _string(input_data.get("mode", "REBUILD"), "mode").upper()
    if mode not in {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}:
        raise ValueError("invalid mode")
    locked = _boolean(input_data, "direction_locked")
    explore = _boolean(input_data, "explore_directions")
    evidence = _strings(input_data.get("evidence_types"), "evidence_types")
    if set(evidence) - EVIDENCE_TYPES:
        raise ValueError("unknown evidence_types; use " + ", ".join(sorted(EVIDENCE_TYPES)))
    prohibited = _strings(input_data.get("prohibited_technologies"), "prohibited_technologies")
    requested = _strings(input_data.get("requested_technologies"), "requested_technologies")
    allowed = sorted({t.lower() for t in requested if t.lower() in TECHNOLOGIES}
                     - {t.lower() for t in prohibited})
    base = {"task": brief["task"], "product": brief["product"], "surface": surface, "mode": mode,
            "requested_technologies_allowed": allowed, "no_implicit_3d_or_animation_stack": True,
            "preserve": brief["brand_invariants"] + brief["protected_flows"],
            "existing_direction": brief["existing_direction"] or "UNKNOWN",
            "limits": "Deterministic pattern selection only; supplied evidence remains unverified. No sources retrieved, implementation, pixels or user research."}
    if mode in {"PATCH", "AUDIT"} or locked or (mode == "REFINE" and not explore):
        return dict(base, status="NO_CREATIVE_REBUILD_REQUIRED", concepts=[],
                    next="Inspect the requested scope and preserve the existing direction; no forced alternatives.")
    eligible = ELIGIBLE_EVIDENCE[surface]
    keys = [EVIDENCE_PATTERNS[e] for e in eligible if e in evidence]
    keys = list(dict.fromkeys(keys + list(DEFAULTS[surface])))[:2]
    concepts = [_make_concept(k, brief, surface, evidence) for k in keys]
    gaps = [field for field in ("product_facts", "user_jobs", "available_assets", "real_action", "objective", "audience")
            if not brief[field]]
    return dict(base, status="PROPOSALS_NOT_RENDERED_NOT_TESTED", concepts=concepts,
                primary_objective=brief["objective"] or "UNKNOWN — establish the outcome",
                audience=brief["audience"] or "UNKNOWN — verify rather than invent personas",
                context_gaps=gaps, evidence_types_supplied_unverified=evidence,
                selection_rule="No winner or preferred order. Inspect actual evidence; compare materially different rendered proofs when scope allows. Preserve losses and replace generic patterns.",
                next="Author a product-specific mechanism beyond these structural hypotheses; implement and inspect it.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Path to a JSON brief")
    args = parser.parse_args()
    try:
        data = json.loads(args.brief.read_text(encoding="utf-8"))
        print(json.dumps(propose(data), ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, "INVALID CREATIVE BRIEF: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
