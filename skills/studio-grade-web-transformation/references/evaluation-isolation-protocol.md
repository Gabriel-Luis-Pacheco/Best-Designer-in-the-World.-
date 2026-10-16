# Segurança e validade de experimentos A/B

O runner usa diretórios de trabalho temporários e limpos, contendo apenas fixtures da tarefa. Isso impede a contaminação de arquivos entre variantes, mas NÃO isola processos, perfis de agente, contexto remoto, rede, credenciais ou ferramenta global. Usar CLI confiável e ambiente autorizado.

Para inferência comparativa: fixar modelo, configuração, prazo, custo, ferramentas e inputs; alternar ordem, repetir casos e guardar artefatos e logs sanitizados. Não deixar a condição sem skill carregar SKILL.md através de configuração global.
Arquivar artefatos só por opt-in (`--capture-workspace`) e revisar antes de compartilhar; arquivos podem conter dados privados.
Avaliações humanas exigem `pair_id` comum para um caso, mesmo revisor, mesmas dimensões e run_id distintos. Não confundir nota descritiva com causalidade, conversão, satisfação ou distinção artística certificada.
