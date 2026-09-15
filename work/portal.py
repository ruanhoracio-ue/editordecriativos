"""Portal Conteúdo Extremo (https://conteudoextremo.conversaoextrema.com) — tabela `criativos` no Supabase.

A chave pública é a mesma que o site usa no navegador; fica em ferramentas/portal.env (linha SUPABASE_KEY=...).
Colunas: id, created_at, status, editor, gravacao, tag, nome_arquivo, link_pasta_base, arquivo_finalizado, alteracao.

Uso:
    python work/portal.py listar [n]
    python work/portal.py cadastrar "Título 1" "Título 2" ...          (Editado / Ruan / hoje / Perpétuo)
    python work/portal.py link "Título" <url_arquivo_finalizado> [url_pasta]
"""
import json, os, sys, time, random, string, urllib.request, urllib.parse, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(l.strip().split("=", 1) for l in open(os.path.join(ROOT, "ferramentas/portal.env")) if "=" in l)
URL = ENV.get("SUPABASE_URL", "https://jtbcdnoiwocgfunckvvz.supabase.co") + "/rest/v1/criativos"
H = {"apikey": ENV["SUPABASE_KEY"], "Authorization": "Bearer " + ENV["SUPABASE_KEY"], "Content-Type": "application/json"}

def req(method, url, body=None, prefer=None):
    h = dict(H); h["Prefer"] = prefer or "return=representation"
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, headers=h, method=method)
    with urllib.request.urlopen(r) as resp: return json.loads(resp.read() or b"[]")

def listar(n=10):
    return req("GET", f"{URL}?select=*&order=created_at.desc&limit={n}")

def novo_id():
    return f"criativo-{int(time.time()*1000)}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"

def cadastrar(titulos, status="Editado", editor="Ruan", gravacao=None, tag="Perpétuo"):
    gravacao = gravacao or datetime.date.today().strftime("%d/%m")
    rows = [{"id": novo_id(), "status": status, "editor": editor, "gravacao": gravacao, "tag": tag, "nome_arquivo": t,
             "link_pasta_base": "", "arquivo_finalizado": "", "alteracao": ""} for t in titulos]
    return req("POST", URL, rows)

def link(titulo, url_final, url_pasta=None):
    body = {"arquivo_finalizado": url_final}
    if url_pasta: body["link_pasta_base"] = url_pasta
    return req("PATCH", f"{URL}?nome_arquivo=eq.{urllib.parse.quote(titulo)}", body)

if __name__ == "__main__":
    cmd, args = (sys.argv[1] if sys.argv[1:] else "listar"), sys.argv[2:]
    if cmd == "listar":
        for x in listar(int(args[0]) if args else 10):
            print(f"{x['created_at'][:16]}  {x['status']:<10} {x['editor']:<8} {x['gravacao']:<6} {x['tag']:<9} {x['nome_arquivo']}  {x['arquivo_finalizado'] or '-'}")
    elif cmd == "cadastrar":
        for x in cadastrar(args): print("cadastrado:", x["id"], x["nome_arquivo"])
    elif cmd == "link":
        for x in link(args[0], args[1], args[2] if len(args) > 2 else None): print("atualizado:", x["nome_arquivo"], x["arquivo_finalizado"])
