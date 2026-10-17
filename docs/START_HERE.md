# Design OS Prime v11.1 — Start here

A skill serve para criar, implementar ou revisar design sem perder realidade de produto.

## Selecione o menor escopo adequado
PATCH corrige uma falha local; AUDIT analisa sem criar implementação fictícia; REFINE melhora tela boa; REDESIGN altera arquitetura ou direção; REBUILD reconstrói quando problemas sistêmicos justificam. Distinga MARKETING (clareza, prova, conversão) de PRODUCT (precisão, tarefas, densidade e estados).

## Processo
1. Inspecionar produto, rota, assets, identidade, público e invariantes antes de editar.
2. Observar página inteira, mobile, estados e fluxo de uso real; registrar observado/inferido/proposto/não verificado.
3. Em redesign estrutural, propor teses diferentes e escolher por clareza, prova, marca, acessibilidade e custo, não preferência vazia.
4. Compor storyboard por pergunta, evidência e ação; construir incrementos pequenos.
5. Validar no navegador, inclusive desktop/mobile, CTA, estados, teclado, reduzido movimento e regressões.
6. Corrigir defeitos P0/P1 comprovados. Documentar o que não pôde testar.

## Exemplo de pedido
"Ative studio-grade-web-transformation. Faça uma auditoria real do meu projeto, preserve fluxos críticos, proponha duas direções de redesign coerentes com minha marca, escolha a mais forte e implemente. Capture página inteira desktop/mobile, teste interações e corrija o pior elo. Não invente resultados."

## Testes e limites
`scripts/check_contracts.py` verifica contratos comerciais do exemplo sintético. `scripts/check_evals.py`, `scripts/test_validators.py` e `skills/.../scripts/validate.py` validam só estrutura. `npm run test:browser:fixtures` verifica fixtures sintéticas, não estética. `scripts/run_evals.py` depende de CLI de agente externo. O documento `docs/EVALUATION_RUNBOOK.md` explica avaliação cega. A rubrica também viaja na skill em `references/quality-rubric.md`.


Ferramenta estratégica: `python skills/studio-grade-web-transformation/brain/route.py skills/studio-grade-web-transformation/brain/examples/fintech-landing.json`. Ver `docs/V95_ARCHITECTURE.md`. 

## V11.0: menos ritual, mais execução
Para rebuilds: autópsia da página → duas direções → implementar abertura/miolo/fecho → capturar desktop/mobile → corrigir pior trecho → recapturar. Veja `references/creative-production-loop.md` e `references/brand-fidelity-review.md`.

## V11.0: RESONANCE method
For artistic REDESIGN/REBUILD, choose two different *formal* hypotheses, build a middle and ending as seriously as the hero, inspect five rendered frames and recover from failed full-page captures. Review the best rival direction without bias. Do not impose this ceremony on PATCH or routine dashboards.

## V10.1 methods preserved
For authored interactive products also consult creative-advantage-loop.md, immersive-3d-product-direction.md and SCENE_CHALLENGE.md. Offline journey_board.py complements the reproducible capture and pair-review V11 tools.
