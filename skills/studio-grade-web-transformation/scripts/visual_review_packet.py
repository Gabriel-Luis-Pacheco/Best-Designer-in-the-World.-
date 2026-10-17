#!/usr/bin/env python3
"""Offline evidence board for before/after PAGE screenshots. Manual review mandatory.

Pixel sizes are checked; matching width does NOT prove identical viewport/browser state.
"""
from __future__ import annotations
import argparse,base64,hashlib,html,json,struct
from pathlib import Path

MAX_BYTES=24_000_000
MAX_PX=250_000_000
def png(path:Path)->dict:
    if not path.is_file() or path.is_symlink():
        raise ValueError("Screenshot must be a regular file")
    raw=path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n") or len(raw)<24 or len(raw)>MAX_BYTES:
        raise ValueError("Provide a valid PNG under 24 MB")
    width,height=struct.unpack(">II",raw[16:24])
    if not (1<=width<=12000 and 1<=height and width*height<=MAX_PX):
        raise ValueError("Invalid or excessive screenshot dimensions")
    return {"name":path.name,"width":width,"height":height,
            "sha256":hashlib.sha256(raw).hexdigest(),
            "data":"data:image/png;base64,"+base64.b64encode(raw).decode("ascii")}

def packet(before:Path,after:Path,out:Path,label:str="Full-page comparison")->dict:
    a,b=png(before),png(after)
    if a["width"]!=b["width"]:
        raise ValueError("Screen widths differ; same viewport width is required for a direct comparison")
    if out.suffix.lower()!=".html":
        raise ValueError("Output must end in .html")
    out.parent.mkdir(parents=True,exist_ok=True)
    title=html.escape(label)
    cards=[]
    for name,item in [("BEFORE",a),("AFTER",b)]:
        cards.append(f'<section><h2>{name}</h2><small>{html.escape(item["name"])} — {item["width"]} × {item["height"]} px — SHA256 {item["sha256"][:18]}…</small><img src="{item["data"]}" alt="{name} screenshot" /></section>')
    body='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'">
<title>Visual evidence review</title><style>*{box-sizing:border-box}body{font:16px/1.5 system-ui;background:#151518;color:#eee;padding:clamp(12px,3vw,40px);margin:0}
h1{font-size:clamp(25px,4vw,48px);margin:0}p,small{color:#bbb}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;align-items:start;margin:30px 0}
section{min-width:0}h2{font-size:14px;letter-spacing:.12em}small{display:block;margin-bottom:12px;overflow-wrap:anywhere}img{width:100%;height:auto;border:1px solid #666;background:white}
aside{padding:18px;border:1px solid #444}li{margin:8px 0}@media(max-width:760px){.grid{grid-template-columns:1fr}}</style>
<h1>'''+title+'''</h1><p>Matched source widths, not guaranteed matched capture state. Do NOT claim visual superiority automatically. Review the whole page and also inspect interactions in browser.</p><div class="grid">'''+''.join(cards)+'''</div><aside><h2>Manual review checklist</h2><ol><li>Opening/middle/ending: did the weakest part become better, and what was removed?</li><li>Brand fidelity: are real characters, surfaces and screenshots consistent?</li><li>Composition: rhythm, whitespace, density, transitions and typography after the first fold.</li><li>Mobile: must have its own pair of screenshots and interaction tests.</li><li>Functionality, accessibility, data truth and performance require separate evidence.</li></ol></aside></html>'''
    out.write_text(body,encoding="utf-8")
    result={"status":"REVIEW_BOARD_ONLY_NOT_APPROVED","label":label,
            "before":{"name":a["name"],"width":a["width"],"height":a["height"],"sha256":a["sha256"]},
            "after":{"name":b["name"],"width":b["width"],"height":b["height"],"sha256":b["sha256"]}}
    out.with_suffix(".evidence.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--before",type=Path,required=True)
    p.add_argument("--after",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--label",default="Full-page comparison")
    args=p.parse_args()
    try:
        print(json.dumps(packet(args.before,args.after,args.out,args.label),indent=2))
    except (OSError,ValueError) as e:
        p.exit(2,f"INVALID REVIEW PAIR: {e}\n")
