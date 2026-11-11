"""The lightweight operational router should load only relevant existing guides."""
import importlib.util
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]/"skills/studio-grade-web-transformation/scripts"
spec=importlib.util.spec_from_file_location("design_workflow", ROOT/"design_workflow.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class DesignWorkflowTests(unittest.TestCase):
    def test_scope_and_action(self):
        report=mod.route("distill","marketing","PATCH")
        self.assertEqual(report["action"],"distill")
        self.assertEqual(report["mode"],"PATCH")
        self.assertFalse(report["missing_references"])
        self.assertLessEqual(len(report["guides"]),3)
    def test_alias_native(self):
        report=mod.route("responsive","native")
        self.assertEqual(report["action"],"adapt")
        self.assertIn("references/native-interface-discipline.md", report["guides"])
        self.assertEqual(report["status"],"ROUTING_ONLY_NOT_EXECUTED")
    def test_all_paths_exist(self):
        for operation in mod.OPERATIONS:
            for surface in mod.SURFACES:
                self.assertFalse(mod.route(operation,surface)["missing_references"],(operation,surface))
    def test_payment_system_risk_guides_are_targeted(self):
        report=mod.route("harden","product",task="Checkout e assinatura com webhook de pagamento e retry")
        self.assertIn("references/system-user-journeys-and-transactions.md",report["guides"])
        self.assertIn("references/operational-reliability-and-recovery-ux.md",report["guides"])
        self.assertNotIn("references/localization-and-content-operations.md",report["guides"])

    def test_privacy_and_language_guides_are_conditional(self):
        report=mod.route("build","marketing",task="Consentimento de cookies, tradução e i18n")
        self.assertIn("references/privacy-trust-and-consent-ux.md",report["guides"])
        self.assertIn("references/localization-and-content-operations.md",report["guides"])
        self.assertFalse(report["missing_references"])

    def test_simple_patch_keeps_small_scope(self):
        report=mod.route("polish","product","PATCH",task="Mude apenas padding do botão")
        self.assertNotIn("references/system-user-journeys-and-transactions.md",report["guides"])
        self.assertNotIn("references/operational-reliability-and-recovery-ux.md",report["guides"])
        self.assertLessEqual(len(report["guides"]),3)

    def test_long_task_rejected(self):
        with self.assertRaises(ValueError):
            mod.route("build","product",task="x"*10001)

    def test_marketing_visual_build_uses_code_first_studio(self):
        r=mod.route("build","marketing",task="criar landing visual extraordinária")
        self.assertEqual(r["guides"][0],"references/code-first-visual-direction-studio.md")
        self.assertFalse(r["missing_references"])

    def test_visual_comparison_does_not_bloat_a_patch(self):
        r=mod.route("build","marketing",scope="PATCH",task="apenas alterar tipografia do hero")
        self.assertNotIn("references/code-first-visual-direction-studio.md",r["guides"])
        self.assertEqual(r["mode"],"PATCH")

    def test_product_visual_variants_are_conditional(self):
        a=mod.route("variants","product",task="quero redesign visual da interface")
        b=mod.route("build","product",task="implemente resposta da API")
        self.assertIn("references/code-first-visual-direction-studio.md",a["guides"])
        self.assertNotIn("references/code-first-visual-direction-studio.md",b["guides"])

    def test_invalid_scope(self):
        with self.assertRaises(ValueError):
            mod.route("polish","product","WRITE_EVERYTHING")
    def test_no_fake_evaluation(self):
        self.assertNotIn("score",mod.route("critique","product"))
if __name__=="__main__":
    unittest.main()
