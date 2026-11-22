#!/usr/bin/env python3
"""Read-only Design OS component-to-expert router; NEVER invokes external skills.

Provides relevant reference guides and *candidate* specialist IDs by component,
not guarantees that references were read, tools exist or quality was achieved.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "research" / "component_expertise_matrix.json"
REGISTRY = ROOT / "research" / "specialist_registry.json"
MODES = {"PATCH", "REFINE", "AUDIT", "REDESIGN", "REBUILD"}
SURFACES = {"marketing", "product", "internal", "read", "art", "native"}
DEEP_RESEARCH_COMPONENTS = {"hero", "b2b-landing", "b2c-landing", "campaign-landing"}
BROADER_MODES = {"REDESIGN", "REBUILD"}


def _load_json(path: Path, max_bytes: int) -> dict:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > max_bytes:
        raise ValueError("Required local manifest unavailable, symlinked or oversized: " + path.name)
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or obj.get("schema_version") != 1:
        raise ValueError("Unexpected schema version: " + path.name)
    return obj


def _normalize(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", text.casefold())
                   if not unicodedata.combining(ch))


def _phrase_match(haystack: str, needle: str) -> bool:
    norm_h = _normalize(haystack)
    norm_n = _normalize(needle).strip()
    if not norm_h or not norm_n:
        return False
    return bool(re.search(r"(?<!\w)" + re.escape(norm_n) + r"(?!\w)", norm_h))


def load() -> tuple[list[dict], dict[str, dict]]:
    matrix = _load_json(MATRIX, 240_000)
    registry = _load_json(REGISTRY, 220_000)
    profiles = matrix.get("profiles")
    entries = registry.get("entries")
    if not isinstance(profiles, list) or not 1 <= len(profiles) <= 200:
        raise ValueError("Invalid component profiles")
    if not isinstance(entries, list):
        raise ValueError("Invalid specialist registry")
    experts = {}
    for row in entries:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or row["id"] in experts:
            raise ValueError("Invalid specialist entry")
        experts[row["id"]] = row
    seen = set()
    for row in profiles:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError("Malformed component profile")
        ident = row["id"]
        if not re.fullmatch(r"[a-z0-9-]{2,60}", ident) or ident in seen:
            raise ValueError("Invalid or duplicate component id")
        seen.add(ident)
        for field in ("aliases", "surfaces", "specialist_ids", "reference_guides"):
            value = row.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(v, str) and v for v in value):
                raise ValueError("Invalid list " + ident + "." + field)
        if not set(row["surfaces"]).issubset(SURFACES):
            raise ValueError("Unknown surface in " + ident)
        for field in ("user_job", "research_focus", "editorial_or_ux_gate"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError("Missing context " + ident + "." + field)
        missing = [name for name in row["specialist_ids"] if name not in experts]
        if missing:
            raise ValueError("Unknown registry specialists in " + ident + ": " + str(missing))
        for guide in row["reference_guides"]:
            if not re.fullmatch(r"[a-z0-9-]+\.md", guide) or not (ROOT / "references" / guide).is_file():
                raise ValueError("Unresolvable/unsafe guide " + ident + ": " + guide)
    return profiles, experts


def suggest(*, component_ids: list[str] | None = None, task: str = "",
            surface: str = "marketing", mode: str = "REDESIGN",
            profiles: list[dict] | None = None,
            experts: dict[str, dict] | None = None) -> dict:
    if mode not in MODES or surface not in SURFACES:
        raise ValueError("Invalid mode or surface")
    if not isinstance(task, str) or len(task) > 10_000:
        raise ValueError("Task must be at most 10,000 characters")
    if component_ids is not None and (not isinstance(component_ids, list)
        or len(component_ids) > 60 or not all(isinstance(x, str) for x in component_ids)):
        raise ValueError("Components must be a list of up to 60 strings")
    if profiles is None or experts is None:
        profiles, experts = load()
    by_id = {p["id"]: p for p in profiles}
    explicit = list(dict.fromkeys(component_ids or []))
    missing = [p for p in explicit if p not in by_id]
    if missing:
        raise ValueError("Unknown component(s): " + ", ".join(missing))
    matches = []
    for profile in profiles:
        if profile["id"] in explicit:
            matches.append((profile, "EXPLICIT"))
        elif not explicit and surface in profile["surfaces"] and any(
            _phrase_match(task, alias) for alias in profile["aliases"] + [profile["id"]]
        ):
            matches.append((profile, "TASK_ALIAS_MATCH"))
    all_candidate_ids = set()
    all_guides = set()
    result = []
    for profile, reason in matches:
        specialists = []
        for ident in profile["specialist_ids"]:
            item = experts[ident]
            all_candidate_ids.add(ident)
            specialists.append({
                "id": ident, "name": item["name"], "lane": item["lane"],
                "source": item["source"]["url"],
                "status": "CANDIDATE_NOT_INVOKED"
            })
        all_guides.update(profile["reference_guides"])
        deep = mode in BROADER_MODES and profile["id"] in DEEP_RESEARCH_COMPONENTS
        result.append({
            "id": profile["id"], "match": reason,
            "surface_compatible": surface in profile["surfaces"],
            "user_job": profile["user_job"],
            "research_focus": profile["research_focus"],
            "editorial_or_ux_gate": profile["editorial_or_ux_gate"],
            "reference_guides": ["references/" + name for name in profile["reference_guides"]],
            "specialists": specialists,
            "benchmark": {
                "target": "UP_TO_TEN_RELEVANT_REFERENCES_WHEN_FEASIBLE" if deep else
                          "TARGETED_REFERENCES_ONLY_WHEN_NEEDED",
                "mandatory_captures": "REAL_OBSERVATIONS_ONLY",
                "status": "NOT_RESEARCHED_BY_THIS_TOOL",
                "rule": "6 direct/substitute + 2 adjacent + 2 cross-category is a reference mix, "
                        "not 10 direct competitors. Reuse recent authorized research."
            }
        })
    return {
        "status": "CANDIDATE_SELECTION_ONLY_NOT_EXECUTED",
        "design_os_is_owner": True,
        "surface": surface,
        "mode": mode,
        "components": result,
        "distinct_skill_candidates": len(all_candidate_ids),
        "guides_to_consult_when_relevant": ["references/" + n for n in sorted(all_guides)],
        "required_process": [
            "Read true product context, user job, brand and critical flows.",
            "Observe real equivalent competitor sections and capture actual screenshots when available.",
            "Invoke genuinely available complementary specialist skills by lane; read instructions first.",
            "Write from human audience voice, reject generic/slop copy and unproven claims.",
            "Implement and compare rendered desktop/mobile states; test actions and first value.",
            "Report applied vs referenced vs unavailable and what evidence is missing."
        ],
        "notes": [
            "This CLI only reads local curated JSON; it does NOT load/install/invoke skills or browse.",
            "A proposed count of ten is conditional for major redesigns, not proof of ten captures.",
            "Self-review is not a human usability test or independent design approval.",
            "If no profile matched, map the actual job and extend the registry instead of inventing expertise."
        ]
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--component", action="append", default=[], help="Repeat for multiple component IDs")
    p.add_argument("--task", default="", help="Autodetect exact aliases when --component is absent")
    p.add_argument("--surface", choices=sorted(SURFACES), default="marketing")
    p.add_argument("--mode", choices=sorted(MODES), default="REDESIGN")
    p.add_argument("--list", action="store_true", help="List valid component IDs")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        profiles, experts = load()
        if args.list:
            print(json.dumps({"components": [x["id"] for x in profiles]}, ensure_ascii=False, indent=2))
            return
        packet = suggest(component_ids=args.component, task=args.task,
                         surface=args.surface, mode=args.mode, profiles=profiles, experts=experts)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.error(str(exc))
    if args.json:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    else:
        print("Design OS owns the product. Candidates only — none invoked.")
        for item in packet["components"]:
            print(item["id"] + " => " + ", ".join(s["id"] for s in item["specialists"]))
            print("  " + item["benchmark"]["target"])
        if not packet["components"]:
            print("No known component matched; inspect the actual job or pass --component.")
if __name__ == "__main__":
    main()
