"""Core packaging must be deterministic, portable and free of vendored code."""
from pathlib import Path
import hashlib
import json
import tempfile
import unittest
from zipfile import ZipFile

from build_core_package import build_archive, SKILL_REL

class CoreArchiveTests(unittest.TestCase):
    def test_excludes_vendor_and_produces_deterministic_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / SKILL_REL
            (skill / "references").mkdir(parents=True)
            (skill / "vendor" / "upstream").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: example\n---\n", encoding="utf-8")
            (skill / "references" / "guide.md").write_text("# guide", encoding="utf-8")
            (skill / "vendor" / "upstream" / "SKILL.md").write_text("# excluded", encoding="utf-8")
            (root / "LICENSE").write_text("license", encoding="utf-8")
            a, b = root / "core-a.zip", root / "core-b.zip"
            build_archive(root, a)
            build_archive(root, b)
            self.assertEqual(hashlib.sha256(a.read_bytes()).digest(), hashlib.sha256(b.read_bytes()).digest())
            with ZipFile(a) as zipfile:
                names = set(zipfile.namelist())
                self.assertIn("skills/studio-grade-web-transformation/SKILL.md", names)
                self.assertIn("skills/studio-grade-web-transformation/references/guide.md", names)
                self.assertIn("LICENSE", names)
                self.assertNotIn("skills/studio-grade-web-transformation/vendor/upstream/SKILL.md", names)
                manifest = json.loads(zipfile.read("PACKAGE_MANIFEST.json"))
                self.assertFalse(manifest["vendored_sources_included"])
                for entry in manifest["files"]:
                    self.assertEqual(hashlib.sha256(zipfile.read(entry["path"])).hexdigest(), entry["sha256"])

    def test_rejects_output_inside_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / SKILL_REL
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("ok", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_archive(root, skill / "archive.zip")

if __name__ == "__main__":
    unittest.main()
