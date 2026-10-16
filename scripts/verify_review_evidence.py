#!/usr/bin/env python3
"""Verify referenced local files; cannot attest image content, reviewer identity or remote URLs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from score_review import load_review

def inspect(review:dict,root:Path)->dict:
    root=root.resolve()
    results=[]
    for raw in review["evidence"]:
        if raw.startswith(("https://","http://")):
            results.append({"reference":raw,"status":"UNKNOWN","reason":"remote content not fetched"})
            continue
        if not isinstance(raw,str) or not raw.strip() or "\\" in raw or Path(raw).is_absolute():
            results.append({"reference":raw,"status":"FAIL","reason":"invalid or absolute path"})
            continue
        path=(root/raw).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            results.append({"reference":raw,"status":"FAIL","reason":"missing or out of evidence root"})
            continue
        if path.stat().st_size==0:
            results.append({"reference":raw,"status":"FAIL","reason":"empty file"})
            continue
        results.append({"reference":raw,"status":"PRESENT","sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    return {"status":"VERIFIED_LOCAL_FILES_ONLY" if all(x["status"]=="PRESENT" for x in results) else "INCOMPLETE",
            "evidence":results,"limitations":"Local presence/hash only; contents and human judgment not validated."}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("review",type=Path)
    p.add_argument("--root",type=Path,required=True,help="Approved evidence directory")
    a=p.parse_args()
    output=inspect(load_review(a.review),a.root)
    print(json.dumps(output,ensure_ascii=False,indent=2))
    if output["status"]=="INCOMPLETE":raise SystemExit(1)
