# Design OS Prime 9.5 — ferramentas e cérebro

## Dois sistemas integrados
**Toolbelt**: contratos de produto, auditoria HTML de origem, preservação de dados, Playwright em Chromium, verificação de anexos, bloqueio conservador de P0/P1, avaliador humano pareado e runner A/B com workspaces separados.

**Brain**: roteiro `brain/route.py`, regras `route_rules.json`, matriz de vertical/superfície, seleção de packs e fontes, perguntas de pesquisa, `decision_guard.py` e `feedback_loop.py`.

O motor determinístico NÃO substitui raciocínio, inspeção, browser, UX research, métricas ou revisão artística. O agente que usa a skill precisa processar o contexto e corrigir hipóteses do motor. URLs são candidatos, não uma alegação de pesquisa.

## Progressão de engenharia
| Versão | Recurso efetivamente adicionado |
| --- | --- |
| 8.2 | Contratos estáticos de produto e testes negativos |
| 8.3 | Catálogo contextual de 18 fontes e playbook de pesquisa |
| 8.4 | Auditoria HTML offline, com limites explícitos |
| 8.5 | Verificação de anexos e hashes de evidência |
| 8.6 | Gate P0/P1 honesto, sem autocertificação |
| 8.7 | 24 cenários e tensões entre metas |
| 8.8 | Controles de ARIA, rótulos e teclado |
| 8.9 | Validação de curadoria e templates de discovery |
| 9.0 | Roteador estratégico configurável, com três exemplos |
| 9.1 | Testes adversariais de classificação e 28 evals |
| 9.2 | Guard de autorização e contratos protegidos |
| 9.3 | Pesquisa por pergunta, vertical e superfície |
| 9.4 | Feedback de resultados com risco de regressão |
| 9.5 | Integração do cérebro ao runner A/B e smoke tests ponta a ponta |

## Exemplo de decisão
Fintech landing: conversão + confiança, prova comercial e condições; pesquisa visual pode ser relevante.
Mesma fintech backoffice: exatidão + eficiência, logs, chaves, operações densas; galerias de marketing não são referência automática.

## Verificação e honestidade
- `python scripts/check_evals.py`, `scripts/verify_brain_examples.py`, `scripts/check_contracts.py`, testes Python e Playwright garantem apenas os checks executados.
- A/B real com agente requer rodar o runner com uma CLI confiável, capturar artefatos, revisão humana comparável e avaliar regressões.
- Sem esse experimento, não há prova de superioridade criativa, ganho de conversão, retenção ou valor comercial.
- A ausência de login/acesso web impede a inspeção de recursos restritos; não alegar que Mobbin ou galerias foram acessadas.
