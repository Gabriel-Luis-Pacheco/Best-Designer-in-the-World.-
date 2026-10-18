#!/usr/bin/env python3
"""Source-only design smells. Hypotheses for visual review, NEVER an aesthetic grade.
Original implementation informed by study of UI Craft/Impeccable audit workflows.
"""
from __future__ import annotations
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
import re
from pathlib import Path

MAX_BYTES=4_000_000
GENERIC_PHRASES=(
    "unlock your potential","revolutionize your workflow",
    "seamless experience","take your business to the next level",
    "transform the way you","solução inovadora","experiência incrível",
    "leve seu negócio ao próximo nível","revolucione sua experiência"
)

def normalized(value:str)->str:
    return re.sub(r"\s+"," ",value.casefold()).strip()

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections=[]
        self.heading_counts=Counter()
        self.media_count=0
        self.autoplay=[]
        self.all_text=[]
        self._stack=[]
        self._excluded=0
        self._heading=None
        self._buttons=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); position=self.getpos()[0]
        if tag in ("script","style","noscript","template"):
            self._excluded+=1
            return
        if self._excluded:return
        if tag in ("section","header","main","footer") and tag=="section":
            self.sections.append({"line":position,"classes":a.get("class",""),"text":[],
                  "paragraphs":0,"articles":0,"media":0,"headings":0,"controls":0})
            self._stack.append(self.sections[-1])
        for sec in self._stack:
            if tag=="p":sec["paragraphs"]+=1
            elif tag=="article":sec["articles"]+=1
            elif tag in ("img","picture","svg","video","canvas"):sec["media"]+=1
            elif tag in ("h1","h2","h3"):sec["headings"]+=1
            elif tag in ("button","input","a"):sec["controls"]+=1
        if tag in ("img","picture","svg","video","canvas"):self.media_count+=1
        if tag in ("audio","video") and "autoplay" in a and "controls" not in a:
            self.autoplay.append({"line":position,"tag":tag,"muted":"muted" in a})
        if tag in ("h1","h2","h3") and self._heading is None:
            self._heading={"text":[],"line":position,"tag":tag}
    def handle_endtag(self,tag):
        if tag in ("script","style","noscript","template"):
            self._excluded=max(0,self._excluded-1)
            return
        if self._excluded:return
        if tag=="section" and self._stack:self._stack.pop()
        if self._heading and tag==self._heading["tag"]:
            h=normalized(" ".join(self._heading["text"]))
            if h:self.heading_counts[h]+=1
            self._heading=None
    def handle_data(self,data):
        if self._excluded:return
        txt=data.strip()
        if not txt:return
        self.all_text.append(txt)
        for s in self._stack:s["text"].append(txt)
        if self._heading:self._heading["text"].append(txt)

def inspect(markup:str)->dict:
    if not isinstance(markup,str) or len(markup.encode("utf-8"))>MAX_BYTES:
        raise ValueError("HTML must be <=4MB UTF-8 text")
    p=Page();p.feed(markup)
    findings=[]
    def flag(code,line,evidence,why,action):
        findings.append({"code":code,"severity":"REVIEW","line":line,"evidence":str(evidence)[:180],
                         "why":why,"suggested_action":action,"certainty":"SOURCE_HEURISTIC_ONLY"})
    text=normalized(" ".join(p.all_text))
    matches=[x for x in GENERIC_PHRASES if x in text]
    if matches:flag("GENERIC_CLAIM_REVIEW",1,", ".join(matches),
                    "Marketing phrase could be substitutable across unrelated products.",
                    "Compare with real product facts and audience language; do not replace without context.")
    for value,count in p.heading_counts.items():
        if count>=3:flag("REPEATED_HEADINGS_REVIEW",1,f"{value} ×{count}",
                         "Repeated headings may indicate generic section assembly.",
                         "Inspect page narrative and purposeful hierarchy.")
    card_run=0
    for i,s in enumerate(p.sections):
        body=normalized(" ".join(s["text"]))
        if s["articles"]>=3 and s["paragraphs"]>=3:card_run+=1
        else:card_run=0
        if card_run>=2:flag("ADJACENT_CARD_SECTIONS_REVIEW",s["line"],
                     f"Adjacent sections {i}–{i+1} each contain >=3 articles and paragraphs.",
                     "Repetitive card architecture may flatten the page.",
                     "Compare rendered sections; vary the visual mechanism only if meaningfully stronger.")
        if len(body)>1150 and s["media"]==0 and s["controls"]==0 and s["paragraphs"]>=4:
            flag("DENSE_SECTION_REVIEW",s["line"],f"{len(body)} chars, {s['paragraphs']} paragraphs",
                 "Text density warrants a comprehension check, but editorial pages may be intentional.",
                 "Review reading hierarchy; do not replace text with decorative cards automatically.")
    for a in p.autoplay:
        # Autoplay muted videos can be appropriate; still review pause/reduced motion.
        flag("AUTOPLAY_WITHOUT_CONTROLS_REVIEW",a["line"],a["tag"]+" muted="+str(a["muted"]),
             "Moving media without native controls needs a way to pause and a reduced-motion plan.",
             "Verify accessible custom controls or remove autoplay.")
    return {"status":"REVIEW_REQUIRED" if findings else "NO_SOURCE_HEURISTIC_FLAGS",
            "findings":findings,"sections_seen":len(p.sections),
            "method":"STATIC_SOURCE_ONLY_NOT_RENDERED",
            "limitations":["Cannot inspect CSS computed styles, React state or images",
                           "Cannot prove AI slop or artistic merit","No false positive is an automatic redesign command"]}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("html",type=Path)
    a.add_argument("--out",type=Path)
    args=a.parse_args()
    try:
        if not args.html.is_file() or args.html.stat().st_size>MAX_BYTES:
            raise ValueError("HTML file missing/oversized")
        result=inspect(args.html.read_text(encoding="utf-8"))
        content=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
        if args.out:
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(content,encoding="utf-8")
        print(content)
    except (OSError,ValueError) as exc:
        a.exit(2,f"INVALID AUDIT INPUT: {exc}\n")
if __name__=="__main__":main()
