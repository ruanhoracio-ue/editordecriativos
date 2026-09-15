"""Teste da edição consolidada (10/09/2026).
Regras vigentes: dividida desde o 1º quadro · título e legenda sobre a divisória ·
SF Pro Bold, legenda simples por padrão e montada só nas frases que carregam a mensagem ·
cena troca 0,20 s antes da fala · corte seco, sem dissolve · branco/preto/verde #12CB87 ·
área de cima sempre com visual novo e em movimento."""
import json, os, re, sys, subprocess, functools, math
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
FF = open("ferramentas/ffmpeg_path.txt").read().strip()
REF = "referencias/reels-por-ia"
W, H, FPS = 1080, 1920, 30
BLACK = (6, 6, 6); CREAM = (242, 238, 228); GREEN = (18, 203, 135); WHITE = (255, 255, 255)
GREY_D = (108, 106, 100); GREY_C = (134, 131, 121); INK = (16, 16, 16)
SPLIT = 980
CAP = 67
PRE = 0.20                       # a cena entra 0,20 s antes da primeira palavra da frase

WORDS = json.load(open("work/v5/words_cut.json"))
T_END = json.load(open("work/v5/cuts.json"))["total"]
FACE = json.load(open("work/v5/face_track.json"))

def cl(x): return max(0.0, min(1.0, x))
def ease(x): x = cl(x); return 1 - (1 - x) ** 3
def eio(x): x = cl(x); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k
def mixc(a, b, k): return tuple(int(lerp(p, q, cl(k))) for p, q in zip(a, b))

@functools.lru_cache(64)
def sf(size, peso="Bold"):
    f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", int(size))
    f.set_variation_by_name(peso); return f

def tw(s, f): return f.getlength(s)
def dtxt(d, x, base, s, f, fill): d.text((x, base), s, font=f, fill=fill, anchor="ls")

def norm(s): return re.sub(r"[^\wÀ-ÿ%-]", "", s).lower()
def wt(text, after=-1.0):
    n = norm(text)
    for w in WORDS:
        if w["s"] >= after and norm(w["w"]) == n: return w["s"]
    raise KeyError(f"{text} após {after}")

_ft = np.array([f["t"] for f in FACE], float)
def _sm(k, n=6):
    v = np.array([f[k] for f in FACE], float)
    return np.convolve(np.pad(v, (n, n), mode="edge"), np.ones(2 * n + 1) / (2 * n + 1), mode="valid")
_cx, _cy = _sm("cx"), _sm("cy")
def face(t): return float(np.interp(t, _ft, _cx)), float(np.interp(t, _ft, _cy))

SRC = av.open("work/v5/base.mov"); VS = SRC.streams.video[0]; VS.thread_type = "AUTO"
def frames():
    for fr in SRC.decode(VS): yield fr.to_image()

def presenter(src, t, rh, zoom=1.0, face_at=0.44):
    rh = int(round(rh)); cw, ch = W / zoom, rh / zoom
    if ch > H: ch = H; cw = ch * W / rh
    fx, fy = face(t)
    left = 0 if cw >= W else cl((fx - cw / 2) / (W - cw)) * (W - cw)
    top = max(0, min(H - ch, fy - ch * face_at))
    c = src.crop((int(left), int(top), int(left + cw), int(top + ch)))
    return c if c.size == (W, rh) else c.resize((W, rh), Image.LANCZOS)

# ---------- legenda: simples por padrão, montada nas frases marcantes ----------
def build_blocks():
    bl, cur = [], []
    for w in WORDS:
        cur.append(w)
        s = " ".join(x["w"] for x in cur)
        if w["w"].endswith((",", ".", "?", "!")) or len(cur) >= 4 or len(s) > 24:
            bl.append(cur); cur = []
    if cur: bl.append(cur)
    out = []
    for i, b in enumerate(bl):
        e = b[-1]["e"] + 0.26
        if i + 1 < len(bl): e = min(e, bl[i + 1][0]["s"])
        out.append({"s": b[0]["s"], "e": e, "words": b})
    return out
BLOCKS = build_blocks()

