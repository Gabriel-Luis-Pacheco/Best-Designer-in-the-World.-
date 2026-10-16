#!/usr/bin/env python3
"""Cross-vertical smoke verification; no browser or agent inference."""
import importlib.util
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]/"skills"/"studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("design_brain_verify",R/"brain/route.py")
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
expected={"fintech-landing":("landing","conversion"),"fintech-internal":("internal","accuracy"),
          "edtech-product":("product","learning")}
for file,(surface,goal) in expected.items():
    ctx=json.loads((R/"brain/examples"/(file+".json")).read_text(encoding="utf-8"))
    out=b.route(ctx)
    assert out["strategy"]["primary_goal"]==goal,(file,out["strategy"]["primary_goal"])
    assert out["product"]["surfaces"]==[surface],(file,out["product"]["surfaces"])
    assert all(item["status"]=="CANDIDATE_NOT_INSPECTED"
               for item in out["tool_routing"]["research_candidates"])
    assert all((R/path).is_file() for path in out["tool_routing"]["selected_skill_refs"])
    print("PASS",file,surface,goal,"(offline triage, not executed research)")
