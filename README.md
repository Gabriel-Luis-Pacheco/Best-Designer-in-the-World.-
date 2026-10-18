# Design OS Prime v11.5 — Best Designer in the World

Skill aberta para agentes de IA trabalharem com direção de arte, UX, UI, brand fidelity, implementação e crítica baseada em evidência. O nome é uma ambição criativa, **não** promessa de prêmio, aumento de conversão ou melhor resultado do mundo.

## Versão ativa — 11.5.0

A skill faz direção de arte, UX/UI e implementação com rotas proporcionais: PATCH, AUDIT, REFINE, REDESIGN e REBUILD. Para projetos visuais, constrói, inspeciona o navegador, corrige a pior cena e documenta o que ficou **não verificado**. Para sistemas operacionais, clareza, precisão e fluxos importam mais que espetáculo.

**Instalação:**
```bash
npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.- --skill studio-grade-web-transformation
```

**Arquivo ativo:** [SKILL.md](skills/studio-grade-web-transformation/SKILL.md).
**Estudos práticos:** [Cenários comerciais, artísticos e operacionais](docs/CASE_STUDIES_V11_1.md).
**Metodologia de avaliação:** [Runbook](docs/EVALUATION_RUNBOOK.md), [protocolo externo](docs/EXTERNAL_EVALUATION_PROTOCOL.md).
**Estado científico:** 61 cenários de avaliação definidos; **não** existe benchmark independente comprovando vitória estética ou conversão. GitHub Actions valida estrutura e comportamento de protótipos.

### V11.5 — menos falso positivo, mais prova de execução
- Roteador de tecnologias distingue pedidos positivos de recusas explícitas (sem WebGL/GSAP), preservando a interpretação do português.
- Avaliador deixa de inventar 3D porque o produto é uma caixa de som: tecnologia deve ser explicitamente solicitada ou escolhida com justificativa real.
- Auditor de navegador agora inclui 320/390/768/1440px e candidatos a imagem quebrada, além de overflow e botões pequenos.
- Novo auditor executável testa se as referências realmente são injetadas para todos os 61 cenários sintéticos, sem transformar esses testes em "nota de beleza".
- Testes negativos para recusa de tecnologia, casos multilíngues e imagem visivelmente quebrada, mantendo fluxos legados.

### V11.4 — evidence-driven superiority, not more instructions
- Fix in evaluation reference injection: specialty modules for CRO, studio Awwwards, and motion/3D are not silently displaced by old generic guides.
- Real Chromium layout inspector (390px/1440px, review-only for overflow/tap targets, localhost-only).
- Multi-skill blind evaluation comparator (Pareto wins/losses, tradeoffs, blocker priority; no fabricated automatic aesthetic grades).
- Regression tests for new route loading, rival-review fairness and browser geometry.
- Relative priority of *actual rendered creativity and usefulness* over compliance paperwork. See docs/COMPETITIVE_TRIAL_PROTOCOL_V11_4.md for honest win requirements.

### V11.3 — competências especializadas e ferramentas executáveis
- Auditor HTML de craft/anti-slop com achados como hipóteses, nunca nota estética.
- Validador estrutural de uma parte da especificação DTCG (aliases/ciclos), com limites explícitos.
- Roteador auxiliar de especialistas externos (15 fontes), limitado a 0–3 sugestões e sem instalação automática.
- Cinco playbooks novos: memória visual/tokens/fontes, QA visual, marketing e funil, engenharia de motion/3D, entrega de sites multipágina.
- Três templates opcionais para canon, conversão e handoff.
- Testes negativos específicos dos novos scripts e do roteador; cobertura estrutural não prova beleza, conversão ou desempenho.
- Relatório de frentes e atribuições em docs/WORKSTREAM_IMPLEMENTATION_V11_3.md.

