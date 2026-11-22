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



def _vendored_reference_index() -> tuple[dict, dict]:
    """Manifest-backed READ-ONLY snapshot paths; no actual skill invocation.

    CORE distribution has no vendor content, so missing manifest is a legitimate
    NOT_AVAILABLE outcome rather than permission to install or claim execution.
    """
    overlay_path = ROOT / "research/vendor_phase_overlay.json"
    if not overlay_path.is_file() or overlay_path.is_symlink() or overlay_path.stat().st_size > 80_000:
        raise ValueError("Vendor phase overlay invalid")
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    if overlay.get("schema_version") != 1:
        raise ValueError("Invalid vendor overlay schema")
    for field in ("phase_packs", "component_priorities"):
        if not isinstance(overlay.get(field), dict):
            raise ValueError("Invalid vendor overlay " + field)
    index_path = ROOT / "vendor/external-skill-packs/INDEX.json"
    if not index_path.is_file() or index_path.is_symlink():
        return overlay, {}
    if index_path.stat().st_size > 150_000:
        raise ValueError("Vendored index unexpectedly large")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    rows = index.get("skills", [])
    if index.get("schema_version") != 1 or not isinstance(rows, list):
        raise ValueError("Invalid vendored index")
    records = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise ValueError("Malformed vendored skill entry")
        name = row["path"].split("/")[-1]
        relative = row.get("local_path")
        if name in records or not isinstance(relative, str):
            raise ValueError("Duplicate vendor skill basename or invalid path")
        local = Path(relative)
        if local.is_absolute() or ".." in local.parts or not relative:
            raise ValueError("Unsafe vendored skill path")
        skill_file = (ROOT / "vendor/external-skill-packs" / local / "SKILL.md")
        exists = skill_file.is_file() and not skill_file.is_symlink() and skill_file.resolve().is_relative_to(ROOT.resolve())
        records[name] = {
            "name": name, "upstream_repository": row.get("repo"),
            "revision": row.get("revision"), "license_reported": row.get("license"),
            "snapshot_file": "vendor/external-skill-packs/" + relative + "/SKILL.md",
            "snapshot_present": bool(exists)
        }
    referenced = {x for v in overlay["phase_packs"].values() for x in v}
    referenced |= {x for v in overlay["component_priorities"].values() for x in v}
    if records and not referenced.issubset(records):
        raise ValueError("Vendor phase overlay contains nonexistent skill IDs")
    return overlay, records


def _vendor_phase_candidates(component_id: str, phase_id: str,
                             overlay: dict, records: dict) -> dict:
    ids = overlay["phase_packs"].get(phase_id, [])
    if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
        raise ValueError("Vendor phase packs must be arrays")
    preferred = overlay["component_priorities"].get(component_id, [])
    if not isinstance(preferred, list):
        raise ValueError("Vendor priorities must be arrays")
    chosen = list(dict.fromkeys(ids))
    chosen.sort(key=lambda x: (0 if x in preferred else 1,
                               preferred.index(x) if x in preferred else ids.index(x)))
    candidates = []
    for name in chosen:
        record = records.get(name)
        if record is None:
            # In CORE the entire vendor directory is absent; never pretend the
            # source was read or a CLI was installed.
            continue
        candidates.append({**record, "status":
            "VENDORED_SNAPSHOT_AVAILABLE_NOT_LOADED" if record["snapshot_present"]
            else "VENDORED_SNAPSHOT_MISSING_NOT_LOADED"})
    return {
        "status": "CANDIDATES_ONLY_NOT_USED" if records else "NO_VENDOR_PACKS_IN_THIS_INSTALL",
        "priority_snapshots": candidates[:3],
        "additional_snapshots_if_relevant": candidates[3:],
        "warning": "Snapshot != installed skill, plugin, CLI, subagent or tested output"
    }


