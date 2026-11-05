#!/usr/bin/env python3
"""Review claim-to-proof and positioning dependencies, never grade copy beauty."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

PROOF_STATES = {"VERIFIED", "SUPPLIED_UNVERIFIED", "PROPOSED", "UNKNOWN"}
ABSOLUTE = re.compile(r"(?i)(\b(?:guaranteed|guarantee|always|never|100%|number one|#1|o melhor do mundo|garantid[oa]|comprovad[oa])\b)")


def nonempty(value, minimum=4):
    return isinstance(value, str) and len(value.strip()) >= minimum


def inspect(payload: dict) -> dict:
    errors, evidence_gaps, review = [], [], []
    if not isinstance(payload, dict):
        return {"status": "INVALID", "errors": ["Expected JSON object"]}
    audience = payload.get("audience")
    if not isinstance(audience, dict) or any(not nonempty(audience.get(k), 8)
                                            for k in ("segment", "job", "trigger")):
        errors.append("Define best-fit audience, job and moment that triggers the need")
    alternatives = payload.get("competitive_alternatives")
    if not isinstance(alternatives, list) or not alternatives or not all(nonempty(x, 5) for x in alternatives):
        errors.append("List realistic alternatives, including status quo when relevant")
    if not nonempty(payload.get("market_category"), 6):
        errors.append("Choose a market frame that makes differentiated value understandable")
    proofs = payload.get("proofs", [])
    if not isinstance(proofs, list):
        proofs = []
        errors.append("proofs must be a list")
    known = {}
    for p in proofs:
        if not isinstance(p, dict) or not nonempty(p.get("id")) or p["id"] in known:
            errors.append("proof ids must be unique nonempty strings")
            continue
        known[p["id"]] = p
        if p.get("status") not in PROOF_STATES:
            errors.append(p["id"] + ": invalid proof status")
        if not nonempty(p.get("source"), 8):
            errors.append(p["id"] + ": include inspectable origin, not invented evidence")
    def check_proofs(ids, label, required=True):
        if not isinstance(ids, list) or (required and not ids):
            errors.append(label + ": associate proof IDs with substantive claims")
            return
        for pid in ids:
            if not isinstance(pid, str) or pid not in known:
                errors.append(label + ": unknown proof id " + str(pid))
            elif known[pid]["status"] != "VERIFIED":
                evidence_gaps.append(label + ": " + pid + " is " + str(known[pid]["status"]))
    differences = payload.get("differentiators")
    if not isinstance(differences, list) or not differences:
        errors.append("Describe specific capability -> alternative gap -> buyer value")
        differences = []
    for i, d in enumerate(differences):
        if not isinstance(d, dict):
            errors.append("Differentiator must be an object")
            continue
        for k in ("capability", "alternative_gap", "customer_outcome"):
            if not nonempty(d.get(k), 12):
                errors.append(f"Differentiator {i}: missing {k}")
        check_proofs(d.get("proof_ids"), f"differentiator {i}")
    message = payload.get("message")
    if not isinstance(message, dict):
        message = {}
        errors.append("message must be an object")
    for k in ("headline", "subheadline", "primary_cta", "cta_destination"):
        if not nonempty(message.get(k)):
            errors.append("Missing user-facing " + k)
    destination = message.get("cta_destination")
    if isinstance(destination, str) and (destination.strip() == "#" or
        destination.strip().lower().startswith(("javascript:", "todo", "coming soon"))):
        errors.append("Primary CTA cannot be a placeholder or JavaScript pseudo-link")
    for k in ("headline", "subheadline"):
        value = message.get(k, "")
        if isinstance(value, str) and ABSOLUTE.search(value):
            review.append("Review absolute/superlative language in " + k + " against verified proof")
    claims = message.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("Main offer claims require a claim-to-proof map")
        claims = []
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict) or not nonempty(claim.get("text"), 10):
            errors.append(f"Claim {i}: missing precise customer-facing claim")
            continue
        check_proofs(claim.get("proof_ids"), "claim " + str(i))
        if ABSOLUTE.search(claim["text"]):
            review.append(f"Claim {i}: verify absolute language; a cited source alone is not proof of this wording")
    objections = message.get("objections", [])
    if not isinstance(objections, list):
        errors.append("objections must be a list")
        objections = []
    for i, objection in enumerate(objections):
        if not isinstance(objection, dict) or not nonempty(objection.get("question"), 8) or not nonempty(objection.get("answer"), 10):
            errors.append(f"Objection {i}: question and accurate answer required")
        else:
            check_proofs(objection.get("proof_ids", []), f"objection {i}", required=False)
    if not message.get("cta_destination"):
        evidence_gaps.append("CTA destination not specified")
    review.extend([
        "Test 5-second offer comprehension and first-action clarity with representative people",
        "Verify that the copy speaks the audience's language, not marketer jargon",
        "Balance feeling, specificity, trust, clarity and art direction; no mandatory formula",
    ])
    state = "INVALID" if errors else "PROOF_GAPS" if evidence_gaps else "READY_FOR_HUMAN_COPY_TEST"
    return {"status": state, "errors": errors, "proof_gaps": sorted(set(evidence_gaps)),
            "review": review,
            "limitations": "Cannot verify sources, customer language, rankings, conversion or reading comprehension"}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("positioning", type=Path)
    args = p.parse_args()
    try:
        if args.positioning.stat().st_size > 200_000:
            raise ValueError("Input exceeds 200 KB")
        result = inspect(json.loads(args.positioning.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.exit(2, "INVALID INPUT: " + str(exc) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "READY_FOR_HUMAN_COPY_TEST":
        p.exit(2)


if __name__ == "__main__":
    main()
