# Design OS Prime v14.0.0

Skill aberta de direção de arte, UX/UI, implementação e revisão de sites e produtos digitais. O nome do repositório expressa uma ambição; qualidade precisa aparecer no produto renderizado e em testes reais.

## Revenue-Centric Design incorporado integralmente — 11/11/2026

A skill principal agora inclui uma **cópia integral e verificada dos 104 arquivos** do [Revenue-Centric Design](https://github.com/heliocosta-dev/revenue-centric-design), de Hélio Costa, com **134 princípios**, 12 guias temáticos, recursos visuais (inclusive o vídeo original), documentação, histórico, licença e ferramentas opcionais de atualização. Tudo fica em [`skills/studio-grade-web-transformation/vendor/revenue-centric-design/`](skills/studio-grade-web-transformation/vendor/revenue-centric-design/). Você continua instalando **apenas** `studio-grade-web-transformation`; o agente consulta esse conhecimento quando a tarefa envolve aquisição, conversão, onboarding, retenção, preço, posicionamento, experimentos ou UX comercial, sem sacrificar identidade visual nem adicionar funis artificiais. [Proveniência e critérios de uso](docs/REVENUE_CENTRIC_DESIGN_INTEGRATION_2026_11_11.md).

**Atribuição e licença:** princípios de Richard ([@richardrx](https://x.com/richardrx)), curados e disponibilizados por [heliocosta-dev](https://github.com/heliocosta-dev/revenue-centric-design) com permissão. A [licença própria do material](skills/studio-grade-web-transformation/vendor/revenue-centric-design/LICENSE) exige crédito e proíbe **qualquer uso desses materiais para apostas, cassinos, gambling e jogos de azar com dinheiro (inclusive loot boxes)**. Essa parte não é MIT; as condições originais foram preservadas.

## Instalar

```bash
npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.- --skill studio-grade-web-transformation
```

[Comece pelo SKILL.md](skills/studio-grade-web-transformation/SKILL.md). Para instalação manual, copie a pasta inteira `skills/studio-grade-web-transformation`, preservando referências e ferramentas. O pacote funciona sem executar os scripts opcionais.

## Visuais extraordinários precisam de páginas renderizadas — 11/11/2026

A Design OS agora prioriza **construir, renderizar e refinar interfaces reais**, antes de investir em longos planos. Quando a direção artística ainda não foi escolhida, o agente cria **duas ideias visualmente distintas em código**, incluindo abertura, prova no meio, fechamento e composição mobile, e pode compará-las num navegador local. Após escolher a direção mais adequada, finaliza o site completo e repara a parte visualmente mais fraca. Não gera fotos/3D sem recursos ou direitos; seleciona o meio adequado e protege a identidade original.

No repositório, com Playwright instalado e um servidor local da fixture rodando:

```bash
npm run visual:directions
```

O relatório em `test-results/visual-direction/index.html` apresenta evidência real lado a lado, **não notas automáticas de beleza**. A ferramenta é portátil na pasta da skill, mas precisa de páginas já implementadas e runtime Playwright. [Método completo](skills/studio-grade-web-transformation/references/code-first-visual-direction-studio.md) · [Auditoria crítica do foco visual](docs/VISUAL_FIRST_CRITICAL_AUDIT_2026-11-11.md).

## Uma única skill para toda a equipe especializada — 10/11/2026

Você recomenda/ativa apenas `studio-grade-web-transformation`. O agente procura e usa especialistas realmente disponíveis conforme a tarefa: Impeccable (refinamento), Anthropic e Taste (arte), UI/UX Pro Max (padrões), Vercel (UX/React), GSAP (motion), Figma (design), e especialistas de CEO/CMO/COO, vendas, growth, funil, marketing, copy, SEO/GEO, analytics e psicologia ética do usuário. Design OS coordena, implementa, inspeciona e entrega um resultado único, sem obedecer a opiniões externas que contradigam o produto.

Catálogo: **46 entrypoints públicos identificados** com vantagens de nicho, gatilhos e pré-requisitos; isso **não** comprova superioridade, instalação, compatibilidade ou execução. A skill não instala dependências automaticamente. O roteiro abaixo lista candidatos e detecta algumas skills locais, não inicia outros agentes:

```bash
python skills/studio-grade-web-transformation/scripts/specialist_router.py --surface marketing --operation build --task "landing de vendas, copy, SEO e GEO" --json
```

[Orquestração de especialistas](skills/studio-grade-web-transformation/references/automatic-specialist-orchestration.md) · [CEO/CMO/COO, vendas e growth](skills/studio-grade-web-transformation/references/full-funnel-commercial-orchestration.md) · [Great Leads aplicado](skills/studio-grade-web-transformation/references/great-leads-ethical-copy-framework.md) · [Psicologia ética do usuário](skills/studio-grade-web-transformation/references/ethical-user-psychology.md) · [Catálogo verificável](skills/studio-grade-web-transformation/research/specialist_registry.json).

## Auditoria crítica de sistemas e orquestração — 11/11/2026

A principal correção foi eliminar a duplicação funcional do roteamento: o fluxo antigo agora consulta o roteador canônico, e a indicação de especialistas respeita restrições explícitas, autoridade sobre o projeto e especialização por tarefa. Foram recuperadas seis áreas técnicas que se perderam no catálogo novo: Three.js, React Three Fiber, performance web, DTCG/design tokens, Playwright e UI Craft.

Novas rotas condicionais cobrem UX de login/autorização/checkout, privacidade/consentimento, localização/CMS e observabilidade/recovery. Use somente para tarefas que envolvam esses riscos; os roteadores não executam especialistas nem certificam segurança ou beleza. [Relatório de auditoria](docs/CRITICAL_AUDIT_2026-11-11.md).

## Novos fluxos operacionais — integração competitiva (10/11/2026)

Adicionados **22 operadores direcionados** (criar, criticar, auditar, polir, simplificar, destacar, acalmar, copy, tipografia, layout, animação, onboarding, hardening, otimização, variantes etc.), orientação para **mobile nativo** e um **scanner original, local e consultivo** para CSS/JSX/HTML. Esses recursos complementam o `craft_audit.py` e a inspeção Playwright existentes sem fingir ser o aplicativo Impeccable, sua extensão ou seu modo de edição ao vivo.

```bash
python skills/studio-grade-web-transformation/scripts/design_workflow.py --list
python skills/studio-grade-web-transformation/scripts/design_workflow.py --action distill --surface marketing --json
python skills/studio-grade-web-transformation/scripts/source_triage.py caminho/para/src --json
python skills/studio-grade-web-transformation/scripts/design_context.py --project caminho/para/projeto --init
```

[Contexto do produto e identidade](skills/studio-grade-web-transformation/references/product-and-design-context.md) · [Operações e limites](skills/studio-grade-web-transformation/references/precision-design-operations.md) · [Source triage → navegador](skills/studio-grade-web-transformation/references/source-triage-and-browser-review.md) · [Mobile nativo](skills/studio-grade-web-transformation/references/native-interface-discipline.md). Códigos de terceiros **não** foram copiados. Os testes incluídos validam lógica e integração, não desempenho estético nem uma vitória sobre concorrentes.

## Integração da pesquisa de landing pages — 06/11/2026

Quatro módulos operacionais transformam pesquisa em decisões de projeto: **intenção do visitante e arquitetura da oferta**, **copywriting e persuasão ética**, **direção de arte original e anti-AI-slop**, **funil, experimentação, acessibilidade e QA real**. Não adicionam templates obrigatórios, número fixo de agentes ou promessas de conversão; carregue os guias conforme o trabalho.

[Mapa de fontes → decisões](docs/RESEARCH_LANDING_PAGE_SYSTEM_2026-11-06.md) · [Fluxo para landings](skills/studio-grade-web-transformation/references/landing-strategy-and-decision-architecture.md) · [Copy + psicologia](skills/studio-grade-web-transformation/references/copy-lab-and-ethical-psychology.md) · [Ateliê anti-slop](skills/studio-grade-web-transformation/references/visual-direction-and-anti-slop-atelier.md) · [Mensuração + release](skills/studio-grade-web-transformation/references/funnel-measurement-experiments-and-release.md)

Os [6 cenários adicionais](skills/studio-grade-web-transformation/evals/landing_research_scenarios.json) estão marcados `NOT_RUN`: são testes propostos, **não** resultados ou vitórias da skill.

## Descoberta orgânica competitiva — SEO, GEO, AEO, AI Search e mais (06/11/2026)

A skill agora trata **visibilidade orgânica como parte da estratégia e do produto**, não como tarefa final de metadados. Pesquisa intenção, SERP e concorrentes reais (quando há ferramentas), identifica provas e conteúdos que merecem ser encontrados, decide canais adequados ao nicho, trabalha SEO técnico/semântico, AI Search, conteúdo original, autoridade, local/internacional/mídia e acompanha desempenho em Google Search Console, Bing/AI e conversão qualificada. Sem prometer 1º lugar, manipular crawlers, gerar spam de IA ou sacrificar direção de arte.

[Fluxo principal](skills/studio-grade-web-transformation/references/organic-discovery-operating-system.md) · [GEO/AEO e IA](skills/studio-grade-web-transformation/references/ai-answer-and-entity-visibility.md) · [Conteúdo e autoridade](skills/studio-grade-web-transformation/references/search-content-and-authority-engine.md) · [Medição e concorrentes](skills/studio-grade-web-transformation/references/search-intelligence-measurement-loop.md) · [Pesquisa e fontes](docs/ORGANIC_DISCOVERY_RESEARCH_2026-11-06.md).

Há um validador **opcional e offline** de evidências declaradas e oito novos cenários de regressão **NOT_RUN** (não são resultados ou vitórias medidos). A versão continua v14 e as avaliações anteriores permanecem intactas.

## v14.0.0 — auditoria crítica e validação mais confiável

A v14 prioriza corrigir erros reais em vez de acumular guias: críticas vazias deixam de ser aprovadas, verificações reconhecem correções efetivas entre o primeiro render e a entrega, PNGs são validados estruturalmente, tipos JSON inválidos não derrubam os validadores, e a qualidade de layouts existentes pode ser preservada quando não há motivo real para refazer.

Novo controlador `scripts/quality_controller.py` integra as evidências disponíveis de briefing, renderização, revisores, assets, posicionamento e SEO conforme o escopo. Ele **não** gera sites, chama subagentes ou atribui nota automática de beleza. [Relatório de auditoria e exemplo de uso](docs/CRITICAL_AUDIT_V14.md). Os **82 cenários declarados** permanecem planos de avaliação, não vitórias verificadas.

## v13.0.0 — posicionamento, copy, SEO e fidelidade ao pedido

A versão 13 adiciona ao núcleo: fidelidade literal às exigências do briefing (inclusive referências nomeadas), checkpoint de direção/primeiro render/entrega, copywriting amarrado a posicionamento e prova real, SEO público contextualmente correto, revisão por perspectivas com subagentes **somente quando realmente disponíveis** e trabalho proativo para cobrir detalhes importantes que um usuário leigo pode não citar.

Quatro utilitários portáteis verificam contratos declarados: `brief_alignment.py`, `positioning_copy_contract.py`, `search_presence_audit.py` e `review_council.py`. Nenhum deles cria subagentes, reconhece visualmente personagens, consulta Google Search Console, determina beleza ou comprova conversão.

Pesquisa com fontes primárias: [estudo e decisões](docs/RESEARCH_DESIGN_GROWTH_2026-11-05.md). [Exemplos executáveis dos quatro validadores](docs/WORKFLOW_CONTRACTS_V13.md). Orientação operacional nas novas referências listadas em [SKILL.md](skills/studio-grade-web-transformation/SKILL.md). Avaliação sintética da skill agora contém **82 casos de avaliação declarados**; não são 82 sites executados ou vencedores.

## v12.0.0 — production evidence, creative differentiation and safer learning

A v12 adds **optional executable contracts**, not an automatic designer: structural concept-diversity checks, verified local asset/canon inventory, cinematic timeline/accessibility plan, real screenshot/build/interaction evidence packets, and learning-rule review that retains baseline wins. Every tool is transparent about what it cannot judge. The next step is to **run** real paired agent builds and independent blind reviews; no public creative superiority has been established.

See [the V12 production manual](docs/PRODUCTION_SYSTEM_V12.md). The full guide is invoked only for substantial projects; small fixes remain small.

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
