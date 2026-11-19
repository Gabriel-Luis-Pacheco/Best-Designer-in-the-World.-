# Execução de qualidade e benchmark real — 19/11/2026

**Status em 19/11:** protocolo criado; comparações empíricas controladas **NÃO EXECUTADAS**. Nenhum ganho estético ou de conversão é atribuído à Design OS com base nesta documentação.

## 1. Primeiro: engenharia e artefatos reais

```bash
python -m unittest discover -s scripts -p "test_*.py" -v
python skills/studio-grade-web-transformation/scripts/validate.py
npm ci
npm run test:browser:scope
npx playwright install chromium
npm run test:browser:fixtures
python scripts/build_core_package.py --output dist/design-os-prime-core.zip
```

O Playwright só pode descobrir testes originais em `tests/browser/` e `examples/playwright-visual.spec.ts`; os espelhos `vendor/` não são parte do teste do Design OS. CI verde comprova somente essas verificações, **não** qualidade estética.

## 2. Experimento recomendado

Selecione dez briefings e snapshots de projetos utilizáveis com direitos claros, sem dados privados. Não modifique o baseline durante a rodada:

1. Landing B2C de prática de idiomas com demo real, público frio
2. Landing B2B para escolas com formulário de lead funcional e prova de oferta
3. Página comercial de serviço especializado com casos reais e objeções
4. Dashboard de operações densas com dados verificáveis e estados vazios
5. Calculadora fiscal de tela compacta, com regras e campos existentes preservados
6. Onboarding mobile de produto com primeira tarefa concreta
7. Portfólio profissional com cases/projetos comprováveis
8. E-commerce de produto físico com variações, frete e confiança
9. Experiência artística com motion significativo e saída acessível
10. Artigo editorial longo com hierarquia de informação, tabelas e leitura mobile

Para cada briefing, executar **três condições** em workspaces independentes: mesmo modelo sem skill de design; mesmo modelo com Design OS; mesmo modelo com skill especialista adequado ao briefing. Repetir pelo menos duas vezes por condição para explorar variabilidade. Com 10 briefs × 3 condições × 2 repetições serão 60 artefatos; documentar os que falharem, sem selecionar só os melhores.

Controlar modelo/revisão, effort, assets, ferramentas/browser, orçamento de tempo e tokens, sistema de prompts, stack, preço e fluxos existentes. Registrar SHA do prompt, da skill realmente **lida** e do projeto-base, telemetria de custo/duração, erros, diff, capturas, caminhos e vídeo/motion quando pertinente. Não usar saída de um concorrente como entrada da outra condição.

## 3. Revisão independente e julgamento

- Capturas equivalentes 1440px / ~390px, abertura, prova, meio e encerramento; testar CTA até primeiro valor e interações críticas.
- Pelo menos dois revisores humanos cegos à condição avaliam as dimensões apropriadas de `docs/QUALITY_RUBRIC.md` (0–3), com evidências de cada nota e P0/P1 separadamente.
- Sempre registrar vitórias, derrotas, empates, `MIXED_TRADEOFF`, revisores discordantes e eixos sem dados. Estimar resultados por categoria, nunca declarar “melhor do mundo” por média de uma amostra.
- Para conversão real, validar instrumentação e dados de tráfego reais; opiniões de revisores e screenshots não bastam.

Ferramentas existentes:
```bash
# Apenas agente CLI autorizado que lê o prompt via stdin:
python scripts/run_evals.py --case 1 --variant both --command "SEU_CLI" --out output/eval-runs

# Apenas avaliações cegas humanas com evidência real e controles equivalentes:
python scripts/compare_skill_league.py reviews.json --evidence-root evidencias/
```

O runner embute até algumas referências e não comprova que o modelo efetivamente aplicou todas elas. Confirmar a leitura com trace. O comparador não verifica se revisores eram de fato cegos nem se os pixels são bons: auditar separadamente. A condição **especialista** deve ser rodada e identificada à parte, porque o runner básico de A/B não a cria sozinho.

## 4. Após obter evidência

Para cada regra/skill extra, fazer ablação (ativar/desativar uma alteração por vez) em casos reais, registrar custo e defeitos. Se uma regra não melhora o resultado ou prejudica casos comuns, simplificar/remover do núcleo; manter conhecimento profundo como referência sob demanda. Priorizar qualidade observada e fiabilidade antes de novas importações. Revisar licenças/atualizações upstream separadamente.

**Nunca afirmar:** “CI verde = premium”, “50 skills foram executadas”, “usuários acharam incrível” sem prova, “ganho de conversão” sem dados, ou “benchmark vencido” sem condições controladas.
