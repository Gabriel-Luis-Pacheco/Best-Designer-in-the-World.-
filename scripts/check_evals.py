#!/usr/bin/env python3
"""Offline, dependency-free, strict structure validator. NOT an aesthetic test."""
from __future__ import annotations
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "studio-grade-web-transformation"
REF_PATTERN = re.compile(r"`((?:references|templates)/[A-Za-z0-9_./-]+\.md)`")


def safe_input_path(skill_root: pathlib.Path, path: str) -> pathlib.Path:
    if not isinstance(path, str) or not path.strip():
        raise ValueError("empty/non-string fixture path")
    candidate = pathlib.PurePosixPath(path)
    if candidate.is_absolute() or ".." in candidate.parts or "\\" in path:
        raise ValueError(f"unsafe fixture path: {path}")
    target = (skill_root / path).resolve()
    if not target.is_relative_to(skill_root.resolve()) or not target.is_file():
        raise ValueError(f"missing/out-of-skill fixture: {path}")
    if target.stat().st_size == 0:
        raise ValueError(f"empty fixture: {path}")
    return target


def validate_case(case: dict, root: pathlib.Path) -> None:
    if not isinstance(case, dict) or not isinstance(case.get("id"), int) or isinstance(case["id"], bool):
        raise ValueError("case id must be an integer")
    for field in ("name", "prompt", "expected_output"):
        if not isinstance(case.get(field), str) or len(case[field].strip()) < (8 if field == "name" else 25):
            raise ValueError(f"case {case['id']}: invalid {field}")
    ex = case.get("expectations")
    if not isinstance(ex, list) or len(ex) < 2 or any(not isinstance(x, str) or len(x.strip()) < 8 for x in ex):
        raise ValueError(f"case {case['id']}: invalid expectations")
    paths = case.get("files")
    if not isinstance(paths, list) or len(paths) != len(set(paths)):
        raise ValueError(f"case {case['id']}: invalid/duplicate files")
    for path in paths:
        safe_input_path(root, path)


def validate(root: pathlib.Path = ROOT) -> dict:
    sk = root / "skills" / "studio-grade-web-transformation"
    text = (sk / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("unclosed YAML frontmatter")
    front = parts[1]
    if not re.search(r"^name: studio-grade-web-transformation$", front, re.M):
        raise ValueError("invalid skill name")
    version = re.search(r'^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', front, re.M)
    if not version:
        raise ValueError("missing metadata.version")
    links = REF_PATTERN.findall(text)
    for link in links:
        if not (sk / link).is_file():
            raise ValueError(f"missing portable reference/template: {link}")
    if len(text.splitlines()) > 500:
        raise ValueError("SKILL.md > 500 lines: use progressive references")
    full = root / "evals" / "evals.json"
    portable = sk / "evals" / "evals.json"
    manifest = json.loads(full.read_text(encoding="utf-8"))
    if manifest != json.loads(portable.read_text(encoding="utf-8")):
        raise ValueError("root and installed eval manifests diverged")
    if manifest.get("skill_name") != sk.name or manifest.get("version") != version.group(1):
        raise ValueError("manifest/version mismatch")
    cases = manifest.get("evals")
    if not isinstance(cases, list) or len(cases) < 12:
        raise ValueError("too few evaluation cases")
    ids = [x.get("id") for x in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate IDs")
    for case in cases:
        validate_case(case, sk)
    with_inputs = [c for c in cases if c["files"]]
    if len(with_inputs) < len(cases) // 2:
        raise ValueError("too few evaluation cases have realistic inputs")
    for must in ("fixtures/landing-generic.html", "fixtures/dashboard-generic.html", "fixtures/brand-original.svg", "references/quality-rubric.md"):
        if not (sk / must).is_file():
            raise ValueError(f"missing package asset: {must}")
    if (root / "docs/QUALITY_RUBRIC.md").read_text(encoding="utf-8") != (sk / "references/quality-rubric.md").read_text(encoding="utf-8"):
        raise ValueError("portable and repository rubric diverged")
    return {"cases": len(cases), "cases_with_inputs": len(with_inputs), "refs": len(links), "version": version.group(1)}


if __name__ == "__main__":
    try:
        result = validate()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        raise SystemExit(1)
    print("PASS: structural schema and portable inputs only:", result)