### Novidades V11.2 — pesquisa Awwwards integrada sem inflar a execução
- Cinco módulos opt-in para pipeline de estúdios criativos, landing/CRO, decisões de tecnologia GSAP/3D, seleção de skills externas e evidência de qualidade.
- Roteamento concreto: EXPERIENCE recebe processo de estúdio; LANDING recebe conversão; 3D/motion só quando solicitado; backoffice não é obrigado a usar espetáculo.
- Dois templates de prova, documentação do inventário tema a tema deste chat e testes de roteamento negativos para evitar regressões.
- Links de fontes e repositórios são candidatos à verificação, não skills instaladas, benchmark, certificação ou promessa de prêmio.
- O contexto principal continua pequeno: referências carregadas seletivamente, com o mesmo processo de autópsia → conceito → implementação → inspeção → correção.

### Correções V11.1
- O runner registra `task_input_sha256` do mesmo briefing/fixtures e `assembled_prompt_sha256` de cada condição; **não** exige prompts montados idênticos.
- Carrega efetivamente as referências novas de assinatura visual e interação em testes criativos; não as injeta em dashboards internos.
- Captura projetos opt-in com configs e assets além do código, hash por arquivo e limites para controle de segredos.
- A captura de cenas falha se encontrar erros JavaScript ou dependências externas bloqueadas e exige intenção semântica/estado para ações; o comparador verifica equivalência.
- Acrescenta Ledger, dashboard operacional com dados fictícios, busca, filtros e exportação, com testes desktop/mobile.

## Histórico — V9.8 Creative Commerce sem perder a V9.7
Este é um registro histórico da V9.8. A comparação posterior de artefatos RESONANCE da **V6.1** indicou vantagem visual da condição sem skill, mas não estabeleceu efeito causal controlado; consulte `docs/RESONANCE_LESSONS_V11.md`. Esta atualização é deliberadamente focada em proteção contra regressões: diferencia experiência artística pura, landing comercial imersiva e sistemas/checkout; classifica criação nova como construção em vez de refinamento; prioriza referências realmente úteis; sincroniza versões e fortalece testes. Consulte `references/experiential-commerce.md` dentro da skill.

**61 casos de avaliação**, sem benchmark cego independente publicado.

## Histórico — Versão 9.7 — Art Director First + A/B integrity
O MIRAGE evidenciou uma comparação inválida: o agente rotulado "com skill" declarou que **não tinha a Design OS instalada** e usou outra skill. A v9.7 não alega superar o baseline; adiciona preflight de leitura, bloqueio de substituições silenciosas, rota `experience` para projetos Awwwards e direção criativa de ponta a ponta. Ver `docs/MIRAGE_AB_LESSONS.md`.

A 9.7 introduziu 44 casos e correções do roteador, sem benchmark cego independente realizado.

## Histórico — Versão 9.6 — Project Intake + Product Intelligence Brain
Agora a skill inclui um planejador integrado `brain/pipeline.py`, que combina roteamento, avaliação de escopo e inventário opcional, sem executar mudanças. A skill inclui inventário local **somente leitura** em `brain/project_intake.py`, melhorias de interpretação de intenção, objetivos globais preservados nas múltiplas superfícies, referências visuais alcançáveis e proteção de contratos hierárquicos. A inspeção de caminhos não equivale a compreensão do negócio, testes de UX ou evidência visual. Ver `docs/V96_ARCHITECTURE.md`.

Versão 9.6 introduziu inventário local e planejamento integrado; ainda sem benchmark visual independente publicado.

## Histórico — Versão 9.5 — Toolbelt + Product Intelligence Brain
A skill investiga produto, contexto, objetivo primário, guardrails e diferenças entre superfícies antes de escolher conhecimentos. Um roteiro determinístico portátil `brain/route.py` gera hipóteses e URLs candidatas, nunca navegação presumida. O adaptador A/B agora inclui o plano contextual no prompt com skill. Execução de agent, pesquisa, testes em projetos reais e revisão humana exigem ferramentas e evidência externas.

```bash
python scripts/verify_brain_examples.py
python skills/studio-grade-web-transformation/brain/route.py skills/studio-grade-web-transformation/brain/examples/fintech-landing.json
```
Consultar `docs/V95_ARCHITECTURE.md` e `skills/studio-grade-web-transformation/brain/README.md`.

