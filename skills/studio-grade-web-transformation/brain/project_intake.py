#!/usr/bin/env python3
"""Bounded, read-only project inventory for a design agent.

This reports file-level evidence, not observed UI, working links, UX quality,
security certification, user behavior or product strategy.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path

HIDDEN={"node_modules",".git",".next",".nuxt","dist","build","coverage","vendor",".venv","venv"}
SKIP_SUFFIXES={".env",".pem",".key",".p12",".pfx",".crt",".sqlite",".db"}
CODE_SUFFIXES={".js",".jsx",".ts",".tsx",".vue",".svelte",".html",".htm"}
ASSET_SUFFIXES={".svg",".png",".jpg",".jpeg",".webp",".gif",".ico"}
MAX_FILES=2500
MAX_ITEMS=32

def visible(path: Path) -> bool:
    return not any(p.startswith(".") or p in HIDDEN for p in path.parts)

def inspect_project(root: str | Path) -> dict:
    root=Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project root must be directory")
    paths=[]
    truncated=False
    for current,dirs,names in os.walk(root,followlinks=False):
        current=Path(current)
        dirs[:]=sorted(d for d in dirs if d not in HIDDEN and not d.startswith(".")
                       and not (current/d).is_symlink())
        for name in sorted(names):
            path=current/name
            relative=path.relative_to(root)
            if not visible(relative) or path.is_symlink() or not path.is_file():
                continue
            if path.suffix.lower() in SKIP_SUFFIXES or name.lower().startswith(("secret","credential")):
                continue
            if len(paths)>=MAX_FILES:
                truncated=True
                break
            paths.append(relative.as_posix())
        if truncated:
            break
    # Evidence-based route candidates are derived from recognized file-router conventions.
    # This does not inspect route ownership, dynamic router tables or the browser.
    route_spec=importlib.util.spec_from_file_location("design_os_route_inventory",Path(__file__).with_name("route_inventory.py"))
    if route_spec is None or route_spec.loader is None:
        raise ValueError("route inventory unavailable")
    route_module=importlib.util.module_from_spec(route_spec)
    route_spec.loader.exec_module(route_module)
    route_evidence=route_module.inspect_routes(root,paths)
    routes=[r["file"] for r in route_evidence["routes"]]
    style=[]
    assets=[]
    tests=[]
    for rel in paths:
        p=Path(rel)
        n=p.name.lower()
        if p.suffix.lower() in {".css",".scss",".sass",".less"} or n in {"design.md","tokens.json","tailwind.config.js","tailwind.config.ts"}:
            style.append(rel)
        if p.suffix.lower() in ASSET_SUFFIXES:
            assets.append(rel)
        if "test" in n or "spec" in n:
            tests.append(rel)
    hints=[]
    scripts=[]
    pkg=root/"package.json"
    if pkg.is_file() and not pkg.is_symlink() and pkg.stat().st_size<=128_000:
        try:
            data=json.loads(pkg.read_text(encoding="utf-8"))
            if isinstance(data,dict):
                dep={**(data.get("dependencies") if isinstance(data.get("dependencies"),dict) else {}),
                     **(data.get("devDependencies") if isinstance(data.get("devDependencies"),dict) else {})}
                known={"next":"Next.js","react":"React","vue":"Vue","@angular/core":"Angular",
                       "svelte":"Svelte","vite":"Vite","expo":"Expo","react-native":"React Native",
                       "@playwright/test":"Playwright","vitest":"Vitest"}
                hints=[display for depname,display in known.items() if depname in dep]
                if isinstance(data.get("scripts"),dict):
                    scripts=sorted(str(k) for k in data["scripts"])[:MAX_ITEMS]
        except (ValueError,UnicodeError,OSError):
            pass
    return {
        "evidence_level":"FILE_INVENTORY_ONLY",
        "status":"PARTIAL" if truncated else "FILE_INVENTORY_COMPLETE_WITH_EXCLUSIONS",
        "file_count_sampled":len(paths),
        "framework_hints":hints,
        "route_file_candidates":routes[:MAX_ITEMS],
        "route_evidence":route_evidence,
        "style_token_candidates":style[:MAX_ITEMS],
        "brand_asset_candidates":assets[:MAX_ITEMS],
        "test_file_candidates":tests[:MAX_ITEMS],
        "package_script_names":scripts,
        "limits":["No rendered UI inspection","No user metrics or flow verification",
                  "No contents or secrets exported","Hidden and generated directories skipped",
                  "File list is capped; labels are hypotheses, not proof of behavior",
                  "Route and repeated-job candidates are based on filenames, not flow ownership"]
    }

def build_plan(context: dict, root: str | Path) -> dict:
    here=Path(__file__).resolve().parent
    spec=importlib.util.spec_from_file_location("design_os_route",here/"route.py")
    if spec is None or spec.loader is None:
        raise ValueError("router unavailable")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    plan=module.route(context)
    inventory=inspect_project(root)
    plan["project_inventory"]=inventory
    plan["recommended_inspection"]=[
        "Read product content and design system from candidate files before choosing a direction",
        "Trace critical actions, original values, routes and data contracts before changes",
        "Run project-specific browser, accessibility and regression tests when available",
    ]
    return plan

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project",required=True,help="Local project directory; never executes it")
    p.add_argument("--context",help="Optional strategy JSON; provides a routed plan")
    args=p.parse_args()
    try:
        result=(build_plan(json.loads(Path(args.context).read_text(encoding="utf-8")),args.project)
                if args.context else inspect_project(args.project))
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        p.exit(2,f"INVALID PROJECT: {exc}\n")
