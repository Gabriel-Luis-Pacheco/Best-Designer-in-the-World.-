# Human review rubric — v11.4
# Rubrica de qualidade visual, funcional e de produto (v9.8)

Este documento dá critérios para humanos compararem artefatos, não substitui testes observados. Sem projeto executável ou capturas integrais, a dimensão correspondente é `UNKNOWN`.

Escala consistente para TODAS as dimensões:
- `0 FALHA`: problema demonstrável que atrapalha objetivo.
- `1 ACEITÁVEL`: funciona ou comunica o mínimo, mas há deficiências evidentes.
- `2 FORTE`: adequado, coerente e bem acabado no contexto.
- `3 EXCEPCIONAL`: solução distintiva e refinada, apoiada em exemplos concretos e contexto.

Dimensões gerais: `clareza`, `direcao_arte`, `narrativa`, `identidade`, `composicao`, `microcraft`, `mobile`, `funcionalidade`, `acessibilidade`, `conteudo_credibilidade`, `performance`.

Em ART/EXPERIENCE/EXPERIENTIAL_COMMERCE, acrescentar quando observável `reconhecimento_produto`, `continuidade_cenas`, `agencia_interativa`, `climax_encerramento`. Elas são opcionais para dashboards, patches e páginas sem narrativa: não penalize o projeto por uma métrica irrelevante. Não use média para esconder uma falha de reconhecimento do produto vendido, funcionalidade ou acesso.
Marcar `UNKNOWN` como valor `null` ou omitir a dimensão, documentando por quê. Não atribuir 3 só por estética pessoal; relacionar cada nota a observação e artefato.

Exemplos de ancoragem:
- Clareza 0: não é possível identificar produto/CTA; 2: promessa concreta visível; 3: promessa, prova e ação se reforçam sem esforço.
- Direção de arte 0: incoerência ou cópia literal; 2: linguagem consistente; 3: composição autoral justificada pela experiência do produto.
- Mobile 0: tarefas centrais inviáveis; 2: leitura e ações fluem em 390 px e zoom; 3: recomposição dedicada com igual hierarquia e sem esforço extra.
- Funcionalidade 0: CTA quebrado; 2: fluxos testados e utilizáveis; 3: fluxos, recuperação e estados críticos muito bem resolvidos.
- Acessibilidade 0: barreira severa comprovada; 2: testes essenciais realizados sem barreiras conhecidas; 3: verificação ampliada com tecnologias assistivas e evidências.
- Performance: UNKNOWN sem medida; 2 apenas com ambiente e métricas registradas.
- Reconhecimento do produto: 0 se uma página comercial faz o produto parecer um objeto diferente; 2 se forma, texto e prova tornam seu uso evidente; 3 se reconhecimento e singularidade estética se reforçam. Para arte abstrata sem produto, omitida.
- Continuidade de cenas: 0 quando cada trecho parece outro template; 2 para transições com vocabulário visual consistente; 3 para narrativa autoral que progride sem repetição.
- Agência interativa: 0 quando controle é ornamental ou inacessível; 2 quando modifica algo compreensível e reversível; 3 quando o gesto revela a ideia central do projeto.
- Clímax e encerramento: 0 quando a experiência abandona o visitante sem resolução; 2 quando fechamento e ação/artefato são relevantes e honestos; 3 quando o final transforma o significado do início.

Severidade em separado: P0 (falha central, falsidade, perda de dados), P1 (prejuízo relevante e demonstrável à tarefa/identidade), P2 (acabamento local). A estética subjetiva sozinha não é P1. P0/P1 conhecido bloqueia status aprovado. A média não apaga bloqueadores.

Campos mínimos por revisão: caso, `pair_id` igual para as duas condições do mesmo par, condição (`with_skill`/`without_skill`), identificador de execução, revisor, dimensões avaliadas 0–3, `evidence` com links/caminhos ou comandos e resultados PASS/FAIL/UNKNOWN. Avaliação cega é preferível; registrar se houve. Não converter notas de uma pessoa em resultado de usuários reais.

Roteiro: primeiro screenshot inteira sem conhecer variante; segundo revisar ações, estados e mobile; terceiro anotar pior elo e riscos; quarto conferir evidência independente. Comparar dois artefatos da MESMA tarefa. Não afirmar ganho estatístico com amostra mínima.

## Creative ceiling review — v11.1
For ART/EXPERIENTIAL_COMMERCE, additionally compare FORMAL signature, MATERIAL system, BEHAVIORAL signature and meaningful climax across captured frames. A technical PASS and polished documentation are not proof that a site is artistically stronger than a rival. Assess blind without knowing the skill variant, and record real screenshots/states and shortcomings. These are contextual human judgments, NOT automatically computed scores; do not force WebGL, exports or theatrical interactions into unrelated products.

## Field-backed checks — v11.2
For creative-technology work, record real visual states and frame pacing/device/browser (or UNKNOWN); a Three.js import is not proof of a smooth immersive experience. For commercial LPs, keep artistic distinction separate from product clarity, truthful CTA, activation and measured conversion (or UNKNOWN). Historical award weights do not override product goals. See references/award-readiness-and-qa.md and references/landing-page-evidence-and-cro.md; never invent an award or audited UX outcome.

## v11.3 specialty evidence boundaries
Text/markup heuristics: REVIEW (never automatic aesthetic FAIL). DTCG aliases: partial structural checks, no automatic contrast pass. Specialist candidates: NOT_INSTALLED and NOT_READ until a true execution trace proves otherwise. For site handoff, distinguish deployed/working from proposal. In marketing, separate measured qualified conversion from the design agent's A/B win rate.

## v11.4 competition integrity
Pair competitor reviews only with the same task SHA, asset/model/tool/budget controls and rating axes. A mixed tradeoff is never an overall win; a P0/P1 on one condition takes precedence over pixel taste. Layout audit findings are REVIEW not WCAG failures. Multiple projects, repeat runs, actual blinded raters and ability to reproduce artifacts are necessary to support claims of consistent superiority.
