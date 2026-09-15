# Referência 4 — cores, animação e fluidez (enviada em 09/09/2026)

Arquivo: `referencia-4-fluidez.mp4` (720x1280, 41,4 s). Mesmo criador da Referência 1. Pedido do usuário: "pegue cores, animações, mas lembre, quero tudo muito fluido, movimentos, bem bonito".

## Paleta (amostrada dos quadros)
- Preto `#030303`
- Creme `#F2EEE4`
- Amarelo `#FBC901`
- Cinza da palavra ainda não dita: `#848177` sobre creme, cinza escuro sobre preto
- Branco `#FFFFFF`

## Animação assinatura: a palavra acende
O texto NÃO entra por deslocamento. Cada palavra surge apagada, em cinza, e **acende** para branco (ou amarelo, se for a palavra-chave) no instante em que é falada. As posições são fixas desde o início: nunca há reflow. Ver `referencia-4-acende-palavra.png`.

## Movimento constante (a "fluidez" pedida)
- Colagens em preto e branco flutuam o tempo todo: deriva senoidal, leve rotação e leve respiração de escala. Nunca ficam paradas.
- Transições entre cenas são crossfade curto, não corte seco.
- O apresentador tem push-in lento e contínuo.
- Botões e cartões também flutuam de leve, com fases diferentes (parallax).

## Elementos
- Layout dividido: gráfico em cima, apresentador embaixo, com barra de progresso amarela na divisória.
- Cenas em tela cheia creme e em tela cheia amarela, com tipografia grande preta. Nessas cenas **não há legenda**: o lettering é a mensagem.
- Botões/chips: retângulo arredondado, borda preta, **sombra dura preta deslocada**, preenchimento creme ou amarelo, texto preto. Ver `referencia-4-botoes.png`.
- Marcador amarelo atrás da palavra-chave em fundo creme.
- Legenda da referência fica numa caixinha creme com texto preto e sublinhado na palavra ativa. **Não adotado**: o usuário já tinha travado a legenda em Helvetica Bold branca.

## Implementação
`work/v2/render4.py`. Arte gerada por código (linha do tempo e forma de onda em traço branco com detalhes amarelos), já que não há colagens gravadas disponíveis.