# frases que carregam a mensagem -> legenda montada palavra por palavra
MONTADAS = set()
def marcar(*inicios):
    for t in inicios:
        b = min(BLOCKS, key=lambda x: abs(x["s"] - t))
        MONTADAS.add(round(b["s"], 3))

def captions(img, t, cy):
    b = next((x for x in BLOCKS if x["s"] <= t < x["e"]), None)
    if not b: return
    montada = round(b["s"], 3) in MONTADAS
    f = sf(CAP); asc, desc = f.getmetrics()
    base_y = cy + (asc - desc) / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if not montada:
        txt = " ".join(w["w"] for w in b["words"]).replace(",", "").replace(".", "")
        dtxt(d, (W - tw(txt, f)) / 2, base_y, txt, f, WHITE)
    else:
        vis = [w for w in b["words"] if w["s"] <= t + 1e-6]
        if not vis: return
        # largura final da linha visível, com a última palavra ainda crescendo
        k_ult = eio((t - vis[-1]["s"]) / 0.26)
        larg = [tw(w["w"].strip(",."), f) for w in vis]
        esp = f.getlength(" ")
        total = sum(larg) + esp * (len(larg) - 1)
        # alvo: linha centrada; anima a recentragem vindo da posição anterior
        if len(vis) > 1:
            larg_ant = [tw(w["w"].strip(",."), f) for w in vis[:-1]]
            total_ant = sum(larg_ant) + esp * (len(larg_ant) - 1)
            x = lerp((W - total_ant) / 2, (W - total) / 2, eio((t - vis[-1]["s"]) / 0.4))
        else:
            x = (W - total) / 2
        for i, w in enumerate(vis):
            txt = w["w"].strip(",.")
            if i == len(vis) - 1 and k_ult < 1:
                a = int(255 * eio((t - w["s"]) / 0.28))
                esc = lerp(1.05, 1.0, k_ult)
                fw = sf(int(CAP * esc))
                dtxt(d, x, base_y, txt, fw, (*WHITE, a))
            else:
                dtxt(d, x, base_y, txt, f, WHITE)
            x += larg[i] + esp
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(lay.split()[3].point(lambda v: int(v * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(9)).transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -3))
    img.alpha_composite(Image.alpha_composite(sh, lay))

def titulo(img, linhas):
    f = sf(76); asc, desc = f.getmetrics(); lh = int((asc + desc) * 1.02)
    y0 = SPLIT - lh * len(linhas) / 2 - (asc - desc) / 2 + 4
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, ln in enumerate(linhas):
        d.text(((W - tw(ln, f)) / 2, y0 + i * lh + asc), ln, font=f, fill=WHITE,
               anchor="ls", stroke_width=3, stroke_fill=(0, 0, 0, 235))
    img.alpha_composite(lay)

# ---------- lettering ----------
def lettering(img, t, linhas, size, cor, destaque, cinza, y0, align="center", x0=80, marcador=None):
    f = sf(size, "Bold"); asc, desc = f.getmetrics(); lh = int((asc + desc) * 1.06); esp = f.getlength(" ")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for li, linha in enumerate(linhas):
        ws = [tw(s, f) for s, _, _ in linha]
        x = x0 if align == "left" else (W - (sum(ws) + esp * (len(linha) - 1))) / 2
        for (s, t_in, hl), wd in zip(linha, ws):
            k = ease((t - t_in) / 0.24); kon = eio((t - t_in - 0.04) / 0.22)
            if k > 0:
                base = y0 + li * lh + asc + (1 - k) * 10
                if hl and marcador is not None:
                    km = eio((t - t_in - 0.04) / 0.26)
                    if km > 0:
                        d.rounded_rectangle((x - 12, base - asc * .78 - 6, x - 12 + (wd + 24) * km, base + desc * .5),
                                            9, fill=(*marcador, int(255 * km)))
                dtxt(d, x, base, s, f, (*mixc(cinza, destaque if hl else cor, kon), int(255 * k)))
            x += wd + esp
    img.alpha_composite(lay)
def LN(*a): return list(a)

