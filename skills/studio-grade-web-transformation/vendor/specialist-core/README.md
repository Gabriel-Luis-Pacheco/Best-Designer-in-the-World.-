# Núcleo dos especialistas — espelhos de instruções, não instalação operacional

**Data da coleta:** 14/11/2026. Estes sete arquivos de instrução foram copiados diretamente dos repositórios originais, acompanhados das licenças correspondentes. O JSON `SOURCES.json` guarda o repositório, o caminho, a revisão observada e o SHA do blob no momento da captura.

**Atenção:** não se trata de um empacotamento funcional de todas as ferramentas. Arquivos internos, referências adicionais, CLIs, binários, hooks, bancos de dados, extensões e assets de cada fornecedor **não** estão presentes aqui. Exemplos: o detector e Live da Impeccable, a base pesquisável do UI/UX Pro Max e os checks/fixtures da Taste. Um arquivo `SOURCE_SKILL.md` local significa somente **referência textual disponível**, nunca `INSTALLED` nem `EXECUTED`.

## Origem, papéis e licenças

| Fonte | O que foi incluído | Licença preservada |
|---|---|---|
| [Impeccable](https://github.com/pbakaus/impeccable) | SKILL principal | Apache-2.0 |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | SKILL principal | MIT |
| [Emil Kowalski](https://github.com/emilkowalski/skills) | `emil-design-eng`, `animate`, `choreograph` | MIT |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | SKILL principal | MIT |
| [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | SKILL principal | Apache-2.0 |

Os arquivos de origem mantêm seu próprio copyright e licença, não herdam automaticamente a licença principal da Design OS. Não alterá-los sem manter atribuições e marcar modificações quando exigido. Para utilizar **as capacidades completas**, instalar as ferramentas a partir das fontes oficiais e seguir seus próprios pré-requisitos. Use `references/full-specialist-stack.md` para orquestração e `scripts/design_stack_router.py` para conferir disponibilidade. A skill principal da Design OS é a responsável por resolver conflitos.

## Por que não incorporamos todos os repositórios completos
A Impeccable inclui runtime, hooks, binários e integração Live; Taste e UI/UX Pro Max incluem scripts/dados; copiar tudo, além de multiplicar tamanho e manutenção, pode introduzir execução de terceiros e licenças específicas. O pedido de usar as cinco é atendido por **orquestração obrigatória nos projetos visuais importantes** e referências internas como contingência. Executar ferramentas externas continua dependendo de instalação real e permissões da máquina.

**Não executar** código copiado de terceiros só porque está presente nesta pasta. O conteúdo é referência, não credencial, plugin instalado ou ferramenta habilitada.
