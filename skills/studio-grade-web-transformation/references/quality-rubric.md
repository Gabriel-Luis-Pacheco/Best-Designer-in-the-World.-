# Rubrica de qualidade visual, funcional e de produto (v9.6)

Este documento dá critérios para humanos compararem artefatos, não substitui testes observados. Sem projeto executável ou capturas integrais, a dimensão correspondente é `UNKNOWN`.

Escala consistente para TODAS as dimensões:
- `0 FALHA`: problema demonstrável que atrapalha objetivo.
- `1 ACEITÁVEL`: funciona ou comunica o mínimo, mas há deficiências evidentes.
- `2 FORTE`: adequado, coerente e bem acabado no contexto.
- `3 EXCEPCIONAL`: solução distintiva e refinada, apoiada em exemplos concretos e contexto.

Dimensões: `clareza`, `direcao_arte`, `narrativa`, `identidade`, `composicao`, `microcraft`, `mobile`, `funcionalidade`, `acessibilidade`, `conteudo_credibilidade`, `performance`.
Marcar `UNKNOWN` como valor `null` ou omitir a dimensão, documentando por quê. Não atribuir 3 só por estética pessoal; relacionar cada nota a observação e artefato.

Exemplos de ancoragem:
- Clareza 0: não é possível identificar produto/CTA; 2: promessa concreta visível; 3: promessa, prova e ação se reforçam sem esforço.
- Direção de arte 0: incoerência ou cópia literal; 2: linguagem consistente; 3: composição autoral justificada pela experiência do produto.
- Mobile 0: tarefas centrais inviáveis; 2: leitura e ações fluem em 390 px e zoom; 3: recomposição dedicada com igual hierarquia e sem esforço extra.
- Funcionalidade 0: CTA quebrado; 2: fluxos testados e utilizáveis; 3: fluxos, recuperação e estados críticos muito bem resolvidos.
- Acessibilidade 0: barreira severa comprovada; 2: testes essenciais realizados sem barreiras conhecidas; 3: verificação ampliada com tecnologias assistivas e evidências.
- Performance: UNKNOWN sem medida; 2 apenas com ambiente e métricas registradas.

Severidade em separado: P0 (falha central, falsidade, perda de dados), P1 (prejuízo relevante e demonstrável à tarefa/identidade), P2 (acabamento local). A estética subjetiva sozinha não é P1. P0/P1 conhecido bloqueia status aprovado. A média não apaga bloqueadores.

Campos mínimos por revisão: caso, `pair_id` igual para as duas condições do mesmo par, condição (`with_skill`/`without_skill`), identificador de execução, revisor, dimensões avaliadas 0–3, `evidence` com links/caminhos ou comandos e resultados PASS/FAIL/UNKNOWN. Avaliação cega é preferível; registrar se houve. Não converter notas de uma pessoa em resultado de usuários reais.

Roteiro: primeiro screenshot inteira sem conhecer variante; segundo revisar ações, estados e mobile; terceiro anotar pior elo e riscos; quarto conferir evidência independente. Comparar dois artefatos da MESMA tarefa. Não afirmar ganho estatístico com amostra mínima.
