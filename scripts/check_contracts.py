#!/usr/bin/env python3
"""Tests explicit facts in a SYNTHETIC design example. Not a production audit."""
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/"skills"/"studio-grade-web-transformation"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.ids=set()
        self.plans=[]
        self.in_plan=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag=="article" and "plan" in a.get("class","").split():
            self.in_plan=True
            self.plans.append([])
        if tag=="a":
            self.links.append(a)
            if self.in_plan:
                self.plans[-1].append(a.get("href"))
    def handle_endtag(self,tag):
        if tag=="article":
            self.in_plan=False

def contract_checks(html:str,brief:str)->None:
    p=Links()
    p.feed(html)
    if "R$ 19,90" not in brief or "R$ 19,90" not in html:
        raise ValueError("price contract lost")
    if "Gratuito" not in html or "R$ 0" not in brief:
        raise ValueError("free tier contract lost")
    if "Checkout NÃO implementado" not in brief or "Checkout não implementado" not in html:
        raise ValueError("checkout prototype disclosure lost")
    primary=[a for a in p.links if "data-design-critical-cta" in a]
    if len(primary)!=1 or primary[0].get("href")!="#demonstracao":
        raise ValueError("primary CTA contract changed")
    if not {"precos","demonstracao"}.issubset(p.ids):
        raise ValueError("required anchor missing")
    for a in p.links:
        h=a.get("href","")
        if h.startswith("#") and h not in ("","#") and h[1:] not in p.ids:
            raise ValueError("broken local anchor: "+h)
    if "Plano Plus aponta para #precos" not in brief:
        raise ValueError("source contract unavailable")
    if len(p.plans)<2 or "#precos" not in p.plans[1]:
        raise ValueError("Plus CTA contract changed")

def main():
    brief=(PACKAGE/"fixtures/fictional-product-brief.md").read_text(encoding="utf-8")
    html=(PACKAGE/"examples/conversaboa-concept.html").read_text(encoding="utf-8")
    contract_checks(html,brief)
    print("PASS: synthetic product contract, not production quality")

if __name__=="__main__":
    main()
