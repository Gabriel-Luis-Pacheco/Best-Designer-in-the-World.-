import pathlib
import tempfile
import unittest
from verify_review_evidence import inspect

def sample(*paths):
    return {"evidence":list(paths)}

class EvidenceCheckTests(unittest.TestCase):
    def test_valid_existing_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);(p/"file.txt").write_text("real bytes",encoding="utf-8")
            report=inspect(sample("file.txt"),p)
            self.assertEqual(report["status"],"VERIFIED_LOCAL_FILES_ONLY")
            self.assertEqual(len(report["evidence"][0]["sha256"]),64)
    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            report=inspect(sample("missing.txt"),pathlib.Path(d))
            self.assertEqual(report["status"],"INCOMPLETE")
    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            report=inspect(sample("../leak.txt"),pathlib.Path(d))
            self.assertEqual(report["status"],"INCOMPLETE")
    def test_remote_is_unknown(self):
        with tempfile.TemporaryDirectory() as d:
            report=inspect(sample("https://example.org/opaque.png"),pathlib.Path(d))
            self.assertEqual(report["evidence"][0]["status"],"UNKNOWN")
