#!/usr/bin/env python3
"""Optional static declaration check, NOT source verification or aesthetic judgement."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

def s(v): return v.strip() if isinstance(v, str) else ""
def normalized(v): return re.sub(r"\s+", " ", s(v)).casefold()
def valid_href(v):
    if not s(v): return False
    if v.startswith(("/", "#")) and not v.startswith("//"): return True
    p = urlparse(v)
    return p.scheme in ("http", "https") and bool(p.netloc)

def audit(doc):
    E, W = [], []
    if not isinstance(doc, dict):
        return {"status":"BLOCKED","errors":["Root must be an object"],"warnings":[]}
    mode=doc.get("mode")
    if mode not in ("concept","production"): E.append("mode must be concept or production")
    if not s(doc.get("project")): W.append("project missing")
    a=doc.get("audience",{})
    if not isinstance(a,dict) or not s(a.get("segment")) or not s(a.get("job")): W.append("audience segment/job missing")
    p=doc.get("promise",{})
    if not isinstance(p,dict) or not s(p.get("outcome")) or not s(p.get("mechanism")): W.append("specific outcome/mechanism missing")
    c=doc.get("primary_cta",{})
    if not isinstance(c,dict) or not s(c.get("label")) or not valid_href(c.get("href")): E.append("primary CTA needs real declared destination and label")
    records=doc.get("evidence",[])
    if not isinstance(records,list): E.append("evidence must be an array"); records=[]
    byid={}
    for record in records:
        if not isinstance(record,dict): E.append("evidence entry is not an object"); continue
        id=s(record.get("id"))
        if not id or id in byid: E.append("missing/duplicate evidence ID"); continue
        byid[id]=record
        if record.get("status") not in ("verified","supplied_unverified","inferred","concept","unknown"): E.append(f"invalid evidence status: {id}")
        if record.get("status")=="verified" and not s(record.get("source")): E.append(f"verified source missing: {id}")
        if record.get("status")=="verified" and not s(record.get("rights")): W.append(f"usage rights missing: {id}")
    claims=doc.get("claims",[])
    if not isinstance(claims,list): E.append("claims must be an array"); claims=[]
    for i,claim in enumerate(claims,1):
        if not isinstance(claim,dict) or not s(claim.get("text")): E.append(f"claim #{i} missing text"); continue
        ids=claim.get("evidence_ids")
        if not isinstance(ids,list) or not ids: E.append(f"claim #{i} missing evidence mapping"); continue
        for eid in ids:
            if eid not in byid: E.append(f"claim #{i} unknown evidence: {eid}")
            elif mode=="production" and byid[eid].get("status")!="verified": E.append(f"claim #{i} unverified production evidence: {eid}")
    scenes=doc.get("scenes",[])
    if not isinstance(scenes,list) or not scenes: E.append("scenes must be nonempty array"); scenes=[]
    names=set(); messages={}
    for i,scene in enumerate(scenes,1):
        if not isinstance(scene,dict): E.append(f"scene #{i} is not object"); continue
        name=s(scene.get("id"))
        if not name or name in names: E.append(f"scene #{i} missing/duplicate ID")
        names.add(name)
        if not s(scene.get("question")) or not s(scene.get("medium")): W.append(f"scene {name} needs visitor question and medium")
        msg=normalized(scene.get("new_information"))
        if not msg: W.append(f"scene {name}: no new information, consider CUT/MERGE")
        elif msg in messages: W.append(f"scene {name}: duplicated message with {messages[msg]}, CUT/MERGE")
        else: messages[msg]=name
        for eid in scene.get("evidence_ids",[]):
            if eid not in byid: E.append(f"scene {name} unknown evidence: {eid}")
        if normalized(scene.get("medium")) in ("webgl","canvas","3d","interactive_3d") and not s(scene.get("fallback")):
            (E if mode=="production" else W).append(f"scene {name}: immersive scene requires fallback")
    d=doc.get("creative_direction",{})
    if not isinstance(d,dict) or not s(d.get("signature")): W.append("brand-specific signature missing")
    if not isinstance(d,dict) or not s(d.get("mobile_recomposition")): W.append("mobile recomposition missing")
    m=doc.get("measurement",{})
    if not isinstance(m,dict) or not s(m.get("primary_event")) or not s(m.get("denominator")): W.append("qualified metric/denominator missing (outcome UNKNOWN)")
    if isinstance(m,dict) and not m.get("guardrails"): W.append("commercial guardrails missing")
    return {"status":"BLOCKED" if E else "REVIEW_REQUIRED" if W else "DECLARATIONS_CHECKED","errors":E,"warnings":W,
            "limitations":"No live source verification, image evaluation, WCAG testing, performance or conversion evidence."}

def main():
    pa=argparse.ArgumentParser(description=__doc__); pa.add_argument("brief",type=Path); pa.add_argument("--json",action="store_true")
    args=pa.parse_args()
    try: data=json.loads(args.brief.read_text(encoding="utf-8"))
    except (OSError,ValueError) as e: print(f"Invalid input: {e}",file=sys.stderr); return 2
    out=audit(data)
    if args.json: print(json.dumps(out,ensure_ascii=False,indent=2))
    else:
        print(out["status"])
        for t in out["errors"]: print("ERROR:",t)
        for t in out["warnings"]: print("REVIEW:",t)
        print(out["limitations"])
    return 1 if out["errors"] else 0
if __name__=="__main__": raise SystemExit(main())
