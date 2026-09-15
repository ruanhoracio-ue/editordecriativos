# videos-tessmann

Projeto de edição dos vídeos pessoais do usuário. A skill `.claude/skills/editor-video-pessoal/SKILL.md` define direção criativa e preferências obrigatórias; ler antes de qualquer edição.

## Pastas

- `brutos/`: vídeos originais. Nunca modificar ou sobrescrever.
- `saidas/`: entregas, sempre com versão no nome (ex.: `nome-v2.mp4`). Não sobrescrever versão anterior.
- `trilhas/`: músicas e efeitos.
- `models/`: cache do faster-whisper (modelo `small` já baixado, usar `local_files_only=True`).
- `ferramentas/`: bibliotecas Python e ffmpeg já instalados localmente. Não há nada instalado no sistema.

## Ambiente de renderização (sem instalar nada no sistema)

O Python do sistema (3.9) NÃO serve. Usar o Python 3.12 do runtime do Codex, que já está no disco:

```
PY=~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
PYTHONPATH=ferramentas/pydeps:ferramentas/cvdeps "$PY" script.py
```

- ffmpeg: caminho em `ferramentas/ffmpeg_path.txt` (binário do imageio_ffmpeg, v7.1, arm64).
- Bibliotecas disponíveis: av (PyAV), numpy, Pillow, cv2, imageio_ffmpeg, faster_whisper, ctranslate2, onnxruntime.
- Fonte: `ferramentas/fontes/Manrope.ttf` (variável; licença ao lado).
- O aviso `objc[...] Class AVFFrameReceiver is implemented in both...` ao importar av e cv2 juntos é conhecido e inofensivo.
- Se o runtime do Codex sumir, alternativa: `python3 -m venv` com Python >= 3.11 e `pip install pillow av numpy imageio-ffmpeg faster-whisper opencv-python-headless` (requer download; pedir ao usuário).

## Histórico

O primeiro vídeo (08/09/2026) foi feito no app ChatGPT/Codex, projeto em `~/Documents/Codex/2026-09-08/cons`. Tem defeitos conhecidos listados na skill; não é modelo aprovado.

## Referências da internet (motivo de o projeto estar no Claude Code)

O usuário quer que cada vídeo use informações, fotos e vídeos reais buscados na internet quando a fala citar algo específico (notícia, pessoa, produto, vídeo, interface). Regras:

- Pesquisar com WebSearch/WebFetch ou o navegador. Conferir identidade, contexto e data antes de usar.
- Baixar arquivos exige pedir permissão ao usuário antes, informando nome, origem e tamanho. Só baixar de fontes confiáveis.
- Guardar o material em `referencias/<nome-do-video>/` com um `fontes.md` contendo URL, autor, data e onde foi usado no vídeo.
- Mostrar atribuição legível na tela quando o material for de terceiros. Preferir fontes oficiais, imprensa, páginas do próprio produto ou licenças livres.
- Nunca inventar imagem e apresentar como real. Se não achar, dizer e pedir link ou arquivo.
- Vídeos do YouTube/TikTok/Instagram: `work/baixar.py URL pasta [ini fim] [nome]` (yt-dlp local em `ferramentas/pydeps`, instalado em 15/09/2026 com autorização). Baixar só o trecho necessário.
