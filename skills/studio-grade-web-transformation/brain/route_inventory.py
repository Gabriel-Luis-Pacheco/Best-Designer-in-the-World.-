#!/usr/bin/env python3
"""Read-only candidate route inventory. Not a visual, semantic or ownership proof."""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {".git", ".next", ".nuxt", "node_modules", "dist", "build", "coverage", "vendor", ".venv", "venv"}
EXTENSIONS = {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".html", ".htm"}
MAX_FILES = 2500
MAX_SOURCE_BYTES = 128_000
MAX_ROUTES = 160
JOBS = {
    "avatar": {"avatar", "avatars", "character", "personagem", "personagens"},
    "lesson": {"lesson", "lessons", "licao", "licoes", "lição", "lições", "trilha", "learn"},
    "checkout": {"checkout", "payment", "pagamento", "purchase"},
    "profile": {"profile", "perfil", "account", "conta"},
    "onboarding": {"onboarding", "welcome", "boas-vindas"},
}
EMOJI_RE = re.compile("[\\U0001F300-\\U0001FAFF]")
CONTROL_RE = re.compile(r"<(?:button|input|textarea|select)\b", re.I)
VISUAL_RE = re.compile(r"<(?:svg|canvas|img|picture|video|AvatarPreview|Progress|LearningPath|Chart|Map)\b", re.I)


def route_for_file(filename: str) -> tuple[str, str] | None:
    """Infer file-based routes only for recognized conventions; not dynamic router configs."""
    parts = filename.replace("\\\\", "/").split("/")
    if not parts or Path(parts[-1]).suffix.lower() not in EXTENSIONS:
        return None
    top = parts[1:] if parts[0] == "src" else parts
    if not top:
        return None
    family = ""
    segments = []
    name = top[-1]
    stem = Path(name).stem
    if top[0] == "app" and name in {"page.tsx", "page.jsx", "page.ts", "page.js"}:
        if "api" in top[1:-1]:
            return None
        family, segments = "next-app", top[1:-1]
    elif top[0] == "pages" and Path(name).suffix.lower() in {".tsx", ".jsx", ".ts", ".js", ".vue"}:
        if stem.startswith("_") or "api" in top[1:]:
            return None
        family, segments = "file-pages", [*top[1:-1], stem]
    elif top[0] == "routes" and name in {"+page.svelte", "+page.tsx", "+page.jsx"}:
        family, segments = "file-routes", top[1:-1]
    elif top == ["index.html"] or top == ["index.htm"]:
        family, segments = "static-html", []
    else:
        return None
    clean = []
    for segment in segments:
        if segment == "index" or (segment.startswith("(") and segment.endswith(")")):
            continue
        if segment.startswith("[[...") and segment.endswith("]]"):
            clean.append(":optional-catchall")
        elif segment.startswith("[...") and segment.endswith("]"):
            clean.append(":catchall")
        elif segment.startswith("[") and segment.endswith("]"):
            clean.append(":" + segment[1:-1])
        elif segment.startswith("+"):
            continue
        else:
            clean.append(segment)
    return "/" + "/".join(clean), family


def job_hints(route: str) -> list[str]:
    segments = set(re.split(r"[/_.-]+", route.casefold()))
    return [job for job, aliases in JOBS.items() if segments & aliases]


def source_signals(root: Path, file: str) -> dict:
    path = root / file
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_SOURCE_BYTES:
            return {"status": "NOT_READ", "reason": "symlink, missing or too large"}
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return {"status": "NOT_READ", "reason": "unreadable text"}
    return {"status": "SOURCE_ONLY",
            "emoji_codepoints": len(EMOJI_RE.findall(source)),
            "native_control_tags": len(CONTROL_RE.findall(source)),
            "visual_markup_hints": len(VISUAL_RE.findall(source))}


def inspect_routes(root: Path, relative_paths: list[str]) -> dict:
    root = Path(root).resolve(strict=True)
    routes = []
    paths_seen = set()
    for rel in relative_paths:
        if not isinstance(rel, str) or rel in paths_seen or len(rel) > 512:
            continue
        paths_seen.add(rel)
        relative = Path(rel)
        if relative.is_absolute() or ".." in relative.parts or any(part.startswith(".") for part in relative.parts):
            continue
        candidate = route_for_file(relative.as_posix())
        if candidate is None:
            continue
        path = root / relative
        if not path.resolve().is_relative_to(root) or path.is_symlink():
            continue
        route, family = candidate
        routes.append({"file": relative.as_posix(), "route": route, "family": family,
                       "job_hints": job_hints(route),
                       "source_signals": source_signals(root, relative.as_posix())})
        if len(routes) >= MAX_ROUTES:
            break
    collisions = []
    for route, group in _group(routes, lambda r: r["route"]).items():
        if len(group) > 1:
            collisions.append({"route": route, "files": [r["file"] for r in group],
                               "certainty": "POSSIBLE_ROUTING_COLLISION"})
    duplicates = []
    for job in JOBS:
        group = [r for r in routes if job in r["job_hints"]]
        if len(set(r["route"] for r in group)) > 1:
            duplicates.append({"job_hint": job, "routes": [r["route"] for r in group],
                               "files": [r["file"] for r in group],
                               "certainty": "POSSIBLE_PARALLEL_JOB_NOT_PROVEN_DUPLICATE"})
    emoji_review = [r["file"] for r in routes
                    if r["source_signals"].get("emoji_codepoints", 0) >= 3
                    and any(j in r["job_hints"] for j in ("lesson", "avatar"))]
    return {
        "method": "FILE_PATHS_AND_BOUNDED_SOURCE_HINTS_ONLY",
        "status": "CANDIDATES_TO_REVIEW" if collisions or duplicates or emoji_review else "NO_DECLARED_RED_FLAGS",
        "routes": routes,
        "possible_route_collisions": collisions,
        "possible_parallel_jobs": duplicates,
        "emoji_heavy_source_candidates": emoji_review,
        "truncated": len(routes) >= MAX_ROUTES,
        "limits": [
            "Does not discover programmatic routes, modals, tabs or permissions",
            "Similar route names are not proof of duplicated components or state owners",
            "Emoji in source can be legitimate; visual markup in child components is not inspected",
            "Does not inspect the DOM, screenshot, behavior, real data or mobile layout",
        ],
    }


def _group(items, selector):
    grouped = defaultdict(list)
    for item in items:
        grouped[selector(item)].append(item)
    return grouped


def collect_project_paths(root: Path) -> tuple[list[str], bool]:
    files = []
    truncated = False
    for current, directories, names in os.walk(root, followlinks=False):
        directories[:] = sorted(
            d for d in directories if d not in SKIP_DIRS and not d.startswith(".")
            and not (Path(current) / d).is_symlink()
        )
        for name in sorted(names):
            path = Path(current) / name
            if name.startswith(".") or path.is_symlink() or not path.is_file():
                continue
            if len(files) >= MAX_FILES:
                truncated = True
                break
            files.append(path.relative_to(root).as_posix())
        if truncated:
            break
    return files, truncated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        root = args.project.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("Not a directory")
        paths, limit = collect_project_paths(root)
        result = inspect_routes(root, paths)
        result["project_file_list_truncated"] = limit
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        print(output, end="")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"INVALID PROJECT: {exc}\n")


if __name__ == "__main__":
    main()
