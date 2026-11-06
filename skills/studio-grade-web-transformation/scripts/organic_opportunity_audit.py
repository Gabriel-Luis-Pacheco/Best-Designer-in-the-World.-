#!/usr/bin/env python3
"""Optional organic opportunity evidence lint: declared inputs, not search rankings.

Offline, standard library only. Does not fetch Google, query AI engines,
measure conversion, decide legal rights, calculate keyword demand or publish.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

MODES = {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}
EVIDENCE = {"OBSERVED", "SUPPLIED_UNVERIFIED", "HYPOTHESIS", "UNKNOWN"}
MAX_BYTES = 512_000
MAX_INTENTS = 100


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def valid_http(value):
    if not nonempty(value):
        return False
    try:
        p = urlparse(value)
        return p.scheme in ("https", "http") and bool(p.netloc) and not p.username and not p.password
    except (TypeError, ValueError):
        return False


def inspect(packet):
    findings = []
    def note(code, severity, where, reason):
        findings.append({"code": code, "severity": severity, "path": where, "reason": reason})

    if not isinstance(packet, dict):
        return {"status": "INVALID", "findings": [{"code": "PACKET_TYPE",
            "severity": "ERROR", "path": "$", "reason": "Expected a JSON object"}]}
    scope = packet.get("scope")
    if scope not in ("public", "private"):
        note("SCOPE_INVALID", "ERROR", "scope", "Scope must be public or private")
    if packet.get("mode") not in MODES:
        note("MODE_INVALID", "ERROR", "mode", "Unknown change scope")
    if scope == "private":
        return {"status": "INVALID" if findings else "NOT_APPLICABLE",
                "findings": findings, "limitations": ["No public discovery duties for private scope"]}
    if not nonempty(packet.get("business_goal")):
        note("BUSINESS_GOAL", "ERROR", "business_goal", "Define actual customer value, not #1 ranking")
    if not nonempty(packet.get("audience")):
        note("AUDIENCE", "ERROR", "audience", "Identify best-fit visitor or actual user job")

    intents = packet.get("intents")
    if not isinstance(intents, list) or not intents or len(intents) > MAX_INTENTS:
        note("INTENTS_INVALID", "ERROR", "intents", "Use 1–100 intentional opportunity items")
        intents = []
    seen = set()
    for i, item in enumerate(intents):
        path = "intents[%d]" % i
        if not isinstance(item, dict):
            note("INTENT_TYPE", "ERROR", path, "Each intent must be an object")
            continue
        for field in ("id", "market", "user_job", "query_family", "reason_to_win"):
            if not nonempty(item.get(field)):
                note("INTENT_FIELD_MISSING", "ERROR", path + "." + field, "Required context is missing")
        key = item.get("id")
        if nonempty(key):
            if key.casefold() in seen:
                note("DUPLICATE_INTENT_ID", "ERROR", path + ".id", "Intent ID duplicated")
            seen.add(key.casefold())
        evidence = item.get("research_status")
        if evidence not in EVIDENCE:
            note("RESEARCH_STATUS", "ERROR", path + ".research_status", "Explicit evidence state required")
        if evidence == "OBSERVED":
            src = item.get("research_source")
            if not isinstance(src, dict) or not (
                nonempty(src.get("date")) and
                (valid_http(src.get("url")) or nonempty(src.get("owned_report")))):
                note("OBSERVED_WITHOUT_SOURCE", "ERROR", path + ".research_source",
                     "An observed SERP/analytics claim requires dated traceable provenance")
        page = item.get("target_url")
        if page is not None and not valid_http(page):
            note("TARGET_URL_INVALID", "ERROR", path + ".target_url",
                 "Published target URLs must be absolute http(s), or null if not created")
        proof = item.get("original_proof")
        if not nonempty(proof):
            note("NO_ORIGINAL_ADVANTAGE", "REVIEW", path + ".original_proof",
                 "Explain evidence/product value that earns this page's existence")
        if not nonempty(item.get("next_user_action")):
            note("NO_ACTION", "REVIEW", path + ".next_user_action", "Describe useful next step")
        if evidence != "OBSERVED" and item.get("ranking_claim") is True:
            note("UNSUPPORTED_RANKING", "ERROR", path + ".ranking_claim",
                 "Do not assert rankings against unverified source data")
        if item.get("publish") is True and not nonempty(proof):
            note("PUBLISH_WITHOUT_PROOF", "REVIEW", path + ".publish",
                 "Publishing requires original beneficial content/proof")
    measurement = packet.get("measurement")
    if not isinstance(measurement, dict):
        note("MEASUREMENT_MISSING", "REVIEW", "measurement",
             "Define a qualified outcome and known/unknown baseline")
    else:
        state = measurement.get("baseline_status")
        if state not in EVIDENCE:
            note("BASELINE_STATUS", "ERROR", "measurement.baseline_status",
                 "Baseline must identify OBSERVED / SUPPLIED_UNVERIFIED / HYPOTHESIS / UNKNOWN")
        if state == "OBSERVED" and not nonempty(measurement.get("baseline_source")):
            note("BASELINE_PROVENANCE", "ERROR", "measurement.baseline_source",
                 "Observed baseline requires named report or source")
        if not nonempty(measurement.get("qualified_outcome")):
            note("OUTCOME_UNDEFINED", "REVIEW", "measurement.qualified_outcome",
                 "Do not optimize impressions without defining useful visitor/business outcome")
    levels = {f["severity"] for f in findings}
    status = "INVALID" if "ERROR" in levels else ("REVIEW" if "REVIEW" in levels else "DECLARED_READY_FOR_REVIEW")
    return {"status": status, "findings": findings,
            "limitations": ["Valid data shapes do not verify keyword demand, rankings, backlinks, conversions or rights",
                            "No online requests or competitor comparisons executed",
                            "Human review of actual sources and deployed website still required"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 if structural ERROR findings exist")
    args = parser.parse_args()
    path = args.packet
    if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_BYTES:
        parser.error("Missing, symlinked, or oversized JSON input")
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        parser.error("Invalid UTF-8 JSON: " + str(exc))
    result = inspect(packet)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.strict and result["status"] == "INVALID":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
