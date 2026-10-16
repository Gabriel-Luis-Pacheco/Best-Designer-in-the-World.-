# Avaliação da skill em casos reproduzíveis

A pasta `evals/evals.json` agora contém cenários conceituais E fixtures sintéticas reais em `fixtures/` (HTML, SVG, brief e contratos de dados). Fixtures não são sites de produção nem modelos de qualidade; alguns defeitos foram preservados intencionalmente.

## Protocolo A/B
1. Fixar modelo/versão, ferramentas, orçamento, ambiente e a mesma entrada em ambas as condições.
2. Executar `without_skill` e `with_skill` separadamente; a única diferença de condição deve ser a orientação da skill. Se ferramentas ou recursos divergirem, marcar estudo inválido para causalidade.
3. Executar pelo menos duas repetições por condição quando viável. Gravar prompts, saídas, mudanças de código, capturas e logs, sem segredos.
4. Revisores que desconhecem a condição avaliam os artefatos usando `references/quality-rubric.md`. Não pedir ao mesmo agente que produziu o design para fingir avaliação independente.
5. Executar tarefas reais de interação, registrar sucesso, erros, bloqueadores P0/P1 e custo/tempo. Preferência estética não substitui sucesso de tarefa.
6. Usar notas de 0–3, com evidência por afirmação; `UNKNOWN` não é `PASS`. Não inferir ganho de conversão.
7. Repetir após mudanças e publicar regressões, não só casos favoráveis.

## Ferramentas no repositório completo
`scripts/check_evals.py` e `scripts/test_validators.py` validam ESTRUTURA, não designs. `scripts/score_review.py` resume notas humanas existentes; `scripts/compare_reviews.py` compara casos pareados sem alegar significância. `scripts/run_evals.py` é um adaptador CLI opcional para executar um agente que leia prompt por stdin; não prova qualidade sozinho. Um ambiente sem modelo/revisor real não pode afirmar teste A/B realizado.

A instalação isolada acompanha `scripts/validate.py`, as fixtures e a rubrica; ferramentas de agregação no repositório completo são opcionais.

## Pareamento e isolamento dos experimentos
Cada condição roda no seu próprio diretório limpo, mas não há isolamento de credenciais, contexto remoto ou rede. Revisões comparáveis usam pair_id, mesmo revisor, dimensões iguais e run_id diferentes. Arquivos gerados somente são arquivados com opt-in. Consulte `references/evaluation-isolation-protocol.md`.
