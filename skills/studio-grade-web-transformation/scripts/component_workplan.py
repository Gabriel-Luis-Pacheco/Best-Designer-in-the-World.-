#!/usr/bin/env python3
"""Build a component-level Design OS work plan using verified local manifests.

This tool selects staged knowledge and candidate skills. It is read-only and
does NOT browse, capture screenshots, call specialists, implement, test or grade.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "research/component_execution_atlas.json"
SMALL_MODES = {"PATCH", "AUDIT"}
MODES = {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}
SURFACES = {"marketing", "product", "internal", "read", "art", "native"}


def _component_router():
    spec = importlib.util.spec_from_file_location("component_skill_candidates", ROOT / "scripts/component_router.py")
    if spec is None or spec.loader is None:
        raise ValueError("Component router not present")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_atlas() -> tuple[dict, dict[str, dict]]:
    if not ATLAS_PATH.is_file() or ATLAS_PATH.is_symlink() or ATLAS_PATH.stat().st_size > 230_000:
        raise ValueError("Atlas missing, symlinked or too large")
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    if not isinstance(atlas, dict) or atlas.get("schema_version") != 1:
        raise ValueError("Invalid atlas schema")
    phases = atlas.get("phase_definitions")
    recipes = atlas.get("profiles")
    if not isinstance(phases, dict) or not isinstance(recipes, list):
        raise ValueError("Invalid atlas phases/profiles")
    if not 8 <= len(phases) <= 35 or not 20 <= len(recipes) <= 200:
        raise ValueError("Unexpected atlas dimensions")
    cmod = _component_router()
    components, experts = cmod.load()
    expected = {p["id"] for p in components}
    known = set()
    for name, phase in phases.items():
        if not re.fullmatch(r"[a-z-]{2,40}", name):
            raise ValueError("Invalid phase id")
        for field in ("title", "goal", "output", "gate"):
            if not isinstance(phase.get(field), str) or not phase[field].strip():
                raise ValueError("Incomplete phase " + name)
        for field in ("inputs", "guides", "role_lanes"):
            vals = phase.get(field)
            if not isinstance(vals, list) or not all(isinstance(x, str) for x in vals):
                raise ValueError("Invalid " + field + " in " + name)
        for path in phase["guides"]:
            if not re.fullmatch(r"[a-z0-9-]+\.md", path) or not (ROOT / "references" / path).is_file():
                raise ValueError("Missing or invalid reference " + path)
    for r in recipes:
        if not isinstance(r, dict) or not isinstance(r.get("id"), str) or r["id"] in known:
            raise ValueError("Duplicate or malformed component recipe")
        known.add(r["id"])
        items = r.get("execution_phases")
        if not isinstance(items, list) or len(items) != len(set(items)) or "truth" not in items or "render" not in items:
            raise ValueError("Incomplete/duplicate execution phases: " + r["id"])
        if not set(items).issubset(phases):
            raise ValueError("Unknown execution phase: " + r["id"])
        for key in ("review_questions", "red_flags"):
            arr = r.get(key)
            if not isinstance(arr, list) or not 2 <= len(arr) <= 12 or not all(isinstance(x, str) and len(x)>9 for x in arr):
                raise ValueError("Weak or missing component gate: " + r["id"] + "." + key)
        if not isinstance(r.get("observable_user_outcome"), str) or not r["observable_user_outcome"].strip():
            raise ValueError("Missing observable outcome " + r["id"])
    if known != expected:
        raise ValueError("Atlas/component matrix drift: " + repr(sorted(expected ^ known)))
    return atlas, experts


def plan(*, component_ids: list[str], surface: str, mode: str,
         task: str = "", atlas: dict | None = None, experts: dict | None = None) -> dict:
    if mode not in MODES or surface not in SURFACES:
        raise ValueError("Unknown mode or surface")
    if not isinstance(task, str) or len(task) > 10_000:
        raise ValueError("Invalid task")
    if not isinstance(component_ids, list) or len(component_ids) > 12 or not all(isinstance(x, str) for x in component_ids):
        raise ValueError("Pass at most 12 component ids")
    if atlas is None or experts is None:
        atlas, experts = load_atlas()
    mod = _component_router()
    candidates = mod.suggest(component_ids=component_ids, task=task, surface=surface, mode=mode)
    recipes = {r["id"]: r for r in atlas["profiles"]}
    phases = atlas["phase_definitions"]
    out = []
    for item in candidates["components"]:
        profile = recipes[item["id"]]
        by_id = {s["id"]: s for s in item["specialists"]}
        phase_ids = list(profile["execution_phases"])
        if mode == "PATCH":
            phase_ids = [p for p in phase_ids if p in ("truth", "ux", "data", "engineering", "accessibility", "render")]
        elif mode == "AUDIT":
            phase_ids = [p for p in phase_ids if p not in ("engineering", "measurement")]
        elif mode == "REFINE":
            # Existing approved decisions should be reused; new market exploration
            # requires an observed gap, not a forced ten-site browsing marathon.
            phase_ids = [p for p in phase_ids if p != "measurement"]
        steps = []
        for phase_id in phase_ids:
            phase = phases[phase_id]
            seen_lanes: set[str] = set()
            recommended, alternates = [], []
            for lane in phase["role_lanes"]:
                for sid in profile_skill_ids(item):
                    if sid not in by_id:
                        continue
                    exp = experts[sid]
                    if exp["lane"] != lane:
                        continue
                    candidate = {
                        "id": sid, "name": exp["name"],
                        "lane": lane, "source": exp["source"]["url"],
                        "skill_file": exp["source"].get("path"),
                        "status": "CANDIDATE_UNVERIFIED_NOT_INVOKED"
                    }
                    if lane not in seen_lanes:
                        recommended.append(candidate)
                        seen_lanes.add(lane)
                    else:
                        alternates.append(candidate)
            steps.append({
                "id": phase_id, "owner_role": phase["title"],
                "goal": phase["goal"], "inputs": phase["inputs"],
                "required_output": phase["output"],
                "no_go": phase["gate"],
                "local_guides": ["references/" + x for x in phase["guides"]],
                "lead_candidates": recommended,
                "alternative_candidates": alternates,
                "status": "NOT_STARTED",
                "dependency": "Inspect previous outputs and actual artifacts, not agents' self-scores.",
                "skip_policy": "Only with a documented reason, not a silent PASS."
            })
        out.append({
            "component_id": item["id"], "job": item["user_job"],
            "surface_compatible": item["surface_compatible"],
            "phases": steps,
            "review_questions": profile["review_questions"],
            "red_flags": profile["red_flags"],
            "observable_user_outcome": profile["observable_user_outcome"],
            "benchmark": item["benchmark"],
            "research_comparison_job": profile["comparison_job"],
            "final_status": "NOT_EXECUTED_NEEDS_REAL_ARTIFACTS"
        })
    return {
        "schema_version": 1, "status": "PLANNED_NOT_EXECUTED",
        "mode": mode, "surface": surface, "components": out,
        "instructions": [
            "Actually inspect and use authorized available skills; source links alone prove nothing.",
            "For major commercial redesign, research up to 10 genuine alternatives plus excellent adjacent examples when available; inspect relevant sections, capture evidence, learn mechanisms not protected expression.",
            "Apply each stage to the same product/job; keep a short recorded handoff and resolve conflicting opinions with truth, brand, usability and real evidence.",
            "Produce working pixels and states, then critique and repair. A build/screenshot or model praise is not design approval.",
            "Use the component delivery evidence gate before shipping; distinguish human review, self-review and untested business outcomes."
        ]
    }


def profile_skill_ids(item: dict) -> list[str]:
    return [s["id"] for s in item["specialists"]]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--component", action="append", default=[])
    p.add_argument("--task", default="")
    p.add_argument("--surface", choices=sorted(SURFACES), default="marketing")
    p.add_argument("--mode", choices=sorted(MODES), default="REDESIGN")
    p.add_argument("--list-phases", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        atlas, experts = load_atlas()
        if args.list_phases:
            print(json.dumps({"phases": list(atlas["phase_definitions"])}, indent=2))
            return
        packet = plan(component_ids=args.component, task=args.task,
                      surface=args.surface, mode=args.mode, atlas=atlas, experts=experts)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        p.error(str(exc))
    if args.json:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    else:
        print("Design OS stage plan only. No external skill executed, source inspected or design approved.")
        for item in packet["components"]:
            print(item["component_id"], "→", " / ".join(x["id"] for x in item["phases"]))
            for phase in item["phases"]:
                print(" -", phase["id"], ":", ", ".join(x["id"] for x in phase["lead_candidates"]))
if __name__ == "__main__":
    main()