# These lanes are deliberately context-dependent. An art/motion piece does not
# need SaaS sales persuasion just because the atlas includes a "proof" phase,
# and internal UX writing does not need a commercial copywriting pitch.
def _applicable_lanes(phase_id: str, default_lanes: list[str],
                      component_id: str, surface: str, task: str) -> list[str]:
    if surface == "art" and phase_id == "proof":
        return ["art-direction", "visual-refinement", "browser-qa"]
    if surface == "art" and phase_id == "ux":
        return ["visual-refinement", "browser-qa", "art-direction"]
    if surface in {"product", "internal", "native", "art"} and phase_id == "editorial":
        return ["pattern-research", "interface-audit", "accessibility", "visual-refinement"]
    if phase_id == "engineering":
        if surface == "art" and component_id == "brand-identity":
            return ["art-direction", "visual-refinement"]
        lanes = ["react-architecture", "react-performance", "web-performance"]
        text = task.casefold()
        if component_id == "motion" or any(word in text for word in ("gsap", "animate", "motion graphics", "animation", "animacao", "animação")):
            lanes.append("motion-implementation")
        if component_id == "3d-interactive" or any(word in text for word in ("webgl", "three.js", "react three fiber", "r3f")):
            lanes.append("r3f-implementation")
        if surface == "art":
            return [x for x in lanes if x in {"motion-implementation", "r3f-implementation"}]
        return lanes
    return default_lanes


def _phase_specialists(item: dict, phase_id: str, phase: dict,
                       experts: dict[str, dict], surface: str,
                       task: str) -> tuple[list[dict], list[dict], list[str]]:
    """Pick the right expert per role: local first, surface-compatible registry fallback.

    Never claim tool invocation. This closes coverage gaps without blindly
    assigning 50 experts or leaking B2C persuasion into sensitive internal UI.
    """
    leads: list[dict] = []
    alternatives: list[dict] = []
    gaps: list[str] = []
    local_ids = profile_skill_ids(item)
    active_lanes = _applicable_lanes(phase_id, phase["role_lanes"], item["id"], surface, task)
    for lane in active_lanes:
        local = [experts[sid] for sid in local_ids
                 if sid in experts and experts[sid]["lane"] == lane
                 and surface in experts[sid]["surfaces"]]
        global_fallback = [exp for exp in experts.values()
                           if exp["lane"] == lane and surface in exp["surfaces"]
                           and exp["id"] not in local_ids]
        pool = [(x, "COMPONENT_PROFILE") for x in local] + [
            (x, "SURFACE_COMPATIBLE_REGISTRY_FALLBACK") for x in global_fallback]
        if not pool:
            gaps.append(lane)
            continue
        for i, (exp, method) in enumerate(pool):
            candidate = {
                "id": exp["id"], "name": exp["name"],
                "lane": lane, "source": exp["source"]["url"],
                "skill_file": exp["source"].get("path"),
                "selection_method": method,
                "status": "CANDIDATE_UNVERIFIED_NOT_INVOKED"
            }
            # A phase can have several complementary lanes; restrict automatic
            # "lead" suggestions to avoid 5 heavyweight skills for routine CSS.
            if i == 0 and len(leads) < 3:
                leads.append(candidate)
            else:
                alternatives.append(candidate)
    return leads, alternatives, gaps


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
    vendor_overlay, vendor_records = _vendored_reference_index()
    out = []
    for item in candidates["components"]:
        if not item["surface_compatible"]:
            raise ValueError("Component " + item["id"] + " is not valid for surface " + surface)
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
            recommended, alternates, missing_lanes = _phase_specialists(
                item, phase_id, phase, experts, surface, task)
            steps.append({
                "id": phase_id, "owner_role": phase["title"],
                "goal": phase["goal"], "inputs": phase["inputs"],
                "required_output": phase["output"],
                "no_go": phase["gate"],
                "local_guides": ["references/" + x for x in phase["guides"]],
                "lead_candidates": recommended,
                "alternative_candidates": alternates,
                "missing_compatible_specialist_lanes": missing_lanes,
                "selection_policy": "Component-matched experts first, then surface-compatible global registry by role. At most three lead suggestions per phase; others are opt-in.",
                "vendored_specialized_references": _vendor_phase_candidates(
                    item["id"], phase_id, vendor_overlay, vendor_records),
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
