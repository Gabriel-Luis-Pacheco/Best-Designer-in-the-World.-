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
    release="v"+version.rsplit(".",1)[0]
    count=len(manifest["evals"])
    docs={"README.md":ROOT/"README.md",
          "SKILL.md":SK/"SKILL.md",
          "EVALUATION_RUNBOOK.md":ROOT/"docs/EVALUATION_RUNBOOK.md",
          "BRAIN_README.md":SK/"brain/README.md"}
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
    if (ROOT/"docs/QUALITY_RUBRIC.md").read_text(encoding="utf-8")!=(SK/"references/quality-rubric.md").read_text(encoding="utf-8"):
        raise ValueError("portable and repository rubrics differ")
    return {"version":version,"evaluation_cases":count,"docs_checked":list(docs)}

if __name__=="__main__":
    print("PASS: release consistency",validate())
