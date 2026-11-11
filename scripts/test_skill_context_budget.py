#!/usr/bin/env python3
"""Static safeguards for reduced SKILL.md; not a runtime token benchmark."""
import unittest
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
SK=ROOT/"skills/studio-grade-web-transformation"
class EntrypointChecks(unittest.TestCase):
    def test_size_and_required_terms(self):
        s=(SK/"SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(s),10000)
        for x in ["PATCH","REFINE","AUDIT","REDESIGN","REBUILD","Original-brief compass","Course correction","NOT VERIFIED","Independent critique","LANDING / MARKETING","CUT"]:
            self.assertIn(x.casefold(),s.casefold())
    def test_references_exist(self):
        s=(SK/"SKILL.md").read_text(encoding="utf-8")
        for name in set(re.findall(r"references/([a-z0-9.-]+\.md)",s)):
            self.assertTrue((SK/"references"/name).exists(),name)
    def test_archive(self):
        t=(SK/"references/archived-v14-core-protocol.md").read_text(encoding="utf-8")
        self.assertIn("## 5. Deliver with proportionate evidence",t)
        self.assertIn("Revenue-Centric Design",t)
if __name__=="__main__":
    unittest.main()
