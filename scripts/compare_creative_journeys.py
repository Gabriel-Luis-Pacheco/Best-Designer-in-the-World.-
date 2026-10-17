#!/usr/bin/env python3
"""Pair 2 real Playwright creative-journey captures for BLIND HUMAN review.

Strictly verifies matching scene/viewport coverage, hashes and files.
This is NOT an aesthetic, causal, accessibility or performance grader.
"""
from __future__ import annotations
import argparse,hashlib,html,json,shutil,struct
from pathlib import Path

MAX_IMAGE_BYTES=20_000_000
def verify_manifest(path:Path)->dict:
    root=path.resolve().parent
    data=json.loads(path.read_text(encoding="utf-8"))
    if data.get("status")!="CAPTURED_FOR_HUMAN_REVIEW":
        raise ValueError("Capture status missing or not complete")
    if data.get("page_errors"):
        raise ValueError("Runtime errors present in capture")
    if any(w.get("type")=="EXTERNAL_RESOURCE_BLOCKED" for w in data.get("warnings", [])):
        raise ValueError("Capture blocked external resources; images may be inaccurate")
    viewports=data.get("viewports")
    frames=data.get("frames")
    if not isinstance(viewports,list) or not viewports or not isinstance(frames,list) or not frames:
        raise ValueError("Empty viewports or frames")
    vp={v["name"]:(v["width"],v["height"]) for v in viewports}
    if len(vp)!=len(viewports):raise ValueError("Duplicate viewport names")
    verified={}
    for f in frames:
        key=(f["viewport"],f["id"])
        if key in verified or key[0] not in vp:raise ValueError("Duplicate or unknown scene: "+str(key))
        rawpath=f.get("file")
        if not isinstance(rawpath,str):raise ValueError("Missing filename")
        candidate=Path(rawpath)
        if candidate.is_absolute() or ".." in candidate.parts or "\\" in rawpath or candidate.suffix.lower()!=".png":
            raise ValueError("Unsafe screenshot path")
        src=(root/candidate).resolve()
        if not src.is_relative_to(root) or not src.is_file() or src.is_symlink():
            raise ValueError("Screenshot unavailable or symlinked")
        raw=src.read_bytes()
        if not raw.startswith(b"\x89PNG\r\n\x1a\n") or len(raw)>MAX_IMAGE_BYTES or len(raw)<100:
            raise ValueError("Invalid PNG evidence: "+str(key))
        width,height=struct.unpack(">II",raw[16:24])
        if (width,height)!=vp[key[0]]:
            raise ValueError("PNG dimensions incompatible with declared viewport: "+str(key))
        sha=hashlib.sha256(raw).hexdigest()
        if f.get("sha256")!=sha:raise ValueError("SHA mismatch: "+str(key))
        action=f.get("action")
        intent=f.get("intent")
        observed=f.get("observed_state")
        if action is not None and (not isinstance(intent,str) or not intent or not isinstance(observed,dict)):
            raise ValueError("Action capture lacks comparable semantic intent/state: "+str(key))
        verified[key]={"path":src,"sha256":sha,"bytes":len(raw),"height":height,
                       "intent":intent,"action_kind":action.get("type") if isinstance(action,dict) else None,
                       "observed_property":observed.get("property") if isinstance(observed,dict) else None,
                       "observed_state":observed.get("value") if isinstance(observed,dict) else None,
                       "scroll_offset_px":f.get("scroll_offset_px",0)}
    return {"frames":verified,"viewports":vp,"config":{"reduced_motion":data.get("reduced_motion"),
             "allow_animations":data.get("allow_animations"),
             "allow_external_requests":data.get("allow_external_requests",False)},"source":path}

def compare(left_path:Path,right_path:Path,out:Path)->dict:
    a=verify_manifest(left_path);b=verify_manifest(right_path)
    if a["viewports"]!=b["viewports"] or a["config"]!=b["config"]:
        raise ValueError("Mismatched viewport or motion capture conditions")
    if set(a["frames"])!=set(b["frames"]):
        raise ValueError("Mismatched scene coverage: recapture equivalent beats")
    for key in a["frames"]:
        left,right=a["frames"][key],b["frames"][key]
        for field in ("intent","action_kind","observed_property","scroll_offset_px"):
            if left[field]!=right[field]:
                raise ValueError(f"Mismatched semantic action/state capture for {key}: {field}")
        if left["intent"] is not None and (left["observed_state"] is None or right["observed_state"] is None):
            raise ValueError(f"Unobserved interactive result for {key}")
    out=out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    images=out/"images";images.mkdir(exist_ok=True)
    sections=[]
    for vp in sorted(a["viewports"]):
        scenes=[key for key in a["frames"] if key[0]==vp]
        frames=[]
        for idx,key in enumerate(scenes):
            visual=[]
            for side,data in (("A",a),("B",b)):
                image=data["frames"][key]
                name=vp+"-"+str(idx+1)+"-"+side+".png"
                shutil.copyfile(image["path"],images/name)
                visual.append('<figure><img src="images/'+html.escape(name)+'" alt="Variant '+side+' scene '+html.escape(key[1])+'"><figcaption>Variant '+side+' — '+html.escape(key[1])+'</figcaption></figure>')
            frames.append('<h3>'+html.escape(key[1])+'</h3><div class="pair">'+''.join(visual)+'</div>')
        sections.append('<section><h2>'+html.escape(vp)+' — '+str(a["viewports"][vp][0])+'px</h2>'+''.join(frames)+'</section>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'">
<title>Blind creative review — no winner assigned</title><style>
body{background:#151b1c;color:#f1f1e9;font:15px/1.5 system-ui;padding:clamp(18px,3vw,56px);margin:0}
h1{font-size:clamp(28px,4vw,54px);line-height:1}h3{margin-top:34px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
figure{margin:0;min-width:0}img{width:100%;height:auto;border:1px solid #64706a;display:block}figcaption{padding:12px;color:#b6cabc}
.notice{padding:18px;border:1px solid #64706a}section{margin-top:48px}@media(max-width:850px){.pair{grid-template-columns:1fr}}</style>
<h1>Blind creative comparison</h1><p class="notice">Two variants shown as A/B only. Technical capture compatibility checked; NO winner, beauty score, independent user result, controlled causal effect or accessibility pass is implied. Review composition, distinctiveness, interaction, meaning, middle scene, climax, ending and mobile separately.</p>'''+''.join(sections)+'</html>'
    (out/"blind-review.html").write_text(page,encoding="utf-8")
    report={"status":"READY_FOR_BLIND_HUMAN_REVIEW_NOT_SCORED",
            "scene_pairs":len(a["frames"]),
            "viewports":a["viewports"],
            "motion_conditions":a["config"],
            "interaction_contract":"MATCHED_SEMANTIC_INTENT_ACTION_KIND_AND_STATE_PROPERTY",
            "not_proven":["skill superiority","artistic quality","randomized or controlled A/B","accessibility","commercial outcomes"]}
    (out/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    # Variant mapping is in the invoker's CLI invocation, not in the public review HTML.
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--a",type=Path,required=True,help="First variant manifest")
    p.add_argument("--b",type=Path,required=True,help="Second variant manifest")
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    try:print(json.dumps(compare(args.a,args.b,args.out),indent=2))
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        p.exit(2,"INVALID COMPARISON: "+str(e)+"\n")
if __name__=="__main__":main()
