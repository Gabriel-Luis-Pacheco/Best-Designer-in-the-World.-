# Aprendizado de resultados sem fabricar causalidade

Loop: objetivo -> hipótese -> intervenção -> evidência -> comparação -> objeção -> correção.
O roteiro `brain/feedback_loop.py` resume observações declaradas, sem verificar sistemas de analytics; dados ausentes permanecem UNKNOWN. Sinais numéricos de uma tela não provam causalidade, eficácia ou melhoria geral. Controles, coortes e amostragem são necessários.

## Exemplo de guardrail
Se a landing converte mais, mas pessoas não compreendem o preço, houve regressão de confiança. Se alunos acessam mais dias, mas resultados em avaliações pioram, retenção não valida aprendizagem. Se a conciliação fica rápida, mas aumenta erro fiscal, velocidade não é vitória.
Diferenciar métricas de tarefa, negócio, satisfação, acessibilidade, erros e longo prazo. Prioridade real depende de evidências, não de um score automático.

## Aprender na skill
Revisão de melhorias somente depois de exemplares antes/depois e casos adversariais. As regras `brain/route_rules.json` são editadas por revisão explícita, nunca automaticamente pelo feedback. Preservar caso desfavorável para impedir overfitting.
