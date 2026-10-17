# Auditoria exaustiva da conversa → Design OS Prime v11.2

Data: 17/10/2026. Escopo: **duas respostas anteriores com rankings de skills**, pesquisa de Awwwards e guia Markdown citado na conversa, confrontados com a árvore da v11.1.0 (159 arquivos) antes da integração. Este documento não é benchmark, nem atestado de que cada repo mencionado nas respostas anteriores existe ou está atualizado.

**Estados:** EXISTIA = mecanismo substantivo já contemplado; APROFUNDADO = método mais operacional neste upgrade; NOVO = regra, evidência ou referência especializada adicionada; CONSULTAR = fonte/candidato externo, não incorporado como código/skill; REJEITADO = não importar indiscriminadamente. Todos os links externos são material não confiável até verificação de licença, conteúdo, segurança e versão no uso.

## 1. O processo Awwwards e o guia de pesquisa (cobertura conceitual)

| Descoberta / item exato da conversa | Estado antes → agora | Integração e limite |
|---|---|---|
| Design / Usabilidade / Criatividade / Conteúdo; pesos 40/30/20/10 citados | REFERÊNCIA → APROFUNDADO | references/awwwards-studio-production.md; pesos históricos são contexto, não rubrica geral do produto, confirmar atualidade |
| Honorable Mention / SOTD / SOM / SOTY / Developer Award | REFERÊNCIA → CONSULTAR | prêmio e elegibilidade apenas na fonte oficial atual; nenhum 'selo' automático |
| Investigar produto/audiência/objetivo antes do código | EXISTIA | SKILL.md, brain/route.py, product-truth.md |
| Diferenciar landing, produto, backoffice, arte e commerce artístico | EXISTIA | brain/route_rules.json, experiential-commerce.md |
| Definir lei formal/material/comportamental própria da marca | EXISTIA | creative-signature-and-form.md, creative-advantage-loop.md |
| Gerar conceitos realmente diferentes (não mudar cores) | EXISTIA | creative-advantage-loop.md; até 3 hipóteses, não 3 sites completos |
| Provar cena-chave tecnicamente arriscada ANTES da página inteira | PARCIAL → NOVO | awwwards-studio-production.md, creative-technology-playbook.md |
| Planejar abertura, transformação, meio, interação, clímax, encerramento | EXISTIA/APROFUNDADO | interaction-dramaturgy-and-payoff.md, studio module |
| Manter hero e meio igualmente autorais | EXISTIA/APROFUNDADO | creative-advantage-loop.md, award-readiness-and-qa.md |
| Site artístico sem CTA comercial obrigatório | EXISTIA | creative-experience-direction.md |
| Landing artística com produto reconhecível + CTA honesto | EXISTIA/APROFUNDADO | experiential-commerce.md, landing-page-evidence-and-cro.md |
| Não usar animação ou 3D sem função | EXISTIA/APROFUNDADO | motion-and-interaction-direction.md, creative-technology-playbook.md |
| Design mobile composto, não miniaturizado | EXISTIA/APROFUNDADO | SKILL.md e módulos de produção, 390px e touch |
| Comparar cenas e estados temporais, não só screenshot comprida | EXISTIA/APROFUNDADO | creative-evidence-journey.md, award-readiness-and-qa.md |
| Capturar real e registrar sem evidência como UNKNOWN | EXISTIA | quality-gates-and-evidence.md, testes e rubrica |
| Crítica adversarial e consertar o pior elo causal | EXISTIA/APROFUNDADO | creative-advantage-loop.md, award-readiness-and-qa.md |
| Loop de duas passagens visual/funcional quando viável | EXISTIA/APROFUNDADO | SKILL.md, award-readiness-and-qa.md, sem ciclo infinito |
| Não declarar vitória A/B com uma amostra só | EXISTIA | MIRAGE_AB_LESSONS.md, scripts/validate_experiment.py |
| Igualar prompt, modelo, orçamento, fixtures, ferramentas e revisor cego | EXISTIA/APROFUNDADO | evaluation docs e award-readiness-and-qa.md |
| Anti AI slop (texto redundante, cartões repetidos, gradientes automáticos) | EXISTIA | anti-slop-composition.md, full-page-craft-review.md |
| Verificar direitos e não copiar assets dos premiados | EXISTIA | ethics-and-licensing.md, research-provenance.md |
| Segurança de código externo/skill não confiável | PARCIAL → APROFUNDADO | specialist-skills-orchestration.md; sem instalação silenciosa |
| Esquema papéis: estrategista, diretor de arte, copy, creative developer, QA | PARCIAL → APROFUNDADO | specialist-skills-orchestration.md; papéis são responsabilidade, não fingir equipe real |
| Métricas reais LCP≤2.5s INP≤200ms CLS≤0.1 (p75) | PARCIAL → NOVO | creative-technology-playbook.md; campo ≠ Lighthouse e medidas UNKNOWN se ausentes |
| Testes Playwright + Storybook/axe/Lighthouse se disponíveis | EXISTIA/APROFUNDADO | existing harness; award-readiness-and-qa.md |
| Não copiar integralmente skills externas e não prometer Awwwards | EXISTIA | licensing, specialist orchestrator |

