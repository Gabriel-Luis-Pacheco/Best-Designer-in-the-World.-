"""Read-only component delivery gate must never approve from self-report alone."""
from __future__ import annotations
import importlib.util
import struct
import zlib
import tempfile
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
spec=importlib.util.spec_from_file_location("component_delivery_gate",ROOT/"scripts/component_delivery_gate.py")
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def tiny_valid_png():
    """Create a real 1×1 RGBA PNG, with valid IHDR/IDAT/IEND CRCs."""
    def chunk(tag, body):
        return (struct.pack(">I",len(body))+tag+body+
                struct.pack(">I",zlib.crc32(tag+body)&0xffffffff))
    ihdr=struct.pack(">IIBBBBB",1,1,8,6,0,0,0)
    return (b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",ihdr)+
            chunk(b"IDAT",zlib.compress(b"\x00\xff\x00\x00\xff"))+
            chunk(b"IEND",b""))


def packet(component="hero",mode="REDESIGN",surface="marketing"):
    return {
        "schema_version":1,"component_id":component,"mode":mode,"surface":surface,
        "stage_records":[],"expert_application_log":[],
        "visual_artifacts":{},"critical_flows":[],
        "editorial_review":{"status":"SELF_REVIEW_ONLY"},
        "blocking_issues":[]
    }


class ComponentDeliveryTests(unittest.TestCase):
    def test_no_evidence_never_passes(self):
        with tempfile.TemporaryDirectory() as d:
            p=gate.inspect(packet(),Path(d))
            self.assertEqual(p["status"],"NEEDS_EVIDENCE")
            self.assertIn("truth",str(p["missing_evidence"]))

    def test_false_stage_done_is_not_accepted(self):
        x=packet()
        x["stage_records"]=[{"phase_id":"truth","status":"DONE",
                             "summary":"Claims and product facts audited against source files.",
                             "evidence_path":"proof/fake.md"}]
        with tempfile.TemporaryDirectory() as d:
            p=gate.inspect(x,Path(d))
            self.assertEqual(p["status"],"NEEDS_EVIDENCE")
            self.assertIn("truth: DONE requires existing artifact",str(p["missing_evidence"]))

    def test_unsafe_evidence_path_is_rejected(self):
        x=packet(mode="PATCH")
        x["stage_records"]=[{"phase_id":"truth","status":"DONE",
                             "summary":"Product facts inspected and recorded for regression avoidance.",
                             "evidence_path":"../../private.txt"}]
        with tempfile.TemporaryDirectory() as d:
            p=gate.inspect(x,Path(d))
            self.assertEqual(p["status"],"NEEDS_EVIDENCE")

    def test_known_failed_primary_flow_blocks(self):
        x=packet()
        x["critical_flows"]=[{"id":"Checkout payment","status":"TESTED_FAIL"}]
        with tempfile.TemporaryDirectory() as d:
            p=gate.inspect(x,Path(d))
            self.assertEqual(p["status"],"BLOCKED")
            self.assertIn("Checkout payment",str(p["blockers"]))

    def test_cannot_claim_skill_applied_without_evidence(self):
        x=packet(mode="PATCH")
        x["expert_application_log"]=[{"id":"marketing-copywriting","status":"APPLIED",
                                      "specific_contribution":"Rewrote copy"}]
        with tempfile.TemporaryDirectory() as d:
            p=gate.inspect(x,Path(d))
            self.assertEqual(p["status"],"NEEDS_EVIDENCE")
            self.assertIn("marketing-copywriting",str(p["missing_evidence"]))

    def test_cannot_claim_real_human_without_documentation(self):
        x=packet()
        x["editorial_review"]={"status":"HUMAN_REVIEWED"}
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(gate.inspect(x,Path(d))["status"],"NEEDS_EVIDENCE")

    def test_structural_ready_does_not_claim_actual_visual_or_human_approval(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            phases=["truth","ux","engineering","accessibility","render"]
            (root/"proof.md").write_text("Evidence from local source files and observed task behavior.",encoding="utf-8")
            (root/"pic.png").write_bytes(tiny_valid_png())
            x=packet(mode="PATCH")
            x["stage_records"]=[
                {"phase_id":phase,"status":"DONE","evidence_path":"proof.md",
                 "summary":"Observed product behavior and documented tests for "+phase}
                for phase in phases]
            x["visual_artifacts"]={"desktop_after":"pic.png"}
            x["critical_flows"]=[{"id":"Main path","status":"TESTED_PASS","evidence_path":"proof.md"}]
            p=gate.inspect(x,root)
            self.assertEqual(p["status"],"READY_FOR_HUMAN_REVIEW")
            self.assertIn("not proof",str(p["limitations"]).lower())

    def test_broken_png_header_does_not_pass_visual_proof(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"fake.png").write_bytes(b"\x89PNG\r\n\x1a\n"+b"x"*120)
            self.assertFalse(gate._safe_artifact(root,"fake.png",image=True))

    def test_incompatible_component_surface_fails(self):
        x=packet(surface="internal")
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(gate.inspect(x,Path(d))["status"],"INVALID")

    def test_invalid_unknown_phase_and_duplicate(self):
        x=packet()
        x["stage_records"]=[
            {"phase_id":"invented","status":"DONE"},
            {"phase_id":"truth","status":"DONE"},
            {"phase_id":"truth","status":"DONE"}]
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(gate.inspect(x,Path(d))["status"],"INVALID")

    def test_research_packet_missing_when_market_marked_done(self):
        x=packet()
        x["stage_records"]=[{"phase_id":"market","status":"DONE",
                             "summary":"Studied matched competitors and extracted mechanisms",
                             "evidence_path":"proof.md"}]
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/"proof.md").write_text("Observed benchmark notes.",encoding="utf-8")
            p=gate.inspect(x,Path(d))
            self.assertIn("market DONE requires existing JSON research_packet",str(p["missing_evidence"]))

    def test_unreviewed_copy_is_not_ready(self):
        x=packet()
        x["editorial_review"]={"status":"NOT_REVIEWED"}
        with tempfile.TemporaryDirectory() as d:
            p=gate.inspect(x,Path(d))
            self.assertIn("editorial not reviewed",str(p["missing_evidence"]))


if __name__=="__main__":
    unittest.main()
