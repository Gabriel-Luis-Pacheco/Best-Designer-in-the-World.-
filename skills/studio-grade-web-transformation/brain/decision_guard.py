#!/usr/bin/env python3
"""Audit proposed edits against explicit scope and protected contract IDs. No mutation."""
import json
import sys
from pathlib import Path

KINDS={"visual","content","pricing","data_schema","route","backend","payments","brand","animation","accessibility"}
HIGH_RISK={"pricing","data_schema","route","backend","payments","brand"}
def evaluate(plan):
    if not isinstance(plan,dict) or plan.get("version")!=1:
        raise ValueError("invalid scope plan")
    allow=plan.get("allowed_kinds",[])
    protected=plan.get("protected_targets",[])
    changes=plan.get("proposals",[])
    if not isinstance(allow,list) or not isinstance(protected,list) or not isinstance(changes,list):
        raise ValueError("invalid lists")
    if any(x not in KINDS for x in allow):
        raise ValueError("invalid allowed kind")
    if any(not isinstance(x,str) or not x for x in protected):
        raise ValueError("invalid protected target")
    ids=set();results=[]
    for item in changes:
        if not isinstance(item,dict):
            raise ValueError("invalid change")
        id_,kind,target=item.get("id"),item.get("kind"),item.get("target")
        if not isinstance(id_,str) or not id_ or id_ in ids or kind not in KINDS or not isinstance(target,str) or not target:
            raise ValueError("invalid proposal")
        ids.add(id_)
        def protected_match(value,barrier):
            # A protected contract covers its descendants; do not block a sibling.
            canonical=lambda x:x.replace("/",".").strip(".")
            value,barrier=canonical(value),canonical(barrier)
            return value==barrier or value.startswith(barrier+".")
        if any(protected_match(target,barrier) for barrier in protected):
            result="BLOCK_PROTECTED_CONTRACT";reason="Target matches protected contract or descendant"
        elif kind not in allow:
            result="NEEDS_AUTHORIZATION";reason="Outside declared change scope"
        elif kind in HIGH_RISK:
            result="REQUIRES_DOMAIN_VERIFICATION";reason="High impact despite authorized change kind"
        else:
            result="IN_SCOPE_FOR_TESTING";reason="Declared scope allows proposal; no execution happened"
        results.append({"id":id_,"kind":kind,"target":target,"decision":result,"reason":reason})
    return {"status":"BLOCKED" if any(x["decision"]=="BLOCK_PROTECTED_CONTRACT" for x in results)
            else "REVIEW_REQUIRED" if any(x["decision"] in ("NEEDS_AUTHORIZATION","REQUIRES_DOMAIN_VERIFICATION") for x in results)
            else "IN_SCOPE_NOT_EXECUTED",
            "changes":results,
            "limitations":"Checks declared contract IDs, their dot/slash descendants and edit types. It does not inspect files or diffs, grant permission or make changes."}

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("usage: decision_guard.py scope-plan.json")
    try:output=evaluate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (ValueError,OSError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    print(json.dumps(output,ensure_ascii=False,indent=2))
    if output["status"]=="BLOCKED":raise SystemExit(1)
