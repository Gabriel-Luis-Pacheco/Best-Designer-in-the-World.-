# Design OS Prime v14 — auditoria crítica baseada no código

Estado: ferramentas e testes estruturais. Isto NÃO é benchmark estético, auditoria WCAG formal, pesquisa com usuários, inspeção ao vivo de um cliente ou prova de conversão.

## Defeitos encontrados e reparos

| Risco | Defeito demonstrado | Medida executada |
|---|---|---|
| P0 | Conselho aceitava aprovações de críticos sem tarefas ou evidências observadas | Agora exige tarefa, artefatos, veredito, providências e evidência pós-correção de P0/P1 |
| P0 | Falha na primeira versão podia bloquear eternamente uma entrega já corrigida | Reconciliação das falhas históricas com o RELEASE, preservando o registro |
| P1 | Bastava um cabeçalho PNG plausível para aceitar uma suposta captura | Validação de chunks, CRC, IHDR, IDAT e IEND; continua sem autenticar o navegador |
| P1 | Toda reconstrução tinha que mudar algo, mesmo sem defeito material | Decisão explícita de preservar trabalho bom com explicação e evidências |
| P1 | Entradas JSON de tipo incorreto causavam exceções em verificadores públicos | Verificações de tipo e testes adversariais para modos, papéis, direitos, resultados e HTML |
| P1 | Uma auditoria inteira perdia lentes de arte/copy e landing simples podia exigir sete críticas | Papéis fundamentais versus opcionais; AUDIT abrangente, PATCH proporcional |
| P1 | Brief, crítica, render, SEO, assets e copy não se encontravam em uma avaliação final | quality_controller.py agrega resultados com estados de incerteza e bloqueio |
| P2 | Direções criativas apenas reordenadas contavam como alternativas diferentes | Rejeição conservadora de quase duplicatas lexicais |
| P2 | O hash de vídeos exigia carregar o arquivo inteiro na memória | Processamento por chunks de 1 MiB |
| P2 | SEO estático falhava em atributos HTML booleanos e não apontava alguns problemas | Sanitização de atributos, língua declarada, links sem href e prévia social |

## Protocolo de produção

1. Volte ao briefing literal antes da direção, após o primeiro render e antes de entregar. Preserve nomes próprios, identidade, comportamento e restrições.
2. Compare ideias que realmente diferem em narrativa, composição e mecanismo específico; não imponha competição de conceitos a um PATCH.
3. Implemente a abertura, o meio, o final, a experiência mobile, as transições e as ações reais conforme o escopo autorizado.
4. Capture o produto renderizado quando o ambiente permitir; não chame de PASS algo que foi apenas proposto.
5. Use especialistas independentes apenas quando subagentes reais estiverem disponíveis, com rastros de execução. Caso contrário, declare autocrítica sequencial.
6. Corrija a causa de problemas P0/P1 e reexecute verificações; preservar uma parte boa também é uma decisão válida.
7. Para sites comerciais públicos, examine posicionamento, copy, prova, próxima ação e SEO. Para produto interno, priorize a tarefa, integridade dos dados e estados reais.
8. Na entrega, compare o estado final com o pedido original e reporte claramente tudo que ainda não foi verificado.

## Controlador integrado

A ferramenta opcional fica em:

    skills/studio-grade-web-transformation/scripts/quality_controller.py

Dentro do projeto autorizado, crie qa/manifest.json com campos conforme o escopo. Exemplo:

    {
      "mode": "REBUILD",
      "surface": "landing",
      "public": true,
      "named_reference_required": true,
      "cinematic_required": false,
      "brief": "qa/brief.json",
      "production": "qa/production.json",
      "reviews": "qa/reviews.json",
      "positioning": "qa/positioning.json",
      "assets": "qa/assets.json",
      "asset_root": ".",
      "evidence_root": "qa/evidence",
      "html_pages": ["dist/index.html"]
    }

Execute na raiz do projeto:

    python skills/studio-grade-web-transformation/scripts/quality_controller.py qa/manifest.json --root .

O resultado diferencia:
- INVALID: dados incompatíveis, arquivos inacessíveis ou caminhos fora do projeto.
- BLOCKED: requisitos críticos ou falhas P0/P1 abertas; por exemplo, noindex inadequado numa landing pública.
- INCOMPLETE: evidências, capturas, revisões ou checagens exigidas ausentes.
- EVIDENCE_PACKET_FOR_HUMAN_REVIEW: o pacote está estruturalmente pronto para análise humana; não significa aprovação visual, legal ou comercial.

As declarações do conselho são confrontadas com arquivos locais reais, mas a existência dos arquivos não autentica avaliação independente nem o conteúdo visual. O controlador não gera imagens, não navega em sites externos e não chama subagentes por conta própria.

## Lacunas que NÃO foram resolvidas

- Sem benchmark real com a mesma tarefa, modelo, ferramentas, recursos e tempo, não há prova de que a v14 supere a v13 ou skills concorrentes.
- Um verificador de manifesto nunca substituirá inspeção visual, vídeo renderizado, qualidade de animação, um designer, testes de tarefas com usuários ou julgamento humano.
- Referências oficiais e hashes não concedem direitos de reprodução de mídia ou personagens em campanhas comerciais.
- SEO e conversão exigem dados de um site publicado; Search Console, indexação, medição de campo e testes reais não são simuláveis por HTML estático.
- A biblioteca contém muitos guias opcionais e sobreposição de linguagem. Novas orientações devem preferencialmente consolidar ou substituir regras antigas com base em defeitos observados, não apenas aumentar o volume de tokens.
- O repositório pode conter caminhos não cobertos por estes testes. O presente relatório é uma auditoria focada no núcleo, nas rotas de avaliação e nos validadores de produção.

**Critério permanente:** intenção exata + implementação real + prova examinável + crítica com fonte identificada + reparo causal. Nenhuma nota de beleza automática nem promessas universais.
