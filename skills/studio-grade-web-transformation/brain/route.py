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

def contains_phrase(text,phrase):
    """Whole-word Unicode matching: 'hospital' cannot match 'hospitalidade'."""
    return bool(re.search(r"(?<!\w)"+re.escape(phrase.strip().casefold())+r"(?!\w)",text.casefold()))

def negated_mention(text, phrase):
    """Conservative exclusion of explicitly negated surface descriptions.

    This is NOT language understanding; narrow sentence-level scope handles
    'not a landing page, but an immersive exhibition' without treating the
    denied category as positive evidence.
    """
    low=text.casefold()
    denied=[]
    for match in re.finditer(r"(?<!\w)"+re.escape(phrase.strip().casefold())+r"(?!\w)",low):
        prefix=low[max(0,match.start()-180):match.start()]
        prefix=re.split(r"[.!?;\n]",prefix)[-1]
        # Positive contrast begins a new clause: "not a landing, it IS an experience".
        prefix=re.split(r"(?:,\s*|\bmas\s+)(?:é|e|será|sera)\s+",prefix)[-1]
        prefix=re.split(r"\b(?:but|mas|porém|porem)\b",prefix)[-1]
        # Negating a surface is different from preserving its behavior:
        # "not a checkout" excludes it; "without changing checkout" does not.
        pt = (r"(?:não|nao)\s+(?:estamos\s+)?(?:criando|fazendo)\b|"
              r"(?:(?:não|nao)\s+(?:é|e|quero(?:\s+(?:criar|fazer|construir|ter))?|sera|será|deve\s+ser)|sem\s+ser)\s+"
              r"(?:(?:um|uma|o|a|outro|outra|novo|nova)\s+){0,2}$")
        en = (r"\b(?:(?:not|without)(?:\s+(?:creating|building|making))?|"
              r"(?:don't|don’t|do\s+not)\s+(?:want(?:\s+to\s+(?:create|build|make))?|create|build|make))\s+"
              r"(?:(?:a|an|the|another|new|commercial|sales|generic|marketing|immersive)\s+){0,3}$")
        denied.append(bool(re.search(pt, prefix) or re.search(en, prefix)))
    return bool(denied) and all(denied)

def affirmative_task_cue(text, phrase):
    """Reject nearby explicit vetoes; a later affirmative occurrence can count.

    Narrow PT/EN heuristic only. Explicit structured mode still wins, and
    complex or conflicting natural language requires actual agent judgment.
    """
    for match in re.finditer(r"(?<!\w)"+re.escape(phrase)+r"(?!\w)",text.casefold()):
        prefix=re.split(r"[.!?;,\n]|\b(?:mas|but|porém|porem)\b",text.casefold()[max(0,match.start()-80):match.start()])[-1]
        if re.search(r"(?:não|nao|sem|not|never|without|don't|don’t)\s+(?:(?:quero|que|você|voce|deve|deveria|precisa|to|want|you|should|ever|um|uma|a|an|o|novo|nova|faça|faca|fazer|do|perform|execute|realize|any|crie|criar|build|create)\s+){0,4}$",prefix):
            continue
        return True
    return False

def positive_tech_mention(text, phrase):
    """Positive technology cue, excluding simple explicit refusal.

    Deterministic, intentionally narrow (not full natural language parsing).
    The NO-* patterns are examined only near the exact cue, and a later
    positive request still activates the tech. A generic term in a product
    description is never treated as permission to introduce a new stack.
    """
    low=text.casefold()
    for found in re.finditer(r"(?<!\w)"+re.escape(phrase.casefold())+r"(?!\w)",low):
        before=re.split(r"[.!?;\n]",low[max(0,found.start()-70):found.start()])[-1]
        before=re.split(r",\s*(?:mas\s+)?",before)[-1]
        denial=r"(?:sem|without|avoid|avoiding|evite|evitar|dispensa|dispensar|not|não|nao)"
        filler=r"(?:(?:usar|use|utilizar|using|quero|want|add|adicionar|inclua|coloque|with|com)\s+){0,2}"
        if re.search(denial+r"\s+"+filler+r"$",before):
            continue
        return True
    return False

def infer_aliases(text, aliases):
    return [label for label, words in aliases.items()
            if any(contains_phrase(text,word) and not negated_mention(text,word) for word in words)]

