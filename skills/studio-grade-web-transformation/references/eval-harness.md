# Avaliação da própria skill (A/B)

Inspirado nas recomendações públicas de avaliação de Agent Skills e Anthropic Skill Creator.

1. Use `evals/evals.json` com prompts realistas, contexto e saída esperada. Incluir casos de falha, regressão, dashboard, brand fidelity, excesso de texto e site já bom que NÃO deve ser reconstruído.
2. Rode cada caso com `with_skill` e `without_skill` sob mesmo modelo, mesmos arquivos, ferramentas e limite de execução. Registre versão, custo e duração.
3. Repita quando possível para estimar variância, não premiar uma execução sortuda.
4. Peça avaliação cega de designers/usuários com `docs/QUALITY_RUBRIC.md`; não revelar qual versão é da skill.
5. Julgue P0/P1, sucesso de tarefa e evidência de implementação separadamente de preferência estética.
6. Registre relatórios e evidências; não invente benchmark ou scores quando não executou.

O script `scripts/check-evals.py` valida o formato dos testes, não roda agente nem decide qualidade visual. `scripts/score_review.py` resume notas humanas registradas; não gera avaliação automaticamente.