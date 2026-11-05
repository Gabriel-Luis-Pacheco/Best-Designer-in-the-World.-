#!/usr/bin/env python3
"""Check local asset inventory, attribution and canonical identity integrity.

This validates supplied provenance records; it does not verify third-party rights.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RIGHTS = {"owned", "licensed", "public_domain", "permission", "generated", "unknown"}
ROLES = {"logo", "mascot", "product", "hero", "editorial", "motion", "3d", "font", "icon", "other"}


def inspect(data: dict, root: Path) -> dict:
    errors, unknown, inspected = [], [], []
    root = root.resolve(strict=True)
    assets = data.get("assets") if isinstance(data, dict) else None
    if not isinstance(assets, list) or not assets:
        return {"status": "INVALID", "errors": ["assets must be a nonempty array"], "unknown": []}
    ids = set()
    for asset in assets:
        if not isinstance(asset, dict):
            errors.append("Asset must be an object")
            continue
        aid = asset.get("id")
        if not isinstance(aid, str) or not aid.strip() or aid in ids:
            errors.append("Asset ids must be unique nonempty strings")
            continue
        ids.add(aid)
        role, rights = asset.get("role"), asset.get("rights")
        if role not in ROLES:
            errors.append(aid + ": unknown asset role")
        if rights not in RIGHTS:
            errors.append(aid + ": rights must use an explicit status")
        elif rights == "unknown":
            unknown.append(aid + ": rights not established")
        source = asset.get("source")
        if not isinstance(source, str) or len(source.strip()) < 4:
            errors.append(aid + ": require source, author or generation record")
        if rights in {"licensed", "permission"} and not asset.get("rights_evidence"):
            unknown.append(aid + ": missing license/permission evidence")
        if rights == "generated" and not asset.get("generation_record"):
            unknown.append(aid + ": generated asset lacks model/prompt provenance")
        paths = asset.get("paths")
        if not isinstance(paths, list) or not paths:
            errors.append(aid + ": paths must contain at least one local file")
            continue
        for rel in paths:
            if not isinstance(rel, str) or not rel.strip():
                errors.append(aid + ": invalid relative path")
                continue
            candidate = root / rel
            full = candidate.resolve()
            if not full.is_relative_to(root) or candidate.is_symlink() or not full.is_file():
                errors.append(aid + ": path outside root, symlink or missing file: " + rel)
                continue
            if full.stat().st_size == 0:
                errors.append(aid + ": empty asset: " + rel)
                continue
            digest = hashlib.sha256(full.read_bytes()).hexdigest()
            inspected.append({"id": aid, "path": rel, "sha256": digest, "bytes": full.stat().st_size})
            if asset.get("canonical"):
                expected = asset.get("canonical_sha256")
                if not isinstance(expected, str) or len(expected) != 64:
                    errors.append(aid + ": canonical assets need known original SHA-256")
                elif digest != expected:
                    errors.append(aid + ": canonical asset differs from recorded original: " + rel)
        if role in {"mascot", "logo"} and not asset.get("canonical"):
            unknown.append(aid + ": identity review required for noncanonical brand asset")
    status = "INVALID" if errors else "PROVENANCE_REVIEW_REQUIRED" if unknown else "INVENTORY_READY_FOR_RIGHTS_REVIEW"
    return {"status": status, "errors": errors, "unknown": unknown, "inspected": inspected,
            "limitations": [
                "Self-declared rights cannot establish ownership, licensing or copyright clearance",
                "Matching hashes confirm bytes only, not visual appropriateness or faithful identity",
                "Generated asset provenance does not automatically confer downstream commercial rights",
            ]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.manifest.stat().st_size > 200_000:
            raise ValueError("Manifest exceeds 200 KB")
        report = inspect(json.loads(args.manifest.read_text(encoding="utf-8")), args.root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"INVALID INPUT: {exc}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "INVENTORY_READY_FOR_RIGHTS_REVIEW":
        parser.exit(2)


if __name__ == "__main__":
    main()
