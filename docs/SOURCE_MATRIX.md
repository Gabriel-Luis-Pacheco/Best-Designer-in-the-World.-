# Matriz de fontes e skills — Design OS Prime v8.1

Curadoria em 16/10/2026. Adaptações escritas especificamente para este projeto. Referências são **links de estudo**, não conteúdo redistribuído; verifique atualizações, licenças e disponibilidade. Não interpretar ranking/popularidade como evidência de resultado para seu produto.

## Skills e harnesses para agentes

| Fonte | URL | Mecanismo observado | O que adotamos | Risco / decisão |
|---|---|---|---|---|
| Anthropic frontend-design | https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md | Conceito intencional, decisões ousadas contextualizadas | Direção antes do JSX, anti-template | Não copiar skill integral; licença própria |
| Anthropic skill-creator | https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md | Iteração e evals sobre casos reais | A/B com e sem skill, variância e avaliação cega | Não declarar benchmark sem executar |
| Anthropic skill schemas | https://github.com/anthropics/skills/blob/main/skills/skill-creator/references/schemas.md | Estrutura de evals.json | Casos com output esperado e checks explícitos | Esquema como inspiração, sem copiar implementação |
| Agent Skills evaluation | https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/evaluating-skills.mdx | Testes estruturados de qualidade | Evals de prompt reais, rastreio de resultados | Resultado subjetivo exige revisor |
| Agent Skills specification | https://agentskills.io/specification | SKILL.md, frontmatter, referências opcionais | Uma skill normativa + carregamento progressivo | Não forçar todas as referências no contexto |
| Vercel web-design-guidelines | https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines | Auditoria de interface e a11y | Revisar UI e estado real | Conteúdo remoto pode mudar; revisar a origem |
| Vercel React Best Practices | https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices | Performance priorizada por impacto | Optimizações de bundle e waterfalls quando React | Não forçar React nem copiar regras |
| Vercel Composition Patterns | https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns | Componentes reutilizáveis e compostos | APIs explícitas para peças complexas | Só quando stack compatível |
| Google Stitch Skills | https://github.com/google-labs-code/stitch-skills | Agent Skills para design/build | Ideia de extrair design system de telas reais | Requer Stitch/tooling se usando a skill |
| Google design-md | https://github.com/google-labs-code/stitch-skills/blob/main/plugins/stitch-utilities/skills/design-md/README.md | Analisar telas e sintetizar DESIGN.md | Contrato canônico para tokens e arte | Sem afirmar que integrou Stitch sem acesso |
| Microsoft Playwright | https://playwright.dev/docs/test-snapshots | Comparar screenshot estável | Baseline e regressão visual | Diff de pixels ≠ design bonito |
| Storybook tests | https://storybook.js.org/docs/writing-tests | Casos de componentes, estados e captura visual | Matriz por estado/componentes | Uso opcional; evitar dependência desnecessária |
| Storybook a11y | https://storybook.js.org/docs/writing-tests/accessibility-testing | Heurísticas de a11y automatizadas | Evidência técnica de problemas comuns | Complementar com testes manuais |
| Deque axe-core | https://www.deque.com/axe/axe-core/ | Regras de acessibilidade automatizadas | Scan como parte da revisão | Nunca chamar de conformidade integral |

## Práticas de estúdios e design systems

| Fonte | URL | Descoberta valiosa | Aplicação |
|---|---|---|---|
| Apple Design Principles | https://developer.apple.com/design/human-interface-guidelines/design-principles | Propósito, agência e inclusão | Justificar escolhas por impacto |
| Apple Layout | https://developer.apple.com/design/human-interface-guidelines/layout | Contexto adaptável, agrupamento e hierarquia | Mobile de verdade + localização/zoom |
| Apple Writing | https://developer.apple.com/design/human-interface-guidelines/writing | Linguagem como parte do produto | Copy explícita e escaneável |
| Apple Motion | https://developer.apple.com/design/human-interface-guidelines/motion | Movimento conciso e com propósito | Motion sem carga cognitiva excessiva |
| Duolingo Characters | https://design.duolingo.com/illustration/characters | Silhueta, linguagem de formas e expressões | Canon de mascotes, sem copiar personagens |
| Atlassian Spacing | https://atlassian.design/foundations/spacing | Tokens e ajuste óptico | Espaçamento sem rigidez cega |
| IBM Carbon Content | https://www.carbondesignsystem.com/building-blocks/foundations/content | Microcopy de sistema e consistência | Labels claros e estados úteis |
| IBM Carbon Accessibility | https://www.carbondesignsystem.com/building-blocks/foundations/accessibility/developers | Semântica e ordenação de foco | Auditoria a11y operacional |
| Shopify Polaris Content | https://polaris-react.shopify.com/content/fundamentals | Palavras como custo de atenção | Remover copy redundante |
| GOV.UK Design System | https://design-system.service.gov.uk/patterns/ | Padrões por tarefa e pesquisa | Escolher padrão pelo objetivo |
| Material Motion | https://m1.material.io/motion/material-motion.html | Continuidade e foco | Coreografia de transição clara |
| NN/g Ten Heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ | Heurísticas universais de UX | Revisor independente |
| NN/g Visual Hierarchy | https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ | Contraste, escala e agrupamento | Teste de squint e foco |
| NN/g How People Read | https://www.nngroup.com/articles/how-people-read-online/ | Leitura por varredura | Sequência visual e escrita enxuta |
| Baymard Mobile Examples | https://baymard.com/mcommerce-usability/benchmark/mobile-page-types/product-page | Pesquisa e screenshots com anotações | Padrões de mobile observados, sem generalizar SaaS |

## Bibliotecas de inspiração (não equivalentes a evidência de conversão)

| Fonte | URL | Usar para |
|---|---|---|
| Awwwards | https://www.awwwards.com/ | Qualidade de direção visual, motion e detalhe |
| SiteInspire | https://www.siteinspire.com/ | Composição editorial e identidade |
| Godly | https://godly.website/ | Ideias visuais e experiências não convencionais |
| Land-book | https://land-book.com/ | Landing pages por contexto e estilo |
| Landingfolio | https://www.landingfolio.com/ | Estruturas e variações de hero |
| Mobbin | https://mobbin.com/ | Telas reais de produto, estados e padrões |
| Page Flows | https://pageflows.com/ | Fluxos e jornadas em produtos reais |
| SaaSFrame | https://www.saasframe.io/ | Referências comerciais de SaaS |

## Como selecionar (em vez de seguir tudo)
1. **Necessidade específica** da tarefa → fonte com mecanismo correspondente.
2. **Evidência confiável** (pesquisa ou uso real) preferível para padrões de UX.
3. **Referência estética** válida para art direction, não para alegação de conversão.
4. **Licença** avaliada antes de copiar qualquer código, snippet, imagem ou arquivo.
5. **Custo/contexto** da ferramenta; não inserir Playwright, Storybook, Stitch ou frameworks à força.
6. **Decisão** documentada como ADOTAR, ADAPTAR, CONSULTAR ou REJEITAR.

Nenhuma dessas fontes, isolada ou combinada, garante Awwwards. A qualidade final precisa ser inspecionada no projeto real e validada com usuários.
