# PADRÃO CRIATIVOS (anúncios) — medido em 15/09/2026

Padrão SEPARADO do estilo dos Reels (Referências 1–7). O usuário pediu: "quero criar um padrão de edição pra criativos... copia exatamente igual". Fonte informada por ele: **TikTok Sans**.

Referência: `criativos-1-referencia.mp4` (1080x1920, 29,97 fps, 1:21, veio sem áudio). Apresentador em estúdio escuro com luz âmbar, camiseta preta, microfone.

## Duas variantes — PERGUNTAR ANTES DE CADA EDIÇÃO (pedido em 15/09/2026)

- **Dividida** (a da referência): gancho de ~4 s em tela dividida com material real embaixo, título na divisória, corte seco pra tela cheia, cutaways em dividida.
- **Inteira**: tela cheia do primeiro quadro ao fim, sem material embaixo, sem cutaway. Título e legenda iguais. (`variante="inteira"` no config; confirmar com ele se o título entra.)

O usuário quer ser perguntado sempre: "essa leva é dividida ou inteira?" antes de começar. Se ele não disser no pedido, perguntar antes de editar — é a exceção à regra de não fazer perguntas.

## Estrutura (tempos da referência)

| Trecho | Layout | O que aparece |
|---|---|---|
| 0,00–3,70 s | **Tela dividida** (apresentador em cima, divisória em ~y 960) | Em baixo, clipes de notícia reais (Lula em Itaipu, Jornal da Band, câmeras). Corte seco a cada ~0,6–1,3 s: 0,47 / 1,10 / 1,67 / 2,44 / 3,70. |
| 0,00–9,80 s | Título | **Título do gancho centrado na divisória**, já começa na tela, sem animação. Some de uma vez em 9,8 s. |
| 3,70 s | Corte seco | Sai a dividida, entra **apresentador em tela cheia**; o título continua no MESMO lugar (y ≈ 940). |
| 9,80–81 s | Tela cheia | Só apresentador + legenda. Título e legenda nunca convivem. |
| 48,55–50,62 s | Cutaway em dividida | Apresentador em cima (enquadramento mais aberto), em baixo vídeo de tela (ChatGPT 48,55–48,98; editor de código 48,98–50,62). Corte seco entrando e saindo. Legenda continua no mesmo y, por cima do vídeo de baixo. |

Cortes no trecho de tela cheia: **jump cuts** simples entre takes (9,8 / 15,5 / 21,8 / 32,6 / 36,3 / 58,2 / 65,8 / 78,6 / 79,6 s). **Não há zoom punch, não há Ken Burns**: a variação de tamanho do rosto é o próprio apresentador se movendo. Enquadramento tela cheia bem fechado: rosto com ~55–65% da largura do quadro, olhos em ~30% da altura.

## Título do gancho

- TikTok Sans **Bold (wght 700)**, **64 px**, branco, **2 linhas**, centrado em x = 540.
- Linhas em y 875–934 e 945–1004 (passo de 70 px). Bloco centrado em y ≈ 940, exatamente sobre a divisória.
- Sombra escura suave (sem caixa, sem contorno).
- Texto da referência: "Algo está acontecendo no / Brasil e ninguém está vendo".

## Legenda

- TikTok Sans **SemiBold/Bold (wght ~650)**, **~51 px** ("tá sendo um ano difícil," mede 521 px de largura, 52 px de ascendente a descendente).
- Branco, **sem caixa, sem contorno**, sombra escura suave.
- **Centrada em x = 540, baseline em y ≈ 1218** (topo do texto em 1178). Fica em ~63% da altura, abaixo do queixo, não em cima da boca. Mesma posição em tela cheia e no cutaway dividido.
- **Uma linha só, 1 a 4 palavras**, caixa normal de frase, pontuação mantida ("vê nos comentários,", "do que uma agência cobra.", "Fechado?").
- **Troca inteira, sem animação**: 73 blocos em 81 s, intervalo mediano **1,03 s** (mín 0,17, máx 7,4 no gancho). Sem palavra por palavra, sem destaque de cor, sem fade.

## Quebra dos blocos de legenda (regra do usuário, 15/09/2026)

Cada bloco é uma **unidade de sentido** completa, nunca um pedaço arbitrário de N palavras. Cortar onde a fala respira: entre sujeito e ação, antes de conector ("enquanto", "que", "e"), antes de complemento longo. Nunca separar artigo/preposição/adjetivo da palavra que acompanham ("a chuva fina" fica junto; "cobria as / ruas" não). Ponto final e vírgula fecham o bloco: nunca começar frase nova no meio de um bloco ("ruas. No café da" é errado).

