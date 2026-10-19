"""Adversarial tests for actual git diff filename scope."""
import importlib.util
import pathlib
import tempfile
import subprocess
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify_change_scope",ROOT/"scripts/verify_change_scope.py")
scope=importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)

class ChangeScopeTests(unittest.TestCase):
    def test_allow_and_protected_precedence(self):
        policy={"version":1,"allowed_paths":["src/*"],"protected_paths":["src/payments/*"]}
        out=scope.assess(["src/ui.ts","src/payments/card.ts"],policy)
        self.assertEqual(out["decision"],"BLOCK")
        self.assertEqual(out["changes"][1]["status"],"BLOCK_PROTECTED")
    def test_unlisted_path_is_blocked(self):
        out=scope.assess(["backend/server.ts"],{"version":1,"allowed_paths":["src/*"]})
        self.assertEqual(out["changes"][0]["status"],"BLOCK_OUTSIDE_SCOPE")
    def test_empty_diff_and_unsafe_paths(self):
        policy={"version":1,"allowed_paths":["src/*"]}
        self.assertEqual(scope.assess([],policy)["decision"],"NO_CHANGES")
        for path in ("../private/file","/tmp/file","src/../private"):
            with self.assertRaises(ValueError):scope.assess([path],policy)
    def test_git_diff_records_both_sides_of_rename(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            def git(*args):
                run=subprocess.run(["git","-C",str(root),*args],check=True,capture_output=True)
                return run.stdout.decode().strip()
            git("init","-q")
            git("config","user.email","designos@example.test")
            git("config","user.name","Design OS CI")
            (root/"old.txt").write_text("hello test",encoding="utf-8")
            git("add","old.txt");git("commit","-qm","first")
            base=git("rev-parse","HEAD")
            git("mv","old.txt","new.txt")
            git("commit","-qam","rename")
            self.assertEqual(scope.git_changed_paths(root,base,"HEAD"),["new.txt","old.txt"])
