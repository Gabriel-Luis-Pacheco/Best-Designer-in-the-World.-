# Design OS Prime — auditoria crítica e correções (11/11/2026)

**Objeto:** repositório completo em relação ao fluxo de uso real da skill (núcleo, especialistas, roteadores legado/canônico, scripts, CI, documentação, riscos de LP e de sistemas). **Método:** inspeção de arquivos e execução de testes sintéticos no GitHub Actions. Não houve benchmark visual controlado, execução dos 46 especialistas, investigação de aplicações clientes, medição de receita, auditoria WCAG integral ou análise de produção.

## Diagnóstico — causa, risco e mudança

| Grau | Causa identificada | Risco antes | Correção |
|---|---|---|---|
| P1 | Dois sistemas independentes de seleção (brain/specialist_router.py + scripts/specialist_router.py) com catálogos e limites diferentes | O mesmo pedido podia produzir experts divergentes e forçar no máximo três, apesar da política sem quotas | O roteador legado passa a ser adaptador do canônico. O catálogo especialista antigo permanece histórico e não é fonte ativa |
| P1 | O roteador novo usava correspondência positiva simples de termos | Pedidos como "sem WebGL/GSAP" ou "sem Impeccable" podiam recomendar justamente o que foi vetado | Negação contextual e veto a nomes, com regressões. Heurística ainda não é linguagem natural completa |
| P1 | CEO específico do BataTalk era elegível por simples ocorrência do nome | Possível sugestão de operador empresarial proprietário fora de autoridade explícita | Gate opt-in para tarefa BataTalk autorizada; não concede permissões ou delegação automática |
| P1 | Roteamento de marketing e dashboard interno se misturava | Um dashboard operacional podia receber especialista de funil comercial irrelevante | Novo filtro de intenção comercial para especialistas de marketing em interface interna |
| P1 | Catálogo atual perdeu 3D, R3F, browser/perf/tokens/anti-slop do antigo | Redução real de cobertura apesar do aumento de 40 especialistas | Seis entrypoints públicos verificados adicionados ao catálogo atual (46 total); real instalação permanece independente |
| P1 | Autenticação, permissões, pagamentos e falha de serviço eram tratados mais como slogans de QA que como jornadas com contratos | Interface podia parecer concluída enquanto estados financeiros/de acesso não estavam confirmados | Guias contextuais de transações, privacidade, internacionalização/CMS e confiabilidade/recuperação |
| P2 | Instruções densas e capacidades externas confundiam "referência" com "ação" | Consumo de contexto e risco de declarar execução inexistente | Roteamento canônico, guias por risco, distinção candidate/detected/invoked/tested e documentação central |
| P2 | Testes não cobriam veto a ferramentas, autoridade CEO e preservação de tarefas pequenas | Regressões ao evoluir catálogo ou roteamento | Testes unitários direcionados + CI sintético; verificações não equivalem a desempenho estético |

## Arquitetura operacional pós-correção

1. **Entrada única:** studio-grade-web-transformation continua responsável por requisito literal, verdade do produto, direção artística, implementação e verificação.
2. **Dois tipos de roteamento, funções diferentes:** scripts/design_workflow.py escolhe guias INTERNOS e riscos por tarefa; scripts/specialist_router.py identifica CANDIDATOS EXTERNOS. brain/specialist_router.py mantém uma interface antiga mas usa o catálogo novo.
3. **Especialistas reais:** disponíveis apenas se a ferramenta/agente os tiver instalado e carregado por mecanismos legítimos. URL GitHub e arquivo local são evidência insuficiente de execução.
4. **Permissão:** mudança financeira, mensagens externas, produção, direitos, dados, ferramentas e políticas dependem de autoridade. BataTalk CEO requer contexto e autorização explícitos.
5. **Saída:** mudanças reais + estados renderizados/funcionais + testes + incertezas. Nunca certificação de beleza por número de guias.

## O que a skill agora cobre melhor

- **Landing:** direção/identidade/anti-slop, mensagem e prova, funil de venda, CRO, growth, SEO/GEO, copy (inclusive Great Leads), psicologia ética, e alinhamento do CTA com primeira experiência real.
- **Produto:** navegação, tarefas e recuperação, autenticação/identidade, papéis/tenants, checkout, permissões, confirmação real de pagamentos, conteúdo e respostas de servidor.
- **Canais/mercados:** formatos regionais, internacionalização, CMS e publicação, conteúdo SEO multilíngue, privacidade/consentimento, marketing e governança.
- **Operação:** estados degradados, retries, logging/analytics com cautela de privacidade, feature flag/rollback quando realmente existem, suporte e qualificação de evidências.
- **Engenharia visual:** especialistas 3D/WebGL/R3F, GSAP, browser Playwright, performance CWV, acessibilidade, tokens/DTCG e QA funcional.

