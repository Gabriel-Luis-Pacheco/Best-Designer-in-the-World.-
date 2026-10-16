# Harness de teste visual e funcional

Combinar captura global de página e snapshots de componentes; documentar ambiente, browser, viewport, escala, fontes e estado dos dados. Comparações de screenshot ficam sensíveis a versão de navegador, OS e renderização.

Playwright: usar `expect(page).toHaveScreenshot()` nos testes executáveis, com baseline aprovada. Preferir alvos determinísticos, aguardar fontes, desabilitar animação durante teste e mascarar somente conteúdo verdadeiramente dinâmico — nunca mascarar bugs.

Cobertura sugerida: 390 e 1440, com extensões para 320, 768 e 1280 conforme produto; hero, seção média, pricing, footer; estados de error/loading; menu mobile; CTA; teclado e redução de movimento.

Visual diff não mede originalidade, coerência narrativa ou estética. Depois das capturas, realizar revisão humana com rubrica. A11y automação detecta parte das falhas; testar teclado e leitores de tela manualmente.