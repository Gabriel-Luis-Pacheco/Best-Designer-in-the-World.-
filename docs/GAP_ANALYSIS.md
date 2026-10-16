# Lacunas V7 → V8

| Problema | V8 implementou | Falta comprovar |
|---|---|---|
| Guia criativo superficial | Anti-slop construtivo + tipografia/layout + interações com exemplos | Melhoria artística em outputs reais |
| Proibições sem alternativas | Duas teses criativas comparadas com trade-offs | Originalidade efetiva |
| Processos pesados em patches | Modos PATCH/AUDIT/REFINE/REDESIGN/REBUILD | Aderência dos agentes |
| Evals somente textuais | 16 cenários, fixtures reais sintéticas HTML/SVG e briefs | A/B com modelos e revisores reais |
| Rubrica de quatro níveis vs notas 0–4 | Escala única 0–3, scripts validam notas e evidência | Concordância entre revisores |
| CTA citado mas não testado | Checagem de CTA estático no browser, suite de fixtures | Fluxos específicos reais |
| CI só de metadados | Python unit + portátil + testes Chromium | Qualidade estética/usuários |
| Rubrica fora do pacote | Cópia portátil verificada pelo validador | Uso real pelo agente |

A V8 é uma melhoria operacional demonstrável em CÓDIGO E COBERTURA. Não afirmar melhora de conversão, estética ou satisfação sem testes específicos.


## V8 → V8.1 — melhorias integradas
| Falha verificada | Mudança executada | Ainda depende de prova |
| --- | --- | --- |
| A/B compartilha cwd e pode contaminar artefato | Diretório temporário por caso/condição, só com fixtures da entrada | Isolamento de conta, rede, perfil e agentes externos |
| Média humana misturava dimensões/revisores | Pareamento por case_id/pair_id/reviewer/dimensões | Revisão humana real com mais de uma repetição |
| Destino de plano poderia divergir | Exemplo alinhado ao brief, checagens negativas de preço, CTA, âncoras e plano | Contratos por projeto real, checkout e ações externas |
| Playbooks artísticos resumidos | Guias editoriais, motion, operações e prova, ligados ao SKILL.md | Comparar qualidade visual de outputs reais |
| Apenas 16 cenários | 20 cenários de avaliação | A/B com modelo real e revisor independente |

**Critério de aceitação:** CI verde significa que verificações de código e fixtures passaram; não constitui certificação estética, comercial, de acessibilidade integral ou de UX com pessoas.
