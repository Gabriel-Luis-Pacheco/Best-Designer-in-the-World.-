# Auditoria tecnica Design OS Prime v14.0.0 — 22/11/2026

**Escopo:** arquitetura e estado do repositório público `Gabriel-Luis-Pacheco/Best-Designer-in-the-World.-`, contrato do `SKILL.md`, matriz/atlas, seleção de especialistas, roteamento primário Brain, injeção nos prompts de avaliação, referências e evidências de benchmark, sistema de gates, pacote CORE e testes automatizados. Verificação estrutural da árvore completa. Não é uma auditoria manual de cada arquivo dos 12 repositórios terceirizados incorporados nem validação de uma landing page/produto específico no navegador.

**Regra de honestidade:** PASS de teste Python não equivale a qualidade visual, comprovação de UX, conformidade WCAG, aprovação por copywriter humano ou aumento de receita. O repositório disponibiliza protocolos e validadores, mas não ativa navegador nem especialistas externos por si só.

## Inventário e situação real

| Item | Evidência observada na árvore | Implicação |
|---|---:|---|
| Repositório FULL | 18.798 arquivos, 575.214.412 bytes em blobs de arquivo | Alto custo de clone, pesquisa e manutenção |
| Espelhos full-upstream | 16.134 arquivos / 485.952.214 bytes | Biblioteca de terceiros; não deve ser carregada indiscriminadamente |
| Packs externos selecionados | 2.166 arquivos / 45.848.059 bytes | Referências opcionais; não provam ferramentas instaladas |
| Revenue-centric-design | 104 arquivos / 41.053.396 bytes | Verificar/licenciar separadamente; LICENSE raiz não os substitui |
| Arquivos fora de `vendor/` | 363 no snapshot inicial | Núcleo próprio muito menor que FULL |
| Guias de referência próprios | 110 arquivos na pasta `references/` | Exige seleção contextual, não pré-carregamento |
| Matriz/atlas | 47 perfis de componente / 15 fases condicionais | Orquestração granular mas exigente em manutenção |
| Transferência de benchmark | 16 fluxos priorizados | Adoção/adaptação de padrões com níveis de evidência |

Os números são inventário de árvore, **não** significa que cada documento de terceiros foi lido, auditado ou aprovado.

## Achados por severidade e ação

### P1 — Corrigido: roteador principal não passava pelo workplan especializado

**Antes:** `brain/pipeline.py` só retornava a estratégia de `brain/route.py` (e inventário/decisões de escopo opcionais). O catálogo de especialistas por componente ficava separado em `scripts/component_workplan.py`; o uso do Brain não assegurava que um redesign de onboarding levasse as fases de mercado, ativação e QA.

**Mudança:** `brain/component_bridge.py` integra os manifests existentes ao `brain/pipeline.py` com um resumo limitado de etapas, candidatos por competência, requisitos de transferências competitivas e status honesto. Aceita IDs de componentes explícitos no JSON (`components`), ou reconhecimento **provisório** por aliases no pedido. No pedido amplo `melhore tudo`, devolve `COMPONENT_INVENTORY_REQUIRED` em vez de inventar seções. **Não invoca especialistas nem pesquisa automaticamente.**

**Regressão:** `scripts/test_pipeline.py` exige seleção coerente para hero, onboarding, checkout, PATCH, escopo explícito e pedidos sem inventário.

### P1 — Corrigido: guia novo de benchmark podia desaparecer antes de chegar ao modelo

**Antes:** mesmo com a regra no `SKILL.md`, `scripts/run_evals.py` injetava referências antigas e aplicava limites/truncamento. Os protocolos de onboarding e conversão podiam não entrar no prompt final. Um primeiro teste adicionando a referência falhou exatamente por ela ser removida posteriormente.

**Mudança:** para REDESIGN/REBUILD pertinente, a seleção agora injeta `references/benchmark-pattern-transfer-and-validation.md` e o protege na etapa de substituição sob orçamento, sem incluir em PATCH ou dashboard operacional. `scripts/test_audit_eval_routing.py` valida **o texto realmente montado** para o agente, não só o catálogo.

### P1 — Corrigido: pesquisa de outro componente podia ser usada como evidência deste

**Antes:** `component_delivery_gate.py` validava a estrutura do JSON de concorrentes, mas não comparava seu `component_id` e `mode` ao redesign em análise.

**Mudança:** exige identidade de componente e modo consistentes. Teste com `checkout` tentando servir de evidência para `hero` retorna `INVALID`.

### P2 — Corrigido: limite do SKILL.md medido em caracteres e não bytes

O ponto de entrada tinha 9.973 caracteres mas 10.038 bytes UTF-8, acima do limite operacional informal de 10 KB. Foi condensado mantendo links essenciais e explicando o novo `brain/pipeline.py`; o ponto de entrada passa a ter 9.999 bytes UTF-8.

