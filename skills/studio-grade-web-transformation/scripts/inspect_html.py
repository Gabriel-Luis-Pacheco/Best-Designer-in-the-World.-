#!/usr/bin/env python3
"""Offline HTML sanity checks. No claim of WCAG conformance or visual quality."""
import argparse
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

class Scanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.targets=[]
        self.issues=[]
        self.html_lang=False
        self.main=0
        self.images=0
        self.inputs=[]
        self.labels=set()
        self.aria_refs=[]
        self.buttons=[]
        self._button=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="html":
            self.html_lang=bool(a.get("lang","").strip())
        if a.get("id"):
            self.ids.append(a["id"])
        if tag=="main":
            self.main+=1
        if tag=="label" and a.get("for"):self.labels.add(a["for"])
        if a.get("aria-labelledby"):
            self.aria_refs.extend(a["aria-labelledby"].split())
        if a.get("aria-describedby"):
            self.aria_refs.extend(a["aria-describedby"].split())
        if tag=="input" and a.get("type","text").lower() not in {"hidden","submit","reset","button"}:
            self.inputs.append((a.get("id"),bool(a.get("aria-label") or a.get("aria-labelledby") or a.get("title")))
        if tag=="img":
            self.images+=1
            if "alt" not in a:
                self.issues.append({"code":"IMAGE_ALT_MISSING","severity":"WARN"})
        if tag=="a":
            href=a.get("href")
            if href is None:
                self.issues.append({"code":"LINK_HREF_MISSING","severity":"WARN"})
            elif href.startswith("#") and len(href)>1:
                self.targets.append(href[1:])
        if tag=="button":
            self._button={"named":bool(a.get("aria-label") or a.get("title")), "text":[]}
    def handle_data(self,data):
        if self._button is not None:
            self._button["text"].append(data)
    def handle_endtag(self,tag):
        if tag=="button" and self._button is not None:
            if not self._button["named"] and not "".join(self._button["text"]).strip():
                self.issues.append({"code":"BUTTON_NAME_MAY_BE_MISSING","severity":"WARN"})
            self._button=None

def inspect(markup):
    s=Scanner();s.feed(markup)
    problems=list(s.issues)
    for i,n in Counter(s.ids).items():
        if n>1:problems.append({"code":"DUPLICATE_ID","severity":"ERROR","detail":i})
    for target in s.aria_refs:
        if target not in s.ids:problems.append({"code":"BROKEN_ARIA_REFERENCE","severity":"ERROR","detail":target})
    for input_id,named in s.inputs:
        if not named and (not input_id or input_id not in s.labels):
            problems.append({"code":"INPUT_LABEL_MAY_BE_MISSING","severity":"WARN","detail":input_id or "(no id)"})
    for t in s.targets:
        if t not in s.ids:problems.append({"code":"BROKEN_ANCHOR","severity":"ERROR","detail":t})
    if not s.html_lang:problems.append({"code":"LANG_MISSING","severity":"WARN"})
    if s.main!=1:problems.append({"code":"MAIN_COUNT","severity":"WARN","detail":str(s.main)})
    return {"status":"FAIL" if any(p["severity"]=="ERROR" for p in problems) else ("WARN" if problems else "PASS"),
            "issues":problems,"method":"static_source_only",
            "limitations":"No JS states, DOM rendering, keyboard, contrast, accessibility tree, or user studies checked."}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("html",type=Path);args=p.parse_args()
    result=inspect(args.html.read_text(encoding="utf-8"))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]=="FAIL":raise SystemExit(1)
