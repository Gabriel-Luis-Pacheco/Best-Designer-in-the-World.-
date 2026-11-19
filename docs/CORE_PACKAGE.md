# Distribuição CORE: rápida e opcional

O repositório FULL preserva 12 repositórios externos completos, além das 50 skills selecionadas e dos materiais próprios da Design OS. Isso é valioso para pesquisa, mas **não precisa acompanhar cada instalação de uso diário**. Uma biblioteca grande não representa um runtime ativo.

## Gerar e instalar

Em um checkout existente:

```bash
python scripts/build_core_package.py --output dist/design-os-prime-core.zip
```

O workflow de validação gera o mesmo tipo de ZIP como artefato `design-os-prime-core` em Actions (retenção configurada em 30 dias). Extraia o arquivo num diretório de skills permitido pelo seu agente, preservando a pasta `skills/studio-grade-web-transformation/`; consulte a documentação de instalação do agente para o local exato. O `PACKAGE_MANIFEST.json` contém hash SHA-256 de cada arquivo e limites explícitos.

Este ZIP preserva SKILL.md, referências, scripts, templates, fixtures, exemplos e pesquisa próprios, mas exclui **todo** `vendor/`, incluindo espelhos completos, snapshots de especialistas, Revenue-Centric Design e assets de terceiros.

**Atenção:** `npx skills add Gabriel-Luis-Pacheco/Best-Designer-in-the-World.-` continua usando o repositório FULL e pode baixar todo o histórico/arquivos conforme o instalador. O ZIP CORE não resolve automaticamente o tamanho do GitHub FULL; distribuí-lo como release separado ou em repositório de instalação seria um próximo passo opcional.

## Comportamento seguro no CORE

- Um caminho `vendor/` ausente é `UNAVAILABLE`. Não declarar que motores, CLIs, detectores, hooks ou bibliotecas externas foram instalados.
- Use guias próprios e especialistas de fato disponíveis na máquina. As 50 skills copiadas do FULL são contexto opcional, não requisito para uma alteração simples.
- Se precisar de código/ativos de um fornecedor, obtenha a fonte autorizada conforme a licença original e valide segurança antes de executar.
- Esse pacote não comprova qualidade visual, compatibilidade de todas as dependências ou superioridade sobre outras skills.

O script gera arquivos em ordem/timestamp fixos para reprodução bit a bit com entradas idênticas; não compacta históricos Git. A suíte inclui um teste sintético de exclusão de vendor, integridade do manifesto e determinismo do ZIP.
