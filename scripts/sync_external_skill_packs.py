#!/usr/bin/env python3
"""Mirror 50 complete upstream skill directories, without executing vendor code.

Usage:
  python3 scripts/sync_external_skill_packs.py --validate
  python3 scripts/sync_external_skill_packs.py --sync
  python3 scripts/sync_external_skill_packs.py --check

This is an acquisition tool, not an agent installer. Only public GitHub source
is copied. No upstream install hooks or scripts are executed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "skills/studio-grade-web-transformation/vendor/external-skill-packs"
MANIFEST = DEST / "SOURCES.json"
MAX_FILE_BYTES = 90 * 1024 * 1024  # GitHub rejects individual files >=100 MiB.
MAX_TOTAL_BYTES = 200 * 1024 * 1024


def cmd(*args: str, cwd: Path | None = None, stdin: str | None = None) -> str:
    result = subprocess.run(
        list(args), cwd=cwd, input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        timeout=300,
    )
    if result.returncode:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {list(args[:5])}\n"
            f"{result.stderr[-1800:]}"
        )
    return result.stdout.strip()


def slug(repo: str) -> str:
    return repo.lower().replace("/", "--")


def load_manifest() -> tuple[dict, list[dict]]:
    obj = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = obj["sources"]
    seen: set[str] = set()
    count = 0
    for entry in sources:
        repo = entry["repo"]
        assert repo.count("/") == 1, repo
        assert entry["license"], repo
        for rel in entry["paths"]:
            path = Path(rel)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                raise ValueError(f"Unsafe path {rel!r}")
            key = f"{repo}:{rel}"
            if key in seen:
                raise ValueError(f"Duplicate skill: {key}")
            seen.add(key)
            count += 1
    if count != 50 or count != obj["selected_skill_count"]:
        raise ValueError(f"Expected exactly 50 unique skills, found {count}")
    print(f"Manifest valid: {len(sources)} repositories, {count} skill directories")
    return obj, sources


def local_tree_copy(source: Path, target: Path) -> tuple[int, int]:
    if not source.is_dir():
        raise FileNotFoundError(f"Missing source skill directory: {source}")
    files = 0
    total_bytes = 0
    for entry in sorted(source.rglob("*")):
        if entry.is_symlink():
            raise RuntimeError(f"Symlink in upstream skill refused: {entry}")
        if not entry.is_file():
            continue
        if any(p in {"node_modules", ".git", "__pycache__"} for p in entry.parts):
            continue
        size = entry.stat().st_size
        if size >= MAX_FILE_BYTES:
            raise RuntimeError(f"Too-large upstream file: {entry} ({size} B)")
        relative = entry.relative_to(source)
        target_file = target / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(entry, target_file)
        files += 1
        total_bytes += size
    if files == 0:
        raise RuntimeError(f"No files copied for {source}")
    if not (target / "SKILL.md").is_file():
        raise RuntimeError(f"Missing SKILL.md under {source}")
    return files, total_bytes


def sync(sources: list[dict]) -> None:
    with tempfile.TemporaryDirectory(prefix="vendor-skill-packs-") as tmp:
        scratch = Path(tmp)
        staged = scratch / "new-pack"
        staged.mkdir()
        report = {"schema_version": 1, "skills": [], "repositories": []}
        bytes_copied = 0

        for index, entry in enumerate(sources, start=1):
            repo = entry["repo"]
            src = scratch / f"source-{index}"
            print(f"[{index}/{len(sources)}] Fetching {repo} by sparse checkout", flush=True)
            cmd(
                "git", "-c", "core.hooksPath=/dev/null",
                "clone", "--quiet", "--filter=blob:none", "--depth=1",
                "--single-branch", "--no-checkout",
                f"https://github.com/{repo}.git", str(src)
            )
            cmd("git", "sparse-checkout", "init", "--cone", cwd=src)
            cmd("git", "sparse-checkout", "set", "--stdin", cwd=src,
                stdin="\n".join(entry["paths"]) + "\n")
            cmd("git", "-c", "core.hooksPath=/dev/null",
                "checkout", "--quiet", "--detach", "HEAD", cwd=src)
            revision = cmd("git", "rev-parse", "HEAD", cwd=src)
            root = staged / slug(repo)
            root.mkdir(parents=True, exist_ok=True)
            for notice in ("LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE", "NOTICE.md",
                           "THIRD_PARTY_NOTICES.md"):
                f = src / notice
                if f.is_file():
                    shutil.copy2(f, root / notice)
            if repo == "vercel-labs/agent-skills":
                # This repo declares MIT under README.md#license (no root LICENSE).
                f = src / "README.md"
                if f.is_file():
                    shutil.copy2(f, root / "UPSTREAM-README.md")
            records = []
            for rel in entry["paths"]:
                dst = root / rel
                file_count, size = local_tree_copy(src / rel, dst)
                bytes_copied += size
                if bytes_copied > MAX_TOTAL_BYTES:
                    raise RuntimeError(
                        f"Vendor directory exceeded {MAX_TOTAL_BYTES} bytes. "
                        "Review large assets instead of silently dropping files."
                    )
                records.append({
                    "repo": repo,
                    "revision": revision,
                    "path": rel,
                    "local_path": f"{slug(repo)}/{rel}",
                    "files": file_count,
                    "bytes": size,
                    "license": entry["license"],
                })
                report["skills"].append(records[-1])
                print(f"    ✓ {rel}: {file_count} files, {size} B", flush=True)
            (root / "SOURCE.json").write_text(
                json.dumps({
                    "repository": repo, "upstream_sha": revision,
                    "url": f"https://github.com/{repo}/tree/{revision}",
                    "license": entry["license"], "skills": records,
                }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            report["repositories"].append({
                "repo": repo, "revision": revision, "skill_count": len(records)
            })

        report["skills_count"] = len(report["skills"])
        report["total_bytes"] = bytes_copied
        report["synced_on_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        if report["skills_count"] != 50:
            raise RuntimeError("Incomplete skill pack; will not publish")
        (staged / "INDEX.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (staged / "ATTRIBUTION.md").write_text(
            "# Third-party skill packs — provenance and licensing\n\n"
            "These 50 skill directories are unmodified upstream source snapshots. "
            "Licenses remain independent of the root repository's MIT license. "
            "Each repository has SOURCE.json and, where upstream provides it, "
            "license/notice files. For Anthropic, consult each copied skill's "
            "LICENSE.txt. Do not execute upstream code automatically.\n\n"
            + "\n".join(
                f"- [{s['repo']}](https://github.com/{s['repo']}/tree/"
                f"{next(v['revision'] for v in report['repositories'] if v['repo']==s['repo'])}) "
                f"— {s['license']} — {len(s['paths'])} skill(s)"
                for s in sources
            ) + "\n", encoding="utf-8"
        )
        # Keep declarative manifest and handwritten README, replace only generated
        # vendor content; never modify other pre-existing vendor packages.
        for f in list(DEST.iterdir()):
            if f.name not in {"SOURCES.json", "README.md"}:
                if f.is_dir():
                    shutil.rmtree(f)
                else:
                    f.unlink()
        for child in staged.iterdir():
            shutil.move(str(child), str(DEST / child.name))
        print(f"SYNC COMPLETE: {report['skills_count']} complete directories, "
              f"{bytes_copied} bytes.")


def check(sources: list[dict]) -> None:
    report_path = DEST / "INDEX.json"
    if not report_path.exists():
        raise RuntimeError("Not yet synced. Run --sync to acquire upstream files.")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("skills_count") != 50:
        raise RuntimeError("The generated source index is incomplete")
    if len(report.get("skills", [])) != 50:
        raise RuntimeError("Wrong number of indexed skills")
    for record in report["skills"]:
        source = DEST / record["local_path"]
        if not (source / "SKILL.md").is_file():
            raise RuntimeError(f"Missing actual source skill: {source}")
        if not (DEST / slug(record["repo"]) / "SOURCE.json").is_file():
            raise RuntimeError(f"Missing source provenance for {source}")
    print("CHECK PASSED: 50 complete skill directories with SKILL.md and provenance.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate", action="store_true")
    group.add_argument("--sync", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    _, source_data = load_manifest()
    if args.sync:
        sync(source_data)
    elif args.check:
        check(source_data)
