#!/usr/bin/env python3
"""Conservative quality readiness gate; input evidence is declared, not authenticated."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

RESULTS={"PASS","FAIL","UNKNOWN"}
SEVERITIES={"P0","P1","P2"}
def assess(report, evidence_root=None):
    if not isinstance(report,dict) or report.get("version")!=1:
        raise ValueError("unsupported report version")
    entries=report.get("checks")
    if not isinstance(entries,list) or not entries:
        raise ValueError("at least one check required")
    ids=set();block=[];warnings=[]
    verified_count=0
    root=Path(evidence_root).resolve() if evidence_root is not None else None
    for x in entries:
        if not isinstance(x,dict) or not isinstance(x.get("id"),str) or not x["id"].strip() or x["id"] in ids:
            raise ValueError("duplicate or invalid check id")
        ids.add(x["id"])
        if x.get("severity") not in SEVERITIES or x.get("result") not in RESULTS:
            raise ValueError("unknown severity or result")
        if x["result"]=="PASS" and not (isinstance(x.get("evidence"),list) and x["evidence"] and all(isinstance(y,str) and y.strip() for y in x["evidence"])):
            raise ValueError("PASS requires declared evidence")
        missing=[]
        if root is not None and x["result"]=="PASS":
            for evidence in x["evidence"]:
                rel=Path(evidence)
                target=(root/rel).resolve()
                if rel.is_absolute() or not target.is_relative_to(root) or not target.is_file() or target.stat().st_size==0:
                    missing.append(evidence)
                else:
                    verified_count+=1
        effective="UNKNOWN" if missing else x["result"]
        if effective!="PASS":
            event={"id":x["id"],"severity":x["severity"],"result":effective}
            if missing:event["missing_or_unsafe_evidence"]=missing
            if x["severity"] in {"P0","P1"}:block.append(event)
            else:warnings.append(event)
    return {"decision":"BLOCK" if block else ("REVIEW_WITH_WARNINGS" if warnings else "READY_FOR_HUMAN_REVIEW"),
            "blockers":block,"warnings":warnings,
            "file_evidence_verified":verified_count if root is not None else None,
            "limitations":("Evidence files were checked for existence, path containment and nonzero bytes; "
                           "their contents and test assertions were NOT verified."
                           if root is not None else
                           "A declared PASS and evidence reference are not independently verified. "
                           "Never call this a design score.")}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("report",type=Path)
    p.add_argument("--evidence-root",type=Path,help="Strictly verify local evidence files before PASS")
    a=p.parse_args()
    result=assess(json.loads(a.report.read_text(encoding="utf-8")),a.evidence_root)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["decision"]=="BLOCK":raise SystemExit(1)
