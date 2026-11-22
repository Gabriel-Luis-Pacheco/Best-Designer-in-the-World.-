#!/usr/bin/env python3
"""Bring existing 47-component specialist workplans into the primary Brain pipeline.

The bridge selects a small, auditable plan from local manifests. It never invokes
specialists, visits competitors, tests browsers, edits files or certifies quality.
Explicit component names are allowed; task alias inference remains provisional.
"""
from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = {"PATCH", "REFINE", "AUDIT", "REDESIGN", "REBUILD"}
SURFACES = {
    "landing": "marketing", "checkout": "product",
    "internal": "internal", "dashboard": "internal",
    "product": "product", "mobile": "product",
    "experience": "art", "read": "read",
}
MAX_COMPONENTS_AUTO = 6
MAX_COMPONENTS_EXPLICIT = 12


@lru_cache(maxsize=2)
def _module(name: str):
    path = ROOT / "scripts" / (name + ".py")
    spec = importlib.util.spec_from_file_location("bridge_" + name, path)
    if spec is None or spec.loader is None:
        raise ValueError("Missing canonical script " + name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _summary(complete: dict) -> dict:
    """Make stage-specific work usable in a normal agent context budget."""
    return {
        "component_id": complete["component_id"],
        "job": complete["job"],
        "phases": [{
            "id": phase["id"],
            "owner_role": phase["owner_role"],
            "required_output": phase["required_output"],
            "no_go": phase["no_go"],
            "lead_experts": [{
                "id": ex["id"],
                "selection_method": ex["selection_method"],
                "status": ex["status"]
            } for ex in phase["lead_candidates"]],
            "missing_compatible_lanes": phase["missing_compatible_specialist_lanes"],
            "guides": phase["local_guides"],
            "status": phase["status"]
        } for phase in complete["phases"]],
        "benchmark_pattern_transfer": (
            {
                "reference_target": complete["benchmark_pattern_transfer"]["reference_target"],
                "stages_to_observe": complete["benchmark_pattern_transfer"]["stages_to_observe"],
                "status": "NOT_OBSERVED_NOT_VALIDATED",
                "gate": complete["benchmark_pattern_transfer"]["gate"]
            } if complete["benchmark_pattern_transfer"] is not None else None
        ),
        "review_questions": complete["review_questions"],
        "red_flags": complete["red_flags"],
        "status": complete["final_status"]
    }


def compose(context: dict, strategy: dict, explicit_components: list[str] | None = None) -> dict:
    """Return a read-only plan, or an explicit gap instead of guessing a page inventory."""
    if not isinstance(context, dict) or not isinstance(strategy, dict):
        raise ValueError("Context and routed strategy must be objects")
    if explicit_components is None:
        explicit_components = context.get("components", [])
    if not isinstance(explicit_components, list) or len(explicit_components) > MAX_COMPONENTS_EXPLICIT or any(
        not isinstance(x, str) or not 1 <= len(x) <= 80 for x in explicit_components
    ):
        raise ValueError("components must list at most 12 known ids, each <=80 characters")
    explicit_components = list(dict.fromkeys(explicit_components))
    task = context.get("task", "")
    description = context.get("description", "")
    if not isinstance(task, str) or not isinstance(description, str):
        raise ValueError("Invalid task or description")
    task = (task + " " + description).strip()
    if len(task) > 10000:
        task = task[:10000]
    mode = strategy.get("strategy", {}).get("mode")
    if mode not in MODES:
        raise ValueError("Unknown strategy mode")
    raw_surfaces = strategy.get("product", {}).get("surfaces", [])
    if not isinstance(raw_surfaces, list) or not raw_surfaces:
        raise ValueError("Routed surfaces required")
    surfaces = list(dict.fromkeys(SURFACES.get(x) for x in raw_surfaces))
    if any(x is None for x in surfaces):
        raise ValueError("Unrecognized routed surface")
    selector = _module("component_router")
    planner = _module("component_workplan")
    profiles, _ = selector.load()
    by_id = {p["id"]: p for p in profiles}
    unknown = [c for c in explicit_components if c not in by_id]
    if unknown:
        raise ValueError("Unknown explicit components: " + ", ".join(unknown))
    outcomes = []
    assigned = set()
    ambiguous = []
    for surface in surfaces:
        matches = ([
            c for c in explicit_components if surface in by_id[c]["surfaces"]
        ] if explicit_components else [
            item["id"] for item in selector.suggest(
                component_ids=[], task=task, surface=surface, mode=mode,
                profiles=profiles, experts=selector.load()[1])["components"]
        ])
        if not matches:
            continue
        if len(matches) > (MAX_COMPONENTS_EXPLICIT if explicit_components else MAX_COMPONENTS_AUTO):
            ambiguous.append({"surface": surface, "matches": matches,
                              "reason": "Too many components; a real page inventory is needed"})
            continue
        if len(matches) > 12:
            raise ValueError("Component cap exceeded")
        result = planner.plan(component_ids=matches, surface=surface, mode=mode, task=task)
        outcomes.append({"surface": surface,
                         "components": [_summary(item) for item in result["components"]],
                         "status": "WORKPLAN_GENERATED_NOT_EXECUTED"})
        assigned.update(matches)
    uncovered = [c for c in explicit_components if c not in assigned]
    if uncovered:
        raise ValueError("Explicit component/surface mismatch: " + ", ".join(uncovered))
    if ambiguous:
        status = "SCOPE_REVIEW_REQUIRED"
    elif outcomes:
        status = "COMPONENT_PLANNED_NOT_EXECUTED"
    else:
        status = "COMPONENT_INVENTORY_REQUIRED"
    return {
        "status": status,
        "mode": mode,
        "selection": "EXPLICIT_USER_IDS" if explicit_components else "PROVISIONAL_TASK_ALIAS_MATCH",
        "surface_mapping": {old: SURFACES[old] for old in raw_surfaces},
        "workplans": outcomes,
        "unresolved": ambiguous,
        "next_step": (
            "Inventory the actual sections, states and journey; supply explicit component IDs, "
            "not arbitrary guessed components, then inspect sources and implement in-scope changes."
            if status != "COMPONENT_PLANNED_NOT_EXECUTED" else
            "Read relevant source skills and evidence, execute actual work, run real browser tests "
            "and attach delivery/research/pattern evidence packets before claiming results."
        ),
        "evidence": "NO_EXTERNAL_SKILLS_OR_BROWSING_OR_IMPLEMENTATION_EXECUTED"
    }
