# Referência 5 — fluidez, parte 2 (enviada em 09/09/2026, à noite)

Arquivo: `referencia-5-fluidez-2.mp4` (720x1280, 41 s, 25 fps). Mesmo criador das Referências 1 e 4. O usuário mandou junto quatro decisões novas (abaixo, em "Decisões do usuário") e pediu para **não criar nada ainda, só salvar**.

## O que a referência faz (observado em quadros consecutivos)

### Fluidez vem de "vida interna", não de efeitos de entrada
- Os elementos gráficos **já estão na tela quando a cena começa**. Nada "pula" para dentro. O que anima é: as palavras acendendo, e os recortes derivando devagar e sem parar (o braço com celular muda de posição a cada quadro, bem pouco).
- A troca entre cenas é corte seco entre composições completas. A sensação de fluidez vem do movimento contínuo dentro da cena, não de transições elaboradas.
- Palavras: surgem apagadas (cinza) e acendem para branco/preto ou para a cor de destaque na hora em que são faladas. Posições fixas, sem reflow. Igual à Ref. 4.
- Um cronômetro em anel ("01.4s") preenche progressivamente: exemplo de micro-animação funcional, não decorativa.

### Recortes fotográficos ("stickers")
- Fotos reais em **preto e branco**, recortadas, com **contorno branco grosso** em volta (efeito adesivo). Mão segurando celular, olho, bússola, mão com crachá.
- Ocupam a tela inteira (abertura) ou um lado da área superior (layout dividido), com o texto do outro lado.
- Derivam continuamente (poucos pixels, senoidal).
- Técnica reproduzível com fotos reais baixadas: converter para P&B, recortar/mascarar, adicionar contorno branco, animar deriva.

### Layout dividido e legenda (`referencia-5-layout-legenda.png`)
- Divisória: linha fina clara entre a área gráfica (em cima) e o apresentador (embaixo).
- **A legenda fica numa caixa centrada exatamente sobre a divisória**, metade sobre cada área. Caixa creme, texto preto, palavra ativa em negrito e sublinhada. Legenda pequena: caixa ≈ 4,7% da altura do quadro, texto ≈ 2,2% da altura (≈ 42 px em 1920).
- Ilustrações pequenas de interface (chip "AI", quadradinhos, "?") desenhadas em traço, em cima do texto nas cenas cheias.

### Paleta da referência
Preto, creme `#F2EEE4`, amarelo. **Para os vídeos do usuário, o amarelo é substituído pelo verde abaixo.**

## Decisões do usuário (09/09/2026, à noite) — valem a partir do próximo vídeo
1. **Começar sempre em tela dividida.** O título de abertura fica **no meio da tela dividida, sobre a divisória**, não sobre o apresentador em tela cheia. Continua sem efeito de entrada e saída, branco, Helvetica Bold, traçado fino.
2. **Legenda principal centrada na divisória**, no meio das duas áreas, **um pouco menor** do que a atual (atual: corpo 80 px; passar para ~64-68 px). Fonte e cor seguem: Helvetica Bold, branca, traçado fino.
3. **Cores das animações: branco, preto e verde `#12CB87`** no lugar do amarelo. O creme pode continuar como fundo claro se fizer sentido; o destaque, marcadores, chips, barra de progresso e palavras-chave passam a ser verdes.
4. **Animações mais fluidas**, no espírito desta referência: elementos já presentes na cena, deriva contínua, palavras acendendo, sem entradas bruscas.

## Decidido pelo usuário (09/09/2026, à noite)
- **Legenda sem caixa.** Fica como hoje: Helvetica Bold branca com traçado fino, só que centrada sobre a divisória e um pouco menor.
- **Fundo creme pode ser usado, se combinar.** Não é obrigatório; o critério é a cena ficar bonita com branco, preto e verde `#12CB87`.

---

# Segunda leitura (09/09/2026, à noite) — sincronismo e por que os gráficos são bonitos

O usuário reenviou esta referência: "as animações bem fluidas, exatamente no tempo que ele fala... quando entra animação tela cheia, não precisa de transição dissolver, deixe mais seco... as animações dele estão bem mais bonitas."

## Sincronismo medido (15 trocas de cena x transcrição com tempo por palavra)
As trocas caem em: 2,52 · 4,2 · 6,8 · 9,8 · 12,64 · 15,24 · 18,88 · 20,88 · 23,4 · 26,72 · 28,88 · 30,16 · 32,84 · 36,04 · 37,68.

Comparando com o início de cada frase falada, o padrão é claro: **a cena troca de 0,10 a 0,30 s ANTES da primeira palavra da frase nova**, média ≈ 0,20 s (6 quadros a 30 fps). Nunca depois. É o que faz parecer "exatamente no tempo": a imagem chega primeiro, a voz confirma.
- 12,64 → "só que a nossa atenção" começa em 12,80 (0,16 antes)
- 18,88 → "porque tudo o que aparece" em 19,10 (0,22 antes)
- 32,84 → "porque em uma internet" em 33,10 (0,26 antes)
Ritmo: 15 cenas em 41 s, uma a cada 2,7 s.

