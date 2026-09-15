# PADRÃO REELS 2 (estilo atual do usuário) — medido em 15/09/2026

Três vídeos editados por ele no Premiere: "Meta demitiu 8 mil" (1:33), "Anúncios dentro do ChatGPT" (1:33), "O Google mudou" (1:51). Pedido: "quero exatamente igual". Este é o padrão vigente de Reels; o estilo antigo (referências 1–7, verde, lettering em tela cheia) fica como histórico.

## Estrutura

| Trecho | Layout |
|---|---|
| 0 até ~60 % do vídeo (56 s / 67 s / 62 s) | **Tela dividida do primeiro quadro**: em cima material real, embaixo o apresentador. **Sem título de abertura.** Legenda começa junto com a fala. |
| Transição | **Flash quente (light leak laranja/amarelo), ~0,37 s = 11 quadros**: 4 quadros subindo sobre a dividida, corte pra tela cheia por baixo do clarão no 5º, 6 quadros descendo. Pico de brilho médio 234/255. (O vídeo 2 usa corte seco; o flash é o padrão.) |
| ~60 % até o fim | **Apresentador em tela cheia**, é a parte do argumento final e da chamada. |

Divisória em **y = 899** (área de cima 0–899, de baixo 899–1920). Sem linha.

## Área de cima: imagens e vídeos reais, o tempo todo

Palavras dele: "em cima é tudo imagens e vídeos trazendo referências do que tá sendo falado, normalmente pego do TikTok, YouTube, enfim, do que tiver algo chamativo e interessante".

- Vídeo de notícia (coletiva, pessoa citada), print da matéria (g1, TechCrunch), logo/produto em close, gravação de tela (site, painel de anúncios) com o dedo apontando, foto da pessoa.
- Ritmo: vídeo 1 = 33 cortes em 57 s (a cada ~1,7 s, em rajadas); vídeo 3 = 23 em 62 s (~2,7 s); vídeo 2 = 7 em 67 s (gravações de tela longas, que já têm movimento). Regra: **trocar a cada 2–3 s, ou deixar um clipe longo só se ele tiver movimento próprio**.
- Material preenche a área inteira (cover), sem moldura, sem crédito na tela.
- **Card de destaque** (número/frase): fundo off-white **#F2F2F2**, texto **#010101**, TikTok Sans, centrado. Medido: frase em 2 linhas com ~72 px (linhas em y 371–445 e 464–525), número "8.000" com ~270 px Bold (y 322–516, larg 687) e subtítulo "10% da empresa" ~72 px. Card fica só na área de cima.

## Legenda (Premiere: TikTok Sans, Medium, tamanho 55, tracking −30, centralizada)

- Em pixels (1080x1920): **TikTok Sans wght 500, ~59 px, tracking −30/1000 em** ("toda empresa" mede 340 px de largura, 54 px de ascendente a descendente). Branca, sombra suave, sem caixa.
- **Na dividida: centrada exatamente sobre a divisória** (y 871–924, centro ≈ 897).
- **Na tela cheia: centro em y ≈ 1113 (58 % da altura)**, logo abaixo do queixo.
- Blocos **muito curtos, 1–3 palavras**, troca inteira: 114 / 121 / 73 trocas, **mediana 0,67 s por bloco**. Quebra por unidade de sentido (regra dele).

## Apresentador

Selfie de celular, tela cheia fechada como nos criativos (rosto grande). Jump cuts entre takes. Sem zoom punch.

## Como reproduzir

1. Preparar como criativo (`work/criativo_prep.py`): corte de respiros, transcrição do áudio cortado, rosto.
2. Buscar material real pra área de cima (notícia, produto, pessoa citada, gravação de tela). **Eu procuro o material por conta** (ele confirmou em 15/09), como nas referências: notícia sobre o assunto, vídeo da pessoa citada, print do produto. Download: `work/baixar.py URL pasta [ini fim] [nome]` (yt-dlp instalado em `ferramentas/pydeps`, pega h264 ≤1080p com áudio, baixa só o trecho). **Sem música de fundo.**
3. Renderizar com o modo `reels2` de `work/criativo.py` (a implementar): dividida até o ponto marcado (`t_cheia`), material em lista com tempos, flash na virada, legenda 59 px wght 500 tracking −30 na divisória / em 58 % na cheia, blocos de ~0,7 s.

Imagens: `reels-2-quadros-*.png`, `reels-2-dividida.png`, `reels-2-tela-cheia.png`, `reels-2-legenda-divisoria.png`, `reels-2-cards.png`, `reels-2-flash.png`. Vídeo: `reels-2-referencia-meta.mp4`.
