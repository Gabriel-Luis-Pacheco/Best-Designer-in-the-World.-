# Comparação profunda: Design OS V6.1 → v7

O que V6.1 já tinha: autópsia da página inteira; estratégia de reconstrução radical; pesquisa de referências e concorrentes; coerência entre seções; Tato/mascotes canônicos; narrativa visual; conversão honesta; QA adversarial; indicação de Playwright; referências de UX, performance, a11y e sistemas internos.

## Lacunas identificadas e decisões

| Tema | V6.1 | Nova adoção v7 | Prova requerida |
|---|---|---|---|
| Extração de design system | Inventário genérico | `DESIGN.md` com tokens medidos, inventário de padrões e fonte de verdade | Screenshot/código e rastreio de fonte |
| Avaliação da própria skill | Não havia harness estruturado de casos | `evals/evals.json` e A/B cego | outputs com e sem skill + revisão |
| Critério visual | Pior elo qualitativo | Rubrica por dimensão + bloqueio P0/P1 independente da nota | screenshot global e anotação por região |
| Benchmark | Galeria e concorrentes | Planilha de **mecanismo → adequação → evidência → decisão** | URL e data, não copiar |
| Teste de regres. | Captura/manual | Receita Playwright snapshots + checagens de fluxo | artefatos reprodutíveis |
| Brand fidelity | Falar sobre canon | Matriz de traços invariáveis e prova de proveniência | arquivo original e comparativo |
| Engenharia | Regras amplas | Composição de componentes, estados e performance por impacto | build e testes específicos |
| Conteúdo | Cortar texto | Informação necessária vs dispensável; sem cards-reembalados | primeiro olhar + leitura sob demanda |
| Pesquisa com usuários | Objetivo implícito | hipóteses e tarefas de compreensão, não validação simulada | resultados reais |
| Segurança de skills | Alerta básico | fonte/licença, web como dados, código externo sob revisão | matriz com direitos/risco |
| Governança | Várias versões/histórico | skill única + referências sob demanda; versões via Git | CI de estrutura e changelog |
| Marketing x dashboard | já separado | rotas de avaliação com rubricas diferentes | task success no sistema |

## O que NÃO foi importado
- Textos integrais, código e ilustrações de skills de terceiros: licenças variáveis e risco de plágio.
- Design trends aplicadas indiscriminadamente: tendências não são identidade de marca.
- Regras arbitrárias como “máximo 100 palavras por seção”: podem esconder informação essencial.
- Nota estética calculada por pixels/computador: não é válida sem julgamento contextual.
- Instalação automática de plugins ou scripts externos: risco de segurança.
- Forçar Figma, Stitch, Storybook ou React em todos os projetos: são ferramentas opcionais.

## Critério de melhoria verificável
V7 só pode ser chamada superior à V6.1 quando rodarmos os mesmos prompts reais, repetidos nas mesmas condições, e tivermos evidência de maior qualidade e menos falhas em revisões cegas. A documentação por si não comprova ganho.
