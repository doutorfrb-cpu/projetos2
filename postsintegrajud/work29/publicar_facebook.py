#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica a peça na Página do Facebook do IntegraJud, pela Graph API.

DIFERENÇA IMPORTANTE PARA O INSTAGRAM: aqui a API aceita o ARQUIVO direto.
Não precisa hospedar as imagens em lugar nenhum — some a dependência de FTP
e de pasta pública no site. É por isso que o Facebook costuma ficar pronto
antes do Instagram.

    Instagram: sobe para o site -> manda a URL -> a Meta baixa
    Facebook:  manda o arquivo -> pronto

USO
    python3 publicar_facebook.py PASTA_DA_PECA

    A pasta é a mesma do Instagram: os três PNGs e o legenda.txt.
    Se existir legenda_facebook.txt, ele usa essa no lugar — e é o certo,
    porque no Facebook o link é clicável e a hashtag não serve de nada.

CONFIGURAÇÃO — no mesmo config_publicacao.json, um bloco novo:

    "facebook": {
      "page_id": "123456789",
      "page_token": "EAA..."
    }

O page_token é o token DA PÁGINA, não o do usuário. Sai de:
    GET /me/accounts   -> campo access_token de cada página

ESSE ARQUIVO GUARDA SEGREDO. Não versionar, não colar em conversa, não
mandar para ninguém. O script lê e nunca imprime o conteúdo.
"""

import json
import re
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://graph.facebook.com/v21.0"


def log(msg):
    print(f"[facebook] {msg}", flush=True)


# ---------------------------------------------------------------- utilidades

def carregar_config(raiz):
    p = os.path.join(raiz, "config_publicacao.json")
    if not os.path.exists(p):
        sys.exit(f"ERRO: falta {p}. Veja o cabeçalho deste arquivo.")
    with open(p, encoding="utf-8") as f:
        cfg = json.load(f)
    fb = cfg.get("facebook")
    if not fb:
        sys.exit("ERRO: config_publicacao.json sem o bloco 'facebook'. "
                 "A publicação no Facebook ainda não foi configurada.")
    if not fb.get("page_id") or str(fb["page_id"]).startswith("COLE_AQUI"):
        sys.exit("ERRO: bloco 'facebook' sem 'page_id'.")

    # O page_token e a fonte historica de erro: e facil colar o token do
    # USUARIO no lugar do token da PAGINA, e a Meta responde com o codigo 200
    # "Unpublished posts must be posted to a page as the page itself", que nao
    # diz o que fazer. A partir daqui o script resolve isso sozinho: ele
    # confere de quem e o token e, sendo do usuario, troca pelo da Pagina.
    fb["page_token"] = resolver_page_token(cfg, fb)
    return fb


def _quem_e(token):
    """Devolve ('PAGE'|'USER'|None, nome). Nao imprime o token."""
    try:
        d = pega("debug_token", {"input_token": token, "access_token": token})
        info = d.get("data", {})
        return info.get("type"), info.get("profile_id")
    except Exception:
        return None, None


def resolver_page_token(cfg, fb):
    candidato = str(fb.get("page_token") or "")
    if candidato and not candidato.startswith("COLE_AQUI"):
        tipo, _ = _quem_e(candidato)
        if tipo == "PAGE":
            return candidato
        print("[facebook] o page_token do arquivo e do USUARIO, nao da Pagina."
              " Buscando o da Pagina...")
    else:
        print("[facebook] page_token nao preenchido. Buscando o da Pagina...")

    base = str(cfg.get("access_token") or "")
    if not base or base.startswith("COLE_AQUI"):
        base = candidato
    if not base or base.startswith("COLE_AQUI"):
        sys.exit("ERRO: nenhum token utilizavel no arquivo. Preencha "
                 "'access_token' com o SEU token de usuario.")

    try:
        d = pega("me/accounts", {"fields": "id,access_token",
                                 "access_token": base, "limit": "100"})
    except Exception as e:
        sys.exit(f"ERRO ao listar as Paginas: {e}")

    alvo = str(fb["page_id"])
    for pag in d.get("data", []):
        if str(pag.get("id")) == alvo:
            print("[facebook] token da Pagina obtido automaticamente.")
            return pag["access_token"]

    sys.exit(f"ERRO: a Pagina {alvo} nao aparece entre as suas. "
             "Confira o page_id, ou gere um token novo com pages_show_list.")



def pega(caminho, params):
    """GET simples na Graph API. Levanta excecao com a mensagem da Meta."""
    url = f"{API}/{caminho}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(erro_meta(e))


def erro_meta(e):
    try:
        corpo = json.loads(e.read().decode())
        m = corpo.get("error", {})
        return f"{m.get('type')} {m.get('code')}: {m.get('message')}"
    except Exception:
        return str(e)


def multipart(campos, arquivo_campo, caminho):
    """Monta um corpo multipart/form-data à mão, sem dependência externa."""
    limite = f"----integrajud{uuid.uuid4().hex}"
    linhas = []
    for k, v in campos.items():
        linhas.append(f"--{limite}\r\n"
                      f'Content-Disposition: form-data; name="{k}"\r\n\r\n'
                      f"{v}\r\n".encode())
    nome = os.path.basename(caminho)
    tipo = mimetypes.guess_type(nome)[0] or "application/octet-stream"
    linhas.append(f"--{limite}\r\n"
                  f'Content-Disposition: form-data; name="{arquivo_campo}"; '
                  f'filename="{nome}"\r\n'
                  f"Content-Type: {tipo}\r\n\r\n".encode())
    with open(caminho, "rb") as f:
        linhas.append(f.read())
    linhas.append(f"\r\n--{limite}--\r\n".encode())
    return b"".join(linhas), f"multipart/form-data; boundary={limite}"


# ------------------------------------------------------------------ publicar

def subir_foto(fb, caminho):
    """Sobe a foto SEM publicar e devolve o id, para virar anexo do post."""
    corpo, content_type = multipart(
        {"published": "false", "access_token": fb["page_token"]},
        "source", caminho)
    req = urllib.request.Request(f"{API}/{fb['page_id']}/photos", data=corpo)
    req.add_header("Content-Type", content_type)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())["id"]


def publicar_post(fb, ids, legenda):
    campos = {"message": legenda, "access_token": fb["page_token"]}
    for i, mid in enumerate(ids):
        campos[f"attached_media[{i}]"] = json.dumps({"media_fbid": mid})
    dados = urllib.parse.urlencode(campos).encode()
    req = urllib.request.Request(f"{API}/{fb['page_id']}/feed", data=dados)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())["id"]


def legenda_da_pasta(pasta):
    """legenda_facebook.txt tem prioridade; senão adapta a do Instagram."""
    fb_txt = os.path.join(pasta, "legenda_facebook.txt")
    if os.path.exists(fb_txt):
        return open(fb_txt, encoding="utf-8").read().strip(), "legenda_facebook.txt"

    ig_txt = os.path.join(pasta, "legenda.txt")
    if not os.path.exists(ig_txt):
        return "", "nenhuma"

    linhas = open(ig_txt, encoding="utf-8").read().splitlines()
    # tira o bloco de hashtags: no Facebook não serve para nada
    limpas = [l for l in linhas if not l.strip().startswith("#")]
    texto = "\n".join(limpas).rstrip()
    log("adaptei a legenda do Instagram: hashtags removidas. "
        "O ideal é escrever uma legenda_facebook.txt com o link no CTA.")
    return texto, "legenda.txt adaptada"


# ---------------------------------------------------------------------- main

def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 publicar_facebook.py PASTA_DA_PECA")

    pasta = os.path.abspath(sys.argv[1])
    if not os.path.isdir(pasta):
        sys.exit(f"ERRO: pasta não encontrada: {pasta}")
    raiz = os.path.dirname(pasta)

    # SO OS SLIDES DA PECA — correcao de 18/08/2026.
    # Antes daqui saia `todo .png da pasta`, e isso publicou um carrossel de
    # SEIS imagens na GKFD: o story_916.png, que o extras.py grava na mesma
    # pasta, entrou como sexto slide, esticado no formato 4:5. Slide de peca
    # sempre termina em _<numero>.png; story, reel e qualquer outro arquivo
    # ficam de fora por construcao, e a ordem passa a ser NUMERICA e nao
    # alfabetica (com dez ou mais slides, _10 vinha antes de _2).
    def _num(nome):
        # story_916.png TAMBEM termina em _<numero>.png — a primeira versao
        # desta correcao caiu nessa e deixou o story passar de novo. Slide de
        # peca e numerado de 1 a 20 e nao carrega 'story' nem 'reel' no nome;
        # arquivos internos comecam com sublinhado.
        base = os.path.basename(nome).lower()
        if base.startswith("_") or "story" in base or "reel" in base:
            return None
        m = re.search(r"_(\d+)\.png$", base)
        if not m:
            return None
        n = int(m.group(1))
        return n if 1 <= n <= 20 else None

    pngs = sorted((f for f in os.listdir(pasta) if _num(f) is not None),
                  key=_num)
    _fora = [f for f in os.listdir(pasta)
             if f.lower().endswith(".png") and _num(f) is None]
    if _fora:
        print("[publicar] fora do carrossel (nao sao slides): %s"
              % ", ".join(sorted(_fora)))
    if not pngs:
        sys.exit("ERRO: nenhuma imagem na pasta.")
    if len(pngs) > 10:
        sys.exit("ERRO: no máximo 10 imagens por post.")
    caminhos = [os.path.join(pasta, n) for n in pngs]

    for c in caminhos:
        mb = os.path.getsize(c) / 1048576
        if mb > 10:
            sys.exit(f"ERRO: {os.path.basename(c)} tem {mb:.1f} MB. O limite é 10 MB.")

    legenda, origem = legenda_da_pasta(pasta)
    fb = carregar_config(raiz)

    log(f"{len(caminhos)} imagens · legenda de {origem} "
        f"({len(legenda)} caracteres)")

    try:
        ids = []
        for c in caminhos:
            ids.append(subir_foto(fb, c))
            log(f"enviada: {os.path.basename(c)}")
        post_id = publicar_post(fb, ids, legenda)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO da Meta: {erro_meta(e)}")

    log(f"PUBLICADO na Página. id do post: {post_id}")
    print(post_id)


if __name__ == "__main__":
    main()
