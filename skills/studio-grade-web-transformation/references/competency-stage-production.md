# Design OS — competencia por etapa, benchmark por job e criterio humano

Este protocolo complementa references/component-first-design-orchestration.md e references/human-editorial-and-anti-slop-gates.md. Seu objetivo e transformar conhecimento disponivel em DECISOES OBSERVAVEIS. **Recomendacao de skill nao significa sua utilizacao; pesquisa planejada nao significa navegacao realizada.**

## Compromisso de execucao

Em trabalho importante, a IA NAO deve se limitar a descrever "vou consultar expertos", a terminar com um belissimo plano, ou a atribuir 9/10 ao proprio layout. Deve produzir:

1. Produto/contexto real, restricoes preservadas, audiencia/necessidade, hipoteses explicitadas.
2. Referencias comparaveis, observadas de verdade, capturadas quando autorizado e possivel.
3. Handoff por competencia: pesquisador -> posicionamento -> copy/editor -> diretor de arte -> UX -> engenharia -> teste/critica; adaptar etapas ao tipo de componente.
4. Interface implementada, copy no layout real, estados completos, screenshots desktop/mobile.
5. Crítica de P0/P1 com reparo demonstrado; registro de resultado e limites da prova.

Para cada componente e modo, consultar research/component_execution_atlas.json, que contem 47 receitas e 15 etapas condicionalmente aplicadas, e gerar um workplan:

~~~bash
python skills/studio-grade-web-transformation/scripts/component_workplan.py --component hero --surface marketing --mode REDESIGN --json
python skills/studio-grade-web-transformation/scripts/component_workplan.py --component checkout --surface marketing --mode REBUILD --json
python skills/studio-grade-web-transformation/scripts/component_workplan.py --component dashboard --surface internal --mode REFINE --json
~~~

**Workplan somente planeja**, nao invoca nenhuma skill. Usar as ferramentas de skills reais da plataforma para verificar instalacao, ler instrucoes originais, respeitar prerequisitos/licencas e aplicar. Se o motor nao existe, usar guias locais, docs oficiais e evidencias honestas. Registre APPLIED, REFERENCED, UNAVAILABLE ou NOT_APPLICABLE com prova do output.

## Vínculo operacional com os 50 pacotes completos

Além dos 46 candidatos do registro central, o workplan agora faz uma **interseção seletiva** com as **50 skills vendorizadas** em `vendor/external-skill-packs/INDEX.json`. O mapa `research/vendor_phase_overlay.json` seleciona automaticamente skills mais específicas conforme o componente e a etapa: por exemplo `landing-page`, `product-proof-saas`, `copy-editing`, `audit-ai-design-slop`, `no-ai-design-slop`, `pricing-page`, `onboarding`, `wcag-audit-patterns`, `webapp-testing` e `verification-before-completion`. Elas entram como `priority_snapshots` (ate tres por fase) ou `additional_snapshots_if_relevant`. A selecao exibe o caminho e a licença reportada, **nunca finge que a skill foi carregada ou executada**. Na versao CORE sem vendor, o workplan mostra `NO_VENDOR_PACKS_IN_THIS_INSTALL` e usa as referencias internas.

Quando uma skill adequada estiver realmente instalada na plataforma, ler seu SKILL.md real e usar a ferramenta adequada; pacote local e so referencia. Nao executar scripts/instaladores externos nem ativar hooks fora do escopo autorizado. Carregar conhecimento progressivamente pelo problema observado, nao indiscriminadamente os 50 pacotes.

### Baseline competitivo para fluxos, nao so para landing page

Para componentes de conversao e ativacao com `benchmark_transfer` no atlas, o agente agora recebe tarefas comparaveis e uma meta de referencias por tipo de fluxo. Um onboarding exige observar **sequencias completas**, nao apenas primeira tela; checkout exige custo/erro/confirmacao, signup exige cadastro e retorno ao primeiro valor. **Padrao observado ≠ experiencia de fato validada**; dados de conversao de concorrentes geralmente nao estao acessiveis.

