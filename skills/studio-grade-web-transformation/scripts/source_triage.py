#!/usr/bin/env python3
"""Fast, local, *advisory* source inspection for common interface risks.

Works without dependencies or network. Findings are hypotheses to inspect in a
browser, not WCAG violations, aesthetic grades or proof of 'AI slop'. For real
layout/interaction use the existing Playwright and HTML inspection tools.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

EXTS={".css",".scss",".sass",".less",".html",".htm",".jsx",".tsx",".vue",".svelte",".astro"}
IGNORED_DIRS={"node_modules",".git",".next",".nuxt","dist","build","coverage","vendor","__pycache__"}
MAX_FILE_BYTES=1_000_000
MAX_FILES=1000
# Only locally recognizable patterns: do not outlaw a palette, font or layout style.
RULES=[
    ("OUTLINE_REMOVAL_REVIEW",r"\boutline\s*:\s*(?:none|0(?:px|rem|em)?)\b",
     "Verify a visible alternative focus indicator in the actual keyboard state."),
    ("BROAD_TRANSITION_REVIEW",r"\btransition\s*:\s*all\b",
     "Specify intended animated properties; check layout thrash and reduced motion."),
    ("OVERFLOW_MASK_REVIEW",r"\boverflow-x\s*:\s*hidden\b",
     "Inspect narrow viewports for clipped content, hidden focus and accidental overflow."),
    ("FIXED_MOBILE_VH_REVIEW",r"\b(?:min-height|height)\s*:\s*100vh\b",
     "Inspect real mobile browser chrome; consider dvh/svh or content-based sizing."),
]
PATTERNS=[(code,re.compile(rx,re.IGNORECASE),action) for code,rx,action in RULES]
REDUCED_MOTION=re.compile(r"prefers-reduced-motion\s*:\s*reduce", re.I)
LOOP_ANIMATION=re.compile(r"\banimation(?:-\w+)?\s*:[^;{}]*\binfinite\b", re.I)
GRADIENT_TEXT=re.compile(r"\b(?:background-clip|webkit-background-clip)\s*:\s*text\b", re.I)
GRADIENT=re.compile(r"(?:linear|radial|conic)-gradient\s*\(",re.I)
SMALL_TEXT=re.compile(r"\bfont-size\s*:\s*(?:[1-9](?:\.\d+)?|10(?:\.\d+)?|11(?:\.\d+)?)px\b", re.I)
JSX_DIV_CLICK=re.compile(r"<(?:div|span)\b[^>]{0,900}?\bonClick\s*=", re.I|re.S)
A11Y_KEYBOARD=re.compile(r"\b(?:onKeyDown|onKeyUp|onKeyPress|role\s*=|tabIndex\s*=)", re.I)

def _line(content: str, start: int) -> int:
    return content.count("\n",0,start)+1

def inspect(content: str, file: str) -> list[dict]:
    findings=[]
    lines=content.splitlines()
    def flag(code: str, at: int, action: str):
        line=_line(content,at)
        snippet=lines[line-1].strip()[:120] if line <= len(lines) else ""
        # Ignore is exact-code and local to this or immediately preceding line.
        neighborhood="\n".join(lines[max(0,line-2):line])
        if re.search(r"design-os-ignore\s+"+re.escape(code)+r"\s*:\s*\S.{7,}",neighborhood,re.I):
            return
        findings.append({"path":file,"line":line,"code":code,"severity":"REVIEW",
                         "evidence":snippet,"next_check":action,
                         "certainty":"STATIC_SOURCE_HEURISTIC"})
    for code,pattern,action in PATTERNS:
        for match in pattern.finditer(content):
            flag(code,match.start(),action)
    if LOOP_ANIMATION.search(content) and not REDUCED_MOTION.search(content):
        for match in LOOP_ANIMATION.finditer(content):
            flag("LOOP_MOTION_FALLBACK_REVIEW",match.start(),
                 "Inspect reduced-motion behavior, pause controls and whether animation conveys a task.")
    if GRADIENT.search(content):
        for match in GRADIENT_TEXT.finditer(content):
            flag("GRADIENT_TEXT_REVIEW",match.start(),
                 "Check type contrast/legibility and whether the treatment fits the approved brand.")
    for match in SMALL_TEXT.finditer(content):
        flag("SMALL_TEXT_REVIEW",match.start(),
             "Verify computed font size, hierarchy, zoom and mobile readability.")
    if Path(file).suffix.lower() in {".jsx",".tsx"}:
        for match in JSX_DIV_CLICK.finditer(content):
            tag=content[match.start():content.find(">",match.start())+1]
            if not A11Y_KEYBOARD.search(tag):
                flag("NONSEMANTIC_CLICK_TARGET_REVIEW",match.start(),
                     "Prefer a native button/link, or verify role, focus and keyboard activation.")
    return findings

def _files(target: Path):
    if target.is_symlink():
        raise ValueError("Symlink targets are not scanned")
    if target.is_file():
        if target.suffix.lower() not in EXTS:
            raise ValueError("Unsupported extension")
        return [target]
    if not target.is_dir():
        raise ValueError("Target must be an existing file/directory")
    found=[]
    for p in target.rglob("*"):
        if p.is_symlink() or not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        if any(part in IGNORED_DIRS for part in p.relative_to(target).parts):
            continue
        found.append(p)
        if len(found)>MAX_FILES:
            raise ValueError("Too many matching files; narrow the directory")
    return sorted(found)

def scan(target: Path)->dict:
    files=_files(target)
    findings=[]
    skipped=[]
    for p in files:
        if p.stat().st_size > MAX_FILE_BYTES:
            skipped.append(str(p))
            continue
        findings.extend(inspect(p.read_text(encoding="utf-8",errors="replace"),str(p)))
    return {"status":"REVIEW_CANDIDATES" if findings else "NO_STATIC_FLAGS",
            "files_scanned":len(files)-len(skipped),"skipped_files":skipped,
            "findings":findings,"method":"STATIC_SOURCE_ONLY",
            "limitations":"No computed CSS, DOM, browser, JS runtime, contrast proof, user research or aesthetic scoring."}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target",type=Path)
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--fail-on-review",action="store_true",help="Optional CI policy; flags are still not proven defects.")
    args=ap.parse_args()
    try:
        result=scan(args.target)
    except (ValueError,OSError) as exc:
        ap.error(str(exc))
    if args.json:
        print(json.dumps(result,indent=2,ensure_ascii=False))
    else:
        for issue in result["findings"]:
            print(f"{issue['path']}:{issue['line']}: {issue['code']} — {issue['next_check']}")
        print(f"{result['files_scanned']} files; {len(result['findings'])} review candidates; {len(result['skipped_files'])} skipped")
    if args.fail_on_review and result["findings"]:
        raise SystemExit(2)
if __name__=="__main__":
    main()
