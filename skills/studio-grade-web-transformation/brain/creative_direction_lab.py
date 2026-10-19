#!/usr/bin/env python3
"""Generate two buildable, non-identical art-direction hypotheses from declared facts.

This is a deterministic creative preflight, NOT a taste engine, reference browser,
site builder, image generator, or guarantee of beauty. No network or side effects.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SURFACES = {"landing", "product", "dashboard", "internal", "experience", "commerce"}
TECHNOLOGIES = {"gsap", "webgl", "webgpu", "three.js", "rive", "css", "svg"}
SCENE_KEYS = ("opening", "recognition", "middle", "interaction", "closure")


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
    return [_string(x, name + " item", True) for x in value]


def _make_concept(key, label, direction, gesture, layout, brief, operational):
    product = brief["product"]
    action = brief["real_action"] or "UNKNOWN — verify the actual user action before implementation"
    if operational:
        scene_map = {
            "opening": "Show the task, current state and next actionable step, not a cinematic hero.",
            "recognition": "Make " + product + " and the authorized data source unambiguous.",
            "middle": "Show actual records, cases and density states; never invent live data.",
            "interaction": "Complete and reverse a REAL permitted task: " + action,
            "closure": "Confirm outcome, next action, recovery and auditability; no fake success."
        }
    else:
        scene_map = {
            "opening": "Make " + product + " recognizable through this specific " + layout + " language.",
            "recognition": "Demonstrate a real property of " + product + ", not a stock illustration.",
            "middle": "Progress the argument with a visibly different but connected scene.",
            "interaction": "Let visitors meaningfully perform: " + action + ". " + gesture,
            "closure": "Resolve the opening idea and present only a truthful existing next action."
        }
    return {
        "id": key,
        "title": label,
        "visual_thesis": direction,
        "composition": layout,
        "signature_gesture": gesture,
        "product_grounding": action,
        "scenes": {k: scene_map[k] for k in SCENE_KEYS},
        "mobile_direction": (
            "Recompose at 320/390px: task first, persistent context, keyboard/zoom safe."
            if operational else
            "Author a 320/390px sequence, not a squeezed desktop canvas. Preserve recognition and payoff."
        ),
        "preserve": brief["brand_invariants"] + brief["protected_flows"],
        "proof_required": [
            "Two or more ACTUAL rendered frames showing the proposed visual mechanism",
            "Real interaction before/after and reduced-motion fallback",
            "360-degree whole-page critique: opener, middle, ending, mobile",
            "Working product fact/CTA checks; otherwise mark UNKNOWN"
        ],
        "risk": ("Data, permissions, table accuracy and state recovery" if operational
                 else "Visual originality without losing product recognition and task clarity")
    }


def propose(input_data):
    if not isinstance(input_data, dict):
        raise ValueError("brief must be a JSON object")
    if len(json.dumps(input_data, ensure_ascii=False)) > 20000:
        raise ValueError("brief too large")
    task = _string(input_data.get("task", ""), "task", True)
    product = _string(input_data.get("product", ""), "product", True)
    surface = _string(input_data.get("surface", "landing"), "surface").lower() or "landing"
    if surface not in SURFACES:
        raise ValueError("surface must be one of " + ", ".join(sorted(SURFACES)))
    mode = _string(input_data.get("mode", "REBUILD"), "mode").upper()
    if mode not in {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}:
        raise ValueError("invalid mode")
    objective = _string(input_data.get("objective", ""), "objective")
    audience = _string(input_data.get("audience", ""), "audience")
    action = _string(input_data.get("real_action", ""), "real_action")
    locked = _strings(input_data.get("brand_invariants"), "brand_invariants")
    flows = _strings(input_data.get("protected_flows"), "protected_flows")
    prohibited = _strings(input_data.get("prohibited_technologies"), "prohibited_technologies")
    requested = _strings(input_data.get("requested_technologies"), "requested_technologies")
    allowed = sorted({t.lower() for t in requested if t.lower() in TECHNOLOGIES}
                     - {t.lower() for t in prohibited})
    brief = {"product": product, "real_action": action,
             "brand_invariants": locked, "protected_flows": flows}
    ops = surface in ("internal", "dashboard")
    if mode in ("PATCH", "AUDIT"):
        return {
            "status": "NO_CREATIVE_REBUILD_REQUIRED",
            "product": product, "surface": surface, "mode": mode,
            "concepts": [],
            "next": "Inspect the requested scope; do not force alternatives or redesign.",
            "limits": "No code, research, pixels or tests were executed."
        }
    if ops:
        concepts = [
            _make_concept("task-first", "Task-first density",
                          "Information hierarchy follows the most costly real operation.",
                          "The next state appears inside the workflow with undo/recovery.",
                          "compact task-oriented grid", brief, True),
            _make_concept("evidence-first", "Evidence-first workbench",
                          "The interface organizes evidence and comparisons before actions.",
                          "Inspect source evidence and return to the exact record.",
                          "document-led split workbench", brief, True)
        ]
    else:
        concepts = [
            _make_concept("editorial-proof", "Editorial demonstration",
                          "Use product-specific typography, crop and pacing as a demonstration.",
                          "One true action reorders the story and reveals new information.",
                          "editorial chapters with deliberate asymmetry", brief, False),
            _make_concept("living-artifact", "Living artifact",
                          "Build a recognizable artifact whose state evolves across the page.",
                          "The visitor changes a real, reversible property of the artifact.",
                          "continuous spatial sequence with evolving object", brief, False)
        ]
    return {
        "status": "PROPOSALS_NOT_RENDERED_NOT_TESTED",
        "task": task,
        "product": product,
        "surface": surface,
        "mode": mode,
        "primary_objective": objective or "UNKNOWN — establish the outcome from user/product evidence",
        "audience": audience or "UNKNOWN — verify rather than invent personas",
        "requested_technologies_allowed": allowed,
        "no_implicit_3d_or_animation_stack": True,
        "concepts": concepts,
        "selection_rule": "Build two materially different opener+middle proofs if scope allows; choose by product truth, real pixels, usability and unique signature. Never claim a win without rendered comparison.",
        "next": "Inspect the actual project, original assets and real references; implement and evaluate. A deterministic suggestion is NOT a creative verdict.",
        "limits": "No sources retrieved, no asset created, no implementation, no screenshots, no user research."
    }


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
