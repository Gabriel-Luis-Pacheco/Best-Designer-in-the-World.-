#!/usr/bin/env python3
"""Competitive full-journey reconstruction evidence gate.

Verifies local evidence and declared coverage only; NOT source authenticity,
copyright clearance, aesthetic taste, conversion, or real browser visits.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

SCOPES = {"LANDING", "ONBOARDING", "SYSTEM", "FULL_FUNNEL"}
MODES = {"REDESIGN", "REBUILD"}
SOURCE_STATES = {"INSPECTED", "PARTIAL", "NOT_OBSERVED"}
SOURCE_ROLES = {"PRIMARY", "SUPPORT"}
SCENE_KINDS = {"MARKETING_SECTION", "APP_SCREEN"}
TRANSFER_DECISIONS = {"ADOPT", "ADAPT", "REJECT"}
FLOW_STATES = {"PASS", "FAIL", "NOT_TESTED", "NOT_OBSERVED"}
REVIEW_STATES = {"PASS", "REWORK", "NOT_REVIEWED"}
REVIEWERS = {"SELF_REVIEW", "INDEPENDENT_AGENT", "HUMAN", "NOT_REVIEWED"}


@lru_cache(maxsize=1)
def _validator():
    path = Path(__file__).with_name("production_evidence.py")
    spec = importlib.util.spec_from_file_location("competitive_png_validation", path)
    if spec is None or spec.loader is None:
        raise ValueError("Missing PNG integrity validator")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.png_dimensions


def _text(value, minimum=20):
    return isinstance(value, str) and minimum <= len(value.strip()) <= 3000


def _https(value):
    if not isinstance(value, str) or len(value) > 2000:
        return False
    try:
        uri = urlsplit(value)
    except ValueError:
        return False
    return uri.scheme == "https" and bool(uri.hostname) and not uri.username and not uri.password


def _file(root: Path, value: object, *, image=False, viewport=None):
    if not isinstance(value, str) or not value or len(value) > 400 or "\\" in value:
        return None
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or p.suffix.lower() not in (
        {".png"} if image else {".md", ".txt", ".log", ".json", ".tsx", ".jsx", ".js", ".ts", ".html", ".css", ".vue", ".svelte"}
    ):
        return None
    try:
        resolved = (root / p).resolve(strict=True)
    except (OSError, ValueError):
        return None
    if not resolved.is_relative_to(root) or not resolved.is_file() or resolved.is_symlink():
        return None
    if not 50 <= resolved.stat().st_size <= 30_000_000:
        return None
    if image:
        try:
            width, height = _validator()(resolved.read_bytes())
        except (ValueError, OSError):
            return None
        if viewport == "desktop" and not (width >= 700 and height >= 400):
            return None
        if viewport == "mobile" and not (300 <= width <= 600 and height >= 480):
            return None
    return resolved


def inspect(packet: object, root: Path) -> dict:
    errors: list[str] = []
    missing: list[str] = []
    blockers: list[str] = []
    warnings: list[str] = []
    if not isinstance(packet, dict) or packet.get("schema_version") != 1:
        return {"status": "INVALID", "errors": ["schema_version must equal 1"]}
    if not isinstance(root, Path) or not root.is_dir():
        return {"status": "INVALID", "errors": ["evidence root does not exist"]}
    root = root.resolve()
    scope, mode = packet.get("scope"), packet.get("mode")
    if scope not in SCOPES:
        errors.append("scope must be LANDING / ONBOARDING / SYSTEM / FULL_FUNNEL")
    if mode not in MODES:
        errors.append("mode must be REDESIGN / REBUILD")
    project = packet.get("project")
    if not isinstance(project, dict):
        project = {}
        errors.append("project object missing")
    for key in ("audience", "actual_offer", "first_value", "protected_constraints"):
        if not _text(project.get(key)):
            missing.append("project." + key + " must contain verified project details")
    requested = project.get("requested_surfaces")
    if not isinstance(requested, list) or not requested or any(
        not isinstance(item, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{1,50}", item) for item in requested
    ) or len(set(requested)) != len(requested):
        errors.append("project.requested_surfaces must enumerate unique target section/screen IDs")
        requested = []
    requested_flows = project.get("requested_flows", [])
    if not isinstance(requested_flows, list) or any(
        not isinstance(v, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{1,50}", v) for v in requested_flows
    ) or len(set(requested_flows)) != len(requested_flows):
        errors.append("project.requested_flows must be unique IDs")
        requested_flows = []
    if scope in {"ONBOARDING", "SYSTEM", "FULL_FUNNEL"} and not requested_flows:
        missing.append("non-landing scope requires explicit requested user flows")

    seen_digests: dict[str, str] = {}
    def capture(value, label, viewport):
        item = _file(root, value, image=True, viewport=viewport)
        if item is None:
            missing.append(f"{label}: valid {viewport} viewport PNG capture missing")
            return
        digest = hashlib.sha256(item.read_bytes()).hexdigest()
        if digest in seen_digests:
            missing.append(f"{label}: identical PNG reused from {seen_digests[digest]}")
        else:
            seen_digests[digest] = label

    research = packet.get("research", {})
    if not isinstance(research, dict):
        research = {}
        errors.append("research object missing")
    sources = research.get("competitors", [])
    if not isinstance(sources, list) or not sources or len(sources) > 16:
        errors.append("research.competitors must contain 1–16 real competitors")
        sources = []
    source_ids: set[str] = set()
    source_scenes: set[tuple[str, str]] = set()
    source_flows: dict[tuple[str, str], set[str]] = {}
    primary_count = inspected_direct = 0
    for i, comp in enumerate(sources):
        tag = f"research.competitors[{i}]"
        if not isinstance(comp, dict):
            errors.append(tag + ": expected object")
            continue
        ident = comp.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9-]{2,60}", ident) or ident in source_ids:
            errors.append(tag + ": unique competitor id required")
            continue
        source_ids.add(ident)
        if not _https(comp.get("url")):
            errors.append(tag + ": HTTPS URL required")
        if comp.get("role") not in SOURCE_ROLES:
            errors.append(tag + ": PRIMARY/SUPPORT role required")
        if comp.get("inspection_status") not in SOURCE_STATES:
            errors.append(tag + ": INSPECTED/PARTIAL/NOT_OBSERVED required")
        if comp.get("kind") not in {"DIRECT", "SUBSTITUTE", "ADJACENT"}:
            errors.append(tag + ": kind must be DIRECT/SUBSTITUTE/ADJACENT")
        observed = comp.get("inspection_status") == "INSPECTED"
        if observed and comp.get("kind") in {"DIRECT", "SUBSTITUTE"}:
            inspected_direct += 1
        if observed and comp.get("role") == "PRIMARY":
            primary_count += 1
        if not observed:
            if not _text(comp.get("access_limit"), 18):
                missing.append(tag + ": partial/unobserved access needs a precise limitation")
            continue
        if not isinstance(comp.get("observed_date"), str) or not re.fullmatch(r"20\d\d-\d\d-\d\d", comp["observed_date"]):
            missing.append(tag + ": real observed_date YYYY-MM-DD required")
        for viewport in ("desktop", "mobile"):
            capture(comp.get(f"{viewport}_full_page"), f"{tag}.{viewport}_full_page", viewport)
        scenes = comp.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            missing.append(tag + ": section-by-section scroll inventory required")
            continue
        sweep = comp.get("scroll_sweep", {})
        if not isinstance(sweep, dict) or sweep.get("from_top_to_footer") is not True:
            missing.append(tag + ": confirm scroll to the footer or document partial access")
        else:
            declared = sweep.get("observed_scene_ids")
            scene_ids = [scene.get("id") for scene in scenes if isinstance(scene, dict)]
            if declared != scene_ids:
                missing.append(tag + ": scroll_sweep must enumerate every observed scene in order")
        if comp.get("role") == "PRIMARY" and len(scenes) < 3:
            missing.append(tag + ": primary benchmark needs detailed multi-section observations")
        seen_order = set()
        for n, scene in enumerate(scenes):
            sub = f"{tag}.scenes[{n}]"
            if not isinstance(scene, dict):
                errors.append(sub + ": expected object")
                continue
            sid = scene.get("id")
            if not isinstance(sid, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{1,50}", sid) or (ident, sid) in source_scenes:
                errors.append(sub + ": duplicate/invalid scene ID")
                continue
            source_scenes.add((ident, sid))
            order = scene.get("order")
            if not isinstance(order, int) or isinstance(order, bool) or order != n + 1 or order in seen_order:
                errors.append(sub + ": scene order must match full-page DOM/scroll sequence 1..N")
            seen_order.add(order)
            if scene.get("kind") not in SCENE_KINDS:
                errors.append(sub + ": scene kind invalid")
            for key in ("visitor_question", "headline_strategy", "body_copy_strategy",
                        "cta_and_proof", "composition", "media_and_motion", "mobile_behavior"):
                if not _text(scene.get(key), 24):
                    missing.append(sub + "." + key + ": actual observed detail required")
            if comp.get("role") == "PRIMARY":
                for viewport in ("desktop", "mobile"):
                    capture(scene.get(f"{viewport}_capture"), f"{sub}.{viewport}_capture", viewport)
        flows = comp.get("flows", [])
        if not isinstance(flows, list):
            errors.append(tag + ": flows must be an array")
            flows = []
        for f in flows:
            if not isinstance(f, dict) or not isinstance(f.get("id"), str):
                errors.append(tag + ": invalid competitor flow")
                continue
            key = (ident, f["id"])
            if key in source_flows:
                errors.append(tag + ": duplicated competitor flow ID")
                continue
            steps = f.get("steps", [])
            if not isinstance(steps, list) or not steps:
                missing.append(tag + ": source flow requires real step inventory")
                continue
            ids = set()
            for step in steps:
                if not isinstance(step, dict) or not isinstance(step.get("id"), str) or step["id"] in ids:
                    errors.append(tag + ": invalid/duplicate source step")
                    continue
                ids.add(step["id"])
                if not _text(step.get("control_and_feedback"), 24):
                    missing.append(tag + ": describe source step labels, choices and feedback")
                if not _text(step.get("access_state"), 12):
                    missing.append(tag + ": source step access/visibility status required")
            source_flows[key] = ids

    minimum = 3 if scope == "LANDING" else 2
    if inspected_direct < minimum or primary_count < 1:
        missing.append(f"research: need at least {minimum} inspected direct/substitute references and 1 deep PRIMARY, or label unfinished")
    if scope == "LANDING" and inspected_direct < 6 and not _text(research.get("shortfall_reason"), 30):
        missing.append("research.shortfall_reason required when fewer than 6 direct competitors inspected")
    if not _text(research.get("selection_rationale"), 30):
        missing.append("research.selection_rationale must explain why the benchmarks fit the user/job")

    target = packet.get("target", {})
    if not isinstance(target, dict):
        target = {}
        errors.append("target object missing")
    surfaces = target.get("surfaces", [])
    if not isinstance(surfaces, list):
        errors.append("target.surfaces must be an array")
        surfaces = []
    target_ids = set()
    for i, item in enumerate(surfaces):
        tag = f"target.surfaces[{i}]"
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append(tag + ": id missing")
            continue
        sid = item["id"]
        if sid in target_ids:
            errors.append(tag + ": duplicate id")
        target_ids.add(sid)
        source = item.get("dominant_source")
        if not isinstance(source, dict):
            errors.append(tag + ": must select dominant source competitor + scene")
            continue
        if (source.get("competitor_id"), source.get("scene_id")) not in source_scenes:
            missing.append(tag + ": dominant source was not observed in a real competitor scene inventory")
        if item.get("transfer") not in TRANSFER_DECISIONS:
            errors.append(tag + ": transfer decision required")
        for key in ("user_decision", "copy_strategy_transfer", "composition_transfer",
                    "media_motion_transfer", "departure_rationale", "brand_and_rights_boundary"):
            if not _text(item.get(key), 24):
                missing.append(tag + "." + key + ": observed-to-implemented decision required")
        paths = item.get("source_files")
        if not isinstance(paths, list) or not paths or any(_file(root, p) is None for p in paths):
            missing.append(tag + ": actual implementation source_files required")
        for viewport in ("desktop", "mobile"):
            capture(item.get(f"{viewport}_after"), f"{tag}.{viewport}_after", viewport)
    if set(requested) != target_ids:
        errors.append(f"requested surface coverage mismatch; missing={sorted(set(requested) - target_ids)} unexpected={sorted(target_ids - set(requested))}")

    flow_rows = target.get("flows", [])
    if not isinstance(flow_rows, list):
        errors.append("target.flows must be array")
        flow_rows = []
    flow_ids = set()
    for n, row in enumerate(flow_rows):
        tag = f"target.flows[{n}]"
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            errors.append(tag + ": invalid target flow")
            continue
        fid = row["id"]
        flow_ids.add(fid)
        source_ref = row.get("dominant_source_flow", {})
        if not isinstance(source_ref, dict) or (source_ref.get("competitor_id"), source_ref.get("flow_id")) not in source_flows:
            missing.append(tag + ": comparable inspected source flow required")
        else:
            allowed = source_flows[source_ref["competitor_id"], source_ref["flow_id"]]
            mapped = row.get("mapped_source_steps", [])
            if not isinstance(mapped, list) or not mapped or not set(mapped).issubset(allowed):
                missing.append(tag + ": mapped_source_steps must refer to observed source steps")
        if not _text(row.get("step_by_step_transfer"), 30):
            missing.append(tag + ": describe each interaction/state used in the target")
        state = row.get("test_status")
        if state not in FLOW_STATES:
            errors.append(tag + ": invalid test_status")
        elif state == "FAIL":
            blockers.append(tag + ": target funnel failed")
        elif state != "PASS":
            missing.append(tag + ": target funnel must be tested or clearly marked unavailable")
        elif _file(root, row.get("test_evidence")) is None:
            missing.append(tag + ": PASS requires an actual flow evidence file")
    if set(requested_flows) != flow_ids:
        errors.append(f"requested flow coverage mismatch; missing={sorted(set(requested_flows)-flow_ids)}")
    journey = target.get("primary_journey", {})
    if not isinstance(journey, dict):
        journey = {}
    state = journey.get("status")
    if state not in FLOW_STATES:
        errors.append("target.primary_journey.status invalid")
    elif state == "FAIL":
        blockers.append("primary CTA-to-first-value journey failed")
    elif state != "PASS":
        missing.append("primary CTA-to-first-value journey untested")
    elif _file(root, journey.get("evidence")) is None:
        missing.append("primary_journey PASS needs real evidence file")

    review = packet.get("review", {})
    if not isinstance(review, dict):
        review = {}
    if review.get("reviewer") not in REVIEWERS or review.get("verdict") not in REVIEW_STATES:
        errors.append("review must identify reviewer and PASS/REWORK/NOT_REVIEWED")
    if review.get("verdict") == "REWORK":
        blockers.append("visual critique says REWORK")
    if review.get("verdict") == "NOT_REVIEWED":
        missing.append("visual review not completed")
    if not _text(review.get("side_by_side_analysis"), 45):
        missing.append("review.side_by_side_analysis must document actual visual and copy differences")
    findings = review.get("critical_findings", [])
    if not isinstance(findings, list):
        errors.append("review.critical_findings must be array")
        findings = []
    for i, finding in enumerate(findings):
        if not isinstance(finding, dict) or finding.get("severity") not in {"P0", "P1", "P2"} or not isinstance(finding.get("resolved"), bool):
            errors.append(f"review.critical_findings[{i}] invalid")
            continue
        if not finding["resolved"] and finding["severity"] in {"P0", "P1"}:
            blockers.append(f"unresolved {finding['severity']}: {finding.get('description','')}")
    if review.get("reviewer") != "HUMAN":
        warnings.append("Self/agent review does not certify human preference or visual quality")

    status = ("INVALID" if errors else "BLOCKED" if blockers else
              "NEEDS_EVIDENCE" if missing else "READY_FOR_HUMAN_REVIEW")
    return {"status": status, "errors": errors, "missing": missing, "blockers": blockers,
            "warnings": warnings, "notice": "Checks document structure and screenshot bytes only; NOT source authenticity, quality or conversion."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        result = inspect(json.loads(args.packet.read_text(encoding="utf-8")), args.root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, "INVALID: " + str(exc) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "READY_FOR_HUMAN_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
