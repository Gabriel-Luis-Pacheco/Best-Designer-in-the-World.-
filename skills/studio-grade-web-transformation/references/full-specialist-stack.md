# FULL STUDIO STACK — integração operacional das skills especialistas

**Data:** 14/11/2026. Objetivo: atender ao pedido de combinar a Design OS Prime com Impeccable, Taste Skill, Emil Kowalski, UI/UX Pro Max, Anthropic Frontend Design e módulos de motion. **A Design OS permanece coordenadora e responsável pelo resultado.** Não declarar que CLIs, browser, hooks, subagentes, dependências ou benchmarks externos rodaram apenas porque seu SKILL.md está copiado.

## 1. Regra operacional para trabalhos de alto impacto
**É obrigatório considerar as cinco famílias em um novo site significativo, produto visual, redesign, landing principal, campanha ou experiência artística importante.** Para cada família registrar em memória de execução, sucintamente: `DISPONÍVEL + APLICADO` (com arquivo/comando/evidência), `CONSULTADO COMO REFERÊNCIA`, `NÃO APLICÁVEL` (motivo preciso) ou `INDISPONÍVEL`. Se houver real ganho complementar, **usar cada uma** na sua especialidade, e não apenas citar nomes.

A consulta a todas as famílias é obrigatória em trabalho visual grande. A execução indiscriminada de todos os comandos **não** é: não acionar um detector de UI num vídeo sem frontend, não executar GSAP num app sem animação, não impor estética de marketing a sistema fiscal. Para PATCH simples, usar só o especialista capaz de resolver o defeito; para REFINE aprovado, preservar direção e pesquisar apenas lacuna observada.