O objetivo e aproveitar convencoes bem fundamentadas antes de inventar interacoes com risco desnecessario. Registrar as escolhas ADOPT/ADAPT/REJECT, fontes, adequacao ao usuario e plano de validacao local conforme `references/benchmark-pattern-transfer-and-validation.md`. Para REDESIGN/REBUILD, o `component_delivery_gate.py` verifica um `pattern_transfer_packet` estruturalmente consistente com o mesmo `research_packet`. Se o navegador nao puder entrar no onboarding concorrente, nao inventar prints; usar pesquisa de usabilidade publicada e reportar limitacoes. PATCH nao exige pesquisa competitiva ampla.

## 1. O que significa pesquisar dez concorrentes de verdade

Para a landing ou hero estrategica, buscar ate dez **alternativas reais**, priorizando concorrentes diretos e substitutos relevantes, **mais** 2–4 exemplos de qualidade em categorias adjacentes quando ajudarem. Nao prometer que dez existem: delimitar mercado, pais, publico e pricing; nao confundir 10 URLs com 10 telas realmente estudadas. Usar tempo e orcamento proporcional: PATCH claro nao precisa de catalogo, REFINE aprovado aproveita screenshots recentes.

O protocolo e um banco de mecanicas visuais E de produto, diferente de teste competitivo real com participantes: a Nielsen Norman Group destaca tarefas equivalentes e observa que uma sessao de comparacao com usuarios normalmente expoe cada participante a dois ou tres sites, nao dez.

Para cada fonte, guardar:

| Campo | Exigencia |
|---|---|
| Identidade | URL original, tipo DIRECT/SUBSTITUTE/ADJACENT/CROSS_CATEGORY, data, audiencia e job |
| Observacao | Status NOT_INSPECTED/INSPECTED_NO_CAPTURE/CAPTURED; browser realmente aberto |
| Pixels | Desktop e mobile com viewport; caminhos de prints reais, sem fingir capturas |
| Estrutura | Hierarquia, headline, CTA, imagem/ilustracao, recorte, ritmo, distribuicao visual, densidade, transicao |
| Trabalho | Problema que secao resolve, evidencia exibida, decisao orientada, estado/resultado da interacao |
| Engenharia | Se observado: velocidade aparente, comportamento scroll, keyboard, loading; nao deduzir de print |
| Falha | Um defeito ou limite concreto da fonte (nao idolatrar o concorrente) |
| Mecanismo | **Por que funciona como HIPOTESE** (ex.: demo imediatamente proxima da promessa) |
| Adaptacao | O que fazer de forma original com a propria marca/produto, sem reproduzir expressao protegida |

**Paridade:** comparar HERO com HERO, prova com prova, precos com precos, onboarding com onboarding, navegação com navegação e job com job; se nao existir a secao equivalente, compare a pergunta do visitante, nao invente semelhanca. **Originalidade de nivel:** manter qualidade de hierarquia, coragem tipografica, clareza, acabamento e demonstracao; nao copiar personagem, fonte protegida, screenshot, assets ou composicao identificavel.

**Nao inferir sucesso comercial:** site famoso, premio de design ou grande numero de seguidores nao comprova taxa de conversao ou adequacao a outro publico. Evidencias observadas suportam descricao, nao causalidade.

## 2. A transferencia de conhecimento entre as etapas e obrigatoria

Cada especialista recebe briefing e outputs anteriores em formato curto. Nenhum produz um PDF generico de "boas praticas":

| Etapa | Que ele recebe | O que PRECISA entregar | Criterio de rejeicao |
|---|---|---|---|
| Truth | Produto, fonte atual, invariantes, oferta | Claims permitidos / desconhecidos, brand canon, risco de regressao | Inventar preco, feature, marca ou mudar login |
| Market | Publico/job, links reais | Capturas, benchmark por secao, mecanismos bons/ruins, gap | Dizer "pesquisei 10" sem abrir as 10 fontes |
| Position | Alternativas e mecanismo real | Promessa, diferenca especifica, objecao, proximo passo | "Plataforma revolucionaria" sem mecanismo |
| Editorial | Voz/palavras reais e claims | Tres angulos substantivos quando necessario, cortes, reescrita, CTA | Frase que serviria a cinco produtos, falsa naturalidade |
| Proof | Recursos e evidencia | Cena/fluxo demonstrando produto sem mockup fraudulento | Depoimento/ROI/metricas falsos |
| Art | Referencias INSPECIONADAS, canon e jobs | Uma tese autoral, opcao alternativa, decisao de tipografia/midia/composicao | Grade de cards por conveniencia, copia da marca rival |
| UX/commerce/activation/data | Regras de tarefa, estados, termos e permissao | Jornada real, questoes de usuario, sucesso/erro, friccao e recuperacao | CTA sem destino, pagamento sem contexto, dado incorreto |
| Search | Intencao, estrutura, indexabilidade | Conteudo util e semantica verdadeira | Conteudo AI-slop feito so para ranking |
| Engineering | Decisoes integradas | Codigo funcional, estados, performance e fallback | "Build success" confundido com qualidade |
| A11y | DOM, teclado, zoom e idiomas | Evidencia de foco, reflow, contraste, controle de movimento | Alegacao "WCAG compliant" sem auditoria |
| Render | Codigo/capturas e fluxo real | Pareamento visual desktop/mobile, lista de P0/P1, reparo e recaptura | Apenas autoelogios, screenshot sem inspecao |
| Measurement | Objetivo e eventos reais | Hipoteses de teste e guardrails sem causalidade inventada | "+37% conversao" sem dados |

