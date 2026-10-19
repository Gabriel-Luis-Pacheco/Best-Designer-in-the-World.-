## v11.6.1 — validação complementar
O comparador aceita `--evidence-root` para rejeitar capturas ausentes ou vazias.
O `scripts/verify_change_scope.py` inspeciona paths realmente alterados por git;
esse teste não comprova contratos em nível de campo. Para uma comparação
completa e honesta, seguir `docs/REAL_WORLD_BENCHMARK_V11_6.md`.

# Design OS Prime v11.5 — guia de avaliação

## Validade antes da qualidade
O MIRAGE rotulado "com skill" declarou indisponibilidade da `studio-grade-web-transformation` e usou `frontend-design`. Portanto o experimento NÃO foi esta skill contra o baseline. Primeiro verificar leitura real da skill, inexistência de substituição e isolamento de outras skills. Qualquer ausência de prova deve ser marcada como comparação inválida, não derrota nem vitória. Usar `scripts/validate_experiment.py` e `docs/MIRAGE_AB_LESSONS.md`.

## Estado comprovável
Existem 61 casos de avaliação, vários com HTML/SVG/brief sintéticos; validadores Python; browser smoke Chromium; rubrica 0–3, resumo de avaliações humanas e adaptador CLI opcional. **Não** há resultados A/B com modelos nem validação estética independente publicada. PASS estrutural NÃO é design aprovado.

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
Cada execução recebe um diretório temporário limpo contendo apenas suas fixtures. Isso não isola credenciais globais, rede ou configuração de agente. Inputs de fixture são iguais em ambas as variantes; a condição `with_skill` acrescenta SKILL.md. O adaptador injeta SKILL.md, uma hipótese de roteamento e até nove referências portáteis (limite adaptativo por projeto) selecionadas por objetivo, modo e superfície; não substitui carregamento dinâmico em um agente com acesso a arquivos. Informar esse limite.

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


## V9.8 — contexto artístico, comercial e operacional integrados
O runner injeta um plano determinístico de intenção e seleção contextual de até nove referências portáteis (limite adaptativo por projeto) na condição com skill. A condição sem skill recebe o mesmo prompt e fixtures, mas não recebe o motor. Os dois workspaces são separados; isso não isola contas de agente, rede ou sistema operacional. O arquivo emitido é uma hipótese, nunca observação de negócio. Para medir qualidade visual, rode o agente, implemente o resultado num browser autorizado e peça avaliação humana cega dos artefatos equivalentes.

## V11.0 — evidence boards
A revisão visual deve incluir ao menos abertura, seção média, encerramento e mobile com **duas iterações renderizadas** quando for uma reconstrução importante. Use `scripts/visual_review_packet.py` na skill instalada para montar comparação de PNGs; o painel não julga estética. Use `scripts/asset_board.py` para investigar mascotes e imagens canônicas. Uma comparação A/B da skill exige execução isolada por variante e avaliação humana cega; não use o conceito fictício como prova de superioridade comercial.

## V11.0 — comparação justa de criatividade
Antes de comparar, confirmar skill carregada via trace e hash; mesma entrada/modelo/ferramentas/tempo/condições independentes. Capturar cinco estados visuais equivalentes (opening, first transformation, middle, climax, ending) em desktop e mobile, incluindo interações de verdade. Em cenas pinned/WebGL, não usar captura full-page isolada como evidência conclusiva. Revisor cego deve separar qualidade técnica/QA de autoria de forma, materialidade, interação e payoff. O baseline sem skill pode vencer. Publicar perdas e incertezas.

### Blind journey pairing — V11.0
Capture both conditions at same viewport, reduced-motion and planned semantic scene IDs, using local authorized projects. Run `python scripts/compare_creative_journeys.py --a WITH/manifest.json --b WITHOUT/manifest.json --out output/pair`. It verifies screenshot paths and hashes, viewport and frame coverage, and produces an anonymized A/B image board. The invocation order determines A/B; keep identity mapping outside reviewer materials. Matching screenshots do not prove same model, time budget, prompt, user state, network, interactions or cognition — verify those separately via the A/B trace controls and documented test procedure.

## V10.1 + V11 reconciliadas
A rubrica preserva quatro dimensões opcionais para trabalhos experienciais — reconhecimento de produto, continuidade de cenas, agência interativa e clímax/encerramento — mais a revisão de assinaturas formal/material/comportamental da V11. Condições são apropriadas ao objetivo; não penalizar dashboards sem clímax. As quatro avaliações da V10.1 continuam, renumeradas 58–61.

## V11.1 — integridade de experimentos
O `task_input_sha256` do briefing e das fixtures é IGUAL entre condições; o `assembled_prompt_sha256` é deliberadamente DIFERENTE porque a condição with_skill recebe instruções adicionais. Injeção de texto da skill no prompt não comprova carregamento da skill instalada; o validador estrito exige rastreio real de leitura e hash. `run_evals.py` registra `INLINE_IN_AGENT_INPUT_NOT_CONFIRMED_READ` e não afirma carregamento.

O runner seleciona guias novos da V11 para experiências artísticas, nunca para impor arte em um dashboard interno. A coleta opcional `--capture-workspace` guarda arquivos de projeto e assets 3D/fonte, mais hashes e limites, mas **pode capturar segredos**: revisar antes de compartilhar. Não salva dependências nem controla credenciais externas.

A captura visual rejeita erros JS e recursos externos bloqueados, registra significado da ação e estado observado; o pareamento exige equivalência semântica antes de permitir avaliação cega. Essas garantias são técnicas, não prova estética.

## v11.2 — avaliação de especialização
A nova cobertura de roteamento é testada em scripts/test_brain.py. Esses testes verificam presença/ausência dos packs e NÃO medem mérito criativo, performance WebGL, conversão ou resultado em Awwwards. Para esses objetivos, ampliar A/B real com protótipos de uma LP comercial, uma experiência artística 3D e um dashboard interno, incluindo renderização mobile, estados reais, revisão cega e critérios de incerteza.

## v11.3 — evidence for new executable workstreams
scripts/craft_audit.py gives source heuristics, and scripts/validate_tokens.py gives narrow DTCG reference checks. Neither renders UI or measures creative quality. brain/specialist_router.py suggests external expertise without installing it. New Python negative tests verify bounded routing, token alias failures and source-audit uncertainty. Need real multi-model, matched-budget browser experiments before any claim of creative superiority or award-level performance.

## v11.4 — compare specialist competitors instead of declaring supremacy
\`python scripts/compare_skill_league.py study/reviews.json\` reads blinded human reviews and compares Design OS vs named competing skills at equal case/model/assets/tools/budget. It never runs competitors, fetches their skills, or gives an aesthetic score. In mixed visual/UX outcomes it returns MIXED_TRADEOFF, not a winner. Review evidence must exist and should be validated separately with verify_review_evidence.py; blind status is declared by submitter. Real trial instructions and JSON schema: docs/COMPETITIVE_TRIAL_PROTOCOL_V11_4.md. New layout auditor inspects browser DOM geometry but not animations over time, WCAG conformance, or creative quality.

## v11.5 — audit actual reference loading
Run \`python scripts/audit_eval_routing.py\` on the repository to verify all 61 synthetic eval briefs have consistent reference routing and *assembled* injection. The report lists selected guides, prompt length, and control warnings. A passing report tests only source-level prompt construction, not a real agent's comprehension. Human study remains mandatory for comparisons with Impeccable, Taste, UI Craft or no skill.
