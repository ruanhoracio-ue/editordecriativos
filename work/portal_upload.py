"""Sobe os vídeos de um criativo para o portal (R2 via /api/media, multipart) como anexos da linha
(prefixo `criativos/<id>`, que é o que a aba Anexos do portal lista) e preenche `arquivo_finalizado`
com a URL do RL. Os endpoints /api/media do Worker não exigem login (conferido no código em 15/09/2026).

Uso:
    python work/portal_upload.py "Título exato da linha" caminho-RL.mp4 [caminho-IN.mp4 caminho-GL.mp4 ...]
"""
import json, os, sys, urllib.request, urllib.parse, mimetypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import portal

BASE = "https://conteudoextremo.conversaoextrema.com"
PARTE = 25 * 1024 * 1024

def _json(method, path, body=None, raw=None, ctype="application/json"):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": ctype, "User-Agent": "Mozilla/5.0 (Macintosh) videos-tessmann"})
    with urllib.request.urlopen(r, timeout=600) as resp: return json.loads(resp.read() or b"{}")

def subir(caminho, prefixo):
    nome = os.path.basename(caminho); ctype = mimetypes.guess_type(nome)[0] or "application/octet-stream"
    tam = os.path.getsize(caminho)
    mpu = _json("POST", "/api/media/mpu/create", {"filename": nome, "contentType": ctype, "prefix": prefixo})
    key, uid = mpu["key"], mpu["uploadId"]
    partes = []; n = 1
    with open(caminho, "rb") as f:
        while True:
            bloco = f.read(PARTE)
            if not bloco: break
            q = f"?key={urllib.parse.quote(key, safe='')}&uploadId={urllib.parse.quote(uid, safe='')}&partNumber={n}"
            p = _json("PUT", "/api/media/mpu/part" + q, raw=bloco, ctype="application/octet-stream")
            partes.append({"partNumber": p["partNumber"], "etag": p["etag"]})
            print(f"   parte {n} ({min(n * PARTE, tam) / 1e6:.0f}/{tam / 1e6:.0f} MB)", flush=True); n += 1
    fim = _json("POST", "/api/media/mpu/complete", {"key": key, "uploadId": uid, "parts": partes})
    return BASE + fim["url"]

def linha(titulo):
    rows = portal.req("GET", f"{portal.URL}?select=id,nome_arquivo,arquivo_finalizado&nome_arquivo=eq.{urllib.parse.quote(titulo)}")
    if not rows: raise SystemExit(f"linha não encontrada no portal: {titulo}")
    return rows[0]

if __name__ == "__main__":
    titulo, arquivos = sys.argv[1], sys.argv[2:]
    row = linha(titulo); print(f"{titulo} -> {row['id']}")
    urls = {}
    for a in arquivos:
        print(" subindo", os.path.basename(a), flush=True)
        urls[a] = subir(a, f"criativos/{row['id']}"); print("  ", urls[a])
    rl = next((u for a, u in urls.items() if a.endswith("RL.mp4") or not any(x in a for x in ("-IN", "-GL"))), None)
    if rl:
        portal.link(titulo, rl); print(" arquivo_finalizado =", rl)
