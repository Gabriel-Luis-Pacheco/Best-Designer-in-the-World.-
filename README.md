# Best Designer in the World — Design OS Prime

**Agent Skill para reconstrução de landing pages, SaaS e interfaces com direção de arte, UX, fidelidade à marca e verificação real de qualidade.**

> Não é um template, promessa de prêmio ou garantia de conversão. É um processo para pesquisar, decidir, construir e avaliar.

## Instalação

```bash
npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.- --skill studio-grade-web-transformation
```

O arquivo principal está em [skills/studio-grade-web-transformation/SKILL.md](skills/studio-grade-web-transformation/SKILL.md). Use [docs/START_HERE.md](docs/START_HERE.md) para o fluxo de trabalho; [docs/SOURCE_MATRIX.md](docs/SOURCE_MATRIX.md) para referências e inspirações; [evals/evals.json](evals/evals.json) para casos de teste.

## Metodologia

1. Investigar o produto e seus assets reais, proteger o que já funciona.
2. Diagnosticar arquitetura e densidade visual da página inteira.
3. Pesquisar concorrentes e estúdios; **extrair mecanismos, não copiar layouts**.
4. Construir uma direção de arte e storyboards coerentes.
5. Preservar, fundir ou reconstruir seções — inclusive a página inteira.
6. Implementar cenas, componentes, estados e motion com propósito.
7. Testar a página rodando, no desktop e mobile, e verificar acessibilidade/performances.
8. Criticar o *pior elo*: nenhuma seção vazia, mockup genérico ou mascote descaracterizado pode ser ignorado.
9. Comparar resultados com e sem skill em avaliações independentes.

## Integridade

Referências externas são creditadas; não incorporar código, textos ou assets de terceiros sem verificar licença. Nada de depoimentos ou métricas inventadas. Scripts externos não são executados automaticamente. Tokens e segredos nunca devem ser publicados.

## Status

Repositório inaugurado com estrutura de skill e documentação; avaliações estéticas e comerciais dependem de testes em produto real.


## Atualização v7 — curadoria técnica e avaliação

A pesquisa cruzou **skills para IA**, design systems, práticas de UX, materiais de arte de marca e ferramentas de teste. A matriz com mais de 35 referências está em [SOURCE_MATRIX.md](docs/SOURCE_MATRIX.md); a análise do que já existia na V6.1 e do que foi acrescentado está em [GAP_ANALYSIS.md](docs/GAP_ANALYSIS.md).

A nova skill inclui **15 referências operacionais próprias**: extração de identidade e tokens, direção de arte da página inteira, personagens/mascotes canônicos, prova visual do produto, implementação de qualidade, crítica de estúdio e pesquisa com usuários.

### Harness de qualidade (não é promessa de resultado)

- [12 casos de avaliação](evals/evals.json) com resultados esperados.
- [Runbook A/B com e sem a skill](docs/EVALUATION_RUNBOOK.md), idealmente com avaliação cega.
- [Rubrica humana](docs/QUALITY_RUBRIC.md) com bloqueio por P0/P1 e pior elo.
- [Validador estrutural](scripts/check_evals.py), que não avalia estética:
  `python scripts/check_evals.py`
- [Resumidor de revisão humana](scripts/score_review.py), que não inventa notas.
- [Exemplo Playwright](examples/playwright-visual.spec.ts) para snapshots em projeto com a dependência instalada.
- [Decisões preservadas de V1–V6.1](docs/LEGACY_V6_1_DECISIONS.md).

**Status real:** documentos, arquivos e testes estruturais publicáveis. Ainda é necessário executar A/B num projeto real para afirmar que esta versão produziu interfaces melhores que a anterior.
