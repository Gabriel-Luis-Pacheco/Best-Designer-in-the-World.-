#!/usr/bin/env python3
"""Safely initialize/inspect a project's explicit product and visual design context.

No inference from code or designs, no identity replacement, no implicit writes,
no claim of context freshness or approval. Created files are editable templates.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

PRODUCT = """# PRODUCT.md — observed product facts (owner review required)

Status: DRAFT / UNVERIFIED

## Audience and primary jobs
- UNKNOWN — add real personas, tasks and context of use.

## Actual product behavior
- UNKNOWN — cite implemented route/feature, not an aspiration.

## Protected contracts
- UNKNOWN — pricing, auth, data, permissions, paths, payments, legal requirements.

## Success and measurement
- UNKNOWN — define actual behavior and validated metrics.

## Owner approvals and evidence
- UNKNOWN — date, source, approver, stable links.
"""
DESIGN = """# DESIGN.md — current visual canon (owner review required)

Status: DRAFT / UNVERIFIED

## Approved identity and canonical assets
- UNKNOWN — logo/mascot identity, approved image source, licensing and provenance.

## Verified interface tokens
- UNKNOWN — typography, semantic colors, spacing, radii and interaction states.

## Spatial/material/behavioral signature
- UNKNOWN — what makes this exact product recognizable and why.

## Protected patterns
- UNKNOWN — approved direction, variants, original references and exceptions.

## Accessibility and responsive behavior
- UNKNOWN — measured contrast, focus, mobile composition, touch, reduced motion.

## Proposed changes (NOT approved canon)
- UNKNOWN — separate suggestions from existing implementation.

## Owner approvals and evidence
- UNKNOWN — date, source, approver and representative rendered screens.
"""
NAME_MAP = {"PRODUCT.md": PRODUCT, "DESIGN.md": DESIGN}
def _file(root: Path, name: str) -> Path:
    if not root.is_dir():
        raise ValueError("Project directory does not exist")
    path = root / name
    if path.is_symlink():
        raise ValueError("Refusing symlink: " + name)
    return path

def status(root: Path) -> dict:
    documents={}
    for name in NAME_MAP:
        path=_file(root,name)
        if not path.is_file():
            documents[name]={"status":"MISSING","unknown_count":None}
        else:
            data=path.read_text(encoding="utf-8")
            documents[name]={"status":"EMPTY" if not data.strip() else "PRESENT_UNVERIFIED",
                             "unknown_count":len(re.findall(r"\bUNKNOWN\b",data))}
    return {"status":"CONTEXT_INVENTORY_ONLY","documents":documents,
            "limitations":"Cannot verify project facts, author approval, actual branding or whether context is stale."}

def init(root: Path) -> dict:
    created=[]
    preserved=[]
    for name,content in NAME_MAP.items():
        path=_file(root,name)
        try:
            # Exclusive creation means existing identity is never overwritten.
            with path.open("x",encoding="utf-8") as handle:
                handle.write(content)
            created.append(name)
        except FileExistsError:
            preserved.append(name)
    report=status(root)
    report.update({"created":created,"preserved":preserved})
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project",type=Path,required=True,help="Existing project root")
    choice=ap.add_mutually_exclusive_group(required=True)
    choice.add_argument("--init",action="store_true",help="Create missing templates ONLY")
    choice.add_argument("--check",action="store_true",help="Read-only status, no inferred approval")
    args=ap.parse_args()
    try:
        report=init(args.project) if args.init else status(args.project)
    except (OSError,ValueError) as error:
        ap.error(str(error))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__ == "__main__":
    main()
