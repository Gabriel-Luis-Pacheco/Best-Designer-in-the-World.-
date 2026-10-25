"""Regression tests for cautious, read-only file-route discovery."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / "skills/studio-grade-web-transformation"
spec = importlib.util.spec_from_file_location("design_os_route_inventory", ROOT / "brain/route_inventory.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RouteInventoryTests(unittest.TestCase):
    def test_multiple_avatar_routes_flag_possible_parallel_work_not_proven_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for route in ("src/app/(onboarding)/onboarding/avatar/page.tsx",
                          "src/app/(account)/profile/avatar/page.tsx"):
                file = root / route
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("export default function Page(){return <div>🎨👀🥔</div>}", encoding="utf-8")
            paths, truncated = module.collect_project_paths(root)
            evidence = module.inspect_routes(root, paths)
            self.assertFalse(truncated)
            self.assertEqual({x["route"] for x in evidence["routes"]},
                             {"/onboarding/avatar", "/profile/avatar"})
            self.assertIn("avatar", [x["job_hint"] for x in evidence["possible_parallel_jobs"]])
            self.assertTrue(evidence["emoji_heavy_source_candidates"])
            self.assertIn("not proof", evidence["limits"][1])

    def test_next_pages_and_svelte_and_html(self):
        self.assertEqual(module.route_for_file("src/pages/index.tsx")[0], "/")
        self.assertEqual(module.route_for_file("src/pages/settings/avatar.tsx")[0], "/settings/avatar")
        self.assertEqual(module.route_for_file("src/routes/help/+page.svelte")[0], "/help")
        self.assertEqual(module.route_for_file("index.html")[0], "/")
        self.assertIsNone(module.route_for_file("src/app/api/foo/route.ts"))
        self.assertIsNone(module.route_for_file("src/pages/api/user.ts"))
        self.assertIsNone(module.route_for_file("src/pages/_app.tsx"))

    def test_route_group_collision_is_not_proven_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            paths=["src/app/(marketing)/page.tsx", "src/app/(app)/page.tsx"]
            for rel in paths:
                file=root/rel
                file.parent.mkdir(parents=True,exist_ok=True)
                file.write_text("export default function Page() { return null }",encoding="utf-8")
            report=module.inspect_routes(root,paths)
            self.assertEqual(len(report["possible_route_collisions"]),1)
            self.assertEqual(report["possible_route_collisions"][0]["route"],"/")

    def test_untrusted_symlink_and_parent_path_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            outside=root.parent/"outside-page.tsx"
            paths=["../outside-page.tsx","src/app/page.tsx"]
            (root/"src/app").mkdir(parents=True)
            (root/"src/app/page.tsx").symlink_to(outside)
            report=module.inspect_routes(root,paths)
            self.assertEqual(report["routes"],[])

    def test_empty_and_delegated_component_do_not_invent_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            file=root/"src/app/learn/page.tsx"
            file.parent.mkdir(parents=True)
            file.write_text("export default function Page(){return <LearningPath/>}",encoding="utf-8")
            report=module.inspect_routes(root,["src/app/learn/page.tsx"])
            self.assertFalse(report["emoji_heavy_source_candidates"])
            self.assertEqual(report["routes"][0]["source_signals"]["status"],"SOURCE_ONLY")
            self.assertIn("not inspected", report["limits"][2])

if __name__=="__main__":
    unittest.main()
