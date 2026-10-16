#!/usr/bin/env python3
"""Validate the curated source index; DOES NOT visit, endorse or license any site."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
def validate_catalog(doc:dict)->dict:
    if not isinstance(doc,dict) or doc.get("version")!=1:
        raise ValueError("catalog schema")
    rows=doc.get("sources")
    if not isinstance(rows,list) or len(rows)<10:
        raise ValueError("catalog too sparse")
    seen=set()
    for x in rows:
        if not isinstance(x,dict) or not isinstance(x.get("id"),str) or not x["id"] or x["id"] in seen:
            raise ValueError("duplicate/invalid source id")
        seen.add(x["id"])
        url=urlsplit(x.get("url",""))
        if url.scheme!="https" or not url.hostname or url.username or url.password:
            raise ValueError("URL must be HTTPS without embedded credentials")
        if not isinstance(x.get("when"),list) or not x["when"] or not all(isinstance(tag,str) and tag.strip() for tag in x["when"]):
            raise ValueError("source needs applicability tags")
        if not x.get("extract") or not x.get("caution") or x.get("access")!="VERIFY_AT_RUNTIME":
            raise ValueError("source requires extraction, caveat and runtime verification flag")
    return {"entries":len(rows),"status":"CATALOG_SHAPE_VALID_ONLY"}

if __name__=="__main__":
    src=ROOT/"research/source_catalog.json"
    print(json.dumps(validate_catalog(json.loads(src.read_text(encoding="utf-8"))),ensure_ascii=False,indent=2))
