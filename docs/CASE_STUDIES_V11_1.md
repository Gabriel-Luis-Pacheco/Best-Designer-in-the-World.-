# V11.1 — estudos de caso de aplicação e limites

Este pacote tem três superfícies de aprendizado, NÃO três cases premiados. Cada exemplo deve ser julgado no navegador, nunca pelo sucesso de um checklist isolado.

## 1. ConversaBoa — oferta comercial fictícia
- Arquivos: `examples/conversaboa-concept.html` e `examples/conversaboa-editorial-alternative.html`.
- Propósito: mostrar método pedagógico e ação possível, sem transformar todas as seções em blocos de texto ou prometer IA/voz inexistente.
- Duas direções espaciais materialmente distintas: cena conversacional versus caderno editorial.
- Testes: estados do diálogo, teclado, mobile, informações comerciais fictícias.
- Limitações: arte e copy ainda carecem de testes com usuários reais; não há serviço nem vendas.

## 2. VESPER — experiência artística fictícia
- Arquivo: `examples/vesper-sculptural-light-study.html`.
- Propósito: trabalhar assinatura formal/material/comportamental, transformação entre cenas e clímax que responde à escolha.
- Testes: 390px/1440px, interação e reset, reduced motion, captura por frames.
- Limitações: peça experimental CSS/JS, não produto real, benchmark profissional ou visualização fisicamente realista; movimento/acabamento ainda podem ser criticados.

## 3. Ledger — sistema operacional fictício
- Arquivo: `examples/ledger-operational-dashboard.html`.
- Propósito: demonstração de UX para tarefas de conferência, leitura densa, estado, busca, filtragem, exportação local e clareza de origem.
- Testes: valores derivados de dataset simulado, filtros, busca, CSV, mobile com rolagem horizontal interna da tabela, teclado.
- Limitações: **sem backend, importação fiscal, autenticação ou persistência**; exportação é apenas dos dados fictícios exibidos. Não reutilizar nomes/valores em produção.

## O que aplicar num projeto real
1. Inspecionar o produto/código/brand canon antes de desenhar.
2. Escolher se a prioridade é compreensão/ação, expressão artística ou fluxo operacional.
3. Avaliar toda a página/tarefa, não só hero.
4. Corrigir o elo fraco em código e capturar depois.
5. Não exigir 3D em dashboard nem converter arte em funil de vendas.
6. Registrar QA técnico e crítica visual separadamente.

**Pendente:** teste real de agentes com e sem skill, mesmo modelo/brief/ferramentas/orçamento, projetos completos, leitura da skill comprovada e avaliação cega humana. Os exemplos são material de desenvolvimento, não prova de vitória.
