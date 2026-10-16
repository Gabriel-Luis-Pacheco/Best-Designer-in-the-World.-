# Harness de avaliação da skill

O pacote de testes em `evals/evals.json` é uma **especificação de casos**, não um relatório de sucesso. Nenhuma execução de modelo foi feita automaticamente.

## Experimento comparativo
1. Registrar modelo e versão, temperatura/esforço, data, ferramentas, stack, hardware e arquivos de entrada.
2. Executar cada caso pelo menos duas vezes **sem a skill** e duas vezes **com a skill** quando custo permitir; a qualidade possui variância.
3. Salvar artefatos e screenshots do projeto inteiro (não só hero). Usar o mesmo ambiente para duas versões.
4. Revisão cega com avaliador humano usando `docs/QUALITY_RUBRIC.md`, sem revelar a condição.
5. Para cada expectativa, marcar PASS/FAIL/UNKNOWN com fonte de evidência. `UNKNOWN` não é PASS.
6. Comparar sucesso em fluxos, falhas P0/P1, preferência humana, esforço de correção e custo. Não colapsar tudo em um “98/100” arbitrário.
7. Repetir depois de mudar a skill. Publicar relatório, inclusive regressões.

## Exemplo de review JSON
```json
{"case_id":1,"variant":"with_skill","reviewer":"designer-01","scores":{"clareza":3,"direcao_arte":4,"identidade":2,"mobile":3},"blockers":[{"severity":"P1","evidence":"Mascote divergente"}],"assertions":[{"text":"Respeita marca original","result":"FAIL"}]}
```

Os scores 0–4 são julgamentos humanos e não pontuação oficial. Se não houver avaliador humano e navegador real, reportar apenas validação estrutural.

## Regressão visual
Receitas em `examples/playwright-visual.spec.ts`. Playwright screenshot diffs detectam alterações inesperadas, não julgam qualidade artística. Fixar navegadores, fontes, dados e screenshots baseline. Não atualizar baseline automaticamente sem review.

## Anti-Goodhart
Uma skill treinada para sempre declarar que “comparou 5 concorrentes” pode cumprir o texto sem realmente ter navegado em nenhum. Exigir URLs, data, captura ou arquivos de prova. Métrica passa se houver evidência, não uma autodeclaração bonita.