**Resolver conflitos** por verdade do produto, seguranca, direitos, pedido do usuario, projeto/canon aprovado, tarefa do usuario e observacao real; guias externos sao conselhos contextuais. O design lead integra e pode rejeitar 12 opinioes se contradizerem evidencia.

## 3. Regras especiais para o HERO — elemento exemplar

Uma hero boa combina:
- **Problema/mercado:** quem compara alternativas e por que esta pagina merece atencao.
- **Copy:** categoria e job claros; diferenca concreta; registro real do publico, sem gírias forcadas, adjetivos vazios e chamadas iguais a qualquer concorrente.
- **Marketing/vendas:** expectativa real, proposta, objecao proximal, CTA para o passo que realmente acontece (signup/demo/tentativa). Se CTA leva ao checkout, comunicar compromisso.
- **Arte:** conceito que so faz sentido para essa marca; hierarquia da mensagem, peso, tipografia, media real, tensao visual, composicao de primeira dobra e recorte pensado para mobile.
- **Prova:** demonstracao do produto real junto da promessa; nao aceitar mascote bonito ou mockup inventado como prova da entrega.
- **UX/tecnica:** nav que orienta, texto legivel, CTA navegavel, teclado, desempenho e reduced motion; mobile e uma nova composicao, nao desktop apertado.
- **Editor cético:** "O que um redator humano excelente acharia constrangedor aqui?", "O que um comprador real entenderia sem um agente explicando?".
- **Benchmark:** avaliar frente a 5–10 seções equivalentes realmente observadas; apontar pelo menos uma decisao em que nosso resultado ainda e inferior e corrigir quando houver evidencia.

**Tres conceitos de copy antes de implementar**, se a direcao nao estiver aprovada:
1. Diretivo — usuario + tarefa + resultado.
2. Situacional — momento real em que usuario sofre + mecanismo e alivio.
3. Autoral — expressao memoravel sustentada por subtitulo concreto e prova real.

Nao escolher "autoral" so por ser criativo; prototipar no layout. Se todas sao clichês, reiniciar a ideia. Nao existem palavras universalmente proibidas: uma palavra pode soar humana num segmento e artificial em outro. A critica exige **contexto**.

## 4. Regras de qualidade por outros exemplos

**Pricing e checkout:** comparar preco total, renovacao, cancelamento, impostos/taxas quando aplicaveis, passos, erros recuperaveis, foco e confirmacao real. Baymard oferece pesquisa extensa especificamente para e-commerce; nao generalizar seus resultados a qualquer SaaS sem verificar modelo de compra. Nao gerar desconto ficticio.

**Dashboard, tabelas e graficos:** pensar primeiro na decisao, nos dados e na fonte, nao em KPIs decorativos; considerar densidade operacional e erros reversiveis. Para produtos internos, skills de vendas nao entram so porque estao no pacote.

**Onboarding e engajamento:** buscar reduzir passos ate um evento de valor real; nao chamar "login completado" de aprendizado conquistado. Retencao nao justifica vergonha, notificacao insistente ou cancelamento escondido.

**Identidade e motion:** personalidade coesa, uso de fotografia/midia licenciado e motion para significado. Nao instalar GSAP, R3F, Remotion ou outra engine por default. Testar input reduzido, desempenho e fallback sem animacao.

