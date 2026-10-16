# UX writing, fluxos e interações com significado

## O trabalho do texto
Escrever para explicar ação, consequência e próximo passo. Trocar "Comece sua jornada" por CTA específico quando houver ação real. Textos essenciais de recorrência, trial, limites, cancelamento e privacidade devem ser descobertos antes da ação, nunca escondidos em tooltip.

## Matriz para cada interação crítica
`estado inicial → intenção → gatilho → feedback → recuperação → próximo estado`.
Para cada fluxo: acessibilidade do nome e foco; bloqueio de clique duplo; loading honesto; mensagem de erro específica e recuperável; ação reversível quando possível; persistência correta; mobile touch; teclado e redução de movimento. Uma demo visual nunca deve sugerir que um recurso funciona quando ele é conceitual.

## Casos que devem ter teste
- Cadastro/login: erro útil, foco orientado, campo preservado, sem revelar dado sensível.
- Pagamentos: plano/preço/recorrência verdadeiros, nenhum plano alterado por design.
- Menu: abrir, percorrer por teclado, fechar, foco coerente e scroll apropriado.
- Tabelas: ordenar, filtrar, exportar, selecionar, desfazer, evitar perda de dados e confusão de unidades.
- Feedback: sucesso sem falsa celebração; recuperação para erro de rede; vazio que explica próxima ação.

## Conversão sem manipulação
Aumentar clareza, demonstração verdadeira e confiança. Não fabricar testemunhos, badges, contadores, escassez ou garantias. Se a hipótese é aumentar conversão, registrar métrica, guardrails e instrumentação; sem teste, chamar hipótese.

## Critério de revisão
Uma pessoa que nunca viu o produto consegue explicar o que acontecerá ao clicar? Se não, melhorar affordance, rótulo, contexto e resposta ao clique, antes de adicionar animação.