## 2. Making-of e técnicas efetivamente estudados

| Projeto/técnica mencionado(a) | Tipo de evidência | Mecanismo a extrair / estado |
|---|---|---|
| Trionn | Artigo dos próprios criadores em Codrops, 15/07/2026 | **NOVO** coordenação de GSAP + Three.js + Lenis + Web Audio, estado/ticker compartilhado |
| PX PUSH | Making-of em Codrops, 07/08/2026 | **NOVO** metáfora do produto governa linguagem visual e navegação |
| Podium | Making-of em Codrops, 23/06/2026 | **NOVO** estrutura narrativa contínua em vez de páginas por template |
| Ridgeline | Making-of em Codrops, 22/07/2026 | **NOVO** scroll, canvas e isolamento de rerenders desnecessários |
| Stefanos Tsitsipas / OFF+BRAND | Making-of em Codrops, 01/07/2026 | **NOVO** photogrammetry/captura → malha/UV/texturas → otimização → publicação |
| Scroll-driven Blender camera path | Tutorial Codrops | **NOVO** pré-direção de câmera e reproduções testáveis em Three + GSAP |
| CSS 3D typography | Tutorial Codrops | **NOVO** tipografia espacial sem engine 3D quando possível |
| Layered zoom GSAP | Tutorial Codrops | **NOVO** imagens/camadas com ritmo cinematográfico |
| Comparação de presença de GSAP em vencedores | Estatística editorial pontual, não benchmark geral | **CONSULTAR**, não extrapolar universalidade |
| Outros sites Awwwards não inspecionados | Galeria visual | **CONSULTAR** por produto/objetivo; não fingir estudo direto |

URL/risco de cada caso em references/awwwards-studio-production.md.

## 3. As 20 skills de design mencionadas anteriormente

| # | Nome/entrada da conversa | Estado neste OS / justificativa |
|---|---|---|
| 1 | Impeccable | CONSULTAR; audit, critique, polish, distill já incorporados como princípios originais, não copiar CLI |
| 2 | UI/UX Pro Max | CONSULTAR; seleção contextual do estilo já existe, nenhum preset automático obrigatório |
| 3 | Anthropic Frontend Design | CONSULTAR; autoria e rejeição de defaults já internalizadas |
| 4 | UI Craft | CONSULTAR para alternativas de design engineering; verificar repo/versão |
| 5 | Taste Skill | CONSULTAR; dials de boldness são hipótese, não nota de gosto |
| 6 | StyleSeed | CONSULTAR; identidade/canon já existe, verificar disponibilidade |
| 7 | Vercel Web Design Guidelines | CONSULTAR como auditoria técnica, mantém QA específico |
| 8 | Baseline UI | CONSULTAR; guardrails Tailwind não são direção artística |
| 9 | Design Tokens Skill | CONSULTAR; design-system-extraction.md já atende fundamentos |
| 10 | Color Expert | CONSULTAR se demanda de cor especializada, respeitar marca |
| 11 | Google Fonts Skill | CONSULTAR; fontes/autoria/licenças em typography-layout-craft.md |
| 12 | Design Motion Principles | CONSULTAR; motion-and-interaction-direction.md já cobre causalidade |
| 13 | UI Animation | CONSULTAR quando microinterações demandam atenção específica |
| 14 | Interaction Design | CONSULTAR para estados/gestos; proteger teclado/touch |
| 15 | Neo User Journey | CONSULTAR; journeys reais preferíveis a opinião |
| 16 | Design Brief | CONSULTAR; brief já existe via templates/PRODUCT_DISCOVERY.md |
| 17 | gstack Design Review | CONSULTAR; revisão no navegador já existe, sem prometer independência |
| 18 | Fixing Accessibility | CONSULTAR como ferramenta a11y, não certificação |
| 19 | shadcn/ui | Biblioteca/componentes (não direção de arte), usar somente quando couber |
| 20 | Web Design (pascalorg) | CONSULTAR; candidato genérico de baixa prioridade |

A lista de 20 da conversa **não** foi benchmark controlado; repositórios comunitários menos conhecidos devem ser revalidados antes da instalação. Não confundir nomes de bibliotecas, skills verificadas e nomes genéricos.

## 4. As 2 skills de sites completos

