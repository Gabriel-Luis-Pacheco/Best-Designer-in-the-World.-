#!/usr/bin/env python3
"""Audit the actual portable guide selection for every synthetic eval case.

Checks route/injection consistency, not model execution, visual quality, or
the competence of any rival skill. Keep this executable to prevent new
specialist playbooks from silently disappearing behind reference truncation.
"""
from __future__ import annotations
import json
import pathlib
from run_evals import ROOT, SK, _route_case, selected_contextual_references, build_prompt

def audit(cases):
    if not isinstance(cases,list) or not cases:
        raise ValueError("nonempty cases required")
    reports=[]
    failures=[]
    for case in cases:
        cid=case.get("id")
        try:
            plan=_route_case(case)
            refs=selected_contextual_references(case,plan)
            assembled=build_prompt(case,"with_skill")
            baseline=build_prompt(case,"without_skill")
            found=[]
            for rel in refs:
                content=(SK / rel).read_text(encoding="utf-8")
                label="TRUSTED CONTEXTUAL REFERENCE: "+rel+"\n"
                if not content.strip() or label not in assembled:
                    raise ValueError("guide listed but missing from assembled prompt: "+rel)
                if label in baseline:
                    raise ValueError("treatment guide leaked into baseline: "+rel)
                found.append(rel)
            if len(refs)!=len(set(refs)) or len(refs)>9:
                raise ValueError("duplicate or >9 specialist refs")
            strategy=plan["strategy"]
            surfaces=plan["product"]["surfaces"]
            if strategy["mode"]=="PATCH" and len(refs)>2:
                raise ValueError("patch overloaded with design references")
            if strategy["creative_authority"]=="ART_DIRECTOR_FIRST":
                if "references/marketing-research-and-experiments.md" in refs:
                    raise ValueError("art-only project contaminated by marketing")
            if ("internal" in surfaces or "dashboard" in surfaces) and not ("landing" in surfaces or "experience" in surfaces):
                if any(x in refs for x in (
                    "references/immersive-3d-product-direction.md",
                    "references/awwwards-studio-production.md",
                    "references/creative-advantage-loop.md"
                )):
                    raise ValueError("internal work overloaded with art references")
            reports.append({"case_id":cid,"mode":strategy["mode"],"surfaces":surfaces,
                            "policy":strategy["creative_authority"],
                            "selected_refs":found,
                            "assembled_prompt_chars":len(assembled),
                            "baseline_prompt_chars":len(baseline)})
        except (OSError,ValueError,KeyError,TypeError) as exc:
            failures.append({"case_id":cid,"reason":str(exc)})
    return {"status":"ROUTING_CONSISTENT_SOURCE_ONLY" if not failures else "ROUTING_REGRESSION",
            "checked":len(cases),"failures":failures,"cases":reports,
            "limitations":["Synthetic cases and prompt strings only; agent may ignore instructions",
                           "Not proof of browser use, design quality or competitor superiority",
                           "Reference selection limits require product-specific expert judgment"]}

def main():
    manifest=json.loads((ROOT/"evals/evals.json").read_text(encoding="utf-8"))
    report=audit(manifest["evals"])
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report["status"]=="ROUTING_CONSISTENT_SOURCE_ONLY" else 1)

if __name__=="__main__":
    main()
