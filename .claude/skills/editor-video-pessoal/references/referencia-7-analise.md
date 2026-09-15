# Referência 7 — YouTube 16:9 "O ChatGPT 6 editou esse vídeo INTEIRO" (Fernando Araújo)

Analisada em 11/09/2026. Arquivo: `referencia-7-youtube-fernando.mp4` (1920×1080, 25 fps, 5 min 51 s, 8.771 quadros).
Método: diferença entre TODOS os quadros consecutivos (54 cortes detectados), folhas de contato a cada 2 s + em cada corte,
sequências quadro a quadro nas transições, alinhamento de perfil horizontal para medir o deslocamento do apresentador,
amostragem de cor em resolução cheia, transcrição com faster-whisper (`referencia-7-transcricao.txt`).

**O usuário pediu "exatamente igual": mesma fonte, mesmas cores, mesmas animações.** Esta referência é 16:9 para YouTube,
não Reels vertical. As regras vigentes da skill (tela dividida em cima/embaixo, legenda SF Pro, verde) são de Reels e
**não se aplicam aqui**; este documento é a direção completa para o formato YouTube.

## 1. Estrutura geral

Quatro modos, sempre com corte seco entre eles (exceção: card claro → apresentador, ver §6):

| modo | o que é | tempo aprox. | duração típica de cada bloco |
|---|---|---|---|
| **talk** | apresentador em tela cheia, centrado, fundo preto de estúdio com spotlight azul-acinzentado atrás; chips pequenos flutuam ao lado | ~37 % | 3–10 s |
| **split** | apresentador desliza ~510 px para a esquerda; painel à direita (x ≈ 879 → 1920, 54 % da largura) claro `#F9F9F9` ou escuro `#050505` com título + widget de interface | ~45 % | 4–6 s |
| **card** | tela cheia clara `#FAFAFA` ou preta `#050505` com uma frase curta em caixa alta, ~150 px, centrada; às vezes um mini-diagrama abaixo | ~12 % | 1,5–5 s |
| **capítulo** | tela preta, "01 / 05" pequeno, "Primeira etapa" branco grande, "A ideia" amarelo abaixo, linha fina | ~6 % | 3,5–4 s |

Mais: b-roll P&B do próprio apresentador (mesa de montagem de filme, escrevendo no caderno, lendo livro, no computador),
sempre com lower-third "Fernando Araújo @fernandoaraujo" no canto inferior esquerdo. Cortes: 54 em 351 s ≈ um a cada 6,5 s.
Movimento médio entre quadros (escala 0–255, quadro inteiro): **2,99**.

**Não há legenda queimada em nenhum quadro.** Zero. A fala é sustentada pelos títulos dos painéis e pelos cards.

## 2. Tipografia

- **Outfit** (Google Fonts), peso Regular 400 para tudo que é texto grande. Identificada pela `a` de um andar, `ç` com
  gancho, `t` com cauda curva, `C/O` perfeitamente redondos, `M` de lados retos. Comparada no specimen do Google Fonts com
  "Primeira etapa · Motion com intenção · A EVOLUÇÃO". Disponível em `@remotion/google-fonts/Outfit`.
  Confirmar visualmente na primeira prévia; se divergir, a segunda candidata é Urbanist.
- Texto miúdo dos widgets: mesma família, Regular/Light, 16–22 px, cinza `#8A8A8A` sobre claro.
- Timestamps, código e "00:01:58:00": **monoespaçada** (tipo JetBrains Mono / SF Mono), branca, com relógio à esquerda.
- Rótulos pequenos como "01 / 05", "DA IDEIA AO RESULTADO", "DIRECIONAR O PRÓXIMO AJUSTE": caixa alta, ~14 px, tracking
  aberto (+0,15 em), cinza.

Tamanhos medidos (altura de maiúscula → corpo, Outfit tem cap-height ≈ 0,70 em):
- Card de frase só texto: caps 106 px → **corpo ≈ 150 px**, linha centrada verticalmente (caps de y 472 a 578 em 1080).
  Frase longa ("DIRECIONAMENTO") reduz para caps 88 px → corpo ≈ 125 px. Sempre cabe em uma linha.
- Card com diagrama abaixo: título sobe para y ≈ 195–300 (caps ~100 px → corpo ≈ 140 px), diagrama em y ≈ 550–690.
- Capítulo: "Primeira etapa" corpo ≈ 135 px, y 384–502; "A ideia" amarelo corpo ≈ 60 px em y ≈ 585–625; linha em y ≈ 709.
- Título do painel split: caps 44–62 px → **corpo ≈ 64 px**, centrado no painel, y ≈ 123–185.
- Chip flutuante: título 22–26 px, corpo 16–18 px.

## 3. Cores medidas