BOM: `A cidade` / `despertava lentamente` / `enquanto a chuva fina` / `cobria as ruas.` / `No café da esquina,` / `pessoas conversavam` / `sobre planos,` / `viagens e problemas` / `que pareciam enormes` / `naquela manhã.` / `Um cachorro` / `observava tudo` / `pela janela,` / `esperando seu dono` / `terminar o café.`

RUIM: `A cidade despertava` / `lentamente enquanto a` / `chuva fina cobria as` / `ruas. No café da` / `esquina, pessoas` / `conversavam sobre` / `planos, viagens e` / `problemas que` / `pareciam enormes naquela` / `manhã. Um cachorro` ...

## Três formatos por vídeo (implementado em 15/09/2026 em `work/criativo.py`)

Todo criativo sai em **RL 1080x1920**, **IN 1080x1350** e **GL 1080x1080** (`--formatos IN,GL`). Mesma largura, então título 64 px e legenda 51 px não mudam. O que muda por formato:

| | RL | IN | GL |
|---|---|---|---|
| divisória | 960 | 675 | 600 (faixa de cima maior p/ a cabeça caber) |
| legenda (baseline) | 63,4 % da altura = 1218 | 856 | 685 |
| tela cheia | zoom do config, face_at 0,33 | zoom x0,95, face_at 0,34 | zoom x0,85, face_at 0,34 |
| dividida (rosto) | face_at 0,44 | 0,47 | 0,50 |
| cutaway | material encosta na divisória, legenda cai por cima com gradiente | material recuado 200 px, legenda em faixa preta | recuado 120 px |

Comando: `PYTHONPATH=ferramentas/pydeps:ferramentas/cvdeps $PY work/cN/cN.py --formatos IN,GL` (sem flag = RL). Config por vídeo em `work/cN/cN.py`; preparação (corte, transcrição, rosto) em `work/criativo_prep.py`.

## Entrega (15/09/2026) — só depois da aprovação do usuário

Fluxo fechado com ele: **edito → mando pra aprovar → ele aprova → aí entrego nos dois lugares**. Nunca subir pro portal antes do "aprovado".

1. **SSD**: `/Volumes/SSD Ruan/Criativos/<pasta da gravação>/<título>/<título> - RL|IN|GL.mp4` (ExFAT: sem `?`, `:`, `/`, `*` no nome).
2. **Portal** (https://conteudoextremo.conversaoextrema.com):
   - `python work/portal.py cadastrar "Título"` (Editado / Ruan / data / Perpétuo) — pular se ele já cadastrou à mão (`listar` antes).
   - `python work/portal_upload.py "Título" RL.mp4 IN.mp4 GL.mp4` — sobe os 3 como anexos da linha e põe a URL do RL em Arquivo Finalizado.
   Detalhes técnicos na memória `portal-conteudo-extremo`.

## Cores e clima

Preto/branco só. Nenhuma cor de destaque, nenhum grafismo, nenhum lettering em tela cheia. O que segura é o rosto grande, a legenda curta e o ritmo de troca.

## Como reproduzir

1. Cortar respiros (`work/cortar_silencios.py`, detector relativo), transcrever o áudio já cortado, revisar.
2. Rastrear o rosto e recortar o bruto em tela cheia fechado (rosto ~60% da largura, olhos a ~30% da altura), suavizado.
3. Gancho: primeiros ~4 s em dividida com clipes/imagens reais em baixo trocando a cada ~1 s; título Bold 64 px centrado na divisória até ~10 s; corte seco para tela cheia em ~4 s.
4. Legenda em blocos de 1–4 palavras, ~1 s cada, TikTok Sans 650/51 px, baseline 1218.
5. Se a fala citar algo mostrável (tela, produto, notícia), cutaway em dividida com corte seco, 1–2 s, legenda no lugar.
6. Fonte em `ferramentas/fontes/TikTokSans-Variable.ttf` (eixos: opsz 12–36, wdth, wght 300–900, slnt; usar `set_variation_by_axes([36, 100, wght, 0])`).

Imagens de apoio: `criativos-1-quadros-*.png`, `criativos-1-abertura.png`, `criativos-1-legenda-zoom.png`, `criativos-1-fonte-comparacao.png`, `criativos-1-cutaway.png`.
