#!/usr/bin/env python3
"""Suggest complementary external skills to the Design OS based on the actual task.

This is an OPTIONAL registry and *read-only local skill-file detector*, not an
agent orchestrator, skill installer, command executor, skill loader, web search
client, user approver, visual judge or proof of local tool capability.

Actual agent: use its native skill listing and invocation mechanisms first.
"""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/specialist_registry.json"
OPERATIONS = {
    "shape","build","critique","audit","polish","distill","bolder","quieter",
    "clarify","typeset","layout","color","animate","delight","overdrive",
    "adapt","harden","onboard","optimize","document","extract","variants"
}
SURFACES = {"marketing","product","internal","read","art","native"}
INSTALL_PATHS = (
    ".agent/skills", ".agents/skills", ".claude/skills", ".cursor/skills",
    ".opencode/skills", ".codex/skills", "skills"
)
GENERAL_SIGNALS = {
    "site","landing","marketing","visual","design","build","conversao",
    "conversão","produto","site novo","copy","user","interface","hero",
    "sales","vender","page","growth","projeto","new","experiencia","usuário",
    "usuários","site design","mobile","ux"
}
DEFAULT_LANES = {
    ("marketing","build"): ("art-direction","conversion","marketing-copy"),
    ("marketing","critique"): ("visual-refinement","conversion"),
    ("marketing","audit"): ("interface-audit","conversion"),
    ("product","build"): ("pattern-research","accessibility"),
    ("product","onboard"): ("growth-onboarding","accessibility"),
    ("internal","audit"): ("interface-audit",),
    ("read","audit"): ("interface-audit",),
    ("art","build"): ("art-direction",),
    ("native","build"): ("accessibility",)
}
TARGET_SCOPE_HINTS = {
    "batatalk", "bata talk", "bata-talk"
}

def normalize(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))

def contains_phrase(text: str, phrase: str) -> bool:
    needle = normalize(phrase).strip()
    if not needle or not text:
        return False
    return bool(re.search(r"(?<![\w])" + re.escape(needle) + r"(?![\w])",text))

def read_registry(path: Path=REGISTRY) -> list[dict]:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 220_000:
        raise ValueError("Registry unavailable, symlinked or exceeds 220KB")
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version")!=1:
        raise ValueError("Registry must be a version-1 object")
    rows=data.get("entries")
    if not isinstance(rows,list):
        raise ValueError("Registry entries must be an array")
    ids=set()
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get("id"),str):
            raise ValueError("Malformed registry entry")
        if row["id"] in ids:
            raise ValueError("Duplicate registry id")
        ids.add(row["id"])
        for attr in ("surfaces","operations","signals","skill_names"):
            if not isinstance(row.get(attr),list) or not all(isinstance(x,str) for x in row[attr]):
                raise ValueError(f"Invalid {attr}: {row['id']}")
        if not isinstance(row.get("lane"),str) or not isinstance(row.get("source"),dict):
            raise ValueError("Missing lane/source")
        if not row["source"].get("url","").startswith("https://github.com/"):
            raise ValueError("Invalid upstream URL")
    return rows

def detect_local(project: Path | None, candidate_names: set[str]) -> dict[str,list[str]]:
    """Read only narrowly-scoped local SKILL.md name keys, never instructions or code."""
    if project is None:
        return {}
    root=project.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("--project must be a directory")
    found: dict[str,list[str]] = {}
    for subdir in INSTALL_PATHS:
        base=root / subdir
        if not base.is_dir() or base.is_symlink() or not base.resolve().is_relative_to(root):
            continue
        # Do not crawl arbitrary descendants or follow symlinks.
        for skill_dir in list(base.iterdir())[:400]:
            if not skill_dir.is_dir() or skill_dir.is_symlink() or not skill_dir.resolve().is_relative_to(root):
                continue
            fp=skill_dir / "SKILL.md"
            if not fp.is_file() or fp.is_symlink() or not fp.resolve().is_relative_to(root):
                continue
            if fp.stat().st_size > 100_000:
                continue
            # The first 20 lines are frontmatter metadata, never an instruction to execute.
            lines=fp.read_text(encoding="utf-8",errors="replace").splitlines()[:20]
            if not lines or lines[0].strip()!="---":
                continue
            name=""
            for line in lines[1:]:
                if line.strip()=="---":
                    break
                match=re.match(r'^name:\s*["\']?([^"\'#\n]+?)["\']?\s*$',line)
                if match:
                    name=match.group(1).strip()
                    break
            if name in candidate_names:
                found.setdefault(name,[]).append(str(fp.relative_to(root)))
    return found

