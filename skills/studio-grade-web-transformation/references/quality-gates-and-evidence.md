# Gates operacionais e registro de evidências

## Níveis de evidência
**E0 — Proposta:** raciocínio sem execução. **E1 — Inspeção:** código/assets/screenshot vistos. **E2 — Execução local:** build, browser, testes reproduzíveis. **E3 — Observação humana:** uso real documentado, com perfil/tarefa e limites. **E4 — Resultado de produto:** métricas em ambiente real com coleta válida.
Não converter E0/E1 em E3/E4. Para cada afirmação de aprovação, anexar o nível disponível, localização do artefato, data, ambiente e responsável.

## Gates
- **Verdade:** preços, limites, alegações, assets e destinos críticos preservados? P0 para afirmação comercial falsa.
- **Funcionamento:** cadastro, checkout, formulários, navegação e estado de erro testados no ambiente adequado?
- **Acessibilidade:** nomes acessíveis, foco visível, controle por teclado, fluxo sem armadilhas, zoom/reflow e reduced motion; ferramenta automática é apoio.
- **Visual:** página completa desktop/mobile, consistência entre cenas, pior seção, estados e crop.
- **Desempenho:** medir em condição reproduzível; nunca atribuir LCP/CLS/INP com base em impressão.
- **Regressão:** comparar baseline aprovado, não aceitar snapshot novo automaticamente.

## Severidade com fundamento
P0 = fluxo central indisponível, perda de dados, falsidade ou barreira crítica comprovada.
P1 = impede de maneira séria objetivo ou entendimento, identidade canônica alterada, dispositivo-chave impraticável.
P2 = refinamento local, desconforto sem prejuízo relevante.
Cada defeito: **passos → evidência → impacto → hipótese causal → correção → reteste**.
A nota subjetiva de beleza nunca se sobrepõe ao funcionamento; preferências individuais não são blocker sem justificativa.

## Modelo de relatório mínimo
`ID | gate | resultado PASS/FAIL/UNKNOWN | evidência | ambiente | próxima ação`. `UNKNOWN` nunca passa. Uma execução parcial não é conclusão total.

## Falha de ferramenta
Se screenshot/browser indisponível, NÃO VERIFICADO para visual e interação. Pode entregar código e descrever testes estáticos reais, mas não declarar qualidade final validada.
