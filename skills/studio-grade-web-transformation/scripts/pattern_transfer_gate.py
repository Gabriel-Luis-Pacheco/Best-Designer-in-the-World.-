#!/usr/bin/env python3
"""Structural guard for evidence-calibrated competitor pattern transfer.

No website access, test execution, business result verification, user research,
skill invocation or visual quality scoring. A ready packet only warrants review.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODES = {"REDESIGN", "REBUILD"}
DECISIONS = {"ADOPT", "ADAPT", "REJECT"}
LEVELS = {"OBSERVED_ONLY", "INDEPENDENT_RESEARCH", "PUBLISHED_RESULT", "OWN_VERIFIED_TEST"}


def _research_gate():
    spec = importlib.util.spec_from_file_location("pattern_transfer_research", HERE / "component_research_gate.py")
    if spec is None or spec.loader is None:
        raise ValueError("Research evidence validator missing")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _atlas():
    p = ROOT / "research/component_execution_atlas.json"
    if not p.is_file() or p.is_symlink() or p.stat().st_size > 230_000:
        raise ValueError("Atlas unavailable")
    j = json.loads(p.read_text(encoding="utf-8"))
    if j.get("schema_version") != 1:
        raise ValueError("Unknown atlas schema")
    return {r["id"]: r for r in j["profiles"] if r.get("benchmark_transfer")}


def _path(root: Path, raw: object) -> Path | None:
    if not isinstance(raw, str) or not raw or len(raw) > 400 or "\\" in raw:
        return None
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts or rel.suffix.lower() not in {".json", ".md", ".txt"}:
        return None
    try:
        base = root.resolve(strict=True)
        path = (base / rel).resolve(strict=True)
    except OSError:
        return None
    if not path.is_relative_to(base) or not path.is_file() or path.is_symlink():
        return None
    if not 10 <= path.stat().st_size <= 250_000:
        return None
    return path


def _jsonfile(root: Path, raw: object) -> dict | None:
    path = _path(root, raw)
    if path is None or path.suffix != ".json":
        return None
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    return obj if isinstance(obj, dict) else None


def _good_text(value: object, n: int = 20) -> bool:
    return isinstance(value, str) and n <= len(value.strip()) <= 3000


def _normalized_url(url: str) -> str:
    return url.strip().rstrip("/").lower()


def _https(url: object) -> bool:
    if not isinstance(url, str) or len(url) > 2048:
        return False
    try:
        p = urlsplit(url)
    except ValueError:
        return False
    return p.scheme == "https" and bool(p.hostname) and not p.username and not p.password


def inspect(data: dict, root: Path, research: dict | None = None) -> dict:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return {"status": "INVALID", "errors": ["schema_version must be 1"]}
    errors: list[str] = []
    missing: list[str] = []
    warnings: list[str] = []
    comp, mode = data.get("component_id"), data.get("mode")
    if comp not in _atlas():
        errors.append("Unknown or non-prioritized component_id")
    if mode not in MODES:
        errors.append("Only REDESIGN/REBUILD transfer decisions are evaluated")
    if not _good_text(data.get("audience_job")):
        missing.append("audience_job must describe the target user's real task")
    if not isinstance(root, Path) or not root.is_dir():
        return {"status": "INVALID", "errors": ["Evidence root unavailable"]}
    root = root.resolve()
    if research is None:
        research = _jsonfile(root, data.get("research_packet"))
    if not isinstance(research, dict):
        missing.append("real existing research_packet JSON required")
        research = {}
    else:
        if research.get("schema_version") != 1:
            errors.append("research_packet schema_version mismatch")
        if research.get("component_id") != comp:
            errors.append("research_packet component_id does not match transfer")
        if research.get("mode") != mode:
            errors.append("research_packet mode differs from transfer")
    refs = research.get("references", [])
    if not isinstance(refs, list):
        errors.append("research references must be an array")
        refs = []
    source_map: dict[str, dict] = {}
    observed = 0
    usable_captures = 0
    first_party = 0
    check = _research_gate()
    for i, item in enumerate(refs):
        if not isinstance(item, dict) or not _https(item.get("url")):
            continue
        ident = _normalized_url(item["url"])
        if ident in source_map:
            errors.append("Duplicate research reference URL: " + ident)
        source_map[ident] = item
        state = item.get("inspection_status")
        if state in {"CAPTURED", "INSPECTED_NO_CAPTURE"}:
            observed += 1
            valid_capture = any(
                check.safe_file(root, item.get(field)) for field in ("desktop_capture", "mobile_capture")
            )
            usable_captures += int(valid_capture)
            if item.get("kind") in {"DIRECT", "SUBSTITUTE"} and valid_capture:
                first_party += 1
    decisions = data.get("candidate_patterns", [])
    if not isinstance(decisions, list) or len(decisions) > 50:
        errors.append("candidate_patterns must be an array <=50")
        decisions = []
    if not decisions:
        missing.append("At least one observed/justified pattern decision required")
    relevant = 0
    kinds: dict[str, int] = {}
    for i, row in enumerate(decisions):
        tag = f"candidate_patterns[{i}]"
        if not isinstance(row, dict):
            errors.append(tag + " must be object")
            continue
        url = row.get("source_url")
        if not _https(url):
            errors.append(tag + ": source_url must be HTTPS")
            continue
        source = source_map.get(_normalized_url(url))
        if source is None:
            errors.append(tag + ": source_url absent from actual research packet")
        elif source.get("inspection_status") == "NOT_INSPECTED":
            errors.append(tag + ": cannot claim mechanism observed from uninspected source")
        for field in ("source_step", "mechanism", "fit_rationale",
                      "original_implementation", "known_risk", "test_plan"):
            if not _good_text(row.get(field)):
                missing.append(tag + ": substantive " + field + " required")
        level = row.get("evidence_level")
        decision = row.get("decision")
        if level not in LEVELS:
            errors.append(tag + ": evidence_level invalid")
        else:
            kinds[level] = kinds.get(level, 0) + 1
        if decision not in DECISIONS:
            errors.append(tag + ": decision must be ADOPT/ADAPT/REJECT")
        elif decision in {"ADOPT", "ADAPT"}:
            relevant += 1
        if level == "OBSERVED_ONLY" and (
            row.get("reported_result") or row.get("conversion_lift")
            or row.get("validated_claim") or row.get("study_url")
        ):
            errors.append(tag + ": an observed competitor UI cannot claim validated conversion or study results")
        if level in {"INDEPENDENT_RESEARCH", "PUBLISHED_RESULT"}:
            if not _https(row.get("study_url")) or not _good_text(row.get("reported_scope"), 30):
                missing.append(tag + ": study URL and observed research scope required")
            if level == "PUBLISHED_RESULT" and (
                not _good_text(row.get("reported_result"), 30)
                or not _good_text(row.get("reported_population_and_period"), 30)
            ):
                missing.append(tag + ": published metric, population and period required")
        if level == "OWN_VERIFIED_TEST":
            if not _path(root, row.get("own_evidence_artifact")) or not _good_text(
                row.get("reported_population_and_period"), 30
            ):
                missing.append(tag + ": own measured test requires real artifact and population/period")
    if not relevant:
        missing.append("No candidate pattern selected for ADOPT or ADAPT; state the fallback and test rationale")
    if not observed:
        missing.append("No comparable source inspected; cannot claim a competitor pattern baseline")
    if usable_captures == 0:
        missing.append("No intact real competitor screenshot in the referenced research packet")
    if first_party == 0:
        missing.append("No intact direct-competitor/substitute flow captured")
    if not _good_text(data.get("baseline_choice"), 30):
        missing.append("baseline_choice must explain the selected familiar pattern and why")
    if not _good_text(data.get("own_validation_plan"), 30):
        missing.append("own_validation_plan required: first-value/completion and relevant guardrails")
    limit = data.get("benchmark_access_limitation")
    if limit is not None and limit != "" and not _good_text(limit, 30):
        errors.append("benchmark_access_limitation must be substantive")
    if comp in _atlas():
        desired = _atlas()[comp]["benchmark_transfer"]["reference_target"]
    else:
        desired = None
    if desired is not None and usable_captures < desired and not limit:
        missing.append(
            f"Captured {usable_captures} of {desired} target benchmarks; provide evidence or a substantive benchmark_access_limitation"
        )
    if usable_captures < 3:
        warnings.append("Small comparison set: observed patterns are hypotheses, not measured conversion evidence")
    status = "INVALID" if errors else ("NEEDS_EVIDENCE" if missing else "READY_FOR_HUMAN_REVIEW")
    return {
        "status": status,
        "component_id": comp,
        "reference_target": desired,
        "inspected_sources": observed,
        "captured_sources": usable_captures,
        "captured_direct_or_substitute": first_party,
        "adopt_or_adapt_decisions": relevant,
        "evidence_levels_declared": kinds,
        "errors": errors,
        "missing_evidence": missing,
        "warnings": warnings,
        "limitations": [
            "URLs and screenshot structures only; no verification of website identity, research validity or image contents.",
            "Observed competitor design is not proof of commercial validation or causality.",
            "A self-reported own result remains a metadata assertion until independently checked.",
            "READY_FOR_HUMAN_REVIEW is not user-study approval, copy quality, WCAG compliance or conversion improvement."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.packet.is_symlink() or args.packet.stat().st_size > 250_000:
            raise ValueError("Packet too large or symlinked")
        root = args.root.resolve(strict=True)
        result = inspect(json.loads(args.packet.read_text(encoding="utf-8")), root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == "INVALID":
        raise SystemExit(2)
    if result["status"] != "READY_FOR_HUMAN_REVIEW":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
