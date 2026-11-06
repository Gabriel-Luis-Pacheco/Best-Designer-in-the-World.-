#!/usr/bin/env python3
"""Static search-discovery audit: review candidates, not indexation/ranking proof."""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlparse


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.in_head = False
        self.in_title = False
        self.in_script = False
        self.script_kind = ""
        self.title = ""
        self.meta = {}
        self.canonical = []
        self.anchors = []
        self.h1 = []
        self.in_h1 = False
        self.in_anchor = False
        self.current_anchor = None
        self.img = []
        self.structured = []
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang") or ""
        elif tag == "head":
            self.in_head = True
        elif tag == "title" and self.in_head:
            self.in_title = True
        elif tag == "meta" and self.in_head:
            key = a.get("name") or a.get("property")
            if key:
                self.meta.setdefault(key.casefold(), []).append(a.get("content") or "")
        elif tag == "link" and self.in_head:
            if "canonical" in (a.get("rel") or "").lower().split():
                self.canonical.append(a.get("href") or "")
        elif tag == "h1":
            self.in_h1 = True
            self.h1.append("")
        elif tag == "a":
            self.in_anchor = True
            self.current_anchor = {"href": a.get("href") or "", "text": ""}
        elif tag == "img":
            self.img.append({"src": a.get("src", ""), "alt": a.get("alt")})
        elif tag == "script":
            self.in_script = True
            self.script_kind = a.get("type") or ""
            self._buffer = []

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h1 and self.h1:
            self.h1[-1] += data
        if self.in_anchor and self.current_anchor is not None:
            self.current_anchor["text"] += data
        if self.in_script and self.script_kind == "application/ld+json":
            self._buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        elif tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "a":
            if self.current_anchor is not None:
                self.anchors.append(self.current_anchor)
            self.in_anchor = False
            self.current_anchor = None
        elif tag == "script":
            if self.in_script and self.script_kind == "application/ld+json":
                try:
                    self.structured.append({"valid": True, "data": json.loads("".join(self._buffer))})
                except json.JSONDecodeError:
                    self.structured.append({"valid": False})
            self.in_script = False
            self.script_kind = ""


