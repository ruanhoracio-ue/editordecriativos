"""Renderizador do padrão CRIATIVOS (references/padrao-criativos.md). Cada vídeo tem um script de
configuração (work/cN/cN.py) que monta um dict CFG e chama `rodar(CFG)`.

CFG:
  id        'c2'                          pasta work/<id> com base.mov, voice.wav, words_cut.json, face_track.json, cuts.json
  ref       'referencias/criativo-2'      pasta do material real
  titulo    ['linha 1', 'linha 2']
  t_gancho  4.4     corte seco dividida -> tela cheia
  t_titulo  10.0    título some (fim da frase do gancho)
  gancho    [(t0, t1, arquivo, foco_vertical, recorte|None), ...]   área de baixo durante o gancho
  cutaways  [(t0, t1, arquivo, foco, recorte), ...]                  voltas à dividida no meio
  repl      {indice: (n_tokens, [novos])}  correções da transcrição
  frases    texto com '|' separando blocos e '\\n' entre linhas (1–4 palavras, por unidade de sentido)
  legenda_desde  palavra (normalizada) depois da qual a legenda começa (padrão: última do gancho)
  enquadro  função t -> (zoom, face_at) para a tela cheia; padrão (1.32, 0.33)
  saida     'saidas/criativo-2-v1.mp4'
  variante  'dividida' (padrão: gancho em tela dividida + cutaways) | 'inteira' (tela cheia do primeiro quadro ao fim, sem material embaixo)
"""
import json, os, re, subprocess, sys, functools
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
FF = open("ferramentas/ffmpeg_path.txt").read().strip()
FPS = 30
# formato: (largura, altura, divisória). Legenda fica em 63,4% da altura (1218/1920 na referência).
FORMATOS = {"RL": (1080, 1920, 960), "IN": (1080, 1350, 675), "GL": (1080, 1080, 600)}   # GL: faixa de cima maior p/ a cabeça caber
W, H, SPLIT = FORMATOS["RL"]
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
FONTE = "ferramentas/fontes/TikTokSans-Variable.ttf"

def cl(x): return max(0.0, min(1.0, x))
def ease(x): x = cl(x); return 1 - (1 - x) ** 3
def lerp(a, b, k): return a + (b - a) * k
def norm(s): return re.sub(r"[^\wÀ-ÿ]", "", s).lower()

@functools.lru_cache(32)
def tk(size, wght):
    f = ImageFont.truetype(FONTE, int(size)); f.set_variation_by_axes([36, 100, wght, 0]); return f

def carregar_palavras(D, repl):
    W0 = json.load(open(f"{D}/words_cut.json")); out = []; i = 0
    while i < len(W0):
        if i in repl:
            n, novos = repl[i]; s0, e0 = W0[i]["s"], W0[i + n - 1]["e"]; dt = (e0 - s0) / max(1, len(novos))
            for j, p in enumerate(novos): out.append({"w": p, "s": round(s0 + j * dt, 3), "e": round(s0 + (j + 1) * dt, 3)})
            i += n; continue
        out.append(dict(W0[i])); i += 1
    return out

def montar_blocos(WORDS, frases, desde, t_end):
    lista = [p.strip() for ln in frases.strip().split("\n") for p in ln.split("|") if p.strip()]
    k = next(i for i, w in enumerate(WORDS) if norm(w["w"]) == norm(desde)) + 1
    blocos = []
    for fr in lista:
        toks = fr.split(); ws = WORDS[k:k + len(toks)]
        for a, b in zip(toks, ws):
            assert norm(a) == norm(b["w"]), f"'{a}' != '{b['w']}' em {k} ({' '.join(x['w'] for x in WORDS[k-2:k+5])})"
        blocos.append({"txt": fr, "s": ws[0]["s"], "e": ws[-1]["e"]}); k += len(toks)
    assert k == len(WORDS), f"sobraram palavras: {' '.join(w['w'] for w in WORDS[k:])}"
    for a, b in zip(blocos, blocos[1:]): a["e"] = b["s"]
    blocos[-1]["e"] = t_end
    return blocos

def sombra_div():
    im = Image.new("RGBA", (W, 240), (0, 0, 0, 0))
    for y in range(240): ImageDraw.Draw(im).line((0, y, W, y), fill=(0, 0, 0, int(190 * (1 - y / 240) ** 1.4)))
    return im

def com_sombra(img, lay, alpha=0.6, blur=7, dy=3):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -dy))
    img.alpha_composite(Image.alpha_composite(sh, lay))

def titulo(img, linhas):
    f = tk(64, 700); asc, desc = f.getmetrics()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    passo = 70; y0 = SPLIT - passo * len(linhas) / 2 + 5     # referência: linhas em 875 e 945 p/ 2 linhas
    for i, ln in enumerate(linhas):
        d.text(((W - f.getlength(ln)) / 2, y0 + i * passo + asc - 6), ln, font=f, fill=WHITE, anchor="ls")
    com_sombra(img, lay)

def legenda(img, blocos, t):
    b = next((x for x in blocos if x["s"] <= t < x["e"]), None)
    if not b: return
    f = tk(51, 650)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(((W - f.getlength(b["txt"])) / 2, round(H * 0.634)), b["txt"], font=f, fill=WHITE, anchor="ls")
    com_sombra(img, lay, 0.55, 6, 2)

def cobrir(im, w, h, foco=0.5, push=1.0):
    k = max(w / im.width, h / im.height) * push
    cw, ch = w / k, h / k
    left = (im.width - cw) / 2; top = (im.height - ch) * foco
    return im.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((w, h), Image.LANCZOS)

