# Design OS Prime v14.0.0 — Start here

A skill serve para criar, implementar ou revisar design sem perder realidade de produto.

## Selecione o menor escopo adequado
PATCH corrige uma falha local; AUDIT analisa sem criar implementação fictícia; REFINE melhora tela boa; REDESIGN altera arquitetura ou direção; REBUILD reconstrói quando problemas sistêmicos justificam. Distinga MARKETING (clareza, prova, conversão) de PRODUCT (precisão, tarefas, densidade e estados).

## Menos poluição, mais produto e marca

Para landing, priorize: intenção da pessoa → promessa verificável → demonstração concreta → ação honesta. Planeje abertura, miolo e fecho, fundindo ou cortando cenas repetitivas antes do polimento. Ative os guias `references/attention-architecture-and-density.md`, `references/brand-affinity-and-desire.md` e, para jornadas de produto, `references/activation-retention-and-ethical-engagement.md`. O critério não é ter poucas palavras: é cada elemento merecer a atenção que recebe.

## Operações de design precisas (10/11/2026)

Antes de carregar todo o sistema, escolha uma tarefa concreta: `polish`, `distill`, `bolder`, `quieter`, `critique`, `audit`, `animate`, `adapt`, `harden`, `onboard`, `variants` etc. Consulte `references/precision-design-operations.md` e execute opcionalmente `scripts/design_workflow.py --action polish --surface marketing --json`. Isto é um seletor de guias; a execução ainda cabe ao agente sobre o projeto real.

Para pistas locais em folhas de estilo ou JSX: `python scripts/source_triage.py caminho/para/src --json`. Confirme flags contra o DOM/viewport, estado de teclado e comportamento real; ausência de flags não é selo de qualidade. Em iOS/Android use `references/native-interface-discipline.md` e testes de plataforma, não apenas Chrome mobile.

## V14: QA que não aprova sem provas

- Em projetos completos, confronte briefing, capturas reais, críticos, provas, assets e SEO no controlador opcional `scripts/quality_controller.py`. Ele não executa os testes por você; detecta lacunas e falhas no pacote apresentado.
- Críticas vazias exigem observação e evidência; falhas P0/P1 devem ser corrigidas e recapturadas antes da conclusão.
- Uma primeira versão ruim pode ser corrigida e aprovada na entrega sem apagar o histórico. Uma parte já excelente não exige uma mudança artificial.
- Um relatório `EVIDENCE_PACKET_FOR_HUMAN_REVIEW` **não** certifica qualidade estética, acessibilidade nem conversão.

Exemplo e auditoria: [CRITICAL_AUDIT_V14.md](CRITICAL_AUDIT_V14.md).

## V13: fidelidade ao pedido e qualidade comercial proativa

1. Guarde o pedido original e preserve personagens, nomes, marcas, cenas e ações específicos. Pesquise referências com fontes confiáveis e verifique a identidade real em vez de substituir por algo genérico.
2. Para sites públicos: confira posicionamento, proposta de valor, copy, provas concretas, CTAs, SEO e distribuição. Não é um funil obrigatório para arte e sistemas internos.
3. Revise abertura, meio, final e mobile contra o briefing original; se a direção não corresponde, volte ao conceito em vez de maquiar a tela.
4. Use agentes revisores independentes quando o ambiente permitir; do contrário, separe papéis e assuma que é autocrítica. Nunca invente usuários.
5. Consulte o [estudo de 2026-11-05](RESEARCH_DESIGN_GROWTH_2026-11-05.md) e os módulos específicos da SKILL.md, sem carregar toda a biblioteca.

Exemplos JSON/CLI: [WORKFLOW_CONTRACTS_V13.md](WORKFLOW_CONTRACTS_V13.md).

Os scripts `brief_alignment.py`, `positioning_copy_contract.py`, `search_presence_audit.py` e `review_council.py` são verificadores opcionais, não certificados de qualidade.

