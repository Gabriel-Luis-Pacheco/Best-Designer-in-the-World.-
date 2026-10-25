#!/usr/bin/env python3
"""Check released version across skill, docs, runtime and portable evaluation package."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SK=ROOT/"skills/studio-grade-web-transformation"

def validate():
    manifest=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))
    version=manifest["version"]
    release="v"+version
    count=len(manifest["evals"])
    docs={"README.md":ROOT/"README.md",
          "SKILL.md":SK/"SKILL.md",
          "EVALUATION_RUNBOOK.md":ROOT/"docs/EVALUATION_RUNBOOK.md",
          "BRAIN_README.md":SK/"brain/README.md",
          "START_HERE.md":ROOT/"docs/START_HERE.md"}
    contents={name:path.read_text(encoding="utf-8") for name,path in docs.items()}
    for name,body in contents.items():
        if release not in body:
            raise ValueError(f"{name}: missing current {release} reference")
    if f'version: "{version}"' not in contents["SKILL.md"]:
        raise ValueError(f"SKILL.md metadata.version must equal {version}")
    if not re.search(r'"version"\s*:\s*"'+re.escape(version)+r'"',
                     (SK/"brain/pipeline.py").read_text(encoding="utf-8")):
        raise ValueError("brain/pipeline.py version mismatch")
    if json.loads((ROOT/"package.json").read_text(encoding="utf-8")).get("version")!=version:
        raise ValueError("package.json version mismatch")
    for name in ("README.md","EVALUATION_RUNBOOK.md"):
        if f"{count} casos de avaliação" not in contents[name]:
            raise ValueError(f"{name}: expected current case count {count}")
    if manifest!=json.loads((SK/"evals/evals.json").read_text(encoding="utf-8")):
        raise ValueError("portable and root evaluation manifests differ")
    rubric=(SK/"references/quality-rubric.md").read_text(encoding="utf-8")
    if (ROOT/"docs/QUALITY_RUBRIC.md").read_text(encoding="utf-8")!=rubric:
        raise ValueError("portable and repository rubrics differ")
    if release not in rubric:
        raise ValueError("human-review rubric version mismatch")
    from quality_schema import load_schema
    groups=load_schema()["dimensions"]
    if {k:len(v) for k,v in groups.items()}!={"general":11,"landing":4,"product":3,"art":4}:
        raise ValueError("rubric dimensions changed without review")
    index=(SK/"references/resource-index.md").read_text(encoding="utf-8")
    listed=set(re.findall(r"references/([a-z0-9.-]+\.md)",index))
    actual={p.name for p in (SK/"references").glob("*.md") if p.name!="resource-index.md"}
    if listed!=actual:
        raise ValueError("reference index drift: missing="+str(sorted(actual-listed))+" extra="+str(sorted(listed-actual)))
    craft=(SK/"references/full-page-craft-review.md").read_text(encoding="utf-8")
    if "0–4" in craft or "0–4" in rubric:
        raise ValueError("inconsistent human-review scale; use 0–3")
    return {"version":version,"evaluation_cases":count,"docs_checked":list(docs)}

if __name__=="__main__":
    print("PASS: release consistency",validate())
