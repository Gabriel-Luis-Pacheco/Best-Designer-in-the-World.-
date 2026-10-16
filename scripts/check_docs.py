#!/usr/bin/env python3
"""Detect stale skill version/case counts in primary user-facing documentation."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SK=ROOT/"skills/studio-grade-web-transformation"

def validate():
    manifest=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))
    version=manifest["version"]
    count=len(manifest["evals"])
    docs={"README.md":ROOT/"README.md",
          "SKILL.md":SK/"SKILL.md",
          "EVALUATION_RUNBOOK.md":ROOT/"docs/EVALUATION_RUNBOOK.md",
          "BRAIN_README.md":SK/"brain/README.md"}
    contents={k:v.read_text(encoding="utf-8") for k,v in docs.items()}
    for name,body in contents.items():
        if "9.6" not in body:
            raise ValueError(f"{name}: missing 9.6 release reference")
    if f'version: "9.6.0"' not in contents["SKILL.md"]:
        raise ValueError("SKILL.md frontmatter does not match v9.6.0")
    for name in ("README.md","EVALUATION_RUNBOOK.md"):
        if f"{count} casos de avaliação" not in contents[name]:
            raise ValueError(f"{name}: expected case count {count}")
    if version!="9.6.0":
        raise ValueError("manifest version must match the release")
    if manifest!=json.loads((SK/"evals/evals.json").read_text(encoding="utf-8")):
        raise ValueError("portable and root evaluation manifests differ")
    if (ROOT/"docs/QUALITY_RUBRIC.md").read_text(encoding="utf-8")!=(SK/"references/quality-rubric.md").read_text(encoding="utf-8"):
        raise ValueError("rubrics differ")
    return {"version":version,"evaluation_cases":count,"docs_checked":list(docs)}

if __name__=="__main__":
    print("PASS: documentation consistency",validate())
