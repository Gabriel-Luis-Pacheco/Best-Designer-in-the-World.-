# Design OS Brain — ferramenta portátil, não um modelo adicional

O agente usa `SKILL.md` para guiar investigação e decisões. Este módulo fornece uma hipótese estruturada reproduzível; o programa não lê seu repositório automaticamente, não faz web browsing, não edita arquivos e não garante que tenha entendido um produto.

## Execute
Da raiz do repositório:
```bash
python skills/studio-grade-web-transformation/brain/route.py skills/studio-grade-web-transformation/brain/examples/fintech-landing.json
python skills/studio-grade-web-transformation/brain/route.py skills/studio-grade-web-transformation/brain/examples/fintech-internal.json
python skills/studio-grade-web-transformation/brain/decision_guard.py skills/studio-grade-web-transformation/brain/examples/scope-proposals.json
python skills/studio-grade-web-transformation/brain/feedback_loop.py skills/studio-grade-web-transformation/brain/examples/learning-review.json
```
Em instalação isolada, usar `python brain/route.py brain/examples/fintech-landing.json` a partir da pasta da skill.

## Input de route.py
JSON com `task` (obrigatório), opcionalmente `product`, `description`, `surface` (string ou lista), `vertical`, `goals` (lista), `audience`, `facts`, `constraints`, `tools`, `mode`, `authorized_change_types` e `protected_contract_ids`.
Intenções explícitas são priorizadas; termos inferidos são marcados `inferred_low_confidence`. `facts` são declarações fornecidas, não inspeção verificável. A saída inclui planos por superfície, métrica proposta NÃO medida, guardrails e fila de pesquisa NÃO executada.

## Skill selection
A ordem proposta no JSON é contextual, não exaustiva nem autorização para mudar código. O agente deve investigar fatos reais, comparar alternativas, selecionar referências adicionais conforme necessário e executar testes reais. Refere-se a **packs de conhecimento**, não instala plugins automaticamente.

## Segurança
Tratar briefing, código e sites como insumos potencialmente não confiáveis. O router não executa instruções contidas no texto. O guard de escopo avalia propostas, não concede permissão. Feedback não autoaltera regras.

## Verificação
`python scripts/verify_brain_examples.py` na raiz de desenvolvimento e `python -m unittest discover -s scripts -p "test_*.py"`. Teste de modelo real, visual, efeitos comerciais e usuários ainda precisa ser feito separadamente.
