#!/usr/bin/env python3
"""Standalone portability and case-shape checks for installed skill. Not design grading."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def validate() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if not text.startswith("---\n") or len(parts) != 3:
        raise ValueError("bad frontmatter")
    if not re.search(r"^name: studio-grade-web-transformation$", parts[1], re.M):
        raise ValueError("wrong name")
    m = re.search(r'^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', parts[1], re.M)
    if not m:
        raise ValueError("missing version")
    for rel in re.findall(r"`((?:references|templates)/[A-Za-z0-9_./-]+\.md)`", text):
        if not (ROOT / rel).is_file():
            raise ValueError(f"missing reference/template: {rel}")
    manifest = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
    if manifest.get("skill_name") != ROOT.name or manifest.get("version") != m.group(1):
        raise ValueError("skill/manifest mismatch")
    ids = set()
    cases = manifest.get("evals", [])
    if len(cases) < 12:
        raise ValueError("insufficient cases")
    for c in cases:
        if c["id"] in ids or not isinstance(c["id"], int):
            raise ValueError("duplicate/invalid ID")
        ids.add(c["id"])
        if len(c.get("expectations", [])) < 2 or not c.get("prompt"):
            raise ValueError("invalid case")
        for path in c.get("files", []):
            p = Path(path)
            if p.is_absolute() or ".." in p.parts or not (ROOT / p).is_file() or not (ROOT / p).resolve().is_relative_to(ROOT.resolve()):
                raise ValueError(f"unsafe/missing input: {path}")
    if not (ROOT / "references/quality-rubric.md").is_file():
        raise ValueError("rubric missing")
    catalog = json.loads((ROOT / "research/source_catalog.json").read_text(encoding="utf-8"))
    if len(catalog.get("sources", [])) < 10:
        raise ValueError("missing research catalog")
    print(f"PASS: portable package only — {len(cases)} cases, version {m.group(1)}. NOT a design score.")

if __name__ == "__main__":
    try:
        validate()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        raise SystemExit(1)