| Entrada | Estado |
|---|---|
| Website Builder / Astro | CONSULTAR se a tarefa envolve conteúdo/múltiplas rotas; nunca migrar React/Next para Astro automaticamente |
| Frontend Design / Anthropic | CONSULTAR para código e arte autoral; sem substituir o roteador de produto da skill |
| Vercel React Best Practices (extra citado) | CONSULTAR quando stack React/Next está presente; melhoria técnica ≠ premiação |

## 5. As 20 skills/áreas para landing pages do chat

| # | Nome/área | Estado e localização nova ou preexistente |
|---|---|---|
| 1 | Landing Page Design (elayadesign) | CONSULTAR; composição já em editorial-art-direction-lab.md |
| 2 | Landing Page Design (2389) | CONSULTAR; hero deve servir prova do produto |
| 3 | Product Marketing | APROFUNDADO; landing-page-evidence-and-cro.md (posicionamento e categoria) |
| 4 | Customer Research | APROFUNDADO; persona/objeções como hipótese verificável |
| 5 | Offers | NOVO; oferta verdadeira com condições explícitas |
| 6 | Copywriting | APROFUNDADO; headline+prova+visuais, sem claims genéricos |
| 7 | Copy Editing | APROFUNDADO; eliminar repetição e promessa sem fundamento |
| 8 | CRO | NOVO; mecanismos e objeções por funil, não por template |
| 9 | A/B Testing | APROFUNDADO; diferenciar testes com usuários de A/B entre skills |
| 10 | Marketing Psychology | CONSULTAR; nunca usar dark patterns, falsa escassez |
| 11 | Pricing | APROFUNDADO; termos, plano, restrições, periodicidade, CTA real |
| 12 | Signup | NOVO; seguir jornada do clique até cadastro efetivo |
| 13 | Onboarding | APROFUNDADO; ativação qualificada, não só cliques |
| 14 | Popups | CONSULTAR, não incorporar como padrão |
| 15 | Lead Magnets | CONSULTAR se oferta existir; não fabricar valor/captura |
| 16 | Competitors | EXISTIA; pesquisa com contexto e URL, sem copiar |
| 17 | Analytics | NOVO; eventos, consentimento, conversão qualificada e guardrails |
| 18 | Site Architecture | EXISTIA/APROFUNDADO; IA e jornada não são lista fixa de seções |
| 19 | SEO Audit | CONSULTAR; otimização onde descoberta orgânica importa |
| 20 | Schema | CONSULTAR; dados estruturados verdadeiros, sem markup falso |
| extra | AI SEO / Programmatic SEO / Launch / Churn Prevention / Paywalls | CONSULTAR condicionalmente; SEO de IA, escala, lançamento e retenção só quando realmente solicitados |

Referência externa principal: https://github.com/coreyhaines31/marketingskills . Alguns subdiretórios mudam de nome ou são fundidos; o caminho no chat anterior pode ter envelhecido. Consultar repositório atual antes de usar.

## 6. Todas as skills de 3D, motion e stacks citadas

| Entrada | Estado |
|---|---|
| Three.js Skill (Picaresco) | CONSULTAR comunidade; comparar API com versão do site |
| Web 3D React Three Fiber (agents-inc) | CONSULTAR; escolher R3F quando stack e lifecycle justificam |
| Three.js Skills CloudAI-X | CONSULTAR por especialidade, nunca dez módulos de uma vez |
| threejs-fundamentals | NOVO no playbook: cena, câmera, renderer e ownership |
| threejs-geometry | NOVO: geometria/instancing/LOD quando apropriado |
| threejs-materials | NOVO: identidade, material honesto, física de luz |
| threejs-lighting | NOVO: composição/luz/sombra guiadas pela direção de arte |
| threejs-textures | NOVO: UV, compressão, texturas e espaço de cor |
| threejs-animation | NOVO: atualização, timeline, rigs e lifecycle |
| threejs-loaders | NOVO: carregamento glTF e prioridades |
| threejs-shaders | NOVO: escalar de DOM/CSS para shader só se necessário |
| threejs-postprocessing | NOVO: custo visual/perceptivo/bloom, verificação |
| threejs-interaction | NOVO: raycasting, toque, teclado, reversibilidade |
| React Three Fiber (lklyne) | CONSULTAR versão atual e stack real |
| Three.js Complete Set | CONSULTAR só como índice, não roteador concorrente |
| GSAP Skills oficial | CONSULTAR como documentação de implementação, não diretriz criativa |
| gsap-core | NOVO: tween/easing com responsabilidade |
| gsap-timeline | NOVO: coreografia sem conflitos |
| gsap-scrolltrigger | NOVO: scrub/pin/scroll progress e cleanup |
| gsap-plugins | CONSULTAR Flip, SplitText etc sob licença/versão |
| gsap-utils | CONSULTAR se necessário |
| gsap-react | NOVO: useGSAP/context lifecycle quando React |
| gsap-performance | APROFUNDADO: evitar animação fora da viewport e excesso de will-change |
| gsap-frameworks | CONSULTAR compatibilidade Nuxt/Vue/Svelte |
| UI Animations (rbaumier) | CONSULTAR microinterações |
| Rive Interactive | CONSULTAR quando assets e machine states existem |
| Ultimate Animation Skill Pack | CONSULTAR, não carregar mega-packs |
| React/Next, Vue/Nuxt, Astro | EXISTIA; escolher pelo projeto, não reescrever stack |
| Lenis | NOVO: sincronizar com ticker e não sequestrar scroll |
| Three.js / R3F / WebGL / WebGPU / TSL / GLSL | APROFUNDADO em creative-technology-playbook.md |
| SVG / CSS / Canvas 2D | NOVO: alternativas preferíveis quando menos custo |
| Web Audio / Howler | NOVO: consentimento, controle, fontes de áudio reais |
| Blender / Cinema 4D / fotogrametria | NOVO: pipeline de assets autorizados |
| glTF/GLB, glTF Transform | NOVO: otimização de modelos |
| Vídeo / Lottie | NOVO: opção econômica quando experiência não depende de agência interativa |