def classify_mode(data,task):
    explicit=text_field(data,"mode").upper()
    if explicit:
        if explicit not in MODES:raise ValueError("unknown mode")
        return explicit,"explicit"
    low=task.casefold()
    limited=any(contains_phrase(low,x) for x in
                ["só","somente","apenas","mínimo","pontual","localizada","isolado"])
    patch=any(affirmative_task_cue(low,x) for x in
              ["corrija","corrige","corrigir","conserte","consertar","fix","patch","bug"])
    rebuild=any(affirmative_task_cue(low,x) for x in
                ["reconstrua","rebuild","do zero","recrie tudo"])
    redesign=any(affirmative_task_cue(low,x) for x in
                 ["redesign","redesenhe","redesenhar","reformule","refaça","nova linguagem","recrie a landing"])
    audit=any(affirmative_task_cue(low,x) for x in
              ["audite","auditar","analise","análise","análise crítica","critique","diagnóstico","audit","review","inspect","analyze"])
    implementation=any(affirmative_task_cue(low,x) for x in
                       ["implemente","implementar","aplique","aplicar","construa","construir","faça","fazer","implement","apply"])
    build_action = bool(re.search(r"(?:^|[.!?;]\s*|\b(?:and|then|please)\s+)build\b", low))
    implementation = implementation or (build_action and affirmative_task_cue(low, "build"))
    if patch and limited:return "PATCH","task_inferred_limited"
    if rebuild:return "REBUILD","task_inferred"
    if redesign:return "REDESIGN","task_inferred"
    # Mixed inspection+implementation is an execution request, not audit-only.
    # Structural redesign/rebuild and explicitly bounded patches are handled above.
    if audit and (implementation or (patch and not limited)):
        return "REFINE","task_inferred_analysis_and_execution"
    if audit and not implementation and not patch:return "AUDIT","task_inferred"
    if patch:return "PATCH","task_inferred"
    if audit:return "AUDIT","task_inferred"
    return "REFINE","default_low_confidence"

def infer_goals(task):
    """Propose explicit-seeming user intent as a hypothesis, not a business fact."""
    signals={
        "trust":["confiança","confiabilidade","transparência","transparencia","credibilidade"],
        "accuracy":["exatidão","exatidao","precisão","precisao","conciliação","conferencia"],
        "learning":["aprendizagem","aprender melhor","aprender de verdade","domínio","dominio"],
        "retention":["retenção","retencao","reter","voltar ao app"],
        "quality_matches":["adoção responsável","adocao responsavel","bons encontros"],
        "efficiency":["eficiência","eficiencia","menos tempo","produtividade"],
        "conversion":["conversão","conversao","vender","vendas","cadastros"],
        "activation":["ativação","ativacao","primeira experiência","primeiro valor"],
        "engagement":["engajamento","cativar"],
        "task_success":["concluir tarefa","resolver tarefa"],
        "artistic_impact":["impacto visual","mais bonito","mais bonita","extraordinário",
                          "extraordinario","awwwards","site of the year","site of the day",
                          "espetáculo visual","espetaculo visual","surpreender","memorável",
                          "memoravel","impressione","direção artística"],
        "immersion":["imersivo","imersiva","imersão","imersao","mundo digital artístico",
                     "experiência visual e interativa"]
    }
    negative_click=any(contains_phrase(task,x) for x in
                       ["não preciso aumentar cliques","nao preciso aumentar cliques",
                        "sem priorizar conversão","sem priorizar conversao"])
    detected=[]
    for goal,expressions in signals.items():
        if goal=="conversion" and negative_click:continue
        if any(contains_phrase(task,x) for x in expressions):detected.append(goal)
    return detected

def intent_policy(task,surfaces):
    """Choose art/commerce/operational emphasis as a hypothesis, not a verdict."""
    # Protect operational and purchase workflows even without art-keyword cues.
    if any(s in surfaces for s in ("internal","dashboard")):
        return "OPERATIONAL_FIRST_ART_SUPPORT"
    if "checkout" in surfaces:
        return "COMMERCE_FIRST_ART_SUPPORT"
    if "experience" not in surfaces:
        return "TASK_FIRST"
    if "landing" in surfaces:
        return "EXPERIENTIAL_COMMERCE"
    if "product" in surfaces:
        return "PRODUCT_FIRST_ART_SUPPORT"
    return "ART_DIRECTOR_FIRST"

