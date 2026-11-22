#!/usr/bin/env python3
"""Check documented phase completion for a Design OS component.

Read-only structural evidence gate. It does NOT validate art quality, actual
source contents, real human participation or measured conversion effects.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_BYTES = 10_000_000
ALLOWED = {".md", ".txt", ".json", ".log", ".png", ".jpg", ".jpeg", ".webp",
           ".html", ".htm", ".css", ".js", ".ts", ".tsx", ".jsx", ".svg", ".pdf"}
STATUSES = {"DONE", "NOT_STARTED", "SKIPPED_WITH_REASON"}
EXPERT_STATUSES = {"APPLIED", "REFERENCED", "UNAVAILABLE", "NOT_APPLICABLE"}
FLOW_STATES = {"TESTED_PASS", "TESTED_FAIL", "NOT_TESTED"}
EDITORIAL_STATES = {"NOT_REVIEWED", "SELF_REVIEW_ONLY", "INDEPENDENT_REVIEW", "HUMAN_REVIEWED"}
MODES = {"PATCH", "REFINE", "AUDIT", "REDESIGN", "REBUILD"}


def _workplan_module():
    spec = importlib.util.spec_from_file_location("component_workplan_for_delivery", HERE / "component_workplan.py")
    if spec is None or spec.loader is None:
        raise ValueError("Missing workplan module")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _safe_artifact(root: Path, raw: str, *, image: bool = False) -> bool:
    if not isinstance(raw, str) or len(raw) > 400 or not raw:
        return False
    p = Path(raw)
    if p.is_absolute() or ".." in p.parts or p.suffix.lower() not in ALLOWED:
        return False
    candidate = root / p
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        return False
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file() or resolved.is_symlink():
        return False
    if any(part.is_symlink() for part in [candidate, *candidate.parents] if part != root and part.is_relative_to(root)):
        return False
    if not 24 <= resolved.stat().st_size <= MAX_BYTES:
        return False
    if image:
        if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            return False
        with resolved.open("rb") as f:
            sig = f.read(12)
        return (sig[:8] == b"\x89PNG\r\n\x1a\n" or sig[:3] == b"\xff\xd8\xff" or
                (sig[:4] == b"RIFF" and sig[8:12] == b"WEBP"))
    return True


def inspect(data: dict, root: Path, *, atlas: dict | None = None) -> dict:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return {"status": "INVALID", "errors": ["Expected schema_version 1 object"]}
    errors: list[str] = []
    missing: list[str] = []
    blockers: list[str] = []
    mode = data.get("mode")
    comp = data.get("component_id")
    surface = data.get("surface")
    if mode not in MODES:
        errors.append("mode invalid")
    if not isinstance(comp, str) or not re.fullmatch(r"[a-z0-9-]{2,60}", comp):
        errors.append("component_id invalid")
    if not isinstance(surface, str) or surface not in {"marketing", "product", "internal", "read", "art", "native"}:
        errors.append("surface invalid")
    if errors:
        return {"status": "INVALID", "errors": errors}
    module = _workplan_module()
    if atlas is None:
        atlas, _ = module.load_atlas()
    recipes = {x["id"]: x for x in atlas["profiles"]}
    if comp not in recipes:
        return {"status": "INVALID", "errors": ["Unknown component_id"]}
    component_router = module._component_router()
    matrix_profiles, _ = component_router.load()
    for profile in matrix_profiles:
        if profile["id"] == comp and surface not in profile["surfaces"]:
            return {"status": "INVALID", "errors": ["Component not valid for surface"]}
    if not isinstance(root, Path) or not root.is_dir():
        return {"status": "INVALID", "errors": ["root must exist"]}
    root = root.resolve()
    phase_ids = recipes[comp]["execution_phases"]
    if mode == "PATCH":
        phase_ids = [p for p in phase_ids if p in ("truth", "ux", "data", "engineering", "accessibility", "render")]
    elif mode == "AUDIT":
        phase_ids = [p for p in phase_ids if p not in ("engineering", "measurement")]
    elif mode == "REFINE":
        phase_ids = [p for p in phase_ids if p != "measurement"]
    stages = data.get("stage_records", [])
    if not isinstance(stages, list) or len(stages) > 35:
        return {"status": "INVALID", "errors": ["stage_records must be list <=35"]}
    stage_map = {}
    for i, stage in enumerate(stages):
        if not isinstance(stage, dict):
            errors.append(f"stage_records[{i}] must be object")
            continue
        name = stage.get("phase_id")
        if not isinstance(name, str) or name not in phase_ids or name in stage_map:
            errors.append(f"Invalid/duplicate phase_id: {name}")
            continue
        stage_map[name] = stage
        state = stage.get("status")
        if state not in STATUSES:
            errors.append(f"{name}: invalid status")
            continue
        if state == "DONE":
            if not _safe_artifact(root, stage.get("evidence_path")):
                missing.append(f"{name}: DONE requires existing artifact evidence_path")
            if not isinstance(stage.get("summary"), str) or len(stage["summary"].strip()) < 20:
                missing.append(f"{name}: DONE requires meaningful summary")
        elif state == "SKIPPED_WITH_REASON":
            if not isinstance(stage.get("reason"), str) or len(stage["reason"].strip()) < 20:
                errors.append(f"{name}: skip requires substantive reason")
            # Missing capability is an honest warning but not evidence of completion.
            if name in {"truth", "engineering", "accessibility", "render"} and mode != "AUDIT":
                missing.append(f"{name}: critical stage not executed")
        else:
            missing.append(f"{name}: NOT_STARTED")
    for phase in phase_ids:
        if phase not in stage_map:
            missing.append(phase + ": no stage record")
    expert_log = data.get("expert_application_log", [])
    if not isinstance(expert_log, list) or len(expert_log) > 100:
        errors.append("expert_application_log invalid")
        expert_log = []
    expert_ids = set()
    for i, entry in enumerate(expert_log):
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            errors.append(f"expert_application_log[{i}] invalid")
            continue
        name = entry["id"]
        if name in expert_ids:
            errors.append("duplicate expert status: " + name)
        expert_ids.add(name)
        if entry.get("status") not in EXPERT_STATUSES:
            errors.append("invalid expert status: " + name)
        if entry.get("status") in {"APPLIED", "REFERENCED"} and not _safe_artifact(root, entry.get("evidence_path")):
            missing.append(name + ": applied/referenced without evidence_path")
        if entry.get("status") == "APPLIED" and not isinstance(entry.get("specific_contribution"), str):
            missing.append(name + ": applied without specific contribution")
    visual = data.get("visual_artifacts", {})
    if not isinstance(visual, dict):
        errors.append("visual_artifacts invalid")
        visual = {}
    if mode in {"REFINE", "REDESIGN", "REBUILD"}:
        for key in ("desktop_after", "mobile_after"):
            if not _safe_artifact(root, visual.get(key), image=True):
                missing.append("visual_artifacts." + key + " missing/invalid")
        if mode in {"REFINE", "REDESIGN"} and not _safe_artifact(root, visual.get("before"), image=True):
            missing.append("visual_artifacts.before missing/invalid")
    if mode == "AUDIT" and not _safe_artifact(root, visual.get("before"), image=True):
        missing.append("visual_artifacts.before unavailable for audit")
    flows = data.get("critical_flows", [])
    if not isinstance(flows, list) or len(flows) > 30:
        errors.append("critical_flows invalid")
        flows = []
    if mode != "AUDIT" and not flows:
        missing.append("No critical flow recorded")
    for i, f in enumerate(flows):
        if not isinstance(f, dict) or not isinstance(f.get("id"), str) or f.get("status") not in FLOW_STATES:
            errors.append(f"critical_flows[{i}] invalid")
            continue
        if f["status"] == "TESTED_FAIL":
            blockers.append(f["id"] + ": tested flow failed")
        elif f["status"] == "NOT_TESTED":
            missing.append(f["id"] + ": flow not tested")
        elif not _safe_artifact(root, f.get("evidence_path")):
            missing.append(f["id"] + ": TESTED_PASS needs test evidence artifact")
    editorial = data.get("editorial_review", {})
    if not isinstance(editorial, dict) or editorial.get("status") not in EDITORIAL_STATES:
        errors.append("editorial_review.status invalid")
    else:
        if editorial["status"] in {"HUMAN_REVIEWED", "INDEPENDENT_REVIEW"} and not _safe_artifact(root, editorial.get("evidence_path")):
            missing.append("editorial: declared independent/human review without artifact")
        if mode in {"REFINE", "REDESIGN", "REBUILD"} and "editorial" in phase_ids and editorial["status"] == "NOT_REVIEWED":
            missing.append("editorial not reviewed")
    issues = data.get("blocking_issues", [])
    if not isinstance(issues, list) or not all(isinstance(v, str) and v.strip() for v in issues):
        errors.append("blocking_issues must be list of strings")
    else:
        blockers.extend(issues)
    research_path = data.get("research_packet")
    if "market" in phase_ids and mode in {"REDESIGN", "REBUILD"}:
        research_status = stage_map.get("market", {}).get("status")
        if research_status == "DONE":
            if not _safe_artifact(root, research_path) or Path(research_path).suffix != ".json":
                missing.append("market DONE requires existing JSON research_packet")
            else:
                try:
                    j = json.loads((root / research_path).read_text(encoding="utf-8"))
                    spec = importlib.util.spec_from_file_location("component_research_gate_check", HERE / "component_research_gate.py")
                    m = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(m)
                    review = m.inspect(j, root)
                    if review["status"] == "INVALID":
                        errors.append("research_packet structurally INVALID: " + "; ".join(review["errors"]))
                    elif review["status"] != "READY_FOR_HUMAN_REVIEW":
                        missing.append("research_packet incomplete: " + "; ".join(review.get("missing_evidence", [])))
                except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                    errors.append("research_packet unreadable: " + str(exc))
    status = "INVALID" if errors else ("BLOCKED" if blockers else
             "NEEDS_EVIDENCE" if missing else "READY_FOR_HUMAN_REVIEW")
    return {
        "status": status, "component_id": comp, "mode": mode, "surface": surface,
        "recorded_phases": len(stage_map), "required_phases": phase_ids,
        "blockers": blockers, "errors": errors, "missing_evidence": missing,
        "limitations": [
            "This gate verifies presence/structure of declared evidence only, not its truth, meaning, creative quality or origin.",
            "A screenshot signature is not proof of accurate visual contents or rights.",
            "Even READY_FOR_HUMAN_REVIEW is NOT human approval, usability study, WCAG certification or conversion lift."
        ]
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    p.add_argument("--root", required=True, type=Path)
    args = p.parse_args()
    try:
        if args.packet.is_symlink() or not args.packet.is_file() or args.packet.stat().st_size > 250_000:
            raise ValueError("Missing or oversized packet")
        root = args.root.resolve(strict=True)
        result = inspect(json.loads(args.packet.read_text(encoding="utf-8")), root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "INVALID":
        raise SystemExit(2)
    if result["status"] in {"BLOCKED", "NEEDS_EVIDENCE"}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