**Regra**: cortar a cena 0,20 s antes do início da frase, não na palavra.

## Transição: corte seco
Não há dissolve em lugar nenhum, e o usuário pediu isso explicitamente para as entradas em tela cheia. **Trocar `XF` (crossfade) por corte seco**, pelo menos nas cenas de tela cheia. A sensação de fluidez não vem da transição: vem do movimento contínuo dentro da cena.

## Por que os gráficos são bonitos (ver `referencia-5-graficos-1.png` e `-2.png`)
1. **Metáfora literal da frase, nunca decoração.**
   - "produzir conteúdo em escala nunca vista" → esteira de fábrica cuspindo cards de post
   - "a nossa atenção continua limitada" → um olho gigante com um cronômetro pendurado nele
   - "ocupa segundos da sua vida" → anel de cronômetro marcando 01.4s, preenchendo em verde/amarelo
   - "pode ser extremamente cansativa" → mão segurando celular apagado
   - "essa pessoa está me levando pra onde?" → mão segurando uma bússola
   - "o conteúdo vai ser infinito" → celular derramando um rolo de filme sem fim
2. **Recorte fotográfico em P&B com contorno branco grosso** (efeito adesivo), com sombra suave por baixo.
3. **Mistura foto recortada + elemento vetorial limpo** (os cards de Instagram na esteira, o anel do cronômetro). É essa mistura que tira o ar de banco de imagens.
4. **Composição de dois objetos** para formar a cena (olho + cronômetro; celular + rolo de filme). Não é uma foto solta.
5. **Muito preto negativo. Poucos elementos e grandes.** Uma ilustração + um bloco de texto de 2-3 linhas do lado oposto. Nunca lotado.
6. **A ilustração invade a divisória**, passando por cima da faixa da legenda. Dá profundidade e amarra as duas metades.

## Como reproduzir (testado, funciona)
`work/sticker.py` faz o recorte: alpha do PNG quando existe, senão máscara por fundo liso, senão GrabCut do OpenCV; depois converte para P&B com contraste, aplica contorno branco e sombra. Testado em `work/teste-sticker/` com fotos reais baixadas — o resultado sai igual ao da referência quando a foto tem fundo limpo.
**Ao buscar imagem, priorizar**: PNG com transparência, ou foto de objeto em fundo liso/branco. Fundo confuso dá borda irregular.


---

# Terceira leitura (10/09/2026) — medição das curvas de movimento

O usuário reenviou o mesmo arquivo (MD5 idêntico) pedindo treino em animação e movimento.
Em vez de repetir, medi o que faltava: as curvas, quadro a quadro.

## CORREÇÃO IMPORTANTE: os gráficos NÃO derivam
Eu tinha escrito que "os recortes flutuam o tempo todo, deriva senoidal, leve rotação, respiração
de escala — nada fica parado". **Isso está errado.** Tirei essa conclusão olhando tiras de quadros
e confundindo ruído de compressão com movimento.

Medindo a caixa dos elementos quadro a quadro, em três cenas diferentes:

| elemento | variação de largura | variação de cx | variação de cy |
|---|---|---|---|
| mão com celular (0–2,5 s) | 0 px | 3 px | 0 px |
| olho + cronômetro (12,7–15,2 s) | 0 px | 0 px | 0 px |
| bússola (33–35,9 s) | 0 px | 0 px | 0 px |
| celular + filme (34,2–36 s) | 0 px | 0 px | 0 px |

Depois de entrar, **o elemento fica completamente parado**. Zero pixel de variação.

## A entrada é uma revelação de baixo para cima
O que dá vida é só a entrada, e ela tem uma mecânica específica:

| t (s) | topo | base | altura |
|---|---|---|---|
| 0,00–0,12 | 493 | 999 | 506 |
| 0,16 | 480 | 999 | 519 |
| 0,24 | 431 | 999 | 568 |
| 0,32 | 396 | 999 | 603 |
| 0,40 | 381 | 999 | 618 |
| 0,48 | 376 | 999 | 623 |
| 0,52+ | 376 | 999 | 623 |

**A base fica fixa em 999 o tempo inteiro. Só o topo sobe.** Ou seja: não é escala, não é fade,
não é slide. O elemento é **revelado para cima a partir de uma linha de base fixa**, como uma
máscara abrindo.

Parâmetros: **0,16 s de espera** depois do corte, depois **0,32 s de movimento** com
**ease-out cúbico** (aos 50% do tempo já andou 83% do caminho). Sem overshoot, sem quique.

## O que realmente cria a sensação de fluidez
1. A revelação de baixo para cima, 0,32 s, ease-out.
2. As palavras acendendo do cinza no tempo da fala.
3. A cena trocando a cada ~2,7 s, sempre 0,20 s antes da frase.
4. O movimento natural do próprio apresentador.
**Não** é deriva contínua. Elemento parado depois de entrar é o correto.