## Melhorias da versão 8.1
- Runner de avaliação com execução por diretório limpo e hashes das fixtures.
- Comparação pareada e estrita: não mistura avaliadores nem dimensões diferentes.
- Contratos comerciais de protótipo sintético testados em CI.
- Novos guias práticos de composição editorial, motion, UX de produto e evidências.

## Cérebro estratégico (v9.0)
O roteador portátil `brain/route.py` gera um **brief estratégico proposto** de produto, público, superfície, objetivo e guardrails; escolhe packs da skill e fontes para pesquisa de acordo com o contexto. Não navega, não executa alterações nem inventa métricas. A IA que usar a skill tem que confrontar hipóteses com o projeto real e corrigir erros de classificação. Exemplos: `python skills/studio-grade-web-transformation/brain/route.py skills/studio-grade-web-transformation/brain/examples/fintech-landing.json`. Uma landing de fintech e um backoffice financeiro recebem estratégias distintas.

## O que mudou
- Modos proporcionais: PATCH, AUDIT, REFINE, REDESIGN e REBUILD. Uma correção local não dispara reconstrução.
- Anti-slop construtivo: composição, tipografia, ritmo, provas e decisões criativas; não apenas estilos proibidos.
- Comparação de duas ou mais direções realmente distintas em mudanças estruturais, com critérios e trade-offs.
- Pacote instalável com 61 casos, fixtures sintéticas HTML/SVG/brief, rubrica, referências e templates.
- CI estrutural, testes negativos Python, browser smoke em Chromium, scripts de revisão humana e runner CLI opcional.
- Nenhuma afirmação estética automática ou evidência falsa.

## Instalação
```bash
npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.- --skill studio-grade-web-transformation
```
O ponto de entrada é `skills/studio-grade-web-transformation/SKILL.md`. É possível copiar somente essa pasta; referências, fixtures e validação portátil a acompanham.

## Testar instalação e comparações A/B
Ao pedir explicitamente esta skill no OpenCode, confirme a leitura real de `skills/studio-grade-web-transformation/SKILL.md`. Se ela não existir na sessão, a execução é **INVALID_COMPARISON**; outra skill não pode substituí-la.
```bash
python scripts/validate_experiment.py --pair caminho/pair.json --skill skills/studio-grade-web-transformation/SKILL.md
```
O validador rejeita ausência de skill, fallback `frontend-design`, ferramentas/modelos/orçamentos desiguais e falta de rastro de leitura. Uma passagem significa somente `READY_FOR_BLIND_REVIEW_NOT_PROVEN` e **não comprova superioridade**. Detalhes e esquema: `docs/MIRAGE_AB_LESSONS.md`.

## Como usar
- "PATCH: corrija apenas o estado de erro deste formulário e preserve o restante."
- "AUDIT: analise a landing e diferencie o que foi observado do que não foi verificado."
- "REDESIGN: compare duas direções criativas, escolha pelos critérios do público e da marca, implemente e valide a página inteira no navegador."
- "PRODUCT: melhore este dashboard preservando dados, colunas, filtros e fluxos críticos."

## Validação estrutural (Python 3.12+)
```bash
python scripts/check_contracts.py
python scripts/check_evals.py
python skills/studio-grade-web-transformation/scripts/validate.py
python -m unittest discover -s scripts -p "test_*.py" -v
```
Isso **não** valida a beleza nem executa um modelo de IA.

## Smoke tests das fixtures (Node + Chromium)
```bash
npm install
npx playwright install chromium
npm run test:browser
```
As fixtures são **sintéticas** e incluem deficiências intencionais. Testes de navegador verificam carga e fatos invariantes, não qualidade artística.

## Teste opcional de site real (ambiente autorizado)
```bash
DESIGN_TEST_URL=http://localhost:3000 DESIGN_CTA_SELECTOR='[data-design-critical-cta]' npm run test:browser:target
```
Captura screenshots em 320/390/768/1440 px e verifica renderização, overflow, IDs duplicados, nome acessível e destino de CTA (contrato opcional `DESIGN_EXPECTED_CTA_URL`); não compra nem envia formulários. Fluxos específicos exigem seus próprios testes.