## 7. Outros âmbitos de site contemplados no chat

| Escopo | Estado |
|---|---|
| Performance CWV e Vercel | APROFUNDADO no playbook com LCP/INP/CLS e limites de medição |
| Responsividade dedicada | EXISTIA; reforçado touch, camera, planos de cena |
| Playwright e snapshots | EXISTIA; testes/screenshot reais vs autodeclaração |
| Regressão visual | EXISTIA; estado temporal e diferencial contextual |
| Microsoft Frontend Review | CONSULTAR se ferramenta disponível |
| SEO Plan / AI SEO / SEO Audit / schema | CONSULTAR só quando intenção orgânica/importância |
| Privacy/auth/payments/security | EXISTIA como contratos protegidos; exige especialistas do stack para teste real |
| Design tokens e shadcn/ui | EXISTIA como padrões; não forçar toolkit |
| Storybook/axe-core | EXISTIA fonte, testes opcionais, não declarar 100% WCAG |
| Product analytics/HEART | EXISTIA/APROFUNDADO, sem métricas inventadas |
| Ethics/licensing | EXISTIA, reforçado inspecionar skills externas |
| Multisurface routing / brain | EXISTIA; ganhou roteamento especializado e testes negativos |
| Creative signatures e anti-AI-slop | EXISTIA; reforçado por mecanismos observáveis |
| Comparar com/sem skill, rastrear hash leitura real | EXISTIA; A/B não confirmado por isso |
| Orçamento / custo de execução | EXISTIA; seleção 0–3 especialistas e protótipo de risco novo |
| Escolher framework | NOVO: escala menor, evitar migração desnecessária |
| Fonte/citação verificável | EXISTIA/APROFUNDADO: mecanismos por origem e status |
| Design autônomo e crítica cega | EXISTIA; separação de owner e avaliador sem alegar equipe real |

## 8. Decisão de implementação — o que entrou de fato na 11.2

**Criado e conectado à skill:**
- references/awwwards-studio-production.md
- references/landing-page-evidence-and-cro.md
- references/creative-technology-playbook.md
- references/specialist-skills-orchestration.md
- references/award-readiness-and-qa.md
- templates/CREATIVE_TECH_PROOF.md
- templates/LANDING_CONVERSION_PROOF.md
- brain/route_rules.json e brain/route.py ampliados; testes em scripts/test_brain.py

**Mantido sem mudanças funcionais:** referências originais de brand fidelity, lettering, design system, anti-slop, QA, estudos comparativos, permission guard, test harness, pacote instalado e fluxos de produto.

**Não incorporado automaticamente:** prompt/code externo sob licença desconhecida, 60+ skills de uma vez, WebGL forçado, animações com pouca utilidade, SEO/popups por padrão, métricas de conversão inventadas, ranking supostamente objetivo de 'melhor skill', automação com auto-instalação.

## 9. Validação restante e limites

Os testes novos validam rotas *previsíveis* e exclusões, não beleza. Validar Python + testes browser existentes em CI; separar falha existente de falha introduzida. Realizar A/B com projetos completos e revisores independentes antes de afirmar que a nova versão vence sem skill. Conferir cada candidato externo, licença e compatibilidade no runtime. Usar Awwwards como inspiração e critério histórico apenas depois de verificar diretrizes atuais. Nenhuma mudança desta rodada concede autoridade para modificar contratos protegidos.
