# Design OS Prime v11.9.0

Skill aberta de direção de arte, UX/UI, implementação e revisão de sites e produtos digitais. O nome do repositório expressa uma ambição; qualidade precisa aparecer no produto renderizado e em testes reais.

## Instalar

```bash
npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.- --skill studio-grade-web-transformation
```

[Comece pelo SKILL.md](skills/studio-grade-web-transformation/SKILL.md). Para instalação manual, copie a pasta inteira `skills/studio-grade-web-transformation`, preservando referências e ferramentas. O pacote funciona sem executar os scripts opcionais.

## v11.9.0 — crítica independente e evidência real

A nova versão reforça o ciclo de construção → revisão independente → reparo e o protocolo de benchmark com condições comparáveis, execuções repetidas, artefatos renderizados e avaliação cega quando viável. Também diferencia observação de usuário, hipótese, preferência específica de projeto e resultado medido, impedindo que impressões de um modelo virem regra universal.

Guia operacional: [crítica independente, benchmarks e aprendizado](skills/studio-grade-web-transformation/references/independent-critique-and-evidence-learning.md). O método usa os comparadores existentes; não cria uma nota automática de beleza nem promete ganhos antes de medi-los.

**Limites:** existem 77 casos de avaliação definidos, não 77 sites produzidos e avaliados por modelos. Esta versão não reivindica vitória sobre outras skills, aumento de conversão ou superioridade visual independente. A comparação continua dependendo de execuções reais e avaliação documentada. Consulte [o protocolo competitivo](docs/COMPETITIVE_TRIAL_PROTOCOL_V11_4.md) e [o log de reparos](docs/QUALITY_REPAIR_LOG_2026-10-25.md).

## Proatividade e resgate de prompts vagos (v11.7.2)
A skill agora tem um [protocolo de recuperação de briefing](skills/studio-grade-web-transformation/references/prompt-rescue-and-autonomous-direction.md). Para "faz um site foda", "melhore tudo" ou "me surpreenda", o agente deve inspecionar materiais disponíveis, fazer decisões criativas reversíveis, construir cenas reais, verificar mobile e corrigir o elo mais fraco. Não substitui verdade, respeito ao escopo ou autorização para mudanças irreversíveis. O roteamento é hipotético, não uma permissão. Oito testes adversariais sintéticos cobrem arte, landing, dados, documentos, limites de implantação e marcas.

## Landing pages cativantes, sem poluição visual
A skill passou a exigir **hierarquia de atenção, propósito único por seção e revisão por subtração**. A IA não deve empilhar automaticamente cards de benefícios, depoimentos, métricas, animações, FAQs e CTAs. Primeiro vem o produto, a promessa específica, a demonstração autêntica, a marca reconhecível e a decisão honesta. O minimalismo também não pode esconder preço, condições ou informações essenciais.

Três guias novos: [atenção e densidade](skills/studio-grade-web-transformation/references/attention-architecture-and-density.md), [marca cativante](skills/studio-grade-web-transformation/references/brand-affinity-and-desire.md) e [ativação/retorno éticos](skills/studio-grade-web-transformation/references/activation-retention-and-ethical-engagement.md). A continuidade entre marketing, primeira experiência, engajamento e retenção é tratada como jornada real — sem confundir clique com venda nem cadastro com usuário retido.
## Integração da pesquisa aprofundada (25/10/2026)
A pesquisa foi convertida em decisões aplicáveis — **sem adicionar seções e efeitos obrigatórios**. Novo [protocolo evidência → cena](skills/studio-grade-web-transformation/references/evidence-to-scene-protocol.md), [atlas Awwwards × grandes empresas](skills/studio-grade-web-transformation/references/award-business-reference-atlas.md), [criação com IA e UX de IA](skills/studio-grade-web-transformation/references/ai-creative-integrity-and-ux.md) e [qualidade mensurável de lançamento](skills/studio-grade-web-transformation/references/commercial-launch-evidence.md).

Use o exemplo sintético de briefing e o teste opcional de consistência:

