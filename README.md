# Design OS Prime v9.8 — Best Designer in the World

Skill aberta para agentes de IA trabalharem com direção de arte, UX, UI, brand fidelity, implementação e crítica baseada em evidência. O nome é uma ambição criativa, **não** promessa de prêmio, aumento de conversão ou melhor resultado do mundo.

## Versão 9.8 — Creative Commerce sem perder a 9.7
O teste RESONANCE foi relatado pelo usuário como uma vitória expressiva da skill, mas os artefatos e logs da nova execução ainda não foram enviados, portanto **não se alega validação independente**. Esta atualização é deliberadamente focada em proteção contra regressões: diferencia experiência artística pura, landing comercial imersiva e sistemas/checkout; classifica criação nova como construção em vez de refinamento; prioriza referências realmente úteis; sincroniza versões e fortalece testes. Consulte `references/experiential-commerce.md` dentro da skill.

**47 casos de avaliação**, sem benchmark cego independente publicado.

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
- Pacote instalável com 47 casos, fixtures sintéticas HTML/SVG/brief, rubrica, referências e templates.
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
Os 47 casos estão em `evals/evals.json`, com entradas sob `skills/studio-grade-web-transformation/fixtures/`. `scripts/run_evals.py` aceita um CLI de agente que leia stdin; não fornece modelo, revisão independente ou julgamento visual. Na condição `with_skill`, o adaptador injeta SKILL.md e até quatro referências contextualizadas por caso, inclusive em CLIs sem acesso a arquivos. Essa seleção é fixa e documentada; não equivale à navegação dinâmica por todas as referências. Veja `docs/EVALUATION_RUNBOOK.md` e `docs/QUALITY_RUBRIC.md`.

## Princípios
Nenhum depoimento, métrica ou funcionalidade inventada. Assets externos e scripts remotos só com licença/segurança verificada. Nunca publicar dados internos ou segredos. Não declarar que testes não executados passaram.

**Status:** v9.8 possui CI de estrutura/fixtures e melhorias no roteador. Superioridade visual, comercial e em UX diante de um agente sem skill permanece NÃO COMPROVADA por A/B real.

Histórico: `CHANGELOG.md`. Licença: `LICENSE`.
