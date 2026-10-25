"""Lossless paired→league→paired review adapter requiring actual metadata."""
from __future__ import annotations
from copy import deepcopy
from score_review import validate_review
from compare_skill_league import validate_review as validate_league
def to_league(review,*,trial_id,task_sha256,controls,system,blind):
    p=validate_review(deepcopy(review))
    if blind is not True or not isinstance(trial_id,str) or not trial_id or not isinstance(system,str) or not system:
        raise ValueError("explicit trial/system and true blind declaration required")
    q={"trial_id":trial_id,"case_id":str(p["case_id"]),"system":system,"reviewer":p["reviewer"],
       "run_id":p["run_id"],"task_sha256":task_sha256,"controls":deepcopy(controls),"blind":True,
       "scores":deepcopy(p["scores"]),"evidence":deepcopy(p["evidence"]),
       "blockers":deepcopy(p.get("blockers",[])),
       "paired_provenance":{"pair_id":p["pair_id"],"variant":p["variant"],
                            "assertions":deepcopy(p.get("assertions",[]))}}
    return validate_league(q)
def to_paired(review):
    r=validate_league(deepcopy(review))
    prov=r.get("paired_provenance")
    if not isinstance(prov,dict) or prov.get("variant") not in ("with_skill","without_skill") or not prov.get("pair_id"):
        raise ValueError("Missing original paired provenance; cannot invent it")
    try:cid=int(r["case_id"])
    except (TypeError,ValueError):raise ValueError("No integer paired case_id") from None
    if cid<=0 or str(cid)!=r["case_id"]:raise ValueError("Lossy case_id conversion")
    p={"case_id":cid,"variant":prov["variant"],"run_id":r["run_id"],"pair_id":prov["pair_id"],
       "reviewer":r["reviewer"],"scores":deepcopy(r["scores"]),"evidence":deepcopy(r["evidence"]),
       "blockers":deepcopy(r.get("blockers",[])),"assertions":deepcopy(prov.get("assertions",[]))}
    return validate_review(p)
