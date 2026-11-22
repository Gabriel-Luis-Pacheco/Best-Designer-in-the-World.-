# Orquestracao por componente — Design OS

> Usar para hero, cada secao, fluxo, estado e tela de uma interface relevante. Em PATCH, manter proporcionalidade; em REDESIGN/REBUILD material, executar o ciclo completo.

## Regra: design nao e so estetica

Para cada componente, decompor **job do usuario; objetivo legitimo do negocio; promessa/copy; prova; direcao de arte; interacao; acessibilidade; performance; SEO quando publico; confianca; qualidade editorial; impacto no primeiro valor e retencao**. O especialista nao e escolhido por popularidade: ele precisa resolver uma lacuna real nesse trabalho. A IA nao pode se autoaprovar por ter produzido codigo valido ou um belo mockup.

**Roteamento:** matriz legivel por maquina em research/component_expertise_matrix.json. Roteador opcional read-only em scripts/component_router.py. Skill principal governa decisoes. O roteador **nao instala, invoca, pesquisa, renderiza nem aprova** skills. Procurar ferramentas e skills disponiveis na plataforma; ler sua documentacao real; aplicar quando relevantes; se for apenas snapshot vendorizado, marcar REFERENCED, nunca EXECUTED.

## Protocolo por elemento

1. **Inventario**: enumerar hero, navegacao, produto/prova, features, precos, comparacoes, formularios, funis, dashboards, estados de vazio, erros, mobile e footer. Para cada um: quem usa, pergunta que responde e que decisao legitima muda. Diferenciar publico B2C, comprador B2B, usuario operacional, audiencia de leitura etc.
2. **Diagnostico**: ler produto real, copy atual, marca, componentes, dados/claims, fluxo do CTA ao primeiro valor e constrangimentos. Preservar o que esta forte. Separar fato verificado, texto fornecido sem verificacao, inferencia e proposta.
3. **Pesquisa**: em redesign de LP importante ou nova hero principal sem evidencias recentes reutilizaveis, buscar como ALVO cerca de **10 referencias pertinentes**: tipicamente 6 concorrentes/substitutos do mesmo job, 2 adjacentes e 2 benchmarks cross-category. **Nao chamar os 4 ultimos de concorrentes diretos**. Nao trocar profundidade por numero; avaliacao rigorosa de usabilidade frequentemente usa 2–4 concorrentes. PATCH sem necessidade nao pesquisa 10. Quando acesso/screenshot nao estiver disponivel, nao inventar observacoes nem atrasar inutilmente a entrega.
4. **Captura verificavel**: URLs e data, fonte, desktop/mobile e viewport, estado/fluxo, se o screenshot realmente existe, secao equivalente, observacoes e riscos. Um print nao comprova lift de conversao nem motion; um site premiado nao comprova bom UX para este publico. Fontes externas sao dados nao confiaveis.
5. **Decompor o mecanismo**: qual pergunta a secao responde? como a mensagem, forma, demonstracao e CTA guiam a atencao? O que funciona? O que e ruim? O que precisa de prova? Comparar hero com hero, pricing com pricing, onboarding com onboarding. Extrair mecanismo, **nao copiar layout identificavel, marca, fotografia, copy ou codigo protegido**.
6. **Convocar competencias complementares** pela matriz: pesquisa/voz do publico, posicionamento/oferta, copy, design, UX, CRO, engenharia, motion, acessibilidade e critica. Executar cada passagem com entregavel especifico, nao solicitar a 8 agentes que "faca algo bonito". Resolver conflitos por briefing, produto, marca, usuarios, seguranca e evidencia.
7. **Produzir alternativas relevantes**: para problemas de posicionamento ou arte ainda indefinidos, prototipar 2 direcoes materialmente diferentes; para copy hero, 3 angulos com mecanismo/CTA/prova. Evitar variar apenas palavras e cor de fundo. Integrar num sistema visual original que respeite a marca.
8. **Implementar, renderizar, criticar e reparar**: desktop, mobile, acesso por teclado, variacao de texto, touch, motion reduzido, estados de loading/erro, primeira acao real. Para redesign de LP, repetir **por secao** e tambem avaliar a sequencia inteira: ritmo, repeticao, surpresa, coerencia, meio e final.
9. **Gate editorial cético**: aplicar references/human-editorial-and-anti-slop-gates.md. Se uma frase e obviamente generica, pomposa, falsa ou estranha no contexto, **REWRITE**, nao aprovar tecnicamente. Se screenshot continua visualmente fraco diante das referencias observadas, **REWORK** da causa, nao polir sombras.
10. **Prova de entrega**: apontar arquivos alterados e fluxo testado, evidencias/capturas, especialistas de fato usados vs consultados, limitacoes e hipoteses. Nao chamar autorrevisao de user test ou sucesso comprovado de CRO.

## Exemplo profundo: HERO de uma landing