def audit_page(name, source, public=True):
    p = PageParser()
    p.feed(source)
    issues = []
    def flag(code, severity, detail):
        issues.append({"code": code, "severity": severity, "detail": detail})
    if not public:
        return {"file": name, "status": "NOT_APPLICABLE_PRIVATE", "issues": [],
                "reason": "Private/internal interfaces do not require public search visibility"}
    title = p.title.strip()
    description = p.meta.get("description", [""])[0].strip()
    if not p.html_lang.strip():
        flag("LANG_REVIEW", "REVIEW", "Declare the correct document language for users and assistive technology")
    if not title:
        flag("TITLE_MISSING", "P1", "Public page has no static title; inspect rendered HTML if framework injects it")
    if not description:
        flag("DESCRIPTION_MISSING", "REVIEW", "Page-specific meta description missing")
    if len(p.meta.get("description", [])) > 1:
        flag("MULTIPLE_DESCRIPTIONS", "REVIEW", "Multiple description declarations")
    if not p.h1 or not any(x.strip() for x in p.h1):
        flag("H1_MISSING", "REVIEW", "No meaningful H1 found in supplied static HTML")
    if len(p.h1) > 1:
        flag("MULTIPLE_H1", "REVIEW", "Check heading hierarchy; multiple H1 elements are not automatically SEO errors")
    robots = " ".join(p.meta.get("robots", []) + p.meta.get("googlebot", [])).lower()
    if "noindex" in robots:
        flag("NOINDEX_PUBLIC", "P0", "Public discovery page instructs crawlers not to index")
    if len(p.canonical) > 1:
        flag("MULTIPLE_CANONICALS", "P1", "Conflicting canonical hints are possible")
    if p.canonical:
        if not p.canonical[0].startswith(("https://", "http://")):
            flag("CANONICAL_NOT_ABSOLUTE", "REVIEW", "Canonical should be an absolute preferred URL")
        if "#" in p.canonical[0]:
            flag("CANONICAL_FRAGMENT", "REVIEW", "Canonical fragment is not a valid canonical target")
    else:
        flag("CANONICAL_REVIEW", "REVIEW", "Consider explicit canonical when duplicate URLs exist")
    for anchor in p.anchors:
        href = anchor["href"].strip()
        if not href or href == "#" or href.lower().startswith("javascript:"):
            flag("NONCRAWLABLE_NAVIGATION", "REVIEW", "A link uses a placeholder or JS href")
        if href and href.startswith(("/", "http")) and anchor["text"].strip().lower() in {
                "click here", "learn more", "clique aqui", "saiba mais"}:
            flag("GENERIC_ANCHOR", "REVIEW", "Inspect whether the anchor communicates its destination in context")
    for image in p.img:
        if image["alt"] is None:
            flag("IMAGE_ALT_MISSING", "REVIEW", "Image missing alt attribute; distinguish informative and decorative images")
    for item in p.structured:
        if not item["valid"]:
            flag("JSONLD_INVALID", "REVIEW", "Structured JSON-LD could not be parsed; verify live rich result eligibility")
    if "og:title" not in p.meta or "og:description" not in p.meta or "og:image" not in p.meta:
        flag("SOCIAL_PREVIEW", "REVIEW", "Check sharing preview metadata if the route is intended to be shared")
    return {"file": name, "status": "STATIC_REVIEW_ONLY", "title": title,
            "description": description, "h1": [s.strip() for s in p.h1],
            "canonical": p.canonical, "issues": issues,
            "limitations": ["No live status, robots.txt, sitemap, hreflang or Google indexing check",
                            "Client-side rendered pages require a real browser and Search Console URL Inspection",
                            "Missing metadata does not establish ranking outcomes"]}


def inspect(files: dict[str, str], public=True):
    if not isinstance(files, dict) or not files or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in files.items()
    ):
        return {"status": "INVALID", "pages": [], "counts": {},
                "errors": ["Expected a nonempty mapping of filenames to HTML text"]}
    results = [audit_page(k, v, public) for k, v in files.items()]
    titles = {}
    descriptions = {}
    for row in results:
        if not public:
            continue
        title = row.get("title", "").casefold()
        desc = row.get("description", "").casefold()
        if title:
            titles.setdefault(title, []).append(row)
        if desc:
            descriptions.setdefault(desc, []).append(row)
    for group in titles.values():
        if len(group) > 1:
            for row in group:
                row["issues"].append({"code": "DUPLICATE_TITLE", "severity": "REVIEW",
                                      "detail": "Identical title in multiple supplied pages"})
    for group in descriptions.values():
        if len(group) > 1:
            for row in group:
                row["issues"].append({"code": "DUPLICATE_DESCRIPTION", "severity": "REVIEW",
                                      "detail": "Identical meta description in multiple supplied pages"})
    return {"status": "NOT_APPLICABLE" if not public else "STATIC_REVIEW_ONLY",
            "pages": results, "counts": {s: sum(i["severity"] == s for r in results
                                               for i in r["issues"]) for s in ("P0", "P1", "REVIEW")}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path, nargs="+")
    ap.add_argument("--scope", choices=("public", "private"), default="public")
    args = ap.parse_args()
    if len(args.html) > 80:
        ap.error("Maximum 80 pages per audit")
    sources = {}
    for path in args.html:
        if not path.is_file() or path.is_symlink() or path.stat().st_size > 4_000_000:
            ap.error("Page missing, symlinked, or larger than 4 MB: " + str(path))
        sources[str(path)] = path.read_text(encoding="utf-8")
    print(json.dumps(inspect(sources, args.scope == "public"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
