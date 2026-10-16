# Protocolo para validação externa de qualidade da skill

A v8.1 entrega instruções, fixtures e infraestrutura. Não possui benchmark visual independente publicado. Este documento é um protocolo para um estudo real, não um relatório de resultado.

## Preparar
Usar no mínimo casos de landing, marca/mascote, dashboard denso, mobile e regressões. Fixar commit da skill, versão do modelo, orçamento, comandos e permissões. Registrar o ambiente. Nunca testar checkout real, publicar dados internos ou conectar usuário sem autorização.

## Comparar
Executar with_skill e without_skill em tentativas isoladas, repetidas, com ordem alternada. Conferir que arquivos, seed e ferramenta sejam equivalentes. Salvar outputs de código, screenshots completas, estados, logs e comandos. O runner fornece isolamento por diretório, não por sistema operacional.

## Revisar sem conhecer condição
Embaralhar os artefatos. Um revisor examina a página inteira, mobile, ações, estados e acesso; usa somente dimensões realmente observadas da rubrica. Registrar pair_id e IDs das execuções em arquivos separados. Um segundo revisor independente é preferível. Diferenças de dimensão/avaliador são rejeitadas pelo comparador.

## Medir o que dá para medir
Teste funcional com scripts de tarefa, teclado, foco, redimensionamento, zoom, ausência de movimento, texto longo, erro e recuperação. Para UX e conversão, usar testes reais com consentimento, métricas definidas antes e guardrails. Não atribuir significância a amostra curta.

## Publicar com limites
Exibir ganhos, empates e regressões por caso; descrever exclusões e UNKNOWN. Se a skill não trouxer melhora demonstrável, revisar as instruções; não modificar as notas para afirmar vitória.
