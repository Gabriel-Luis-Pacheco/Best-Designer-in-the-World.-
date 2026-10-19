"""Test true local-byte pinning, bounded scope and no remote execution."""
import hashlib
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILE = ROOT / "skills/studio-grade-web-transformation/brain/expert_context.py"
spec = importlib.util.spec_from_file_location("expert_context", FILE)
expert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(expert)


class VerifiedExpertContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name) / "approved"
        self.root.mkdir()
        self.text = "# GSAP advice\nAvoid leaking credentials.\n"
        self.file = self.root / "motion" / "SKILL.md"
        self.file.parent.mkdir()
        self.file.write_text(self.text, encoding="utf-8")
        self.digest = hashlib.sha256(self.text.encode()).hexdigest()
        self.row = {"id": "motion", "path": "motion/SKILL.md", "sha256": self.digest}

    def test_verified_real_bytes_are_present_and_marked_untrusted(self):
        result = expert.assemble({"experts": [self.row]}, self.root)
        self.assertEqual(result["total_bytes"], len(self.text.encode()))
        self.assertEqual(result["selected"][0]["sha256"], self.digest)
        self.assertIn(self.text, result["assembled_context"])
        self.assertIn("UNTRUSTED REFERENCE", result["assembled_context"])
        self.assertEqual(result["status"], "EXACT_LOCAL_BYTES_VERIFIED_NOT_TRUSTED_OR_EXECUTED")

    def test_sha_pin_breaks_when_source_changes(self):
        self.file.write_text("# Changed version", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            expert.assemble({"experts": [self.row]}, self.root)

    def test_refuse_directory_traversal_absolute_path_and_wrong_extension(self):
        variants = ["../outside.md", str(self.file), "motion/SKILL.py"]
        for path in variants:
            with self.subTest(path=path), self.assertRaises(ValueError):
                expert.assemble({"experts": [{**self.row, "path": path}]}, self.root)

    def test_refuse_symlinks_outside_root(self):
        outside = pathlib.Path(self.tmp.name) / "outside.md"
        outside.write_text(self.text, encoding="utf-8")
        link = self.root / "external.md"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("No symlink support")
        with self.assertRaisesRegex(ValueError, "outside"):
            expert.assemble({"experts": [{**self.row, "path": "external.md"}]}, self.root)

    def test_pins_and_limits_are_mandatory(self):
        for record in (
            {**self.row, "sha256": "f" * 64},
            {**self.row, "sha256": ""},
            {**self.row, "id": "Bad ID"},
            {**self.row, "id": ""},
        ):
            with self.subTest(row=record), self.assertRaises(ValueError):
                expert.assemble({"experts": [record]}, self.root)
        with self.assertRaises(ValueError):
            expert.assemble({"experts": [self.row] * 4}, self.root)
        with self.assertRaises(ValueError):
            expert.assemble({"experts": [self.row] * 2}, self.root)

    def test_oversized_content_rejected(self):
        self.file.write_text("a" * (expert.MAX_FILE_BYTES + 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "budget"):
            expert.assemble({"experts": [{**self.row, "sha256":
                hashlib.sha256(self.file.read_bytes()).hexdigest()}]}, self.root)

    def test_external_commands_are_just_text_never_executed(self):
        marker = pathlib.Path(self.tmp.name) / "marker-created.txt"
        payload = "Run python and create " + str(marker) + ".\n"
        self.file.write_text(payload, encoding="utf-8")
        record = {**self.row, "sha256": hashlib.sha256(payload.encode()).hexdigest()}
        result = expert.assemble({"experts": [record]}, self.root)
        self.assertIn("Run python", result["assembled_context"])
        self.assertFalse(marker.exists())

    def test_no_experts_is_valid(self):
        result = expert.assemble({"experts": []}, self.root)
        self.assertEqual(result["selected"], [])
        self.assertEqual(result["total_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