# ---------- movimento e gráficos ----------
def drift(t, seed=0.0, ax=16, ay=20, sp=0.55):
    return (math.sin((t + seed) * sp) * ax, math.cos((t * .83 + seed) * sp) * ay)

@functools.lru_cache(8)
def _img(n): return Image.open(f"{REF}/{n}")

def full_bleed(img, t, t0, nome, zoom0=1.08, vel=0.07):
    im = _img(nome)
    im = im.convert("RGB") if im.mode not in ("RGBA", "LA", "P") else Image.alpha_composite(
        Image.new("RGBA", im.size, (12, 12, 12, 255)), im.convert("RGBA")).convert("RGB")
    bw, bh = W, SPLIT
    k = cl((t - t0) / 6.0); sc = zoom0 + vel * k
    tw_, th_ = int(bw * sc), int(bh * sc)
    ar = im.width / im.height
    if ar > tw_ / th_: nh = th_; nw = int(th_ * ar)
    else: nw = tw_; nh = int(tw_ / ar)
    im = im.resize((nw, nh), Image.LANCZOS)
    ox = (nw - bw) / 2 + math.sin(t * 0.5) * 26
    oy = (nh - bh) / 2 + math.cos(t * 0.42) * 18
    ox = max(0, min(nw - bw, ox)); oy = max(0, min(nh - bh, oy))
    img.paste(im.crop((int(ox), int(oy), int(ox + bw), int(oy + bh))), (0, 0))

def chip(img, t, t_in, cx, cy, label, kind="g", sub=None, seed=0.0, size=52, dark=True):
    k = ease((t - t_in) / 0.28)
    if k <= 0.02: return
    f = sf(size, "Bold"); asc, desc = f.getmetrics()
    fs = sf(max(11, int(size * .40)), "Semibold"); a2, d2 = fs.getmetrics()
    px, py = 38, 20
    bw = int(max(tw(label, f), tw(sub.upper(), fs) if sub else 0) + px * 2)
    bh = int(asc + desc + py * 2 + (a2 + d2 + 8 if sub else 0))
    lay = Image.new("RGBA", (bw + 14, bh + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    edge = (255, 255, 255) if dark else (0, 0, 0)
    d.rounded_rectangle((9, 11, bw + 9, bh + 11), 15, fill=(*edge, 255))
    fill = GREEN if kind == "g" else ((28, 28, 28) if dark else (252, 251, 247))
    d.rounded_rectangle((0, 0, bw, bh), 15, fill=fill, outline=edge, width=4)
    txtcol = INK if (kind == "g" or not dark) else WHITE
    yy = py
    if sub:
        dtxt(d, px, yy + a2, sub.upper(), fs, (70, 70, 66) if kind == "g" else ((165, 165, 165) if dark else (110, 108, 102)))
        yy += a2 + d2 + 6
    dtxt(d, px, yy + asc, label, f, txtcol)
    esc = lerp(0.92, 1.0, eio((t - t_in) / 0.28))
    lay = lay.resize((max(1, int(lay.width * esc)), max(1, int(lay.height * esc))), Image.LANCZOS)
    if k < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * k)))
    dx, dy = drift(t, seed, 9, 12, 0.5)
    img.alpha_composite(lay, (int(cx - lay.width / 2 + dx), int(cy - lay.height / 2 + dy)))

