# Contrato de fixture operacional (fictícia)
É proibido alterar, adicionar ou renomear colunas/valores no redesign sem solicitação específica.
Colunas nesta ordem: Chave NF-e | CNPJ | Competência | Valor (R$) | Situação.
Registros:
- 00001 | 11.111.111/0001-11 | 09/2026 | 123,45 | Divergente
- 00002 | 22.222.222/0001-22 | 09/2026 | 987,65 | Conciliado
Objetivo: encontrar divergência, filtrar por situação e exportar seleção. Na fixture, exportação não é implementada: o redesign não deve afirmar que funciona.
A tarefa correta mantém hierarquia densa, legibilidade, filtro utilizável, indicadores confiáveis e aviso de funcionalidades demonstrativas.
