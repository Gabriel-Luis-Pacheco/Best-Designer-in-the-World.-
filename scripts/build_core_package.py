#!/usr/bin/env python3
"""Build a deterministic standalone CORE zip from this checkout.

This keeps every original vendored source in Git; the core distribution excludes
vendor/ and is documented as a smaller, intentionally limited package. It does
not install upstream CLIs, copy third-party licenses, or promise parity with FULL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_REL = Path("skills/studio-grade-web-transformation")
IGNORED_PARTS = {"vendor", "__pycache__", "node_modules", ".git", "test-results", "dist"}
TIMESTAMP = (2026, 11, 19, 0, 0, 0)

def build_archive(root: Path, output: Path) -> dict:
    root = root.resolve()
    skill = root / SKILL_REL
    if not (skill / "SKILL.md").is_file():
        raise ValueError("Missing studio-grade-web-transformation/SKILL.md")
    # Avoid accidentally putting the archive inside the package source.
    output = output.resolve()
    if output.is_relative_to(skill.resolve()):
        raise ValueError("Output archive cannot be inside the packaged skill")
    members = []
    for src in sorted(skill.rglob("*")):
        rel = src.relative_to(skill)
        if any(part in IGNORED_PARTS for part in rel.parts):
            continue
        if src.is_symlink():
            raise ValueError("Refusing symlink in core package: " + str(rel))
        if not src.is_file() or src.suffix in (".pyc", ".pyo"):
            continue
        data = src.read_bytes()
        members.append((SKILL_REL / rel, data))
    license_file = root / "LICENSE"
    if license_file.is_file():
        members.append((Path("LICENSE"), license_file.read_bytes()))
    entries = [{"path": str(rel).replace(os.sep, "/"),
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
               for rel, data in sorted(members, key=lambda x: x[0].as_posix())]
    manifest = {"schema_version": 1, "distribution": "core",
                "skill": SKILL_REL.name,
                "vendored_sources_included": False,
                "important_limitations": [
                    "Excludes all third-party vendor/ mirrors and optional upstream executables",
                    "Some external-specialist paths mentioned in guides will not exist",
                    "No benchmark or model comparison has been executed by this archive"
                ], "files": entries}
    output.parent.mkdir(parents=True, exist_ok=True)
    # Fixed timestamps/order make identical inputs generate byte-identical ZIPs.
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=8) as archive:
        for rel, data in sorted(members, key=lambda x: x[0].as_posix()):
            info = ZipInfo(rel.as_posix(), TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=8)
        info = ZipInfo("PACKAGE_MANIFEST.json", TIMESTAMP)
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
                         compress_type=ZIP_DEFLATED, compresslevel=8)
    return {"output": str(output), "files": len(entries), "bytes": output.stat().st_size,
            "vendors_included": False}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPOSITORY / "dist/design-os-prime-core.zip")
    args = parser.parse_args()
    print(json.dumps(build_archive(REPOSITORY, args.output), indent=2))

if __name__ == "__main__":
    main()