def autonomy_guidance(mode, audience, facts):
    """Non-authoritative, bounded next actions for a weak brief, never permission."""
    if mode=="AUDIT":
        actions=["Inspect real assets/code and identify evidence-based faults",
                 "Report prioritized corrections without implementing"]
    elif mode=="PATCH":
        actions=["Inspect exact defect and protected contracts",
                 "Apply smallest authorized fix and verify affected states"]
    else:
        actions=["Inspect existing product, brand, sources and critical workflows",
                 "Choose a justified ownable direction with reversible defaults",
                 "Build full key journey and intentional mobile composition",
                 "Render, critique weakest part, correct and retest"]
        if not facts:
            actions.insert(1,"If truth remains unavailable, label concepts/sample content, never invent real commercial proof")
    return {
        "status":"ADVICE_ONLY_NOT_PERMISSION",
        "brief_state":"UNDERSPECIFIED_OR_UNVERIFIED" if not facts or not audience else "SUPPLIED_NOT_INDEPENDENTLY_VERIFIED",
        "agent_owned_next_actions":actions,
        "reversible_defaults":["hierarchy","spacing","responsive visual composition","clearly labeled prototype"],
        "must_not_infer":["real capabilities","testimonials","sales metrics","prices/payment terms",
                          "brand asset rights","authorization for destructive changes"],
        "clarify_only_if":"Material blocking unknown cannot be inspected or safely represented as a labeled hypothesis"
    }


