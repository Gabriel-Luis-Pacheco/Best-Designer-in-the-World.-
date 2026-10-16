# Tipografia, composição e acabamento — roteiro executável

## Antes dos tokens
Defina ordem de leitura e linha dominante de atenção. Com palavras reais, teste título curto, longo e quebrado. Não aprove comp apenas com lorem ipsum. Marque landmarks, hierarquia semântica e idioma. Fonte é voz, não troféu; licença e carregamento importam.

## Construir hierarquia
- **Escala:** distinguir título, subtítulo, seção, corpo e legenda por função; usar 2–3 saltos significativos em vez de oito pesos parecidos.
- **Ritmo:** alternar trecho compacto de prova, trecho expressivo e pausa. Vazio precisa organizar atenção; vazio recorrente sem intenção transmite conteúdo ausente.
- **Largura:** controlar comprimento de linha para leitura confortável; ajustar segundo família, tamanho, idioma e dispositivo, não por uma fórmula universal.
- **Quebra:** validar títulos em 320, 390, 768 e 1440 px; evitar órfãs e cortes, sem impor `white-space: nowrap` como remendo.
- **Relação:** um visual pode sustentar o texto, ou o texto pode ser o protagonista, mas evite competição entre duas estrelas iguais.

## Gramática de composição
1. Traçar eixo de alinhamento primário, áreas de densidade e espaço de respiro.
2. Definir como cada tipo de evidência ocupa o grid: ilustração livre, screenshot de interface, tabela, depoimento verificado, texto.
3. Decidir quando quebrar o grid: quebra deve realçar significado, não apenas parecer "criativa".
4. Fazer miniatura (squint): o olhar descobre começo, transição e chegada sem precisar ler?
5. Comparar micro e macro: tooltip refinado não compensa seção inteira perdida; reestruturação macro antecede alinhamento óptico.

## Revisão óptica deliberada
Alinhamento geométrico nem sempre parece alinhamento visual: triângulos, círculos, formas irregulares e letras com curvas exigem ajustes pequenos. Verificar direção de ícones, baseline de texto, peso percebido, crop de fotos, contraste aparente, stroke e sombras em escalas reais. Registrar o motivo para exceções aos tokens, em vez de espalhar valores mágicos.

## Verificações reproduzíveis
Com viewport fixa, inspecionar heading em 3 comprimentos; textos de botão longos; zoom 200%; idioma expansivo; foco visível; alto contraste; modo redução de movimento; performance da fonte (fallback e layout shift). Se a fonte customizada não carregar, conteúdo e hierarquia devem continuar utilizáveis.

## Erros típicos e correção
- **Tudo igual:** variar escala e meio segundo a importância, não aleatoriamente.
- **Tudo gigante:** manter informação primária perto da tarefa e revelar detalhes quando útil.
- **Tudo elegante porém fraco:** testar contraste e leitura em tela real, não apenas mockup estático.
- **Todos os cantos iguais por token rígido:** manter consistência de família e ajustar onde o conteúdo demanda.
- **Cada seção de uma marca:** retornar às regras de cor, imagem, tipografia e motion antes de inventar nova solução.