## Lacunas que permanecem ou só são abordadas parcialmente

| Prioridade | Âmbito | Status real / próxima melhoria necessária |
|---|---|---|
| ALTA | Benchmark real das skills | Ainda não há experimento controlado com mesmo modelo, tempo, assets, ferramentas, screenshots e revisores cegos. Não há prova de liderança estética |
| ALTA | Testes de uso com pessoas | Guias pedem pesquisa, mas o repositório não executa recrutamento, sessões, testes de compreensão, entrevistas ou experimentos com usuários |
| ALTA | Segurança, privacidade e conformidade técnica | Guias UX não substituem revisão de auth/RLS, ameaças, segredo, fraude, proteção de APIs, LGPD/GDPR e validação de pagamentos |
| ALTA | Performance e acessibilidade de produção | Fixtures Playwright não cobrem toda configuração de navegadores, leitores de tela, dispositivos reais, campo RUM, WCAG completo |
| ALTA | Telemetria e atribuição comercial de verdade | Precisa de dados reais de produção, métricas por coorte, consentimento e integrações com analytics/CRM; nada é inferido por mockups |
| MÉDIA | Design de produtos AI-native | Falta aprofundar avaliação de resposta probabilística, controle do usuário, recuperação de erro do modelo, transparência, custo/latência e segurança de prompt/entrada |
| MÉDIA | Sistemas administrativos complexos e enterprise | Fluxos profundos de RBAC, SSO/SCIM, auditoria, dados em massa, estados offline, migração, filas e acessibilidade em tabelas densas ainda dependem do projeto |
| MÉDIA | Design system vivo e governança | Tokens/componentes e Figma estão documentados, mas não há sincronização automática comprovada entre componentes, documentação, CI visual e rollout |
| MÉDIA | Conteúdo e brand operations | CMS agora tem critérios; faltam ferramentas de aprovação, direitos/licenciamento automatizados, tradução real e revisão regular de provas expiráveis |
| MÉDIA | Suporte, confiança e pós-venda | Existe orientação genérica de recuperação; não há produto de suporte (central de ajuda, tickets, SLA, revisão de reclamações, aprendizado) implementado |
| MÉDIA | Otimização contínua por dados | Sem ferramenta conectada de experimentos/RUM/CRM, a skill não consegue provar conversão e retenção, nem atualizar prioridades com telemetria |
| BAIXA/CONDICIONAL | 3D de alto custo e XR, interfaces multimodais, acessibilidade nativa específica | Precisam de runtime, devices/assistive tech, assets e métricas compatíveis; não justifica impor isso a uma LP comum |

## Recomendações para a próxima evolução

1. **Menos texto de instrução, mais execução de fixtures reais.** Evitar novo catálogo universal; consolidar guias redundantes quando forem identificadas falhas concretas.
2. **Avaliação adversarial por tipo de tarefa.** Testar contra prompts com vetos, permissões, pequenas alterações, projetos existentes excelentes, múltiplos papéis, preços, dados e marcas canônicas.
3. **Benchmark comparativo honesto.** Selecionar 8–12 briefs heterogêneos e repetir baseline sem skill, Design OS e rival apropriada; medir funcionalidade, UX com pessoas, visual em viewport e regressões de negócio, com julgamento independente.
4. **Conectar dados reais somente com autorização.** Analytics/CRM, provedor de pagamentos, pesquisa de usuários, CI de app cliente e observabilidade; sem permissões ou ferramentas disponíveis, registrar bloqueio.
5. **Preservar fronteiras do produto.** O sistema é um orquestrador de qualidade visual/UX e experiência comercial, não uma autorização automática para operar uma empresa, fazer auditoria jurídica ou modificar infraestrutura crítica.

**Estado dos testes:** use a execução mais recente de GitHub Actions no PR #28; status de CI não foi fixado artificialmente neste documento. Um CI verde comprova apenas verificações que de fato foram realizadas. As comparações reais com outras skills permanecem NÃO_EXECUTADAS.