def recommend(surface: str, operation: str, task: str="", project: Path | None=None,
              product: str="", include_all_matches: bool=False, registry: list[dict] | None=None) -> dict:
    if surface not in SURFACES:
        raise ValueError("Invalid surface")
    if operation not in OPERATIONS:
        raise ValueError("Invalid operation")
    if not isinstance(task,str) or len(task)>10_000 or not isinstance(product,str) or len(product)>100:
        raise ValueError("Task/product text invalid or exceeds safe size")
    rows=registry if registry is not None else read_registry()
    query=normalize(task)
    product_query=normalize(product)
    is_batatalk=any(contains_phrase(query,t) or contains_phrase(product_query,t) for t in TARGET_SCOPE_HINTS)
    all_names={n for row in rows for n in row["skill_names"]}
    local=detect_local(project,all_names)
    choices=[]
    defaults=DEFAULT_LANES.get((surface,operation),())
    for row in rows:
        if surface not in row["surfaces"]:
            continue
        # If exact project owner-specific skill would be out of scope, never suggest it.
        if row.get("scope_guard")=="BATATALK_AUTHORIZED_ONLY" and not is_batatalk:
            continue
        if row.get("lane")=="figma-prerequisite":
            continue  # Included only as a dependency where Figma specialist is selected.
        matched=[x for x in row["signals"] if contains_phrase(query,x)]
        specific=[x for x in matched if normalize(x) not in {normalize(g) for g in GENERAL_SIGNALS}]
        explicitly_named=any(contains_phrase(query,n) for n in row["skill_names"]+[row["name"],row["id"]])
        # For most specialists, a general request is not enough. Controlled defaults allow
        # relevant fallback directions for broadly stated new work.
        eligible=bool(specific or explicitly_named or (row["lane"] in defaults and operation in row["operations"]))
        if not eligible:
            continue
        if operation not in row["operations"] and not explicitly_named and not specific:
            continue
        score=(5 if operation in row["operations"] else 0) + len(specific)*4 + len(matched) + (10 if explicitly_named else 0)
        if row["lane"] in defaults and operation in row["operations"]:
            score+=2
        installed_names={n:local[n] for n in row["skill_names"] if n in local}
        choices.append({
            "id":row["id"],"name":row["name"],"lane":row["lane"],"score":score,
            "matched_signals":matched[:8],"specific_match":bool(specific or explicitly_named),
            "niche_advantage_not_proven_superiority":row["edge"],
            "source":row["source"]["url"],"skill_names":row["skill_names"],
            "availability":"LOCAL_SKILL_FILE_DETECTED_NOT_LOADED" if installed_names else "NOT_DETECTED_CHECK_HOST_SKILL_TOOLS",
            "local_files":installed_names,"requires":row.get("requires",[]),
            "scope_guard":row.get("scope_guard")
        })
    choices.sort(key=lambda x:(-x["score"],x["id"]))
    # Limit repetitive experts in the same niche lane, not the total count of agents.
    # The user can request all matching candidates for comparison.
    if not include_all_matches:
        seen_lanes=set()
        distinct=[]
        for row in choices:
            if row["lane"] in seen_lanes:
                continue
            distinct.append(row)
            seen_lanes.add(row["lane"])
        choices=distinct
    wanted=set(dep for row in choices for dep in row["requires"])
    dependencies=[]
    for dep in sorted(wanted):
        hit=next((r for r in rows if r["id"]==dep),None)
        if hit:
            dependencies.append({"id":dep,"name":hit["name"],"skill_names":hit["skill_names"],
                                 "source":hit["source"]["url"],
                                 "availability":"LOCAL_SKILL_FILE_DETECTED_NOT_LOADED" if any(n in local for n in hit["skill_names"]) else "NOT_DETECTED_CHECK_HOST_SKILL_TOOLS",
                                 "reason":"Mandatory tool-specific prerequisite; load before using dependent specialist"})
    internal=["references/automatic-specialist-orchestration.md"]
    if surface=="marketing" and any(contains_phrase(query,s) for s in ("vendas","growth","marketing","funil","funnel","crm","cmo","seo","geo","landing","oferta")):
        internal.append("references/full-funnel-commercial-orchestration.md")
    if any(contains_phrase(query,s) for s in ("great leads","lead","headline","copy","copywriting","hero","lide","abertura","primeira dobra")):
        internal.append("references/great-leads-ethical-copy-framework.md")
    if any(contains_phrase(query,s) for s in ("psicologia","psicólogo","psychology","vieses","comportamento","persuasao")):
        internal.append("references/ethical-user-psychology.md")
    if "ceo" in query or "coo" in query or "cmo" in query or "operacao" in query:
        internal.append("references/full-funnel-commercial-orchestration.md")
    internal=list(dict.fromkeys(internal))
    return {
        "status":"CANDIDATE_SELECTION_ONLY_NOT_EXECUTED",
        "design_os_is_primary":True,"surface":surface,"operation":operation,"product":product or None,
        "candidates":choices,"prerequisites":dependencies,"internal_guides":internal,
        "number_of_distinct_lanes":len(choices),
        "next_actions":[
            "Inspect actual product/brief and authoritative current asset/source context.",
            "Use the agent's native skill listing first; local scan sees only project files.",
            "Read and invoke genuinely available specialists, satisfying prerequisites and user permissions.",
            "Integrate advice under Design OS, implement, render, test and verify independently where possible.",
            "If unavailable, use Design OS internal references without claiming external skill execution."
        ],
        "limitations":[
            "External source listed does not establish a local installation or supported tool integration.",
            "Local skill-file presence does not establish agent read, skill invocation, genuine expertise or compatibility.",
            "No downloads, installations, agents, shells, prompts executed, scoring of design quality, browser or external API calls.",
            "Candidate score is for routing relevance only, not skill superiority or final product quality."
        ]
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface",required=True,choices=sorted(SURFACES))
    parser.add_argument("--operation",required=True,choices=sorted(OPERATIONS))
    parser.add_argument("--task",default="")
    parser.add_argument("--project",type=Path)
    parser.add_argument("--product",default="")
    parser.add_argument("--all-matches",action="store_true")
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    try:
        packet=recommend(args.surface,args.operation,args.task,args.project,args.product,args.all_matches)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(packet,indent=2,ensure_ascii=False))
    else:
        print("Design OS is responsible for the result. Specialized candidates, not invoked:")
        for c in packet["candidates"]:
            print(f" - {c['name']} [{c['lane']}] ({c['availability']}) — {c['source']}")
        if packet["prerequisites"]:
            print("Prerequisites:",", ".join(x["name"] for x in packet["prerequisites"]))
        print("Internal:",", ".join(packet["internal_guides"]))
if __name__=="__main__":
    main()