def onda(img, t, cx, cy, larg=560, alt=190, n=30, seed=0.0):
    """Forma de onda viva: as barras pulsam continuamente."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bw = larg / (n * 1.7); gap = bw * 0.7
    x = cx - (n * bw + (n - 1) * gap) / 2
    for i in range(n):
        amp = (0.22 + 0.78 * abs(math.sin(i * 0.8 + t * 3.1 + seed))) * alt / 2
        col = GREEN if i % 4 == 1 else WHITE
        d.rounded_rectangle((x, cy - amp, x + bw, cy + amp), bw / 2, fill=(*col, 235))
        x += bw + gap
    img.alpha_composite(lay)

def barra_progresso(img, t, t0, dur, cx, cy, larg=620, rot="RENDERIZANDO"):
    """Micro-animação funcional: barra preenchendo, para segurar o olho."""
    k = cl((t - t0) / dur)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    dx, dy = drift(t, 3.0, 7, 9, 0.4)
    x0 = cx - larg / 2 + dx; y0 = cy + dy
    d.rounded_rectangle((x0, y0, x0 + larg, y0 + 26), 13, fill=(40, 40, 40, 255), outline=(255, 255, 255, 190), width=3)
    d.rounded_rectangle((x0 + 3, y0 + 3, x0 + 3 + (larg - 6) * eio(k), y0 + 23), 11, fill=(*GREEN, 255))
    f = sf(26, "Semibold")
    dtxt(d, x0, y0 - 18, rot, f, (*WHITE, 220))
    dtxt(d, x0 + larg - tw(f"{int(k*100)}%", f), y0 - 18, f"{int(k*100)}%", f, (*GREEN, 235))
    img.alpha_composite(lay)

def relogio(img, t, t0, cx, cy, r=92):
    """Anel preenchendo, como o cronômetro da referência."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    dx, dy = drift(t, 5.0, 8, 10, 0.45)
    cx += dx; cy += dy
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 90), width=9)
    ang = 360 * cl((t - t0) / 2.2)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + ang, fill=(*GREEN, 255), width=9)
    f = sf(40, "Bold"); s = f"{t - t0:04.1f}s"
    dtxt(d, cx - tw(s, f) / 2, cy + 14, s, f, WHITE)
    img.alpha_composite(lay)

# ---------- roteiro: 9 cenas, uma a cada ~2,7 s ----------
T = {}
def A(k, s, after=-1.0): T[k] = wt(s, after); return T[k]
A("eu", "Eu"); A("reels", "Reels"); A("emelhor", "E", 3.3); A("nada1", "nada", 5.0)
A("so", "Só"); A("gpt", "GPT-6"); A("pedi", "pedi"); A("corte", "Corte")
A("ritmo", "ritmo"); A("legendas", "legendas"); A("efeitos", "efeitos"); A("musica", "música")
A("basicamente", "basicamente"); A("enquanto", "Enquanto"); A("faco", "faço")
A("absolutamente", "Absolutamente"); A("nada2", "nada", 17.0)
A("ese", "E", 17.7); A("bom", "bom"); A("seficar", "Se", 19.4); A("ruim", "ruim"); A("tambem", "também")
A("fazer", "fazer"); T["ia_fim"] = WORDS[-1]["s"]

marcar(T["absolutamente"], T["ese"], T["seficar"], T["eu"])

BEATS = [
    (0.00,               T["emelhor"] - PRE, "titulo",   "escuro"),
    (T["emelhor"] - PRE, T["so"] - PRE,      "nada",     "cheia-branco"),
    (T["so"] - PRE,      T["gpt"] - PRE,     "gravei",   "escuro"),
    (T["gpt"] - PRE,     T["corte"] - PRE,   "gpt",      "escuro"),
    (T["corte"] - PRE,   T["musica"] - PRE,  "tarefas",  "escuro"),
    (T["musica"] - PRE,  T["enquanto"] - PRE,"musica",   "escuro"),
    (T["enquanto"] - PRE,T["absolutamente"] - PRE, "trabalhando", "escuro"),
    (T["absolutamente"] - PRE, T["ese"] - PRE, "nada2",  "cheia-preto"),
    (T["ese"] - PRE,     T["seficar"] - PRE, "bom",      "escuro"),
    (T["seficar"] - PRE, T_END,              "ruim",     "cheia-branco"),
]

def beat_at(t):
    for s, e, n, bg in BEATS:
        if s <= t < e: return s, e, n, bg
    return BEATS[-1]

