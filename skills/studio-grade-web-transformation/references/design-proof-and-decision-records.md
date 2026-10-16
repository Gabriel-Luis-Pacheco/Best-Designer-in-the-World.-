# Contratos e decisões com evidência

## Inventário de invariantes
Registrar para cada tarefa: rotas, links, preços, recorrência, limites, CTAs, dados e unidades, colunas/identificadores, estados de interação, marca e licença. Para cada linha: ID, fonte, confirmação, risco, teste e permissão de alteração.
Exemplo fictício: CTA-1 "Experimentar uma conversa" -> #demonstracao; PRICE-1 Plus R$19,90/mês; TRUTH-1 o protótipo não implementa checkout.

## Verdade, inferência e proposta
VERIFICADO exige código, execução ou fonte realmente inspecionada. INFERIDO não se transforma em fato por repetição. PROPOSTO é decisão candidata. NÃO VERIFICADO é obrigatório quando ambiente, permissão ou ferramenta estiverem indisponíveis. Nunca mudar briefing para legitimar uma interface já construída.

## Registro de evidência
Toda afirmação de qualidade precisa de: claim, método, ambiente, data, artefato, resultado, limites e revisor.
- E0: ideia ou hipótese.
- E1: inspeção de código, imagem ou documentação.
- E2: execução ou teste reproduzível.
- E3: observação humana real, com tarefa e perfil registrado.
- E4: resultado de produto com coleta válida.
Uma screenshot nunca é E3 e um CI verde nunca prova E4.

## Decisão adversarial
Descrever a solução escolhida, alternativa derrotada, trade-off, principal argumento contra a escolha, evidência necessária para rever e impacto no contrato.
P0/P1 documentado bloqueia aprovação; UNKNOWN não equivale a PASS. Sem revisão independente, não atribuir tal revisão.
