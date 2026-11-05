#!/usr/bin/env python3
"""Validate a real production evidence packet before anyone claims readiness.

The packet can prove files/check reports exist, not that screenshots look good
or that an untrusted PASS assertion is true. A human must examine the evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

MODES = {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}
STATUS = {"PASS", "FAIL", "UNKNOWN"}
REQUIRED_SCENES = {"opening", "middle", "closing"}
CORE_CHECKS = {"build", "primary_flow", "mobile", "keyboard"}
EXPERIENCE_CHECKS = {"reduced_motion", "scene_interaction"}


def artifact(root: Path, name: str, *, png: bool = False) -> dict:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Artifact path must be nonempty")
    path = (root / name).resolve()
    if not path.is_relative_to(root) or not path.is_file() or path.is_symlink():
        raise ValueError("Artifact must be a regular file inside evidence root: " + name)
    data = path.read_bytes()
    if not data or len(data) > 30_000_000:
        raise ValueError("Artifact must be nonempty and at most 30 MB: " + name)
    out = {"path": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    if png:
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 33 or data[12:16] != b"IHDR":
            raise ValueError("Expected actual PNG header: " + name)
        width, height = struct.unpack(">II", data[16:24])
        if width < 1 or height < 1 or width > 12000 or width * height > 250_000_000:
            raise ValueError("Invalid PNG dimensions: " + name)
        out["width"], out["height"] = width, height
    return out


def inspect(packet: dict, root: Path) -> dict:
    root = root.resolve(strict=True)
    errors, warnings, observed = [], [], []
    if not isinstance(packet, dict):
        return {"status": "INVALID", "errors": ["Packet must be an object"], "warnings": []}
    mode, surface = packet.get("mode"), packet.get("surface")
    if mode not in MODES:
        errors.append("mode must be PATCH/AUDIT/REFINE/REDESIGN/REBUILD")
    if not isinstance(surface, str) or not surface.strip():
        errors.append("surface must be supplied")
    significant = mode in {"REDESIGN", "REBUILD"}
    expressive = surface in {"ART", "EXPERIENCE", "EXPERIENTIAL_COMMERCE", "art", "experience", "experiential_commerce"}
    scenes = packet.get("scenes", [])
    if not isinstance(scenes, list):
        errors.append("scenes must be an array")
        scenes = []
    scene_ids = set()
    for scene in scenes:
        if not isinstance(scene, dict) or not isinstance(scene.get("id"), str):
            errors.append("Each scene requires a string id")
            continue
        sid = scene["id"]
        if sid in scene_ids:
            errors.append("Duplicate scene id: " + sid)
        scene_ids.add(sid)
        if not isinstance(scene.get("purpose"), str) or len(scene["purpose"].strip()) < 12:
            errors.append(sid + ": explain why this scene exists")
        for viewport in ("desktop", "mobile"):
            name = scene.get(viewport)
            if not name:
                if significant:
                    errors.append(sid + ": missing " + viewport + " screenshot")
                continue
            try:
                observed.append(artifact(root, name, png=True))
            except ValueError as exc:
                errors.append(str(exc))
    if significant:
        missing = REQUIRED_SCENES - scene_ids
        if missing:
            errors.append("Missing opening/middle/closing scenes: " + ", ".join(sorted(missing)))
    checks = packet.get("checks", [])
    if not isinstance(checks, list):
        errors.append("checks must be an array")
        checks = []
    check_ids = set()
    failed = []
    unknown = []
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get("id"), str):
            errors.append("Each check needs an id")
            continue
        cid = check["id"]
        if cid in check_ids:
            errors.append("Duplicate check id: " + cid)
        check_ids.add(cid)
        status = check.get("status")
        if status not in STATUS:
            errors.append(cid + ": use PASS/FAIL/UNKNOWN")
            continue
        if status == "FAIL":
            failed.append(cid)
        if status == "UNKNOWN":
            unknown.append(cid)
            if not isinstance(check.get("reason"), str) or len(check["reason"].strip()) < 8:
                errors.append(cid + ": UNKNOWN requires a reason")
        if status == "PASS":
            evidence = check.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(cid + ": PASS requires real artifact paths")
            else:
                for name in evidence:
                    try:
                        observed.append(artifact(root, name))
                    except ValueError as exc:
                        errors.append(str(exc))
    if significant:
        required = CORE_CHECKS | (EXPERIENCE_CHECKS if expressive else set())
        absent = required - check_ids
        if absent:
            errors.append("Missing required check declarations: " + ", ".join(sorted(absent)))
        if expressive and not isinstance(packet.get("motion_fallback"), str):
            errors.append("Expressive experiences must describe a non-motion fallback")
        iteration = packet.get("iteration")
        if not isinstance(iteration, dict):
            errors.append("REDESIGN/REBUILD needs the rendered weakest-link correction")
        else:
            if iteration.get("scene_id") not in scene_ids:
                errors.append("Iteration scene_id must match a captured scene")
            if not isinstance(iteration.get("cause"), str) or len(iteration["cause"].strip()) < 12:
                errors.append("Iteration needs a causal diagnosis")
            if not isinstance(iteration.get("change"), str) or len(iteration["change"].strip()) < 12:
                errors.append("Iteration needs a material change description")
            try:
                before = artifact(root, iteration.get("before"), png=True)
                after = artifact(root, iteration.get("after"), png=True)
                observed.extend((before, after))
                if before["width"] != after["width"]:
                    errors.append("Iteration screenshots must have equal width")
                if before["sha256"] == after["sha256"]:
                    errors.append("Iteration screenshots are identical; no visual change evidenced")
            except ValueError as exc:
                errors.append(str(exc))
    for blocker in packet.get("blockers", []):
        if not isinstance(blocker, dict) or blocker.get("severity") not in {"P0", "P1", "P2"}:
            errors.append("Blockers must identify severity P0/P1/P2")
        elif blocker["severity"] in {"P0", "P1"}:
            failed.append("blocker " + blocker["severity"])
    if not errors and not failed:
        warnings.append("PASS is only a supplied assertion; check contents and runtime independently")
        warnings.append("Visual/aesthetic quality and commercial impact remain UNVERIFIED")
    state = ("INVALID" if errors else "BLOCKED" if failed else
             "INCOMPLETE_UNKNOWN" if unknown else "EVIDENCE_READY_FOR_HUMAN_REVIEW")
    return {"status": state, "errors": errors, "failed": failed, "unknown": unknown,
            "artifact_count": len(observed), "warnings": warnings,
            "limitations": "File/header checks cannot authenticate screenshots, reviewer independence, usability or quality"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.packet.stat().st_size > 200_000:
            raise ValueError("Packet exceeds 200 KB")
        result = inspect(json.loads(args.packet.read_text(encoding="utf-8")), args.root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"INVALID INPUT: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "EVIDENCE_READY_FOR_HUMAN_REVIEW":
        parser.exit(2)


if __name__ == "__main__":
    main()