def new_project_request(task):
    """Avoid treating a fresh commissioned website as a refinement of an existing one."""
    build=any(affirmative_task_cue(task,p) for p in
              ["crie","criar","cria","construa","construir","desenvolva","desenvolver",
               "do zero","from scratch","build a","create a","faça um","faça uma","faz um","faz uma","make me a"])
    existing=any(contains_phrase(task,p) for p in
                 ["existente","atual","corrija","corrigir","melhore","melhorar",
                  "refine","ajuste","ajustar","conserte","bug"])
    return build and not existing

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
        if kind=="visual" and "read" in tags and not {"landing","experience"}.intersection(tags):
            continue  # Informational work needs information design, not gallery defaults.
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
    if mode=="REFINE" and new_project_request(task):
        mode,mode_source="REBUILD","new_project_build"
    policy=intent_policy(task,surfaces)
    goals=normalized_values(context.get("goals",context.get("goal")),"goals",RULES["goals"],4)
    goal_source="explicit" if goals else "inferred_low_confidence"
    if not goals:
        intent_goals=infer_goals(task)
        goals=intent_goals + [RULES["surfaces"][s]["primary_goal"] for s in surfaces]
        if policy=="ART_DIRECTOR_FIRST":
            # A digital artwork has no default commercial funnel.
            intent_goals=[g for g in intent_goals if g not in {"conversion","activation"}]
            goals=["artistic_impact","immersion"]+[g for g in goals if g not in {"artistic_impact","immersion","conversion","activation"}]
        elif policy=="EXPERIENTIAL_COMMERCE":
            # Spectacle and buyer understanding are BOTH essential.
            goals=["artistic_impact","conversion","immersion"]+[g for g in goals if g not in
                  {"artistic_impact","conversion","immersion"}]
        elif policy in {"OPERATIONAL_FIRST_ART_SUPPORT","COMMERCE_FIRST_ART_SUPPORT",
                        "PRODUCT_FIRST_ART_SUPPORT"}:
            protected_order=("internal","dashboard") if policy=="OPERATIONAL_FIRST_ART_SUPPORT" else (
                            ("checkout",) if policy=="COMMERCE_FIRST_ART_SUPPORT" else ("product",))
            op=next((RULES["surfaces"][s]["primary_goal"] for s in protected_order
                     if s in surfaces),"task_success")
            goals=[op]+[g for g in goals if g not in {op,"artistic_impact","immersion"}]+["artistic_impact"]
        # Pedagogical mastery is the goal of a learning PRODUCT, not necessarily its landing page.
        if vertical=="education" and any(s in surfaces for s in ("product","mobile")):
            goals.insert(0,"learning")
        if vertical=="social_impact" and any(s in surfaces for s in ("product","mobile")):
            goals.insert(0,"quality_matches")
        if vertical=="fintech" and "trust" not in goals:goals.append("trust")
        # A goal stated in natural language outranks our industry defaults.
        goals=list(dict.fromkeys((goals if "experience" in surfaces else intent_goals+goals)))[:4]
        if intent_goals:goal_source="task_inferred_low_confidence"
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
    refs=(["creative-experience-direction.md","motion-and-interaction-direction.md"]
          if "experience" in surfaces and policy not in
          {"OPERATIONAL_FIRST_ART_SUPPORT","COMMERCE_FIRST_ART_SUPPORT"} else
          ["product-truth.md","brand-canon.md","design-proof-and-decision-records.md"])
    if policy=="EXPERIENTIAL_COMMERCE":
        refs.extend(["experiential-commerce.md","product-truth.md","full-page-craft-review.md"])
    if policy=="OPERATIONAL_FIRST_ART_SUPPORT":
        refs.extend(["advanced-product-ux-operations.md","product-truth.md"])
    for surface in surfaces:
        if surface=="experience" and policy in {"OPERATIONAL_FIRST_ART_SUPPORT","COMMERCE_FIRST_ART_SUPPORT"}:
            continue  # Artistic labels cannot override data/payment contracts.
        refs.extend(RULES["surfaces"][surface]["refs"])
    refs.extend(RULES["verticals"][vertical]["refs"])
    for goal in goals:
        if goal in {"learning","retention","engagement"}:refs.append("user-research-and-proof.md")
        if goal in {"conversion","trust"}:refs.append("visual-storytelling.md")
    if mode in {"REDESIGN","REBUILD"}:
        # Operational products must not inherit an art-gallery agenda by default.
        if any(s in surfaces for s in ("internal","dashboard","checkout")):
            # Surface type, not an ART-only policy, governs operational references.
            # This also covers ordinary backoffices with no "experience" label.
            refs.extend(["advanced-product-ux-operations.md","typography-layout-craft.md"])
        elif "read" in surfaces and not {"landing","experience"}.intersection(surfaces):
            refs.extend(["reading-and-information-design.md","typography-layout-craft.md"])
        else:
            refs.extend(["editorial-art-direction-lab.md","typography-layout-craft.md"])
            if "experience" in surfaces and policy not in {"OPERATIONAL_FIRST_ART_SUPPORT","COMMERCE_FIRST_ART_SUPPORT"}:
                refs.extend(["creative-experience-direction.md","full-page-craft-review.md"])
            else:
                refs.append("applied-design-decisions.md")
    # A high-effect brief triggers the technology playbook; ordinary landing/product
    # work does not inherit 3D dependencies. Keywords are provisional only.
    creative_tech_terms = ["webgl", "webgpu", "three.js", "react three fiber",
        "shader", "shaders", "3d", "r3f", "gsap", "rive", "scroll cinematográfico",
        "scroll cinematografico", "câmera 3d", "camera 3d", "motion complexo"]
    if any(positive_tech_mention(content, term) for term in creative_tech_terms):
        refs.append("creative-technology-playbook.md")
    if "experience" in surfaces or ("landing" in surfaces and
            any(contains_phrase(content,term) for term in
            ["awwwards", "site of the day", "site of the year"])):
        refs.append("award-readiness-and-qa.md")
    if any(contains_phrase(content,term) for term in
           ["orquestração de skills", "orquestracao de skills", "seleção de skills",
            "selecao de skills", "skills externas", "skill router"]):
        refs.append("specialist-skills-orchestration.md")
    # Select specialized knowledge by actual task; never load it for every project.
    if mode in {"AUDIT","REFINE","REDESIGN"} and any(s in surfaces for s in ("landing","experience","product")):
        refs.append("design-audit-execution.md")
    if mode in {"REDESIGN","REBUILD"} and any(s in surfaces for s in ("landing","experience","product")):
        refs.append("persistent-design-knowledge.md")
    if "landing" in surfaces and any(g in goals for g in ("conversion","activation","trust")):
        refs.append("marketing-research-and-experiments.md")
    if any(positive_tech_mention(content, term) for term in
           ["three.js","webgl","webgpu","r3f","gsap","rive","shader","shaders","motion complexo","3d"]):
        refs.append("motion-3d-engineering-cookbook.md")
    if any(contains_phrase(content, term) for term in
           ["site completo","site multipágina","site multipagina","multipágina",
            "multipagina","publicação","publicacao","deploy","launch website"]):
        refs.append("site-build-to-handoff.md")
    refs=list(dict.fromkeys(refs))
    missing=[x for x in refs if not (ROOT/"references"/x).is_file()]
    if missing:raise ValueError("missing skill pack: "+", ".join(missing))
    guardrails=list(dict.fromkeys(RULES["verticals"][vertical]["guardrails"]+
                                 [RULES["goals"][g]["guardrail"] for g in goals]+constraints))
    alltags=surfaces+[vertical]+goals+["research","accessibility"]
    if "landing" in surfaces:
        alltags+=["marketing","editorial"]
    if mode in {"REDESIGN","REBUILD"} and "landing" in surfaces:
        alltags+=["brand"]
    if "experience" in surfaces:
        alltags+=["brand","editorial","visual"]
    refs_selected=choose_sources(alltags,mode,tools)
    if "experience" in surfaces:
        # Creative works favor artistic reference discovery; research is still not performed.
        refs_selected.sort(key=lambda x:(x["kind"]!="visual", x["kind"]!="research", x["id"]))
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
                      "priority_goal":target,"governing_goal":goals[0],
                      "explicit_goals_not_overridden":goal_source=="explicit",
                      "reference_packs":conf["refs"],
                      "suggested_measure":RULES["goals"].get(target,{}).get("metric",conf["metric"]),
                      "status":"HYPOTHESIS_NOT_VALIDATED"})
    if not audience:unknown.append("Audience and actual task context not supplied.")
    if not facts:unknown.append("Project facts are not supplied; inspect actual code/site and ask only if blocked.")
    if "web" not in tools and "browser" not in tools and refs_selected:
        unknown.append("Curated references selected offline; none were visited.")
    # The router can expose its uncertainty, never erase it. This is deterministic
    # keyword triage, not project understanding or a replacement for agent judgment.
    inferred_fields=[key for key,src in (
        ("surface",surface_source),("vertical",vertical_source),
        ("mode",mode_source),("goal",goal_source))
        if src!="explicit"]
    context_gaps=[]
    if not audience:context_gaps.append("audience")
    if not facts:context_gaps.append("verified_product_facts")
    if surface_source!="explicit" and len(surfaces)>1:
        context_gaps.append("multiple_inferred_surfaces")
    if policy in {"ART_DIRECTOR_FIRST","EXPERIENTIAL_COMMERCE"}:
        context_gaps.append("visual_art_direction_must_be_proven_in_render")
    return {"schema_version":"11.7",
      "task":task,
      "product":{"name":product,"audience":audience or "UNKNOWN","vertical":vertical,"vertical_source":vertical_source,
                 "surfaces":surfaces,"surface_source":surface_source,"facts_provided_unverified":facts},
      "strategy":{"mode":mode,"mode_source":mode_source,"primary_goal":goals[0],
                  "secondary_goals":goals[1:],"goal_source":goal_source,
                  "goal_policy":"Explicit goals govern all surface plans; surface-specific defaults are subgoals, not replacements.",
                  "goal_mechanism":RULES["goals"][goals[0]]["action"],
                  "guardrails":guardrails,"surface_plans":plans,
                  "measurement_status":"NOT_MEASURED",
                  "anti_goal":("Replacing art direction with conventional components or explanatory UI" if
                               "experience" in surfaces else
                               "Optimizing vanity metrics while damaging user outcome or a protected contract"),
                  "creative_authority":policy,
                  "artistic_priority":("Composition, memorable scenes, typography as material, spatial transition, interactive climax"
                                      if policy=="ART_DIRECTOR_FIRST" else
                                      "Art and product story with a real next step" if policy=="EXPERIENTIAL_COMMERCE" else
                                      "SUPPORTS_PRIMARY_GOAL"),
                  "quality_axes":(["originality","composition","interaction","narrative","mobile","performance"]
                                  if policy=="ART_DIRECTOR_FIRST" else
                                  ["artistic_impact","product_clarity","desire","action_integrity","mobile","performance"]
                                  if policy=="EXPERIENTIAL_COMMERCE" else
                                  ["task_accuracy","data_integrity","accessibility","efficiency"])},
      "autonomy_guidance":autonomy_guidance(mode,audience,facts),
      "triage_review":{"interpretation":"HYPOTHESIS_ONLY",
                       "execution_intent":("ANALYZE_AND_IMPLEMENT" if mode_source=="task_inferred_analysis_and_execution"
                                           else "ANALYSIS_ONLY" if mode=="AUDIT" else "IMPLEMENTATION_OR_PLANNING"),
                       "inferred_fields":inferred_fields,
                       "context_gaps":context_gaps,
                       "must_validate_against":"actual user brief, code, canonical assets and rendered behavior",
                       "approval":"NOT_AUTHORIZED_TO_EDIT_FROM_THIS_OUTPUT"},
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