## V12: execução real

Os validadores opcionais verificam diversidade estrutural, inventário de assets, plano cinematográfico, pacotes de evidência e aprendizado com contraprovas. Não criam arte, não substituem implementação e não certificam qualidade estética. Instruções e formatos em [PRODUCTION_SYSTEM_V12.md](PRODUCTION_SYSTEM_V12.md). Use conforme o escopo; PATCH simples não exige novos rituais.

## Processo
1. Inspecionar produto, rota, assets, identidade, público e invariantes antes de editar.
2. Observar página inteira, mobile, estados e fluxo de uso real; registrar observado/inferido/proposto/não verificado.
3. Em redesign estrutural, propor teses diferentes e escolher por clareza, prova, marca, acessibilidade e custo, não preferência vazia.
4. Compor storyboard por pergunta, evidência e ação; construir incrementos pequenos.
5. Validar no navegador, inclusive desktop/mobile, CTA, estados, teclado, reduzido movimento e regressões.
6. Corrigir defeitos P0/P1 comprovados. Documentar o que não pôde testar.

## Exemplo de pedido
"Ative studio-grade-web-transformation. Faça uma auditoria real do meu projeto, preserve fluxos críticos, proponha duas direções de redesign coerentes com minha marca, escolha a mais forte e implemente. Capture página inteira desktop/mobile, teste interações e corrija o pior elo. Não invente resultados."

## Crítica independente e aprendizado com evidências

Em REDESIGN/REBUILD significativos, faça uma revisão independente da saída renderizada quando possível. Separe crítica visual, validação funcional/acessibilidade e evidência de usuários. Uma autocrítica não é uma revisão independente, e avaliações declaradas não são benchmarks executados. Consulte `references/independent-critique-and-evidence-learning.md` para fixar condições, repetir execuções, preservar resultados negativos e registrar o que permanece UNKNOWN.

## Testes e limites
`scripts/check_contracts.py` verifica contratos comerciais do exemplo sintético. `scripts/check_evals.py`, `scripts/test_validators.py` e `skills/.../scripts/validate.py` validam só estrutura. `npm run test:browser:fixtures` verifica fixtures sintéticas, não estética. `scripts/run_evals.py` depende de CLI de agente externo. O documento `docs/EVALUATION_RUNBOOK.md` explica avaliação cega. A rubrica também viaja na skill em `references/quality-rubric.md`.


Ferramenta estratégica: `python skills/studio-grade-web-transformation/brain/route.py skills/studio-grade-web-transformation/brain/examples/fintech-landing.json`. Ver `docs/V95_ARCHITECTURE.md`. 

## V11.0: menos ritual, mais execução
Para rebuilds: autópsia da página → duas direções → implementar abertura/miolo/fecho → capturar desktop/mobile → corrigir pior trecho → recapturar. Veja `references/creative-production-loop.md` e `references/brand-fidelity-review.md`.

## V11.0: RESONANCE method
For artistic REDESIGN/REBUILD, choose two different *formal* hypotheses, build a middle and ending as seriously as the hero, inspect five rendered frames and recover from failed full-page captures. Review the best rival direction without bias. Do not impose this ceremony on PATCH or routine dashboards.

## V10.1 methods preserved
For authored interactive products also consult creative-advantage-loop.md, immersive-3d-product-direction.md and SCENE_CHALLENGE.md. Offline journey_board.py complements the reproducible capture and pair-review V11 tools.

## V11.6.1 — resultado verificável
- Um pedido `analise e implemente` precisa de implementação real.
- Antes de prometer escopo protegido, inspecione o diff e rode o verificador
  com `docs/SCOPE_POLICY.example.json` adaptado ao projeto.
- Faça revisões comparativas com `--evidence-root` quando os arquivos existirem.
- Execute benchmark real de acordo com `docs/REAL_WORLD_BENCHMARK_V11_6.md`.