| uso | valor |
|---|---|
| fundo claro (card e painel) | `#FAFAFA` (250,250,250) |
| fundo preto (card, capítulo, painel escuro) | `#050505` |
| preto do estúdio ao redor do apresentador | `#030303` |
| texto sobre claro | `#131313` |
| texto sobre preto | `#FDFDFD` |
| **amarelo de destaque** | **`#F8C20E`** (248,194,14) — subtítulo do capítulo, badge "04", ponto no gráfico, botão de enviar, marcador da forma de onda |
| chip escuro | `#141414` com borda 1 px `rgba(255,255,255,0.08)`, raio 12–14 px |
| widget claro | branco `#FFFFFF` sobre `#FAFAFA`, borda 1 px `#E6E6E6`, raio 16 px, sombra quase nula |
| botão preto | `#111111`, texto branco, raio 12 px (quadrado) ou pílula |
| cinza de texto secundário | `#8A8A8A` |
| linha fina do capítulo | cinza `#3A3A3A` (base) e branco (a que desenha por cima) |

O amarelo é usado com **muita parcimônia**: um elemento por cena, nunca em área grande.
**Conflito com a regra 18 da skill (verde `#12CB87`, "nada de amarelo")** — o usuário pediu "mesmas cores" desta
referência. Perguntar antes de decidir; ver pendências no fim.

## 4. Apresentador

- Estúdio: fundo preto, spotlight circular azul-acinzentado atrás da cabeça, camiseta preta. Enquadramento médio,
  centrado (cabeça em x ≈ 960).
- **Em split, o vídeo do apresentador desliza para a esquerda ≈ 510 px** (26,5 % da largura), mesma escala (erro de
  alinhamento < 3 px, logo não há zoom). Medido quadro a quadro em duas transições:
  - entrada (49,0 → 49,9 s): 0 → −504 px em **22 quadros = 0,88 s**, ease-in-out simétrico (velocidade máxima no meio,
    incrementos por quadro: 4, 10, 10, 14, 20, 24, 32, 40, 48, 56, 52, 44, 36, 28, 24, 18, 12, 10, 8, 6, 4, 2).
    Sem overshoot mensurável (ruído do próprio apresentador é ±8 px).
  - saída (253,4 → 254,3 s): −518 → 0 px, mesma duração e mesma curva.
  - Aproximação em Remotion: `interpolate(frame, [0, 22*fps/25], [0, -510], {easing: Easing.inOut(Easing.quad)})`
    ou `Easing.bezier(0.45, 0, 0.2, 1)`.
- Chips flutuantes no modo talk **não** deslocam o apresentador: ficam sobre o preto ao lado (canto superior esquerdo,
  superior direito, ou inferior direito), com texto de rótulo curto abaixo/ao lado.

## 5. Como o texto entra

- **Palavra por palavra, pré-posicionada, aparecendo de uma vez (pop), sem fade nem escala.** Medido em "Primeira" →
  "Primeira etapa" (4 quadros entre uma e outra), "É" → "É A" (4 quadros), "EDIÇÃO" → "EDIÇÃO DINÂMICA", "Cada" → "Cada fala" →
  "Cada fala tem seu tempo", "Motion com" → "Motion com intenção", "Um" → "Um pedido não basta".
- A frase final é **centrada**; as palavras vão surgindo da esquerda para a direita nas posições finais ("PALAVRAS"
  começa em x = 210 tanto sozinha quanto em "PALAVRAS COM EFEITO"). Nunca há reflow nem recentragem.
- O ritmo das palavras acompanha a fala (uma palavra a cada ~4–6 quadros quando o apresentador fala rápido).
- O card entra **~0,2–0,5 s antes** da primeira palavra da frase falada (corte em 3,88 s para "edição" dita em ~4,3 s).

## 6. Transições medidas

| de → para | o que acontece | duração |
|---|---|---|
| talk ou split → card (claro ou preto) | **corte seco**; primeira palavra já na tela | 0 |
| card claro → talk | **dissolve** do card inteiro (fundo + texto escuro) sobre o apresentador; o chip seguinte já está lá desde o primeiro quadro do dissolve | 5 quadros = 0,20 s |
| card preto → talk | corte seco | 0 |
| talk → split | painel aparece de uma vez (fundo e título) e o apresentador desliza (§4); widget entra com fade curto | painel 0; slide 0,88 s |
| split (painel escuro) → split (painel claro) | fundo do painel troca em 1–2 quadros; widget antigo **cresce ~5 % e some em fade** enquanto o novo já está na posição, em fade de entrada; título troca em pop | ~6 quadros = 0,24 s |
| split → talk com chip | fundo do painel some em **1 quadro** (corte); widget faz fade + leve escala para cima em ~6 quadros; chip novo aparece em fade de ~4 quadros; apresentador desliza de volta em 0,88 s | 0,24 s + slide |
| card → capítulo | corte seco; título já na tela | 0 |

