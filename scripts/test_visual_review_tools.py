"""Real regression tests for offline boards; NOT any test of visual quality."""
import importlib.util
import pathlib
import struct
import tempfile
import unittest
import zlib

ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation"
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/"scripts"/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

ASSET=load("asset_board")
REVIEW=load("visual_review_packet")

def make_png(width,height):
    def chunk(kind,payload):
        import zlib
        return struct.pack(">I",len(payload))+kind+payload+struct.pack(">I",zlib.crc32(kind+payload)&0xffffffff)
    row=b"\x00"+b"\x93\x75\x42"*width
    compressed=zlib.compress(row*height)
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,2,0,0,0))+chunk(b"IDAT",compressed)+chunk(b"IEND",b"")

class ReviewToolTests(unittest.TestCase):
    def test_asset_board_real_fixture(self):
        p=ROOT/"fixtures/brand-original.svg"
        with tempfile.TemporaryDirectory() as folder:
            out=pathlib.Path(folder)/"compare.html"
            result=ASSET.create_board(p,[p],out)
            self.assertEqual(result["status"],"BOARD_CREATED_HUMAN_REVIEW_REQUIRED")
            text=out.read_text()
            self.assertIn("CANON / ORIGINAL",text)
            self.assertIn("PROPOSAL 1",text)
            self.assertIn("default-src 'none'",text)
    def test_svg_rejects_active_content(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"evil.svg"
            p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
            with self.assertRaises(ValueError): ASSET.load_image(p)
    def test_asset_rejects_wrong_binary_header(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"fake.png";p.write_bytes(b"NOT_A_PNG")
            with self.assertRaises(ValueError): ASSET.load_image(p)
    def test_visual_review_generates_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            d=pathlib.Path(folder)
            before,after=d/"before.png",d/"after.png"
            before.write_bytes(make_png(390,600))
            after.write_bytes(make_png(390,700))
            result=REVIEW.packet(before,after,d/"comparison.html","Mobile")
            self.assertEqual(result["status"],"REVIEW_BOARD_ONLY_NOT_APPROVED")
            self.assertTrue((d/"comparison.evidence.json").is_file())
            self.assertIn("Manual review", (d/"comparison.html").read_text())
    def test_visual_review_rejects_mismatched_width(self):
        with tempfile.TemporaryDirectory() as folder:
            d=pathlib.Path(folder)
            before,after=d/"before.png",d/"after.png"
            before.write_bytes(make_png(390,700));after.write_bytes(make_png(1440,700))
            with self.assertRaises(ValueError): REVIEW.packet(before,after,d/"not-generated.html")
    def test_visual_review_rejects_nonpng(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/"fake.png";p.write_bytes(b"no")
            with self.assertRaises(ValueError):REVIEW.png(p)

if __name__=="__main__":unittest.main()