## Avaliação A/B
Os 61 casos estão em `evals/evals.json`, com entradas sob `skills/studio-grade-web-transformation/fixtures/`. `scripts/run_evals.py` aceita um CLI de agente que leia stdin; não fornece modelo, revisão independente ou julgamento visual. Na condição `with_skill`, o adaptador injeta SKILL.md e até quatro referências contextualizadas por caso, inclusive em CLIs sem acesso a arquivos. Essa seleção é fixa e documentada; não equivale à navegação dinâmica por todas as referências. Veja `docs/EVALUATION_RUNBOOK.md` e `docs/QUALITY_RUBRIC.md`.

## Princípios
Nenhum depoimento, métrica ou funcionalidade inventada. Assets externos e scripts remotos só com licença/segurança verificada. Nunca publicar dados internos ou segredos. Não declarar que testes não executados passaram.

**Status:** v11.0 possui CI de estrutura/fixtures e melhorias no roteador. Superioridade visual, comercial e em UX diante de um agente sem skill permanece NÃO COMPROVADA por A/B real.

Histórico: `CHANGELOG.md`. Licença: `LICENSE`.

## V11.0 — ciclo prático e ferramentas de revisão
O auditor opcional de ritmo HTML `scripts/section_rhythm.py` identifica padrões para revisão sem atribuir pontuação estética. A skill principal é mais enxuta e prioriza construir abertura/miolo/fechamento, inspecionar pixels, refazer o elo fraco e registrar evidência — inclusive em mobile. Nova comparação canônica de assets em `scripts/asset_board.py` e antes/depois real em `scripts/visual_review_packet.py` (ambos dentro da skill instalada). Um segundo conceito experimental, `examples/conversaboa-editorial-alternative.html`, serve para comparar direções realmente distintas, não como certificado de beleza. Veja `docs/V10_CREATIVE_VALIDATION.md`.

## V11.0 — o que o teste RESONANCE ensinou
Nesta revisão, acrescentamos assinatura FORMAL/MATERIAL/COMPORTAMENTAL, transformação entre cenas, dramaturgia do gesto, clímax contextual e revisão em cinco frames. A comparação original avaliou um pacote V6.1, **não V10/V11**, e não foi um experimento causal controlado. Evitamos impor o anel, a cor verde ou o SVG final do projeto vencedor. Consulte [lições do RESONANCE](docs/RESONANCE_LESSONS_V11.md), [assinatura criativa](skills/studio-grade-web-transformation/references/creative-signature-and-form.md) e [jornada visual](skills/studio-grade-web-transformation/references/creative-evidence-journey.md).

O capturador local de cenas é opcional e não executa acesso à internet nem análise estética: `npm run capture:journey` (com servidor fixture rodando). **61 casos de avaliação** existem como cenários; não equivalem a 57 testes criativos vencidos.

### V11 — comparativo cego de cenas
Após capturar dois sites com o mesmo storyboard, o comando `python scripts/compare_creative_journeys.py --a output/A/manifest.json --b output/B/manifest.json --out output/pair-review` confere frames, viewport, motion e SHA256, depois produz `blind-review.html` com variantes A/B, sem nota. As imagens podem conter dados privados: manter evidências no ambiente autorizado. Não publicar artefatos do usuário nem afirmar que há experimento causal sem log real de modelo/skill/ferramentas.

## Preservação da evolução paralela V10.1
Além das novidades V11, esta integração mantém [Creative Advantage Loop](skills/studio-grade-web-transformation/references/creative-advantage-loop.md), [Immersive 3D Product Direction](skills/studio-grade-web-transformation/references/immersive-3d-product-direction.md), o [Scene Challenger](skills/studio-grade-web-transformation/templates/SCENE_CHALLENGE.md), `journey_board.py`, melhorias no runner A/B e os quatro cenários V10.1 (IDs 58–61). Histórico: [V10.1 Creative Advantage](docs/V101_CREATIVE_ADVANTAGE.md). São **61 casos de avaliação**, não 61 resultados positivos.
