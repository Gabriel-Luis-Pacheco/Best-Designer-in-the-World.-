"""Regression checks for declared product-surface triage; not aesthetic scoring."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec = importlib.util.spec_from_file_location("surface_map_audit", ROOT / "scripts/surface_map_audit.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def screen(sid, route, job, representation="product_ui", **options):
    return {"id": sid, "route": route, "job": job, "surface_type": "product",
            "primary_representation": representation, **options}

class SurfaceMapTests(unittest.TestCase):
    def test_two_avatar_editors_have_no_single_owner(self):
        payload = {"surfaces": [screen("a", "/welcome/avatar", "avatar", canonical=True),
                                screen("b", "/profile/avatar", "avatar", canonical=True)]}
        self.assertIn("DUPLICATE_JOB_OWNERSHIP_REVIEW",
                      [x["code"] for x in m.inspect(payload)["findings"]])

    def test_shared_component_flow_is_not_forced_into_one_route(self):
        payload = {"surfaces": [screen("owner", "/profile/avatar", "avatar", canonical=True),
                                screen("entry", "/welcome/avatar", "avatar", variant_of="owner")]}
        self.assertEqual(m.inspect(payload)["status"], "NO_DECLARED_FLAGS")

    def test_emoji_text_and_repeated_copy_are_review_candidates(self):
        payload = {"surfaces": [
            screen("path", "/learn", "lessons", "emoji"),
            screen("speaking", "/speak", "speak", "text", interaction_required=True,
                   content_blocks=["paragraph"] * 5)]}
        codes = [x["code"] for x in m.inspect(payload)["findings"]]
        for code in ("EMOJI_AS_PRIMARY_UI_REVIEW", "TEXT_REPLACING_INTERACTION_REVIEW",
                     "REPEATED_EXPLANATION_REVIEW"):
            self.assertIn(code, codes)
        self.assertTrue(all(x["severity"] == "REVIEW" for x in m.inspect(payload)["findings"]))

    def test_reading_screen_is_not_penalized_for_text(self):
        payload = {"surfaces": [{"id": "terms", "route": "/terms", "job": "read",
                  "surface_type": "read", "primary_representation": "text",
                  "content_blocks": ["paragraph"] * 10}]}
        self.assertEqual(m.inspect(payload)["status"], "NO_DECLARED_FLAGS")

    def test_unexplained_parallel_screen(self):
        payload = {"surfaces": [screen("main", "/profile/avatar", "avatar", canonical=True),
                                screen("other", "/welcome/avatar", "avatar")]}
        self.assertIn("UNEXPLAINED_PARALLEL_SCREEN_REVIEW",
                      [x["code"] for x in m.inspect(payload)["findings"]])

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            m.inspect({"surfaces": [screen("a", "/a", "a", variant_of="missing")]})
        with self.assertRaises(ValueError):
            m.inspect({"surfaces": [screen("a", "/a", "a"), screen("a", "/b", "b")]})
        with self.assertRaises(ValueError):
            m.inspect({"surfaces": "invalid"})
if __name__ == "__main__":
    unittest.main()
