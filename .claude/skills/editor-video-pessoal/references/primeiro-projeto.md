# Primeiro projeto: contexto, não template aprovado

## Material e entrega

- Bruto: `Perfect-Selfie-Videos-20260908-154545.MOV`, vídeo vertical 1080 × 1920, aproximadamente 30,24 s.
- Primeira entrega: `video-editado.mp4`, 1080 × 1920, 30 fps, 26,3 s, 789 quadros, 15 cenas.
- Projeto editável já entregue no chat original: `projeto-editavel.zip`.
- Esses três arquivos não estão embutidos nesta skill. O usuário pode anexá-los separadamente se desejar continuar exatamente esse projeto. Não presumir acesso ao computador ou aos caminhos locais do chat anterior.

## Conteúdo da fala

O usuário pergunta se o espectador ainda perde horas editando vídeo. Fala sobre usar GPT-6 e IA para transformar ideias em vídeo, criar roteiro, sugerir cortes, organizar cenas, pensar em legendas e transições, definir estilo e ajustar o resultado por conversa. Fecha dizendo que é um teste e imaginando possibilidades futuras.

Este resumo descreve a fala gravada, não verifica as alegações sobre produtos ou modelos. Para citá-las como fatos em outro contexto, consultar fontes atuais.

## Implementação anterior

A composição foi inicialmente escrita em Remotion. O navegador de renderização falhou por uma restrição do sandbox do macOS naquela sessão. Isso não demonstra incompatibilidade geral com Remotion; verificar o ambiente atual se a ferramenta for usada.

O MP4 efetivamente entregue foi composto com Python, Pillow, PyAV e FFmpeg. A fonte foi Manrope. Houve redução de pausas, tratamento de voz, trilha e efeitos sintetizados localmente e ilustração da mão com uma claquete gerada por ImageGen.

No pacote editável antigo, os principais arquivos são:

- `work/render_video.py`: implementação que realmente gerou a entrega.
- `work/edit/src/data.json`: cenas e legendas.
- `work/face_track.json`: posições do rosto.
- `work/edit/public/base.mp4`: vídeo com pausas encurtadas.
- `work/edit/public/voice.wav` e `score.wav`: voz tratada e trilha/efeitos.
- `work/edit/public/idea.png`, `Manrope.ttf`: ilustração e fonte.
- `work/legendas.srt`: legendas separadas.

## Problemas explicitamente apontados

1. Palavras das legendas em alturas diferentes. Desenho de palavras com alinhamento pelo topo visível pode explicar o defeito; usar baseline comum e confirmar visualmente.
2. Bordas/faixas laterais na metade inferior, causadas por imagem reduzida e laterais desfocadas. O usuário quer a área totalmente preenchida.
3. Necessidade de referências reais pesquisadas quando a fala citar assuntos específicos.
4. Lettering deve ganhar entrada palavra por palavra, fluidez e protagonismo, removendo microfrases acessórias.

A verificação técnica anterior confirmou decodificação e timestamps, mas não tornou o resultado visual aprovado. Não usar sucesso técnico como substituto da revisão estética.

## Estado da colaboração

O usuário pediu para salvar essas mudanças e não refazer o vídeo naquele momento. Depois solicitou este pacote para levar o contexto ao Claude. Receber o contexto não autoriza automaticamente uma nova renderização.