### As cinco especialidades combinadas
| Especialista | Responsabilidade no FULL STUDIO | Uso concreto quando instalado | Fallback incluído na skill |
|---|---|---|---|
| **Impeccable** ([fonte](https://github.com/pbakaus/impeccable)) | Diagnóstico de UI real, detector de slop, `critique`/`audit`, polish, variantes Live quando permitido | Chamar CLI nativa `impeccable` nos comandos alvo e ambiente local; verificar resultados | `vendor/specialist-core/impeccable/SOURCE_SKILL.md`; NÃO possui binário, detector ou Live |
| **Taste Skill** ([fonte](https://github.com/Leonxlnx/taste-skill)) | Tese de direção de arte, autenticidade, composição, critérios de acabamento | Consultar a skill instalada e aplicar apenas regras compatíveis com brief e marca; inspecionar real render | `vendor/specialist-core/taste/SOURCE_SKILL.md` |
| **Emil Kowalski** ([fonte](https://github.com/emilkowalski/skills)) | Microinterações, coreografia, easing, performance e animação | `animate`, `choreograph`, `review-animations` ou área exata que a ferramenta instalar | `vendor/specialist-core/emil/SOURCE_SKILL.md`, `ANIMATE_SKILL.md`, `CHOREOGRAPH_SKILL.md` |
| **UI/UX Pro Max** ([fonte](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)) | Pesquisa e seleção de padrões, contraste, tipografia, templates adequados à tarefa | Busca local na base de dados/CLI oficial se efetivamente instalada | `vendor/specialist-core/ui-ux-pro-max/SOURCE_SKILL.md` sem bancos/CLI de busca |
| **Anthropic Frontend Design** ([fonte](https://github.com/anthropics/skills/tree/main/skills/frontend-design)) | Linguagem visual autoral, qualidade de primeira direção, escolhas de layout/copy com opinião | Leitura/invocação do skill oficial instalado para nova direção ou redesign | `vendor/specialist-core/anthropic/SOURCE_SKILL.md` |

**Sequência em trabalho visual grande:**
1. Brief, site/código atual, cânone, marketing, público, função e dados. Decidir PATCH/REFINE/REBUILD e superfície Persuade/Operate/Read/Experience.
2. **Anthropic + Taste:** formar ou criticar ideia visual específica com referências realmente inspecionadas, sem impor looks genéricos.
3. **UI/UX Pro Max:** procurar padrões, tokens, tipografia e riscos relacionados ao tipo de tela; não deixar uma categoria substituir a personalidade da marca.
4. **Emil:** definir comportamento/microinteração e quando NÃO animar; não colocar efeitos em conteúdos de leitura sem propósito.
5. **Impeccable:** revisar/polir/auditar no código e navegador disponíveis; detector e Live apenas se instalados/permitidos. **Atenção:** o modo Live pode aplicar alterações executando agentes com permissões elevadas dependendo da configuração: não ativar bypass de aprovação, nem contra CSP/produção, sem consentimento e entendimento do risco.
6. Design OS integra, implementa em código real, testa o alvo, captura desktop/mobile, corrige o defeito crítico e entrega. Um relatório de cinco especialistas sem implementação não é entrega.

O processo não exige cinco agentes LLM separados: pode ser leitura/ferramenta especializada, desde que **realmente aplicada** e com evidências. Ponto de vista independente só quando execução separada existe.

## 2. Motion Studio — mais três famílias oficiais/referenciadas
Quando houver **motion substantivo, anúncio, Reel, microanimação, vídeo comercial ou demo**, ler `references/motion-studio-pack-2026.md`. Avaliar estas três famílias adicionalmente:

| Família | Status nesta skill | Quando usar |
|---|---|---|
| [Charlie947 motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills) | **15 `SKILL.md` copiados**, licença MIT preservada em `vendor/motion-graphics-charlie947/` | brand intake, motion brief, explainer, charts, launch, title 3D, export social etc. |
| [Awesome Claude Motion Graphics](https://awesomeclaude.ai/claude-motion-graphics) | **17 estilos catalogados e adaptados**, processo de storyboard/frames reproduzido em linguagem própria | Escolher gramática visual específica e verificável por frames |
| [Remotion Agent Skills](https://www.remotion.dev/docs/ai/skills) | **Roteamento para instalação oficial**, sem alegar que os arquivos/engine estão incluídos | Projeto de vídeo React/Remotion; criar, renderizar, captions e docs com API/versionamento certo |

**Remotion não substitui HyperFrames automaticamente.** Para BataTalk em `v8-publica`, manter o pipeline determinístico salvo justificativa real. Para página web com animação scroll, GSAP/DOM podem ser adequados; para peça React renderizada em MP4, Remotion pode ser melhor. Escolher por resultado e custo, não por “todos ao mesmo tempo”.

## 3. Instalações oficiais opcionais (não executadas automaticamente)
Estas são as rotas documentadas nos repositórios. A cópia de SOURCE_SKILL não inclui seus motores. Executar no projeto **somente após verificar ambiente, versões, dependências e aprovação**:
```bash
# Impeccable (instalador e detector, com hooks a revisar)
npx impeccable install

# Skills de Emil
npx skills add emilkowalski/skills

# Taste
npx skills add Leonxlnx/taste-skill

# UI/UX Pro Max (conforme README oficial)
npx ui-ux-pro-max-cli init --ai claude

# Anthropic Frontend Design
npx skills add anthropics/skills --skill frontend-design

# Charlie947: 15 workflows de motion
npx skills add charlie947/motion-graphics-skills

# Remotion: somente quando Remotion for usado
npx remotion skills add
```

Estes comandos são **instruções, não ações já efetuadas no computador do usuário**. Confirmar argumentos da versão vigente antes de instalar. Nunca iniciar binário desconhecido, apagar skills preexistentes ou habilitar hooks de terceiros sem supervisão. Quando o usuário pedir execução local, o agente pode fazer a instalação permitida com inspeção de riscos no ambiente correto.

## 4. Orçamento de contexto e conflitos
Os especialistas podem se contradizer (ex.: princípios de `no gradient` versus marca com gradiente aprovado). Resolver por brief real, função, teste de visual e direitos, não por obediência simultânea a proibições. **Ler todos os 5 arquivos integrais em toda tarefa pode custar muitos tokens e reduzir foco**: na triagem ler cabeçalho/instruções relevantes, carregar referência inteira só para especialidade que mudará a decisão.

Em trabalho complexo, relatórios curtos por lane, uma única direção final, um único ciclo de código/render/critique/repair. Um score de Impeccable não comprova conversão, e nenhuma grande marca/skill garante Awwwards.

## 5. Evidência auditável
Fechamento do trabalho substancial:
- Que specialists foram realmente instalados e usados? Quais eram apenas snapshots consultados? Quais não se aplicaram?
- Código/arquivo alterado, caminho do artefato, teste real e capturas pertinentes.
- Qual problema dominava? O que foi corrigido? Prova antes/depois no mesmo viewport/estado.
- Resultado de acessibilidade/performance **quando medidos**, hipóteses quando não.
- Não publicar, instalar no sistema do usuário, conectar credenciais, habilitar telemetria/hook ou burlar permissões por conta própria.

**Fontes/licenças:** `vendor/specialist-core/README.md` e `SOURCES.json`. Remotion e Awesome Claude permanecem referências/integrações condicionais. Dados de qualidade e comparações futuras exigem testes reais com as mesmas tarefas.
