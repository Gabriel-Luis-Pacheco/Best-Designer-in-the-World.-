#!/usr/bin/env python3
"""Validate honesty/completeness of a component reference evidence packet.

NOT a visual-quality, legal-rights, WCAG, conversion or independent-human test.
No network, downloads, executables or external skills.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

VALID_MODES = {"PATCH", "REFINE", "AUDIT", "REDESIGN", "REBUILD"}
KINDS = {"DIRECT", "SUBSTITUTE", "ADJACENT", "CROSS_CATEGORY", "RESEARCH"}
STATES = {"NOT_INSPECTED", "INSPECTED_NO_CAPTURE", "CAPTURED"}
REVIEWS = {"NOT_REVIEWED", "SELF_REVIEW_ONLY", "INDEPENDENT_REVIEW", "HUMAN_REVIEWED"}


@lru_cache(maxsize=1)
def _png_validator():
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "component_reference_png_validator", here / "production_evidence.py")
    if spec is None or spec.loader is None:
        raise ValueError("PNG validator unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.png_dimensions


def safe_file(root: Path, value: str) -> bool:
    if not isinstance(value, str) or not value or len(value) > 400:
        return False
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or p.suffix.lower() != ".png":
        return False
    target = root / p
    if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
        return False
    if not 32 <= target.stat().st_size <= 10_000_000:
        return False
    try:
        # A signature-only test can accept arbitrary bytes with a PNG prefix.
        # The existing validator verifies chunk boundaries, CRC and dimensions.
        _png_validator()(target.read_bytes())
    except (ValueError, OSError):
        return False
    return True



def valid_url(url: str) -> bool:
    if not isinstance(url, str) or len(url) > 2048:
        return False
    obj = urlparse(url)
    return obj.scheme == "https" and bool(obj.netloc) and not obj.username and not obj.password


def inspect(data: dict, root: Path) -> dict:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return {"status": "INVALID", "errors": ["schema_version must be 1"]}
    errors: list[str] = []
    missing: list[str] = []
    component = data.get("component_id")
    mode = data.get("mode")
    if not isinstance(component, str) or not re.fullmatch(r"[a-z0-9-]{2,60}", component):
        errors.append("component_id invalid")
    if mode not in VALID_MODES:
        errors.append("mode invalid")
    refs = data.get("references", [])
    if not isinstance(refs, list) or len(refs) > 100:
        errors.append("references must be an array with at most 100 entries")
        refs = []
    captured = 0
    seen = set()
    for i, item in enumerate(refs):
        tag = f"references[{i}]"
        if not isinstance(item, dict):
            errors.append(tag + " must be object")
            continue
        url = item.get("url")
        if not valid_url(url):
            errors.append(tag + " invalid HTTPS URL")
        elif url.lower().rstrip("/") in seen:
            errors.append(tag + " duplicate URL")
        else:
            seen.add(url.lower().rstrip("/"))
        if item.get("kind") not in KINDS:
            errors.append(tag + " invalid kind")
        state = item.get("inspection_status")
        if state not in STATES:
            errors.append(tag + " inspection_status invalid")
            continue
        has_any_capture = False
        for key in ("desktop_capture", "mobile_capture"):
            value = item.get(key)
            if value is None or value == "":
                continue
            if not safe_file(root, value):
                errors.append(tag + " " + key + " not a real accessible image under root")
            else:
                has_any_capture = True
        mechanism = item.get("observed_mechanism")
        if state == "CAPTURED":
            if not has_any_capture:
                errors.append(tag + " CAPTURED without actual image")
            if not isinstance(mechanism, str) or len(mechanism.strip()) < 12:
                errors.append(tag + " CAPTURED without observed mechanism")
            captured += int(has_any_capture)
        elif state == "NOT_INSPECTED":
            if has_any_capture:
                errors.append(tag + " NOT_INSPECTED contradicts screenshot")
            if isinstance(mechanism, str) and mechanism.strip():
                errors.append(tag + " cannot claim observed mechanism when NOT_INSPECTED")
        elif state == "INSPECTED_NO_CAPTURE":
            if has_any_capture:
                errors.append(tag + " should be CAPTURED if screenshot provided")
        if state != "NOT_INSPECTED" and not item.get("inspection_date"):
            missing.append(tag + " inspection_date")
    decisions = data.get("decisions")
    if not isinstance(decisions, dict):
        errors.append("decisions must be object")
        decisions = {}
    for key in ("selected_mechanism", "original_application", "rejected_options"):
        val = decisions.get(key)
        if key == "rejected_options":
            if not isinstance(val, list) or len(val) < 1:
                missing.append("decisions.rejected_options")
        elif not isinstance(val, str) or len(val.strip()) < 15:
            missing.append("decisions." + key)
    implementation = data.get("implementation", {})
    if not isinstance(implementation, dict):
        errors.append("implementation must be object")
        implementation = {}
    if mode in {"REFINE", "REDESIGN", "REBUILD"}:
        if not implementation.get("changed_files"):
            missing.append("implementation.changed_files")
        for key in ("before_capture", "after_capture"):
            value = implementation.get(key)
            if not value or not safe_file(root, value):
                missing.append("implementation." + key)
        if implementation.get("journey_status") not in {"TESTED_PASS", "TESTED_FAIL", "NOT_TESTED"}:
            missing.append("implementation.journey_status")
    editorial = data.get("editorial", {})
    if not isinstance(editorial, dict) or editorial.get("status") not in REVIEWS:
        errors.append("editorial.status invalid")
    else:
        if editorial["status"] in {"HUMAN_REVIEWED", "INDEPENDENT_REVIEW"} and not editorial.get("review_evidence"):
            errors.append("review cannot be claimed without review_evidence")
        if editorial.get("status") == "NOT_REVIEWED":
            missing.append("editorial review")
    benchmark = data.get("benchmark", {})
    if not isinstance(benchmark, dict):
        errors.append("benchmark must be object")
        benchmark = {}
    target = benchmark.get("target")
    if isinstance(target, bool) or not isinstance(target, int) or not 0 <= target <= 100:
        errors.append("benchmark.target must be integer 0..100")
        target = 0
    if captured < target and target:
        missing.append(f"{target} captured references targeted, only {captured} provided; explain limits")
    if captured < target and not benchmark.get("limitation_reason"):
        missing.append("benchmark.limitation_reason")
    # A string in review_evidence is only a declaration; this script cannot
    # determine whether the human is real or whether their feedback is useful.
    status = "INVALID" if errors else ("NEEDS_EVIDENCE" if missing else "READY_FOR_HUMAN_REVIEW")
    return {
        "status": status, "component_id": component,
        "captured_references": captured, "reference_target": target,
        "errors": errors, "missing_evidence": missing,
        "limitations": [
            "Structural checks are not proof of screenshot content, ownership or observed site identity.",
            "No visual, editorial taste, accessibility or conversion quality is certified.",
            "HUMAN_REVIEWED is reported from supplied metadata; this CLI cannot verify the reviewer."
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.packet.stat().st_size > 250_000 or args.packet.is_symlink():
        parser.error("Invalid/oversized packet")
    try:
        root = args.root.resolve(strict=True)
        data = json.loads(args.packet.read_text(encoding="utf-8"))
        packet = inspect(data, root)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(packet, indent=2, ensure_ascii=False))
    if packet["status"] == "INVALID":
        raise SystemExit(2)
    if packet["status"] == "NEEDS_EVIDENCE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
