# Design OS Prime v11.7.0

Skill aberta de direção de arte, UX/UI, implementação e revisão de sites e produtos digitais. O nome do repositório expressa uma ambição; qualidade precisa aparecer no produto renderizado e em testes reais.

## Instalar

```bash
npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.- --skill studio-grade-web-transformation
```

[Comece pelo SKILL.md](skills/studio-grade-web-transformation/SKILL.md). Para instalação manual, copie a pasta inteira `skills/studio-grade-web-transformation`, preservando referências e ferramentas. O pacote funciona sem executar os scripts opcionais.

## O que esta versão melhora

- **Execução mais clara:** núcleo reduzido de aproximadamente 3.622 para 1.611 palavras, com uma sequência única de investigação, escolha, implementação, inspeção e correção. Histórico de releases fica no [CHANGELOG](CHANGELOG.md).
- **Direções ligadas ao contexto:** o laboratório opcional diferencia dez superfícies e considera tipos de evidência declarados, fatos do produto, tarefas e assets. As saídas continuam sendo hipóteses estruturais, sem geração de pixels ou julgamento estético.
- **Preservação de decisões:** PATCH e AUDIT não abrem conceitos; REFINE só explora alternativas por opt-in; uma direção marcada como escolhida é preservada.
- **Informação com objetivo próprio:** documentação recebe orientações de leitura, busca e navegação, inclusive no contexto realmente injetado pelo runner de avaliação.
- **Melhor interpretação de escopo:** recusas próximas de comandos não devem virar pedidos de implementação. Menções de checkout e dashboard em frases de preservação continuam relevantes. As heurísticas exigem revisão do agente.
- **Revisão proporcional:** recursos existentes continuam disponíveis por necessidade; não é preciso carregar todo o catálogo ou preencher templates para fazer uma alteração pequena.

## Escolha o escopo

| Modo | Trabalho |
|---|---|
| PATCH | Corrigir um defeito isolado e verificar o que foi afetado |
| AUDIT | Inspecionar e entregar crítica com evidências |
| REFINE | Melhorar acabamento ou uso preservando um conceito forte |
| REDESIGN | Mudar estrutura ou direção quando a causa exige isso |
| REBUILD | Criar do zero ou reconstruir uma solução com falhas sistêmicas |

Uma landing demonstra valor e ação; um dashboard protege precisão e tarefas; documentação facilita encontrar e entender respostas; uma experiência artística precisa de autoria, comportamento e resolução. Uma página comercial expressiva combina reconhecimento do produto e linguagem própria.

## Exemplos de pedido

- “PATCH: corrija apenas o estado de erro deste formulário e preserve o restante.”
- “AUDIT: analise a página inteira e diferencie observado, inferido e não verificado.”
- “REFINE: preserve a direção aprovada e melhore legibilidade, estados e mobile.”
- “REDESIGN: entenda o produto, compare duas direções específicas, implemente a escolhida e corrija o pior trecho após inspecionar no navegador.”
- “READ: reorganize esta documentação para encontrar respostas, preservando conteúdo, versões e links.”
- “PRODUCT: melhore o dashboard preservando dados, colunas, filtros e fluxos críticos.”

## Ferramentas opcionais

```bash
python skills/studio-grade-web-transformation/brain/route.py contexto.json
python skills/studio-grade-web-transformation/brain/creative_direction_lab.py brief.json
python skills/studio-grade-web-transformation/brain/project_intake.py --project caminho/do/projeto
```

O roteador usa regras e palavras-chave; não é um modelo de compreensão de negócio. O laboratório seleciona estruturas por superfície/evidência declarada; não é um motor de originalidade. Ambos são auxiliares que o agente deve corrigir diante do projeto real.

[Direção baseada no produto](skills/studio-grade-web-transformation/references/product-grounded-direction.md) documenta o briefing do laboratório. O [índice de recursos](skills/studio-grade-web-transformation/references/resource-index.md) reúne referências e ferramentas sem exigir leitura integral. Para fontes especialistas locais, veja [verificação de hashes e limites](docs/VERIFIED_LOCAL_EXPERTS.md); o loader não instala nem executa terceiros.

## Validar o pacote

Python 3.12+; verificações locais de estrutura e lógica:

```bash
python scripts/check_contracts.py
python scripts/check_evals.py
python scripts/check_docs.py
python skills/studio-grade-web-transformation/scripts/validate.py
python scripts/verify_brain_examples.py
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/audit_eval_routing.py
```

Smoke tests de navegador das fixtures sintéticas, com Node e Chromium:

```bash
npm install
npx playwright install chromium
npm run test:browser
```

Teste opcional de um site local autorizado:

```bash
DESIGN_TEST_URL=http://localhost:3000 DESIGN_CTA_SELECTOR='[data-design-critical-cta]' npm run test:browser:target
```

Os testes técnicos verificam fatos e regressões definidos. Não certificam beleza, acessibilidade completa, desempenho, conversão ou prêmios. Uma alteração de texto na skill não significa que um agente seguiu esse texto em produção.

## Evidência e limites

Existem **61 casos de avaliação** definidos e exemplos fictícios comerciais, artísticos e operacionais. O [runbook](docs/EVALUATION_RUNBOOK.md) explica o runner de agentes, captura de artefatos e revisão cega. Os [estudos de aplicação](docs/CASE_STUDIES_V11_1.md) registram limites dos protótipos.

A [matriz de 30 skills](docs/HEAD_TO_HEAD_30_SKILLS.md) descreve confrontos planejados, não vitórias. O [protocolo de projetos reais](docs/REAL_WORLD_BENCHMARK_V11_6.md) exige condições comparáveis, repetições, artefatos funcionando e avaliadores cegos. O baseline sem skill pode vencer; perdas e resultados mistos devem permanecer no relatório.

**Superioridade visual/comercial independente ainda não foi demonstrada.** A v11.7 melhora instruções e comportamento testável, preservando essa distinção. Não publicar métricas, estudos, screenshots, funcionalidade ou depoimentos inventados.

Mais orientação: [início rápido](docs/START_HERE.md), [rubrica humana](docs/QUALITY_RUBRIC.md), [fontes](docs/SOURCE_MATRIX.md). Licença: [MIT](LICENSE).
