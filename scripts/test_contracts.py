"""Negative tests for product truth, links and regression detection."""
import unittest
from check_contracts import contract_checks,PACKAGE

class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.brief=(PACKAGE/"fixtures/fictional-product-brief.md").read_text(encoding="utf-8")
        cls.html=(PACKAGE/"examples/conversaboa-concept.html").read_text(encoding="utf-8")

    def test_valid_prototype(self):
        contract_checks(self.html,self.brief)

    def test_price_mutation_fails(self):
        with self.assertRaisesRegex(ValueError,"price"):
            contract_checks(self.html.replace("R$ 19,90","R$ 29,90"),self.brief)

    def test_primary_link_mutation_fails(self):
        modified=self.html.replace('href="#demonstracao" class="button" data-design-critical-cta',
                                   'href="#precos" class="button" data-design-critical-cta')
        self.assertNotEqual(modified,self.html)
        with self.assertRaisesRegex(ValueError,"primary CTA"):
            contract_checks(modified,self.brief)

    def test_plan_destination_mutation_fails(self):
        modified=self.html.replace('href="#precos">Rever informações do plano',
                                   'href="#demonstracao">Rever informações do plano')
        self.assertNotEqual(modified,self.html)
        with self.assertRaisesRegex(ValueError,"Plus CTA"):
            contract_checks(modified,self.brief)

    def test_broken_anchor_fails(self):
        modified=self.html.replace('href="#como-funciona"','href="#nao-existe"')
        self.assertNotEqual(modified,self.html)
        with self.assertRaisesRegex(ValueError,"broken local anchor"):
            contract_checks(modified,self.brief)

if __name__=="__main__":
    unittest.main()
