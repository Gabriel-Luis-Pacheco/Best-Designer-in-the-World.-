# Creative evidence journey — avalie cenas reais, não somente screenshot longa

A captura integral pode enganar quando há canvas/WebGL, pinning, lazy-load, transições controladas por scroll ou elementos virtualizados. No teste RESONANCE, uma screenshot do projeto com skill mostrava uma área escura enganosa; o vídeo e frames de cena documentaram conteúdo. Nunca diagnosticar vazio só porque a captura longa parece vazia — nem tratar o arquivo como representação fiel sem conferir os estados.

## Coleta comparável
- Documente commit, browser, dimensões da viewport, device scale, fonts, URL, motion, condição do WebGL, posição do scroll, evento e estado da interação.
- Capture abertura, primeira transformação, meio representativo, clímax e conclusão; também mobile de 390 px e reduced-motion.
- Role e ACIONE estados explicitamente; aguarde fontes e estabilidade antes da captura. Em seções maiores que a tela, o capturador deve alinhar o **início** da cena por padrão; marque um deslocamento de scroll intencional no roteiro para mostrar um beat posterior. Um enquadramento que começa no meio de um título pode ser falha de captura, não do layout.
- Não use fullPage:true como única evidência de scrollytelling. Capture o viewport após scroll/trigger e produza uma contact sheet ordenada.
- Em cenas de timeline, use vídeo com roteiro de ações replicável, não imagens de momentos diferentes como se fossem iguais.
- Frames ausentes são falhas de coleta; hashes idênticos entre cenas diferentes exigem revisão, mas não provam defeito artístico.
- Screenshot não prova FPS, performance, acessibilidade, marketing ou qualidade estética.

## Ferramenta
O comando node scripts/capture_creative_journey.mjs --config path/to/storyboard.json (na raiz do repositório) lê um roteiro JSON local com URL localhost, seletores, ações click e tempos. Gera frames PNG, manifest com hashes, viewport e metadados e painel HTML local. Não executa comandos do JSON, não inicia servidor e não navega para endereço externo.

Exemplo de configuração em tests/browser/creative-journey.sample.json. Substitua seletores pelos da experiência. Um frame sem selector não passa silenciosamente. NUNCA enviar capturas privadas para repositório público sem autorização.

## Qualificações
- CAPTURED_FOR_HUMAN_REVIEW significa somente evidência criada.
- MISSING_SCENE ou FAILED_CAPTURE exige retestar; não aprovar.
- Repetição de imagem = REVIEW_DUPLICATE_FRAMES; verificar pin/canvas/movimento antes de acusar falha.
- Em A/B com skill e sem skill, aplicar mesmo roteiro de viewport/gestos, ambiente e recursos, e avaliar independentemente.

## V11.1 state-integrity rule
A captured frame with an action must declare an explicit semantic `intent` and a `state` observation (text/value/aria-selected); matching screenshots without matching gesture meaning are not a valid A/B. The capturer fails closed on browser runtime errors, denied external resources and observed state mismatch. Request outside-local resources only with explicit `allow_external_requests: true` for a controlled, trusted project; record this condition for both variants.
