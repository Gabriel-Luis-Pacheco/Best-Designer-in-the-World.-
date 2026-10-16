# Caso trabalhado — ConversaBoa (projeto fictício)

Artefatos: `../fixtures/landing-generic.html` (antes), `conversaboa-concept.html` (conceito construído) e `../fixtures/fictional-product-brief.md` (verdade permitida). **Não são dados ou telas reais do BataTalk.**

## Problema
A fixture inicial vende "reinvenção" em termos genéricos, repete blocos de cards, pouco demonstra a prática e não tem sistema de ritmo expressivo. Os planos existem, mas a maior parte do espaço de tela não prova a promessa.

## Direções concorrentes
A. **Conversa como palco editorial:** uma troca de mensagens protagoniza a primeira dobra, conduzindo a demonstração textual clicável, três passos funcionais e pricing verdadeiro. Linguagem de poster acolhedor com creme, ameixa, verde-claro e coral. Principal risco: parecer uma conversa de chat genérica; corrigir com gramática de material e tipografia consistentes.
B. **Mapa de progresso:** história por capítulos (situação/tentativa/feedback/repetição) e marcos de aprendizado. Principal risco: sugerir tracking e gamificação não previstos no brief. Rejeitada por falta de evidência de progressão armazenada.

Escolha: A. Demonstra o único mecanismo confirmado pelo brief sem inventar reconhecimento de voz, professor, certificados nem métricas. O stage inicial é **ilustração editorial, não screenshot**, identificado de forma visível/assistiva.

## Decisões
- Hero enorme mas com CTA claro, sem adjetivo vazio.
- Cena com silhueta de balão e componente de conversa, não mockup falsamente realista.
- Uma seção escura de demonstração para mudar ritmo sem quebrar paleta.
- Feedback clicável como protótipo local (sem back-end ou claim de IA real).
- Passos em lista editorial para evitar três cards repetidos.
- Plans em comparação simples, valores e recorrência preservados, sem checkout fictício.
- Mobile com mudança de layout deliberada, altura do palco reduzida, comparação empilhada com separação evidente.
- Motion mínimo, scroll desativado em reduced motion.

## Evidências existentes e lacunas
O arquivo é executável, e `tests/browser/design-example.spec.ts` verifica renderização responsiva, CTA, fatos comerciais e a interação do feedback quando executado. Não há teste de preferência humana, conversion lift, revisão cega ou prova de que esta opção é artisticamente superior em todos os contextos. Testes funcionais da própria fixture não avaliam estética.

Para a skill, esse exemplo mostra a transformação de princípios em decisões e código; o avaliador deve ainda usar a rubrica e criticar o resultado.
