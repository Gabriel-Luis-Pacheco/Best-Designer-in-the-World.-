#!/usr/bin/env python3
"""Portable, stdlib-only HTML contract assertions; checks static source, not live flows."""
from __future__ import annotations
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"contains_text", "contains_id", "link_with_text", "prohibited_text"}

class Snapshot(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[]
        self.ids=set()
        self.links=[]
        self._href=None
        self._chunks=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag=="a":
            self._href=a.get("href")
            self._chunks=[]
    def handle_data(self,data):
        self.text.append(data)
        if self._href is not None:
            self._chunks.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self._href is not None:
            self.links.append((self._href," ".join(" ".join(self._chunks).split())))
            self._href=None

def within(path):
    if not isinstance(path,str) or not path or "\\" in path:
        raise ValueError("unsafe file path")
    candidate=(ROOT/path).resolve()
    if not candidate.is_relative_to(ROOT.resolve()) or not candidate.is_file():
        raise ValueError("unsafe or missing file")
    return candidate

def validate_spec(spec):
    if not isinstance(spec,dict) or spec.get("version")!=1:
        raise ValueError("unsupported contract schema")
    if not isinstance(spec.get("checks"),list) or not spec["checks"]:
        raise ValueError("checks required")
    within(spec.get("artifact"))
    seen=set()
    for item in spec["checks"]:
        if not isinstance(item,dict) or item.get("kind") not in KINDS:
            raise ValueError("unknown check")
        if not isinstance(item.get("id"),str) or not item["id"].strip() or item["id"] in seen:
            raise ValueError("duplicate/empty check ID")
        seen.add(item["id"])
        if not isinstance(item.get("value"),str) or not item["value"].strip():
            raise ValueError("check requires value")
        if item["kind"]=="link_with_text" and (not isinstance(item.get("href"),str) or not item["href"].strip()):
            raise ValueError("link needs target")

def check(spec):
    validate_spec(spec)
    snap=Snapshot()
    snap.feed(within(spec["artifact"]).read_text(encoding="utf-8"))
    text=" ".join(" ".join(snap.text).split()).casefold()
    out=[]
    for item in spec["checks"]:
        kind,value=item["kind"],item["value"]
        if kind=="contains_text": ok=value.casefold() in text
        elif kind=="prohibited_text": ok=value.casefold() not in text
        elif kind=="contains_id": ok=value in snap.ids
        else:
            ok=any(item["href"]==href and value.casefold() in label.casefold() for href,label in snap.links)
        out.append({"id":item["id"],"kind":kind,"status":"PASS" if ok else "FAIL"})
    return {"status":"PASS" if all(x["status"]=="PASS" for x in out) else "FAIL","checks":out,
            "limitations":"Static HTML only. JS and click behavior NOT tested."}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("contract",help="JSON relative to the installed skill root")
    a=p.parse_args()
    output=check(json.loads(within(a.contract).read_text(encoding="utf-8")))
    print(json.dumps(output,ensure_ascii=False,indent=2))
    if output["status"]=="FAIL": raise SystemExit(1)
