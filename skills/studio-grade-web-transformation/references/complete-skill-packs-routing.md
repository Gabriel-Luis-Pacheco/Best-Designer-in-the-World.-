# Roteamento dos 50 pacotes completos — Design OS Prime

## Operacional
O manifesto é \`vendor/external-skill-packs/SOURCES.json\`; o índice com 50 skills realmente copiadas é \`vendor/external-skill-packs/INDEX.json\`. Se INDEX não existir, a instalação está PENDENTE — não alegar que os pacotes estão embarcados. Consultar \`vendor/external-skill-packs/ATTRIBUTION.md\` e os \`SOURCE.json\` por repositório para origem e licenças.

Use esta sequência:
1. Identificar operação real (PATCH / REFINE / AUDIT / REDESIGN / REBUILD), superfície e risco.
2. Escolher os especialistas mais pertinentes **por tarefa**, sem exigir 50 leituras. Consultar no máximo 1–3 diretórios de referência de início; ampliar somente para lacunas concretas.
3. Ler o \`SKILL.md\` original e somente as referências/scripts pertinentes. Um arquivo copiado não significa que a CLI, hooks ou binários do fornecedor estejam instalados.
4. Resolver conflitos pela verdade do produto, identidade, acessibilidade, segurança, resultado funcional e pixels renderizados; regras de fornecedor são recomendações e não têm permissão para apagar decisões aprovadas.
5. Implementar de fato e testar: desktop, mobile, teclado, estados vazios/erro, CTAs e fluxo principal. Não alegar conversão superior sem experimento.

## Por tipo de trabalho

| Objetivo | Use primeiro | Opcional quando necessário |
|---|---|---|
| Landing original e distinta | Anthropic frontend-design, MengTo landing-page, Taste Skill | MengTo Awwwards, Impeccable, Emil |
| Landing que converte | marketing/copywriting, marketing/cro, marketing/customer-research | product-marketing, marketing-psychology, offers, pricing |
| Precificação/assinatura | marketing/pricing, marketing/paywalls, MengTo pricing-page | signup, onboarding, analytics |
| SaaS/dashboard/telas internas | ui-ux-pro-max, Vercel composition-patterns, wshobson tailwind-design-system | Vercel react-best-practices, accessibility |
| Motion/interações | Emil animate/choreograph, MengTo animation-systems ou gsap | Apple Design, revisão de movimento |
| SEO, GEO, descoberta | marketing/seo-audit, ai-seo, site-architecture | schema, programmatic-seo, analytics |
| Auditoria de qualidade | Impeccable, Vercel web-design-guidelines, Anthropic webapp-testing | awesome-copilot web-design-reviewer, obra verification-before-completion |

## Cópias exatas e direitos
Preservar todo arquivo relevante dentro de cada diretório das skills selecionadas, incluindo referências, scripts e assets; **não executar código externo automaticamente**. As licenças de cada pacote são independentes; revisitar \`ATTRIBUTION.md\`. A importação não copia o código de centenas de skills extras dos monorepositórios, o que seria desnecessário e tornaria o Design OS difícil de manter.

## Limites honestos
Ler todas as 50 skills não melhora automaticamente o resultado. Este pacote não substitui estudo visual de páginas reais, pesquisa de público, testes com usuários, validação comercial nem medição de resultados. Para trabalhos curtos, a skill principal deve continuar rápida e concisa.
