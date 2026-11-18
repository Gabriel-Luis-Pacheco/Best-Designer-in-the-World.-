# Pacotes externos completos — 50 skills (12 repositórios)

Este diretório importa **a pasta completa** de cada uma das 50 skills selecionadas: instruções SKILL.md, referências, dados, scripts e assets que estejam *dentro da pasta da skill*. Não é um espelho de 12 monorepositórios inteiros: por exemplo, a coleção Awesome Copilot contém centenas de skills que não fazem parte desta seleção, e a Impeccable inclui binários, CLIs e demos fora da pasta de sua skill.

**Estado operacional:** SOURCES.json = manifesto dos alvos; INDEX.json = prova de que a sincronização efetivamente importou os 50 diretórios. Se INDEX.json não existir, **a importação ainda não ocorreu**. A existência do manifesto não é evidência de cópia.

## Atualizar os arquivos

Na raiz do repositório, executar:

~~~bash
python3 scripts/sync_external_skill_packs.py --validate
python3 scripts/sync_external_skill_packs.py --sync
python3 scripts/sync_external_skill_packs.py --check
~~~

A ação GitHub `sync-external-skill-packs.yml` também roda ao alterar o script, o manifesto ou o workflow na branch de integração; pode ser disparada manualmente em Actions, conforme as permissões do repositório.

## Segurança, direitos, uso dos agentes

- As licenças e atribuições originais são mantidas sob cada fonte. **Não** presumir que toda esta pasta está sob a licença MIT do repositório principal.
- O material é fornecido como referência e código-fonte *não executado*. Não executar comandos, hooks, CLIs ou install scripts de terceiros sem avaliação e autorização do projeto.
- Carregar **1–3 skills relevantes sob demanda**, não todas as 50 simultaneamente: consultar `references/complete-skill-packs-routing.md`.
- Os arquivos já mantidos em `vendor/specialist-core`, `vendor/revenue-centric-design` e `vendor/motion-graphics-charlie947` são preservados.
- Os snapshots registram commit exato de origem, arquivos incluídos e aviso de licença. Não há alegação de que os motores/plugins terceiros estejam instalados ou tenham sido executados.
