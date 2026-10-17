"""Regression tests of offline journey board, NOT aesthetic scoring."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec = importlib.util.spec_from_file_location("journey_board", ROOT / "scripts/journey_board.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def png(width=390, height=200):
    def chunk(tag, value):
        return struct.pack(">I", len(value)) + tag + value + struct.pack(">I", zlib.crc32(tag + value) & 0xffffffff)
    row = b"\x00" + b"\x42\x72\x95" * width
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(row * height)) + chunk(b"IEND", b""))

class JourneyTests(unittest.TestCase):
    def test_stage_board_is_not_aesthetic_winner(self):
        with tempfile.TemporaryDirectory() as folder:
            d = Path(folder)
            (d / "a.png").write_bytes(png())
            (d / "b.png").write_bytes(png(1440))
            data = {"title": "<script>hi</script>", "required_beats": ["opening", "middle"],
                    "candidates": [
                        {"id": "skill", "frames": [{"beat": "opening", "path": "a.png", "viewport": "390x800", "state": "rest"}]},
                        {"id": "baseline", "frames": [{"beat": "opening", "path": "b.png", "viewport": "1440x800", "state": "rest"}]}]}
            (d / "manifest.json").write_text(json.dumps(data))
            result = module.build(d / "manifest.json", d / "board.html")
            self.assertEqual(result["status"], "EVIDENCE_BOARD_ONLY_NO_AUTOMATIC_WINNER")
            kinds = {w["kind"] for w in result["warnings"]}
            self.assertIn("MISSING_REQUIRED_FRAME", kinds)
            self.assertIn("CAPTURE_VIEWPORT_MISMATCH", kinds)
            body = (d / "board.html").read_text()
            self.assertIn("&lt;script&gt;", body)
            self.assertNotIn("<script>hi</script>", body)
            self.assertIn("default-src 'none'", body)
            self.assertNotIn("aesthetic_score", result)
            self.assertTrue((d / "board.evidence.json").is_file())

    def test_duplicate_beats_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            d = Path(folder)
            (d / "shot.png").write_bytes(png())
            frame = {"beat": "opening", "path": "shot.png"}
            data = {"candidates": [{"id": "a", "frames": [frame, frame]},
                                   {"id": "b", "frames": [frame]}]}
            (d / "manifest.json").write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                module.build(d / "manifest.json", d / "board.html")

    def test_parent_path_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            d = Path(folder)
            data = {"candidates": [{"id": "a", "frames": [{"beat": "opening", "path": "../secret.png"}]},
                                   {"id": "b", "frames": [{"beat": "opening", "path": "../secret.png"}]}]}
            (d / "manifest.json").write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "relative PNG"):
                module.build(d / "manifest.json", d / "board.html")

if __name__ == "__main__":
    unittest.main()
