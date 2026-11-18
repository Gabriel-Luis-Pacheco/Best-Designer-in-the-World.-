# 12 repositórios completos — espelhos integrais

Este diretório contém cópias de TODOS os arquivos rastreados pelos 12 repositórios originais que fornecem skills para a Design OS: código-fonte, CLIs, exemplos, demos, scripts, documentação, assets, extensões e skills adicionais, inclusive arquivos ocultos.

Cada pasta usa o nome owner--repo, mantém os caminhos originais e contém DESIGN_OS_SOURCE_SNAPSHOT.json com o commit de origem e a contagem de arquivos. INDEX.json só é criado depois da conferência de todos os 12, com ZERO omissões.

A única exceção é o diretório interno .git (histórico Git, e não arquivos rastreados do projeto). Para consultar commits antigos, acesse o repositório upstream pelo SHA registrado.

Licenças e avisos originais são preservados no próprio espelho. Código externo não é executado ou instalado automaticamente, e assets podem ter licenças específicas diferentes da licença raiz. A Design OS seleciona o que precisa, sem carregar todos os repositórios de uma vez.

A biblioteca anterior das 50 skills, os pacotes de motion e Revenue-Centric Design continuam preservados. Atualização: python3 scripts/sync_full_upstreams.py --sync-one OWNER/REPO; finalize com --finalize e --verify.