```bash
python skills/studio-grade-web-transformation/scripts/landing_truth_gate.py skills/studio-grade-web-transformation/templates/LANDING_EVIDENCE_PACKET.json --json
```

Ele não verifica visual, fontes externas nem conversão. O [mapeamento de adoção](docs/RESEARCH_TO_SKILL_MAPPING_2026-10-25.md) registra o que foi incorporado, adaptado ou rejeitado.

## Reforço visual-first para produtos completos

A revisão de produto agora começa identificando todas as rotas, as tarefas e o proprietário de cada fluxo. Ela exige construir trilhas visuais com estados reais, seletores com prévia, exercícios com interação e componentes reutilizáveis onde apropriado, sem substituir interface por emoji ou paredes de texto. Telas repetidas (por exemplo, dois editores de avatar) precisam ser justificadas ou consolidadas sem perder navegação e dados. Leitura e dados densos continuam tendo a representação adequada ao objetivo.

[Protocolo visual-first](skills/studio-grade-web-transformation/references/visual-first-product-architecture.md). Triagem opcional de inventário declarado:

```bash
python skills/studio-grade-web-transformation/scripts/surface_map_audit.py skills/studio-grade-web-transformation/fixtures/surface-map-anti-example.json
```

O auditor não inspeciona React ou screenshots sozinho, e seus sinais não são uma nota de beleza. É preciso implementar, renderizar e testar o produto real.

## Auditoria de rotas de um projeto real (opcional)

A diferença entre instruções de design e resultado verificado é importante: a skill pode agora extrair **candidatos** a rotas de um projeto local e oferecer uma matriz de inspeção do navegador para caminhos concretos. Isso ajuda a localizar possíveis jornadas duplicadas (como dois editores de avatar), sem afirmar que são o mesmo componente ou que um visual está ruim sem ver pixels.

```bash
python skills/studio-grade-web-transformation/brain/route_inventory.py --project /caminho/projeto --out route-candidates.json
# Revise os caminhos, adicione valores reais para rotas dinâmicas e escolha as telas críticas:
# routes-to-check.json: {"paths":["/","/onboarding/avatar","/profile/avatar"]}
node skills/studio-grade-web-transformation/scripts/route_matrix_audit.mjs --url http://127.0.0.1:3000 --manifest routes-to-check.json --out route-review.json --screenshots route-captures
```

O app deve estar rodando localmente. O inventário cobre convenções de rotas baseadas em arquivos, não modais nem todos os roteadores programáticos; a matriz visita até 12 rotas fornecidas em 320/390/768/1440 px, e marca rotas dinâmicas ou excedentes como não testadas. Capturas e sinais de layout exigem revisão humana; **não** provam usabilidade, marca, conversão, acessibilidade integral nem qualidade artística. O processo continua exigindo clicar fluxos e testar estados reais.

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

Existem **77 casos de avaliação** definidos e exemplos fictícios comerciais, artísticos e operacionais. O [runbook](docs/EVALUATION_RUNBOOK.md) explica o runner de agentes, captura de artefatos e revisão cega. Os [estudos de aplicação](docs/CASE_STUDIES_V11_1.md) registram limites dos protótipos.

A [matriz de 30 skills](docs/HEAD_TO_HEAD_30_SKILLS.md) descreve confrontos planejados, não vitórias. O [protocolo de projetos reais](docs/REAL_WORLD_BENCHMARK_V11_6.md) exige condições comparáveis, repetições, artefatos funcionando e avaliadores cegos. O baseline sem skill pode vencer; perdas e resultados mistos devem permanecer no relatório.

**Superioridade visual/comercial independente ainda não foi demonstrada.** A v11.7 melhora instruções e comportamento testável, preservando essa distinção. Não publicar métricas, estudos, screenshots, funcionalidade ou depoimentos inventados.

Mais orientação: [início rápido](docs/START_HERE.md), [rubrica humana](docs/QUALITY_RUBRIC.md), [fontes](docs/SOURCE_MATRIX.md). Licença: [MIT](LICENSE).
