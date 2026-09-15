# Skill: editor-video-pessoal

Skill do Claude Code que edita vídeos verticais (Reels e criativos de anúncio) a partir de um bruto gravado no celular: corta os respiros sem comer palavra, transcreve, acompanha o rosto, monta título/legenda e busca material real na internet pra área de cima. Sai em 1080x1920 (RL), 1080x1350 (IN) e 1080x1080 (GL).

Tudo que o Claude precisa saber está em `.claude/skills/editor-video-pessoal/SKILL.md` (regras) e `references/` (análises das referências, medidas de fonte, tempos). Os scripts em `work/` são o pipeline que a skill usa.

## Como usar

1. Clone este repositório e abra a pasta no Claude Code (app ou terminal).
2. Prepare o ambiente (abaixo). O Claude lê o `CLAUDE.md` e a skill sozinho.
3. Jogue o bruto em `brutos/` e peça: "edita esse como criativo" (ele vai perguntar: dividida ou inteira?) ou "edita como Reel".
4. As saídas vão pra `saidas/`.

## Ambiente (uma vez)

Nada é instalado no sistema; tudo fica na pasta.

```bash
python3 -m venv ferramentas/venv            # Python 3.11 ou mais novo
ferramentas/venv/bin/pip install pillow av numpy imageio-ffmpeg faster-whisper opencv-python-headless
ferramentas/venv/bin/python -c "import imageio_ffmpeg,pathlib;pathlib.Path('ferramentas/ffmpeg_path.txt').write_text(imageio_ffmpeg.get_ffmpeg_exe())"
ferramentas/venv/bin/python -c "from faster_whisper import WhisperModel; WhisperModel('small', download_root='models')"
```

Depois disso, os comandos do pipeline rodam com `ferramentas/venv/bin/python` (o `CLAUDE.md` explica o caminho; ajuste a variável `PY` lá se necessário).

Fontes já incluídas em `ferramentas/fontes/` (TikTok Sans e Manrope, licença OFL ao lado). A legenda dos Reels usa a SF Pro do macOS (`/System/Library/Fonts/SFNS.ttf`); em outro sistema, troque por outra Bold na skill.

## Pipeline de criativos

```bash
PY=ferramentas/venv/bin/python
PYTHONPATH=work $PY work/criativo_prep.py c1 brutos/meu-video.MOV     # corte, voz, transcrição, rosto -> work/c1/
# escrever work/c1/c1.py a partir de work/exemplos/ (título, gancho, cutaways, blocos de legenda)
$PY work/c1/c1.py --blocos                                              # confere o mapeamento das legendas
$PY work/c1/c1.py --stills 1,5,20                                       # prévias em work/c1/prev/
$PY work/c1/c1.py --formatos RL,IN,GL                                   # renders em saidas/
```

O Claude faz esses passos sozinho quando você pede a edição; o comando está aqui pra quem quiser rodar na mão.

## O que NÃO está aqui

- Os vídeos de referência (direitos de terceiros) — só as análises e alguns quadros.
- `work/portal.py` e `work/portal_upload.py` são do portal interno do autor (precisam de `ferramentas/portal.env`); ignore se não for o seu caso.
