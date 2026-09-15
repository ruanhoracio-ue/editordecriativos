# Referência 6 — legendas (enviada em 09/09/2026)

Arquivo: `referencia-6-legendas.mp4` (720x1280, 1:36, 24 fps). O usuário pediu: "dá só uma olhada nas legendas desse vídeo com calma, vê se tu consegue fazer igual, ou não".

**Resposta: consigo. É mais simples do que a legenda que estou fazendo hoje.**

## CORREÇÃO (o usuário me corrigiu, com razão)
Na primeira leitura eu disse "Helvetica Neue Medium" e "frase inteira de uma vez, sem animação". **Os dois estavam errados.** Eu tinha amostrado quadros consecutivos em apenas dois instantes, e calhou de cair num trecho em que a legenda estava parada. Generalizei de uma amostra ruim.

Refiz medindo a caixa do texto **quadro a quadro** (108 quadros seguidos, 24 fps). O resultado está abaixo.

## Fonte: SF Pro Bold
O usuário disse SF Pro Bold e confere. Comparei os pesos com a largura casada na largura real da linha (340 px de 720) — ver `referencia-6-comparacao-fontes.png`. Semibold fica leve, Heavy fica pesado, **Bold bate**.
- `/System/Library/Fonts/SFNS.ttf` com `set_variation_by_name("Bold")`.
- Tamanho **45 px** no quadro 720x1280 → **~67 px em 1080x1920**.
- Branco puro, sem caixa, sem contorno, sombra difusa suave por baixo.
- Espaçamento entre letras normal.

## A legenda TEM movimento (medido quadro a quadro)
Trecho limpo, t = 6,33 s a 7,25 s, a frase "ao seu time" sendo montada:

| t (s) | largura | centro x | px brancos | o que está acontecendo |
|---|---|---|---|---|
| 6,33 – 6,50 | 102 → 106 | 191 → 170 | 698 → 1369 | "ao" **acendendo** (largura fixa, brilho subindo) |
| 6,54 | 277 | 253 | 1504 | entra "seu", ainda apagado |
| 6,54 – 6,71 | 278 → 271 | 252 → 244 | 1504 → 3005 | "seu" acende e a linha **recentra suavemente** |
| 6,75 | 504 | 360 | 3793 | entra "time", ainda apagado |
| 6,75 – 7,17 | 504 → 481 | 360 → 348 | 3793 → 5323 | "time" acende, **encolhe 4,5%** e a linha recentra |

Três coisas acontecem juntas a cada palavra nova:
1. **Palavra por palavra.** A frase é montada acrescentando uma palavra por vez, não trocada inteira.
2. **A palavra nova acende**: entra apagada e sobe para branco em 0,2 a 0,4 s. Mesma mecânica da Referência 5.
3. **A palavra nova entra ~5% maior e assenta no tamanho normal**, e a linha inteira **recentra com suavização** (o centro caminhou 360 → 348 em 10 quadros, desacelerando). Não é salto.

Ver `referencia-6-animacao-real.png`: dá para ver "ao" → "ao seu" → "ao seu time", com a palavra nova cinza antes de virar branca.

## Segunda correção: a animação é EXCEÇÃO, não a regra
O usuário apontou: "essa animação é só às vezes, de resto é legenda normal básica sem animação. Entra animação só em palavras-chaves e frases específicas, marcantes."

Ele está certo. Eu tinha visto um trecho animado e generalizei de novo, na direção oposta. Medi o vídeo inteiro (2314 quadros, localizando a legenda em qualquer altura da metade de baixo, porque **ela muda de altura conforme a cena**):

- **1638 quadros com legenda localizada (≈68 s de 96 s).**
- **12 momentos** em que a legenda realmente monta palavra por palavra, ou seja **cerca de um a cada 8 segundos**.
- Todo o resto é **legenda simples**: a frase aparece inteira, fica parada e é substituída pela próxima. Verificado a olho: em 12,5 s "Ou seja," aparece inteira e não muda por 12 quadros; em 27–28 s "E cada" / "item esquecido" / "é um negócio" são só trocas de frase, sem montagem.

Os 12 momentos animados caem em: "você monta o playbook", "treina todo mundo", "está lá improvisando tudo", "deixa o cliente sair da call", "um PDF salvo no computador", "mas e se ele entrar?", "você nem precisa", "clica em remixar", "uma cópia inteira do sistema", "o playbook sai de um PDF aleatório", "não depois que ela foi perdida", "o link tá na minha bio". São as frases que carregam o argumento e a chamada final, não a fala de ligação.

## Regra final da legenda
1. **Padrão: legenda simples.** Frase inteira, parada, trocada pela próxima. Sem fade, sem escala, sem palavra por palavra. É assim na maior parte do vídeo.
2. **Exceção, mais ou menos uma vez a cada 8 segundos**, nas frases que carregam a mensagem: montar **palavra por palavra**, com a palavra nova entrando apagada e **acendendo** em 0,2–0,4 s, entrando ~5% maior e assentando, e a linha **recentrando com easing** de ~0,4 s.
3. Escolher essas frases pelo conteúdo, não por intervalo fixo: o problema, a virada, o número, a chamada final.
4. **A legenda não fica sempre na mesma altura.** Ela acompanha a composição da cena.

## Como fazer igual
- SF Pro Bold, ~67 px em 1080x1920, branco, sem contorno, sombra difusa, espaçamento normal.
- Implementar os dois modos: `simples` (padrão) e `montada` (exceção), e marcar à mão quais frases usam o modo montado.
