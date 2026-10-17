"""Verify blind creative pair comparison integrity without aesthetic scoring."""
import hashlib,importlib.util,json,pathlib,struct,tempfile,unittest,zlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("creative_pair",ROOT/"scripts/compare_creative_journeys.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def png(width,height):
    def chunk(k,p):return struct.pack(">I",len(p))+k+p+struct.pack(">I",zlib.crc32(k+p)&0xffffffff)
    row=b"\x00"+b"\x70\x70\x70"*width
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(row*height))+chunk(b"IEND",b"")
def make_manifest(root,width=390,scene="opening",body=None,reduced=False):
    root.mkdir(parents=True,exist_ok=True);(root/"frames").mkdir(exist_ok=True)
    raw=body or png(width,844)
    (root/"frames/test.png").write_bytes(raw)
    result={"status":"CAPTURED_FOR_HUMAN_REVIEW",
        "viewports":[{"name":"mobile","width":width,"height":844}],
        "reduced_motion":reduced,"allow_animations":False,
        "frames":[{"id":scene,"viewport":"mobile","file":"frames/test.png","sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}]}
    p=root/"manifest.json";p.write_text(json.dumps(result));return p
class PairedCreativeTests(unittest.TestCase):
    def test_ready_for_human_review_without_winner(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a");b=make_manifest(d/"b")
            r=mod.compare(a,b,d/"review")
            self.assertEqual(r["status"],"READY_FOR_BLIND_HUMAN_REVIEW_NOT_SCORED")
            self.assertTrue((d/"review/blind-review.html").is_file())
            self.assertNotIn("with_skill",(d/"review/blind-review.html").read_text())
    def test_mismatched_viewports_are_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a");b=make_manifest(d/"b",width=420)
            with self.assertRaisesRegex(ValueError,"Mismatched viewport"):mod.compare(a,b,d/"bad")
    def test_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a");b=make_manifest(d/"b")
            (d/"b/frames/test.png").write_bytes(png(390,844)+b"tamper")
            with self.assertRaisesRegex(ValueError,"SHA mismatch"):mod.compare(a,b,d/"bad")
    def test_semantic_action_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a");b=make_manifest(d/"b")
            for manifest,intent in ((a,"open-object"),(b,"download-receipt")):
                value=json.loads(manifest.read_text())
                value["frames"][0]["intent"]=intent
                value["frames"][0]["action"]={"type":"click","selector":"button"}
                value["frames"][0]["observed_state"]={"property":"text","value":"Done"}
                manifest.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError,"Mismatched semantic action"):
                mod.compare(a,b,d/"invalid")
    def test_errored_capture_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a")
            value=json.loads(a.read_text())
            value["page_errors"]=[{"error":"TypeError"}]
            a.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError,"Runtime errors"):
                mod.verify_manifest(a)

    def test_different_scenes_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a");b=make_manifest(d/"b",scene="climax")
            with self.assertRaisesRegex(ValueError,"Mismatched scene coverage"):mod.compare(a,b,d/"bad")
    def test_capture_motion_conflict_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            d=pathlib.Path(t);a=make_manifest(d/"a");b=make_manifest(d/"b",reduced=True)
            with self.assertRaisesRegex(ValueError,"Mismatched viewport or motion"):mod.compare(a,b,d/"bad")
if __name__=="__main__":unittest.main()
