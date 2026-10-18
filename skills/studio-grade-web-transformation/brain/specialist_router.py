#!/usr/bin/env python3
"""Optional advisory skill-routing workstream. NEVER installs or executes external code.
Curated entries point to sources for runtime verification; explicit goal takes priority.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"research/specialist_catalog.json"
def phrase(haystack,needle):
    """Positive mention only. Skip nearby explicit denials such as 'sem WebGL'.

    Narrow textual exclusion, not comprehensive natural-language understanding.
    """
    text=haystack.casefold()
    for match in re.finditer(r"(?<!\w)"+re.escape(needle.casefold())+r"(?!\w)",text):
        prior=re.split(r"[.!?;\n]",text[max(0,match.start()-90):match.start()])[-1]
        if re.search(r"(?:não|nao|sem|without|avoid|do not|don't)\s+(?:(?:quero|usar|use|add|adicionar|inclua|com|using)\s+)?$",prior):
            continue
        return True
    return False

def suggest(context:dict,catalog=None)->dict:
    if not isinstance(context,dict):raise ValueError("Context must be a JSON object")
    text=" ".join(str(context.get(x,"")) for x in ("task","surface","stack","goal","description"))
    mode=str(context.get("mode","")).upper()
    if not text.strip():raise ValueError("Provide task/surface/goal/stack")
    if catalog is None:catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    if catalog.get("version")!=1 or not isinstance(catalog.get("specialists"),list):
        raise ValueError("Invalid specialist catalog")
    if mode=="PATCH" and not any(phrase(text,x) for x in ("gsap","three.js","webgl","accessibility","performance")):
        return {"status":"NO_EXTERNAL_SKILL_NEEDED","specialists":[],"reason":"Patch stays focused unless a specialist is explicitly requested."}
    results=[]
    for row in catalog["specialists"]:
        keywords=row.get("triggers",[])
        hits=[s for s in keywords if phrase(text,s)]
        surfaces=row.get("surfaces",[])
        surface=str(context.get("surface","")).casefold()
        explicit_surface=surface in surfaces if surface else False
        if not hits and not explicit_surface:continue
        if surface in ("internal","dashboard","checkout") and row.get("only_marketing"):
            continue
        score=3*len(hits)+(1 if explicit_surface else 0)
        results.append((score,row["id"],row,hits))
    results.sort(key=lambda x:(-x[0],x[1]))
    limit=context.get("max_specialists",3)
    if not isinstance(limit,int) or isinstance(limit,bool) or limit<0 or limit>3:
        raise ValueError("max_specialists must be 0..3")
    chosen=[]
    for _,_,row,hits in results[:limit]:
        chosen.append({"id":row["id"],"url":row["url"],"skill_path":row.get("skill_path"),
                       "relevance":row["purpose"],"matched_terms":hits,
                       "license_reported":row["license_reported"],
                       "status":"CANDIDATE_NOT_INSTALLED_NOT_INSPECTED",
                       "next_action":"Confirm current license, exact SKILL.md, version and relevance before optional use."})
    return {"status":"PROPOSED_ONLY_NOT_EXECUTED","specialists":chosen,
            "limits":"Deterministic routing by text/declared surface; no browsing, reading, installation, team delegation or evidence of quality."}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("context",type=Path)
    a=p.parse_args()
    try:
        data=json.loads(a.context.read_text(encoding="utf-8"))
        print(json.dumps(suggest(data),ensure_ascii=False,indent=2))
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as e:
        p.exit(2,f"INVALID ROUTE: {e}\n")
if __name__=="__main__":main()
