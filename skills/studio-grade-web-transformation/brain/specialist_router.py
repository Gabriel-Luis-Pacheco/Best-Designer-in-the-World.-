#!/usr/bin/env python3
"""Compatibility adapter for the canonical, tested scripts/specialist_router.py.

Legacy callers may keep sending a JSON context. This adapter no longer uses a
second, stale catalog or silently imposes a 3-expert ceiling. It suggests
specialists only; it never loads, installs, invokes or authorizes a skill.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "scripts/specialist_router.py"
SURFACE_ALIASES = {
    "landing":"marketing","marketing":"marketing","commerce":"marketing",
    "checkout":"marketing","experience":"art","art":"art",
    "app":"product","product":"product","dashboard":"internal",
    "internal":"internal","docs":"read","reading":"read","read":"read",
    "native":"native",
}
MODE_TO_OPERATION = {
    "PATCH":"polish","AUDIT":"audit","REFINE":"polish",
    "REDESIGN":"build","REBUILD":"build"
}

def _load_router():
    spec = importlib.util.spec_from_file_location("design_os_canonical_specialists", MOD_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("Canonical specialist router unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def suggest(context: dict, catalog=None) -> dict:
    if not isinstance(context, dict):
        raise ValueError("Context must be a JSON object")
    if catalog is not None:
        raise ValueError("Legacy specialist catalog override retired; use canonical registry")
    fragments=[]
    for key in ("task","goal","description","stack"):
        value=context.get(key,"")
        if not isinstance(value,str) or len(value)>10_000:
            raise ValueError("Invalid text field "+key)
        fragments.append(value)
    task=" ".join(x for x in fragments if x)
    surface=SURFACE_ALIASES.get(str(context.get("surface","product")).lower())
    if surface is None:
        raise ValueError("Unknown surface")
    if not task.strip():
        raise ValueError("Provide task, goal, description or stack")
    mode=str(context.get("mode","REBUILD")).upper()
    if mode not in MODE_TO_OPERATION:
        raise ValueError("Invalid mode")
    requested_limit=context.get("max_specialists")
    if requested_limit is not None and (not isinstance(requested_limit,int)
        or isinstance(requested_limit,bool) or not 0 <= requested_limit <= 32):
        raise ValueError("max_specialists must be an integer 0..32 when supplied")
    operation=MODE_TO_OPERATION[mode]
    router=_load_router()
    project=context.get("project")
    if project is not None and not isinstance(project,str):
        raise ValueError("project must be a path string")
    allow=bool(context.get("owner_authorized",False))
    if context.get("owner_authorized") not in (None,True,False):
        raise ValueError("owner_authorized must be boolean")
    if mode=="PATCH" and not any(router.contains_phrase(task,x) for x in (
        "impeccable","gsap","three.js","webgl","performance","accessibility","a11y","figma")):
        return {"status":"NO_EXTERNAL_SKILL_NEEDED","specialists":[],
                "source_of_truth":"scripts/specialist_router.py",
                "reason":"Narrow patch without an explicitly relevant specialist."}
    packet=router.recommend(
        surface,operation,task,
        project=Path(project) if project else None,
        product=str(context.get("product","")),
        allow_project_ceo=allow,
        include_all_matches=bool(context.get("all_matches",False))
    )
    choices=packet["candidates"]
    if requested_limit is not None:
        choices=choices[:requested_limit]
    registry={item["id"]:item for item in router.read_registry()}
    specialists=[]
    for entry in choices:
        source=registry[entry["id"]]["source"]
        specialists.append({
            "id":entry["id"],"url":entry["source"],
            "skill_path":source["path"],"relevance":entry["niche_advantage_not_proven_superiority"],
            "matched_terms":entry["matched_signals"],
            "status":"CANDIDATE_NOT_INSTALLED_NOT_INVOKED",
            "availability":entry["availability"],
            "requires":entry["requires"]
        })
    return {
        "status":"PROPOSED_ONLY_NOT_EXECUTED",
        "source_of_truth":"scripts/specialist_router.py",
        "specialists":specialists,
        "prerequisites":packet["prerequisites"],
        "limits":"Legacy context adapter; candidate relevance only, not an actual agent call, expert verdict or permissions."
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context",type=Path)
    args=parser.parse_args()
    try:
        payload=json.loads(args.context.read_text(encoding="utf-8"))
        print(json.dumps(suggest(payload),ensure_ascii=False,indent=2))
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as exc:
        parser.exit(2,f"INVALID ROUTE: {exc}\n")
if __name__=="__main__":
    main()
