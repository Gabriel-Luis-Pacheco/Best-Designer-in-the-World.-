#!/usr/bin/env python3
"""Evidence-aware design feedback summaries, never auto-changing the strategy rules."""
from __future__ import annotations
import json
import sys
from pathlib import Path

def summarize(report):
    if not isinstance(report,dict) or report.get("version")!=1:
        raise ValueError("unsupported feedback")
    if not isinstance(report.get("goal"),str) or not report["goal"].strip():
        raise ValueError("goal missing")
    obs=report.get("observations")
    if not isinstance(obs,list) or not obs:
        raise ValueError("observations required")
    results=[];regressed=[];unknown=[]
    for o in obs:
        if not isinstance(o,dict) or not isinstance(o.get("metric"),str) or not o["metric"].strip():
            raise ValueError("metric invalid")
        if o.get("direction") not in {"up","down"} or o.get("role") not in {"primary","guardrail"}:
            raise ValueError("direction/role invalid")
        a,b=o.get("baseline"),o.get("after")
        proof=o.get("evidence")
        if (type(a) not in {int,float} or type(b) not in {int,float}
            or not isinstance(proof,str) or not proof.strip()
            or not isinstance(o.get("sample"),int) or isinstance(o["sample"],bool) or o["sample"]<1):
            unknown.append({"metric":o["metric"],"status":"UNKNOWN","reason":"baseline, follow-up, provenance and positive sample required"})
            continue
        delta=b-a
        improved=delta>0 if o["direction"]=="up" else delta<0
        unchanged=delta==0
        status="NO_CHANGE" if unchanged else ("IMPROVED_OBSERVED" if improved else "REGRESSION_OBSERVED")
        item={"metric":o["metric"],"role":o["role"],"baseline":a,"after":b,"delta":delta,
              "sample":o["sample"],"evidence_claim":proof,"status":status}
        results.append(item)
        if o["role"]=="guardrail" and status=="REGRESSION_OBSERVED":regressed.append(o["metric"])
    return {"decision":"INVESTIGATE_GUARDRAIL_REGRESSION" if regressed else "INSUFFICIENT_EVIDENCE" if unknown else "REVIEW_OBSERVATIONS",
            "observed":results,"unknown":unknown,"guardrails_regressed":regressed,
            "next_actions":["Review confounders, cohorts, instrumentation and causal validity",
                            "Inspect affected user tasks and artifact changes",
                            "Propose rule updates only after independent evaluation"],
            "limitations":"Numbers are user-declared and not validated against a measurement system; observed movement is not causal lift."}

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("usage: feedback_loop.py study.json")
    try:r=summarize(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (ValueError,OSError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps(r,ensure_ascii=False,indent=2))
