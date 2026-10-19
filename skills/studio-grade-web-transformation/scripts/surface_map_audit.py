#!/usr/bin/env python3
"""Advisory audit of a DECLARED screen inventory, not a source/runtime design judge."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

MEDIA = {"text", "emoji", "product_ui", "custom_visual", "diagram", "data_view", "table", "photography", "other"}
KINDS = {"product", "landing", "internal", "read", "commerce", "experience"}

def inspect(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("surfaces"), list):
        raise ValueError("Expected an object containing surfaces array")
    surfaces = payload["surfaces"]
    if len(surfaces) > 500:
        raise ValueError("Maximum 500 surfaces")
    known = set()
    jobs = defaultdict(list)
    routes = defaultdict(list)
    findings = []

    def review(code, screen_ids, reason):
        findings.append({"code": code, "severity": "REVIEW", "surfaces": screen_ids,
                         "reason": reason, "certainty": "DECLARED_ONLY"})

    for n, s in enumerate(surfaces):
        if not isinstance(s, dict):
            raise ValueError(f"Surface {n} must be an object")
        for key in ("id", "route", "job", "surface_type", "primary_representation"):
            if not isinstance(s.get(key), str) or not s[key].strip():
                raise ValueError(f"Surface {n} needs nonempty {key}")
        sid = s["id"]
        if sid in known:
            raise ValueError(f"Duplicate surface ID: {sid}")
        known.add(sid)
        if s["surface_type"] not in KINDS or s["primary_representation"] not in MEDIA:
            raise ValueError(f"Invalid kind or representation: {sid}")
        if not isinstance(s.get("canonical", False), bool):
            raise ValueError(f"canonical must be boolean: {sid}")
        if not isinstance(s.get("interaction_required", False), bool):
            raise ValueError(f"interaction_required must be boolean: {sid}")
        blocks = s.get("content_blocks", [])
        if not isinstance(blocks, list) or not all(isinstance(b, str) for b in blocks):
            raise ValueError(f"content_blocks must be strings: {sid}")
        routes[s["route"]].append(sid)
        if s["surface_type"] == "product":
            jobs[s["job"].casefold().strip()].append(s)
            if s["primary_representation"] == "emoji":
                review("EMOJI_AS_PRIMARY_UI_REVIEW", [sid], "Emoji declared as the primary product representation.")
            if s.get("interaction_required") and s["primary_representation"] == "text":
                review("TEXT_REPLACING_INTERACTION_REVIEW", [sid], "Interactive job declared with text-only representation.")
            if s["primary_representation"] in ("emoji", "text") and sum(b in ("paragraph", "copy_card", "text_panel") for b in blocks) >= 4:
                review("REPEATED_EXPLANATION_REVIEW", [sid], "Four or more copy-only blocks; inspect actual UX.")

    for route, ids in routes.items():
        if len(ids) > 1:
            review("SHARED_ROUTE_REVIEW", ids, f"Multiple screens declare route {route}; verify variants.")
    for job, group in jobs.items():
        if len(group) < 2:
            continue
        owners = [s for s in group if s.get("canonical")]
        if len(owners) != 1:
            review("DUPLICATE_JOB_OWNERSHIP_REVIEW", [s["id"] for s in group],
                   f"Job {job} declares {len(owners)} canonical owners.")
        else:
            owner = owners[0]["id"]
            for s in group:
                if s["id"] != owner and s.get("variant_of") != owner and not s.get("distinct_reason", "").strip():
                    review("UNEXPLAINED_PARALLEL_SCREEN_REVIEW", [owner, s["id"]],
                           f"Job {job} has another screen with no declared reused flow or distinct purpose.")
    by_id = {s["id"]: s for s in surfaces}
    for s in surfaces:
        ref = s.get("variant_of")
        if not ref:
            continue
        owner = by_id.get(ref)
        if owner is None:
            raise ValueError(f"variant_of points to missing ID on {s['id']}")
        if not owner.get("canonical") or s["job"].casefold().strip() != owner["job"].casefold().strip():
            raise ValueError(f"variant_of must reference a canonical screen with the same user job on {s['id']}")

    return {"status": "REVIEW_REQUIRED" if findings else "NO_DECLARED_FLAGS",
            "surfaces_seen": len(surfaces), "jobs_compared": len(jobs), "findings": findings,
            "method": "DECLARED_INVENTORY_ONLY",
            "limitations": ["Does not discover React routes or component data flow",
                            "Does not inspect pixels, prove duplicates or measure user experience",
                            "No flags does not mean a good design"]}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("inventory", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    try:
        if not args.inventory.is_file() or args.inventory.stat().st_size > 1_000_000:
            raise ValueError("Missing or oversized inventory")
        report = inspect(json.loads(args.inventory.read_text(encoding="utf-8")))
        content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(content, encoding="utf-8")
        print(content, end="")
    except (OSError, ValueError) as err:
        p.exit(2, f"INVALID INVENTORY: {err}\n")

if __name__ == "__main__":
    main()