### P1 — Aberto: "skills integradas" não significa especialistas efetivamente executados

Existem skill packs, registros de fontes, guias, roteador e logs declarados de aplicação, mas não há um orquestrador universal capaz de obrigar Claude/Codex/OpenCode/Grok a realmente ler e usar todos os especialistas. O mesmo vale para o navegador: os scripts locais não capturam espontaneamente os dez concorrentes nem testam a interface final.

**Recomendação:** no runtime específico usado pelo agente, instrumentar o consumo real de referências com recursos autorizados de navegador e registro de decisões por etapa. Proibir alegações de uso/executado sem artefatos. Não converter fontes externas em instruções privilegiadas.

### P1 — Aberto: FULL excessivamente grande para instalação cotidiana

O repositório completo é pesado e contém licenças de terceiros distintas. Existe `scripts/build_core_package.py`, que gera ZIP CORE reproduzível e exclui `vendor/`. **A CORE deve ser a opção padrão de uso cotidiano quando suportada.** Não remover espelhos/licenças sem revisão. Publicar a CORE como release instalável ou origem separada reduziria download/clone, mas requer decisão explícita sobre distribuição.

### P1 — Aberto: qualidade de copy, arte e conversão não tem prova automática

Os gates são predominantemente **verificações estruturais**. Screenshot PNG íntegro não certifica que as capturas mostram o site real ou que um layout funciona. Nome de concorrente grande não valida sua taxa de conversão. A avaliação editorial automatizada não substitui editor humano. Métricas exigem telemetria real e desenho experimental adequado.

**Recomendação:** estudo de caso completo e replicável em uma página real, com matriz de referências capturadas, implementação antes/depois, avaliação humana independente, fluxos completos, mobile, acessibilidade, performance e instrumentação de primeira tarefa. Publicar resultados medidos, inclusive perdas/UNKNOWN.

### P2 — Aberto: mapa das referências precisa continuar coerente com o runtime

110 referências não devem ser enviadas juntas ao modelo. O `SKILL.md` já adota progressive disclosure; as rotas de `run_evals.py` e os limites de tokens devem ser testados sempre que se adiciona uma referência, para evitar que conteúdo essencial suma na truncagem. O teste introduzido verifica especificamente o protocolo de benchmark em um fluxo de produto.

### P2 — Aberto: atualização de espelhos e direitos de uso requer governança

O FULL conserva cópias independentes, assets e materiais licenciados. `SKILL.md` declara corretamente que licenças específicas prevalecem. Antes de incorporar novo vendor, validar licença, origem, segurança, qualidade e necessidade; limitar execução de scripts externos. **Não houve auditoria de cada uma das 18 mil fontes terceirizadas.**

## Matriz de subsistemas

| Sistema | Situação da revisão | O que o teste garante |
|---|---|---|
| Ponto de entrada SKILL | Ajustado | Referências e versão coerentes, tamanho UTF-8 menor |
| Router de objetivo e superfície | Mantido | Hipóteses determinísticas, não interpretação humana |
| Brain pipeline | **Integrado com componentes** | Encaminhamento em planilha JSON, sem execução |
| Atlas de especialistas | Mantido | 47 perfis e fallback contextual já existentes |
| Benchmark de concorrentes | **Injetado e protegido no runner** | O guia entra em prompts pertinentes |
| Research/delivery gates | **Vinculação componente/modo reforçada** | Impede reuso acidental entre componentes |
| QA renderizado | Sem alteração de capacidade | Fixtures browser sintéticas ≠ teste de produto |
| Avaliações A/B de agente | Sem execução de modelos reais nesta revisão | Suite verifica prompts/roteamento, não vence comparações |
| Distribuição CORE/FULL | Mantida | CORE exclui vendor; FULL segue pesado |
| Direitos, performance, acessibilidade | Protocolos existentes | Exigem verificação por projeto |

## Validação recomendada

Na raiz do repositório:

~~~bash
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/check_docs.py
python scripts/audit_eval_routing.py
python scripts/build_core_package.py --output dist/design-os-prime-core.zip
~~~

**Reprodução do caminho principal** (a execução apenas planeja):

~~~bash
python skills/studio-grade-web-transformation/brain/pipeline.py plano.json
~~~

O JSON pode conter `context` e `components: ["onboarding", "activation"]`. Ver `brain/README.md`. Verificar os checks da pull request de revisão antes de alegar CI final completo.

## Decisão de arquitetura

O maior avanço possível daqui não é ter 100, 300 ou 1000 skills. É reduzir a distância entre conhecimento, decisões e pixels, com seleção contextual, evidência de uso real, teste visual, feedback humano e validação pós-lançamento. Nenhuma métrica comercial deve ser inferida de um catálogo ou captura.
