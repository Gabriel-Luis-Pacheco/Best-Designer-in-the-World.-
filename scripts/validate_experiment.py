#!/usr/bin/env python3
"""Fail-closed provenance checks for paired design experiments.

Checks declared metadata and local trace artifacts; neither tool transcripts nor
self-reported provenance prove cognitive use or aesthetic improvement.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

NAME="studio-grade-web-transformation"
REQUIRED_EQUAL=("model","model_revision","thinking_effort","settings",
                "task_input_sha256","tool_profile","budget")
def check_pair(pair,skill_path):
    problems=[]
    if not isinstance(pair,dict):
        return {"status":"INVALID_COMPARISON","reasons":["pair must be an object"]}
    a,b=pair.get("with_skill"),pair.get("without_skill")
    if not isinstance(a,dict) or not isinstance(b,dict):
        return {"status":"INVALID_COMPARISON","reasons":["missing conditions"]}
    for condition, data in (("with_skill", a), ("without_skill", b)):
        assembled = data.get("assembled_prompt_sha256")
        if not isinstance(assembled, str) or len(assembled) != 64 or any(c not in "0123456789abcdef" for c in assembled):
            problems.append(f"{condition}: missing or invalid assembled prompt hash")
        task_hash = data.get("task_input_sha256")
        if not isinstance(task_hash, str) or len(task_hash) != 64 or any(c not in "0123456789abcdef" for c in task_hash):
            problems.append(f"{condition}: invalid common task hash")
    for k in REQUIRED_EQUAL:
        if k not in a or k not in b or a.get(k) in (None,"",{}) or b.get(k) in (None,"",{}):
            problems.append(f"missing comparison control: {k}")
        elif a[k]!=b[k]:
            problems.append(f"unmatched comparison control: {k}")
    if a.get("assembled_prompt_sha256") == b.get("assembled_prompt_sha256"):
        problems.append("identical assembled prompts: treatment may not have been applied")
    if not a.get("workspace_id") or not b.get("workspace_id") or a["workspace_id"]==b["workspace_id"]:
        problems.append("workspaces not demonstrably isolated")
    if a.get("skill_delivery") == "INLINE_IN_AGENT_INPUT_NOT_CONFIRMED_READ":
        problems.append("inline skill instructions do not establish actual agent read trace")
    if a.get("skill_name")!=NAME or a.get("skill_loaded") is not True:
        problems.append("design-os not explicitly loaded in treatment")
    if a.get("other_design_skills")!=[]:
        problems.append("treatment has unexcluded alternative design skills")
    if b.get("skill_loaded") is not False or b.get("loaded_design_skills")!=[]:
        problems.append("baseline not isolated from installed/auto-loaded design skills")
    if not isinstance(a.get("read_trace"),list) or not a["read_trace"]:
        problems.append("no skill read trace supplied")
    try:
        skill_bytes=Path(skill_path).read_bytes()
        digest=hashlib.sha256(skill_bytes).hexdigest()
    except (OSError,TypeError,ValueError):
        problems.append("expected skill file unavailable for hash comparison")
        digest=None
    if digest:
        if a.get("skill_sha256")!=digest:
            problems.append("treatment skill hash differs from expected installed skill")
        if not any(isinstance(event,dict) and
                   event.get("operation")=="read_skill" and
                   event.get("skill_name")==NAME and
                   event.get("content_sha256")==digest
                   for event in (a.get("read_trace") if isinstance(a.get("read_trace"),list) else [])):
            problems.append("no matching read event in reported tool trace")
    return {"status":("INVALID_COMPARISON" if problems else
                       "READY_FOR_BLIND_REVIEW_NOT_PROVEN"),
            "reasons":problems,
            "limitations":["Metadata and trace are supplied by the experiment, not cryptographic proof of agent comprehension",
                           "No assertion about visual quality, A/B superiority or statistical significance",
                           "Use identical browser capture and multiple independent blinded reviews"]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair",type=Path,required=True)
    parser.add_argument("--skill",type=Path,required=True)
    args=parser.parse_args()
    try:
        pair=json.loads(args.pair.read_text(encoding="utf-8"))
        report=check_pair(pair,args.skill)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        report={"status":"INVALID_COMPARISON","reasons":[str(exc)]}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report["status"]=="READY_FOR_BLIND_REVIEW_NOT_PROVEN" else 2)

if __name__=="__main__":
    main()
