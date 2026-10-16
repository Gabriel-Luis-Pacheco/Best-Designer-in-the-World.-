# UX de produto denso e operacional

A excelência de dashboard e SaaS nasce da precisão, eficiência e controle do usuário — não de transformá-lo numa landing com cards enormes.

## Contrato da tarefa
Por papel, levantar objetivo, frequência, dados necessários, decisão, custo do erro, reversibilidade e estado após falha. Validar com dados reais autorizados ou fixtures sintéticas claramente rotuladas.

## Invariantes de dados
Preservar colunas, chaves, unidades, filtros, ordenação, identidade de linha e provenance. Nunca acrescentar, remover ou renomear dado por estética sem consentimento. Exportação deve representar a seleção e os filtros anunciados.
Distinguir zeros, ausências, dados não carregados e filtros sem resultado. Compor tabelas para varredura, números alinhados, cabeçalhos inteligíveis e truncamento reversível. Em mobile, priorizar tarefa e permitir acesso ao dado completo, sem eliminar campos ocultamente.

## Estados extremos
Testar 0/1/100/100000 linhas, nomes extensos, caracteres internacionais, loading, erro de rede, permissão negada, duplicidade, seleção em lote, atualização concorrente e exportação. Testar sem mouse e com zoom.
Dar confirmação para efeitos irreversíveis; oferecer desfazer quando possível. Uma interface silenciosa após erro não é minimalismo, é falha.

## Métricas reais
Tempo de conclusão, taxa de erro, recuperação e precisão de exportação são mais relevantes que "uau visual". Quando não medidos, descrever hipóteses, não porcentagens.
