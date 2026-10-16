# Implementação de qualidade sem engenharia ornamental

Primeiro garantir: conteúdo real, arquitetura, hierarquia, responsividade e acessibilidade. Depois: componentes, estados, motion e otimizações.

Seguir stack existente. Em React/Next, consultar Vercel React Best Practices e Composition Patterns conforme necessidade: evitar waterfalls e grandes bundles, componentes com APIs claras, estados explícitos, otimizações baseadas em profiling.

Estados obrigatórios quando aplicáveis: foco, hover, sucesso, erro, loading, vazio, disabled. Testar navegação teclado, formulários, links, zoom, texto longo, layout em mobile e prefers-reduced-motion.

Motion deve comunicar continuidade ou status; não atrasar ação. Imagens otimizadas, fontes licenciadas, alternativas textuais e fallback sem mídia. Não instalar biblioteca pesada para executar efeito decorativo.

Não alterar autenticação, preços e APIs ao redesenhar marketing sem um requisito específico. Build verde não prova que a landing é boa.