Regra geral: **fundos trocam por corte; conteúdo sai por fade curto com leve escala; o único movimento longo é o slide
do apresentador.**

## 7. Capítulo (quadro a quadro, f1590–f1620)

1. Corte seco do card anterior para preto. "Primeira" já visível no quadro 1, "01 / 05" em cinza acima.
2. "etapa" aparece no quadro 5 (pop).
3. Linha cinza fina (1 px, ~150 px de largura, centrada) já existe desde o começo.
4. A partir do quadro ~14 (0,56 s), uma linha branca **desenha da esquerda para a direita** por cima da cinza, em ~10
   quadros (0,4 s), ease-out.
5. O subtítulo amarelo ("A ideia") entra em pop quando a palavra é dita, ~1,3 s depois.
6. Dura 3,5–4 s e corta seco para o próximo modo.

## 8. Painel split e widgets

- Painel ocupa x 879–1920. Título Outfit ~64 px centrado no painel (y ≈ 150). Widget centrado abaixo (y ≈ 260–800),
  largura ~640 px, raio 16 px.
- Widgets vistos (cada um é a **metáfora literal da fala**, reconstruído como interface, nunca screenshot real):
  caixa de prompt do ChatGPT (logo acima, campo com cursor piscando, botão de enviar ↑ preto ou amarelo, texto digitado
  letra a letra), checklist com itens marcando ✓ um a um, barras "Tempo / Tokens" preenchendo, contador "01 → 03"
  com barras crescendo, tabela de timestamps com linha destacada, lista de arquivos com ✓, fluxo `video.mp4 +
  timestamp.txt → logo GPT`, cartão "Sua ideia em vídeo." com botão "VER RESULTADO", editor de código com prévia,
  curva de easing com ponto amarelo, forma de onda com cursor, "Duração 20 s / 30 s / 4 min" com barra, botão "Deixa o
  like 👍 1 LIKE" com cursor clicando, "INSCREVA-SE" virando "✓ INSCRITO", caixa de comentário sendo digitada.
- Micro-animação dentro do widget o tempo inteiro (digitação, ✓, barras, cursor de mouse que se move e clica). Isso é
  o que mantém a tela viva; o widget em si não flutua nem deriva.
- Cursor de mouse desenhado (seta branca com contorno preto) aparece em vários widgets e realmente "clica".

## 9. Chips no modo talk

Cartão pequeno (~300×110 px) escuro `#141414`, raio 12 px, 1 px de borda sutil, no canto superior esquerdo ou direito,
a ~60 px da borda. Conteúdo: ícone + rótulo curto ("A ferramenta", "Aprendizado", "Dentro do projeto", "2026" em
calendário, "Seu tempo · Direção com IA", "Se cuidar"). Entra em fade de ~4 quadros; o rótulo em texto abaixo entra
em pop palavra por palavra. Lower-third do Instagram no b-roll: cartão claro, avatar, nome em negrito, @ em cinza.
CTA final: cartão escuro no canto inferior direito "Aprenda a editar vídeos com IA" com botão.

## 10. O que reproduzir no Remotion (resumo operacional)

1. Composição 1920×1080. Fonte Outfit via `@remotion/google-fonts/Outfit` (Regular; SemiBold só em "Sua ideia em
   vídeo." e botões). Mono para timestamps.
2. Vídeo do apresentador em tela cheia, sem máscara, sem borda. `translateX` animado 0 ↔ −510 px em 0,88 s ease-in-out
   quando entra/sai do split.
3. Cinco componentes: `Card` (claro/preto, frase caixa alta ~150 px, palavras pré-posicionadas em pop, opcional
   diagrama), `Capitulo` (número, título, subtítulo amarelo, linha que desenha), `Painel` (claro/escuro, título 64 px +
   widget), `Chip` (canto, ícone + rótulo), `LowerThird`.
4. Transições: corte seco por padrão; dissolve de 5 quadros só de card claro para talk; fade + escala 1,05 de 6 quadros
   para widget saindo.
5. Texto sincronizado com a fala pela legenda (SRT) — cada palavra do título aparece no timestamp da palavra dita.
6. Sem legenda queimada.

## Pendências para o usuário decidir

1. **Amarelo `#F8C20E` (referência) ou verde `#12CB87` (regra da skill)?** "Mesmas cores" aponta para o amarelo.
2. **Sem legenda**, como na referência? A regra 9–12 da skill (SF Pro) é de Reels.
3. B-roll P&B do apresentador não existe no material dele; sem isso, esses trechos viram talk + chip ou card.
4. Formato: 16:9 para YouTube confirmado? (Bruto dele costuma ser vertical de selfie.)
