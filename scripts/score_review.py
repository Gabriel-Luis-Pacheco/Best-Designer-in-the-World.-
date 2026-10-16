#!/usr/bin/env python3
"""Summarize HUMAN reviews only; do not invent aesthetic scores."""
import json,sys,pathlib
if len(sys.argv)!=2:
    raise SystemExit("usage: python scripts/score_review.py path/to/human-review.json")
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text(encoding="utf-8"))
assert d.get("reviewer"),"reviewer is required"
assert d.get("case_id") is not None and d.get("variant") in ("with_skill","without_skill")
scores=d.get("scores",{})
assert isinstance(scores,dict) and scores,"human scores required"
for name,value in scores.items():
    assert isinstance(value,int) and 0<=value<=4,(name,value)
blockers=d.get("blockers",[])
assert isinstance(blockers,list)
for b in blockers:
    assert b.get("severity") in ("P0","P1","P2") and b.get("evidence"),"severity and evidence required"
assertions=d.get("assertions",[])
for a in assertions:
    assert a.get("result") in ("PASS","FAIL","UNKNOWN")
print("Case:",d["case_id"],"| Variant:",d["variant"],"| Human reviewer:",d["reviewer"])
print("Judgments (0-4):",scores)
print("Worst dimension:",min(scores,key=scores.get),"=",min(scores.values()))
print("Blockers:",len([b for b in blockers if b["severity"] in ("P0","P1")]))
print("Assertions:",{x:sum(a["result"]==x for a in assertions) for x in ("PASS","FAIL","UNKNOWN")})
print("Status:",("BLOCKED" if any(b["severity"] in ("P0","P1") for b in blockers) else "HUMAN_REVIEW_ONLY"))
