# Auditoria crítica da Design OS Prime — 20/11/2026

**Escopo:** inventário completo da árvore Git de main, revisão de SKILL.md, README, scripts de validação, workflows, referências centrais de direção de arte, landing, copy, evidências, portabilidade e benchmark. **Não** houve leitura manual de cada arquivo terceirizado, benchmark cego com pessoas ou avaliação visual de um site real.

## Inventário observado

| Informação | Medida |
|---|---:|
| Arquivos versionados | 18.773 |
| Arquivos sob vendor/ | 18.435 |
| Arquivos próprios fora de vendor/ | 338 |
| Tamanho bruto dos arquivos próprios fora de vendor/ | ~1,81 MB |
| Referências internas próprias | 105 arquivos Markdown |
| CI no main inspecionado | Validate Design OS e Competitive lab regressions passaram em 19/11 |
| Prova de superioridade visual/comercial | Não demonstrada por testes estruturais |

## Achados prioritários

### P1 — Biblioteca externa desproporcional
**Fato:** ~98,2% dos arquivos são cópias sob vendor. O projeto já oferece um CORE offline e preserva licenças independentes. **Risco ainda não mensurado:** tempo de clone, busca ruidosa, custo de navegação e manutenção. **Melhoria aplicada:** quickstart no topo do README e destaque para o CORE, sem apagar terceiros. Próximo passo separado: publicar CORE como pacote leve diretamente instalável e rever versões/procedência/licenças por upstream.

### P1 — Redesign pode ignorar o meio e final da página
**Fato:** existem gates de briefing, produção, screenshots e fluxo de primeiro valor, mas não um contrato específico cobrindo **todas as seções declaradas** com before/after e decisão KEEP/REWORK/ADD/REMOVE. **Aplicado:** guia section-parity-and-competitive-rebuild.md, template JSON e script section_parity.py com testes. **Limite:** o agente precisa inventariar DOM/rotas de verdade; JSON declarativo não detecta se o agente omitiu uma seção. O script não avalia beleza de pixels nem preferência de clientes.

### P1 — Orquestração pode substituir trabalho concreto
**Fato:** o núcleo menciona cinco famílias especialistas, 50 skills e 12 repositórios completos. Já diz para só executar ferramentas de fato disponíveis. **Recomendação:** manter especialista apenas quando altera uma decisão, evitar leitura automática de vendor e sempre priorizar código, render e correção de causas. Arquivo copiado não é motor instalado nem agente executado.

### P2 — README estruturado como changelog
**Fato:** instrução para instalar aparecia depois de uma longa sequência de notícias sobre integrações. **Aplicado:** instrução clara, modo de uso e exemplo de solicitação primeiro, mantendo o histórico logo abaixo.

### Alerta permanente — CI verde não prova estética nem vendas
**Fato:** as pipelines passaram em main, mas testam código, contratos e fixtures sintéticas, não uma landing viva com usuários. O repositório já declara corretamente esse limite. **Próxima validação:** testar comparações controladas sem skill vs Design OS vs um especialista, com mesmo brief/modelo/assets, capturas pareadas e avaliação humana cega. Medir conversão apenas com instrumentação e tráfego reais. Consulte EXECUTION_AND_BENCHMARK_2026-11-19.md.

## O que esta PR altera

1. README e START_HERE passam a orientar uma execução rápida.
2. SKILL.md passa a rotear explicitamente a reconstrução seção por seção.
3. Novo protocolo de comparação real de páginas, sem clonagem de marca.
4. Novo validador Python offline para cobertura, PNG, CTA→primeiro valor, P0/P1 e honestidade de evidência.
5. Testes de regressão para lacunas, arquivos inválidos, segurança de caminhos, primeira experiência e aprovação indevida.
6. Índice de referências sincronizado.

## O que não foi feito nem alegado

Não houve alteração de site real, checkout, backend, deploy ou dados de clientes. Não houve remoção de vendor, mudança de licenças, benchmark com usuários ou promessa de conversão. Nenhum dos 18.435 arquivos externos foi supostamente revisado linha a linha.

**Aceite:** CI passando; template novo inicia como UNKNOWN; testes de status INVALID, BLOCKED, NEEDS_EVIDENCE e READY_FOR_HUMAN_REVIEW. O último significa material pronto para revisão humana, jamais certificação estética.