**Conteudo e GEO:** escrever para o usuario e a consulta real; verificar fatos e originalidade, crawler/indexabilidade, schema verdadeiro e fontes. Nao inventar "ChatGPT recomenda nossa marca".

**Admin/financeiro:** permissao, rastreio, integridade dos numeros e recuperacao superam exibicao. Nao mexer em backend ou contratos por estetica.

## 5. Rastro de conhecimento realmente aplicado — obrigatório em REDESIGN/REBUILD

O conhecimento não conta apenas por estar no repositório. Para cada fase ativa do atlas, o agente deve documentar em `competency_coverage` **de onde veio a ideia, qual decisão mudou e onde verificar o resultado**. O novo `component_delivery_gate.py` considera incompleto um redesenho grande sem esse rastro; a finalidade é impedir que 50 skills sejam apenas citadas como argumento de autoridade.

Exemplo de entrada do pacote JSON:

~~~json
{
  "phase_id": "editorial",
  "source_kind": "LOCAL_GUIDE",
  "source_id": "human-editorial-and-anti-slop-gates.md",
  "status": "REFERENCED",
  "evidence_path": "evidence/hero-copy-critique.md",
  "decision_influenced": "A headline genérica foi cortada e substituída por uma descrição verificável da tarefa, com três abordagens comparadas no layout."
}
~~~

`source_kind`: `LOCAL_GUIDE` deve pertencer à fase; `REGISTERED_SPECIALIST` deve existir no registro e ser adequado à superfície; `VENDORED_REFERENCE` precisa constar do índice e **nunca pode ser declarado uma skill externa executada**. `status=APPLIED` descreve trabalho feito e evidência real; `REFERENCED` indica consulta contextual, não invocação. O artefato citado precisa existir no projeto. Na falta de alguma ferramenta, usar guia local aplicável e declarar limites. O validador checa a estrutura, **não consegue confirmar que um humano escreveu aquele log nem que a melhoria realmente é boa**.

## 6. Gate adversarial e comprovacao

Em fases criativas, uma critica e obrigatoria: **3 defeitos localizados, 1 corte/merge real e 1 comparacao com referencia**, quando tais defeitos existirem. Nao forcar tres problemas inexistentes para preencher checklist. Nenhum agente pode dizer "melhor do mundo" sem experimento controlado.

Para trabalho implementado, guardar os artefatos de fase num packet baseado em templates/COMPONENT_DELIVERY_PACKET.example.json. Rodar:

~~~bash
python skills/studio-grade-web-transformation/scripts/component_delivery_gate.py \
  component-delivery.json --root .
~~~

Este gate exige provas declaradas para as fases, arquivos de revisao, screenshots e fluxos pertinentes; bloqueia falha conhecida e relata o que ainda falta. **Ele nao consegue medir bom gosto, copy humana, fidelidade de screenshot, autonomia real nem conversao.** O ultimo controle e julgamento humano profissional com tarefas representativas quando viavel. Registrar SELF_REVIEW_ONLY se so o modelo criticou.

Para pesquisa de referencias, continuar usando scripts/component_research_gate.py com template de referencia. Nenhuma das ferramentas locais chama MCPs de terceiros, instala skills, abre browser, tira screenshot ou altera o projeto automaticamente. Elas so ajudam o agente a nao se enganar sobre o que fez.

## Fontes e hierarquia de evidencias

Metodologias de fonte primaria ajudam a fazer melhores perguntas, mas **nenhuma diretriz garante que um layout converta mais**.

- NN/g competitive usability, tarefas equivalentes e recomendacoes de design: https://www.nngroup.com/articles/competitive-usability-evaluations/
- GOV.UK writing for interfaces, linguagem de usuario e texto escaneavel: https://www.gov.uk/service-manual/design/writing-for-user-interfaces
- Baymard checkout UX 2026, evidencia para transacoes ecommerce: https://baymard.com/research-articles/current-state-of-checkout-ux
- W3C WCAG 2.2, criterios de acessibilidade: https://www.w3.org/TR/WCAG22/
- web.dev performance e Web Vitals: https://web.dev/performance

**Limites:** recomendacoes de source catalog e arquivos vendorizados nao sao skills instaladas; autoavaliacao nao e pesquisa de usuario; screenshot externo nao certifica receita, acessibilidade ou bom gosto; funcionalidade passada no build nao e experiencia concluida.
