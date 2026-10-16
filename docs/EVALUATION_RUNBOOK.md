# Harness de avaliação — V8.1

## Estado comprovável
Existem 20 casos de teste, vários com HTML/SVG/brief sintéticos; validadores Python; browser smoke Chromium; rubrica 0–3, resumo de avaliações humanas e adaptador CLI opcional. **Não** há resultados A/B com modelos nem validação estética independente publicada. PASS estrutural NÃO é design aprovado.

## Execução
```bash
python scripts/check_contracts.py
python scripts/check_evals.py
python skills/studio-grade-web-transformation/scripts/validate.py
python -m unittest discover -s scripts -p "test_*.py" -v
npm install && npx playwright install chromium
npm run test:browser:fixtures
```
CI executa esses testes em push/PR, com evidências anexadas ao workflow.

Para gerar SAÍDAS (não notas) de um CLI de agente confiável, capaz de ler prompt via stdin:
```bash
python scripts/run_evals.py --case 1 --variant both --command "SEU_CLI_DE_AGENTE" --out output/eval-runs
```
Cada execução recebe um diretório temporário limpo contendo apenas suas fixtures. Isso não isola credenciais globais, rede ou configuração de agente. Inputs de fixture são iguais em ambas as variantes; a condição `with_skill` acrescenta SKILL.md. O adaptador injeta SKILL.md e até duas referências portáteis relevantes por caso (seleção fixa); não substitui carregamento dinâmico em um agente com acesso a arquivos. Informar esse limite.

A avaliação precisa de `pair_id` comum às variantes do mesmo caso, o mesmo revisor, dimensões idênticas e run_id diferentes. Comparações inválidas são excluídas, não promediadas. O runner só captura arquivos gerados com opt-in `--capture-workspace`; revise segredos antes de compartilhar.

## Comparação justa
Fixar modelo, versão, contexto, ferramentas, orçamento, stack, entradas e comandos. Repetir por condição. Executar no browser e salvar artefatos, screenshot completa, rotas, estados e custo. Obter avaliadores cegos ao tipo de execução, idealmente mais de um, comparando tarefas iguais. Não atribuir score de UI a texto de resposta sem implementação.

## Revisão 0–3 com evidência
Todas as dimensões usam `0=FALHA, 1=ACEITÁVEL, 2=FORTE, 3=EXCEPCIONAL`. Omitir dimensões não observadas, jamais inventar nota. P0/P1 conhecidos bloqueiam aprovação. Exemplo **apenas de esquema, não avaliação real**:
```json
{
  "case_id": 1, "variant": "with_skill", "run_id": "run-001", "pair_id": "pair-001", "reviewer": "designer-01",
  "scores": {"clareza": 2, "direcao_arte": 1, "mobile": 2},
  "evidence": ["artifacts/run-001/mobile.png", "artifacts/run-001/desktop.png"],
  "blockers": [{"severity": "P1", "evidence": "Problema documentado no vídeo do fluxo"}],
  "assertions": [{"text": "CTA funciona", "result": "FAIL", "evidence": "navegador: destino ausente"}]
}
```
```bash
python scripts/score_review.py caminho/review.json
python scripts/compare_reviews.py review-com-skill.json review-sem-skill.json
```
Comparação é DESCRITIVA. Dimensões ou revisores diferentes distorcem médias; não declarar causalidade ou ganho comercial. `UNKNOWN` não é `PASS`.

## Anti-Goodhart
Não usar URLs inventadas, entrevistas simuladas, screenshots falsas, dados inexistentes, atualizações automáticas de baseline, métricas sem medição ou "nota de beleza" automática. Revisar o próprio pior caso, não só a média.


## V9.5 — cérebro integrado à condição with_skill
O runner injeta um plano determinístico de intenção e seleção contextual de até três referências portáteis na condição com skill. A condição sem skill recebe o mesmo prompt e fixtures, mas não recebe o motor. Os dois workspaces são separados; isso não isola contas de agente, rede ou sistema operacional. O arquivo emitido é uma hipótese, nunca observação de negócio. Para medir qualidade visual, rode o agente, implemente o resultado num browser autorizado e peça avaliação humana cega dos artefatos equivalentes.
