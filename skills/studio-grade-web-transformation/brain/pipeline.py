#!/usr/bin/env python3
"""Compose product strategy, optional file inventory, and scope gate into one plan.

This is a planning boundary, not execution authorization, semantic understanding,
external research, or live browser testing.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load_module(name):
    spec=importlib.util.spec_from_file_location("design_os_"+name,HERE/(name+".py"))
    if spec is None or spec.loader is None:
        raise ValueError("missing brain module: "+name)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def compose(payload,project=None):
    if not isinstance(payload,dict) or not isinstance(payload.get("context"),dict):
        raise ValueError("a context object is required")
    context=payload["context"]
    strategy=(load_module("project_intake").build_plan(context,project)
              if project is not None else load_module("route").route(context))
    result={"version":"10.0.0","strategy":strategy,
            "research_state":"CANDIDATES_NOT_VISITED",
            "execution_state":"PLAN_ONLY_NOT_EXECUTED",
            "source_evidence":"NO_RUNTIME_BROWSER_OR_USER_EVIDENCE"}
    proposals=payload.get("proposals",[])
    if not isinstance(proposals,list):
        raise ValueError("proposals must be list")
    if proposals:
        change_plan={
            "version":1,
            "allowed_kinds":context.get("authorized_change_types",[]),
            "protected_targets":context.get("protected_contract_ids",[]),
            "proposals":proposals
        }
        decision=load_module("decision_guard").evaluate(change_plan)
        result["change_review"]=decision
        if decision["status"]=="BLOCKED":
            result["execution_state"]="STOP_PROTECTED_CONTRACT"
        elif decision["status"]=="REVIEW_REQUIRED":
            result["execution_state"]="REQUIRES_SCOPE_OR_DOMAIN_REVIEW"
        else:
            result["execution_state"]="IN_SCOPE_BUT_NOT_EXECUTED"
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("plan",type=Path,help="JSON with context and optional proposed edits")
    p.add_argument("--project",type=Path,help="Read-only project file inventory")
    args=p.parse_args()
    try:
        data=json.loads(args.plan.read_text(encoding="utf-8"))
        output=compose(data,args.project)
        print(json.dumps(output,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as exc:
        p.exit(2,f"INVALID PLAN: {exc}\n")
