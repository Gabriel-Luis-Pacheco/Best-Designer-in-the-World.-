#!/usr/bin/env python3
"""Create a LOCAL side-by-side asset comparison HTML. Never claims visual identity.

Inputs must be trusted local images. No network calls, external programs, or AI grader.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import html
from pathlib import Path
import re
import sys

TYPES={".svg":"image/svg+xml",".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp",".gif":"image/gif"}
MAX_BYTES=8_000_000
MAX_ITEMS=9

def load_image(path: Path) -> dict:
    if path.suffix.lower() not in TYPES:
        raise ValueError("Only SVG, PNG, JPEG, WebP and GIF assets are accepted")
    if not path.is_file() or path.is_symlink():
        raise ValueError("Asset path must reference a regular local file")
    raw=path.read_bytes()
    if not raw or len(raw)>MAX_BYTES:
        raise ValueError("Asset must be between 1 byte and 8 MB")
    kind=TYPES[path.suffix.lower()]
    if kind=="image/svg+xml":
        lowered=raw.lower()
        # Safe default: no active/external content in the review document.
        if any(x in lowered for x in (b"<script",b"<foreignobject",b"<!entity",b"<!doctype",
                                    b"javascript:",b"data:text/html",b"onload=",b"onclick=",
                                    b"onerror=",b"@import")) or re.search(rb'(?:href|src)\\s*=\\s*["\\\']\\s*(?:https?://|//|javascript:)', lowered):
            raise ValueError("SVG contains external/active markup; sanitize an offline copy first")
        if b"<svg" not in lowered:
            raise ValueError("Invalid SVG content")
    if kind=="image/png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Invalid PNG signature")
    if kind=="image/jpeg" and not raw.startswith(b"\xff\xd8"):
        raise ValueError("Invalid JPEG signature")
    if kind=="image/webp" and not (raw[:4]==b"RIFF" and raw[8:12]==b"WEBP"):
        raise ValueError("Invalid WebP signature")
    if kind=="image/gif" and raw[:6] not in (b"GIF87a",b"GIF89a"):
        raise ValueError("Invalid GIF signature")
    return {"name":path.name,"bytes":len(raw),"sha":hashlib.sha256(raw).hexdigest(),
            "uri":f"data:{kind};base64,"+base64.b64encode(raw).decode("ascii")}

def render(original: dict, candidates: list[dict]) -> str:
    cards=[]
    for i, a in enumerate([original]+candidates):
        label="CANON / ORIGINAL" if i==0 else f"PROPOSAL {i}"
        cards.append(
            f'<figure class="card"><figcaption><strong>{label}</strong><span>{html.escape(a["name"])}</span></figcaption>'
            f'<div class="stage"><img loading="eager" src="{a["uri"]}" alt="{html.escape(label)}: {html.escape(a["name"])}"></div>'
            f'<p>{a["bytes"]:,} bytes · SHA256 <code>{a["sha"][:16]}…</code></p></figure>'
        )
    return """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Brand asset comparison — manual review</title><style>
:root{color-scheme:light dark}*{box-sizing:border-box}body{font:16px/1.45 system-ui,sans-serif;margin:0;padding:clamp(16px,4vw,56px);background:#1b1b22;color:#f4f3ee}
h1{font-size:clamp(26px,4vw,52px);letter-spacing:-.04em;line-height:1.1;margin:0 0 12px}p{max-width:85ch;color:#bcbcc5}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:20px;margin-top:32px}.card{margin:0;border:1px solid #494957;background:#272731;border-radius:14px;overflow:hidden}
figcaption{padding:18px;display:grid;gap:3px}figcaption strong{font-size:12px;letter-spacing:.1em;color:#bed9aa}figcaption span{overflow-wrap:anywhere}
.stage{height:350px;display:grid;place-items:center;padding:20px;background:linear-gradient(45deg,#d8d8dc 25%,transparent 25%),linear-gradient(-45deg,#d8d8dc 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d8d8dc 75%),linear-gradient(-45deg,transparent 75%,#d8d8dc 75%);background-size:28px 28px;background-position:0 0,0 14px,14px -14px,-14px 0;background-color:#f2f2f3}
.stage img{max-width:100%;max-height:100%;object-fit:contain}.card p{font-size:12px;margin:0;padding:14px 18px;overflow-wrap:anywhere}code{color:#f6c67b}
.notes{border-top:1px solid #494957;margin-top:28px;padding-top:12px}li{margin:8px 0;max-width:100ch}
</style><main><h1>Does the new asset still belong to the same brand?</h1><p>Files placed at comparable scale. This board does not certify identity, aesthetic quality or licensing. Use official original assets and compare silhouette, anatomy, expression, palette, stroke, material, lighting and appearance in the real interface.</p>
<div class="grid">""" + "".join(cards) + """</div><section class="notes"><h2>Human review required</h2><ol><li>Compare silhouette and proportions without reading names.</li><li>Compare palette, outlines, expression, material and lighting.</li><li>Open real interface at hero, compact and mobile sizes; this board does not replace context.</li><li>Record: PASS, REVISE or REJECT with a concrete evidence trail and canonical source.</li></ol></section></main></html>"""

def create_board(original_path:Path,candidates:list[Path],out:Path)->dict:
    if not 1<=len(candidates)<=MAX_ITEMS:
        raise ValueError(f"Provide 1–{MAX_ITEMS} candidate images")
    original=load_image(original_path)
    proposals=[load_image(p) for p in candidates]
    if out.suffix.lower()!=".html":
        raise ValueError("Output must be an .html file")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(render(original,proposals),encoding="utf-8")
    return {"output":str(out),"original_sha256":original["sha"],"candidate_sha256":[p["sha"] for p in proposals],
            "status":"BOARD_CREATED_HUMAN_REVIEW_REQUIRED"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original",type=Path,required=True)
    p.add_argument("--candidate",type=Path,action="append",required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    try:
        result=create_board(args.original,args.candidate,args.out)
        print(result)
    except (OSError,ValueError) as exc:
        p.exit(2,f"INVALID ASSET COMPARISON: {exc}\n")

if __name__=="__main__":main()
