# Auditoria crítica: Design OS Prime orientada a resultado VISUAL — 11/11/2026

**Pergunta real:** a skill ajuda de modo confiável a criar landing pages, sites e sistemas com uma direção de arte memorável, visual de alto nível e implementação de verdade?

**Veredito:** o repertório conceitual é amplo, mas ainda não há prova de superioridade estética. A v14 cobria muito bem briefing, produto, CRO/SEO, anti-AI-slop e evidência, mas o núcleo tinha 38.742 caracteres e podia priorizar declarações de qualidade e tarefas de governança antes de colocar a composição em um navegador. A maior lacuna operacional era a ausência de uma comparação simples de **duas versões de código renderizado**, por cenas equivalentes e viewports. Um documento de roteiro e um manifest não substituem esse passo.

## Defeitos e reparos desta rodada

| Gravidade | Diagnóstico | Risco artístico | Mudança |
|---|---|---|---|
| ALTA | Muitos comandos de planejamento e crítica; pouca exigência prática de prova visual antes de expandir o site | Texto e checklist com aparência de bom trabalho sem um site diferenciado | Priorização VISUAL PRODUCTION FIRST no núcleo e guia curto de execução code-first |
| ALTA | A skill falava em duas direções/miniaturas, mas não fornecia um workbench próprio para confrontar 2–3 páginas executáveis em mesmas condições | Escolher tese por adjetivos e reproduzir sempre o mesmo layout | script Playwright visual_direction_studio.mjs: opener/proof/decision por candidato e viewport, galeria e SHA de capturas |
| ALTA | Risco de hero excelente seguido por seções triviais | Página final genérica apesar de abertura forte | Vertical slice com começo + prova do meio + fim antes de finalizar ou polir a primeira dobra |
| ALTA | Escolha de imagens/ícones ainda era descrita como princípio, não ordem produtiva | Placeholders, mascotes inventados e fake screenshots persistirem | Asset ladder: canon real → product demo → imagens autorizadas → mídia original gerada se houver ferramenta → alternativa tipográfica/CSS/SVG |
| MÉDIA | Core acumulava SEO, governança, papel de CEO e verificação em excesso, mesmo para um pedido visual | Contexto da IA ocupado por instruções que não melhoram pixels | Condensação de invariantes, SEO e ferramentas históricas em apontadores para guias condicionais (em vez de remover capacidades) |
| MÉDIA | Provas atuais são muito centradas em HTML e hashes, não qualidade percebida | Falso positivo de visual excelente | Workbench só retorna evidências e warnings, nunca nota automática de beleza |
| MÉDIA | Revisão estética sem comparação de mobile e de cenas de prova | Falha de continuidade da identidade e legibilidade | Capturas pareadas de desktop/mobile, hero/miolo/final e pergunta específica por cena |
| BAIXA | Variações visuais sem limites de direitos/assets | Acelerar um caminho criativo não licenciado | URLs locais, requests externos bloqueados por padrão e checklist de fonte/direitos |

## Fluxo preferido para landing page visualmente ambiciosa

1. Descobrir marca, produto, provas verdadeiras e assets originais.
2. Definir um motivo visual que só faz sentido para aquele produto; não por paleta da moda.
3. Escolher o melhor meio para a prova (produto real, fotografia, desenho, vídeo, tipografia, 3D).
4. Se o caminho estiver aberto, criar duas direções **em código** rapidamente, com abertura/prova/fechamento.
5. Renderizar em navegador local, capturar seções equivalentes em desktop e mobile.
6. Escolher com base em evidência visual real, objetivo e trade-offs; aprimorar uma única tese consistente.
7. Corrigir a seção visualmente mais fraca. Repetir render apenas onde agrega valor.
8. Verificar interação, teclado, dados, tempo de carregamento, direitos e compromisso do CTA antes de entregar.

**Sem rigidez estética:** nenhum framework é obrigatório, não se proíbem gradientes/cards/serifas/Glassmorphism/3D por decreto, e um layout minimalista pode ser excelente. A questão é se a composição, a imagem e o movimento são autênticos e fortes para o produto.

## Como inspecionar duas direções reais

No repositório, com o Playwright instalado e servidor local acessível, execute:

    npm run visual:directions

O script usa tests/browser/visual-direction.sample.json, comparando duas páginas de exemplo em 1440×900 e 390×844 nas cenas abertura, demonstração e preço/decisão. Gera index.html, imagens e manifest em test-results/visual-direction/. O arquivo é uma galeria para decisão humana, não um juiz automático. A ferramenta portátil está em skills/studio-grade-web-transformation/scripts/visual_direction_studio.mjs.

O build de uma página **não acontece automaticamente pelo script**: o agente executando a skill precisa construir as variantes de verdade e apontar seus URLs reais. Fluxos com scroll animado ou WebGL precisam adicionalmente de capturas temporais em movimento normal e reduzido (capture_creative_journey.mjs).

## Fontes consultadas — princípios, não layouts para clonar

- [NNGroup: Five Principles of Visual Design](https://www.nngroup.com/articles/principles-visual-design/): escala, hierarquia, equilíbrio, contraste e Gestalt, com revisão indicada em setembro/2026.
- [Webby Awards 2026/27 Judging Criteria](https://www.webbyawards.com/judging-criteria/): conteúdo, estrutura, navegação, design visual, funcionalidade, interatividade, inovação e experiência integrada.
- [Baymard UX Benchmark](https://baymard.com/ux-benchmark): pesquisa de produto/e-commerce sobre navegação e tarefas, não certificação de um estilo específico.
- [Impeccable Changelog](https://impeccable.style/changelog/): benchmarks, núcleo com testes de ablação, protótipos em código e live-mode para algumas plataformas; não reivindicamos equivalência funcional sem implementação e experimentos.

## O que ainda impediria o rótulo de “perfeita”

- **Ainda não existe benchmark controlado demonstrando vantagem estética** frente a Impeccable, Taste Skill, Anthropic Frontend Design ou baseline sem skill.
- Falta um sistema de avaliação de ablação real: testar quais regras do prompt melhoram ou pioram resultados **com modelos e tarefas verdadeiras**, não em exemplos sintéticos; remover regras sem efeito e controlar custo/contexto.
- O workbench **não gera** código/arte por conta própria nem possui editor visual interativo como o live-mode da Impeccable; precisa do agente e browser configurado.
- Os exemplos atuais são sintéticos e suas imagens de teste não equivalem a feedback de usuários; precisamos confrontar saídas reais de LPs de diferentes mercados e produtos, inclusive mobile.
- Assets reais/fotografia, direção de fotografia, tipografia licenciada, motion e identidade de mascotes exigem ferramentas e acervo com direitos, que não se instalam só por instruções.
- Revisão independente de craft e usabilidade precisa de avaliadores reais e/ou pesquisadores; CI, screenshot e agente sozinho não podem certificar um design excelente.

**Próxima melhoria prioritária:** benchmark cego replicado (mesmo briefing/assets/modelo/orçamento/ambiente) contra baseline e especialistas; usar evidência para reduzir regras redundantes em vez de crescer mais uma camada de prompts. Testes CI da alteração atual verificam scripts e snapshots de fixtures, não valor visual subjetivo.
