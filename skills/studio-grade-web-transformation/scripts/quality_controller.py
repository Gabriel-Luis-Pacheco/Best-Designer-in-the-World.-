#!/usr/bin/env python3
"""One proportionate evidence audit across the portable Design OS quality gates.

Does not render the site, dispatch subagents, verify external rights, or certify
aesthetic quality. Every missing/invalid proof remains visible.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODES = {"PATCH", "AUDIT", "REFINE", "REDESIGN", "REBUILD"}
COMMERCIAL = {"landing", "marketing", "commerce", "experiential_commerce"}
ART = {"art", "experience", "experiential_commerce"}


def _module(name: str):
    spec = importlib.util.spec_from_file_location("quality_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise ValueError("Missing portable validator: " + name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _safe_path(root: Path, relative: str, directory: bool = False) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("Expected safe relative path, got: " + repr(relative))
    raw = root / relative
    path = raw.resolve()
    if not path.is_relative_to(root) or raw.is_symlink():
        raise ValueError("Path escapes project root or links elsewhere: " + relative)
    if directory:
        if not path.is_dir():
            raise ValueError("Missing directory: " + relative)
    elif not path.is_file() or path.is_symlink():
        raise ValueError("Missing or symlinked file: " + relative)
    return path


def _json(root: Path, relative: str) -> dict:
    path = _safe_path(root, relative)
    if path.stat().st_size > 250_000:
        raise ValueError("JSON contract exceeds 250 KB: " + relative)
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("Expected JSON object: " + relative)
    return obj


def _file_report(root: Path, rel: str) -> dict:
    path = _safe_path(root, rel)
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return {"path": rel, "sha256": h.hexdigest(), "bytes": path.stat().st_size}


def inspect(config: dict, root: Path) -> dict:
    errors, blockers, missing, warnings, gates, review_needed = [], [], [], [], [], []
    if not isinstance(config, dict):
        return {"status": "INVALID", "errors": ["Config must be a JSON object"]}
    root = root.resolve(strict=True)
    mode, surface = config.get("mode"), config.get("surface")
    if not isinstance(mode, str) or mode not in MODES:
        errors.append("mode must be PATCH/AUDIT/REFINE/REDESIGN/REBUILD")
    if not isinstance(surface, str) or not surface.strip():
        errors.append("surface must be nonempty")
        surface = "unknown"
    surface = surface.casefold()
    public = config.get("public")
    if not isinstance(public, bool):
        errors.append("public must explicitly be true/false; do not infer indexability")
        public = False
    major = isinstance(mode, str) and mode in {"REDESIGN", "REBUILD"}
    required = {
        "brief": major,
        "production": major,
        "reviews": major,
        "positioning": major and surface in COMMERCIAL,
        "assets": config.get("named_reference_required") is True,
        "cinematic": config.get("cinematic_required") is True,
    }
    if not isinstance(config.get("named_reference_required", False), bool) or not isinstance(
            config.get("cinematic_required", False), bool):
        errors.append("named_reference_required and cinematic_required must be booleans")

    def register(name, status, details=None):
        gates.append({"gate": name, "status": status, "details": details})
        if status == "REVIEW_NEEDED":
            review_needed.append(name)
        if status == "INVALID":
            errors.append(name + ": invalid evidence")
        elif status == "BLOCKED":
            blockers.append(name + ": critical requirements or failures remain")
        elif status in {"MISSING", "UNKNOWN", "INCOMPLETE"}:
            missing.append(name + ": " + status)

    for key in ("brief", "production", "reviews", "positioning", "assets", "cinematic"):
        rel = config.get(key)
        if not rel:
            if required[key]:
                register(key, "MISSING", "Required for this release scope")
            continue
        try:
            data = _json(root, rel)
            if key == "brief":
                raw = _module("brief_alignment").inspect(data)
                register(key, {
                    "INVALID": "INVALID", "BLOCKED": "BLOCKED",
                    "NOT_VERIFIED": "INCOMPLETE",
                    "READY_FOR_HUMAN_REVIEW": "REVIEW_NEEDED",
                }.get(raw["status"], "UNKNOWN"), raw)
            elif key == "production":
                ev_root = _safe_path(root, config.get("evidence_root", "evidence"), directory=True)
                raw = _module("production_evidence").inspect(data, ev_root)
                register(key, {
                    "INVALID": "INVALID", "BLOCKED": "BLOCKED",
                    "INCOMPLETE_UNKNOWN": "INCOMPLETE",
                    "EVIDENCE_READY_FOR_HUMAN_REVIEW": "REVIEW_NEEDED",
                }.get(raw["status"], "UNKNOWN"), raw)
            elif key == "reviews":
                raw = _module("review_council").inspect(data)
                review_status = {
                    "INVALID": "INVALID", "BLOCKED": "BLOCKED",
                    "ASSIGNMENTS_ONLY": "INCOMPLETE", "INCOMPLETE": "INCOMPLETE",
                    "REVIEWED_NOT_CERTIFIED": "REVIEW_NEEDED",
                }.get(raw["status"], "UNKNOWN")
                if review_status == "REVIEW_NEEDED":
                    # Require real local evidence bytes for critic signoffs;
                    # timestamps and agent independence still need human audit.
                    ev_root = _safe_path(root, config.get("evidence_root", "evidence"), directory=True)
                    checked, unchecked = [], []
                    for entry in data.get("reviews", []):
                        references = list(entry.get("inspected_evidence", []))
                        for finding in entry.get("findings", []):
                            references += finding.get("evidence", [])
                            if finding.get("resolution") == "VERIFIED_FIXED":
                                references += finding.get("fix_evidence", [])
                        for rel in references:
                            if rel.startswith(("http://", "https://", "route:")):
                                unchecked.append(rel)
                            else:
                                checked.append(_file_report(ev_root, rel))
                    if unchecked or not checked:
                        review_status = "INCOMPLETE"
                    raw["local_evidence_files_checked"] = checked
                    raw["unverified_external_or_route_refs"] = unchecked
                    warnings.append("Verified file bytes do not prove reviewer independence, factual accuracy or visual quality")
                register(key, review_status, raw)
            elif key == "positioning":
                raw = _module("positioning_copy_contract").inspect(data)
                register(key, {"INVALID": "INVALID", "PROOF_GAPS": "INCOMPLETE",
                               "READY_FOR_HUMAN_COPY_TEST": "REVIEW_NEEDED"}.get(raw["status"], "UNKNOWN"), raw)
            elif key == "assets":
                asset_root = _safe_path(root, config.get("asset_root", "."), directory=True)
                raw = _module("asset_provenance").inspect(data, asset_root)
                register(key, {
                    "INVALID": "INVALID", "PROVENANCE_REVIEW_REQUIRED": "INCOMPLETE",
                    "INVENTORY_READY_FOR_RIGHTS_REVIEW": "REVIEW_NEEDED",
                }.get(raw["status"], "UNKNOWN"), raw)
            elif key == "cinematic":
                raw = _module("cinematic_timeline").inspect(data)
                register(key, "INVALID" if raw["status"] == "INVALID" else "REVIEW_NEEDED", raw)
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            register(key, "INVALID", str(exc))
    pages = config.get("html_pages", [])
    if not isinstance(pages, list) or any(not isinstance(p, str) for p in pages):
        errors.append("html_pages must be a list of safe relative HTML files")
        pages = []
    if public:
        if not pages:
            register("public_seo", "MISSING", "No public rendered/HTML pages supplied")
        else:
            try:
                if len(pages) > 80:
                    raise ValueError("At most 80 HTML pages")
                sources = {}
                for rel in pages:
                    path = _safe_path(root, rel)
                    if path.stat().st_size > 4_000_000:
                        raise ValueError("HTML page exceeds 4 MB: " + rel)
                    sources[rel] = path.read_text(encoding="utf-8")
                raw = _module("search_presence_audit").inspect(sources, public=True)
                counts = raw.get("counts", {})
                status = ("INVALID" if raw["status"] == "INVALID" else
                          "BLOCKED" if counts.get("P0", 0) else
                          "INCOMPLETE" if counts.get("P1", 0) else
                          "REVIEW_NEEDED")
                register("public_seo", status, raw)
                warnings.append("Static SEO does not verify live HTTP, crawling, robots.txt, indexing or Search Console")
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                register("public_seo", "INVALID", str(exc))
    elif pages:
        warnings.append("Internal/private pages do not require public SEO; no search claim was made")

    if not gates:
        missing.append("No gate executed; empty checklist cannot certify readiness")
    if errors:
        status = "INVALID"
    elif blockers:
        status = "BLOCKED"
    elif missing:
        status = "INCOMPLETE"
    else:
        status = "EVIDENCE_PACKET_FOR_HUMAN_REVIEW"
    return {
        "status": status,
        "scope": {"mode": mode, "surface": surface, "public": public},
        "gates": gates, "errors": errors, "blockers": blockers,
        "unverified_or_missing": missing, "human_review_required": review_needed, "warnings": warnings,
        "limitations": [
            "No source-derived gate authenticates independent reviewers or input truth",
            "No browser was launched by this command",
            "No visual aesthetics, verified rights, search ranking, conversion or user comprehension certified",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        if args.manifest.stat().st_size > 250_000:
            raise ValueError("Manifest exceeds 250 KB")
        result = inspect(json.loads(args.manifest.read_text(encoding="utf-8")), root)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(2, "INVALID INPUT: " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "EVIDENCE_PACKET_FOR_HUMAN_REVIEW":
        parser.exit(2)


if __name__ == "__main__":
    main()