def compose(src, t):
    img = Image.new("RGBA", (W, H), (*BLACK, 255))
    s0, e0, nome, bg = beat_at(t)
    cheia = bg.startswith("cheia")
    fundo = WHITE if bg == "cheia-branco" else BLACK
    ImageDraw.Draw(img).rectangle((0, 0, W, H), fill=(*fundo, 255))

    if nome == "titulo":
        full_bleed(img, t, s0, "openai-gpt6-astra-career-website.png", 1.14, 0.12)
    elif nome == "nada":
        lettering(img, t, [LN(("Eu não vou", T["emelhor"], False)), LN(("fazer", T["fazer"], False), ("nada.", T["nada1"], True))],
                  118, INK, INK, (188, 188, 188), 760, marcador=GREEN)
    elif nome == "gravei":
        full_bleed(img, t, s0, "remotion-editor.jpg", 1.10, 0.09)
    elif nome == "gpt":
        full_bleed(img, t, s0, "cnn-codex.jpg", 1.10, 0.13)
    elif nome == "tarefas":
        chip(img, t, T["corte"], 300, 250, "Corte", "g", "tarefa 1", 0.2, 48)
        chip(img, t, T["ritmo"], 790, 250, "Ritmo", "w", "tarefa 2", 1.1, 48)
        chip(img, t, T["legendas"], 300, 470, "Legendas", "w", "tarefa 3", 2.0, 48)
        chip(img, t, T["efeitos"], 790, 470, "Efeitos", "g", "tarefa 4", 2.9, 48)
        barra_progresso(img, t, T["corte"], 4.2, W / 2, 700)
    elif nome == "musica":
        onda(img, t, W / 2, 300, 640, 230, 34)
        chip(img, t, T["musica"], W / 2, 600, "Música", "g", "tarefa 5", 0.6, 52)
        lettering(img, t, [LN(("e ele que se vira.", T["basicamente"] + 0.35, False))],
                  50, (225, 225, 225), GREEN, GREY_D, 760)
    elif nome == "trabalhando":
        full_bleed(img, t, s0, "remotion-timeline.png", 1.12, 0.13)
    elif nome == "nada2":
        lettering(img, t, [LN(("Absolutamente", T["absolutamente"], False)), LN(("nada.", T["nada2"], True))],
                  126, WHITE, GREEN, GREY_D, 780)
    elif nome == "bom":
        full_bleed(img, t, s0, "claude-code-og.webp", 1.08, 0.14)
    else:  # ruim
        lettering(img, t, [LN(("Se ficar", T["seficar"], False), ("ruim,", T["ruim"], True)),
                           LN(("também foi", T["tambem"], False)), LN(("a IA.", T["ia_fim"], True))],
                  104, INK, INK, (188, 188, 188), 660, marcador=GREEN)

    if not cheia:
        img.paste(presenter(src, t, H - SPLIT, lerp(1.0, 1.05, cl((t - s0) / 5.0))), (0, SPLIT))
        ImageDraw.Draw(img).rectangle((0, SPLIT - 3, W, SPLIT), fill=(*(BLACK if bg == "escuro" else (206, 202, 192)), 255))
        captions(img, t, SPLIT) if nome != "titulo" else None
    if nome == "titulo" and t < BEATS[0][1] - 0.05:
        titulo(img, ["Deixei a IA editar", "esse Reel inteiro."])
    if t > T_END - 0.4:
        ImageDraw.Draw(img).rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * ease((t - (T_END - 0.4)) / 0.4))))
    return img.convert("RGB")

if __name__ == "__main__":
    if sys.argv[1:2] == ["--stills"]:
        want = sorted(float(x) for x in sys.argv[2].split(",")); os.makedirs("work/v5/prev", exist_ok=True); i = 0
        for n, src in enumerate(frames()):
            t = n / FPS
            while i < len(want) and want[i] <= t + 1e-6:
                compose(src, t).save(f"work/v5/prev/t{want[i]:05.2f}.png"); i += 1
            if i >= len(want): break
        print("prévias:", i); sys.exit()
    out = sys.argv[1] if sys.argv[1:] else "saidas/reels-por-ia-v1.mp4"
    p = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "work/v5/mix.wav",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for n, src in enumerate(frames()):
        p.stdin.write(compose(src, n / FPS).tobytes())
        if n % 200 == 0: print(n, flush=True)
    p.stdin.close(); p.wait(); print("saída:", out, p.returncode)
