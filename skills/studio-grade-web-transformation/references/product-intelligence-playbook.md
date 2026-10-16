# Product Intelligence → Goal Intelligence → Skill Orchestration

O "cérebro" existe para responder: **que produto é, quem o usa, qual resultado importa, por que a interface atual não o produz e que conhecimento resolve a causa?** O script portátil `brain/route.py` é apenas um primeiro roteador determinístico, não substitui inspeção ou raciocínio do agente.

## Protocolo de descoberta proporcional
1. Ler repositório/site/brief disponíveis e recuperar superfícies, rotas, fluxos, público, plano/preço, modelo de negócio, posicionamento, recursos existentes, dados e marca. Não presumir funcionalidades.
2. Descobrir objetivo explicitamente declarado e objetivo implícito, separando intenção de pessoa, negócio e design. Uma conversão não é valiosa se viola confiança ou contrato; retenção só serve se gerar valor real.
3. Dividir produto em superfícies diferentes: uma fintech pode ter landing de aquisição, onboarding, portal e backoffice; cada uma exige um plano e skills distintos.
4. Consultar o roteador: `python brain/route.py brain/examples/fintech-landing.json` (na pasta da skill). Validar ou corrigir o resultado pelo conteúdo real e evidência; registrar onde a hipótese do roteador estava errada.
5. Priorizar constraints P0/P1 e objetivos; escolher referências com causalidade em domínio, mecanismo e expressão.
6. Produzir um Product Decision Brief: objetivo primário, trabalho da pessoa, sinais relevantes, 2 guardrails, antiobjetivo, fluxo atual, hipótese de intervenção, alternativas criativas, plano de testes.
7. Selecionar skill packs por **necessidade observada** e custo de contexto. Nunca carregar tudo; não usar decoração de landing como UX de sistema. Nunca mudar preço, campo, identidade ou navegação sem fundamento/autorização.
8. Executar proativamente diagnósticos adjacentes úteis dentro do escopo. Ao detectar um problema fora de escopo, registrar e propor sem alterá-lo de surpresa.

## Risco de heurísticas
Palavras-chave podem classificar errado ("página de vendas" discutida em documentação de dashboard). Contexto explícito é priorizado, sinais competidores tornam a classificação ambígua. O agente tem obrigação de validar a triagem, não tratá-la como fato.
A presença de uma referência no catálogo não comprova visita; `CANDIDATE_NOT_INSPECTED` deve ser respeitado.

## Saída
Entregar plano com produto e público, superfície, modo, objetivo e contraobjetivo, restrições, pesquisa contextual, skills por necessidade, métrica proposta (não medida), evidência e lacunas. Em PATCH seguro, reduzir o processo ao mínimo útil.