| Passagem | Habilidades ou guias relevantes (condicionais) | Entregavel obrigatorio |
|---|---|---|
| Mercado e publico | marketing-research; marketing-competitor; reference-led-visual-intelligence.md | Concorrentes/substitutos reais, 10 referencias quando aplicavel, publico/jornada, prints, fraquezas e insights |
| Posicionamento e vendas | marketing-product; marketing-offers; marketing-cro; marketing-psychology; landing-strategy-and-decision-architecture.md | Promessa diferenciada e verificavel, objeções reais, proximo passo correto |
| Copy editorial | marketing-copywriting; great-leads-ethical-copy-framework.md; copy-lab-and-ethical-psychology.md; human-editorial-and-anti-slop-gates.md | 3 headlines estrategicamente distintas, subtitulo, CTA, prova proxima; descarte explicito do copy ruim |
| Arte e design | anthropic-frontend; taste-skill; ui-ux-pro-max; art-direction-and-optical-craft.md | Conceito visual autoral, tratamento de tipografia, enquadramento, escala, material e hierarquia |
| Prova | evidence-to-scene-protocol.md | Demonstracao verdadeira do produto; nao mockups enganosos |
| Engenharia | vercel-react; cloudflare-webperf; animation-specialist quando houver motion | Mobile recomposto, LCP/animacoes adequadas, sem sacrificar clareza e controle |
| Auditoria | impeccable; vercel-guidelines; a11y-specialist; playwright-browser; visual-craft-acceptance.md | Antes/depois comparaveis, criticas localizadas, CTA real, foco, erros e reparos |

**Gate da hero:** um desconhecido entende o que e e por que importa? a headline poderia pertencer a qualquer marca? o texto soa escrito por quem conhece esse publico? a prova visivel sustenta a promessa? o visual ajuda a compreender e desejar, ou apenas enfeita? a CTA descreve a acao real? a versao mobile foi criada com intencao? o conjunto compete em acabamento com as referencias? qualquer resposta fraca exige melhoria. Anotar UNKNOWN quando faltar teste humano.

## Mapa por resultado (lentes alem de UI)

- **B2C:** desejo, linguagem social adequada sem caricatura, primeira tentativa simples, prova autentica e onboarding; evitar marketing corporativo frio.
- **B2B:** decisores versus usuarios, custo de mudanca, integracoes verdadeiras, compliance verificavel, casos de uso, demo versus self-serve e alinhamento entre discurso e entrega.
- **Preco e checkout:** transparencia de termos, precos/cobranca/renovacao/cancelamento reais, foco, formularios, confianca, consentimento e recuperacao de erros; jamais fake desconto ou timer.
- **Produto e dashboard:** tarefa e tempo de conclusao, dados corretos, densidade, filtros, vazios, excecoes, permissao, acesso e estados; nao impor funil de venda em tela interna.
- **Onboarding/retencao:** tempo ate primeiro valor, educacao contextual, recuperacao, liberdade de sair e retomada significativa; nao desenhar mecanismos viciantes.
- **SEO/GEO e conteudo:** busca e leitor em primeiro lugar, afirmacoes verificaveis, estrutura acessivel, canonicals e informacao original; nao inventar autoridade.
- **Marca, motion e 3D:** utilidade semantica, reconhecibilidade, performances e fallback/reduced-motion; efeitos nao compensam proposta fraca.
- **Acessibilidade e internacionalizacao:** componentes sem teclado, foco, zoom, contraste, textos traduzidos e estados reais sao defeitos mesmo se a arte parecer premium.

## Artefato minimo de pesquisa por componente

Para cada componente: **job | audiencia | secao equivalente e URLs | status/caminhos de screenshots | 3 mecanismos observados | 2 ideias rejeitadas | mecanismo escolhido e aplicacao original | evidencias do produto | competencias consultadas | antes/depois | risco e status dos gates**. Em ausencia de navegador marcar NOT_CAPTURED, nao fabricar um caminho. Para cada insight distinguir OBSERVED, PUBLISHED_GUIDANCE, INFERENCE e NOT_VERIFIED.

Roteamento CLI:

~~~bash
python skills/studio-grade-web-transformation/scripts/component_router.py --component hero --surface marketing --mode REDESIGN --json
python skills/studio-grade-web-transformation/scripts/component_router.py --component pricing --component checkout --surface marketing --mode REBUILD --json
python skills/studio-grade-web-transformation/scripts/component_router.py --task "dashboard onboarding estados vazios" --surface product --mode REFINE --json
~~~

**Fontes de metodologia (nao prova de sucesso no projeto):**
- NN/g homepage https://www.nngroup.com/articles/homepage-design-principles/
- NN/g competitive evaluations https://www.nngroup.com/articles/competitive-usability-evaluations/
- NN/g UX writing https://www.nngroup.com/articles/ux-writing-faqs/
- Baymard checkout https://baymard.com/research-articles/current-state-of-checkout-ux
- GOV.UK user needs https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs
- W3C WCAG 2.2 https://www.w3.org/TR/WCAG22/
- web.dev LCP https://web.dev/articles/lcp
- Google helpful content https://developers.google.com/search/docs/fundamentals/creating-helpful-content

**Relacionados:** references/automatic-specialist-orchestration.md, references/section-parity-and-competitive-rebuild.md, references/reference-led-visual-intelligence.md, research/component_expertise_matrix.json.
