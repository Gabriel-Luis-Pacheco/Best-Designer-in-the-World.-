#!/usr/bin/env python3
"""Design OS Brain: evidence-aware deterministic triage, not a model or a crawler."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RULES=json.loads((ROOT/"brain/route_rules.json").read_text(encoding="utf-8"))
CATALOG=json.loads((ROOT/"research/source_catalog.json").read_text(encoding="utf-8"))
RESEARCH=json.loads((ROOT/"brain/research_briefs.json").read_text(encoding="utf-8"))
MODES={"PATCH","AUDIT","REFINE","REDESIGN","REBUILD"}

def text_field(data,key,default=""):
    value=data.get(key,default)
    if not isinstance(value,str) or len(value)>10000:
        raise ValueError(f"{key} must be a string of <=10000 characters")
    return value.strip()

def normalized_values(raw,field,allowed,limit=4):
    if raw is None or raw=="":return []
    values=[raw] if isinstance(raw,str) else raw
    if not isinstance(values,list) or len(values)>limit or any(not isinstance(x,str) for x in values):
        raise ValueError(f"invalid {field}")
    cleaned=list(dict.fromkeys(x.strip().lower() for x in values if x.strip()))
    invalid=[x for x in cleaned if x not in allowed]
    if invalid: raise ValueError(f"unknown {field}: {', '.join(invalid)}")
    return cleaned

def infer_aliases(text, aliases):
    matches=[]
    for label,words in aliases.items():
        if any(word in text for word in words):matches.append(label)
    return matches

def classify_mode(data,task):
    explicit=text_field(data,"mode").upper()
    if explicit:
        if explicit not in MODES:raise ValueError("unknown mode")
        return explicit,"explicit"
    low=task.casefold()
    if any(w in low for w in ["audite","auditar","analise","análise crítica","critique","diagnóstico"]):return "AUDIT","task_inferred"
    if any(w in low for w in ["reconstrua","rebuild","do zero","recrie tudo"]):return "REBUILD","task_inferred"
    if any(w in low for w in ["redesign","reformule","refaça a landing","nova linguagem"]):return "REDESIGN","task_inferred"
    if any(w in low for w in ["bug","corrija apenas","fix","patch","conserte o erro"]):return "PATCH","task_inferred"
    return "REFINE","default_low_confidence"

def choose_sources(tags,mode,tools):
    if mode=="PATCH":return []
    candidates=[]
    tags=set(tags)
    for row in CATALOG["sources"]:
        matching=tags.intersection(row["when"])
        if not matching and "any" not in row["when"]:continue
        kind=("visual" if row["id"] in {"awwwards","siteinspire","landbook","godly"}
              else "product-pattern" if row["id"] in {"mobbin","pageflows","carbon","atlassian","material","duolingo","apple-hig","shopify-polaris"}
              else "research")
        if kind=="visual" and ({"internal","dashboard"} & tags) and "landing" not in tags:
            continue  # Avoid marketing-gallery suggestions for data-dense tools.
        candidates.append((len(matching),kind,row))
    budget={"AUDIT":4,"REFINE":5,"REDESIGN":7,"REBUILD":7}.get(mode,4)
    candidates.sort(key=lambda x:(-x[0],x[2]["id"]))
    chosen=[];used=set()
    # Diversity: avoid treating a single aesthetic gallery as complete research.
    for required_kind in ("research","product-pattern","visual"):
        for _,kind,row in candidates:
            if kind==required_kind and row["id"] not in used:
                chosen.append((kind,row));used.add(row["id"]);break
    for _,kind,row in candidates:
        if len(chosen)>=budget:break
        if row["id"] not in used:chosen.append((kind,row));used.add(row["id"])
    return [{"id":row["id"],"url":row["url"],"kind":kind,
             "why":"Matches context: "+", ".join(sorted(tags.intersection(row["when"])) or ["general"]),
             "status":"CANDIDATE_NOT_INSPECTED",
             "next_action":"inspect with authorized browser" if "web" in tools or "browser" in tools else "research only if permitted tool available"}
            for kind,row in chosen[:budget]]

def route(context):
    if not isinstance(context,dict):raise ValueError("context must be object")
    task=text_field(context,"task")
    if not task:raise ValueError("task required")
    product=text_field(context,"product") or "Produto sem nome confirmado"
    audience=text_field(context,"audience")
    raw=text_field(context,"description")
    content=(task+" "+product+" "+raw).casefold()
    unknown=[]
    surface_source="explicit"
    surfaces=normalized_values(context.get("surface"),"surface",RULES["surfaces"],4)
    if not surfaces:
        inferred=infer_aliases(content,RULES["surface_aliases"])
        surfaces=inferred[:3] if inferred else ["product"]
        surface_source="inferred_low_confidence"
        if len(inferred)>1:
            unknown.append("Multiple surface candidates detected; validate distinct flows before design.")
        if not inferred:
            unknown.append("Surface unknown; PRODUCT provisional default.")
    vertical_source="explicit"
    vertical=normalized_values(context.get("vertical"),"vertical",RULES["verticals"],1)
    if vertical:vertical=vertical[0]
    else:
        found=infer_aliases(content,RULES["vertical_aliases"])
        vertical=found[0] if found else "general"
        vertical_source="inferred_low_confidence"
        if len(found)>1:unknown.append("Competing vertical signals: "+", ".join(found))
    mode,mode_source=classify_mode(context,task)
    goals=normalized_values(context.get("goals",context.get("goal")),"goals",RULES["goals"],4)
    goal_source="explicit" if goals else "inferred_low_confidence"
    if not goals:
        goals=[RULES["surfaces"][s]["primary_goal"] for s in surfaces]
        if vertical=="education" and "learning" not in goals:goals.insert(0,"learning")
        if vertical=="social_impact" and "quality_matches" not in goals:goals.insert(0,"quality_matches")
        if vertical=="fintech" and "trust" not in goals:goals.append("trust")
        goals=list(dict.fromkeys(goals))[:3]
    tools=context.get("tools",[])
    for field in ("authorized_change_types","protected_contract_ids"):
        val=context.get(field,[])
        if not isinstance(val,list) or len(val)>100 or any(not isinstance(x,str) or len(x)>200 for x in val):
            raise ValueError("invalid "+field)
    if not isinstance(tools,list) or len(tools)>20 or any(not isinstance(x,str) for x in tools):
        raise ValueError("tools must be a list of strings")
    tools=[x.strip().lower() for x in tools]
    facts=context.get("facts",[])
    constraints=context.get("constraints",[])
    for label,value in (("facts",facts),("constraints",constraints)):
        if not isinstance(value,list) or len(value)>100 or any(not isinstance(x,str) or len(x)>2000 for x in value):
            raise ValueError(label+" must be a bounded list of strings")
    refs=["product-truth.md","brand-canon.md","design-proof-and-decision-records.md"]
    for surface in surfaces:refs.extend(RULES["surfaces"][surface]["refs"])
    refs.extend(RULES["verticals"][vertical]["refs"])
    for goal in goals:
        if goal in {"learning","retention","engagement"}:refs.append("user-research-and-proof.md")
        if goal in {"conversion","trust"}:refs.append("visual-storytelling.md")
    if mode in {"REDESIGN","REBUILD"}:refs.extend(["editorial-art-direction-lab.md","typography-layout-craft.md"])
    refs=list(dict.fromkeys(refs))
    missing=[x for x in refs if not (ROOT/"references"/x).is_file()]
    if missing:raise ValueError("missing skill pack: "+", ".join(missing))
    guardrails=list(dict.fromkeys(RULES["verticals"][vertical]["guardrails"]+
                                 [RULES["goals"][g]["guardrail"] for g in goals]+constraints))
    alltags=surfaces+[vertical]+goals+["research","accessibility"]
    refs_selected=choose_sources(alltags,mode,tools)
    research_questions=[]
    if mode!="PATCH":
        for surface in surfaces:
            questions=(RESEARCH.get(f"{vertical}:{surface}") or RESEARCH.get(f"general:{surface}")
                       or RESEARCH["general:product"])
            for layer,question,query in questions:
                research_questions.append({"surface":surface,"layer":layer,
                    "question":question,"suggested_query":query,
                    "status":"NOT_EXECUTED","caution":"No findings before inspecting actual sources"})
    plans=[]
    for s in surfaces:
        conf=RULES["surfaces"][s]
        target=goals[0] if len(surfaces)==1 else conf["primary_goal"]
        plans.append({"surface":s,"default_job":conf["jobs"],
                      "priority_goal":target,"reference_packs":conf["refs"],
                      "suggested_measure":RULES["goals"].get(target,{}).get("metric",conf["metric"]),
                      "status":"HYPOTHESIS_NOT_VALIDATED"})
    if not audience:unknown.append("Audience and actual task context not supplied.")
    if not facts:unknown.append("Project facts are not supplied; inspect actual code/site and ask only if blocked.")
    if "web" not in tools and "browser" not in tools and refs_selected:
        unknown.append("Curated references selected offline; none were visited.")
    return {"schema_version":"9.0",
      "task":task,
      "product":{"name":product,"audience":audience or "UNKNOWN","vertical":vertical,"vertical_source":vertical_source,
                 "surfaces":surfaces,"surface_source":surface_source,"facts_provided_unverified":facts},
      "strategy":{"mode":mode,"mode_source":mode_source,"primary_goal":goals[0],
                  "secondary_goals":goals[1:],"goal_source":goal_source,
                  "goal_mechanism":RULES["goals"][goals[0]]["action"],
                  "guardrails":guardrails,"surface_plans":plans,
                  "measurement_status":"NOT_MEASURED",
                  "anti_goal":"Optimizing vanity metrics while damaging user outcome or a protected contract"},
      "tool_routing":{"selected_skill_refs":["references/"+x for x in refs],
                      "research_candidates":refs_selected,
                      "research_questions":research_questions,
                      "recommended_execution":"Inspect first; research as allowed; implement only within authorized scope; test relevant real flows."},
      "permission_boundary":{"authorized_change_types":context.get("authorized_change_types",[]),
        "protected_contract_ids":context.get("protected_contract_ids",[]),
        "default":"No alteration outside explicit authorization; run brain/decision_guard.py for proposed edits."},
      "uncertainties":unknown,
      "interpretation_limits":"Deterministic triage is not research, browser inspection, independent creative judgment or measured business impact."}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("context",nargs="?",help="Context JSON; omitted reads stdin")
    a=p.parse_args()
    try:
        raw=Path(a.context).read_text(encoding="utf-8") if a.context else sys.stdin.read()
        print(json.dumps(route(json.loads(raw)),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as exc:
        print("INVALID CONTEXT:",exc,file=sys.stderr);raise SystemExit(2)
