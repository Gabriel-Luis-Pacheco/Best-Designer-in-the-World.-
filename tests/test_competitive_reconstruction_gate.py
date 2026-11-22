"""Regression tests for evidence-based full-page competitor reconstruction."""
import copy
import importlib.util
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

SCRIPT = (Path(__file__).resolve().parents[1] /
          "skills/studio-grade-web-transformation/scripts/competitive_reconstruction_gate.py")
spec = importlib.util.spec_from_file_location("competitive_reconstruction_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

COPY = "This source headline uses a direct category promise and specific benefit"
BODY = "Each paragraph changes the reader's belief with a clear customer example"
CTA = "Primary action starts a free trial; supporting proof precedes the form"
COMPOSITION = "A single large product demonstration anchors the reading order and spacing"
MEDIA = "Real product screenshot; no animation was observed in this static state"
MOBILE = "Visual demonstration follows short offer text; CTA remains visible"


def scene(name, order, kind="MARKETING_SECTION"):
    return dict(
        id=name, order=order, kind=kind,
        visitor_question="Can a relevant buyer recognize a concrete task benefit?",
        headline_strategy=COPY, body_copy_strategy=BODY,
        cta_and_proof=CTA, composition=COMPOSITION,
        media_and_motion=MEDIA, mobile_behavior=MOBILE,
        copy_inventory_complete=True,
        text_items=[
            {"id":"headline", "role":"HEADLINE",
             "observed_purpose":"Describe the category and specific CRM task for decision makers",
             "strategy":"Concrete category-first headline with one plausible outcome"},
            {"id":"cta", "role":"CTA",
             "observed_purpose":"Tell the buyer the exact action available before a demo",
             "strategy":"One primary trial verb with a clearly subordinate demo option"}
        ],
        media_items=[{"kind":"SCREENSHOT",
                      "observed_role":"Authentic product surface demonstrates the practical lead-creation task"}],
        desktop_capture=f"shots/primary-{name}-desktop.png",
        mobile_capture=f"shots/primary-{name}-mobile.png"
    )


def packet():
    competitors = []
    for n in range(3):
        ident = f"crm-{n}"
        primary = n == 0
        scenes = [scene(name, i+1) for i, name in enumerate(("hero","proof","pricing"))] if primary else [
            dict(scene("main", 1), desktop_capture=None, mobile_capture=None)
        ]
        competitors.append({
            "id": ident, "kind":"DIRECT", "role":"PRIMARY" if primary else "SUPPORT",
            "url":f"https://example.org/crm/{n}", "inspection_status":"INSPECTED",
            "observed_date":"2026-11-22", "access_limit":"",
            "desktop_full_page": f"shots/{ident}-full-desktop.png",
            "mobile_full_page": f"shots/{ident}-full-mobile.png",
            "scroll_sweep":{"from_top_to_footer": True,
                            "observed_scene_ids":[x["id"] for x in scenes]},
            "scenes":scenes, "flows":[]
        })
    return {
        "schema_version":1, "scope":"LANDING", "mode":"REDESIGN",
        "project":{
            "audience":"B2B team lead comparing AI CRM workflow tools",
            "actual_offer":"Real CRM trial and honest functionality known from our code",
            "first_value":"User creates a lead and records the next action",
            "protected_constraints":"Keep routes, customer rights, privacy and verified prices",
            "requested_surfaces":["hero","proof","pricing"],"requested_flows":[]
        },
        "research":{"selection_rationale":"We selected same-job CRM tools with comparable audiences and sales processes",
                    "shortfall_reason":"The remaining direct sites require unprovided research access or deeper browser coverage",
                    "competitors": competitors},
        "target":{"surfaces":[{
                "id":name,
                "dominant_source":{"competitor_id":"crm-0","scene_id":name},
                "transfer":"ADAPT",
                "user_decision":"Make the product task and next action obvious without invented numbers",
                "copy_strategy_transfer":"Recreate the observed claim/objection structure using original wording",
                "composition_transfer":"Use observed product-first hierarchy with authentic visual proof",
                "media_motion_transfer":"Use genuine local product views; avoid fake movement",
                "departure_rationale":"Different brand assets, feature scope and accessible interface constraints",
                "brand_and_rights_boundary":"No source code, proprietary copy, photographs or brand-distinctive designs",
                "source_files":["src/landing.html"],
                "desktop_after":f"shots/target-{name}-desktop.png",
                "mobile_after":f"shots/target-{name}-mobile.png"
            } for name in ("hero","proof","pricing")],
            "flows":[],
            "primary_journey":{"status":"PASS","evidence":"evidence/journey.txt"}
        },
        "review":{"reviewer":"SELF_REVIEW","verdict":"PASS",
                  "side_by_side_analysis":"All three target scenes were compared at matched viewports, including copy, spacing and CTA behavior",
                  "critical_findings":[]}
    }


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "shots").mkdir()
        (self.root / "src").mkdir()
        (self.root / "evidence").mkdir()
        (self.root / "src/landing.html").write_text(
            "<!doctype html><html><body><main>Real implemented example</main></body></html>")
        (self.root / "evidence/journey.txt").write_text(
            "Browser navigation confirmed actual CTA reached user first value and result.")
        p = packet()
        paths = []
        for ref in p["research"]["competitors"]:
            paths += [ref[f"{v}_full_page"] for v in ("desktop","mobile")]
            for scene_row in ref["scenes"]:
                paths += [scene_row[f"{v}_capture"] for v in ("desktop","mobile") if scene_row[f"{v}_capture"]]
        for x in p["target"]["surfaces"]:
            paths += [x[f"{v}_after"] for v in ("desktop","mobile")]
        for stage in ("source", "target"):
            paths += [f"shots/flow-{stage}-create-{view}.png" for view in ("desktop", "mobile")]
        def chunk(kind, data):
            b = kind + data
            return struct.pack(">I", len(data)) + b + struct.pack(">I", zlib.crc32(b))
        for seed, name in enumerate(paths, start=1):
            width, height = (960, 700) if "desktop" in name else (390, 800)
            rgba = bytes((seed*19 % 256, seed*23 % 256, seed*31 % 256, 255))
            data = (b"\x89PNG\r\n\x1a\n" +
                    chunk(b"IHDR",struct.pack(">2I5B",width,height,8,6,0,0,0)) +
                    chunk(b"IDAT",zlib.compress((b"\x00" + rgba*width)*height)) +
                    chunk(b"IEND",b""))
            (self.root / name).write_bytes(data)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_complete_packet_only_ready_for_human_review(self):
        result = gate.inspect(packet(),self.root)
        self.assertEqual(result["status"],"READY_FOR_HUMAN_REVIEW",result)
        self.assertTrue(any("human" in s.lower() for s in result["warnings"]))

    def test_only_competitor_hero_is_not_full_scroll(self):
        p = packet()
        p["research"]["competitors"][0]["scenes"] = [p["research"]["competitors"][0]["scenes"][0]]
        p["research"]["competitors"][0]["scroll_sweep"]["observed_scene_ids"] = ["hero"]
        self.assertEqual(gate.inspect(p,self.root)["status"],"NEEDS_EVIDENCE")

    def test_missing_section_copy_inventory_is_not_approved(self):
        p = packet()
        p["research"]["competitors"][0]["scenes"][1]["text_items"] = []
        self.assertEqual(gate.inspect(p,self.root)["status"],"NEEDS_EVIDENCE")

    def test_unobserved_animation_is_not_fake_proof(self):
        p = packet()
        p["research"]["competitors"][0]["scenes"][1]["media_items"] = [
            {"kind":"VIDEO", "observed_role":"Hero video demonstrates a workflow through motion"}
        ]
        self.assertEqual(gate.inspect(p,self.root)["status"],"NEEDS_EVIDENCE")

    def test_unmapped_target_section_fails_coverage(self):
        p = packet()
        p["target"]["surfaces"].pop()
        self.assertEqual(gate.inspect(p,self.root)["status"],"INVALID")

    def test_fictitious_reference_id_not_accepted(self):
        p = packet()
        p["target"]["surfaces"][0]["dominant_source"]["competitor_id"] = "fake-crm"
        self.assertEqual(gate.inspect(p,self.root)["status"],"NEEDS_EVIDENCE")

    def test_reused_screenshot_bytes_not_independent_evidence(self):
        p = packet()
        p["target"]["surfaces"][0]["desktop_after"] = p["research"]["competitors"][0]["desktop_full_page"]
        r = gate.inspect(p,self.root)
        self.assertEqual(r["status"],"NEEDS_EVIDENCE")
        self.assertTrue(any("identical" in s for s in r["missing"]))

    def test_missing_mobile_capture_not_approved(self):
        p = packet()
        p["target"]["surfaces"][0]["mobile_after"] = None
        self.assertEqual(gate.inspect(p,self.root)["status"],"NEEDS_EVIDENCE")

    def test_failed_real_user_journey_blocks(self):
        p = packet()
        p["target"]["primary_journey"]["status"] = "FAIL"
        self.assertEqual(gate.inspect(p,self.root)["status"],"BLOCKED")

    def test_scope_system_requires_actual_target_flow(self):
        p = packet()
        p["scope"] = "SYSTEM"
        p["project"]["requested_flows"] = ["first-lead"]
        self.assertEqual(gate.inspect(p,self.root)["status"],"INVALID")

    def test_system_with_matching_source_and_tested_flow(self):
        p = packet()
        p["scope"] = "SYSTEM"
        p["project"]["requested_flows"] = ["first-lead"]
        p["research"]["competitors"][0]["flows"] = [{
            "id":"lead-creation", "inspection_status":"INSPECTED",
            "steps":[{"id":"create",
                      "access_state":"PUBLIC_DEMO_GENUINELY_OBSERVED",
                      "control_and_feedback":"Lead form presents fields with inline validation and next step",
                      "branching_and_errors":"Back, save and empty-validation states were observed and recorded",
                      "desktop_capture":"shots/flow-source-create-desktop.png",
                      "mobile_capture":"shots/flow-source-create-mobile.png"}]
        }]
        p["target"]["flows"] = [{
            "id":"first-lead",
            "dominant_source_flow":{"competitor_id":"crm-0","flow_id":"lead-creation"},
            "mapped_source_steps":["create"],
            "step_by_step_transfer":"Implemented comparable create flow with inline feedback, success and return",
            "steps":[{"source_step":"create",
                      "feedback_and_errors":"Inline validation, empty list and success return states are implemented",
                      "desktop_capture":"shots/flow-target-create-desktop.png",
                      "mobile_capture":"shots/flow-target-create-mobile.png"}],
            "test_status":"PASS",
            "test_evidence":"evidence/journey.txt"
        }]
        self.assertEqual(gate.inspect(p,self.root)["status"],"READY_FOR_HUMAN_REVIEW")


if __name__ == "__main__":
    unittest.main()
