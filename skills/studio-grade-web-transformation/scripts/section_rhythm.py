#!/usr/bin/env python3
"""Analyze static page section rhythm to flag candidates for HUMAN review.

Informational heuristics only: text quantity and HTML shape do not determine
aesthetic quality, comprehension, CSS presentation or rendered page geometry.
"""
from __future__ import annotations
import argparse,json,re,sys
from html.parser import HTMLParser
from pathlib import Path

class SectionParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections=[]
        self.stack=[]
        self.in_skipped=0
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style","noscript"):
            self.in_skipped+=1
            return
        if tag=="section":
            node={"section":len(self.sections)+1,"text":[],"paragraphs":0,"headings":0,
                  "articles":0,"visuals":0,"controls":0,"links":0,"classes":"",
                  "id":""}
            a=dict(attrs)
            node["classes"]=a.get("class","")
            node["id"]=a.get("id","")
            self.sections.append(node)
            self.stack.append(node)
        for n in self.stack:
            if tag=="p":n["paragraphs"]+=1
            elif tag in ("h1","h2","h3","h4"):n["headings"]+=1
            elif tag=="article":n["articles"]+=1
            elif tag in ("img","svg","video","canvas","picture"):n["visuals"]+=1
            elif tag in ("button","input","select","textarea"):n["controls"]+=1
            elif tag=="a":n["links"]+=1
    def handle_endtag(self,tag):
        if tag in ("script","style","noscript"):
            self.in_skipped=max(0,self.in_skipped-1)
        if tag=="section" and self.stack:self.stack.pop()
    def handle_data(self,data):
        if not self.in_skipped:
            for n in self.stack:n["text"].append(data.strip())
def inspect(source:str)->dict:
    p=SectionParser()
    p.feed(source)
    result=[]
    for s in p.sections:
        text=" ".join(x for x in s["text"] if x)
        text=re.sub(r"\s+"," ",text).strip()
        flags=[]
        if s["articles"]>=3 and s["paragraphs"]>=3:flags.append("REPEATED_CARD_PATTERN_REVIEW")
        if len(text)>450 and not (s["visuals"] or s["controls"]) and s["paragraphs"]>=3:
            flags.append("LONG_TEXT_WITHOUT_MARKUP_VISUAL_OR_CONTROL_REVIEW")
        if s["paragraphs"]>=5 and s["headings"]<=1:
            flags.append("MANY_PARAGRAPHS_SINGLE_HEADING_REVIEW")
        result.append({"section":s["section"],"id":s["id"],"classes":s["classes"][:140],
                       "text_characters":len(text),"paragraphs":s["paragraphs"],
                       "headings":s["headings"],"articles":s["articles"],
                       "visual_elements":s["visuals"],"controls":s["controls"],
                       "links":s["links"],"review_flags":flags})
    signatures=[(x["articles"]>=3,x["visual_elements"]>0,x["controls"]>0,x["headings"]>0)
                for x in result]
    repeated=[]
    for i in range(1,len(signatures)):
        if signatures[i]==signatures[i-1] and signatures[i][0]:
            repeated.append((i,i+1))
    return {"status":"STATIC_HEURISTIC_ONLY_NOT_VISUAL_VERDICT","section_count":len(result),
            "sections":result,"adjacent_card_patterns":repeated,
            "limitations":["Cannot see CSS, geometry, scene content, imagery semantics or real mobile render",
                           "Text-heavy editorial pages can be excellent","Flags require visual and human review"]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html",type=Path)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    try:
        if args.html.stat().st_size>4_000_000:raise ValueError("HTML input too large")
        result=inspect(args.html.read_text(encoding="utf-8"))
        serialized=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
        if args.out:
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(serialized,encoding="utf-8")
        print(serialized)
    except (OSError,ValueError) as exc:
        parser.exit(2,f"INVALID INPUT: {exc}\n")
if __name__=="__main__":main()
