#!/usr/bin/env python3
"""Compare PNG frames of two design variants by story beat, without grading taste.

Input: {"title": "...", "required_beats":["opening","middle","ending","mobile_opening"],
"candidates":[{"id":"a","frames":[{"beat":"opening","path":"a.png","viewport":"1440x900","state":"rest"}]}]}
Paths must be relative to the JSON file directory. No URLs, SVG or executable content.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import struct

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 24_000_000
MAX_TOTAL_BYTES = 96_000_000
DEFAULT_BEATS = ("opening", "middle", "ending", "mobile_opening")

def _image(path: Path, base: Path) -> dict:
    if path.is_absolute() or ".." in path.parts or path.suffix.lower() != ".png":
        raise ValueError("Only relative PNG screenshot paths are allowed")
    full = (base / path).resolve()
    if not full.is_relative_to(base.resolve()) or not full.is_file() or full.is_symlink():
        raise ValueError("Screenshot outside manifest folder, missing, or symlink")
    raw = full.read_bytes()
    if not (24 <= len(raw) <= MAX_IMAGE_BYTES) or not raw.startswith(PNG_MAGIC) or raw[12:16] != b"IHDR":
        raise ValueError("Invalid PNG or screenshot exceeds 24 MB")
    w, h = struct.unpack(">II", raw[16:24])
    if not (1 <= w <= 12000 and 1 <= h and w * h <= 250_000_000):
        raise ValueError("Invalid PNG dimensions")
    return {"width": w, "height": h, "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "url": "data:image/png;base64," + base64.b64encode(raw).decode("ascii")}

def build(manifest: Path, out: Path) -> dict:
    if out.suffix.lower() != ".html":
        raise ValueError("Output must end in .html")
    raw = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("candidates"), list) or len(raw["candidates"]) != 2:
        raise ValueError("Provide exactly two candidate variants")
    required = raw.get("required_beats", list(DEFAULT_BEATS))
    if not isinstance(required, list) or not required or len(required) != len(set(required)):
        raise ValueError("Invalid required beats")
    if any(not isinstance(x, str) or not x.strip() for x in required):
        raise ValueError("Invalid beat name")
    variants, ids, total = [], set(), 0
    for variant in raw["candidates"]:
        if not isinstance(variant, dict) or not isinstance(variant.get("id"), str) or not variant["id"].strip() or variant["id"] in ids:
            raise ValueError("Missing/duplicate variant id")
        ids.add(variant["id"])
        frames = variant.get("frames")
        if not isinstance(frames, list) or not frames or len(frames) > 16:
            raise ValueError("Each candidate needs 1-16 frames")
        mapped = {}
        for f in frames:
            if not isinstance(f, dict) or not isinstance(f.get("beat"), str) or not f["beat"].strip() or f["beat"] in mapped:
                raise ValueError("Duplicate or invalid beat")
            if not isinstance(f.get("path"), str) or not f["path"].strip():
                raise ValueError("Missing screenshot path")
            img = _image(Path(f["path"]), manifest.parent)
            total += img["size"]
            if total > MAX_TOTAL_BYTES:
                raise ValueError("Total screenshot media exceeds 96 MB")
            mapped[f["beat"]] = {"image": img,
                "state": str(f.get("state", "UNSPECIFIED")),
                "viewport": str(f.get("viewport", "UNSPECIFIED"))}
        variants.append({"id": variant["id"], "frames": mapped})
    beats = list(dict.fromkeys([*required, *(b for v in variants for b in v["frames"])]))
    warnings = []
    sections = []
    for beat in beats:
        left, right = (v["frames"].get(beat) for v in variants)
        if (left is None or right is None) and beat in required:
            warnings.append({"beat": beat, "kind": "MISSING_REQUIRED_FRAME"})
        if left and right:
            if left["image"]["width"] != right["image"]["width"] or left["viewport"] != right["viewport"]:
                warnings.append({"beat": beat, "kind": "CAPTURE_VIEWPORT_MISMATCH"})
            if left["state"] != right["state"]:
                warnings.append({"beat": beat, "kind": "CAPTURE_STATE_MISMATCH"})
            if left["image"]["sha256"] == right["image"]["sha256"]:
                warnings.append({"beat": beat, "kind": "IDENTICAL_IMAGES_REVIEW"})
        cards = []
        for v, f in zip(variants, (left, right)):
            if not f:
                cards.append("<div class='missing'>MISSING — " + html.escape(v["id"]) + "</div>")
                continue
            im = f["image"]
            meta = (html.escape(v["id"]) + " · " + html.escape(f["viewport"]) + " · " +
                    html.escape(f["state"]) + " · " + str(im["width"]) + "×" + str(im["height"]) +
                    " · SHA " + im["sha256"][:12])
            cards.append("<figure><figcaption>" + meta + "</figcaption><img loading='lazy' alt='" +
                         html.escape(v["id"] + " / " + beat, quote=True) + "' src='" + im["url"] + "'></figure>")
        sections.append("<section><h2>" + html.escape(beat) + "</h2><div class='grid'>" + "".join(cards) + "</div></section>")
    title = html.escape(str(raw.get("title", "Journey review")))
    warn = "".join("<li>" + html.escape(w["beat"] + ": " + w["kind"]) + "</li>" for w in warnings)
    page = ("<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'\">"
            "<title>" + title + "</title><style>*{box-sizing:border-box}body{font:16px/1.5 system-ui;margin:0;padding:24px;background:#171719;color:#fafafa}"
            "h1{font-size:clamp(26px,4vw,46px)}h2{text-transform:uppercase;letter-spacing:.1em;font-size:15px;margin:45px 0 10px}"
            ".grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}figure{margin:0;min-width:0}"
            "figcaption{font-size:12px;color:#bcbcbc;overflow-wrap:anywhere;margin-bottom:8px}"
            "img{max-width:100%;height:auto;border:1px solid #656565}.missing{padding:20px;border:1px dashed #888}"
            "li{margin:4px 0}@media(max-width:750px){.grid{grid-template-columns:1fr}}</style>"
            "<h1>" + title + "</h1><p>Matched story beats, not an algorithmic aesthetic score. Different scroll timing and camera states invalidate direct conclusions.</p>"
            "<h2>Evidence warnings</h2><ul>" + (warn or "<li>None detected by basic metadata checks. Capture conditions may still differ.</li>") +
            "</ul>" + "".join(sections) + "<p>Human review is required for originality, comprehension, interaction, accessibility and performance.</p></html>")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    result = {"status": "EVIDENCE_BOARD_ONLY_NO_AUTOMATIC_WINNER",
              "candidates": [v["id"] for v in variants], "beats": beats, "warnings": warnings,
              "sources": [{ "id": v["id"], "frames": {beat: {
                  "sha256": f["image"]["sha256"], "width": f["image"]["width"],
                  "height": f["image"]["height"], "state": f["state"], "viewport": f["viewport"]
                  } for beat, f in v["frames"].items()}} for v in variants]}
    out.with_suffix(".evidence.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.manifest, args.out), indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, "INVALID BOARD: " + str(exc) + "\n")