# tela cheia por formato: (multiplicador do zoom, face_at). Quadro mais baixo pede menos zoom p/ o queixo não bater na legenda.
AJUSTE = {"RL": (1.0, None, 0.44, 0), "IN": (0.95, 0.34, 0.47, 200), "GL": (0.85, 0.34, 0.50, 120)}   # (zoom x, face_at cheia, face_at dividida, recuo do material no cutaway p/ a legenda cair em faixa preta)

def rodar_formatos(CFG):
    """CLI: `--formatos IN,GL [--stills t,t]` ou `--stills t,t` (RL) ou `--blocos` ou nada (RL)."""
    argv = sys.argv[1:]; fmts = ["RL"]
    if argv[:1] == ["--formatos"]:
        fmts = argv[1].split(","); sys.argv = [sys.argv[0]] + argv[2:]
    for f in fmts: rodar(CFG, f)

def rodar(CFG, formato="RL"):
    global W, H, SPLIT
    W, H, SPLIT = FORMATOS[formato]; SOMBRA_DIV = sombra_div()
    kz, fa_fmt, fa_div, recuo = AJUSTE[formato]
    D = f"work/{CFG['id']}"; REF = CFG["ref"]
    WORDS = carregar_palavras(D, CFG.get("repl", {}))
    T_END = min(json.load(open(f"{D}/cuts.json"))["total"], WORDS[-1]["e"] + 0.5)   # termina 0,5 s depois da última palavra
    desde = CFG.get("legenda_desde") or WORDS[next(i for i, w in enumerate(WORDS) if w["s"] >= CFG["t_titulo"]) - 1]["w"]
    BLOCOS = montar_blocos(WORDS, CFG["frases"], desde, T_END)
    enq = CFG.get("enquadro", lambda t: (1.32, 0.33))

    FACE = json.load(open(f"{D}/face_track.json"))
    ft = np.array([f["t"] for f in FACE], float)
    def sm(k, n=5):
        v = np.array([f[k] for f in FACE], float)
        med = np.array([np.median(v[max(0, i - 4):i + 5]) for i in range(len(v))])
        return np.convolve(np.pad(med, (n, n), mode="edge"), np.ones(2 * n + 1) / (2 * n + 1), mode="valid")
    cx, cy = sm("cx"), sm("cy")
    def face(t): return float(np.interp(t, ft, cx)), float(np.interp(t, ft, cy))

    src_c = av.open(f"{D}/base.mov"); VS = src_c.streams.video[0]; VS.thread_type = "AUTO"
    SW, SH = VS.width, VS.height
    def frames():
        for fr in src_c.decode(VS): yield fr.to_image()

    def presenter(src, t, rh, zoom, face_at):
        cw = SW / zoom; ch = cw * rh / W
        if ch > SH: ch = SH; cw = ch * W / rh
        fx, fy = face(t)
        left = max(0, min(SW - cw, fx - cw / 2)); top = max(0, min(SH - ch, fy - ch * face_at))
        return src.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((W, rh), Image.LANCZOS)

    @functools.lru_cache(16)
    def img_ref(n): return Image.open(f"{REF}/{n}").convert("RGB")
    def clipe(img, t, lista, d=0):
        for s, e, nome, foco, rec in lista:
            if s <= t < e:
                im = img_ref(nome); im = im.crop(rec) if rec else im
                push = lerp(1.0, 1.04, (t - s) / max(0.4, e - s))
                img.paste(cobrir(im, W, H - SPLIT - d, foco, push), (0, SPLIT + d)); return

    def compose(src, t):
        img = Image.new("RGBA", (W, H), (*BLACK, 255))
        inteira = CFG.get("variante", "dividida") == "inteira"
        gancho = t < CFG["t_gancho"] and not inteira
        dividida = gancho or (not inteira and any(s <= t < e for s, e, *_ in CFG.get("cutaways", [])))
        if dividida:
            img.paste(presenter(src, t, SPLIT, 1.0, fa_div), (0, 0))
            clipe(img, t, CFG["gancho"]) if gancho else clipe(img, t, CFG["cutaways"], recuo)
        else:
            z, fa = enq(t); img.paste(presenter(src, t, H, z * kz, fa_fmt or fa), (0, 0))
        if t < CFG["t_titulo"]:
            if gancho:   # sombra no topo da área de baixo p/ o título não cair em fundo claro (manchete branca)
                img.alpha_composite(SOMBRA_DIV, (0, SPLIT))
            titulo(img, CFG["titulo"])
        else:
            if dividida and not recuo: img.alpha_composite(SOMBRA_DIV, (0, SPLIT))   # RL: legenda cai sobre o material
            legenda(img, BLOCOS, t)
        if t > T_END - 0.3:
            ImageDraw.Draw(img).rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * ease((t - (T_END - 0.3)) / 0.3))))
        return img.convert("RGB")

    if sys.argv[1:2] == ["--stills"]:
        want = sorted(float(x) for x in sys.argv[2].split(",")); os.makedirs(f"{D}/prev", exist_ok=True); i = 0
        for n, src in enumerate(frames()):
            t = n / FPS
            while i < len(want) and want[i] <= t + 1e-6:
                compose(src, t).save(f"{D}/prev/{formato}-t{want[i]:05.2f}.png"); i += 1
            if i >= len(want): break
        print("prévias:", i); return
    if sys.argv[1:2] == ["--blocos"]:
        for b in BLOCOS: print(f"{b['s']:6.2f}-{b['e']:6.2f}  {b['txt']}")
        return
    out = CFG["saida"] if formato == "RL" else CFG["saida"].replace(".mp4", f"-{formato}.mp4")
    p = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{D}/voice.wav",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for n, src in enumerate(frames()):
        p.stdin.write(compose(src, n / FPS).tobytes())
        if n % 600 == 0: print(n, flush=True)
    p.stdin.close(); p.wait(); print("saída:", out, p.returncode)
