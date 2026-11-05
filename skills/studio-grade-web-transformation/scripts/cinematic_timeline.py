#!/usr/bin/env python3
"""Validate a cinematic interaction plan before production, not its artistic merit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BEATS = ("opening", "development", "climax", "resolution")
INPUTS = {"autoplay", "click", "tap", "scroll", "keyboard", "video_end", "user_choice"}
ENGINES = {"css", "svg", "video", "canvas", "gsap", "three", "r3f", "rive", "other"}


def inspect(data: dict) -> dict:
    errors, warnings = [], []
    if not isinstance(data, dict):
        return {"status": "INVALID", "errors": ["Expected JSON object"], "warnings": []}
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("Provide authored scenes")
        scenes = []
    beats, ids = [], set()
    total_ms = 0
    for i, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            errors.append("Each scene must be an object")
            continue
        sid = scene.get("id")
        if not isinstance(sid, str) or not sid.strip() or sid in ids:
            errors.append(f"Scene {i}: id missing or duplicated")
        ids.add(sid)
        beat = scene.get("beat")
        if beat not in BEATS:
            errors.append(f"Scene {i}: invalid narrative beat")
        else:
            beats.append(beat)
        if scene.get("engine") not in ENGINES:
            errors.append(f"Scene {i}: engine must be justified explicitly")
        if scene.get("trigger") not in INPUTS:
            errors.append(f"Scene {i}: unknown trigger")
        duration = scene.get("duration_ms")
        if not isinstance(duration, int) or isinstance(duration, bool) or not 0 <= duration <= 120000:
            errors.append(f"Scene {i}: duration_ms must be 0..120000")
        else:
            total_ms += duration
        if not isinstance(scene.get("payoff"), str) or len(scene["payoff"].strip()) < 10:
            errors.append(f"Scene {i}: identify visible change or dramatic purpose")
        if scene.get("interaction"):
            for key in ("keyboard", "touch", "cancel"):
                if not isinstance(scene.get(key), str) or not scene[key].strip():
                    errors.append(f"Scene {i}: interactive scene needs {key} behavior")
    for beat in BEATS:
        if beat not in beats:
            errors.append("Missing narrative beat: " + beat)
    order = [BEATS.index(b) for b in beats]
    if order != sorted(order):
        errors.append("Narrative beats must progress opening → development → climax → resolution")
    runtime = data.get("runtime")
    if not isinstance(runtime, dict):
        errors.append("Missing runtime control plan")
        runtime = {}
    for key in ("time_owner", "reduced_motion", "no_gpu_fallback", "mobile_direction", "skip_or_replay"):
        if not isinstance(runtime.get(key), str) or len(runtime[key].strip()) < 12:
            errors.append("runtime." + key + " needs a concrete strategy")
    if runtime.get("autoplay_audio") is True:
        errors.append("Audio cannot autoplay; require deliberate user activation")
    if not isinstance(runtime.get("audio_control"), str) or not runtime["audio_control"].strip():
        errors.append("runtime.audio_control must specify mute/unmute or no audio")
    if total_ms > 9000:
        warnings.append("Long total timed sequence: validate skip affordance and perceived delay in actual browser")
    warnings.append("Runtime performance, frame pacing, rights, genuine agency and art direction require real validation")
    return {"status": "PLAN_READY_FOR_PROTOTYPE" if not errors else "INVALID",
            "errors": errors, "warnings": warnings, "declared_duration_ms": total_ms,
            "limitations": "A timeline is a production contract, not an implemented animation or FPS measurement"}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("timeline", type=Path)
    args = p.parse_args()
    try:
        if args.timeline.stat().st_size > 100_000:
            raise ValueError("Timeline exceeds 100 KB")
        result = inspect(json.loads(args.timeline.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        p.exit(2, f"INVALID INPUT: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["errors"]:
        p.exit(2)


if __name__ == "__main__":
    main()
